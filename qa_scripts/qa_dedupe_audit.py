#!/usr/bin/env python3
import os
import re
import json
import glob
import argparse
from collections import defaultdict

from _qa_common import qa_logger, write_report, load_chunks_from_jsonl, normalize_for_shingles, shingles, jaccard


def load_dedup_map(path: str) -> list[dict]:
    if not os.path.exists(path):
        return []
    try:
        obj = json.load(open(path, 'r', encoding='utf-8'))
        return obj.get('groups', []) or []
    except Exception:
        return []


def grid_eval(chunks: dict, thresholds: list[float], k_values: list[int], ignore_boilerplate: bool, boilerplate_signatures: list[str]):
    ids = list(chunks.keys())
    texts = {
        cid: chunks[cid]['text'] for cid in ids
    }
    if ignore_boilerplate and boilerplate_signatures:
        for cid, t in list(texts.items()):
            for sig in boilerplate_signatures:
                t = t.replace(sig, ' ')
            texts[cid] = t
    results = []
    for k in k_values:
        sigs = { cid: shingles(normalize_for_shingles(texts[cid]), k) for cid in ids }
        for thr in thresholds:
            visited = set()
            dup = 0
            for i, cid in enumerate(ids):
                if cid in visited:
                    continue
                visited.add(cid)
                for j in range(i+1, len(ids)):
                    eid = ids[j]
                    if eid in visited:
                        continue
                    if jaccard(sigs[cid], sigs[eid]) >= thr:
                        visited.add(eid)
                        dup += 1
            ratio = dup / max(1, len(ids))
            results.append({'k': k, 'threshold': thr, 'duplicate_ratio': round(ratio, 4)})
    return results


def main():
    ap = argparse.ArgumentParser(description='QA: Dedupe audit & parameter grid')
    ap.add_argument('--chunks-glob', default='data/interim/chunks/*.chunks.jsonl')
    ap.add_argument('--dedup-map', default='data/interim/dedup/dedup_map.json')
    ap.add_argument('--boilerplate', default='qa_data/outputs/boilerplate_signatures.json')
    ap.add_argument('--limit', type=int, default=None)
    ap.add_argument('--out', default='qa_data/outputs/dedupe_audit.json')
    args = ap.parse_args()

    logger, log_path = qa_logger('qa_dedupe_audit')
    files = sorted(glob.glob(args.chunks_glob))
    if args.limit:
        files = files[: args.limit]

    chunks = {}
    for f in files:
        for ch in load_chunks_from_jsonl(f):
            chunks[ch['chunk_id']] = ch

    groups = load_dedup_map(args.dedup_map)
    dup_chunks = set(d for g in groups for d in g.get('duplicate_chunk_ids', []))

    # Cause attribution via boilerplate signature presence
    boilerplate_signatures = []
    if os.path.exists(args.boilerplate):
        try:
            data = json.load(open(args.boilerplate, 'r', encoding='utf-8'))
            boilerplate_signatures = [s['signature'] for s in data.get('signatures', [])]
        except Exception:
            pass

    bp_hits = 0
    for cid in dup_chunks:
        t = chunks.get(cid, {}).get('text', '')
        if any(sig in t for sig in boilerplate_signatures):
            bp_hits += 1

    # Grid search
    grid = grid_eval(chunks, thresholds=[0.85, 0.9, 0.95], k_values=[5, 7], ignore_boilerplate=True, boilerplate_signatures=boilerplate_signatures)

    report = {
        'total_chunks': len(chunks),
        'duplicate_chunks_marked': len(dup_chunks),
        'boilerplate_attributed_duplicates': int(bp_hits),
        'boilerplate_attributed_pct': round((bp_hits/max(1, len(dup_chunks))), 4),
        'grid_results': grid,
        'recommended': {'threshold': 0.9, 'k': 5},
        'log_path': log_path,
    }
    write_report(args.out, report)
    logger.info(f"Dedupe audit: dup={len(dup_chunks)}, grid={len(grid)} -> {args.out}")


if __name__ == '__main__':
    main()

