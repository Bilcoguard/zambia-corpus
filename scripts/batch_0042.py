#!/usr/bin/env python3
"""
Batch 0042: 2015 Acts No. 10, 14-20 from parliament.gov.zm
Phase 4 bulk ingestion — up to 8 records.
"""

import hashlib
import json
import os
import re
import sqlite3
import sys
import time
from datetime import datetime, timezone

# Add parent dir so we can import fetch_one as a module pattern
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# We'll use the fetch function directly from fetch_one
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import importlib.util
spec = importlib.util.spec_from_file_location("fetch_one", os.path.join(os.path.dirname(__file__), "fetch_one.py"))
fetch_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fetch_mod)

from bs4 import BeautifulSoup
import pdfplumber

WORKSPACE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(WORKSPACE)

BATCH_NUM = 42
RATE_LIMIT_PARLIAMENT = 2  # seconds between requests
USER_AGENT = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
PARSER_VERSION = "0.3.0"

# Target: 2015 Acts No. 10, 14, 15, 16, 17, 18, 19, 20
TARGET_ACTS = [10, 14, 15, 16, 17, 18, 19, 20]

fetch_count = 0
records_added = []


def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def do_fetch(url, out_path=None):
    """Fetch a URL using the audited fetcher, respecting rate limits."""
    global fetch_count
    time.sleep(RATE_LIMIT_PARLIAMENT)
    result = fetch_mod.fetch(url)
    fetch_mod.log_provenance(result)
    fetch_count += 1

    # Log to costs.log
    cost_entry = {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "url": url,
        "bytes": result["body_len"],
        "fetch_n": fetch_count
    }
    with open("costs.log", "a") as f:
        f.write(json.dumps(cost_entry) + "\n")

    if result["error"]:
        print(f"  ERROR fetching {url}: {result['error']}")
        return None

    if out_path and result["body_len"] > 0:
        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(result["_body_bytes"])

    return result


def find_act_on_index_pages(act_number, year=2015):
    """Search parliament.gov.zm index pages for a specific act."""
    # Try pages 1-15 (2015 acts should be in later pages)
    for page_num in range(1, 16):
        url = f"https://www.parliament.gov.zm/acts-of-parliament?page={page_num}"
        result = do_fetch(url)
        if not result:
            continue

        soup = BeautifulSoup(result["_body_bytes"], "html.parser")
        links = soup.find_all("a", href=True)

        for link in links:
            text = link.get_text(strip=True)
            href = link["href"]
            # Look for "No. X of 2015" pattern
            pattern = rf'(?:No\.?\s*{act_number}\s+of\s+{year}|Act\s+No\.?\s*{act_number}\s+of\s+{year})'
            if re.search(pattern, text, re.IGNORECASE):
                node_url = href if href.startswith("http") else f"https://www.parliament.gov.zm{href}"
                return node_url, text

        # Check if we've gone past 2015 content (page has older years)
        page_text = soup.get_text()
        if "2014" in page_text and "2015" not in page_text:
            break

    return None, None


def find_pdf_on_node_page(node_url):
    """Extract PDF link from a parliament node page."""
    result = do_fetch(node_url)
    if not result:
        return None, None

    soup = BeautifulSoup(result["_body_bytes"], "html.parser")
    # Look for PDF links
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.lower().endswith(".pdf"):
            pdf_url = href if href.startswith("http") else f"https://www.parliament.gov.zm{href}"
            return pdf_url, link.get_text(strip=True)

    # Also check for embedded file links
    for link in soup.find_all("span", class_="file"):
        a = link.find("a", href=True)
        if a and a["href"].lower().endswith(".pdf"):
            pdf_url = a["href"] if a["href"].startswith("http") else f"https://www.parliament.gov.zm{a['href']}"
            return pdf_url, a.get_text(strip=True)

    return None, None


def parse_pdf_to_sections(pdf_path):
    """Parse a PDF into sections."""
    sections = []
    full_text = ""

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text() or ""
                full_text += text + "\n"
    except Exception as e:
        print(f"  PDF parse error: {e}")
        return []

    # Split into sections by looking for section number patterns
    # Pattern: number followed by period or parenthesis at start of line
    lines = full_text.split("\n")
    current_section = None
    current_heading = ""
    current_text = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Match section numbers like "3.", "3.—(1)", "3. ", etc.
        section_match = re.match(r'^(\d+)\.\s*[—\-]?\s*(?:\(1\))?\s*(.*)', line)
        if section_match:
            # Save previous section
            if current_section is not None:
                sections.append({
                    "number": current_section,
                    "heading": current_heading.strip(),
                    "text": "\n".join(current_text).strip()
                })

            current_section = section_match.group(1)
            heading_text = section_match.group(2).strip()

            # Check if the heading is on this line or split
            if heading_text:
                current_heading = heading_text
            else:
                current_heading = ""
            current_text = []
        elif current_section is not None:
            # Check if this line is a heading continuation (CAPS or specific pattern)
            if not current_heading and line and line[0].isupper():
                current_heading = line
            else:
                current_text.append(line)

    # Don't forget last section
    if current_section is not None:
        sections.append({
            "number": current_section,
            "heading": current_heading.strip(),
            "text": "\n".join(current_text).strip()
        })

    return sections


def slugify(title):
    """Create a URL-safe slug from a title."""
    s = title.lower().strip()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'[\s]+', '-', s)
    s = re.sub(r'-+', '-', s)
    return s.strip('-')


def build_record(act_number, year, title, sections, source_url, source_hash, pdf_path):
    """Build a corpus record."""
    slug = slugify(title)
    record_id = f"act-zm-{year}-{act_number:03d}-{slug}"

    record = {
        "id": record_id,
        "type": "act",
        "jurisdiction": "ZM",
        "title": title,
        "citation": f"Act No. {act_number} of {year}",
        "enacted_date": str(year),
        "commencement_date": None,
        "in_force": True,
        "amended_by": [],
        "repealed_by": None,
        "sections": sections,
        "source_url": source_url,
        "source_hash": f"sha256:{source_hash}",
        "fetched_at": utc_now(),
        "parser_version": PARSER_VERSION
    }

    return record_id, record


def save_record(record_id, record):
    """Save record JSON file."""
    out_dir = os.path.join("records", "acts")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{record_id}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
    return out_path


def update_sqlite(records):
    """Update corpus.sqlite with new records."""
    db_path = "corpus.sqlite"
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Ensure table exists
    c.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id TEXT PRIMARY KEY,
            type TEXT,
            jurisdiction TEXT,
            title TEXT,
            citation TEXT,
            enacted_date TEXT,
            in_force INTEGER,
            source_url TEXT,
            source_hash TEXT,
            fetched_at TEXT,
            parser_version TEXT,
            section_count INTEGER,
            json_path TEXT
        )
    """)

    # Ensure FTS table exists
    c.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS records_fts USING fts5(
            id, title, citation, content='records',
            content_rowid='rowid'
        )
    """)

    for record_id, record, json_path in records:
        section_count = len(record.get("sections", []))
        c.execute("""
            INSERT OR REPLACE INTO records
            (id, type, jurisdiction, title, citation, enacted_date, in_force,
             source_url, source_hash, fetched_at, parser_version, section_count, json_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            record_id, record["type"], record["jurisdiction"],
            record["title"], record["citation"], record["enacted_date"],
            1 if record["in_force"] else 0,
            record["source_url"], record["source_hash"],
            record["fetched_at"], record["parser_version"],
            section_count, json_path
        ))

        # Update FTS
        c.execute("INSERT OR REPLACE INTO records_fts(id, title, citation) VALUES (?, ?, ?)",
                  (record_id, record["title"], record["citation"]))

    conn.commit()
    conn.close()


def integrity_check(records):
    """Run integrity checks on the batch."""
    errors = []

    # Check no duplicate IDs
    ids = [r[0] for r in records]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate IDs in batch")

    # Check each record
    for record_id, record, json_path in records:
        # Check source_hash matches raw file
        raw_path = os.path.join("raw", "acts", f"{record_id}.pdf")
        if os.path.exists(raw_path):
            with open(raw_path, "rb") as f:
                actual_hash = hashlib.sha256(f.read()).hexdigest()
            expected_hash = record["source_hash"].replace("sha256:", "")
            if actual_hash != expected_hash:
                errors.append(f"{record_id}: source_hash mismatch (expected {expected_hash}, got {actual_hash})")

        # Check required fields
        for field in ["id", "type", "jurisdiction", "title", "citation", "source_url", "source_hash", "fetched_at", "parser_version"]:
            if not record.get(field):
                errors.append(f"{record_id}: missing required field '{field}'")

        # Check amended_by/repealed_by references resolve (if any)
        # For new records, these are typically empty

    # Check against existing DB for duplicate IDs
    if os.path.exists("corpus.sqlite"):
        conn = sqlite3.connect("corpus.sqlite")
        c = conn.cursor()
        for rid in ids:
            c.execute("SELECT id FROM records WHERE id = ?", (rid,))
            if c.fetchone():
                # It's okay to update existing records, but log it
                print(f"  Note: {rid} already exists in DB, will be updated")
        conn.close()

    return errors


# Known act mappings for 2015 (from parliament.gov.zm discovery)
# We'll try to find them on the index pages
KNOWN_2015_ACTS = {
    10: "The Zambia Wildlife Act",
    14: "The Appropriation Act",
    15: "The Zambia Institute of Chartered Accountants Act",
    16: "The National Health Insurance Act",
    17: "The Cyber Security and Cyber Crimes Act",
    18: "The Electronic Communications and Transactions Act",
    19: "The Public-Private Partnership Act",
    20: "The Planning and Budgeting Act",
}


def main():
    print(f"=== Batch {BATCH_NUM:04d} START: {utc_now()} ===")
    print(f"Target: 2015 Acts No. {TARGET_ACTS}")
    print()

    batch_records = []
    gaps = []

    for act_num in TARGET_ACTS:
        print(f"\n--- Processing 2015 Act No. {act_num} ---")
        expected_title = KNOWN_2015_ACTS.get(act_num, f"Act No. {act_num} of 2015")

        # Step 1: Try direct node URL patterns
        # Parliament.gov.zm node IDs for 2015 acts vary, so search index
        node_url = None
        pdf_url = None
        actual_title = expected_title

        # Try to find on index pages
        node_url, link_text = find_act_on_index_pages(act_num, 2015)

        if node_url:
            print(f"  Found node: {node_url} ({link_text})")
            if link_text:
                actual_title = link_text

            # Get PDF from node page
            pdf_url, pdf_text = find_pdf_on_node_page(node_url)

        if not pdf_url:
            print(f"  No PDF found for 2015 Act No. {act_num}")
            gaps.append({
                "act": f"Act No. {act_num} of 2015",
                "title": expected_title,
                "reason": "No PDF found on parliament.gov.zm",
                "node_url": node_url
            })
            continue

        print(f"  PDF: {pdf_url}")

        # Step 2: Download PDF
        raw_dir = os.path.join("raw", "acts")
        os.makedirs(raw_dir, exist_ok=True)
        slug = slugify(actual_title)
        record_id_preview = f"act-zm-2015-{act_num:03d}-{slug}"
        raw_path = os.path.join(raw_dir, f"{record_id_preview}.pdf")

        result = do_fetch(pdf_url, out_path=raw_path)
        if not result or result["error"]:
            gaps.append({
                "act": f"Act No. {act_num} of 2015",
                "title": actual_title,
                "reason": f"PDF download failed: {result['error'] if result else 'no response'}",
                "url": pdf_url
            })
            continue

        source_hash = result["sha256"]
        print(f"  Downloaded: {result['body_len']} bytes, sha256:{source_hash[:16]}...")

        # Step 3: Parse PDF
        sections = parse_pdf_to_sections(raw_path)
        print(f"  Parsed: {len(sections)} sections")

        # Extract cleaner title from PDF content if possible
        try:
            with pdfplumber.open(raw_path) as pdf:
                first_page = pdf.pages[0].extract_text() or ""
                # Try to find the act title
                title_match = re.search(r'(?:The\s+)?(.+?)(?:\s*Act\s*,?\s*(?:No\.?\s*\d+\s+of\s+)?\d{4})', first_page, re.IGNORECASE)
                if title_match:
                    clean = title_match.group(0).strip()
                    # Only use if reasonable length
                    if 10 < len(clean) < 200:
                        actual_title = clean
        except:
            pass

        # Clean up the title
        actual_title = re.sub(r'\s+', ' ', actual_title).strip()
        # Remove "The" prefix for consistency with existing records
        title_for_record = re.sub(r'^The\s+', '', actual_title).strip()

        # Step 4: Build record
        record_id, record = build_record(act_num, 2015, title_for_record, sections,
                                          pdf_url, source_hash, raw_path)
        json_path = save_record(record_id, record)
        batch_records.append((record_id, record, json_path))
        records_added.append({
            "id": record_id,
            "title": record["title"],
            "citation": record["citation"],
            "sections": len(sections)
        })
        print(f"  Record: {record_id} ({len(sections)} sections)")

    print(f"\n=== Batch {BATCH_NUM:04d} FETCH COMPLETE: {len(batch_records)} records ===")
    print(f"Total fetches: {fetch_count}")

    if not batch_records:
        print("No records to commit. Logging gaps and stopping.")
        if gaps:
            with open("gaps.md", "a") as f:
                f.write(f"\n### Batch {BATCH_NUM:04d} — 2015 Acts gaps\n")
                for g in gaps:
                    f.write(f"- **{g['act']}** ({g.get('title', 'unknown')}): {g['reason']}\n")
        with open("worker.log", "a") as f:
            f.write(f"[{utc_now()}] Phase 4 Batch {BATCH_NUM:04d}: 0 records added. {len(gaps)} gaps. See gaps.md.\n")
        return

    # Step 5: Integrity check
    print("\nRunning integrity checks...")
    errors = integrity_check(batch_records)
    if errors:
        print(f"INTEGRITY CHECK FAILED: {len(errors)} errors")
        for e in errors:
            print(f"  - {e}")
        # Write diagnostics
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        os.makedirs("error-reports", exist_ok=True)
        with open(f"error-reports/{ts}.md", "w") as f:
            f.write(f"# Batch {BATCH_NUM:04d} Integrity Failure\n\n")
            for e in errors:
                f.write(f"- {e}\n")
        with open("gaps.md", "a") as f:
            f.write(f"\n### Batch {BATCH_NUM:04d} — Integrity check failed\n")
            for e in errors:
                f.write(f"- {e}\n")
        with open("worker.log", "a") as f:
            f.write(f"[{utc_now()}] Phase 4 Batch {BATCH_NUM:04d} INTEGRITY FAIL: {len(errors)} errors. NOT committed.\n")
        sys.exit(1)

    print("Integrity checks: ALL PASS")

    # Step 6: Update SQLite
    update_sqlite(batch_records)
    print("SQLite updated")

    # Step 7: Write batch report
    os.makedirs("reports", exist_ok=True)
    report_path = f"reports/batch-{BATCH_NUM:04d}.md"
    with open(report_path, "w") as f:
        f.write(f"# Batch {BATCH_NUM:04d} Report\n\n")
        f.write(f"**Date:** {utc_now()}\n")
        f.write(f"**Phase:** 4 (Bulk Ingestion)\n")
        f.write(f"**Records added:** {len(batch_records)}\n")
        f.write(f"**Source:** parliament.gov.zm\n\n")
        f.write("## Records\n\n")
        for r in records_added:
            f.write(f"- **{r['citation']}** — {r['title']} ({r['sections']} sections)\n")
        f.write(f"\n## Notes\n\n")
        existing_2015 = len([x for x in os.listdir("records/acts") if "2015" in x])
        f.write(f"- 2015 Acts progress: {existing_2015}/23 ingested\n")
        f.write(f"- Total fetches this batch: {fetch_count}\n")
        if gaps:
            f.write(f"- Gaps: {len(gaps)} acts not found\n")
            for g in gaps:
                f.write(f"  - {g['act']}: {g['reason']}\n")

    # Log gaps
    if gaps:
        with open("gaps.md", "a") as f:
            f.write(f"\n### Batch {BATCH_NUM:04d} — 2015 Acts gaps\n")
            for g in gaps:
                f.write(f"- **{g['act']}** ({g.get('title', 'unknown')}): {g['reason']}\n")

    # Worker log
    titles_summary = ", ".join([r['title'][:30] for r in records_added[:3]]) + ("..." if len(records_added) > 3 else "")
    with open("worker.log", "a") as f:
        f.write(f"[{utc_now()}] Phase 4 Batch {BATCH_NUM:04d} COMPLETE: +{len(batch_records)} acts (2015 No. {', '.join(str(a) for a in TARGET_ACTS if any(r['citation'].endswith(f'{a} of 2015') for r in records_added))}). "
                f"Fetches: {fetch_count}, total today: ~{306 + fetch_count}/2000. "
                f"Integrity checks: ALL PASS. Batch report: {report_path}. "
                f"B2 sync skipped — rclone not available in sandbox.\n")

    print(f"\n=== Batch {BATCH_NUM:04d} DONE: +{len(batch_records)} records ===")
    print(f"Report: {report_path}")


if __name__ == "__main__":
    main()
