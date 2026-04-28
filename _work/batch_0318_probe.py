"""Batch 0318 — Phase 4 / minimal upstream-refresh tick (29th consecutive steady-state tick).

Probe-only. Zero record writes by design.
"""
import hashlib, json, os, re, ssl, sys, time
from datetime import datetime, timezone
from pathlib import Path

import certifi
import requests
from bs4 import BeautifulSoup

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA, "Accept": "text/html,application/xhtml+xml"}

# Establish trust bundle: certifi + RapidSSL intermediate workaround
CERT_OUT = "_work/trust_bundle_0318.pem"
def build_trust_bundle():
    base = Path(certifi.where()).read_bytes()
    extra = Path("scripts/certs/rapidssl_tls_rsa_ca_g1.pem").read_bytes()
    Path(CERT_OUT).write_bytes(base + b"\n" + extra)
    return CERT_OUT

VERIFY = build_trust_bundle()

EXPECTED = {
    "https://zambialii.org/robots.txt":  ("fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0", 5),
    "https://www.parliament.gov.zm/robots.txt": ("278e83bcf567badfebcdea4d5d20ca9898e4449fe4eb2e3b5a08227b4ca9b762", 10),
}

PROBES = [
    ("zambialii", "https://zambialii.org/legislation/recent", 6),
    ("parliament", "https://www.parliament.gov.zm/acts-of-parliament", 11),
]

def utc_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def fetch(url):
    r = requests.get(url, headers=HEADERS, timeout=60, verify=VERIFY)
    r.raise_for_status()
    return r.content

results = {"started_at": utc_iso(), "user_agent": UA, "checks": []}

# 1) robots.txt re-verification
for url, (expected_sha, crawl_delay) in EXPECTED.items():
    body = fetch(url)
    sha = hashlib.sha256(body).hexdigest()
    match = sha == expected_sha
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    domain = "zambialii" if "zambialii" in url else "parliament"
    out_dir = Path(f"raw/{domain}/_robots")
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"robots-{ts}.txt"
    out.write_bytes(body)
    results["checks"].append({
        "kind": "robots",
        "url": url,
        "sha256": sha,
        "expected_sha256": expected_sha,
        "match": match,
        "bytes": len(body),
        "saved": str(out),
    })
    print(f"robots {domain}: sha={sha[:16]}... match={match} bytes={len(body)}")
    time.sleep(crawl_delay)

# 2) Refresh probes
zam_links = []
parl_acts = []
parl_bytes = 0
zam_bytes = 0
zam_sha = None
parl_sha = None

for name, url, delay in PROBES:
    body = fetch(url)
    text = body.decode("utf-8", "replace")
    if name == "zambialii":
        zam_bytes = len(body)
        zam_sha = hashlib.sha256(body).hexdigest()
        soup = BeautifulSoup(text, "html.parser")
        for a in soup.find_all("a", href=True):
            m = re.search(r"/akn/zm/act/(\d{4})/(\d+)", a["href"])
            if m:
                yr, num = m.group(1), m.group(2)
                pair = f"{yr}/{num}"
                if pair not in zam_links:
                    zam_links.append(pair)
        Path("_work/zambia_recent_b0318.html").write_bytes(body)
    else:
        parl_bytes = len(body)
        parl_sha = hashlib.sha256(body).hexdigest()
        soup = BeautifulSoup(text, "html.parser")
        page_text = soup.get_text(" ", strip=True)
        for m in re.finditer(r"Act\s+No\.?\s*(\d+)\s+of\s+(\d{4})", page_text):
            num, yr = m.group(1), m.group(2)
            pair = f"{yr}/{num}"
            if pair not in parl_acts:
                parl_acts.append(pair)
        Path("_work/parliament_acts_b0318.html").write_bytes(body)
    time.sleep(delay)

# 3) Cross-check vs records/acts/
records_root = Path("records/acts")
on_disk = set()
if records_root.exists():
    for p in records_root.rglob("act-zm-*.json"):
        m = re.match(r"act-zm-(\d{4})-0*(\d+)-", p.name)
        if m:
            on_disk.add(f"{m.group(1)}/{m.group(2)}")

zam_novel = [p for p in zam_links if p not in on_disk]
parl_novel = [p for p in parl_acts if p not in on_disk]

results["zambialii_recent"] = {
    "url": "https://zambialii.org/legislation/recent",
    "bytes": zam_bytes,
    "sha256": zam_sha,
    "act_pairs": zam_links,
    "novel_count": len(zam_novel),
    "novel_pairs": zam_novel,
}
results["parliament_page0"] = {
    "url": "https://www.parliament.gov.zm/acts-of-parliament",
    "bytes": parl_bytes,
    "sha256": parl_sha,
    "act_pairs": parl_acts,
    "novel_count": len(parl_novel),
    "novel_pairs": parl_novel,
}
results["records_on_disk_count"] = len(on_disk)
results["finished_at"] = utc_iso()

Path("_work/batch_0318_probe.json").write_text(json.dumps(results, indent=2))
print(json.dumps({
    "zam_pairs": len(zam_links), "zam_novel": len(zam_novel),
    "parl_pairs": len(parl_acts), "parl_novel": len(parl_novel),
    "records_on_disk": len(on_disk),
}, indent=2))
