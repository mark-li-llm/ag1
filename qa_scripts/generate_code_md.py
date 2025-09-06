#!/usr/bin/env python3
# FILE: qa_scripts/generate_code_md.py
# Purpose: Summarize repo structure, key modules, configs, entrypoints into code.md
# Standard library only.

import os, sys, re, ast
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = ROOT / "code.md"

SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", "data/raw"}
INCLUDE_DIRS = ["scripts", "qa_scripts", "configs", "qa_configs", "data", "diagnostics", "tests", "notebooks", "eval"]

def list_tree(base: Path, max_depth=3):
    lines = []
    def walk(p: Path, depth=0):
        if depth > max_depth: return
        try:
            entries = sorted(p.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
        except Exception:
            return
        for e in entries:
            if e.name in SKIP_DIRS: continue
            rel = e.relative_to(base)
            prefix = "  " * depth + ("├─ " if depth>0 else "")
            if e.is_dir():
                lines.append(f"{prefix}{rel.name}/")
                walk(e, depth+1)
            else:
                lines.append(f"{prefix}{rel.name}")
    walk(base, 0)
    return "\n".join(lines)

def summarize_python_file(p: Path):
    info = {"path": str(p), "imports": [], "functions": [], "classes": [], "has_main": False, "cli_flags": []}
    try:
        src = p.read_text(errors="replace")
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names: info["imports"].append(n.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module: info["imports"].append(node.module)
            elif isinstance(node, ast.FunctionDef):
                info["functions"].append(node.name)
            elif isinstance(node, ast.ClassDef):
                info["classes"].append(node.name)
        info["has_main"] = bool(re.search(r'if __name__\s*==\s*[\'\"]__main__[\'\"]', src))
        flags = re.findall(r'add_argument\(\s*[\'\"](--[A-Za-z0-9_\-]+)', src)
        info["cli_flags"] = sorted(set(flags))
    except Exception as e:
        info["error"] = repr(e)
    return info

def collect_configs():
    cfgs = []
    for d in ["configs", "qa_configs"]:
        dp = ROOT / d
        if dp.exists():
            for p in dp.rglob("*"):
                if p.is_file() and p.suffix.lower() in {".yaml", ".yml", ".json"}:
                    try:
                        text = p.read_text(errors="replace")
                        keys = re.findall(r'^\s*([A-Za-z0-9_\-]+)\s*:', text, flags=re.M)
                        cfgs.append({"path": str(p), "size_bytes": p.stat().st_size, "sample_keys": sorted(set(keys))[:20]})
                    except Exception as e:
                        cfgs.append({"path": str(p), "error": repr(e)})
    return cfgs

def main():
    now = datetime.utcnow().isoformat() + "Z"
    lines = []
    lines.append(f"# Repository Code Context\n_Generated: {now}_\n")
    lines.append("## Directory Tree (depth ≤ 3)\n")
    lines.append("```\n" + list_tree(ROOT, max_depth=3) + "\n```")

    lines.append("\n## Key Script Modules & Entry Points\n")
    py_files = []
    for d in ["scripts", "qa_scripts", "tools", "tests"]:
        dp = ROOT / d
        if dp.exists():
            py_files.extend([p for p in dp.rglob("*.py") if p.is_file()])
    for p in sorted(py_files, key=lambda x: str(x)):
        info = summarize_python_file(p)
        lines.append(f"### `{p}`")
        lines.append(f"- Imports: {', '.join(sorted(set(info.get('imports', [])))[:12])}")
        lines.append(f"- Functions: {', '.join(info.get('functions', [])[:12])}")
        lines.append(f"- Classes: {', '.join(info.get('classes', [])[:12])}")
        lines.append(f"- Entry point: {info.get('has_main')}")
        flags = info.get('cli_flags', [])
        if flags: lines.append(f"- CLI flags detected: {' '.join(flags)}")
        if "error" in info: lines.append(f"- Parse error: {info['error']}")
        lines.append("")

    lines.append("\n## Config Files Summary\n")
    for meta in collect_configs():
        if "error" in meta:
            lines.append(f"- `{meta['path']}` (error parsing: {meta['error']})")
        else:
            lines.append(f"- `{meta['path']}` (size: {meta['size_bytes']} bytes) sample keys: {', '.join(meta['sample_keys'])}")

    lines.append("\n## Data & Reports Present\n")
    known = [
        "data/final/inventory/salesforce_inventory.csv",
        "data/final/reports/day1_verification.json",
        "data/final/reports/link_health.json",
        "data/interim/dedup/dedup_map.json",
        "data/interim/eval/salesforce_eval_seed.jsonl",
    ]
    for k in known:
        p = ROOT / k
        status = "FOUND" if p.exists() else "MISSING"
        lines.append(f"- {k}: {status}")

    OUT_PATH.write_text("\n".join(lines), errors="replace")

if __name__ == "__main__":
    main()

