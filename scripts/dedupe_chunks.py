#!/usr/bin/env python3
import os
import re
import glob
import json
import argparse
from collections import defaultdict

from _common import setup_logger, read_text, write_text, write_json
import os


def normalize_for_shingles(text: str) -> list[str]:
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    words = [w for w in text.split() if w]
    return words


def load_boilerplate_allowlist(path: str = os.path.join('qa_configs','qa.boilerplate.allowlist.txt')) -> list[str]:
    sigs = []
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                s = line.strip()
                if not s or s.startswith('#'):
                    continue
                if len(s) >= 80:
                    sigs.append(s)
    except Exception:
        pass
    return sorted(set(sigs), key=lambda x: -len(x))


def strip_boilerplate(text: str, doctype: str, allowlist: list[str]) -> str:
    if doctype not in ('press','product'):
        return text
    for sig in allowlist:
        if sig and sig in text:
            text = text.replace(sig, ' ')
    return text


def shingles(words: list[str], k: int = 5) -> set[str]:
    if len(words) < k:
        return set([' '.join(words)])
    return { ' '.join(words[i:i+k]) for i in range(0, len(words)-k+1) }


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def main():
    ap = argparse.ArgumentParser(description='Dedupe near-duplicate chunks across all docs.')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--limit', type=int, default=999999)
    ap.add_argument('--since', type=str, default=None)
    ap.add_argument('--until', type=str, default=None)
    ap.add_argument('--concurrency', type=int, default=4)
    args = ap.parse_args()

    logger, log_path = setup_logger('dedupe')
    chunks_dir = os.path.join('data', 'interim', 'chunks')
    out_dir = os.path.join('data', 'interim', 'chunks', 'filtered')
    os.makedirs(out_dir, exist_ok=True)

    # Load all chunks
    allowlist = load_boilerplate_allowlist()
    chunk_files = glob.glob(os.path.join(chunks_dir, '*.chunks.jsonl'))[: args.limit]
    chunk_texts = {}
    for f in chunk_files:
        for line in read_text(f).splitlines():
            if not line.strip():
                continue
            try:
                rec = json.loads(line)
            except Exception:
                # skip malformed line
                continue
            # Apply boilerplate stripping to press/product chunks before sigs
            dt = (rec.get('metadata_snapshot') or {}).get('doctype')
            if allowlist:
                rec['text'] = strip_boilerplate(rec.get('text',''), dt, allowlist)
            chunk_texts[rec.get('chunk_id')] = rec

    ids = list(chunk_texts.keys())
    sigs = {}
    for cid in ids:
        words = normalize_for_shingles(chunk_texts[cid]['text'])
        sigs[cid] = shingles(words, 5)

    # Naive O(n^2) dedupe with early skip; acceptable for Day-1 scale
    threshold = 0.98
    visited = set()
    groups = []
    for i, cid in enumerate(ids):
        if cid in visited:
            continue
        visited.add(cid)
        group = [cid]
        for j in range(i+1, len(ids)):
            eid = ids[j]
            if eid in visited:
                continue
            sim = jaccard(sigs[cid], sigs[eid])
            if sim >= threshold:
                visited.add(eid)
                group.append(eid)
        if len(group) > 1:
            groups.append(group)

    # Choose canonical (earliest publish_date; tie-break longer word_count)
    dedup_map = []
    for group in groups:
        # Build helper map doc publish_date
        def doc_key(cid):
            rec = chunk_texts[cid]
            d = rec['metadata_snapshot'].get('date') or '9999-12-31'
            wc = rec.get('word_count', 0)
            return (d, -wc)
        group_sorted = sorted(group, key=doc_key)
        canonical = group_sorted[0]
        duplicates = group_sorted[1:]
        dedup_map.append({'canonical_chunk_id': canonical, 'duplicate_chunk_ids': duplicates})

    # Write filtered per-doc chunk files
    dup_set = set(d for g in dedup_map for d in g['duplicate_chunk_ids'])
    kept = 0
    for f in chunk_files:
        lines = []
        for line in read_text(f).splitlines():
            if not line.strip():
                continue
            try:
                rec = json.loads(line)
            except Exception:
                continue
            if rec.get('chunk_id') in dup_set:
                continue
            lines.append(json.dumps(rec, ensure_ascii=False))
            kept += 1
        out_path = os.path.join(out_dir, os.path.basename(f))
        if args.dry_run:
            logger.info(f"[dry-run] Would write {out_path}")
        else:
            write_text(out_path, '\n'.join(lines) + '\n')

    write_json(os.path.join('data', 'interim', 'dedup', 'dedup_map.json'), {'groups': dedup_map})
    logger.info(f"Dedupe groups: {len(dedup_map)}, kept chunks: {kept}. Log: {log_path}")


if __name__ == '__main__':
    main()
