#!/usr/bin/env python3
import os
import json
import glob
import argparse
from datetime import date, timedelta

from _qa_common import qa_logger, write_report, month_bucket
from _common import read_json


def main():
    ap = argparse.ArgumentParser(description='QA: Coverage and recency report')
    ap.add_argument('--norm-glob', default='data/interim/normalized/*.json')
    ap.add_argument('--out', default='qa_data/outputs/coverage_report.json')
    args = ap.parse_args()

    logger, log_path = qa_logger('qa_coverage_report')
    docs = [read_json(p) for p in glob.glob(args.norm_glob)]

    by_doctype = {}
    by_domain = {}
    month_hist = {}
    pr_last12 = 0
    today = date.today()
    last12 = today - timedelta(days=365)

    sec_present = {'10-K': 0, '10-Q': 0, '8-K': 0}

    for d in docs:
        dt = d.get('doctype', '')
        dm = d.get('source_domain', '')
        by_doctype[dt] = by_doctype.get(dt, 0) + 1
        by_domain[dm] = by_domain.get(dm, 0) + 1
        month_hist[month_bucket(d.get('publish_date'))] = month_hist.get(month_bucket(d.get('publish_date')), 0) + 1
        if dt == 'press':
            try:
                y, m, dd = d.get('publish_date', '1900-01-01').split('-')
                docd = date(int(y), int(m), int(dd))
                if docd >= last12:
                    pr_last12 += 1
            except Exception:
                pass
        if d.get('source_domain') == 'sec.gov' and dt in sec_present:
            sec_present[dt] += 1

    report = {
        'total_docs': len(docs),
        'by_doctype': by_doctype,
        'by_source_domain': by_domain,
        'month_histogram': month_hist,
        'press_docs_last_12mo': pr_last12,
        'sec_presence': sec_present,
        'log_path': log_path,
    }
    write_report(args.out, report)
    logger.info(f"Coverage report: docs={len(docs)}, PR last12={pr_last12}")


if __name__ == '__main__':
    main()
