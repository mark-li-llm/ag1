#!/usr/bin/env python3
import os
import re
import glob
import argparse
from datetime import date, datetime, timedelta

from _common import (
    setup_logger, read_json, write_json, load_yaml, parse_iso_date, date_to_iso,
    token_count, detect_language, source_domain
)


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


def backfill_publish_date(doc: dict, raw_meta: dict) -> str | None:
    # Precedence per blueprint
    doctype = doc.get('doctype')
    if doc.get('source_domain') == 'sec.gov':
        if raw_meta.get('filing_date'):
            return raw_meta.get('filing_date')
    # IR/newsroom
    for key in ('rss_pubdate', 'visible_date', 'meta_published_time'):
        if raw_meta.get(key):
            d = parse_iso_date(raw_meta.get(key))
            if d:
                return date_to_iso(d)
    # HTTP Last-Modified
    lm = (raw_meta.get('headers') or {}).get('last-modified') or raw_meta.get('last_modified_http')
    if lm:
        d = parse_iso_date(lm)
        if d:
            return date_to_iso(d)
    return None


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
        title = doc.get('title') or raw_meta.get('headline') or raw_meta.get('title_hint') or ''
        doc['title'] = title
        # Publish date precedence
        pd = doc.get('publish_date') or backfill_publish_date(doc, raw_meta)
        doc['publish_date'] = pd or doc.get('publish_date') or ''
        # URL / source domain
        if not doc.get('url') and raw_meta.get('url'):
            doc['url'] = raw_meta['url']
        if not doc.get('source_domain') and doc.get('url'):
            doc['source_domain'] = source_domain(doc['url'])
        # Topic & personas
        doc['topic'] = apply_topics(doc.get('text', ''), title, lexicon)
        doc['persona_tags'] = apply_personas(doc.get('text', ''), prompts)
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

