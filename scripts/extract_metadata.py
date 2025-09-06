#!/usr/bin/env python3
import os
import re
import glob
import argparse
from datetime import date, datetime, timedelta

from _common import (
    setup_logger, read_json, write_json, load_yaml, parse_iso_date, date_to_iso,
    token_count, detect_language, source_domain, guess_title_from_html, http_fetch, parse_meta_published_time
)
from urllib.parse import urlparse


def load_topic_lexicon(cfg: dict) -> dict:
    return cfg.get('topic_lexicon', {})


def apply_topics(text: str, title: str, lexicon: dict) -> str:
    tags = []
    hay = f"{title}\n{text}".lower()
    for tag, kws in lexicon.items():
        for kw in kws:
            if kw.lower() in hay:
                tags.append(tag)
                break
    return '|'.join(sorted(set(tags)))


def apply_personas(text: str, prompts: dict) -> list[str]:
    personas = []
    hay = text.lower()
    for persona, meta in prompts.get('personas', {}).items():
        for kw in meta.get('keywords', []):
            if kw.lower() in hay:
                personas.append(persona)
                break
    return sorted(set(personas))


def backfill_publish_date(doc: dict, raw_meta: dict) -> tuple[str | None, str]:
    # Returns (date_iso, provenance)
    if doc.get('source_domain') == 'sec.gov' and raw_meta.get('filing_date'):
        d = parse_iso_date(raw_meta.get('filing_date'))
        if d:
            return date_to_iso(d), 'sec_filed'
    for key, prov in (
        ('rss_pubdate', 'rss_pubdate'),
        ('visible_date', 'visible_dateline'),
        ('meta_published_time', 'meta_published_time'),
    ):
        if raw_meta.get(key):
            d = parse_iso_date(raw_meta.get(key))
            if d:
                return date_to_iso(d), prov
    lm = (raw_meta.get('headers') or {}).get('last-modified') or raw_meta.get('last_modified_http')
    if lm:
        d = parse_iso_date(lm)
        if d:
            return date_to_iso(d), 'http_last_modified'
    return None, 'missing'


def main():
    ap = argparse.ArgumentParser(description='Extract metadata and populate required fields in normalized docs.')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--limit', type=int, default=999999)
    ap.add_argument('--since', type=str, default=None)
    ap.add_argument('--until', type=str, default=None)
    ap.add_argument('--concurrency', type=int, default=4)
    args = ap.parse_args()

    logger, log_path = setup_logger('normalize')
    prompts = load_yaml(os.path.join('configs', 'eval.prompts.yaml'))
    lexicon = load_topic_lexicon(prompts)

    norm_dir = os.path.join('data', 'interim', 'normalized')
    updated = 0
    for p in glob.glob(os.path.join(norm_dir, '*.json'))[: args.limit]:
        doc = read_json(p)
        # Locate raw meta alongside source collection by scanning raw subdirs
        raw_meta = {}
        docid = doc.get('doc_id')
        for src in ('sec', 'investor_news', 'newsroom', 'product', 'dev_docs', 'help_docs', 'wikipedia'):
            meta_path = os.path.join('data', 'raw', src, f'{docid}.meta.json')
            if os.path.exists(meta_path):
                raw_meta = read_json(meta_path)
                break
        # Title precedence: doc.title -> raw_meta.headline/title_hint -> raw HTML <title> -> slug from doc_id
        title = doc.get('title') or raw_meta.get('headline') or raw_meta.get('title_hint') or ''
        if not title:
            # try parse raw HTML
            for src in ('sec', 'investor_news', 'newsroom', 'product', 'dev_docs', 'help_docs', 'wikipedia'):
                raw_html_path = os.path.join('data', 'raw', src, f'{docid}.raw.html')
                if os.path.exists(raw_html_path):
                    try:
                        html = open(raw_html_path, 'r', encoding='utf-8', errors='ignore').read()
                        title = guess_title_from_html(html) or ''
                    except Exception:
                        pass
                    if title:
                        break
        if not title:
            # fallback to slug
            try:
                slug = docid.split('::')[3]
                title = slug.replace('-', ' ').title()
            except Exception:
                title = ''
        doc['title'] = title
        # URL / domain fields
        if not doc.get('url') and raw_meta.get('url'):
            doc['url'] = raw_meta['url']
        if doc.get('url'):
            try:
                doc['full_domain'] = urlparse(doc['url']).netloc.lower()
            except Exception:
                doc['full_domain'] = ''
            doc['source_domain'] = source_domain(doc['url'])

        # Publish date precedence with provenance
        pd, prov = backfill_publish_date(doc, raw_meta)
        if not pd:
            # Try parsing meta published time from raw HTML
            for src in ('sec', 'investor_news', 'newsroom', 'product', 'dev_docs', 'help_docs', 'wikipedia'):
                raw_html_path = os.path.join('data', 'raw', src, f'{docid}.raw.html')
                if os.path.exists(raw_html_path):
                    try:
                        html = open(raw_html_path, 'r', encoding='utf-8', errors='ignore').read()
                        maybe = parse_meta_published_time(html)
                        if maybe:
                            pd = maybe
                            prov = 'meta_published_time'
                            break
                    except Exception:
                        pass
        if not pd and doc.get('url'):
            # Try HTTP HEAD for Last-Modified
            try:
                status, _, info = http_fetch(doc['url'], logger, timeout=5.0, method='HEAD')
                lm = (info.get('headers') or {}).get('last-modified')
                if lm:
                    d = parse_iso_date(lm)
                    if d:
                        pd = date_to_iso(d)
                        prov = 'http_last_modified'
            except Exception:
                pass
        # Do not fallback to today; leave missing if not found
        doc['publish_date'] = pd or ''
        doc['publish_date_provenance'] = prov if pd else 'missing'
        conf_map = {
            'sec_filed': 1.00,
            'rss_pubdate': 0.95,
            'meta_published_time': 0.90,
            'visible_dateline': 0.80,
            'http_last_modified': 0.60,
            'fallback_today': 0.10,
            'missing': 0.0,
        }
        doc['publish_date_confidence'] = conf_map.get(doc['publish_date_provenance'], 0.0)
        doc['was_fallback_today'] = False
        # Ensure doctype from doc_id if missing/unknown
        dt = (doc.get('doctype') or '').strip()
        if not dt or dt == 'unknown':
            try:
                doc['doctype'] = docid.split('::')[1]
            except Exception:
                pass
        # Topic & personas
        doc['topic'] = apply_topics(doc.get('text', ''), title, lexicon) or 'General'
        personas = apply_personas(doc.get('text', ''), prompts)
        doc['persona_tags'] = personas or ['general']
        # Language enforce
        lang = detect_language(doc.get('text', ''))
        doc['language'] = 'en' if lang == 'en' else lang
        # Token recount if needed
        if not doc.get('token_count'):
            doc['token_count'] = token_count(doc.get('text', ''))
        if args.dry_run:
            logger.info(f"[dry-run] Would update {p}")
        else:
            write_json(p, doc)
            updated += 1
    logger.info(f"Updated metadata for {updated} docs. Log: {log_path}")


if __name__ == '__main__':
    main()
