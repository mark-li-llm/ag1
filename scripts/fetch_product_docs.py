#!/usr/bin/env python3
import os
import argparse
from datetime import date

from _common import (
    setup_logger, RateLimiter, load_yaml, http_fetch, clean_url_params,
    source_domain, slugify, doc_id, write_json, ensure_parent, parse_iso_date,
    guess_title_from_html, date_to_iso
)


def main():
    ap = argparse.ArgumentParser(description='Fetch Salesforce product/overview pages.')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--limit', type=int, default=3)
    ap.add_argument('--since', type=str, default=None)
    ap.add_argument('--until', type=str, default=None)
    ap.add_argument('--concurrency', type=int, default=3)
    args = ap.parse_args()

    logger, log_path = setup_logger('fetch')
    cfg = load_yaml(os.path.join('configs', 'sources.salesforce.yaml'))
    urls = cfg['sources']['product']['urls'][: args.limit]
    rate = RateLimiter(6.0)

    saved = 0
    for url in urls:
        url = clean_url_params(url)
        rate.acquire()
        s, b, inf = http_fetch(url, logger, timeout=10)
        if s != 200:
            logger.warning(f"Skip non-200 {url}: {s}")
            continue
        html = b.decode('utf-8', errors='ignore')
        title = guess_title_from_html(html)
        slug = slugify(title or os.path.basename(url).strip('/'))
        # Prefer HTTP Last-Modified if available to avoid 'today' placeholders
        lm = (inf.get('headers') or {}).get('last-modified')
        d = parse_iso_date(lm) if lm else None
        date_iso = date_to_iso(d) if d else date.today().isoformat()
        did = doc_id('product', date_iso, slug, b)
        raw_dir = os.path.join('data', 'raw', 'product')
        ensure_parent(raw_dir + '/.keep')
        raw_path = os.path.join(raw_dir, f'{did}.raw.html')
        meta_path = os.path.join(raw_dir, f'{did}.meta.json')
        meta = {
            'url': inf.get('final_url', url),
            'source_domain': source_domain(url),
            'title_hint': title,
        }
        if args.dry_run:
            logger.info(f"[dry-run] Would save {raw_path}")
        else:
            with open(raw_path, 'wb') as f:
                f.write(b)
            write_json(meta_path, meta)
            saved += 1
    logger.info(f"Saved {saved} product pages. Log: {log_path}")


if __name__ == '__main__':
    main()
