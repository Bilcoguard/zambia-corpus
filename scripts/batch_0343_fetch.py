#!/usr/bin/env python3
"""Batch 0343 — Phase 5 ZMCC ingestion (continuation).

This script ONLY fetches+persists raw HTML+PDF for a slice of TARGETS
(controlled by env START/END indices) so the long-running fetcher can be
split across multiple bash calls without exceeding sandbox timeouts.

Targets (8 candidates, in order):
  0. ZMCC 2026/01 (2026-01-20) — last 2026 ConCourt candidate (deferred at b0342)
  1. ZMCC 2025/33 (2025-12-18)
  2. ZMCC 2025/32 (2025-12-16)
  3. ZMCC 2025/31 (2025-12-10)
  4. ZMCC 2025/30 (2025-12-11)
  5. ZMCC 2025/29 (2025-12-08)
  6. ZMCC 2025/28 (2025-12-05)
  7. ZMCC 2025/27 (2025-12-05)
"""

import hashlib
import json
import os
import pathlib
import re
import time
import urllib.request
from datetime import datetime, timezone

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
RATE_LIMIT_S = 5  # zambialii_seconds_between_requests

ROOT = pathlib.Path("/sessions/charming-dreamy-cori/mnt/corpus")
RAW_DIR = ROOT / "raw" / "zambialii" / "judgments"
WORK = ROOT / "_work" / "b0343"
WORK.mkdir(parents=True, exist_ok=True)

TARGETS = [
    ("zmcc", 2026, 1,  "2026-01-20"),
    ("zmcc", 2025, 33, "2025-12-18"),
    ("zmcc", 2025, 32, "2025-12-16"),
    ("zmcc", 2025, 31, "2025-12-10"),
    ("zmcc", 2025, 30, "2025-12-11"),
    ("zmcc", 2025, 29, "2025-12-08"),
    ("zmcc", 2025, 28, "2025-12-05"),
    ("zmcc", 2025, 27, "2025-12-05"),
]


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def http_get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read()


def slugify(name: str, max_len: int = 50) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s[:max_len].rstrip("-")


def fetch_one(court, year, num, dt):
    raw_year_dir = RAW_DIR / court / str(year)
    raw_year_dir.mkdir(parents=True, exist_ok=True)

    # If we have html+pdf already on disk for this (year, num) skip.
    existing_html = list(raw_year_dir.glob(f"judgment-zm-{year}-{court}-{num:02d}-*.html"))
    existing_pdf = list(raw_year_dir.glob(f"judgment-zm-{year}-{court}-{num:02d}-*.pdf"))
    if existing_html and existing_pdf:
        return {"status": "skip-already", "year": year, "num": num,
                "html": str(existing_html[0]), "pdf": str(existing_pdf[0])}

    html_url = f"https://zambialii.org/akn/zm/judgment/{court}/{year}/{num}/eng@{dt}"
    pdf_url = html_url + "/source.pdf"

    fetched = []
    try:
        html_bytes = http_get(html_url)
    except Exception as e:
        return {"status": "html-fail", "year": year, "num": num,
                "url": html_url, "err": str(e)}
    fetched.append((html_url, len(html_bytes), "judgment-html"))

    # Build slug from h1
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_bytes.decode("utf-8", "ignore"), "html.parser")
    h1 = soup.find("h1")
    title_preview = h1.get_text(" ", strip=True) if h1 else f"zmcc-{year}-{num}"
    cn_preview = re.sub(r"\s*\([^)]*\)\s*\[[^\]]*\][^()]*\([^)]*\)\s*$", "", title_preview).strip()
    cn_preview = re.sub(r"\s*\([^)]*\)\s*$", "", cn_preview).strip()
    cn_preview = re.sub(r"\s*\[[^\]]*\]\s*ZMCC.*$", "", cn_preview).strip()
    slug = slugify(cn_preview, 50)
    base = f"judgment-zm-{year}-{court}-{num:02d}-{slug}"

    html_path = raw_year_dir / f"{base}.html"
    html_path.write_bytes(html_bytes)
    time.sleep(RATE_LIMIT_S)

    try:
        pdf_bytes = http_get(pdf_url)
    except Exception as e:
        return {"status": "pdf-fail", "year": year, "num": num,
                "url": pdf_url, "err": str(e),
                "html": str(html_path), "fetched": fetched}
    fetched.append((pdf_url, len(pdf_bytes), "judgment-pdf"))

    pdf_path = raw_year_dir / f"{base}.pdf"
    pdf_path.write_bytes(pdf_bytes)
    time.sleep(RATE_LIMIT_S)

    return {"status": "ok", "year": year, "num": num,
            "html": str(html_path), "pdf": str(pdf_path),
            "html_url": html_url, "pdf_url": pdf_url,
            "html_sha": "sha256:" + hashlib.sha256(html_bytes).hexdigest(),
            "raw_sha": hashlib.sha256(pdf_bytes).hexdigest(),
            "fetched_at": now_iso(),
            "fetched": fetched}


def main():
    start = int(os.environ.get("START", "0"))
    end = int(os.environ.get("END", str(len(TARGETS))))
    slice_ = TARGETS[start:end]
    out = []
    for t in slice_:
        r = fetch_one(*t)
        out.append(r)
        print(json.dumps({"year": r["year"], "num": r["num"], "status": r["status"]}))

    log = WORK / f"fetch_{start}_{end}.json"
    log.write_text(json.dumps(out, indent=2))
    print(f"WROTE {log}")


if __name__ == "__main__":
    main()
