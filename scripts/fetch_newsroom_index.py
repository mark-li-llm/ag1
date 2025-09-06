#!/usr/bin/env python3
import os
import re
import argparse
from urllib.parse import urljoin
from datetime import date

from _common import (
    setup_logger, RateLimiter, http_fetch, clean_url_params, source_domain,
    slugify, doc_id, write_json, ensure_parent, parse_iso_date, date_to_iso,
    guess_title_from_html, parse_meta_published_time
)


INDEX_URL = 'https://www.salesforce.com/news/all-news-press-salesforce/'


def discover_links(html: str, base: str) -> list[str]:
    hrefs = set()
    for m in re.finditer(r'<a\s+[^>]*href=["\']([^"\']+)["\']', html, re.I):
        href = m.group(1)
        if '/news/' in href and '/press-releases/' in href:
            hrefs.add(urljoin(base, href))
    return list(hrefs)


def extract_visible_date(html: str) -> str | None:
    m = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}', html)
    if m:
        from _common import parse_iso_date, date_to_iso
        return date_to_iso(parse_iso_date(m.group(0)))
    return None


def main():
    ap = argparse.ArgumentParser(description='Crawl Salesforce Newsroom index and fetch first N articles (no JS).')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--limit', type=int, default=20)
    ap.add_argument('--since', type=str, default='2024-01-01')
    ap.add_argument('--until', type=str, default=None)
    ap.add_argument('--concurrency', type=int, default=6)
    args = ap.parse_args()

    logger, log_path = setup_logger('fetch')
    since_d = parse_iso_date(args.since) if args.since else None
    until_d = parse_iso_date(args.until) if args.until else None
    rate = RateLimiter(6.0)

    rate.acquire()
    s, b, inf = http_fetch(INDEX_URL, logger, timeout=12)
    if s != 200:
        logger.error(f"Index fetch failed: {s}")
        return
    html = b.decode('utf-8', errors='ignore')
    links = discover_links(html, inf.get('final_url', INDEX_URL))

    saved = 0
    for url in links:
        if saved >= args.limit:
            break
        url = clean_url_params(url)
        rate.acquire()
        ss, bb, info2 = http_fetch(url, logger, timeout=10)
        if ss != 200:
            logger.warning(f"Skip non-200 {url}: {ss}")
            continue
        ah = bb.decode('utf-8', errors='ignore')
        pub = parse_meta_published_time(ah) or extract_visible_date(ah)
        pub_d = parse_iso_date(pub) if pub else None
        if since_d and pub_d and pub_d < since_d:
            continue
        if until_d and pub_d and pub_d > until_d:
            continue
        title = guess_title_from_html(ah)
        slug = slugify(title or os.path.basename(url).split('.')[0])
        date_iso = pub or date.today().isoformat()
        did = doc_id('press', date_iso, slug, bb)
        raw_dir = os.path.join('data', 'raw', 'newsroom')
        ensure_parent(raw_dir + '/.keep')
        raw_path = os.path.join(raw_dir, f'{did}.raw.html')
        meta_path = os.path.join(raw_dir, f'{did}.meta.json')
        meta = {
            'url': info2.get('final_url', url),
            'source_domain': source_domain(url),
            'visible_date': pub,
            'headline': title,
        }
        if args.dry_run:
            logger.info(f"[dry-run] Would save {raw_path}")
        else:
            with open(raw_path, 'wb') as f:
                f.write(bb)
            write_json(meta_path, meta)
            saved += 1
    logger.info(f"Saved {saved} Newsroom index items. Log: {log_path}")


if __name__ == '__main__':
    main()
