#!/usr/bin/env python3
"""Batch 0353 — Phase 5 ZMCC ingestion (continuation).

Probes ZMCC 2023 most-recent-first, starting from 2023/30 and walking
DESC. Stops after up to 8 successful fetches OR after 5 consecutive
404s (interpreted as "we've walked past the top"). The 8-cap is the
MAX_BATCH_SIZE from the tick prompt.

Frozen from b0348/b0351 fetcher logic:
  * Dateless canonical URL (`/akn/zm/judgment/{court}/{year}/{num}/eng`),
    dates discovered from the ZambiaLII 302-redirect.
  * 5s rate limit between fetches (including failed/404 probes).
  * UA per approvals.yaml.
  * No re-fetch if HTML+PDF already on disk.

NEW: HTTPError handling — 404s mean "this number does not exist on
ZambiaLII" (typical when probing past the top of a year). Logged
separately and counted toward the consecutive-404 stop condition.
"""

import hashlib
import json
import os
import pathlib
import re
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
RATE_LIMIT_S = 5  # zambialii_seconds_between_requests

HERE = pathlib.Path(__file__).resolve()
ROOT = HERE.parent.parent
RAW_DIR = ROOT / "raw" / "zambialii" / "judgments"
WORK = ROOT / "_work" / "b0353"
WORK.mkdir(parents=True, exist_ok=True)

COURT = "zmcc"
YEAR = 2023
PROBE_FROM = 19  # educated guess; ZMCC 2024 had 27, ZMCC 2025 had 33
WALK_TO = 1
MAX_HITS = 8           # MAX_BATCH_SIZE per tick prompt
STOP_ON_404_RUN = 5    # consecutive 404s => past the top of the year


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def http_get(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read(), r.url, r.status


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
        html_bytes, final_url, status = http_get(dateless_url)
    except urllib.error.HTTPError as e:
        return {"status": "http-error", "year": year, "num": num,
                "url": dateless_url, "code": e.code}
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
        pdf_bytes, _, _ = http_get(pdf_url)
    except urllib.error.HTTPError as e:
        return {"status": "pdf-http-error", "year": year, "num": num,
                "url": pdf_url, "code": e.code,
                "html": str(html_path)}
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
    probe_from = int(os.environ.get("PROBE_FROM", str(PROBE_FROM)))
    walk_to = int(os.environ.get("WALK_TO", str(WALK_TO)))
    max_hits = int(os.environ.get("MAX_HITS", str(MAX_HITS)))
    stop_404 = int(os.environ.get("STOP_ON_404_RUN", str(STOP_ON_404_RUN)))

    out = []
    hits = 0
    consecutive_404 = 0
    n = probe_from
    while n >= walk_to and hits < max_hits and consecutive_404 < stop_404:
        r = fetch_one(COURT, YEAR, n)
        out.append(r)
        print(json.dumps({"year": r["year"], "num": r["num"],
                          "status": r["status"],
                          "code": r.get("code"),
                          "date": r.get("date"),
                          "html_bytes": r.get("html_bytes"),
                          "pdf_bytes": r.get("pdf_bytes")}))
        if r["status"] == "ok" or r["status"] == "skip-already":
            hits += 1
            consecutive_404 = 0
        elif r["status"] == "http-error" and r.get("code") == 404:
            consecutive_404 += 1
            time.sleep(RATE_LIMIT_S)  # rate-limit 404s too
        else:
            # Other failures — count as a non-hit but don't trip 404 counter
            time.sleep(RATE_LIMIT_S)
        n -= 1

    log = WORK / f"fetch_probe_{probe_from}_walk_{walk_to}.json"
    log.write_text(json.dumps({
        "started_walk_from": probe_from,
        "stopped_at_n": n + 1,
        "hits": hits,
        "consecutive_404_at_stop": consecutive_404,
        "results": out,
    }, indent=2))
    print(f"WROTE {log}")
    print(f"SUMMARY: hits={hits} stop_n={n+1} consecutive_404={consecutive_404}")


if __name__ == "__main__":
    main()
