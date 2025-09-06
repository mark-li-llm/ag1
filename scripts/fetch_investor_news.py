#!/usr/bin/env python3
import os
import re
import argparse
from datetime import date
from urllib.parse import urljoin

from _common import (
    setup_logger, RateLimiter, load_yaml, http_fetch, clean_url_params,
    source_domain, slugify, doc_id, write_json, ensure_parent, parse_iso_date, date_to_iso,
    guess_title_from_html, parse_meta_published_time
)


def discover_article_links(html: str, base_url: str) -> list[str]:
    # Collect anchors with '/news/' in href
    hrefs = set()
    for m in re.finditer(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>', html, re.I):
        href = m.group(1)
        if '/news/' in href:
            hrefs.add(urljoin(base_url, href))
    return list(hrefs)


def extract_visible_date(html: str) -> str | None:
    # Look for patterns like 'January 1, 2025'
    m = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}', html)
    if m:
        return date_to_iso(parse_iso_date(m.group(0)))
    return None


def main():
    ap = argparse.ArgumentParser(description='Fetch Salesforce Investor Relations news articles.')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--limit', type=int, default=30)
    ap.add_argument('--since', type=str, default='2024-01-01')
    ap.add_argument('--until', type=str, default=None)
    ap.add_argument('--concurrency', type=int, default=4)
    args = ap.parse_args()

    logger, log_path = setup_logger('fetch')
    cfg = load_yaml(os.path.join('configs', 'sources.salesforce.yaml'))
    start_url = cfg['sources']['investor_news']['start_url']
    since_d = parse_iso_date(args.since) if args.since else None
    until_d = parse_iso_date(args.until) if args.until else None
    target = min(args.limit, int(cfg['sources']['investor_news'].get('target_count', 20)))
    rate = RateLimiter(6.0)

    # Fetch listing
    rate.acquire()
    status, body, info = http_fetch(start_url, logger, timeout=10)
    if status != 200:
        logger.error(f"Failed to fetch listing: {status}")
        return
    listing_html = body.decode('utf-8', errors='ignore')
    links = discover_article_links(listing_html, info.get('final_url', start_url))

    saved = 0
    for url in links:
        if saved >= target:
            break
        url = clean_url_params(url)
        rate.acquire()
        s, b, inf = http_fetch(url, logger, timeout=10)
        if s != 200:
            logger.warning(f"Skip non-200 {url}: {s}")
            continue
        html = b.decode('utf-8', errors='ignore')
        pub = parse_meta_published_time(html) or extract_visible_date(html)
        pub_d = parse_iso_date(pub) if pub else None
        if since_d and pub_d and pub_d < since_d:
            continue
        if until_d and pub_d and pub_d > until_d:
            continue
        title = guess_title_from_html(html)
        slug = slugify(title or os.path.basename(url).split('.')[0])
        date_iso = pub or date.today().isoformat()
        did = doc_id('press', date_iso, slug, b)
        raw_dir = os.path.join('data', 'raw', 'investor_news')
        ensure_parent(raw_dir + '/.keep')
        raw_path = os.path.join(raw_dir, f'{did}.raw.html')
        meta_path = os.path.join(raw_dir, f'{did}.meta.json')
        meta = {
            'url': inf.get('final_url', url),
            'source_domain': source_domain(url),
            'visible_date': pub,
            'headline': title,
        }
        if args.dry_run:
            logger.info(f"[dry-run] Would save {raw_path}")
        else:
            with open(raw_path, 'wb') as f:
                f.write(b)
            write_json(meta_path, meta)
            saved += 1
    logger.info(f"Saved {saved} Investor News articles. Log: {log_path}")


if __name__ == '__main__':
    main()

