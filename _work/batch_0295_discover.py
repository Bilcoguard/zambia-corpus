"""Batch 0295 discover/probe — minimal upstream refresh.

Probes:
  - zambialii.org/robots.txt  (verify unchanged)
  - zambialii.org/legislation/recent
  - parliament.gov.zm/robots.txt
  - parliament.gov.zm/acts-of-parliament  (page 0)

Compares against on-disk records/acts/**/*.json and reports any novel
modern acts. PROBE-ONLY: no record writes.

robots.txt expected sha256s:
  zambialii:  fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0
  parliament: 278e83bcf567badfebcdea4d5d20ca9898e4449fe4eb2e3b5a08227b4ca9b762

USER_AGENT: KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)
Crawl-delay: 6s zambialii, 11s parliament.
"""
import glob
import hashlib
import json
import os
import re
import ssl
import sys
import time
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup

# Build SSL context with extra certs from scripts/certs/ (per fetch_one.py).
# Needed for parliament.gov.zm (RapidSSL chain not in default trust store).
EXTRA_CERTS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "scripts", "certs",
)
SSL_CTX = ssl.create_default_context()
if os.path.isdir(EXTRA_CERTS_DIR):
    for pem in sorted(glob.glob(os.path.join(EXTRA_CERTS_DIR, "*.pem"))):
        try:
            SSL_CTX.load_verify_locations(cafile=pem)
        except Exception as e:
            print(f"WARN: failed to load {pem}: {e}", file=sys.stderr)
HTTPS_HANDLER = urllib.request.HTTPSHandler(context=SSL_CTX)
OPENER = urllib.request.build_opener(HTTPS_HANDLER)

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "_work"
COSTS_LOG = ROOT / "costs.log"
DATE = "2026-04-27"
BATCH = "0295"

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}

EXPECTED_ZAMBIALII_ROBOTS_SHA = "fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0"
EXPECTED_PARLIAMENT_ROBOTS_SHA = "278e83bcf567badfebcdea4d5d20ca9898e4449fe4eb2e3b5a08227b4ca9b762"

ZAMBIALII_DELAY = 6
PARLIAMENT_DELAY = 11


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def log_cost(url: str, n_bytes: int, kind: str = "probe"):
    rec = {"date": DATE, "url": url, "bytes": n_bytes, "batch": BATCH, "kind": kind}
    with open(COSTS_LOG, "a") as f:
        f.write(json.dumps(rec) + "\n")


def fetch(url: str, save_to: Path, kind: str = "probe", delay_after: float = 0):
    print(f"[fetch] {url}")
    req = urllib.request.Request(url, headers=HEADERS)
    with OPENER.open(req, timeout=30) as resp:
        body = resp.read()
    save_to.write_bytes(body)
    log_cost(url, len(body), kind=kind)
    if delay_after > 0:
        time.sleep(delay_after)
    return body


def main():
    out = {
        "batch": BATCH,
        "date": DATE,
        "tick_start_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "fetches": [],
    }

    # --- zambialii robots ---
    z_robots = fetch("https://zambialii.org/robots.txt",
                     WORK / f"batch_{BATCH}_zambialii_robots.txt",
                     delay_after=ZAMBIALII_DELAY)
    z_robots_sha = sha256(z_robots)
    out["zambialii_robots_sha256"] = z_robots_sha
    out["zambialii_robots_match_expected"] = (z_robots_sha == EXPECTED_ZAMBIALII_ROBOTS_SHA)

    # --- zambialii /legislation/recent ---
    z_recent = fetch("https://zambialii.org/legislation/recent",
                     WORK / f"batch_{BATCH}_zambialii_recent.html",
                     delay_after=ZAMBIALII_DELAY)
    soup = BeautifulSoup(z_recent, "html.parser")
    # Acts: links to /akn/zm/act/... patterns
    act_links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        m = re.search(r"/akn/zm/act/(\d{4})/(\d+)", href)
        if m:
            year = int(m.group(1))
            num = int(m.group(2))
            act_links.append({"year": year, "num": num, "href": href, "text": a.get_text(strip=True)})
    # Dedupe
    seen = set()
    unique_acts = []
    for x in act_links:
        k = (x["year"], x["num"])
        if k in seen:
            continue
        seen.add(k)
        unique_acts.append(x)
    out["zambialii_recent_acts"] = unique_acts

    # --- parliament robots ---
    p_robots = fetch("https://www.parliament.gov.zm/robots.txt",
                     WORK / f"batch_{BATCH}_parliament_robots.txt",
                     delay_after=PARLIAMENT_DELAY)
    p_robots_sha = sha256(p_robots)
    out["parliament_robots_sha256"] = p_robots_sha
    out["parliament_robots_match_expected"] = (p_robots_sha == EXPECTED_PARLIAMENT_ROBOTS_SHA)

    # --- parliament /acts-of-parliament page 0 ---
    p_page = fetch("https://www.parliament.gov.zm/acts-of-parliament",
                   WORK / f"batch_{BATCH}_parliament_p0.html",
                   delay_after=PARLIAMENT_DELAY)
    p_soup = BeautifulSoup(p_page, "html.parser")
    p_text = p_soup.get_text("\n")
    # Pattern: "Act No. <N> of <YYYY>"
    p_matches = set()
    for m in re.finditer(r"Act\s+No\.?\s*(\d+)\s*of\s*(\d{4})", p_text, re.IGNORECASE):
        p_matches.add((int(m.group(2)), int(m.group(1))))
    out["parliament_page0_acts"] = sorted(p_matches)

    # --- existing-set check ---
    on_disk_acts = set()
    for jf in (ROOT / "records" / "acts").rglob("*.json"):
        m = re.search(r"act-zm-(\d{4})-(\d+)", jf.name)
        if m:
            on_disk_acts.add((int(m.group(1)), int(m.group(2))))
    # Fallback: also read citation field for non-canonical filenames
    out["on_disk_acts_count"] = len(on_disk_acts)

    novel_zambialii = []
    for x in unique_acts:
        k = (x["year"], x["num"])
        if k not in on_disk_acts:
            novel_zambialii.append(x)
    novel_parliament = []
    for k in sorted(p_matches):
        if k not in on_disk_acts:
            novel_parliament.append({"year": k[0], "num": k[1]})

    # Fall through to JSON content for non-canonical filenames
    def fallthrough_check(year, num):
        # Read all JSON files for this year (if any) and check citation
        ydir = ROOT / "records" / "acts" / str(year)
        if not ydir.exists():
            return False
        cite_pat = re.compile(rf"\bAct\s+No\.?\s*{num}\s+of\s+{year}\b", re.IGNORECASE)
        cite_pat2 = re.compile(rf'"id":\s*"act-zm-{year}-0*{num}-')
        for jf in ydir.glob("*.json"):
            try:
                content = jf.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            if cite_pat.search(content) or cite_pat2.search(content):
                return True
        return False

    novel_zambialii_true = [x for x in novel_zambialii if not fallthrough_check(x["year"], x["num"])]
    novel_parliament_true = [x for x in novel_parliament if not fallthrough_check(x["year"], x["num"])]

    out["novel_zambialii_raw"] = novel_zambialii
    out["novel_parliament_raw"] = novel_parliament
    out["novel_zambialii_true"] = novel_zambialii_true
    out["novel_parliament_true"] = novel_parliament_true
    out["tick_end_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    (WORK / f"batch_{BATCH}_probe.json").write_text(json.dumps(out, indent=2))
    print(json.dumps({
        "zambialii_robots_match": out["zambialii_robots_match_expected"],
        "parliament_robots_match": out["parliament_robots_match_expected"],
        "zambialii_recent_count": len(unique_acts),
        "parliament_page0_count": len(p_matches),
        "novel_zambialii_true": len(novel_zambialii_true),
        "novel_parliament_true": len(novel_parliament_true),
        "on_disk_acts_count": len(on_disk_acts),
    }, indent=2))


if __name__ == "__main__":
    main()
