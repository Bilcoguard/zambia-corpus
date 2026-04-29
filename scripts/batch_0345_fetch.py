#!/usr/bin/env python3
"""Batch 0345 — Phase 5 ZMCC ingestion (continuation of ZMCC 2025 sweep).

Sliceable fetcher (START/END env). Persists raw HTML+PDF for 8 ZMCC 2025
candidates, going most-recent-first from 2025/26 backwards (the next slice
after b0343's 2025/{27..33}+2026/01).

Targets (8 candidates, in order):
  0. ZMCC 2025/26 (2025-11-18) — Jayesh Shah v Attorney General
  1. ZMCC 2025/25 (2025-12-04) — Tresford Chali v Attorney General
  2. ZMCC 2025/24 (2025-11-28) — LAZ v Speaker of the National Assembly
  3. ZMCC 2025/23 (2025-11-27) — Emmanuel Kayuni v ...
  4. ZMCC 2025/22 (2025-11-27) — Sean Tembo (Tonse Alliance) v AG
  5. ZMCC 2025/21 (2025-11-25) — LAZ and Ors v AG (2025/CCZ/0029)
  6. ZMCC 2025/20 (2025-10-03) — Edward Bwalya Phiri v AG
  7. ZMCC 2025/19 (2025-09-30) — BetBio Zambia Ltd v AG

Source URLs follow the akn pattern:
    https://zambialii.org/akn/zm/judgment/zmcc/{year}/{num}/eng@{date}
PDFs at the same URL with /source.pdf appended.

Honours 5s zambialii_seconds_between_requests rate limit. UA per
approvals.yaml. No re-fetch if HTML+PDF already on disk.
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

# Detect the workspace mount root from the script's location, so the
# script works under any sandbox session name.
HERE = pathlib.Path(__file__).resolve()
ROOT = HERE.parent.parent
RAW_DIR = ROOT / "raw" / "zambialii" / "judgments"
WORK = ROOT / "_work" / "b0345"
WORK.mkdir(parents=True, exist_ok=True)

TARGETS = [
    ("zmcc", 2025, 26, "2025-11-18"),
    ("zmcc", 2025, 25, "2025-12-04"),
    ("zmcc", 2025, 24, "2025-11-28"),
    ("zmcc", 2025, 23, "2025-11-27"),
    ("zmcc", 2025, 22, "2025-11-27"),
    ("zmcc", 2025, 21, "2025-11-25"),
    ("zmcc", 2025, 20, "2025-10-03"),
    ("zmcc", 2025, 19, "2025-09-30"),
]


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def http_get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read()


def slugify(name: str, max_len: int = 50) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s[:max_len].rstrip("-")


def fetch_one(court, year, num, dt):
    raw_year_dir = RAW_DIR / court / str(year)
    raw_year_dir.mkdir(parents=True, exist_ok=True)

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
