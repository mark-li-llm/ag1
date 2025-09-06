#!/usr/bin/env python3
import os
import glob
import json
import argparse
from datetime import date, timedelta

from _common import setup_logger, read_json, make_inventory_row, ensure_parent


def main():
    ap = argparse.ArgumentParser(description='Compute Day-1 verification metrics and write inventory.')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--limit', type=int, default=999999)
    ap.add_argument('--since', type=str, default=None)
    ap.add_argument('--until', type=str, default=None)
    ap.add_argument('--concurrency', type=int, default=4)
    args = ap.parse_args()

    logger, log_path = setup_logger('eval')
    norm_dir = os.path.join('data', 'interim', 'normalized')
    docs_all = [read_json(p) for p in glob.glob(os.path.join(norm_dir, '*.json'))[: args.limit]]
    # Exclude investor hub domain to avoid WAF and low-content hubs
    docs = [d for d in docs_all if d.get('source_domain') != 'investor.salesforce.com']

    # Inventory CSV
    inv_path = os.path.join('data', 'final', 'inventory', 'salesforce_inventory.csv')
    ensure_parent(inv_path)
    header = ['doc_id', 'company', 'doctype', 'title', 'publish_date', 'url', 'final_url', 'source_domain', 'section', 'topic', 'persona_tags', 'language', 'word_count', 'token_count', 'ingestion_ts', 'hash_sha256']
    inv_rows = [','.join(header)]
    for d in docs:
        inv_rows.append(','.join(make_inventory_row(d)))
    if not args.dry_run:
        with open(inv_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(inv_rows) + '\n')

    # Dedup map
    dedup_path = os.path.join('data', 'interim', 'dedup', 'dedup_map.json')
    duplicates_removed = 0
    if os.path.exists(dedup_path):
        dm = read_json(dedup_path)
        duplicates_removed = sum(len(g.get('duplicate_chunk_ids', [])) for g in dm.get('groups', []))

    # Chunk counts
    chunks_dir = os.path.join('data', 'interim', 'chunks')
    chunks_total = 0
    for p in glob.glob(os.path.join(chunks_dir, '*.chunks.jsonl')):
        with open(p, 'r', encoding='utf-8') as f:
            chunks_total += sum(1 for _ in f)

    # Link health
    link_ok = sum(1 for d in docs if d.get('link_ok'))
    link_ok_pct = (link_ok / len(docs)) if docs else 0.0

    # By doctype/source counts
    by_doctype = {}
    by_domain = {}
    for d in docs:
        by_doctype[d.get('doctype', '')] = by_doctype.get(d.get('doctype', ''), 0) + 1
        by_domain[d.get('source_domain', '')] = by_domain.get(d.get('source_domain', ''), 0) + 1

    # PR docs in last 12 months
    today = date.today()
    last12 = today - timedelta(days=365)
    pr_docs_last_12mo = 0
    for d in docs:
        if d.get('doctype') == 'press':
            try:
                y, m, dd = d.get('publish_date', '1900-01-01').split('-')
                docd = date(int(y), int(m), int(dd))
                if docd >= last12:
                    pr_docs_last_12mo += 1
            except Exception:
                pass

    report = {
        'total_docs': len(docs),
        'docs_with_dates': sum(1 for d in docs if d.get('publish_date')),
        'chunks_total': chunks_total,
        'duplicates_removed': int(duplicates_removed),
        'link_ok_pct': round(link_ok_pct, 4),
        'by_doctype_counts': by_doctype,
        'by_source_domain_counts': by_domain,
        'pr_docs_last_12mo': pr_docs_last_12mo,
    }
    report_path = os.path.join('data', 'final', 'reports', 'day1_verification.json')
    ensure_parent(report_path)
    if not args.dry_run:
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)

    logger.info(f"Verification report written. Log: {log_path}")


if __name__ == '__main__':
    main()
