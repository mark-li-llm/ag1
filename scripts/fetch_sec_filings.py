#!/usr/bin/env python3
import os
import re
import argparse
from datetime import date

from _common import (
    setup_logger, RateLimiter, load_yaml, http_fetch, clean_url_params,
    source_domain, slugify, doc_id, write_json, ensure_parent, parse_iso_date, date_to_iso,
    guess_title_from_html
)


def parse_filed_date(html: str) -> str | None:
    # Try common SEC patterns
    # e.g., "Filed: March 05, 2025" or "Filed 2025-03-05"
    m = re.search(r'Filed\s*[:]?\s*([A-Za-z]{3,9}\s+\d{1,2},\s+\d{4})', html, re.I)
    if m:
        d = parse_iso_date(m.group(1))
        if d:
            return date_to_iso(d)
    m = re.search(r'Filed\s*[:]?\s*(\d{4}-\d{2}-\d{2})', html)
    if m:
        return m.group(1)
    # Sometimes inline XBRL viewer places date in meta
    m = re.search(r'"filingDate"\s*:\s*"(\d{4}-\d{2}-\d{2})"', html)
    if m:
        return m.group(1)
    return None


def infer_doctype(url: str, html: str, hints: dict) -> str:
    for key, dt in (hints or {}).items():
        if key in url:
            return dt
    # Fallback: inspect html
    if re.search(r'FORM\s+10-K', html, re.I):
        return '10-K'
    if re.search(r'FORM\s+10-Q', html, re.I):
        return '10-Q'
    if re.search(r'FORM\s+8-K', html, re.I):
        return '8-K'
    # PDF ARS by URL extension
    if url.lower().endswith('.pdf'):
        return 'ars_pdf'
    return '8-K'


def main():
    ap = argparse.ArgumentParser(description='Fetch Salesforce SEC filings (specific URLs).')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--limit', type=int, default=100)
    ap.add_argument('--since', type=str, default=None)
    ap.add_argument('--until', type=str, default=None)
    ap.add_argument('--concurrency', type=int, default=4)
    args = ap.parse_args()

    logger, log_path = setup_logger('fetch')
    cfg = load_yaml(os.path.join('configs', 'sources.salesforce.yaml'))
    urls = cfg['sources']['sec']['urls']
    hints = cfg['sources']['sec'].get('doctype_hints', {})
    since_d = parse_iso_date(args.since) if args.since else None
    until_d = parse_iso_date(args.until) if args.until else None
    rate = RateLimiter(6.0)

    saved = 0
    for url in urls[: args.limit]:
        url = clean_url_params(url)
        rate.acquire()
        status, body, info = http_fetch(url, logger, timeout=10, method='GET', allow_redirects=True)
        if status != 200:
            logger.warning(f"Non-200 for {url}: {status}")
            continue
        final_url = info.get('final_url', url)
        domain = source_domain(final_url)
        is_pdf = final_url.lower().endswith('.pdf')
        html = body.decode('utf-8', errors='ignore') if not is_pdf else ''
        filed_date = parse_filed_date(html) if not is_pdf else None
        # If filed_date missing and URL contains crm-YYYYMMDD, that is period end; leave None, will be filled later
        dt = infer_doctype(final_url, html, hints)
        title = guess_title_from_html(html) if not is_pdf else 'Annual Report to Security Holders'
        slug = slugify(title or os.path.basename(url).split('.')[0])
        # For doc_id, require a date; if missing, use today as placeholder; normalization will correct later
        date_iso = filed_date or date.today().isoformat()
        did = doc_id(dt, date_iso, slug, body)
        raw_dir = os.path.join('data', 'raw', 'sec')
        ensure_parent(raw_dir + '/.keep')
        ext = '.pdf' if is_pdf else '.raw.html'
        raw_path = os.path.join(raw_dir, f'{did}{ext}')
        meta_path = os.path.join(raw_dir, f'{did}.meta.json')
        meta = {
            'url': final_url,
            'source_domain': domain,
            'doctype_hint': dt,
            'filing_date': filed_date,
            'title_hint': title,
            'http_status': status,
            'headers': info.get('headers', {}),
        }
        if args.dry_run:
            logger.info(f"[dry-run] Would save {raw_path}")
        else:
            with open(raw_path, 'wb') as f:
                f.write(body)
            write_json(meta_path, meta)
            saved += 1
    logger.info(f"Saved {saved} SEC artifacts. Log: {log_path}")


if __name__ == '__main__':
    main()

