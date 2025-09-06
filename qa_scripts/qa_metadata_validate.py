#!/usr/bin/env python3
import os
import re
import csv
import json
import argparse
from typing import Dict, Any

from _qa_common import qa_logger, list_json_files, write_report
from _common import read_json, load_yaml, source_domain


def read_baselines(path: str) -> Dict[str, Dict[str, str]]:
    base: Dict[str, Dict[str, str]] = {}
    if not os.path.exists(path):
        return base
    with open(path, 'r', encoding='utf-8') as f:
        r = csv.DictReader(f)
        for row in r:
            base[row['doc_id']] = row
    return base


def main():
    ap = argparse.ArgumentParser(description='QA: Metadata correctness & date/title/url cross-validation')
    ap.add_argument('--input-glob', default='data/interim/normalized/*.json')
    ap.add_argument('--baselines', default='qa_data/baselines/ground_truth_dates.csv')
    ap.add_argument('--cfg', default='qa_configs/qa.sources.baselines.yaml')
    ap.add_argument('--limit', type=int, default=None)
    ap.add_argument('--out', default='qa_data/outputs/metadata_report.json')
    ap.add_argument('--fail-on', default='auto')
    args = ap.parse_args()

    logger, log_path = qa_logger('qa_metadata_validate')
    paths = list_json_files(args.input_glob, args.limit)
    baselines = read_baselines(args.baselines)
    cfg = load_yaml(args.cfg)
    allow_domains = set(cfg.get('allow_domains', []))

    total = 0
    date_matches = 0
    date_total = 0
    title_matches = 0
    title_total = 0
    domain_ok = 0
    domain_total = 0
    # Coverage & provenance/fallback metrics
    baseline_doc_ids = set()
    prov_counts = {}
    fallback_today = 0
    fallback_any = 0
    top_date_counter = {}
    diffs = []

    for p in paths:
        doc = read_json(p)
        total += 1
        did = doc.get('doc_id')
        bid = baselines.get(did)
        base_date = bid.get('baseline_date') if bid else None
        base_title = bid.get('baseline_title') if bid else None
        base_url = bid.get('baseline_url') if bid else None

        # Date check only when baseline available
        if base_date:
            date_total += 1
            date_ok = (doc.get('publish_date') == base_date)
            if date_ok:
                date_matches += 1
        else:
            date_ok = False
        if base_date:
            baseline_doc_ids.add(did)
        # Title check only when baseline available
        if base_title:
            title_total += 1
            title_ok = ((doc.get('title') or '').strip() == (base_title or '').strip())
            if title_ok:
                title_matches += 1
        else:
            title_ok = False
        # Domain check only when we have a URL to assess
        dom = source_domain(doc.get('final_url') or doc.get('url') or '')
        if dom:
            domain_total += 1
            domain_ok_flag = (dom in allow_domains)
            if domain_ok_flag:
                domain_ok += 1
        else:
            domain_ok_flag = False

        if not (date_ok and title_ok and domain_ok_flag) and len(diffs) < 100:
            diffs.append({
                'doc_id': did,
                'publish_date': doc.get('publish_date'),
                'baseline_date': base_date,
                'title': doc.get('title'),
                'baseline_title': base_title,
                'final_url': doc.get('final_url') or doc.get('url'),
                'domain_ok': domain_ok_flag,
            })
        # Provenance/fallback tracking
        prov = doc.get('publish_date_provenance') or 'unknown'
        prov_counts[prov] = prov_counts.get(prov, 0) + 1
        if prov == 'fallback_today' or doc.get('was_fallback_today'):
            fallback_today += 1
        if prov in ('http_last_modified', 'fallback_today'):
            fallback_any += 1
        # Date histogram for concentration
        pd = doc.get('publish_date')
        if isinstance(pd, str) and pd:
            top_date_counter[pd] = top_date_counter.get(pd, 0) + 1

    # Coverage metrics
    baseline_coverage_rate_overall = (len(baseline_doc_ids) / total) if total else 0.0
    top_share = (max(top_date_counter.values())/total) if (total and top_date_counter) else 0.0

    report = {
        'total_docs': total,
        'date_total': date_total,
        'date_match_rate': round((date_matches/date_total) if date_total else 0.0, 4),
        'title_total': title_total,
        'title_match_rate': round((title_matches/title_total) if title_total else 0.0, 4),
        'domain_total': domain_total,
        'final_url_domain_ok_rate': round((domain_ok/domain_total) if domain_total else 0.0, 4),
        'baseline_coverage_rate_overall': round(baseline_coverage_rate_overall, 4),
        'publish_date_provenance_distribution': prov_counts,
        'fallback_today_rate_overall': round((fallback_today/total) if total else 0.0, 4),
        'fallback_any_rate_overall': round((fallback_any/total) if total else 0.0, 4),
        'top_publish_date_share': round(top_share, 4),
        'examples': diffs,
        'log_path': log_path,
    }
    write_report(args.out, report)
    logger.info(f"Metadata validated: {date_matches} date matches, {title_matches} title matches of {total}")


if __name__ == '__main__':
    main()
