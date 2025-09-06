#!/usr/bin/env python3
import os
import json
import glob
import argparse
from statistics import median

from _qa_common import qa_logger, write_report, load_chunks_from_jsonl, overlap_tokens
from _common import token_count, read_json


def main():
    ap = argparse.ArgumentParser(description='QA: Chunk size, overlap, and SEC boundary integrity')
    ap.add_argument('--chunks-glob', default='data/interim/chunks/*.chunks.jsonl')
    ap.add_argument('--filtered-glob', default='data/interim/chunks/filtered/*.chunks.jsonl')
    ap.add_argument('--norm-glob', default='data/interim/normalized/*.json')
    ap.add_argument('--cfg', default='configs/chunking.config.json')
    ap.add_argument('--limit', type=int, default=None)
    ap.add_argument('--out', default='qa_data/outputs/chunk_quality_report.json')
    ap.add_argument('--fail-on', default='auto')
    args = ap.parse_args()

    logger, log_path = qa_logger('qa_chunk_quality')
    use_glob = args.filtered_glob if glob.glob(args.filtered_glob) else args.chunks_glob
    files = sorted(glob.glob(use_glob))
    if args.limit:
        files = files[: args.limit]

    token_lens = []
    overlaps = []
    boundary_crossings = 0
    total_chunks = 0
    empty_heads = 0

    # Load SEC spans map
    sec_spans = {}
    for np in glob.glob(args.norm_glob):
        doc = read_json(np)
        if doc.get('sec_spans'):
            sec_spans[doc['doc_id']] = doc['sec_spans']

    for f in files:
        chunks = load_chunks_from_jsonl(f)
        total_chunks += len(chunks)
        for i, ch in enumerate(chunks):
            tl = ch.get('token_count') or token_count(ch.get('text', ''))
            token_lens.append(tl)
            if not ch.get('local_heads'):
                empty_heads += 1
            if i > 0:
                overlaps.append(overlap_tokens(chunks[i-1]['text'], ch['text']))
            # SEC boundary crossing check
            spans = sec_spans.get(ch['doc_id'])
            if spans:
                s = ch.get('start_char', 0)
                e = ch.get('end_char', 0)
                # identify which span start/end fall into
                span_start = None
                span_end = None
                for sp in spans:
                    if sp['start_char'] <= s < sp['end_char']:
                        span_start = sp['section']
                    if sp['start_char'] <= e-1 < sp['end_char']:
                        span_end = sp['section']
                if span_start and span_end and span_start != span_end:
                    boundary_crossings += 1

    med_len = int(median(token_lens)) if token_lens else 0
    within_len = sum(1 for x in token_lens if 500 <= x <= 1100)
    within_len_pct = (within_len / len(token_lens)) if token_lens else 0.0
    mean_overlap = (sum(overlaps)/len(overlaps)) if overlaps else 0.0
    heads_ok_pct = 1.0 - (empty_heads / max(1, total_chunks))

    report = {
        'total_chunks': total_chunks,
        'median_token_length': med_len,
        'len_within_range_pct': round(within_len_pct, 4),
        'mean_overlap_tokens': round(mean_overlap, 2),
        'sec_boundary_crossings': int(boundary_crossings),
        'chunks_with_local_heads_pct': round(heads_ok_pct, 4),
        'log_path': log_path,
    }
    write_report(args.out, report)
    logger.info(f"Chunk quality: median={med_len}, within%={within_len_pct:.2f}, overlap={mean_overlap:.1f}, crossings={boundary_crossings}")


if __name__ == '__main__':
    main()
