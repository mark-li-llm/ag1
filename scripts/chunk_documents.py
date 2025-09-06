#!/usr/bin/env python3
import os
import glob
import argparse
import json

from _common import setup_logger, read_json, token_count, write_text


def chunk_text(text: str, target: int, overlap: int) -> list[tuple[int, int, str]]:
    # naive tokenization by counting via token_count; split by paragraphs as hints
    paras = [p.strip() for p in text.split('\n\n') if p.strip()]
    chunks = []
    buf = []
    buf_tokens = 0
    start_char = 0
    current_start = 0
    for p in paras:
        ptok = token_count(p)
        if buf_tokens + ptok <= target or not buf:
            buf.append(p)
            buf_tokens += ptok
            continue
        # flush
        chunk_text = '\n\n'.join(buf)
        end_char = current_start + len(chunk_text)
        chunks.append((current_start, end_char, chunk_text))
        # start new buffer with overlap: take last paragraph(s) until overlap reached
        overlap_buf = []
        overlap_tokens = 0
        for prev in reversed(buf):
            if overlap_tokens >= overlap:
                break
            overlap_buf.insert(0, prev)
            overlap_tokens += token_count(prev)
        buf = overlap_buf + [p]
        buf_tokens = overlap_tokens + ptok
        current_start = end_char  # monotonic approx
    if buf:
        chunk_text = '\n\n'.join(buf)
        end_char = current_start + len(chunk_text)
        chunks.append((current_start, end_char, chunk_text))
    return chunks


def main():
    ap = argparse.ArgumentParser(description='Chunk normalized documents into retrieval-friendly windows.')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--limit', type=int, default=999999)
    ap.add_argument('--since', type=str, default=None)
    ap.add_argument('--until', type=str, default=None)
    ap.add_argument('--concurrency', type=int, default=4)
    args = ap.parse_args()

    logger, log_path = setup_logger('chunk')
    cfg = json.load(open(os.path.join('configs', 'chunking.config.json'), 'r'))
    target = int(cfg.get('target_tokens', 800))
    overlap = int(cfg.get('overlap_tokens', 120))
    short_one = int(cfg.get('short_doc_single_chunk_threshold', 350))

    norm_dir = os.path.join('data', 'interim', 'normalized')
    out_dir = os.path.join('data', 'interim', 'chunks')
    os.makedirs(out_dir, exist_ok=True)

    processed = 0
    for p in glob.glob(os.path.join(norm_dir, '*.json'))[: args.limit]:
        doc = read_json(p)
        text = doc.get('text', '')
        tc = doc.get('token_count') or token_count(text)
        chunks = []
        if tc <= short_one:
            chunks = [(0, len(text), text)]
        else:
            chunks = chunk_text(text, target, overlap)

        # build JSONL output
        out_lines = []
        for i, (s, e, ctext) in enumerate(chunks):
            chunk_id = f"{doc['doc_id']}::chunk{str(i).zfill(4)}"
            rec = {
                'chunk_id': chunk_id,
                'doc_id': doc['doc_id'],
                'seq_no': i,
                'text': ctext,
                'word_count': len(ctext.split()),
                'token_count': token_count(ctext),
                'start_char': int(s),
                'end_char': int(e),
                'local_heads': [],
                'metadata_snapshot': {
                    'doctype': doc.get('doctype'),
                    'date': doc.get('publish_date'),
                    'topic': doc.get('topic'),
                    'url': doc.get('url'),
                    'title': doc.get('title'),
                    'company': doc.get('company'),
                    'persona_tags': doc.get('persona_tags') or [],
                },
            }
            out_lines.append(json.dumps(rec, ensure_ascii=False))
        out_path = os.path.join(out_dir, f"{doc['doc_id']}.chunks.jsonl")
        if args.dry_run:
            logger.info(f"[dry-run] Would write {out_path}")
        else:
            write_text(out_path, '\n'.join(out_lines) + '\n')
            processed += 1
    logger.info(f"Chunked {processed} documents. Log: {log_path}")


if __name__ == '__main__':
    main()

