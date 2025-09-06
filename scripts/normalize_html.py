#!/usr/bin/env python3
import os
import glob
import argparse
import json
from datetime import datetime

from _common import (
    setup_logger, load_yaml, html_to_text, token_count, detect_language,
    sha256_hex, write_json, read_json, ensure_parent, source_domain
)

RAW_DIRS = [
    os.path.join('data', 'raw', 'sec'),
    os.path.join('data', 'raw', 'investor_news'),
    os.path.join('data', 'raw', 'newsroom'),
    os.path.join('data', 'raw', 'product'),
    os.path.join('data', 'raw', 'dev_docs'),
    os.path.join('data', 'raw', 'help_docs'),
    os.path.join('data', 'raw', 'wikipedia'),
]


def normalized_path(doc_id: str) -> str:
    return os.path.join('data', 'interim', 'normalized', f'{doc_id}.json')


def main():
    ap = argparse.ArgumentParser(description='Normalize raw HTML/PDF into clean text JSON records.')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--limit', type=int, default=999999)
    ap.add_argument('--since', type=str, default=None)
    ap.add_argument('--until', type=str, default=None)
    ap.add_argument('--concurrency', type=int, default=4)
    args = ap.parse_args()

    logger, log_path = setup_logger('normalize')
    rules = load_yaml(os.path.join('configs', 'normalization.rules.yaml'))

    count = 0
    for raw_dir in RAW_DIRS:
        if not os.path.isdir(raw_dir):
            continue
        # process HTML first
        for raw_file in glob.glob(os.path.join(raw_dir, '*.raw.html')):
            if count >= args.limit:
                break
            doc_id = os.path.basename(raw_file).replace('.raw.html', '')
            meta_file = os.path.join(raw_dir, f'{doc_id}.meta.json')
            if not os.path.exists(meta_file):
                # Skip artifacts without meta; prevents stray/partial docs
                continue
            meta = read_json(meta_file)
            with open(raw_file, 'rb') as f:
                raw_bytes = f.read()
            html = raw_bytes.decode('utf-8', errors='ignore')
            text, _ = html_to_text(html, rules)
            lang = detect_language(text)
            if rules['global']['language'].get('drop_non_english') and lang != 'en':
                logger.info(f"Drop non-English: {doc_id} ({lang})")
                continue
            wc = len(text.split())
            tc = token_count(text)
            norm = {
                'doc_id': doc_id,
                'company': 'Salesforce',
                'doctype': doc_id.split('::')[1] if '::' in doc_id else meta.get('doctype_hint') or '',
                'title': meta.get('title_hint') or '',
                'publish_date': doc_id.split('::')[2] if '::' in doc_id else '',
                'url': meta.get('url', ''),
                'final_url': meta.get('url', ''),
                'source_domain': meta.get('source_domain') or source_domain(meta.get('url', '')),
                'section': 'body',
                'topic': '',
                'persona_tags': [],
                'language': lang,
                'text': text,
                'word_count': wc,
                'token_count': tc,
                'ingestion_ts': datetime.utcnow().isoformat(),
                'hash_sha256': sha256_hex(text.encode('utf-8')),
                'html_title': meta.get('title_hint', ''),
                'meta_published_time': meta.get('rss_pubdate') or meta.get('visible_date') or '',
                'last_modified_http': meta.get('last_modified_http') or (meta.get('headers', {}).get('last-modified') if meta.get('headers') else ''),
            }
            out = normalized_path(doc_id)
            if args.dry_run:
                logger.info(f"[dry-run] Would write {out}")
            else:
                write_json(out, norm)
                count += 1
        # PDFs
        for raw_file in glob.glob(os.path.join(raw_dir, '*.pdf')):
            if count >= args.limit:
                break
            try:
                from pdfminer.high_level import extract_text
            except Exception:
                logger.error('pdfminer.six not installed; skipping PDF extraction')
                continue
            doc_id = os.path.basename(raw_file).replace('.pdf', '')
            meta_file = os.path.join(raw_dir, f'{doc_id}.meta.json')
            if not os.path.exists(meta_file):
                continue
            meta = read_json(meta_file)
            text = extract_text(raw_file) or ''
            lang = detect_language(text)
            if rules['global']['language'].get('drop_non_english') and lang != 'en':
                logger.info(f"Drop non-English (pdf): {doc_id} ({lang})")
                continue
            wc = len(text.split())
            tc = token_count(text)
            norm = {
                'doc_id': doc_id,
                'company': 'Salesforce',
                'doctype': doc_id.split('::')[1] if '::' in doc_id else meta.get('doctype_hint') or 'ars_pdf',
                'title': meta.get('title_hint') or 'Annual Report',
                'publish_date': doc_id.split('::')[2] if '::' in doc_id else '',
                'url': meta.get('url', ''),
                'final_url': meta.get('url', ''),
                'source_domain': meta.get('source_domain') or source_domain(meta.get('url', '')),
                'section': 'body',
                'topic': '',
                'persona_tags': [],
                'language': lang,
                'text': text,
                'word_count': wc,
                'token_count': tc,
                'ingestion_ts': datetime.utcnow().isoformat(),
                'hash_sha256': sha256_hex(text.encode('utf-8')),
            }
            out = normalized_path(doc_id)
            if args.dry_run:
                logger.info(f"[dry-run] Would write {out}")
            else:
                write_json(out, norm)
                count += 1

    logger.info(f"Normalized {count} documents. Log: {log_path}")


if __name__ == '__main__':
    main()
