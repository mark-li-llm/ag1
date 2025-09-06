#!/usr/bin/env python3
import os
import csv
import glob
import json
import random
import argparse
from collections import defaultdict

from _qa_common import qa_logger
from _common import read_json


def main():
    ap = argparse.ArgumentParser(description='QA: Build manual review samples for docs and chunks')
    ap.add_argument('--norm-glob', default='data/interim/normalized/*.json')
    ap.add_argument('--chunks-glob', default='data/interim/chunks/*.chunks.jsonl')
    ap.add_argument('--reports-root', default='qa_data/outputs')
    ap.add_argument('--out-docs', default='qa_data/samples/manual_review_samples/docs_for_review.csv')
    ap.add_argument('--out-chunks', default='qa_data/samples/manual_review_samples/chunks_for_review.csv')
    args = ap.parse_args()

    logger, log_path = qa_logger('qa_manual_samples')
    os.makedirs(os.path.dirname(args.out_docs), exist_ok=True)

    docs = [read_json(p) for p in glob.glob(args.norm_glob)]
    by_dt = defaultdict(list)
    for d in docs:
        by_dt[d.get('doctype','unknown')].append(d)

    # ingest failures from reports if present
    fails = set()
    def add_fails(report_name, key):
        p = os.path.join(args.reports_root, report_name)
        if os.path.exists(p):
            try:
                obj = json.load(open(p, 'r', encoding='utf-8'))
                for ex in obj.get(key, []):
                    did = ex.get('doc_id') or ex.get('chunk_id') or ''
                    if did:
                        fails.add(did.split('::')[0])
            except Exception:
                pass

    add_fails('schema_report.json', 'examples')
    add_fails('text_quality_report.json', 'examples')

    random.seed(42)
    doc_rows = [['doc_id','doctype','title','publish_date','url','flags']]
    for dt, arr in by_dt.items():
        sample = random.sample(arr, min(5, len(arr)))
        for d in sample:
            flags = []
            if d.get('doc_id') in fails:
                flags.append('failing')
            doc_rows.append([d.get('doc_id'), d.get('doctype'), d.get('title'), d.get('publish_date'), d.get('url'), '|'.join(flags)])

    with open(args.out_docs, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerows(doc_rows)

    # chunks sample: pick first chunk per selected doc
    chunk_rows = [['chunk_id','doc_id','text_snippet','local_heads','overlap_prev','overlap_next','dup_status']]
    # optional: not computing actual overlaps here; placeholder N/A
    for row in doc_rows[1:]:
        did = row[0]
        chunk_file = os.path.join('data','interim','chunks', f'{did}.chunks.jsonl')
        if os.path.exists(chunk_file):
            line = open(chunk_file, 'r', encoding='utf-8').readline()
            if line:
                try:
                    rec = json.loads(line)
                    snippet = (rec.get('text','')[:400]).replace('\n',' ')
                    chunk_rows.append([rec.get('chunk_id'), rec.get('doc_id'), snippet, ';'.join(rec.get('local_heads') or []), 'NA','NA','unknown'])
                except Exception:
                    pass

    with open(args.out_chunks, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerows(chunk_rows)

    logger.info(f"Manual review samples: {len(doc_rows)-1} docs, {len(chunk_rows)-1} chunks")


if __name__ == '__main__':
    main()
