#!/usr/bin/env python3
"""Batch 0302 probe — minimal upstream-refresh for Phase 4 / acts_in_force.

Fetches:
  - https://zambialii.org/robots.txt
  - https://www.parliament.gov.zm/robots.txt
  - https://zambialii.org/legislation/recent
  - https://www.parliament.gov.zm/acts-of-parliament

Verifies robots.txt sha256 against expected; enumerates act (year, num)
pairs from chronological feeds; cross-references against on-disk
records/acts/**/act-zm-YYYY-NNN-*.json. Emits _work/batch_0302_probe.json
and appends fetch entries to costs.log + provenance.log.

Honours rate limits: 6s zambialii, 11s parliament. UA per approvals.yaml.
"""
import hashlib
import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import certifi
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
BATCH = "0302"
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

EXPECTED = {
    "https://zambialii.org/robots.txt":
        "fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0",
    "https://www.parliament.gov.zm/robots.txt":
        "278e83bcf567badfebcdea4d5d20ca9898e4449fe4eb2e3b5a08227b4ca9b762",
}

# RapidSSL chain workaround for parliament.gov.zm
RAPIDSSL_PEM = ROOT / "scripts" / "certs" / "rapidssl_tls_rsa_ca_g1.pem"
MERGED_BUNDLE = ROOT / "_work" / f"trust_bundle_{BATCH}.pem"
with open(certifi.where(), "rb") as a, open(RAPIDSSL_PEM, "rb") as b:
    MERGED_BUNDLE.write_bytes(a.read() + b"\n" + b.read())

COSTS_LOG = ROOT / "costs.log"
PROV_LOG = ROOT / "provenance.log"


def log_cost(url, body):
    rec = {"date": TODAY, "url": url, "bytes": len(body), "batch": BATCH, "kind": "probe"}
    with COSTS_LOG.open("a") as f:
        f.write(json.dumps(rec) + "\n")


def log_prov(url, sha, body):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    rec = {
        "ts": ts, "batch": BATCH, "url": url,
        "sha256": sha, "bytes": len(body), "kind": "probe",
    }
    with PROV_LOG.open("a") as f:
        f.write(json.dumps(rec) + "\n")


def fetch(url, *, delay=6, verify=True):
    time.sleep(delay)
    r = requests.get(url, headers={"User-Agent": UA}, timeout=30, verify=verify)
    r.raise_for_status()
    body = r.content
    sha = hashlib.sha256(body).hexdigest()
    log_cost(url, body)
    log_prov(url, sha, body)
    return body, sha


def existing_act_pairs():
    pairs = set()
    pat = re.compile(r"act-zm-(\d{4})-(\d{1,4})-")
    for p in (ROOT / "records" / "acts").rglob("act-zm-*.json"):
        m = pat.match(p.name)
        if m:
            year = m.group(1)
            num = str(int(m.group(2)))  # strip leading zeros
            pairs.add((year, num))
    return pairs


def parse_zambialii_recent(html):
    """zambialii.org/legislation/recent → list of (year, num) for ZM Acts."""
    soup = BeautifulSoup(html, "html.parser")
    out = []
    seen = set()
    # Match URLs like /akn/zm/act/2025/29/ and /akn/zm/act/2025/29/eng@2025-...
    pat = re.compile(r"/akn/zm/act/(\d{4})/(\d+)(?:/|$)")
    for a in soup.find_all("a", href=True):
        m = pat.search(a["href"])
        if m:
            key = (m.group(1), m.group(2))
            if key not in seen:
                seen.add(key)
                out.append({"year": key[0], "num": key[1]})
    return out


def parse_parliament_acts(html):
    """parliament.gov.zm/acts-of-parliament → list of (year, num)."""
    soup = BeautifulSoup(html, "html.parser")
    out = []
    seen = set()
    text = soup.get_text("\n")
    # "Act No. N of YYYY" pattern in body text
    pat = re.compile(r"Act\s+No\.\s*(\d+)\s+of\s+(\d{4})", re.IGNORECASE)
    for m in pat.finditer(text):
        num, year = m.group(1), m.group(2)
        key = (year, num)
        if key not in seen:
            seen.add(key)
            out.append({"year": year, "num": num})
    return out


def main():
    result = {
        "batch": BATCH,
        "date": TODAY,
        "robots": {},
        "zambia_acts": [],
        "parliament_acts": [],
        "zambia_novel": [],
        "parliament_novel": [],
        "robots_match_all": True,
        "existing_act_pairs": 0,
    }

    # 1. robots.txt — zambialii
    body, sha = fetch("https://zambialii.org/robots.txt", delay=0)
    match = sha == EXPECTED["https://zambialii.org/robots.txt"]
    result["robots"]["https://zambialii.org/robots.txt"] = {
        "sha256": sha, "match": match, "len": len(body)
    }
    if not match:
        result["robots_match_all"] = False

    # 2. zambialii recent
    body, _ = fetch("https://zambialii.org/legislation/recent", delay=6)
    result["zambia_acts"] = parse_zambialii_recent(body.decode("utf-8", errors="replace"))

    # 3. robots.txt — parliament
    body, sha = fetch(
        "https://www.parliament.gov.zm/robots.txt",
        delay=11,
        verify=str(MERGED_BUNDLE),
    )
    match = sha == EXPECTED["https://www.parliament.gov.zm/robots.txt"]
    result["robots"]["https://www.parliament.gov.zm/robots.txt"] = {
        "sha256": sha, "match": match, "len": len(body)
    }
    if not match:
        result["robots_match_all"] = False

    # 4. parliament acts page 0
    body, _ = fetch(
        "https://www.parliament.gov.zm/acts-of-parliament",
        delay=11,
        verify=str(MERGED_BUNDLE),
    )
    result["parliament_acts"] = parse_parliament_acts(body.decode("utf-8", errors="replace"))

    # 5. cross-reference
    existing = existing_act_pairs()
    result["existing_act_pairs"] = len(existing)

    for entry in result["zambia_acts"]:
        if (entry["year"], entry["num"]) not in existing:
            result["zambia_novel"].append(entry)
    for entry in result["parliament_acts"]:
        if (entry["year"], entry["num"]) not in existing:
            result["parliament_novel"].append(entry)

    out = ROOT / "_work" / f"batch_{BATCH}_probe.json"
    out.write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
