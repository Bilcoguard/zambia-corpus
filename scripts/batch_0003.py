#!/usr/bin/env python3
"""
Phase 4 Batch 0003 — acts_in_force (parliament.gov.zm), continuing from batch 0002.
Processes up to MAX_BATCH_SIZE=8 acts from cached listing pages.
Target: 2019 Acts No. 1-8 (nodes 7942, 7947, 7948, 7946, 7945, 7944, 8206, 8204).
"""

import hashlib
import json
import os
import re
import sys
import time
import datetime
import urllib.robotparser
import urllib.parse
from pathlib import Path

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup
import pdfplumber

# ── Config ──────────────────────────────────────────────────────────────────
WORKSPACE = Path("/sessions/compassionate-adoring-albattani/mnt/corpus")
RAW_DIR = WORKSPACE / "raw"
RECORDS_DIR = WORKSPACE / "records" / "acts"
REPORTS_DIR = WORKSPACE / "reports"
COSTS_LOG = WORKSPACE / "costs.log"
PROVENANCE_LOG = WORKSPACE / "provenance.log"
GAPS_MD = WORKSPACE / "gaps.md"
WORKER_LOG = WORKSPACE / "worker.log"

BASE_URL = "https://www.parliament.gov.zm"
LISTING_PATH = "/acts-of-parliament"
USER_AGENT = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
RATE_LIMIT_SEC = 2   # default between requests
PARLIAMENT_RATE = 2  # parliament.gov.zm rate limit
PARSER_VERSION = "0.3.0"

MAX_BATCH_SIZE = 8
BATCH_NUMBER = "0003"
TODAY = datetime.date.today().isoformat()

HEADERS = {"User-Agent": USER_AGENT}

SESSION = requests.Session()
SESSION.headers.update(HEADERS)

DISCOVERY_DIR = RAW_DIR / "discovery" / "parliament-zm"
BULK_DIR = RAW_DIR / "bulk" / "parliament-zm"

# Today's running fetch count — start from what costs.log shows
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

FETCH_BUDGET = 2000
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


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def budget_check() -> bool:
    return fetch_counter[0] < FETCH_BUDGET


def fetch_with_retry(url: str, timeout: int = 30) -> bytes | None:
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


def get_existing_record_ids() -> set:
    ids = set()
    if RECORDS_DIR.exists():
        for f in RECORDS_DIR.glob("*.json"):
            ids.add(f.stem)
    jdir = WORKSPACE / "records" / "judgments"
    if jdir.exists():
        for f in jdir.glob("*.json"):
            ids.add(f.stem)
    return ids


def parse_listing_page(html_path: Path) -> list[dict]:
    """Parse a cached parliament.gov.zm listing page and extract act candidates."""
    with html_path.open("rb") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    candidates = []
    rows = soup.select("table.views-table tbody tr")
    if not rows:
        rows = soup.select(".view-content .views-row")

    for row in rows:
        cells = row.find_all("td")
        if len(cells) >= 1:
            title_cell = cells[0]
            link = title_cell.find("a")
            if link and link.get("href"):
                href = link["href"]
                text = link.get_text(strip=True)
                node_url = href if href.startswith("http") else BASE_URL + href
                node_match = re.search(r'/node/(\d+)', href)
                node_id = node_match.group(1) if node_match else None
                if node_id:
                    candidates.append({
                        "title": text,
                        "node_url": node_url,
                        "node_id": node_id,
                        "source_page": str(html_path)
                    })

    if not candidates:
        for row in soup.select(".view-content .views-row"):
            link = row.find("a")
            if link and link.get("href"):
                href = link["href"]
                text = link.get_text(strip=True)
                node_url = href if href.startswith("http") else BASE_URL + href
                node_match = re.search(r'/node/(\d+)', href)
                node_id = node_match.group(1) if node_match else None
                if node_id:
                    candidates.append({
                        "title": text,
                        "node_url": node_url,
                        "node_id": node_id,
                        "source_page": str(html_path)
                    })

    return candidates


def extract_pdf_url_from_node(node_html: bytes | None, node_url: str) -> tuple[str | None, str | None]:
    """Extract PDF link from a parliament.gov.zm node page. Returns (pdf_url, full_title)."""
    if not node_html:
        return None, None
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
        if "documents/acts" in href or "amendment_act" in href or "files/documents" in href:
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


def make_act_id(citation: str, year: int | None, title: str) -> str:
    """Build a stable act ID from citation components."""
    m = re.search(r"(?:act\s+)?no\.?\s*(\d+)\s+of\s+(\d{4})", citation, re.I)
    if m:
        act_num = int(m.group(1))
        act_year = int(m.group(2))
        title_slug = slugify(re.sub(r"^the\s+", "", title, flags=re.I), 50)
        return f"act-zm-{act_year}-{act_num:03d}-{title_slug}"
    title_slug = slugify(re.sub(r"^the\s+", "", title, flags=re.I), 60)
    if year:
        return f"act-zm-{year}-{title_slug}"
    return f"act-zm-{title_slug}"


def parse_citation_from_title(title: str) -> tuple[str | None, int | None]:
    """Extract citation like 'Act No. X of YYYY' from listing title."""
    m = re.search(r"Act\s+No\.?\s*(\d+)\s+of\s+(\d{4})", title, re.I)
    if m:
        return f"Act No. {m.group(1)} of {m.group(2)}", int(m.group(2))
    m = re.search(r"No\.?\s*(\d+)\s+of\s+(\d{4})", title, re.I)
    if m:
        return f"Act No. {m.group(1)} of {m.group(2)}", int(m.group(2))
    return None, None


def parse_pdf_sections(pdf_path: Path) -> list[dict]:
    """Parse a PDF into sections using pdfplumber."""
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
    """Try to extract the date of assent from the PDF."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages[:3]):
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


def build_record(
    act_id: str,
    title: str,
    citation: str,
    year: int | None,
    pdf_url: str,
    pdf_path: Path,
    node_url: str,
    fetched_at: str,
) -> dict:
    source_hash = sha256_file(pdf_path)
    sections = parse_pdf_sections(pdf_path)
    assent_date = extract_assent_date_from_pdf(pdf_path)

    return {
        "id": act_id,
        "type": "act",
        "jurisdiction": "ZM",
        "title": title,
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


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print(f"=== Phase 4 Batch {BATCH_NUMBER} ===")
    print(f"Started: {datetime.datetime.utcnow().isoformat()}Z")

    existing_ids = get_existing_record_ids()
    print(f"Existing records: {len(existing_ids)}")

    # Build full inventory from cached listing pages
    listing_files = sorted(DISCOVERY_DIR.glob("acts-of-parliament*.html"))
    print(f"Cached listing pages: {len(listing_files)}")

    all_candidates = []
    seen_node_ids = set()

    for page_file in listing_files:
        page_candidates = parse_listing_page(page_file)
        for c in page_candidates:
            if c["node_id"] not in seen_node_ids:
                seen_node_ids.add(c["node_id"])
                all_candidates.append(c)

    print(f"Total unique candidates from cached pages: {len(all_candidates)}")

    # Identify already-processed acts by citation key (act_number, year)
    processed_citation_keys = set()
    for rec_file in RECORDS_DIR.glob("*.json"):
        with rec_file.open() as f:
            try:
                rec = json.load(f)
                citation = rec.get("citation", "")
                m = re.search(r'No\.?\s*(\d+)\s+of\s+(\d{4})', citation, re.I)
                if m:
                    processed_citation_keys.add((int(m.group(1)), int(m.group(2))))
            except Exception:
                pass

    jdir = WORKSPACE / "records" / "judgments"
    if jdir.exists():
        for rec_file in jdir.glob("*.json"):
            with rec_file.open() as f:
                try:
                    rec = json.load(f)
                    citation = rec.get("citation", "")
                    m = re.search(r'No\.?\s*(\d+)\s+of\s+(\d{4})', citation, re.I)
                    if m:
                        processed_citation_keys.add((int(m.group(1)), int(m.group(2))))
                except Exception:
                    pass

    print(f"Already-processed citation keys: {len(processed_citation_keys)}")

    def get_citation_key(title: str) -> tuple | None:
        m = re.search(r'No\.?\s*(\d+)\s+of\s+(\d{4})', title, re.I)
        if m:
            return (int(m.group(1)), int(m.group(2)))
        return None

    to_process = [c for c in all_candidates
                  if get_citation_key(c["title"]) not in processed_citation_keys
                  or get_citation_key(c["title"]) is None]
    print(f"Remaining candidates from cached pages: {len(to_process)}")

    batch = to_process[:MAX_BATCH_SIZE]
    print(f"This batch: {len(batch)} candidates")

    records_created = []
    gaps = []

    for i, candidate in enumerate(batch):
        node_id = candidate["node_id"]
        listing_title = candidate["title"]
        node_url = candidate["node_url"]

        print(f"\n[{i+1}/{len(batch)}] Node {node_id}: {listing_title[:70]}")

        node_dir = BULK_DIR / f"node-{node_id}"
        node_dir.mkdir(parents=True, exist_ok=True)
        node_html_path = node_dir / "node.html"

        fetched_at = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        # Fetch node page if not cached
        if not node_html_path.exists():
            print(f"  Fetching node page...")
            node_data = fetch_with_retry(node_url)
            if not node_data:
                gaps.append({
                    "node_id": node_id,
                    "title": listing_title,
                    "reason": "node_fetch_failed",
                    "url": node_url
                })
                continue
            node_html_path.write_bytes(node_data)
        else:
            print(f"  Node HTML cached.")
            node_data = node_html_path.read_bytes()

        # Parse PDF URL from node page
        pdf_url, full_title = extract_pdf_url_from_node(node_data, node_url)

        if not pdf_url:
            print(f"  [WARN] No PDF URL found on node page")
            gaps.append({
                "node_id": node_id,
                "title": listing_title,
                "reason": "no_pdf_url",
                "url": node_url
            })
            continue

        print(f"  PDF URL: {pdf_url[:80]}")

        # Check for cached PDF
        pdf_path = None
        existing_pdfs = list(node_dir.glob("*.pdf"))
        if existing_pdfs:
            pdf_path = existing_pdfs[0]
            print(f"  PDF already cached: {pdf_path.name}")
        else:
            pdf_filename = urllib.parse.unquote(pdf_url.split("/")[-1].split("?")[0])
            if not pdf_filename.lower().endswith(".pdf"):
                pdf_filename += ".pdf"
            pdf_path = node_dir / pdf_filename

        # Fetch PDF if not cached
        if not pdf_path.exists():
            print(f"  Fetching PDF ({pdf_path.name[:60]})...")
            pdf_data = fetch_with_retry(pdf_url, timeout=60)
            if not pdf_data:
                gaps.append({
                    "node_id": node_id,
                    "title": listing_title,
                    "reason": "pdf_fetch_failed",
                    "url": pdf_url
                })
                continue
            pdf_path.write_bytes(pdf_data)
            print(f"  PDF saved: {len(pdf_data):,} bytes")
        else:
            print(f"  PDF size: {pdf_path.stat().st_size:,} bytes")

        # Parse citation
        citation, year = parse_citation_from_title(listing_title)
        use_title = full_title or listing_title
        use_title = re.sub(r"\s+", " ", use_title).strip()

        if not citation and full_title:
            citation, year = parse_citation_from_title(full_title)

        if not citation:
            print(f"  [WARN] Could not extract citation for node {node_id}")
            gaps.append({
                "node_id": node_id,
                "title": listing_title,
                "reason": "no_citation",
                "url": node_url
            })
            title_slug = slugify(re.sub(r"^the\s+", "", use_title, flags=re.I), 60)
            citation = f"Parliament of Zambia Act (node {node_id})"
            year = None

        # Build act ID
        act_id = make_act_id(citation, year, use_title)

        # Check for ID collision
        if act_id in existing_ids:
            print(f"  [SKIP] ID {act_id} already in corpus")
            continue

        print(f"  Building record: {act_id}")

        try:
            record = build_record(
                act_id=act_id,
                title=use_title,
                citation=citation,
                year=year,
                pdf_url=pdf_url,
                pdf_path=pdf_path,
                node_url=node_url,
                fetched_at=fetched_at,
            )
        except Exception as e:
            print(f"  [ERROR] Record build failed: {e}")
            gaps.append({
                "node_id": node_id,
                "title": listing_title,
                "reason": f"record_build_error: {e}",
                "url": node_url
            })
            continue

        records_created.append(record)
        existing_ids.add(act_id)
        print(f"  Sections: {len(record['sections'])}")

        rec_path = RECORDS_DIR / f"{act_id}.json"
        with rec_path.open("w") as f:
            json.dump(record, f, indent=2, ensure_ascii=False)
        print(f"  Saved: {rec_path.name}")

    print(f"\n=== Batch summary ===")
    print(f"Records created: {len(records_created)}")
    print(f"Gaps: {len(gaps)}")
    print(f"Fetches this batch: {batch_fetches[0]}")

    return records_created, gaps, batch_fetches[0]


if __name__ == "__main__":
    records, gaps, fetches = main()
    print(json.dumps({
        "records_created": len(records),
        "gaps": len(gaps),
        "fetches": fetches,
        "record_ids": [r["id"] for r in records],
        "gap_details": gaps,
    }, indent=2))
