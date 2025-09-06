#!/usr/bin/env python3
import os
import json
import glob
import random
import argparse

from _qa_common import qa_logger, write_report
from _common import read_json, http_fetch, source_domain


def main():
    ap = argparse.ArgumentParser(description='QA: Link health stability retest')
    ap.add_argument('--link-report', default='data/final/reports/link_health.json')
    ap.add_argument('--norm-glob', default='data/interim/normalized/*.json')
    ap.add_argument('--sample-frac', type=float, default=0.10)
    ap.add_argument('--out', default='qa_data/outputs/link_health_retest.json')
    args = ap.parse_args()

    logger, log_path = qa_logger('qa_link_health_retest')
    prior = read_json(args.link_report) if os.path.exists(args.link_report) else {'summary': []}
    docs = [read_json(p) for p in glob.glob(args.norm_glob)]
    url_map = {d.get('doc_id'): (d.get('url') or d.get('final_url')) for d in docs}

    sample = []
    # include all previously failing or redirected
    for r in prior.get('summary', []):
        if r.get('status') != 200:
            sample.append(r.get('url'))
    # random 10%
    urls = [u for u in url_map.values() if u]
    random.seed(42)
    k = max(1, int(len(urls) * args.sample_frac))
    sample.extend(random.sample(urls, min(k, len(urls))))
    sample = list(dict.fromkeys(sample))  # dedupe

    results = []
    ok = 0
    for url in sample:
        status, _, info = http_fetch(url, logger, timeout=5.0, method='GET')
        if status != 200:
            status, _, info = http_fetch(url, logger, timeout=5.0, method='HEAD')
        dom_ok = source_domain(info.get('final_url') or url) in {
            'sec.gov','investor.salesforce.com','salesforce.com','developer.salesforce.com','help.salesforce.com','wikipedia.org'
        }
        ok += 1 if (status == 200 and dom_ok) else 0
        results.append({'url': url, 'status': status, 'final_url': info.get('final_url') or url, 'domain_ok': dom_ok})

    report = {
        'tested': len(sample),
        'ok': ok,
        'ok_pct': round((ok/max(1,len(sample))), 4),
        'results': results[:500],
        'log_path': log_path,
    }
    write_report(args.out, report)
    logger.info(f"Link retest OK {ok}/{len(sample)} -> {args.out}")


if __name__ == '__main__':
    main()
