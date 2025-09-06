#!/usr/bin/env python3
import os
import re
import json
import argparse
from typing import Dict, Any

from _qa_common import qa_logger, list_json_files, write_report
from _common import load_yaml, read_json


def validate_doc(doc: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
    errors = []
    missing = []
    enum_viol = []
    type_viol = []

    fields = schema.get('fields', {})
    for key, rule in fields.items():
        if rule.get('required') and (key not in doc or doc.get(key) in (None, '', [])):
            missing.append(key)
            continue
        if key not in doc:
            continue
        val = doc.get(key)
        typ = rule.get('type')
        if typ == 'string' and not isinstance(val, str):
            type_viol.append(key)
        if typ == 'integer' and not isinstance(val, int):
            type_viol.append(key)
        if typ == 'datetime' and not isinstance(val, str):
            type_viol.append(key)
        if typ == 'array[string]':
            if not isinstance(val, list) or any(not isinstance(x, str) for x in val):
                type_viol.append(key)
        if key == 'publish_date' and isinstance(val, str):
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', val):
                type_viol.append(key)
        if 'allowed' in rule and val not in rule.get('allowed', []):
            enum_viol.append({key: str(val)})

    return {
        'missing_fields': missing,
        'enum_violations': enum_viol,
        'type_violations': type_viol,
    }


def main():
    ap = argparse.ArgumentParser(description='QA: Schema & Field Validation for normalized docs')
    ap.add_argument('--input-glob', default='data/interim/normalized/*.json')
    ap.add_argument('--schema', default='configs/metadata.dictionary.yaml')
    ap.add_argument('--limit', type=int, default=None)
    ap.add_argument('--out', default='qa_data/outputs/schema_report.json')
    ap.add_argument('--fail-on', default='auto', help='auto|never|always')
    args = ap.parse_args()

    logger, log_path = qa_logger('qa_schema_validate')
    paths = list_json_files(args.input_glob, args.limit)
    schema = load_yaml(args.schema)

    total = 0
    valid = 0
    examples = []
    missing_breakdown = {}
    enum_viol = []
    type_viol = []

    for p in paths:
        try:
            doc = read_json(p)
        except Exception:
            continue
        total += 1
        res = validate_doc(doc, schema)
        if not res['missing_fields'] and not res['enum_violations'] and not res['type_violations']:
            valid += 1
        else:
            if len(examples) < 20:
                examples.append({'doc_id': doc.get('doc_id'), 'path': p, **res})
            for m in res['missing_fields']:
                missing_breakdown[m] = missing_breakdown.get(m, 0) + 1
            enum_viol.extend(res['enum_violations'])
            type_viol.extend(res['type_violations'])

    valid_pct = (valid / total) if total else 0.0
    report = {
        'total_docs': total,
        'docs_valid': valid,
        'valid_pct': round(valid_pct, 4),
        'missing_fields_breakdown': missing_breakdown,
        'enum_violations': enum_viol[:50],
        'type_violations': type_viol[:50],
        'examples': examples,
        'log_path': log_path,
    }
    write_report(args.out, report)
    logger.info(f"Schema validation: {valid}/{total} valid -> {args.out}")


if __name__ == '__main__':
    main()
