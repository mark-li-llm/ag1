#!/usr/bin/env python3
import os
import json
import glob
import argparse

from _qa_common import qa_logger, write_report
from _common import read_json, load_yaml


def main():
    ap = argparse.ArgumentParser(description='QA: SEC section validation (Items order and presence)')
    ap.add_argument('--norm-glob', default='data/interim/normalized/*.json')
    ap.add_argument('--cfg', default='qa_configs/qa.sec.sections.yaml')
    ap.add_argument('--out', default='qa_data/outputs/sec_section_report.json')
    args = ap.parse_args()

    logger, log_path = qa_logger('qa_sec_section_validate')
    req = load_yaml(args.cfg).get('required_items', [])
    docs = [read_json(p) for p in glob.glob(args.norm_glob)]

    total = 0
    pass_count = 0
    examples = []

    for d in docs:
        if d.get('source_domain') != 'sec.gov':
            continue
        if d.get('doctype') not in ('10-K', '10-Q'):
            continue
        total += 1
        spans = d.get('sec_spans') or []
        labels = [s.get('section') for s in spans]
        ok_present = all(x in labels for x in req)
        ok_order = True
        if ok_present:
            indices = [labels.index(x) for x in req]
            ok_order = indices == sorted(indices)
        ok = ok_present and ok_order
        pass_count += 1 if ok else 0
        if not ok and len(examples) < 20:
            examples.append({'doc_id': d.get('doc_id'), 'labels': labels})

    report = {
        'total_sec_docs': total,
        'pass': pass_count,
        'pass_pct': round((pass_count/max(1,total)), 4),
        'examples': examples,
        'log_path': log_path,
    }
    write_report(args.out, report)
    logger.info(f"SEC section pass {pass_count}/{total}")


if __name__ == '__main__':
    main()
