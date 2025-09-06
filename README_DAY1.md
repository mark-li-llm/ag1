# Salesforce Day‑1 Data Pipeline

This repository implements the Day‑1 data & schema pipeline for Salesforce, Inc. (CRM) public materials per the provided blueprint. It provides:

- Frozen configs under `configs/`
- Fetchers for SEC filings, Investor News, Newsroom RSS, Product, Dev Docs, Help, Wikipedia
- Normalization, metadata extraction, SEC section parsing
- Chunking and deduplication
- Link health verification
- Inventory CSV, eval seed set, and Day‑1 verification report

## Quickstart

1) Python 3.10+

2) Install dependencies (optional libs are auto‑detected; scripts will degrade gracefully when missing):

```
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

3) Run in order (dry run first):

```
# Fetch (respect caps and windows from configs)
python scripts/fetch_sec_filings.py --since 2024-01-01 --limit 10 --dry-run
python scripts/fetch_investor_news.py --since 2024-01-01 --limit 30 --dry-run
python scripts/fetch_newsroom_rss.py --since 2024-01-01 --limit 30 --dry-run
python scripts/fetch_product_docs.py --limit 3 --dry-run
python scripts/fetch_dev_docs.py --limit 4 --dry-run
python scripts/fetch_help_docs.py --limit 1 --dry-run
python scripts/fetch_wikipedia.py --limit 1 --dry-run

# Normalize & metadata
python scripts/normalize_html.py --limit 99999
python scripts/parse_sec_structures.py --limit 99999
python scripts/extract_metadata.py --limit 99999

# Chunk & dedupe
python scripts/chunk_documents.py --limit 99999
python scripts/dedupe_chunks.py --limit 99999

# Link health (must be 100%)
python scripts/link_health_check.py --limit 99999

# Inventory, eval, verification
python scripts/build_eval_seed.py --limit 99999
python scripts/verify_day1_milestones.py
```

Logs are written under `logs/<stage>/YYYYMMDD_HHMMSS.log`. All scripts accept:

- `--dry-run` (no writes)
- `--limit N`
- `--since YYYY-MM-DD`
- `--until YYYY-MM-DD`
- `--concurrency K`

## Acceptance Gates (Day‑1)

- total_docs ≥ 80 with publish_date; ≤ 120 fetched
- Dedupe ratio ≤ 15%
- Link health 100%
- Metadata completeness ≥ 98%
- PR recency: ≥ 15 docs since 2024‑01‑01 and ≥ 8 in last 12 months

See `configs/` for frozen rules and dictionaries.

