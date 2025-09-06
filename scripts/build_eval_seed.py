#!/usr/bin/env python3
import os
import glob
import json
import argparse
import random
from datetime import date, timedelta

from _common import setup_logger, read_json, read_text, write_text


def pick_keyphrases(text: str, n: int = 3) -> list[str]:
    # pick distinct longer words (as a proxy for keyphrases)
    words = [w.strip('.,:;()"\'') for w in text.split() if len(w) >= 6]
    uniq = []
    seen = set()
    for w in words:
        lw = w.lower()
        if lw not in seen and any(c.isalpha() for c in lw):
            seen.add(lw)
            uniq.append(w)
        if len(uniq) >= n:
            break
    return uniq


def main():
    ap = argparse.ArgumentParser(description='Build retrieval-readiness eval seed set (query->chunk pairs).')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--limit', type=int, default=999999)
    ap.add_argument('--since', type=str, default=None)
    ap.add_argument('--until', type=str, default=None)
    ap.add_argument('--concurrency', type=int, default=4)
    args = ap.parse_args()

    logger, log_path = setup_logger('eval')
    chunks_dir = os.path.join('data', 'interim', 'chunks')
    filt_dir = os.path.join(chunks_dir, 'filtered')
    use_dir = filt_dir if os.path.isdir(filt_dir) else chunks_dir

    chunk_paths = glob.glob(os.path.join(use_dir, '*.chunks.jsonl'))[: args.limit]
    eval_items = []
    eid = 0
    random.seed(42)

    # Sample across files
    for p in chunk_paths:
        content = read_text(p)
        if not content.strip():
            continue
        lines = content.splitlines()
        if not lines or not lines[0].strip():
            continue
        # pick first chunk for simplicity
        try:
            rec = json.loads(lines[0])
        except Exception:
            continue
        text = rec['text']
        keyphrases = pick_keyphrases(text, n=3)
        if not keyphrases:
            continue
        persona = 'vp_sales_ops' if rec['metadata_snapshot'].get('doctype') == 'press' else 'cio'
        query = f"What does this document say about {keyphrases[0]}?"
        eid += 1
        eval_items.append({
            'eval_id': f'crm-eval-{str(eid).zfill(4)}',
            'persona': persona,
            'query_text': query,
            'expected_doc_id': rec['doc_id'],
            'expected_chunk_id': rec['chunk_id'],
            'expected_answer_keyphrases': keyphrases[:3],
            'source_type': rec['metadata_snapshot'].get('doctype'),
            'created_from_url': rec['metadata_snapshot'].get('url'),
            'label_date': rec['metadata_snapshot'].get('date'),
            'difficulty': 'easy',
            'notes': ''
        })
        if len(eval_items) >= 40:
            break

    out_path = os.path.join('data', 'interim', 'eval', 'salesforce_eval_seed.jsonl')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    content = '\n'.join(json.dumps(e, ensure_ascii=False) for e in eval_items) + ('\n' if eval_items else '')
    if args.dry_run:
        logger.info(f"[dry-run] Would write {out_path}")
    else:
        write_text(out_path, content)
    logger.info(f"Eval seed items: {len(eval_items)}. Log: {log_path}")


if __name__ == '__main__':
    main()
