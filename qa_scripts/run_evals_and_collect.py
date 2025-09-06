#!/usr/bin/env python3
# FILE: qa_scripts/run_evals_and_collect.py
# Purpose: Discover and run feasible eval/QA/verify entrypoints (esp. under qa_scripts/), 
# capture stdout/stderr/returncode without stopping on first error, and write a summary JSON.
# Standard library only.

import os, sys, json, subprocess, time, datetime, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # repo root
DIAG_DIR = ROOT / "diagnostics"
RUNS_DIR = DIAG_DIR / "runs"
ENV_DIR = DIAG_DIR / "environment"
RUNS_DIR.mkdir(parents=True, exist_ok=True)
ENV_DIR.mkdir(parents=True, exist_ok=True)

TS = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
SESSION_DIR = RUNS_DIR / f"run_{TS}"
SESSION_DIR.mkdir(parents=True, exist_ok=True)

TIMEOUT_PER_TASK = int(os.environ.get("DIAG_TIMEOUT_PER_TASK_SEC", "900"))  # 15 min
PYTHON = sys.executable

EXCLUDE_BASENAMES = {
    "run_evals_and_collect",   # this orchestrator
    "generate_code_md",        # created below
    "make_diagnostic_bundle",  # created below
}

def safe_cmd(cmd_list, cwd=None, timeout=TIMEOUT_PER_TASK, env=None):
    t0 = time.time()
    try:
        proc = subprocess.run(
            cmd_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cwd or ROOT,
            timeout=timeout,
            env=env or os.environ.copy(),
            text=True,
        )
        dt = int((time.time() - t0) * 1000)
        return {
            "status": "success" if proc.returncode == 0 else "runtime_error",
            "return_code": proc.returncode,
            "duration_ms": dt,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }
    except subprocess.TimeoutExpired as e:
        dt = int((time.time() - t0) * 1000)
        return {"status": "timeout", "return_code": None, "duration_ms": dt, "stdout": e.stdout or "", "stderr": e.stderr or ""}
    except FileNotFoundError as e:
        dt = int((time.time() - t0) * 1000)
        return {"status": "not_found", "return_code": None, "duration_ms": dt, "stdout": "", "stderr": str(e)}
    except Exception as e:
        dt = int((time.time() - t0) * 1000)
        return {"status": "exception", "return_code": None, "duration_ms": dt, "stdout": "", "stderr": repr(e)}

def detect_py_scripts():
    # Primary search in qa_scripts/, plus a few likely paths
    patterns = [
        "qa_scripts/qa_*.py",
        "qa_scripts/*eval*.py",
        "qa_scripts/*.py",
        "scripts/*eval*.py",
        "scripts/verify_day1_milestones.py",
        "scripts/link_health_check.py",
        "qa/*.py",
    ]
    candidates = []
    for pat in patterns:
        for p in ROOT.glob(pat):
            if p.is_file():
                base = p.stem
                if base in EXCLUDE_BASENAMES:
                    continue
                candidates.append(p)
    # de-dup
    seen = set(); uniq = []
    for p in candidates:
        sp = str(p.resolve())
        if sp not in seen:
            uniq.append(p)
            seen.add(sp)
    return uniq

def check_module_available(mod_name):
    code = f"import importlib,sys; sys.exit(0 if importlib.util.find_spec('{mod_name}') else 3)"
    rc = subprocess.run([PYTHON, "-c", code]).returncode
    return rc == 0

def run_python_script(script_path: Path):
    name = script_path.stem
    out_dir = SESSION_DIR / f"py_{name}"
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1st try: with --dry-run (if script supports)
    res = safe_cmd([PYTHON, str(script_path), "--dry-run"], cwd=ROOT)
    # If CLI complains about "--dry-run", try no-arg run
    needs_retry_noarg = False
    comb = (res.get("stderr","") + "\n" + res.get("stdout",""))
    lc = comb.lower()
    if ("unrecognized arguments" in lc) or ("usage:" in lc and "--dry-run" in lc and res["return_code"] != 0):
        needs_retry_noarg = True

    if needs_retry_noarg:
        res = safe_cmd([PYTHON, str(script_path)], cwd=ROOT)

    # Persist logs
    (out_dir / "stdout.txt").write_text(res.get("stdout",""), errors="replace")
    (out_dir / "stderr.txt").write_text(res.get("stderr",""), errors="replace")

    # Parse missing deps
    missing_deps = []
    for line in (res.get("stderr","") + "\n" + res.get("stdout","")).splitlines():
        m = re.search(r"(ModuleNotFoundError|No module named)\:?\s+['\"]?([A-Za-z0-9_\-\.]+)", line)
        if m:
            missing_deps.append(m.group(2))

    return {
        "type": "python",
        "name": name,
        "path": str(script_path),
        "status": res["status"],
        "return_code": res["return_code"],
        "duration_ms": res["duration_ms"],
        "stdout_path": str(out_dir / "stdout.txt"),
        "stderr_path": str(out_dir / "stderr.txt"),
        "missing_dependencies": sorted(set(missing_deps)),
    }

def main():
    summary = {
        "session": TS,
        "root": str(ROOT),
        "python": sys.version,
        "results": [],
        "errors": [],
    }

    # Save environment basics
    env_info = {
        "python_version": sys.version,
        "executable": sys.executable,
        "platform": sys.platform,
        "cwd": str(ROOT),
    }
    (ENV_DIR / "env.json").write_text(json.dumps(env_info, indent=2))

    # Try pip freeze (best effort)
    pf = safe_cmd([PYTHON, "-m", "pip", "freeze"])
    (ENV_DIR / "pip_freeze.txt").write_text((pf.get("stdout") or "")[:200000], errors="replace")

    # Discover and run
    py_scripts = detect_py_scripts()
    for ps in py_scripts:
        try:
            res = run_python_script(ps)
            summary["results"].append(res)
        except Exception as e:
            summary["errors"].append({"stage":"run_python_script", "path":str(ps), "error":repr(e)})

    # Persist summary
    (SESSION_DIR / "summary.json").write_text(json.dumps(summary, indent=2))
    (RUNS_DIR / "summary.latest.json").write_text(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()

