#!/usr/bin/env python3
import os
import re
import json
import glob
import argparse
from collections import defaultdict

from _qa_common import qa_logger, write_report, load_chunks_from_jsonl, jaccard


def extract_spans(text: str, ngram_range=(8, 20), min_span_chars=150) -> set[str]:
    words = re.findall(r"\w+", text.lower())
    spans = set()
    for n in range(ngram_range[0], ngram_range[1]+1):
        if len(words) < n:
            break
        for i in range(0, len(words)-n+1):
            w = words[i:i+n]
            s = ' '.join(w)
            if len(s) >= min_span_chars:
                spans.add(s)
    return spans


def main():
    ap = argparse.ArgumentParser(description='QA: Mine recurring boilerplate spans from chunks')
    ap.add_argument('--chunks-glob', default='data/interim/chunks/*.chunks.jsonl')
    ap.add_argument('--doctype-filter', default='press,product')
    ap.add_argument('--min_doc_freq', type=int, default=8)
    ap.add_argument('--min_docs_for_boilerplate', type=int, default=10)
    ap.add_argument('--out', default='qa_data/outputs/boilerplate_signatures.json')
    args = ap.parse_args()

    logger, log_path = qa_logger('qa_boilerplate_mine')
    files = sorted(glob.glob(args.chunks_glob))
    types = set(x.strip() for x in args.doctype_filter.split(','))

    span_docs = defaultdict(set)  # span -> set(doc_id)
    for f in files:
        chunks = load_chunks_from_jsonl(f)
        for ch in chunks:
            dt = (ch.get('metadata_snapshot') or {}).get('doctype')
            if dt not in types:
                continue
            spans = extract_spans(ch.get('text', ''))
            for sp in spans:
                span_docs[sp].add(ch['doc_id'])

    # filter by min doc freq
    candidates = [(sp, len(docs)) for sp, docs in span_docs.items() if len(docs) >= args.min_doc_freq]
    # simple clustering: dedupe spans with high jaccard
    candidates.sort(key=lambda x: -x[1])
    clusters = []
    used = set()
    for sp, df in candidates:
        if sp in used:
            continue
        group = [sp]
        used.add(sp)
        for sp2, df2 in candidates:
            if sp2 in used:
                continue
            j = jaccard(set(sp.split()), set(sp2.split()))
            if j >= 0.85:
                used.add(sp2)
                group.append(sp2)
        clusters.append({'signature': sp, 'variants': group, 'doc_freq': df})

    # mark approved boilerplate if appears in >= min_docs_for_boilerplate docs
    signatures = [c for c in clusters if c['doc_freq'] >= args.min_docs_for_boilerplate]
    out = {
        'signatures': signatures[:200],
        'total_candidates': len(candidates),
        'clusters': len(clusters),
        'log_path': log_path,
    }
    write_report(args.out, out)

    # update allowlist file with top signatures (append)
    allowlist_path = 'qa_configs/qa.boilerplate.allowlist.txt'
    os.makedirs(os.path.dirname(allowlist_path), exist_ok=True)
    with open(allowlist_path, 'a', encoding='utf-8') as f:
        for sig in signatures[:20]:
            f.write(sig['signature'][:500] + '\n')

    logger.info(f"Boilerplate signatures: {len(signatures)} -> {args.out}")


if __name__ == '__main__':
    main()

