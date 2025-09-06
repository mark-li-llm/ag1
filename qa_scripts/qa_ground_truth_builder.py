#!/usr/bin/env python3
import os
import re
import csv
import glob
import argparse
from typing import Dict, Any

from _qa_common import qa_logger, list_json_files, ensure_parent
from _common import read_json, read_text, parse_iso_date, date_to_iso, guess_title_from_html, parse_meta_published_time


def parse_filed_date_from_html(html: str) -> str | None:
    m = re.search(r'Filed\s*:?\s*([A-Za-z]{3,9}\s+\d{1,2},\s+\d{4})', html, re.I)
    if m:
        from scripts._common import parse_iso_date, date_to_iso
        return date_to_iso(parse_iso_date(m.group(1)))
    m = re.search(r'Filed\s*:?\s*(\d{4}-\d{2}-\d{2})', html)
    if m:
        return m.group(1)
    m = re.search(r'"filingDate"\s*:\s*"(\d{4}-\d{2}-\d{2})"', html)
    if m:
        return m.group(1)
    return None


def main():
    ap = argparse.ArgumentParser(description='QA: Build ground-truth baselines from raw artifacts')
    ap.add_argument('--raw-root', default='data/raw')
    ap.add_argument('--out-dates', default='qa_data/baselines/ground_truth_dates.csv')
    ap.add_argument('--out-rss', default='qa_data/baselines/newsroom_rss_dates.csv')
    ap.add_argument('--limit', type=int, default=None)
    args = ap.parse_args()

    logger, log_path = qa_logger('qa_ground_truth_builder')

    rows = []
    # Iterate over meta files under raw/**
    metas = glob.glob(os.path.join(args.raw_root, '**', '*.meta.json'), recursive=True)
    if args.limit:
        metas = metas[: args.limit]

    for mp in metas:
        meta = read_json(mp)
        doc_id = os.path.basename(mp).replace('.meta.json', '')
        src_type = mp.split(os.sep)[2] if len(mp.split(os.sep)) >= 3 else ''
        baseline_date = ''
        title = meta.get('headline') or meta.get('title_hint') or ''
        url = meta.get('url', '')
        method = ''
        # SEC: parse from HTML if present
        if src_type == 'sec':
            raw_html = mp.replace('.meta.json', '.raw.html')
            if os.path.exists(raw_html):
                html = read_text(raw_html)
                d = parse_filed_date_from_html(html)
                if d:
                    baseline_date = d
                    method = 'filed_header'
            if not baseline_date and meta.get('filing_date'):
                baseline_date = meta.get('filing_date')
                method = method or 'edgar_index_meta'
        elif src_type in ('newsroom', 'investor_news'):
            if meta.get('rss_pubdate'):
                baseline_date = meta['rss_pubdate']
                method = 'rss_pubdate'
            elif meta.get('visible_date'):
                baseline_date = meta['visible_date']
                method = 'visible_dateline'
            if not baseline_date:
                raw_html = mp.replace('.meta.json', '.raw.html')
                if os.path.exists(raw_html):
                    html = read_text(raw_html)
                    p = parse_meta_published_time(html)
                    if p:
                        baseline_date = p
                        method = 'meta_article_published_time'
        elif src_type in ('product', 'dev_docs', 'help_docs', 'wikipedia'):
            lm = (meta.get('headers') or {}).get('last-modified') or meta.get('last_modified_http')
            if lm:
                d = parse_iso_date(lm)
                if d:
                    baseline_date = date_to_iso(d)
                    method = 'http_last_modified'
            if not baseline_date:
                raw_html = mp.replace('.meta.json', '.raw.html')
                if os.path.exists(raw_html):
                    html = read_text(raw_html)
                    p = parse_meta_published_time(html)
                    if p:
                        baseline_date = p
                        method = 'meta_article_published_time'
        # Title fallback via raw HTML
        if not title:
            raw_html = mp.replace('.meta.json', '.raw.html')
            if os.path.exists(raw_html):
                try:
                    html = read_text(raw_html)
                    title = guess_title_from_html(html) or ''
                except Exception:
                    pass
        rows.append([doc_id, src_type, baseline_date, title, url, method])

    ensure_parent(args.out_dates)
    with open(args.out_dates, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['doc_id', 'source_type', 'baseline_date', 'baseline_title', 'baseline_url', 'method'])
        w.writerows(rows)

    # Build RSS dates baseline (newsroom feeds embedded in meta)
    # We re-emit rows where method == rss_pubdate for convenience
    rss_rows = [r for r in rows if r[-1] == 'rss_pubdate']
    ensure_parent(args.out_rss)
    with open(args.out_rss, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['doc_id', 'source_type', 'baseline_date', 'baseline_title', 'baseline_url', 'method'])
        w.writerows(rss_rows)

    logger.info(f"Ground-truth rows: {len(rows)} written to {args.out_dates}")


if __name__ == '__main__':
    main()
