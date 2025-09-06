import os
import re
import json
import glob
import random
import logging
import sys
from datetime import datetime, date

from typing import Tuple, List, Dict, Any

# Ensure we can import pipeline common utilities without making scripts a package
THIS_DIR = os.path.dirname(__file__)
SCRIPTS_DIR = os.path.abspath(os.path.join(THIS_DIR, os.pardir, 'scripts'))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from _common import setup_logger, read_json, write_json, read_text, write_text, load_yaml, token_count


def qa_logger(script_name: str) -> Tuple[logging.Logger, str]:
    # Place QA logs under logs/qa/<script_name>/
    stage = f"qa/{script_name}"
    return setup_logger(stage)


def ensure_parent(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)


def write_report(out_path: str, obj: dict):
    ensure_parent(out_path)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)


def list_json_files(glob_pattern: str, limit: int | None = None) -> List[str]:
    files = sorted(glob.glob(glob_pattern))
    return files[: limit] if limit else files


def printable_ratio(s: str) -> float:
    if not s:
        return 1.0
    total = len(s)
    printable = sum(1 for c in s if c == '\n' or (32 <= ord(c) <= 126) or (ord(c) >= 160))
    return printable / max(1, total)


def count_replacement_char(s: str) -> int:
    return s.count('\ufffd')  # '�'


def stopword_ratio(words: List[str]) -> float:
    sw = {
        'the','and','is','in','to','of','a','for','that','on','as','with','are','was','by','it','be','or','an','this','from','at','we','our','you','your','their','have','has','will','can'
    }
    if not words:
        return 0.0
    w = [w.lower() for w in words if re.match(r"[a-zA-Z']+$", w)]
    if not w:
        return 0.0
    swc = sum(1 for x in w if x in sw)
    return swc / max(1, len(w))


def char_bigram_entropy(s: str) -> float:
    from math import log2
    if len(s) < 2:
        return 0.0
    counts: Dict[str, int] = {}
    total = 0
    for i in range(len(s) - 1):
        bg = s[i:i+2]
        counts[bg] = counts.get(bg, 0) + 1
        total += 1
    probs = [c / total for c in counts.values()]
    return -sum(p * log2(p) for p in probs)


def mean(xs: List[float]) -> float:
    return (sum(xs) / len(xs)) if xs else 0.0


def month_bucket(d: str | None) -> str:
    if not d or not re.match(r"\d{4}-\d{2}-\d{2}", d):
        return 'unknown'
    return d[:7]


def load_chunks_from_jsonl(path: str) -> List[dict]:
    lines = read_text(path).splitlines()
    recs = []
    for line in lines:
        if not line.strip():
            continue
        try:
            recs.append(json.loads(line))
        except Exception:
            continue
    return recs


def overlap_tokens(prev_text: str, cur_text: str, max_window: int = 200) -> int:
    # approximate overlap via suffix/prefix commonality on tokens
    def toks(s: str) -> List[str]:
        return re.findall(r"\w+", s)[-max_window:]
    a = toks(prev_text)
    b = re.findall(r"\w+", cur_text)[:max_window]
    # longest common suffix/prefix length
    m = 0
    for k in range(1, min(len(a), len(b)) + 1):
        if a[-k:] == b[:k]:
            m = k
        else:
            break
    return m


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    u = len(a | b)
    i = len(a & b)
    return i / u if u else 0.0


def shingles(words: List[str], k: int) -> set[str]:
    if len(words) < k:
        return set([' '.join(words)]) if words else set()
    return { ' '.join(words[i:i+k]) for i in range(0, len(words)-k+1) }


def normalize_for_shingles(text: str) -> List[str]:
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return [w for w in text.split() if w]

