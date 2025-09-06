#!/usr/bin/env python3
import os
import json
import argparse

from _qa_common import qa_logger, write_report


def load(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    try:
        return json.load(open(path, 'r', encoding='utf-8'))
    except Exception:
        return {}


def main():
    ap = argparse.ArgumentParser(description='QA: Regression pack comparator (critical subset)')
    ap.add_argument('--prev-root', default='qa_data/outputs_prev')
    ap.add_argument('--curr-root', default='qa_data/outputs')
    ap.add_argument('--out', default='qa_data/outputs/regression_pack.json')
    args = ap.parse_args()

    logger, log_path = qa_logger('qa_regression_pack')
    keys = ['schema_report.json', 'metadata_report.json', 'text_quality_report.json', 'chunk_quality_report.json', 'coverage_report.json']
    diffs = []
    for k in keys:
        prev = load(os.path.join(args.prev_root, k))
        curr = load(os.path.join(args.curr_root, k))
        if not prev or not curr:
            continue
        diffs.append({'report': k, 'prev_keys': sorted(list(prev.keys()))[:10], 'curr_keys': sorted(list(curr.keys()))[:10]})

    out = {
        'compared_reports': len(diffs),
        'diffs': diffs,
        'log_path': log_path,
    }
    write_report(args.out, out)
    logger.info(f"Regression pack compared {len(diffs)} reports -> {args.out}")


if __name__ == '__main__':
    main()

