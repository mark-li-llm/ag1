#!/usr/bin/env python3
import os
import json
import argparse
from typing import Dict, Any

from _qa_common import (
    qa_logger, list_json_files, write_report, printable_ratio,
    count_replacement_char, stopword_ratio, char_bigram_entropy
)
from _common import read_json


def main():
    ap = argparse.ArgumentParser(description='QA: Text quality & garble detection')
    ap.add_argument('--input-glob', default='data/interim/normalized/*.json')
    ap.add_argument('--chunks-glob', default='data/interim/chunks/*.chunks.jsonl')
    ap.add_argument('--limit', type=int, default=None)
    ap.add_argument('--out', default='qa_data/outputs/text_quality_report.json')
    ap.add_argument('--fail-on', default='auto')
    args = ap.parse_args()

    logger, log_path = qa_logger('qa_text_quality')
    paths = list_json_files(args.input_glob, args.limit)

    total = 0
    doc_ok = 0
    repchar_free = 0
    examples = []
    doc_metrics = []

    for p in paths:
        d = read_json(p)
        text = d.get('text', '')
        total += 1
        pr = printable_ratio(text)
        rc = count_replacement_char(text)
        words = text.split()
        swr = stopword_ratio(words)
        ent = char_bigram_entropy(text[:20000])  # cap for speed
        ok = (pr >= 0.995) and (rc == 0) and (0.25 <= swr <= 0.65) and (2.5 <= ent <= 5.0)
        repchar_free += 1 if rc == 0 else 0
        doc_ok += 1 if ok else 0
        if not ok and len(examples) < 50:
            examples.append({'doc_id': d.get('doc_id'), 'printable_ratio': pr, 'replacement_chars': rc, 'stopword_ratio': swr, 'bigram_entropy': ent})
        doc_metrics.append({'doc_id': d.get('doc_id'), 'printable_ratio': pr, 'replacement_chars': rc, 'stopword_ratio': swr, 'bigram_entropy': ent})

    report = {
        'total_docs': total,
        'docs_quality_ok': doc_ok,
        'docs_quality_ok_pct': round((doc_ok/total) if total else 0.0, 4),
        'replacement_char_free_docs_pct': round((repchar_free/total) if total else 0.0, 4),
        'examples': examples,
        'log_path': log_path,
    }
    write_report(args.out, report)
    logger.info(f"Text quality OK {doc_ok}/{total} -> {args.out}")


if __name__ == '__main__':
    main()
