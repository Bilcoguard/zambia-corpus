#!/usr/bin/env python3
"""
Phase 4 Batch 0009 — acts_in_force (parliament.gov.zm)
Target: 2017 Acts No. 12-19.
Nodes: 7334, 7333, 7336, 7331, 7329, 7335, 7324, 7330
"""

import hashlib
import json
import os
import re
import sys
import time
import datetime
import urllib.parse
from pathlib import Path

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup
import pdfplumber

# ── Config ──────────────────────────────────────────────────────────────────
WORKSPACE = Path("/sessions/charming-eager-cannon/mnt/corpus")
RAW_DIR = WORKSPACE / "raw"
RECORDS_DIR = WORKSPACE / "records" / "acts"
REPORTS_DIR = WORKSPACE / "reports"
COSTS_LOG = WORKSPACE / "costs.log"
PROVENANCE_LOG = WORKSPACE / "provenance.log"
GAPS_MD = WORKSPACE / "gaps.md"
WORKER_LOG = WORKSPACE / "worker.log"

BASE_URL = "https://www.parliament.gov.zm"
USER_AGENT = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
PARLIAMENT_RATE = 2
PARSER_VERSION = "0.2.0"

MAX_BATCH_SIZE = 8
BATCH_NUMBER = "0009"
TODAY = datetime.date.today().isoformat()

HEADERS = {"User-Agent": USER_AGENT}
SESSION = requests.Session()
SESSION.headers.update(HEADERS)

BULK_DIR = RAW_DIR / "bulk" / "parliament-zm"

# Targets: 2017 Acts No. 12-19
TARGETS = [
    {"act_num": 12, "year": 2017, "node_id": "7334", "listing_title": "The Value Added Tax (Amendment) (Act No. 12 of 2017)"},
    {"act_num": 13, "year": 2017, "node_id": "7333", "listing_title": "The Skills Development Levy (Amendment) (Act No. 13 of 2017)"},
    {"act_num": 14, "year": 2017, "node_id": "7336", "listing_title": "The Customs and Excise (Amendment) (Act No. 14 of 2017)"},
    {"act_num": 15, "year": 2017, "node_id": "7331", "listing_title": "Insurance Premium Levy (Amendment) (Act No. 15 of 2017)"},
    {"act_num": 16, "year": 2017, "node_id": "7329", "listing_title": "Income Tax (Amendment) (Act No. 16 of 2017)"},
    {"act_num": 17, "year": 2017, "node_id": "7335", "listing_title": "Zambia National Broadcasting Corporation (Amendment) (Act No. 17 of 2017)"},
    {"act_num": 18, "year": 2017, "node_id": "7324", "listing_title": "Independent Broadcasting Authority (Amendment) (Act No. 18 of 2017)"},
    {"act_num": 19, "year": 2017, "node_id": "7330", "listing_title": "Industrial and Labour Relations (Amendment) (Act No. 19 of 2017)"},
]

FETCH_BUDGET = 2000

# ── Helpers ─────────────────────────────────────────────────────────────────

def get_today_fetch_count() -> int:
    count = 0
    if COSTS_LOG.exists():
        with COSTS_LOG.open() as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                    if r.get("date") == TODAY:
                        count = max(count, r.get("fetch_n", 0))
                except Exception:
                    pass
    return count

fetch_counter = [get_today_fetch_count()]
batch_fetches = [0]
FETCH_BUDGET_REMAINING = FETCH_BUDGET - fetch_counter[0]
print(f"Starting fetch counter: {fetch_counter[0]} (budget remaining: {FETCH_BUDGET_REMAINING})")


def log_fetch(url: str, byte_count: int):
    fetch_counter[0] += 1
    batch_fetches[0] += 1
    with COSTS_LOG.open("a") as f:
        f.write(json.dumps({
            "date": TODAY,
            "url": url,
            "bytes": byte_count,
            "fetch_n": fetch_counter[0]
        }) + "\n")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def budget_check() -> bool:
    return fetch_counter[0] < FETCH_BUDGET


def fetch_url(url: str, timeout: int = 30) -> bytes | None:
    if not budget_check():
        print(f"  [BUDGET] fetch budget exhausted at {fetch_counter[0]}")
        return None
    try:
        resp = SESSION.get(url, timeout=timeout, verify=False)
        resp.raise_for_status()
        log_fetch(url, len(resp.content))
        time.sleep(PARLIAMENT_RATE)
        return resp.content
    except Exception as e:
        print(f"  [WARN] fetch error for {url}: {e}")
        return None


def extract_pdf_url_from_node(node_html: bytes, node_url: str):
    soup = BeautifulSoup(node_html, "html.parser")
    h1 = soup.find("h1")
    full_title = h1.get_text(strip=True) if h1 else None
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if ".pdf" in href.lower():
            pdf_url = href if href.startswith("http") else BASE_URL + href
            return pdf_url, full_title
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "documents/acts" in href or "files/documents" in href:
            pdf_url = href if href.startswith("http") else BASE_URL + href
            return pdf_url, full_title
    return None, full_title


def slugify(text: str, max_len: int = 60) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    text = text.strip("-")
    return text[:max_len].rstrip("-")


def make_act_id(act_num: int, year: int, title: str) -> str:
    title_slug = slugify(re.sub(r"^the\s+", "", title, flags=re.I), 50)
    return f"act-zm-{year}-{act_num:03d}-{title_slug}"


def parse_pdf_sections(pdf_path: Path) -> list:
    sections = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                full_text += page_text + "\n"

        lines = full_text.split("\n")
        current_sec_num = None
        current_sec_heading = None
        current_text_lines = []

        section_pattern = re.compile(r"^(\d{1,3})\.\s+([A-Z][^\n]{0,120})$")
        alt_pattern = re.compile(r"^Section\s+(\d{1,3})[.:]?\s*(.*)")

        for line in lines:
            line_s = line.strip()
            if not line_s:
                if current_text_lines:
                    current_text_lines.append("")
                continue

            m = section_pattern.match(line_s) or alt_pattern.match(line_s)
            if m:
                if current_sec_num is not None:
                    sections.append({
                        "number": current_sec_num,
                        "heading": current_sec_heading,
                        "text": " ".join(t for t in current_text_lines if t).strip()
                    })
                current_sec_num = m.group(1)
                current_sec_heading = m.group(2).strip() if m.group(2) else ""
                current_text_lines = []
            else:
                if current_sec_num is not None:
                    current_text_lines.append(line_s)

        if current_sec_num is not None:
            sections.append({
                "number": current_sec_num,
                "heading": current_sec_heading,
                "text": " ".join(t for t in current_text_lines if t).strip()
            })

        if not sections:
            sections = [{"number": "1", "heading": "Full text", "text": full_text[:50000]}]

    except Exception as e:
        print(f"  [WARN] PDF parse error: {e}")
        sections = [{"number": "1", "heading": "Parse error", "text": str(e)}]

    return sections


def extract_assent_date_from_pdf(pdf_path: Path) -> str | None:
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages[:3]:
                text = page.extract_text() or ""
                m = re.search(
                    r"Date of Assent[:\s]+(\d{1,2})(?:st|nd|rd|th)?\s+(\w+)[,\s]+(\d{4})",
                    text, re.I
                )
                if m:
                    day, month_str, year = int(m.group(1)), m.group(2), int(m.group(3))
                    months = {
                        "january": 1, "february": 2, "march": 3, "april": 4,
                        "may": 5, "june": 6, "july": 7, "august": 8,
                        "september": 9, "october": 10, "november": 11, "december": 12
                    }
                    month_num = months.get(month_str.lower())
                    if month_num:
                        return f"{year:04d}-{month_num:02d}-{day:02d}"
                m2 = re.search(r"assented to.*?(\d{1,2}).*?(\w+)[,\s]+(\d{4})", text, re.I)
                if m2:
                    day, month_str, year = int(m2.group(1)), m2.group(2), int(m2.group(3))
                    months = {
                        "january": 1, "february": 2, "march": 3, "april": 4,
                        "may": 5, "june": 6, "july": 7, "august": 8,
                        "september": 9, "october": 10, "november": 11, "december": 12
                    }
                    month_num = months.get(month_str.lower())
                    if month_num:
                        return f"{year:04d}-{month_num:02d}-{day:02d}"
    except Exception:
        pass
    return None


def get_existing_record_ids() -> set:
    ids = set()
    for d in [RECORDS_DIR, WORKSPACE / "records" / "judgments"]:
        if d.exists():
            for f in d.glob("*.json"):
                ids.add(f.stem)
    return ids


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print(f"=== Phase 4 Batch {BATCH_NUMBER} ===")
    print(f"Started: {datetime.datetime.utcnow().isoformat()}Z")

    existing_ids = get_existing_record_ids()
    print(f"Existing records: {len(existing_ids)}")

    records_created = []
    gaps = []

    for i, target in enumerate(TARGETS[:MAX_BATCH_SIZE]):
        node_id = target["node_id"]
        act_num = target["act_num"]
        year = target["year"]
        listing_title = target["listing_title"]
        node_url = f"{BASE_URL}/node/{node_id}"

        print(f"\n[{i+1}/{len(TARGETS)}] Act No. {act_num} of {year} (node {node_id})")

        node_dir = BULK_DIR / f"node-{node_id}"
        node_dir.mkdir(parents=True, exist_ok=True)
        node_html_path = node_dir / "node.html"

        fetched_at = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        # Fetch node page
        if node_html_path.exists():
            print(f"  Node HTML cached.")
            node_data = node_html_path.read_bytes()
        else:
            print(f"  Fetching node page...")
            node_data = fetch_url(node_url)
            if not node_data:
                gaps.append({"node_id": node_id, "title": listing_title, "reason": "node_fetch_failed", "url": node_url})
                continue
            node_html_path.write_bytes(node_data)

        # Extract PDF URL
        pdf_url, full_title = extract_pdf_url_from_node(node_data, node_url)
        if not pdf_url:
            print(f"  [WARN] No PDF URL found on node page")
            gaps.append({"node_id": node_id, "title": listing_title, "reason": "no_pdf_url", "url": node_url})
            continue

        print(f"  PDF URL: {pdf_url[:80]}")

        # Fetch PDF
        pdf_filename = urllib.parse.unquote(pdf_url.split("/")[-1].split("?")[0])
        if not pdf_filename.lower().endswith(".pdf"):
            pdf_filename += ".pdf"
        pdf_path = node_dir / pdf_filename

        existing_pdfs = list(node_dir.glob("*.pdf"))
        if existing_pdfs:
            pdf_path = existing_pdfs[0]
            print(f"  PDF cached: {pdf_path.name} ({pdf_path.stat().st_size:,} bytes)")
        elif not pdf_path.exists():
            print(f"  Fetching PDF...")
            pdf_data = fetch_url(pdf_url, timeout=60)
            if not pdf_data:
                gaps.append({"node_id": node_id, "title": listing_title, "reason": "pdf_fetch_failed", "url": pdf_url})
                continue
            pdf_path.write_bytes(pdf_data)
            print(f"  PDF saved: {len(pdf_data):,} bytes")

        # Build record
        use_title = full_title or listing_title
        use_title = re.sub(r"\s+", " ", use_title).strip()
        citation = f"Act No. {act_num} of {year}"
        act_id = make_act_id(act_num, year, use_title)

        if act_id in existing_ids:
            print(f"  [SKIP] ID {act_id} already in corpus")
            continue

        source_hash = sha256_file(pdf_path)
        sections = parse_pdf_sections(pdf_path)
        assent_date = extract_assent_date_from_pdf(pdf_path)

        record = {
            "id": act_id,
            "type": "act",
            "jurisdiction": "ZM",
            "title": use_title,
            "citation": citation,
            "date_of_assent": assent_date,
            "commencement_date": None,
            "in_force": True,
            "amended_by": [],
            "repealed_by": None,
            "sections": sections,
            "source_url": pdf_url,
            "source_hash": source_hash,
            "node_url": node_url,
            "fetched_at": fetched_at,
            "parser_version": PARSER_VERSION,
        }

        rec_path = RECORDS_DIR / f"{act_id}.json"
        with rec_path.open("w") as f:
            json.dump(record, f, indent=2, ensure_ascii=False)

        records_created.append(record)
        existing_ids.add(act_id)
        print(f"  Record: {act_id} | {len(sections)} sections | assent: {assent_date}")

        # Provenance log
        with PROVENANCE_LOG.open("a") as f:
            f.write(json.dumps({
                "id": act_id,
                "source_url": pdf_url,
                "source_hash": source_hash,
                "fetched_at": fetched_at,
                "parser_version": PARSER_VERSION,
                "batch": BATCH_NUMBER
            }) + "\n")

    # ── Summary ──────────────────────────────────────────────────────────────
    print(f"\n=== Batch {BATCH_NUMBER} Summary ===")
    print(f"Records created: {len(records_created)}")
    print(f"Gaps: {len(gaps)}")
    print(f"Fetches this batch: {batch_fetches[0]}")
    print(f"Total fetches today: {fetch_counter[0]}/{FETCH_BUDGET}")

    return records_created, gaps


if __name__ == "__main__":
    records, gaps = main()
    # Output structured summary
    print("\n" + json.dumps({
        "batch": BATCH_NUMBER,
        "records_created": len(records),
        "record_ids": [r["id"] for r in records],
        "section_counts": {r["id"]: len(r["sections"]) for r in records},
        "gaps": gaps,
        "fetches": batch_fetches[0],
        "total_fetches_today": fetch_counter[0],
    }, indent=2))
