#!/usr/bin/env python3
"""Batch 0348 — Phase 5 ZMCC ingestion.

Slice next-after b0347: the only two remaining ZMCC 2025 numeric slots
(2025/{2,1}) plus a step into ZMCC 2024 most-recent-first (2024/{27..22})
to fill the 8-record batch budget.

Frozen from b0347:
  * Dateless canonical URL (`/akn/zm/judgment/{court}/{year}/{num}/eng`),
    dates discovered from the ZambiaLII 302-redirect.
  * 5s rate limit between fetches.
  * UA per approvals.yaml.
  * No re-fetch if HTML+PDF already on disk.
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

HERE = pathlib.Path(__file__).resolve()
ROOT = HERE.parent.parent
RAW_DIR = ROOT / "raw" / "zambialii" / "judgments"
WORK = ROOT / "_work" / "b0348"
WORK.mkdir(parents=True, exist_ok=True)

# Numeric sequence only — date is discovered at fetch time.
TARGETS = [
    ("zmcc", 2025, 2),
    ("zmcc", 2025, 1),
    ("zmcc", 2024, 27),
    ("zmcc", 2024, 26),
    ("zmcc", 2024, 25),
    ("zmcc", 2024, 24),
    ("zmcc", 2024, 23),
    ("zmcc", 2024, 22),
]


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def http_get(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read(), r.url


def slugify(name: str, max_len: int = 50) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s[:max_len].rstrip("-")


def fetch_one(court, year, num):
    raw_year_dir = RAW_DIR / court / str(year)
    raw_year_dir.mkdir(parents=True, exist_ok=True)

    existing_html = list(raw_year_dir.glob(f"judgment-zm-{year}-{court}-{num:02d}-*.html"))
    existing_pdf = list(raw_year_dir.glob(f"judgment-zm-{year}-{court}-{num:02d}-*.pdf"))
    if existing_html and existing_pdf:
        return {"status": "skip-already", "year": year, "num": num,
                "html": str(existing_html[0]), "pdf": str(existing_pdf[0])}

    dateless_url = f"https://zambialii.org/akn/zm/judgment/{court}/{year}/{num}/eng"

    try:
        html_bytes, final_url = http_get(dateless_url)
    except Exception as e:
        return {"status": "html-fail", "year": year, "num": num,
                "url": dateless_url, "err": str(e)}

    m = re.search(r"/eng@(\d{4}-\d{2}-\d{2})$", final_url)
    if not m:
        return {"status": "no-date-redirect", "year": year, "num": num,
                "url": dateless_url, "final_url": final_url}
    dt = m.group(1)
    html_url = final_url
    pdf_url = html_url + "/source.pdf"

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_bytes.decode("utf-8", "ignore"), "html.parser")
    h1 = soup.find("h1")
    title_preview = h1.get_text(" ", strip=True) if h1 else f"{court}-{year}-{num}"
    cn_preview = re.sub(r"\s*\([^)]*\)\s*\[[^\]]*\][^()]*\([^)]*\)\s*$", "", title_preview).strip()
    cn_preview = re.sub(r"\s*\([^)]*\)\s*$", "", cn_preview).strip()
    cn_preview = re.sub(r"\s*\[[^\]]*\]\s*ZMCC.*$", "", cn_preview).strip()
    slug = slugify(cn_preview, 50)
    base = f"judgment-zm-{year}-{court}-{num:02d}-{slug}"

    html_path = raw_year_dir / f"{base}.html"
    html_path.write_bytes(html_bytes)
    time.sleep(RATE_LIMIT_S)

    try:
        pdf_bytes, _ = http_get(pdf_url)
    except Exception as e:
        return {"status": "pdf-fail", "year": year, "num": num,
                "url": pdf_url, "err": str(e),
                "html": str(html_path)}

    pdf_path = raw_year_dir / f"{base}.pdf"
    pdf_path.write_bytes(pdf_bytes)
    time.sleep(RATE_LIMIT_S)

    return {"status": "ok", "year": year, "num": num, "date": dt,
            "html": str(html_path), "pdf": str(pdf_path),
            "html_url": html_url, "pdf_url": pdf_url,
            "html_sha": "sha256:" + hashlib.sha256(html_bytes).hexdigest(),
            "raw_sha": hashlib.sha256(pdf_bytes).hexdigest(),
            "fetched_at": now_iso(),
            "html_bytes": len(html_bytes), "pdf_bytes": len(pdf_bytes)}


def main():
    start = int(os.environ.get("START", "0"))
    end = int(os.environ.get("END", str(len(TARGETS))))
    slice_ = TARGETS[start:end]
    out = []
    for t in slice_:
        r = fetch_one(*t)
        out.append(r)
        print(json.dumps({"year": r["year"], "num": r["num"],
                          "status": r["status"],
                          "date": r.get("date"),
                          "html_bytes": r.get("html_bytes"),
                          "pdf_bytes": r.get("pdf_bytes")}))

    log = WORK / f"fetch_{start}_{end}.json"
    log.write_text(json.dumps(out, indent=2))
    print(f"WROTE {log}")


if __name__ == "__main__":
    main()
