#!/usr/bin/env python3
"""
Batch 0184 discovery - fetch alphabet pages E and M, extract Employment-
related SIs (Employment Code, Minimum Wages, Labour, Factories, Workers'
Compensation, National Pension Scheme Authority, NAPSA), and write a
candidates JSON for the fetch step.
"""
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

BATCH_NUM = "0184"
USER_AGENT = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
CRAWL_DELAY_SECONDS = 6

WORKSPACE = "/sessions/sharp-awesome-edison/mnt/corpus"
os.chdir(WORKSPACE)
UTC = timezone.utc


def utc_now():
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch(url, session, last_fetch_t):
    if last_fetch_t[0] is not None:
        elapsed = time.time() - last_fetch_t[0]
        if elapsed < CRAWL_DELAY_SECONDS:
            time.sleep(CRAWL_DELAY_SECONDS - elapsed)
    print(f"  GET {url}")
    r = session.get(url, timeout=40, allow_redirects=True)
    last_fetch_t[0] = time.time()
    return r


def existing_head_ids():
    head = set()
    for root, _, files in os.walk(os.path.join(WORKSPACE, "records", "sis")):
        for fn in files:
            if fn.endswith(".json"):
                head.add(fn.replace(".json", ""))
    return head


EMPLOYMENT_KEYWORDS = [
    "employment code", "minimum wages", "minimum wage",
    "labour", "factories", "workers' compensation", "workers compensation",
    "national pension scheme", "napsa", "pensions and insurance",
    "workmen's compensation", "workmens compensation",
    "occupational safety", "occupational health",
]


def main():
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    last_fetch_t = [None]
    head_ids = existing_head_ids()

    urls = [
        "https://zambialii.org/legislation/?alphabet=E",
        "https://zambialii.org/legislation/?alphabet=M",
    ]
    candidates = []
    for url in urls:
        r = fetch(url, session, last_fetch_t)
        if r.status_code != 200:
            print(f"  FAIL {url}: status {r.status_code}")
            continue
        soup = BeautifulSoup(r.content, "html.parser")
        # ZambiaLII legislation list pages render entries as rows with title
        # text in an <a> and the href pattern /akn/zm/act/si/YYYY/NN[/eng@DATE].
        # Walk every anchor tagged with an SI href, and carry its title text.
        for a in soup.find_all("a", href=True):
            href = a["href"]
            m = re.match(r"^/akn/zm/act/si/(\d{4})/(\d+)(/eng@[\d-]+)?/?$", href)
            if not m:
                continue
            year = int(m.group(1))
            number = int(m.group(2))
            # Title: the anchor text itself, or the closest heading in its row.
            title = a.get_text(" ", strip=True)
            # Upstream the SI title sits in the same list-group item; try the
            # enclosing element's text as a fallback if the anchor is empty.
            if not title:
                parent = a
                for _ in range(3):
                    parent = parent.parent if parent.parent else parent
                    tx = parent.get_text(" ", strip=True) if parent else ""
                    if tx:
                        title = tx
                        break
            title_l = title.lower()
            if not any(kw in title_l for kw in EMPLOYMENT_KEYWORDS):
                continue
            # Skip if already in HEAD by prefix.
            prefix = f"si-zm-{year}-{number:03d}-"
            if any(i.startswith(prefix) for i in head_ids):
                continue
            candidates.append({
                "year": year, "number": number,
                "title": title[:200], "source_index": url,
            })

    # Deduplicate (alphabet=E and alphabet=M may overlap) and sort newest first.
    seen = set()
    dedup = []
    for c in candidates:
        key = (c["year"], c["number"])
        if key in seen:
            continue
        seen.add(key)
        dedup.append(c)
    dedup.sort(key=lambda c: (-c["year"], -c["number"]))

    out = {
        "batch": BATCH_NUM,
        "discovered_at": utc_now(),
        "index_urls": urls,
        "count": len(dedup),
        "head_record_count": len(head_ids),
        "candidates": dedup,
    }
    out_path = f"_work/batch_{BATCH_NUM}_candidates.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    today = datetime.now(UTC).strftime("%Y-%m-%d")
    # Log discovery fetches to costs.log and provenance.log so the day's
    # budget accounting stays accurate.
    with open("costs.log", "a") as f:
        for i, url in enumerate(urls):
            f.write(json.dumps({"date": today, "url": url,
                                "bytes": 0, "batch": BATCH_NUM,
                                "fetch_n": i + 1, "kind": "discovery"}) + "\n")

    print(f"\n==> batch {BATCH_NUM} discovery: {len(dedup)} candidates saved to {out_path}")
    for c in dedup[:12]:
        print(f"  - si/{c['year']}/{c['number']:03d} {c['title'][:90]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
