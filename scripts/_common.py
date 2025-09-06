import os
import re
import sys
import json
import time
import math
import queue
import atexit
import errno
import hashlib
import logging
import threading
from datetime import datetime, timezone, date
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

try:
    import requests
except Exception:  # pragma: no cover
    requests = None

try:
    from bs4 import BeautifulSoup
except Exception:  # pragma: no cover
    BeautifulSoup = None

try:
    import tiktoken
except Exception:  # pragma: no cover
    tiktoken = None

try:
    from langdetect import detect
except Exception:  # pragma: no cover
    detect = None

try:
    import feedparser
except Exception:  # pragma: no cover
    feedparser = None

try:
    from dateutil import parser as dateparser
except Exception:  # pragma: no cover
    dateparser = None


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
DATA_DIR = os.path.join(REPO_ROOT, 'data')
LOG_DIR = os.path.join(REPO_ROOT, 'logs')


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def ensure_parent(path: str):
    ensure_dir(os.path.dirname(path))


def now_ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ts_for_log() -> str:
    return datetime.now().strftime('%Y%m%d_%H%M%S')


def setup_logger(stage: str) -> tuple[logging.Logger, str]:
    ensure_dir(LOG_DIR)
    stage_dir = os.path.join(LOG_DIR, stage)
    ensure_dir(stage_dir)
    ts = ts_for_log()
    log_path = os.path.join(stage_dir, f'{ts}.log')
    logger = logging.getLogger(f'{stage}-{ts}')
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    fh = logging.FileHandler(log_path)
    fh.setFormatter(fmt)
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger, log_path


def parse_iso_date(s: str | None) -> date | None:
    if not s:
        return None
    try:
        if dateparser:
            return dateparser.parse(s).date()
        return datetime.fromisoformat(s).date()
    except Exception:
        return None


def date_to_iso(d: date | None) -> str | None:
    return d.isoformat() if d else None


class RateLimiter:
    def __init__(self, rate_per_sec: float = 6.0):
        self.rate = rate_per_sec
        self.min_interval = 1.0 / rate_per_sec if rate_per_sec > 0 else 0
        self.lock = threading.Lock()
        self.next_time = 0.0

    def acquire(self):
        with self.lock:
            now = time.time()
            wait = max(0.0, self.next_time - now)
            if wait > 0:
                time.sleep(wait)
            self.next_time = max(now, self.next_time) + self.min_interval


def clean_url_params(url: str) -> str:
    try:
        parts = urlparse(url)
        q = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if not k.lower().startswith('utm_')]
        new_parts = parts._replace(query=urlencode(q))
        return urlunparse(new_parts)
    except Exception:
        return url


def source_domain(url: str) -> str:
    try:
        netloc = urlparse(url).netloc.lower()
        # Keep primary domain
        return '.'.join(netloc.split('.')[-2:])
    except Exception:
        return ''


def slugify(text: str, max_len: int = 60) -> str:
    text = text.strip().lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = re.sub(r'-{2,}', '-', text).strip('-')
    return text[:max_len] if max_len else text


def sha1_8(b: bytes) -> str:
    return hashlib.sha1(b).hexdigest()[:8]


def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


_TOKENIZER = None


def token_count(text: str) -> int:
    global _TOKENIZER
    if tiktoken and _TOKENIZER is None:
        try:
            _TOKENIZER = tiktoken.get_encoding('cl100k_base')
        except Exception:
            _TOKENIZER = None
    if _TOKENIZER:
        try:
            return len(_TOKENIZER.encode(text))
        except Exception:
            pass
    # Fallback heuristic: max(words, chars/4)
    words = len(text.split())
    chars = len(text)
    return max(words, chars // 4)


def detect_language(text: str) -> str:
    if detect:
        try:
            lang = detect(text[:1000])
            return 'en' if lang == 'en' else lang
        except Exception:
            pass
    # Heuristic fallback
    ascii_ratio = sum(1 for c in text if ord(c) < 128) / max(1, len(text))
    return 'en' if ascii_ratio > 0.8 else 'und'


def html_to_text(html: str, rules: dict | None = None) -> tuple[str, dict]:
    rules = rules or {}
    if BeautifulSoup is None:
        # crude fallback
        text = re.sub(r'<(script|style)[\s\S]*?</\1>', '', html, flags=re.I)
        text = re.sub(r'<br\s*/?>', '\n', text, flags=re.I)
        text = re.sub(r'</p>', '\n\n', text, flags=re.I)
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip(), {}
    soup = BeautifulSoup(html, 'lxml') if 'lxml' in sys.modules else BeautifulSoup(html, 'html.parser')
    # Drop undesired nodes
    for sel in (rules.get('global', {}) or {}).get('drop_selectors', []):
        for tag in soup.select(sel):
            tag.decompose()
    # Convert breaks/paragraphs to line breaks
    for br in soup.find_all('br'):
        br.replace_with('\n')
    for p in soup.find_all('p'):
        if p.text:
            p.insert_before('\n')
    text = soup.get_text('\n')
    text = re.sub(r'[\t\r]', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    return text.strip(), {}


def read_json(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_json(path: str, obj: dict):
    ensure_parent(path)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False)


def read_text(path: str) -> str:
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()


def write_text(path: str, text: str):
    ensure_parent(path)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def load_yaml(path: str) -> dict:
    import yaml  # local import to avoid hard dep in some scripts
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def doc_id(doctype: str, date_iso: str, slug: str, content_bytes: bytes) -> str:
    return f"crm::{doctype}::{date_iso}::{slug}::{sha1_8(content_bytes)}"


def http_fetch(url: str, logger: logging.Logger, timeout: float = 5.0, method: str = 'GET', allow_redirects: bool = True) -> tuple[int, bytes, dict]:
    headers = {
        'User-Agent': 'Day1Pipeline/1.0 (+https://openai.com)'
    }
    info = {}
    if requests is None:
        import urllib.request
        req = urllib.request.Request(url, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read()
                info['final_url'] = resp.geturl()
                info['status_code'] = resp.status
                info['headers'] = {k.lower(): v for k, v in resp.headers.items()}
                return resp.status, body, info
        except Exception as e:
            logger.warning(f"fetch error {url}: {e}")
            return 0, b'', info
    s = requests.Session()
    try:
        r = s.request(method, url, headers=headers, timeout=timeout, allow_redirects=allow_redirects)
        info['final_url'] = str(r.url)
        info['status_code'] = int(r.status_code)
        info['headers'] = {k.lower(): v for k, v in r.headers.items()}
        return int(r.status_code), r.content or b'', info
    except Exception as e:
        logger.warning(f"fetch error {url}: {e}")
        return 0, b'', info


def guess_title_from_html(html: str) -> str:
    if not html:
        return ''
    m = re.search(r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)["\']', html, re.I)
    if m:
        return m.group(1).strip()
    m = re.search(r'<title>([^<]+)</title>', html, re.I)
    if m:
        return m.group(1).strip()
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.I | re.S)
    if m:
        return re.sub(r'<[^>]+>', '', m.group(1)).strip()
    return ''


def parse_meta_published_time(html: str) -> str | None:
    m = re.search(r'<meta[^>]+property=["\']article:published_time["\'][^>]+content=["\']([^"\']+)["\']', html, re.I)
    if not m:
        m = re.search(r'<time[^>]+datetime=["\']([^"\']+)["\']', html, re.I)
    if m:
        d = parse_iso_date(m.group(1))
        return date_to_iso(d) if d else None
    return None


def make_inventory_row(doc: dict) -> list[str]:
    persona_str = ','.join(doc.get('persona_tags') or [])
    return [
        doc.get('doc_id', ''),
        doc.get('company', ''),
        doc.get('doctype', ''),
        doc.get('title', ''),
        doc.get('publish_date', ''),
        doc.get('url', ''),
        doc.get('final_url', ''),
        doc.get('source_domain', ''),
        doc.get('section', ''),
        doc.get('topic', ''),
        persona_str,
        doc.get('language', ''),
        str(doc.get('word_count', '')),
        str(doc.get('token_count', '')),
        doc.get('ingestion_ts', ''),
        doc.get('hash_sha256', ''),
    ]

