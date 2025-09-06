#!/usr/bin/env python3
# FILE: qa_scripts/make_diagnostic_bundle.py
# Purpose: Aggregate run summaries, environment snapshot, dataset stats into diagnostics/diagnostic_bundle.json
# Standard library only.

import os, sys, json, csv
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
OUT_JSON = ROOT / "diagnostics" / "diagnostic_bundle.json"
RUNS_DIR = ROOT / "diagnostics" / "runs"
ENV_DIR = ROOT / "diagnostics" / "environment"

def read_json(p: Path, default=None):
    try:
        return json.loads(p.read_text())
    except Exception:
        return default

def csv_rows(p: Path):
    try:
        with p.open(newline="", encoding="utf-8", errors="replace") as f:
            return max(0, sum(1 for _ in csv.reader(f)) - 1)
    except Exception:
        return None

def try_read_text(p: Path, max_chars=20000):
    try:
        return p.read_text(errors="replace")[:max_chars]
    except Exception:
        return None

def latest_run_summary():
    latest = RUNS_DIR / "summary.latest.json"
    if latest.exists():
        return read_json(latest, {"results": [], "errors": []})
    runs = sorted(RUNS_DIR.glob("run_*/summary.json"))
    if runs:
        return read_json(runs[-1], {"results": [], "errors": []})
    return {"results": [], "errors": []}

def gather_env():
    env = read_json(ENV_DIR / "env.json", {})
    pip = try_read_text(ENV_DIR / "pip_freeze.txt", 20000)
    env["pip_freeze_excerpt"] = pip
    return env

def gather_dataset():
    inv = ROOT / "data" / "final" / "inventory" / "salesforce_inventory.csv"
    day1 = ROOT / "data" / "final" / "reports" / "day1_verification.json"
    link = ROOT / "data" / "final" / "reports" / "link_health.json"
    dedup = ROOT / "data" / "interim" / "dedup" / "dedup_map.json"
    eval_seed = ROOT / "data" / "interim" / "eval" / "salesforce_eval_seed.jsonl"

    ds = {
        "inventory_rows": csv_rows(inv) if inv.exists() else None,
        "day1_verification": read_json(day1, {}),
        "link_health": read_json(link, {}),
        "dedup_map_present": dedup.exists(),
        "eval_seed_count": None,
    }
    if eval_seed.exists():
        try:
            ds["eval_seed_count"] = sum(1 for _ in eval_seed.open("r", encoding="utf-8", errors="replace"))
        except Exception:
            ds["eval_seed_count"] = None
    return ds

def auto_flags(ds):
    flags = []
    vr = ds.get("day1_verification", {})
    inv_rows = ds.get("inventory_rows")
    if inv_rows is not None and inv_rows < 80:
        flags.append({"id":"low_inventory_rows", "level":"error", "value":inv_rows, "threshold":80})

    # duplicate rate if we have fields
    if isinstance(vr, dict) and "duplicates_removed" in vr and "chunks_total" in vr:
        try:
            dr = vr["duplicates_removed"]/max(1, vr["chunks_total"]) * 100.0
            if dr > 15.0:
                flags.append({"id":"duplicate_rate_above_15pct", "level":"warn", "value":round(dr,2), "threshold":15.0})
        except Exception:
            pass

    # link health
    link = ds.get("link_health", {})
    # Compute ok % robustly from structures we see in this repo
    try:
        summary = None
        if isinstance(link, dict):
            if isinstance(link.get("summary"), list):
                summary = link.get("summary")
        elif isinstance(link, list):
            summary = link
        if summary is not None:
            total = len(summary)
            ok = sum(1 for r in summary if isinstance(r, dict) and int(r.get("status", 0)) == 200)
            ok_pct_calc = (ok / total * 100.0) if total else None
            if ok_pct_calc is not None and ok_pct_calc < 100.0:
                flags.append({"id":"link_health_below_100", "level":"error", "value":round(ok_pct_calc,2), "threshold":100.0})
    except Exception:
        pass

    return flags

def main():
    bundle = {
        "generated_at_utc": datetime.utcnow().isoformat() + "Z",
        "root": str(ROOT),
        "artifacts": {
            "code_md": "code.md",
            "runs_dir": "diagnostics/runs/",
            "env_dir": "diagnostics/environment/"
        },
        "environment": gather_env(),
        "dataset": gather_dataset(),
        "eval_runs": latest_run_summary(),
    }
    bundle["auto_flags"] = auto_flags(bundle["dataset"])

    # Pointers to key files if present
    pointers = []
    for rel in [
        "data/final/inventory/salesforce_inventory.csv",
        "data/final/reports/day1_verification.json",
        "data/final/reports/link_health.json",
        "data/interim/dedup/dedup_map.json",
        "data/interim/eval/salesforce_eval_seed.jsonl",
    ]:
        if (ROOT / rel).exists():
            pointers.append(rel)
    bundle["present_key_files"] = pointers

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(bundle, indent=2))

if __name__ == "__main__":
    main()
