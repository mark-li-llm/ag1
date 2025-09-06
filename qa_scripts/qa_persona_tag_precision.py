#!/usr/bin/env python3
import os
import json
import glob
import argparse

from _qa_common import qa_logger, write_report
from _common import read_json, load_yaml


def main():
    ap = argparse.ArgumentParser(description='QA: Persona tag precision audit')
    ap.add_argument('--norm-glob', default='data/interim/normalized/*.json')
    ap.add_argument('--prompts', default='configs/eval.prompts.yaml')
    ap.add_argument('--out', default='qa_data/outputs/persona_tag_precision.json')
    args = ap.parse_args()

    logger, log_path = qa_logger('qa_persona_tag_precision')
    docs = [read_json(p) for p in glob.glob(args.norm_glob)]
    cfg = load_yaml(args.prompts)

    persona_kws = {p: set([k.lower() for k in meta.get('keywords', [])]) for p, meta in (cfg.get('personas') or {}).items()}

    counts = {p: {'tp': 0, 'total': 0} for p in persona_kws.keys()}
    examples = []

    for d in docs:
        tags = d.get('persona_tags') or []
        if not tags:
            continue
        text = (d.get('text') or '').lower()
        for tag in tags:
            if tag not in counts:
                counts[tag] = {'tp': 0, 'total': 0}
            counts[tag]['total'] += 1
            kws = persona_kws.get(tag, set())
            hit = any(kw in text for kw in kws) if kws else False
            counts[tag]['tp'] += 1 if hit else 0
            if not hit and len(examples) < 30:
                examples.append({'doc_id': d.get('doc_id'), 'persona': tag, 'missing_keywords': list(kws)[:5]})

    precision = {p: (v['tp'] / v['total'] if v['total'] else None) for p, v in counts.items()}
    report = {
        'precision_by_persona': precision,
        'counts': counts,
        'examples': examples,
        'log_path': log_path,
    }
    write_report(args.out, report)
    logger.info(f"Persona precision computed for {len(precision)} personas -> {args.out}")


if __name__ == '__main__':
    main()
