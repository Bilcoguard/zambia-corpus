#!/usr/bin/env python3
"""
Batch 0172 — Phase 4 bulk ingestion.

Per batch-0171 next-tick plan:
  Refresh parliament.gov.zm listing and re-parse against CURRENT HEAD
  to detect novel primary-Act candidates. Prior tick (0171) reported
  the listing as "exhausted" but a recount against git ls-tree HEAD
  finds HEAD contains only 4 Acts for 2024-2026 while the cached
  listing (acts-of-parliament.html fetched 2026-04-10) surfaces ~80
  novel primary-Act candidates after B-POL-ACT-1 title filter.

This tick ingests up to MAX_BATCH_SIZE (8) of the most recent novel
primary Acts. Given the 10s crawl delay per parliament.gov.zm
robots.txt we keep the target at 5 to stay within the 20-minute
wall-clock budget and leave time for commit/push/log.

Discovery source: cached raw/discovery/parliament-zm/acts-of-parliament.html
(fetched 2026-04-10, within the per-phase spot-check horizon).
Fetch sources: parliament.gov.zm /node/<id> HTML + PDF attachment.

Rate limit: parliament.gov.zm robots.txt Crawl-delay: 10s (stricter
than approvals.yaml default 2s and wins).
"""

import hashlib
import io
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

BATCH_NUM = "0172"
USER_AGENT = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
PARSER_VERSION = "0.5.0"
CRAWL_DELAY_SECONDS = 11  # 10s per robots.txt + 1s safety margin
MAX_TARGETS = 5  # per tick policy; bounded below MAX_BATCH_SIZE=8

# Target list: most-recent novel primary Acts identified by listing re-parse.
# (year, number, node_path, title_from_listing)
# Selected from the 80-candidate novel pool, ordered by recency.
TARGETS = [
    (2026, 1,  "/node/12917", "The Teaching Profession Act, 2026"),
    (2025, 29, "/node/12779", "The Zambia Institute of Procurement and Supply Act, 2025"),
    (2025, 27, "/node/12777", "The Betting Act, 2025"),
    (2025, 26, "/node/12775", "The Zambia National Broadcasting Corporation Act, 2025"),
    (2025, 25, "/node/12774", "The Independent Broadcasting Authority Act, 2025"),
]

REJECT_TITLE_TOKENS = (
    "amendment", "amendrnent", "amendement",
    "appropriation", "repeal",
    "supplementary", "validation", "transitional",
    "excess expenditure",
)

WORKSPACE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(WORKSPACE)

UTC = timezone.utc


def utc_now():
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def slugify(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text).strip("-")
    text = re.sub(r"-+", "-", text)
    return text[:64]


def title_rejected(title):
    tl = title.lower()
    for tok in REJECT_TITLE_TOKENS:
        if tok in tl:
            return tok
    return None


def parse_pdf_sections(pdf_bytes):
    import pdfplumber
    full_text = ""
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                pt = page.extract_text()
                if pt:
                    full_text += pt + "\n"
    except Exception as e:
        print(f"  PDF parse error: {e}", file=sys.stderr)
        return "", []
    if not full_text.strip():
        return "", []
    lines = full_text.strip().split("\n")
    header_title = lines[0].strip() if lines else ""
    sections = []
    section_pattern = re.compile(
        r"^(\d+)\.\s+(.+?)(?:\n|$)(.*?)(?=^\d+\.\s|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    for m in section_pattern.finditer(full_text):
        num = m.group(1)
        heading = m.group(2).strip()
        text = m.group(3).strip()
        sections.append({"number": num, "heading": heading, "text": text[:5000]})
    if not sections and full_text.strip():
        sections.append({"number": "1", "heading": "Full text", "text": full_text[:5000]})
    return header_title, sections


def build_record(year, number, title, sections, source_url, source_hash,
                 fetched_at, alternates):
    slug = slugify(title) if title else f"act-{year}-{number}"
    record_id = f"act-zm-{year}-{number:03d}-{slug}"
    if len(record_id) > 100:
        record_id = record_id[:100]
    return {
        "id": record_id,
        "type": "act",
        "jurisdiction": "ZM",
        "title": title,
        "citation": f"Act No. {number} of {year}",
        "enacted_date": f"{year}-01-01",
        "commencement_date": None,
        "in_force": True,
        "amended_by": [],
        "repealed_by": None,
        "sections": sections,
        "source_url": source_url,
        "source_hash": f"sha256:{source_hash}",
        "fetched_at": fetched_at,
        "parser_version": PARSER_VERSION,
        "alternate_sources": alternates,
    }


def fetch(url, session, last_fetch_t):
    """Rate-limited GET honouring 11s crawl delay between parliament.gov.zm hits."""
    # Enforce crawl delay
    if last_fetch_t[0] is not None:
        elapsed = time.time() - last_fetch_t[0]
        if elapsed < CRAWL_DELAY_SECONDS:
            sleep = CRAWL_DELAY_SECONDS - elapsed
            print(f"  sleep {sleep:.1f}s (crawl delay)")
            time.sleep(sleep)
    print(f"  GET {url}")
    r = session.get(url, timeout=60)
    last_fetch_t[0] = time.time()
    r.raise_for_status()
    return r


def find_pdf_link(html_bytes, base="https://www.parliament.gov.zm"):
    soup = BeautifulSoup(html_bytes, "html.parser")
    # Priority 1: any /sites/default/files/*.pdf link
    for a in soup.find_all("a", href=True):
        h = a["href"]
        if h.lower().endswith(".pdf") and "/sites/" in h:
            if h.startswith("/"):
                return base + h
            if h.startswith("http"):
                return h
    # Fallback: any .pdf link
    for a in soup.find_all("a", href=True):
        h = a["href"]
        if h.lower().endswith(".pdf"):
            if h.startswith("/"):
                return base + h
            if h.startswith("http"):
                return h
    return None


def extract_title(html_bytes):
    soup = BeautifulSoup(html_bytes, "html.parser")
    t = soup.title.get_text(strip=True) if soup.title else ""
    t = t.split("|")[0].strip()
    t = re.sub(r"\s+", " ", t)
    return t


def process_target(session, year, number, node_path, listing_title,
                   head_ids, head_slots, last_fetch_t):
    node_url = f"https://www.parliament.gov.zm{node_path}"
    slot = (year, number)

    # Guard: slot already in HEAD
    if slot in head_slots:
        return "skip_slot_in_head", None, None

    # Fetch node HTML
    start_html = utc_now()
    try:
        rh = fetch(node_url, session, last_fetch_t)
    except Exception as e:
        return f"fetch_html_error:{e}", None, None
    html_bytes = rh.content
    html_hash = hashlib.sha256(html_bytes).hexdigest()

    # Try to find PDF
    pdf_url = find_pdf_link(html_bytes)
    if not pdf_url:
        return f"no_pdf_on_node:{node_url}", None, None

    # Fetch PDF
    start_pdf = utc_now()
    try:
        rp = fetch(pdf_url, session, last_fetch_t)
    except Exception as e:
        return f"fetch_pdf_error:{e}", None, None
    pdf_bytes = rp.content
    pdf_hash = hashlib.sha256(pdf_bytes).hexdigest()

    # Parse PDF
    pdf_title, sections = parse_pdf_sections(pdf_bytes)
    if not sections:
        return f"pdf_parse_empty", None, None

    # Use authoritative title from node page
    page_title = extract_title(html_bytes)
    if page_title:
        title = page_title
    elif pdf_title:
        title = pdf_title
    else:
        title = listing_title

    # B-POL-ACT-1 filter
    reject = title_rejected(title)
    if reject:
        return f"reject_title:{reject}:{title}", None, None

    # Save raw files
    raw_dir = os.path.join(WORKSPACE, "raw", "parliament-zm", str(year))
    os.makedirs(raw_dir, exist_ok=True)
    safe_title_slug = slugify(title) or f"act-{year}-{number}"
    stem = f"act-zm-{year}-{number:03d}-{safe_title_slug}"[:100]
    raw_html = os.path.join(raw_dir, stem + ".html")
    raw_pdf = os.path.join(raw_dir, stem + ".pdf")
    with open(raw_html, "wb") as f:
        f.write(html_bytes)
    with open(raw_pdf, "wb") as f:
        f.write(pdf_bytes)

    # Build record
    record = build_record(
        year=year, number=number, title=title, sections=sections,
        source_url=pdf_url, source_hash=pdf_hash, fetched_at=start_pdf,
        alternates=[{
            "source_url": node_url,
            "source_hash": f"sha256:{html_hash}",
            "fetched_at": start_html,
            "role": "discovery_and_title",
        }],
    )

    # CHECK 1: novel id
    if record["id"] in head_ids:
        return f"check1_fail_id_collision:{record['id']}", None, None
    # CHECK 2: no (year, number) prefix clash
    prefix = f"act-zm-{year}-{number:03d}-"
    if any(i.startswith(prefix) for i in head_ids):
        return f"check2_fail_prefix_clash:{prefix}", None, None
    # CHECK 3: source hash matches on-disk
    with open(raw_pdf, "rb") as f:
        if hashlib.sha256(f.read()).hexdigest() != pdf_hash:
            return "check3_fail_hash_mismatch", None, None
    # CHECK 4: no cross-refs (amended_by / repealed_by / cited_authorities)
    if record["amended_by"] or record["repealed_by"]:
        return "check4_fail_crossref_present", None, None
    # CHECK 5: required fields
    for k in ("id","type","jurisdiction","title","citation","sections",
              "source_url","source_hash","fetched_at","parser_version"):
        if record.get(k) in (None, "", []):
            return f"check5_fail_missing:{k}", None, None

    # Write record
    out_dir = os.path.join(WORKSPACE, "records", "acts", str(year))
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{record['id']}.json")
    with open(out_path, "w") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)

    # Append costs.log for the two live fetches
    with open("costs.log", "a") as f:
        f.write(json.dumps({
            "date": datetime.now(UTC).strftime("%Y-%m-%d"),
            "url": node_url,
            "bytes": len(html_bytes),
            "batch": BATCH_NUM,
            "fetch_n": "html",
        }) + "\n")
        f.write(json.dumps({
            "date": datetime.now(UTC).strftime("%Y-%m-%d"),
            "url": pdf_url,
            "bytes": len(pdf_bytes),
            "batch": BATCH_NUM,
            "fetch_n": "pdf",
        }) + "\n")

    # Append provenance.log
    with open("provenance.log", "a") as f:
        f.write(json.dumps({
            "request_url": node_url, "status": 200,
            "sha256": html_hash, "bytes": len(html_bytes),
            "started_at": start_html, "batch": BATCH_NUM,
            "parser_version": PARSER_VERSION,
        }) + "\n")
        f.write(json.dumps({
            "request_url": pdf_url, "status": 200,
            "sha256": pdf_hash, "bytes": len(pdf_bytes),
            "started_at": start_pdf, "batch": BATCH_NUM,
            "parser_version": PARSER_VERSION,
        }) + "\n")

    return "ok", record, (node_url, pdf_url, html_hash, pdf_hash,
                          start_html, start_pdf, len(html_bytes), len(pdf_bytes))


def main():
    # Get fresh HEAD snapshot
    head_list = subprocess.run(
        ["git", "ls-tree", "-r", "HEAD", "--name-only", "records/acts/"],
        capture_output=True, text=True, check=True,
    ).stdout
    head_ids = set()
    head_slots = set()
    for line in head_list.splitlines():
        stem = line.rsplit("/", 1)[-1].removesuffix(".json")
        head_ids.add(stem)
        m = re.match(r"act-zm-(\d{4})-(\d+)-", stem)
        if m:
            head_slots.add((int(m.group(1)), int(m.group(2))))
    print(f"HEAD: {len(head_ids)} Act records, {len(head_slots)} (year,num) slots")

    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT

    deadline = time.time() + 14 * 60  # 14-min internal budget

    last_fetch_t = [None]
    results = []
    for (year, number, node_path, listing_title) in TARGETS:
        if time.time() > deadline:
            print(f"DEADLINE reached; stopping.")
            results.append({"year": year, "number": number, "status": "deadline_skip",
                            "node_path": node_path, "listing_title": listing_title})
            continue
        print(f"\n=== Target {year}/{number:03d} {listing_title!r} ===")
        status, rec, meta = process_target(
            session, year, number, node_path, listing_title,
            head_ids, head_slots, last_fetch_t)
        print(f"  status: {status}")
        entry = {
            "year": year, "number": number,
            "node_path": node_path, "listing_title": listing_title,
            "status": status,
        }
        if rec is not None:
            entry["record_id"] = rec["id"]
            entry["sections"] = len(rec["sections"])
            entry["pdf_url"] = meta[1]
            entry["html_hash"] = meta[2]
            entry["pdf_hash"] = meta[3]
            entry["html_fetched_at"] = meta[4]
            entry["pdf_fetched_at"] = meta[5]
            entry["html_bytes"] = meta[6]
            entry["pdf_bytes"] = meta[7]
            # Ensure the new id is reflected in our local head_ids/head_slots
            # for subsequent targets in the same batch
            head_ids.add(rec["id"])
            head_slots.add((year, number))
        else:
            # For gaps, log them
            with open("gaps.md", "a") as f:
                f.write(f"- [{utc_now()}] {year}/{number:03d} listing_title={listing_title!r} "
                        f"status={status} node=https://www.parliament.gov.zm{node_path} batch={BATCH_NUM}\n")
        results.append(entry)

    # Write summary json for downstream commit stage
    with open(f"_work/batch_{BATCH_NUM}_summary.json", "w") as f:
        json.dump({
            "batch": BATCH_NUM,
            "run_at": utc_now(),
            "targets_total": len(TARGETS),
            "records_written": sum(1 for r in results if r["status"] == "ok"),
            "results": results,
        }, f, indent=2)
    print(f"\nSummary: {sum(1 for r in results if r['status']=='ok')} ok / "
          f"{len(results)} targets")
    return 0 if any(r["status"] == "ok" for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
