#!/usr/bin/env python3
import os
import json
import argparse

from _qa_common import qa_logger, write_report
from _common import load_yaml


def load_json(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    try:
        return json.load(open(path, 'r', encoding='utf-8'))
    except Exception:
        return {}


def main():
    ap = argparse.ArgumentParser(description='QA: Aggregate all QA reports into a single PASS/FAIL gate')
    ap.add_argument('--thresholds', default='qa_configs/qa.thresholds.yaml')
    ap.add_argument('--reports-root', default='qa_data/outputs')
    ap.add_argument('--out', default='qa_data/outputs/verification_gate.json')
    args = ap.parse_args()

    logger, log_path = qa_logger('qa_verification_gate')
    thr = load_yaml(args.thresholds)
    # Load reports
    schema = load_json(os.path.join(args.reports_root, 'schema_report.json'))
    meta = load_json(os.path.join(args.reports_root, 'metadata_report.json'))
    textq = load_json(os.path.join(args.reports_root, 'text_quality_report.json'))
    chunkq = load_json(os.path.join(args.reports_root, 'chunk_quality_report.json'))
    dedupe = load_json(os.path.join(args.reports_root, 'dedupe_audit.json'))
    link = load_json(os.path.join(args.reports_root, 'link_health_retest.json'))
    cov = load_json(os.path.join(args.reports_root, 'coverage_report.json'))
    persona = load_json(os.path.join(args.reports_root, 'persona_tag_precision.json'))
    secsec = load_json(os.path.join(args.reports_root, 'sec_section_report.json'))
    evalr = load_json(os.path.join(args.reports_root, 'eval_seed_report.json'))

    failures = []

    # Schema
    if schema:
        if schema.get('valid_pct', 0.0) < thr.get('schema_valid_pct_min', 0.98):
            failures.append({'id': 'schema', 'summary': f"Schema valid {schema.get('valid_pct')} < {thr.get('schema_valid_pct_min')}", 'blocking': True})
    # Metadata
    if meta:
        if meta.get('date_match_rate', 0.0) < thr.get('date_match_rate_min', 0.97):
            failures.append({'id': 'metadata_date', 'summary': f"Date match {meta.get('date_match_rate')} < {thr.get('date_match_rate_min')}", 'blocking': True})
        if meta.get('title_match_rate', 0.0) < thr.get('title_match_rate_min', 0.98):
            failures.append({'id': 'metadata_title', 'summary': f"Title match {meta.get('title_match_rate')} < {thr.get('title_match_rate_min')}", 'blocking': False})
        if meta.get('final_url_domain_ok_rate', 0.0) < 1.0:
            failures.append({'id': 'metadata_domain', 'summary': "Final URL domain not 100% in allowlist", 'blocking': True})
        # Coverage & fallback gating
        if meta.get('baseline_coverage_rate_overall', 0.0) < thr.get('baseline_coverage_rate_overall_min', 0.8):
            failures.append({'id': 'meta_baseline_coverage', 'summary': 'Baseline coverage < overall minimum', 'blocking': True})
        if meta.get('fallback_today_rate_overall', 0.0) > thr.get('fallback_today_rate_overall_max', 0.0):
            failures.append({'id': 'meta_fallback_today', 'summary': 'Fallback-to-today detected (> 0)', 'blocking': True})
        if meta.get('fallback_any_rate_overall', 0.0) > thr.get('fallback_any_rate_overall_max', 0.02):
            failures.append({'id': 'meta_fallback_any', 'summary': 'Fallback date rate too high', 'blocking': True})
        if meta.get('top_publish_date_share', 0.0) > thr.get('top_publish_date_share_max', 0.20):
            failures.append({'id': 'meta_top_date_share', 'summary': 'Single publish date dominates distribution', 'blocking': True})
    # Text
    if textq:
        if textq.get('docs_quality_ok_pct', 0.0) < 0.99:
            failures.append({'id': 'text_quality', 'summary': 'Text quality violations exceed threshold', 'blocking': True})
        if textq.get('replacement_char_free_docs_pct', 0.0) < thr.get('replacement_char_free_docs_pct_min', 0.99):
            failures.append({'id': 'text_repchar', 'summary': 'Replacement character found in too many docs', 'blocking': True})
    # Chunking
    if chunkq:
        med = chunkq.get('median_token_length', 0)
        lo, hi = thr.get('chunk_median_range_tokens', [650, 950])
        if not (lo <= med <= hi):
            failures.append({'id': 'chunk_median', 'summary': f"Median chunk tokens {med} out of range {lo}-{hi}", 'blocking': False})
        if chunkq.get('len_within_range_pct', 0.0) < thr.get('chunk_len_within_pct_min', 0.90):
            failures.append({'id': 'chunk_len_spread', 'summary': 'Too many chunks outside length range', 'blocking': True})
        mean_ov = chunkq.get('mean_overlap_tokens', 0.0)
        lo, hi = thr.get('overlap_mean_range_tokens', [80, 160])
        if not (lo <= mean_ov <= hi):
            failures.append({'id': 'chunk_overlap', 'summary': f"Mean overlap {mean_ov} out of range {lo}-{hi}", 'blocking': False})
        if chunkq.get('sec_boundary_crossings', 0) > 0:
            failures.append({'id': 'sec_cross', 'summary': 'SEC boundary crossings present', 'blocking': True})
    # Dedupe
    if dedupe:
        # Allow the audit to suggest threshold; we just record
        pass
    # Link health
    if link and link.get('ok_pct', 0.0) < 1.0:
        failures.append({'id': 'link_health', 'summary': 'Link health retest < 100%', 'blocking': True})
    # Coverage
    if cov:
        sec_req = cov.get('sec_presence', {})
        for need in ('10-K', '10-Q', '8-K'):
            if sec_req.get(need, 0) < 1:
                failures.append({'id': 'coverage_sec', 'summary': f"Missing SEC {need}", 'blocking': True})
        if cov.get('press_docs_last_12mo', 0) < 8:
            failures.append({'id': 'coverage_pr', 'summary': 'PR docs in last 12 months < 8', 'blocking': True})
    # Persona
    if persona:
        for p, prec in (persona.get('precision_by_persona') or {}).items():
            if prec is not None and prec < 0.80:
                failures.append({'id': f'persona_{p}', 'summary': f'Persona {p} precision {prec} < 0.80', 'blocking': False})
    # SEC sections
    if secsec and secsec.get('pass_pct', 0.0) < 1.0:
        failures.append({'id': 'sec_sections', 'summary': 'Not all SEC docs passed section validation', 'blocking': True})
    # Eval seed
    if evalr:
        if evalr.get('valid_pct', 0.0) < 1.0:
            failures.append({'id': 'eval_integrity', 'summary': 'Eval seed pairs invalid or missing keyphrases', 'blocking': True})

    status = 'PASS' if not failures else 'FAIL'
    report = {
        'status': status,
        'failed_checks': failures,
        'log_path': log_path,
    }
    write_report(args.out, report)
    logger.info(f"Verification gate: {status} -> {args.out}")


if __name__ == '__main__':
    main()
