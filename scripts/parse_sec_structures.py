#!/usr/bin/env python3
import os
import re
import glob
import argparse

from _common import setup_logger, read_json, write_json


ITEMS = [
    (r'Item\s+1\.', 'Item 1.'),
    (r'Item\s+1A\.', 'Item 1A.'),
    (r'Item\s+7\.', 'Item 7.'),
    (r'Item\s+7A\.', 'Item 7A.'),
    (r'Item\s+8\.', 'Item 8.'),
]


def find_spans(text: str) -> list[dict]:
    spans = []
    matches = []
    for pattern, label in ITEMS:
        for m in re.finditer(pattern, text, re.I):
            matches.append((m.start(), label))
    matches.sort(key=lambda x: x[0])
    for i, (start, label) in enumerate(matches):
        end = matches[i + 1][0] if i + 1 < len(matches) else len(text)
        spans.append({'section': label, 'start_char': int(start), 'end_char': int(end)})
    return spans


def main():
    ap = argparse.ArgumentParser(description='Parse SEC Items and annotate spans in normalized docs.')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--limit', type=int, default=999999)
    ap.add_argument('--since', type=str, default=None)
    ap.add_argument('--until', type=str, default=None)
    ap.add_argument('--concurrency', type=int, default=4)
    args = ap.parse_args()

    logger, log_path = setup_logger('normalize')
    norm_dir = os.path.join('data', 'interim', 'normalized')
    paths = glob.glob(os.path.join(norm_dir, '*.json'))
    updated = 0
    for p in paths[: args.limit]:
        doc = read_json(p)
        if doc.get('source_domain') != 'sec.gov':
            continue
        dt = doc.get('doctype')
        if dt not in ('10-K', '10-Q', '8-K'):
            continue
        spans = find_spans(doc.get('text', ''))
        if not spans:
            continue
        doc['sec_spans'] = spans
        if not args.dry_run:
            write_json(p, doc)
            updated += 1
    logger.info(f"Annotated SEC spans in {updated} docs. Log: {log_path}")


if __name__ == '__main__':
    main()

