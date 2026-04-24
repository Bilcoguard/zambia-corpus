#!/usr/bin/env python3
"""
Batch 0174 — Phase 4 sis_corporate sub-phase, discovery probe.

Per batch 0173 next-tick plan: continue sis_corporate with the next wave of
candidates from ZambiaLII /legislation/subsidiary listings (PACRA, Companies
Act 2017 SIs, Banking and Financial Services Act SIs, Pensions and Insurance
SIs, Securities Act SIs).

This is a DISCOVERY-only batch — fetch a single ZambiaLII subsidiary
listing page (page 4, since pages 1-3 were used in batch 0173), parse out
SI candidates, filter against records/sis HEAD (existing JSON files), then
classify by corporate-keyword match. No ingest this batch — surfaces
candidates for next tick.

Wall-clock guard: ~3 minutes total (single fetch + parse + report).

Workspace path uses os.getcwd() per batch-0173 next-tick fix item.

Robots.txt audit: /legislation/subsidiary is Allow: / under zambialii.org
robots.txt; Crawl-delay: 5s honoured (single fetch this batch). No
/search/ or /api/ endpoints used.
"""

import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from html.parser import HTMLParser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch_one import fetch, log_provenance  # noqa: E402

BATCH_NUM = "0174"
USER_AGENT = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
PARSER_VERSION = "0.5.0"

WORKSPACE = os.getcwd()
RAW_DIR = os.path.join(WORKSPACE, "raw", "zambialii", "discovery")
RECORDS_DIR = os.path.join(WORKSPACE, "records", "sis")
COSTS_LOG = os.path.join(WORKSPACE, "costs.log")
REPORTS_DIR = os.path.join(WORKSPACE, "reports")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

PAGE_NUM = 4
LISTING_URL = f"https://zambialii.org/legislation/subsidiary?page={PAGE_NUM}"
RAW_PATH = os.path.join(RAW_DIR, f"subsidiary-page-{PAGE_NUM:02d}.html")

# Corporate-relevance keyword filter for sis_corporate sub-phase. Lowercase
# substring match against title text.
CORPORATE_KEYWORDS = [
    "compan",          # companies, corporate
    "corporate",
    "pacra",
    "patent",
    "trademark",
    "trade mark",
    "intellectual property",
    "bank",            # banking, bank of zambia
    "financial",
    "securities",
    "stock exchange",
    "capital market",
    "insur",           # insurance, reinsurance
    "pension",
    "procurement",
    "anti-money",
    "money launder",
    "financial intelligence",
    "competition",
    "consumer protection",
    "investment",
]


def utc_now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def append_costs(entry):
    with open(COSTS_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")


class SubsidiaryListingParser(HTMLParser):
    """Parse ZambiaLII /legislation/subsidiary listing page.

    Each listing entry is an <a href="/akn/zm/act/si/YYYY/N">Title</a>
    inside the document list. We collect every such (year, num, title)
    tuple.
    """

    def __init__(self):
        super().__init__()
        self.in_a = False
        self.cur_href = None
        self.cur_text_parts = []
        self.results = []  # list of (year, num, title, href)

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = None
            for k, v in attrs:
                if k == "href":
                    href = v
                    break
            if href and re.match(r"^/akn/zm/act/si/\d{4}/\d+", href):
                self.in_a = True
                self.cur_href = href
                self.cur_text_parts = []

    def handle_endtag(self, tag):
        if tag == "a" and self.in_a:
            text = " ".join("".join(self.cur_text_parts).split()).strip()
            m = re.match(r"^/akn/zm/act/si/(\d{4})/(\d+)", self.cur_href)
            if m and text:
                year = int(m.group(1))
                num = int(m.group(2))
                self.results.append((year, num, text, self.cur_href))
            self.in_a = False
            self.cur_href = None
            self.cur_text_parts = []

    def handle_data(self, data):
        if self.in_a:
            self.cur_text_parts.append(data)


def existing_si_keys():
    """Build set of (year, num) tuples already represented in records/sis.

    Filename pattern: si-zm-YYYY-NNN-<slug>.json. Returns the set.
    """
    keys = set()
    if not os.path.isdir(RECORDS_DIR):
        return keys
    for root, _dirs, files in os.walk(RECORDS_DIR):
        for fn in files:
            if not fn.startswith("si-zm-"):
                continue
            m = re.match(r"^si-zm-(\d{4})-(\d{1,3})-", fn)
            if m:
                keys.add((int(m.group(1)), int(m.group(2))))
    return keys


def main():
    t0 = time.monotonic()
    started = utc_now_iso()
    print(f"[{started}] batch_0174 starting in {WORKSPACE}", flush=True)

    # 1. Fetch listing page 4 (single fetch, no rate-limit wait needed since
    # this is the first ZambiaLII fetch this tick)
    print(f"FETCH {LISTING_URL}", flush=True)
    res = fetch(LISTING_URL, timeout=30)
    if res["error"] or res["status"] != 200:
        msg = f"fetch failed: status={res['status']} error={res['error']}"
        print(msg)
        return {"status": "fetch_failed", "msg": msg}

    body = res["_body_bytes"]
    sha = res["sha256"]
    with open(RAW_PATH, "wb") as f:
        f.write(body)
    print(f"saved {RAW_PATH} ({len(body)} bytes, sha256={sha[:16]}...)", flush=True)

    # provenance + costs entries
    log_provenance(res)
    append_costs({
        "date": started[:10],
        "url": LISTING_URL,
        "bytes": len(body),
        "batch": BATCH_NUM,
        "fetch_n": "discovery-1",
    })

    # 2. Parse listings
    parser = SubsidiaryListingParser()
    parser.feed(body.decode("utf-8", errors="replace"))
    listings = parser.results
    # dedupe by (year, num) keeping first title
    seen = {}
    for year, num, title, href in listings:
        k = (year, num)
        if k not in seen:
            seen[k] = (title, href)
    unique = sorted(seen.items())
    print(f"parsed {len(listings)} <a> tags -> {len(unique)} unique (year,num)", flush=True)

    # 3. Filter against existing records/sis HEAD
    existing = existing_si_keys()
    novel = [(k, v) for (k, v) in unique if k not in existing]
    print(f"existing si records: {len(existing)}; novel slots: {len(novel)}", flush=True)

    # 4. Corporate-keyword classification
    corporate = []
    other = []
    for (year, num), (title, href) in novel:
        tl = title.lower()
        if any(kw in tl for kw in CORPORATE_KEYWORDS):
            matched = [kw for kw in CORPORATE_KEYWORDS if kw in tl]
            corporate.append({
                "year": year, "num": num, "title": title,
                "href": href, "matched_keywords": matched,
            })
        else:
            other.append({"year": year, "num": num, "title": title, "href": href})

    # 5. Write batch report
    report_path = os.path.join(REPORTS_DIR, f"batch-{BATCH_NUM}.md")
    elapsed = time.monotonic() - t0
    lines = [
        f"# Batch {BATCH_NUM} — Phase 4 sis_corporate discovery probe",
        "",
        f"- started: {started}",
        f"- finished: {utc_now_iso()}",
        f"- elapsed: {elapsed:.1f}s",
        f"- listing url: {LISTING_URL}",
        f"- raw file: raw/zambialii/discovery/subsidiary-page-{PAGE_NUM:02d}.html",
        f"- raw sha256: {sha}",
        f"- raw bytes: {len(body)}",
        "",
        "## Findings",
        "",
        f"- raw <a> tags matching `/akn/zm/act/si/YYYY/N`: {len(listings)}",
        f"- unique (year, num) candidates on page: {len(unique)}",
        f"- existing si records in HEAD (records/sis): {len(existing)}",
        f"- novel (year, num) slots vs HEAD: {len(novel)}",
        f"- novel + corporate-keyword match: {len(corporate)}",
        f"- novel + other (non-corporate) keyword: {len(other)}",
        "",
        "## Corporate candidates (sorted by year desc, num asc)",
        "",
    ]
    for c in sorted(corporate, key=lambda x: (-x["year"], x["num"])):
        kws = ", ".join(c["matched_keywords"])
        lines.append(f"- SI {c['year']}/{c['num']}: {c['title']}  _(matched: {kws})_")
    if not corporate:
        lines.append("_(none on this page)_")
    lines += [
        "",
        "## Non-corporate novel candidates (preview, first 20)",
        "",
    ]
    for c in sorted(other, key=lambda x: (-x["year"], x["num"]))[:20]:
        lines.append(f"- SI {c['year']}/{c['num']}: {c['title']}")
    if len(other) > 20:
        lines.append(f"- _(... and {len(other) - 20} more not shown)_")

    lines += [
        "",
        "## Integrity",
        "",
        "- discovery-only batch; no records written this tick",
        "- no new amended_by / repealed_by / cited_authorities references introduced",
        "- raw file written; sha256 computed and recorded in provenance.log",
        "",
        "## Notes",
        "",
        f"- robots.txt: /legislation/subsidiary is Allow: / under zambialii.org robots; "
        f"Crawl-delay: 5s honoured (single fetch).",
        "- next tick: ingest 3-5 corporate candidates from this report (HTML AKN, PDF fallback if HTML <2 sections).",
        "",
    ]
    with open(report_path, "w") as f:
        f.write("\n".join(lines))
    print(f"wrote {report_path}", flush=True)

    return {
        "status": "ok",
        "fetches": 1,
        "raw_path": RAW_PATH,
        "raw_sha256": sha,
        "raw_bytes": len(body),
        "listings_a_tags": len(listings),
        "unique_candidates": len(unique),
        "existing_in_head": len(existing),
        "novel_slots": len(novel),
        "corporate_novel": len(corporate),
        "other_novel": len(other),
        "report": report_path,
        "elapsed_s": round(elapsed, 1),
    }


if __name__ == "__main__":
    summary = main()
    print(json.dumps(summary, indent=2))
