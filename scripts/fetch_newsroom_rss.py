#!/usr/bin/env python3
import os
import argparse
from datetime import date

from _common import (
    setup_logger, RateLimiter, load_yaml, http_fetch, clean_url_params,
    source_domain, slugify, doc_id, write_json, ensure_parent, parse_iso_date, date_to_iso,
    guess_title_from_html
)

try:
    import feedparser
except Exception:
    feedparser = None


def main():
    ap = argparse.ArgumentParser(description='Fetch Salesforce Newsroom items via RSS feeds.')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--limit', type=int, default=30)
    ap.add_argument('--since', type=str, default='2024-01-01')
    ap.add_argument('--until', type=str, default=None)
    ap.add_argument('--concurrency', type=int, default=6)
    args = ap.parse_args()

    logger, log_path = setup_logger('fetch')
    cfg = load_yaml(os.path.join('configs', 'sources.salesforce.yaml'))
    feeds = cfg['sources']['newsroom_rss']['feeds']
    since_d = parse_iso_date(args.since) if args.since else None
    until_d = parse_iso_date(args.until) if args.until else None
    target_total = min(args.limit, int(cfg['sources']['newsroom_rss'].get('target_count_total', 30)))
    rate = RateLimiter(6.0)

    if feedparser is None:
        logger.error('feedparser not installed. pip install feedparser')
        return

    entries = []
    for feed in feeds:
        fp = feedparser.parse(feed)
        entries.extend(getattr(fp, 'entries', []) or [])

    # Fallback: parse XML manually if feedparser yields nothing
    if not entries:
        for feed in feeds:
            s, b, _ = http_fetch(feed, logger, timeout=10)
            if s != 200 or not b:
                continue
            xml = b.decode('utf-8', errors='ignore')
            import re
            for item in re.findall(r'<item[\s\S]*?</item>', xml, re.I):
                mlink = re.search(r'<link>([^<]+)</link>', item, re.I)
                mdate = re.search(r'<pubDate>([^<]+)</pubDate>', item, re.I)
                mtitle = re.search(r'<title>([^<]+)</title>', item, re.I)
                if not mlink:
                    continue
                entries.append({
                    'link': mlink.group(1).strip(),
                    'published': (mdate.group(1).strip() if mdate else None),
                    'title': (mtitle.group(1).strip() if mtitle else None),
                })

    # Filter by date window and sort recent first
    def eget(e, k):
        return e.get(k) if isinstance(e, dict) else getattr(e, k, None)

    def entry_date(e):
        dt = None
        for key in ('published', 'updated', 'created'):
            val = eget(e, key)
            if val:
                dt = parse_iso_date(val)
                if dt:
                    break
        return dt or date.today()

    entries.sort(key=entry_date, reverse=True)

    saved = 0
    for e in entries:
        if saved >= target_total:
            break
        link = clean_url_params(eget(e, 'link') or '')
        pub = eget(e, 'published') or eget(e, 'updated')
        pub_d = parse_iso_date(pub) if pub else None
        if since_d and pub_d and pub_d < since_d:
            continue
        if until_d and pub_d and pub_d > until_d:
            continue
        rate.acquire()
        s, b, inf = http_fetch(link, logger, timeout=10)
        if s != 200:
            logger.warning(f"Skip non-200 {link}: {s}")
            continue
        html = b.decode('utf-8', errors='ignore')
        title = eget(e, 'title') or guess_title_from_html(html)
        slug = slugify(title or os.path.basename(link).split('.')[0])
        date_iso = date_to_iso(pub_d) if pub_d else date.today().isoformat()
        did = doc_id('press', date_iso, slug, b)
        raw_dir = os.path.join('data', 'raw', 'newsroom')
        ensure_parent(raw_dir + '/.keep')
        raw_path = os.path.join(raw_dir, f'{did}.raw.html')
        meta_path = os.path.join(raw_dir, f'{did}.meta.json')
        meta = {
            'url': inf.get('final_url', link),
            'source_domain': source_domain(link),
            'rss_pubdate': date_iso,
            'headline': title,
        }
        if args.dry_run:
            logger.info(f"[dry-run] Would save {raw_path}")
        else:
            with open(raw_path, 'wb') as f:
                f.write(b)
            write_json(meta_path, meta)
            saved += 1
    logger.info(f"Saved {saved} Newsroom RSS items. Log: {log_path}")


if __name__ == '__main__':
    main()
