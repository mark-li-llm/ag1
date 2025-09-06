#!/usr/bin/env python3
import os
import json
import glob
import argparse
from collections import Counter

from _qa_common import qa_logger, write_report, load_chunks_from_jsonl


def main():
    ap = argparse.ArgumentParser(description='QA: Eval seed integrity checks')
    ap.add_argument('--eval-path', default='data/interim/eval/salesforce_eval_seed.jsonl')
    ap.add_argument('--chunks-glob', default='data/interim/chunks/*.chunks.jsonl')
    ap.add_argument('--out', default='qa_data/outputs/eval_seed_report.json')
    args = ap.parse_args()

    logger, log_path = qa_logger('qa_eval_seed_validate')
    evals = []
    if os.path.exists(args.eval_path):
        for line in open(args.eval_path, 'r', encoding='utf-8'):
            if line.strip():
                try:
                    evals.append(json.loads(line))
                except Exception:
                    pass

    # Load chunks index
    chunk_map = {}
    for f in glob.glob(args.chunks_glob):
        for ch in load_chunks_from_jsonl(f):
            chunk_map[ch['chunk_id']] = ch

    ok = 0
    fails = []
    persona_counts = Counter()
    type_counts = Counter()

    for e in evals:
        cid = e.get('expected_chunk_id')
        ch = chunk_map.get(cid)
        exists = ch is not None
        key_ok = False
        if ch:
            text = ch.get('text', '')
            keyphrases = e.get('expected_answer_keyphrases') or []
            key_ok = all(k in text for k in keyphrases)
        if exists and key_ok:
            ok += 1
            persona_counts[e.get('persona')] += 1
            type_counts[e.get('source_type')] += 1
        else:
            fails.append({'eval_id': e.get('eval_id'), 'reason': 'missing_chunk' if not exists else 'missing_keyphrases'})

    report = {
        'total_eval_pairs': len(evals),
        'valid_pairs': ok,
        'valid_pct': round((ok/max(1, len(evals))), 4),
        'failures': fails[:100],
        'persona_dist': dict(persona_counts),
        'source_type_dist': dict(type_counts),
        'log_path': log_path,
    }
    write_report(args.out, report)
    logger.info(f"Eval seed integrity: {ok}/{len(evals)} valid -> {args.out}")


if __name__ == '__main__':
    main()

