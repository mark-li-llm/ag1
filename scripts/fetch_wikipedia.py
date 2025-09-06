#!/usr/bin/env python3
import os
import argparse
from datetime import date

from _common import (
    setup_logger, RateLimiter, load_yaml, http_fetch, clean_url_params,
    source_domain, slugify, doc_id, write_json, ensure_parent,
    guess_title_from_html, parse_iso_date, date_to_iso
)


def main():
    ap = argparse.ArgumentParser(description='Fetch Wikipedia: Salesforce page.')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--limit', type=int, default=1)
    ap.add_argument('--since', type=str, default=None)
    ap.add_argument('--until', type=str, default=None)
    ap.add_argument('--concurrency', type=int, default=1)
    args = ap.parse_args()

    logger, log_path = setup_logger('fetch')
    cfg = load_yaml(os.path.join('configs', 'sources.salesforce.yaml'))
    url = cfg['sources']['wikipedia']['url']
    rate = RateLimiter(6.0)

    url = clean_url_params(url)
    rate.acquire()
    s, b, inf = http_fetch(url, logger, timeout=10, method='GET')
    if s != 200:
        logger.error(f"Failed to fetch Wikipedia page: {s}")
        return
    html = b.decode('utf-8', errors='ignore')
    title = guess_title_from_html(html) or 'Salesforce - Wikipedia'
    slug = slugify('wikipedia-salesforce')
    lm = (inf.get('headers') or {}).get('last-modified')
    d = parse_iso_date(lm) if lm else None
    date_iso = date_to_iso(d) if d else date.today().isoformat()
    did = doc_id('wiki', date_iso, slug, b)
    raw_dir = os.path.join('data', 'raw', 'wikipedia')
    ensure_parent(raw_dir + '/.keep')
    raw_path = os.path.join(raw_dir, f'{did}.raw.html')
    meta_path = os.path.join(raw_dir, f'{did}.meta.json')
    meta = {
        'url': inf.get('final_url', url),
        'source_domain': source_domain(url),
        'last_modified_http': (inf.get('headers') or {}).get('last-modified'),
        'title_hint': title,
    }
    if args.dry_run:
        logger.info(f"[dry-run] Would save {raw_path}")
    else:
        with open(raw_path, 'wb') as f:
            f.write(b)
        write_json(meta_path, meta)
    logger.info(f"Saved Wikipedia page. Log: {log_path}")


if __name__ == '__main__':
    main()
