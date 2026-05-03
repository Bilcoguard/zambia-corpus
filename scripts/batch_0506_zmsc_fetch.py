#!/usr/bin/env python3
"""Batch 0506 — judgment-ingestion-worker dedicated tick.

Phase 5 (Phase 5 already procedurally complete; this is the
dedicated post-Phase-5 judgment ingestion task per Peter's
2026-05-03 directive).

Fetches missing ZMSC judgments using the canonical URL pattern
established by existing zmsc records on disk:

    https://zambialii.org/akn/zm/judgment/zmsc/{year}/{num}/eng

then follows the 302 to /eng@YYYY-MM-DD/. The PDF is at .../source.pdf.

Rate-limit 5s per zambialii_seconds_between_requests in approvals.yaml.
"""
import hashlib
import json
import pathlib
import re
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
RATE_LIMIT_S = 5

HERE = pathlib.Path(__file__).resolve()
ROOT = HERE.parent.parent
RAW_DIR = ROOT / "raw" / "zambialii" / "judgments"
WORK = ROOT / "_work" / "b0504"
WORK.mkdir(parents=True, exist_ok=True)
TARGETS = WORK / "targets.json"


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def http_get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read(), r.url, r.status


def slugify(name, max_len=50):
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
    cn = title_preview
    cn = re.sub(r"\s*\([^)]*\)\s*\[[^\]]*\][^()]*\([^)]*\)\s*$", "", cn).strip()
    cn = re.sub(r"\s*\([^)]*\)\s*$", "", cn).strip()
    cn = re.sub(r"\s*\[[^\]]*\]\s*ZMSC.*$", "", cn).strip()
    slug = slugify(cn, 50)
    base = f"judgment-zm-{year}-{court}-{num:02d}-{slug}"

    html_path = raw_year_dir / f"{base}.html"
    html_path.write_bytes(html_bytes)
    time.sleep(RATE_LIMIT_S)

    try:
        pdf_bytes, _, _ = http_get(pdf_url)
    except urllib.error.HTTPError as e:
        return {"status": "pdf-http-error", "year": year, "num": num,
                "url": pdf_url, "code": e.code, "html": str(html_path)}
    except Exception as e:
        return {"status": "pdf-fail", "year": year, "num": num,
                "url": pdf_url, "err": str(e), "html": str(html_path)}

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
    targets = json.loads(TARGETS.read_text())
    results = []
    for t in targets:
        r = fetch_one(t["court"], int(t["year"]), int(t["num"]))
        results.append(r)
        print(json.dumps({
            "court": t["court"], "year": t["year"], "num": t["num"],
            "status": r["status"], "code": r.get("code"),
            "date": r.get("date"), "html_bytes": r.get("html_bytes"),
            "pdf_bytes": r.get("pdf_bytes"),
        }))
    (WORK / "fetch_results.json").write_text(json.dumps(results, indent=2))
    ok = sum(1 for r in results if r["status"] in ("ok", "skip-already"))
    print(f"SUMMARY: ok/skip={ok}/{len(results)}")


if __name__ == "__main__":
    main()
