#!/usr/bin/env python3
"""
Batch 0053: 2010 Acts No. 28-36 from parliament.gov.zm
Phase 4 bulk ingestion — up to 8 records.
Continuing from batch 0052 which ingested 2010 No. 37-45.
"""

import hashlib
import json
import os
import re
import sqlite3
import sys
import time
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import importlib.util
spec = importlib.util.spec_from_file_location("fetch_one", os.path.join(os.path.dirname(__file__), "fetch_one.py"))
fetch_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fetch_mod)

from bs4 import BeautifulSoup
import pdfplumber

WORKSPACE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(WORKSPACE)

BATCH_NUM = 53
RATE_LIMIT_PARLIAMENT = 2  # seconds between requests
PARSER_VERSION = "0.3.0"
MAX_RECORDS = 8

fetch_count = 0
records_added = []


def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def do_fetch(url, out_path=None):
    global fetch_count
    time.sleep(RATE_LIMIT_PARLIAMENT)
    result = fetch_mod.fetch(url)
    fetch_mod.log_provenance(result)
    fetch_count += 1

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


def discover_2010_acts_from_index():
    """Discover 2010 acts from parliament.gov.zm index pages."""
    discovered = {}  # act_number -> {node_url, title}

    # 2010 acts appear on pages ~21-25 of the index
    for page_num in range(20, 26):
        url = f"https://www.parliament.gov.zm/acts-of-parliament?page={page_num}"
        print(f"  Scanning index page {page_num}...")
        result = do_fetch(url)
        if not result:
            continue

        soup = BeautifulSoup(result["_body_bytes"], "html.parser")

        # Look for links containing "of 2010"
        for link in soup.find_all("a", href=True):
            text = link.get_text(strip=True)
            href = link["href"]

            # Match "No. X of 2010" in the link text
            match = re.search(r'No\.?\s*(\d+)\s+of\s+2010', text, re.IGNORECASE)
            if match:
                act_num = int(match.group(1))
                node_url = href if href.startswith("http") else f"https://www.parliament.gov.zm{href}"
                if act_num not in discovered:
                    discovered[act_num] = {"node_url": node_url, "title": text.strip()}
                    print(f"    Found: Act No. {act_num} of 2010 — {text.strip()[:60]}")

        # If we found 2009 content but no 2010, we've gone too far
        page_text = soup.get_text()
        if "2009" in page_text and "2010" not in page_text:
            break

    return discovered


def find_pdf_on_node_page(node_url):
    result = do_fetch(node_url)
    if not result:
        return None, None

    soup = BeautifulSoup(result["_body_bytes"], "html.parser")
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.lower().endswith(".pdf"):
            pdf_url = href if href.startswith("http") else f"https://www.parliament.gov.zm{href}"
            return pdf_url, link.get_text(strip=True)

    for span in soup.find_all("span", class_="file"):
        a = span.find("a", href=True)
        if a and a["href"].lower().endswith(".pdf"):
            pdf_url = a["href"] if a["href"].startswith("http") else f"https://www.parliament.gov.zm{a['href']}"
            return pdf_url, a.get_text(strip=True)

    return None, None


def parse_pdf_to_sections(pdf_path):
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

    lines = full_text.split("\n")
    current_section = None
    current_heading = ""
    current_body = []
    current_part = None
    current_part_title = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Detect Part headings
        part_match = re.match(r'^PART\s+([IVXLC]+)\s*[—\-–]?\s*(.*)', line, re.IGNORECASE)
        if part_match:
            current_part = part_match.group(1).upper()
            current_part_title = part_match.group(2).strip() or None
            continue

        # Match section numbers
        section_match = re.match(r'^(\d+)\.\s*[—\-–]?\s*(?:\(1\))?\s*(.*)', line)
        if section_match:
            if current_section is not None:
                sections.append({
                    "number": current_section,
                    "title": current_heading.strip(),
                    "part": current_part,
                    "part_title": current_part_title,
                    "page_start": None,
                    "body": "\n".join(current_body).strip() or None,
                    "subsections": []
                })

            current_section = section_match.group(1)
            heading_text = section_match.group(2).strip()
            current_heading = heading_text if heading_text else ""
            current_body = []
        elif current_section is not None:
            if not current_heading and line and line[0].isupper():
                current_heading = line
            else:
                current_body.append(line)

    if current_section is not None:
        sections.append({
            "number": current_section,
            "title": current_heading.strip(),
            "part": current_part,
            "part_title": current_part_title,
            "page_start": None,
            "body": "\n".join(current_body).strip() or None,
            "subsections": []
        })

    return sections


def slugify(title):
    s = title.lower().strip()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'[\s]+', '-', s)
    s = re.sub(r'-+', '-', s)
    return s.strip('-')[:80]


def build_record(act_number, year, title, sections, source_url, source_hash):
    slug = slugify(title)
    record_id = f"act-zm-{year}-{act_number:03d}-{slug}"
    # Truncate to max 128 chars
    if len(record_id) > 128:
        record_id = record_id[:128].rstrip('-')

    record = {
        "id": record_id,
        "type": "act",
        "jurisdiction": "ZM",
        "title": title,
        "citation": f"Act No. {act_number} of {year}",
        "date_of_assent": None,
        "commencement_date": None,
        "in_force": True,
        "version_type": "as_enacted",
        "consolidated_as_of": None,
        "amended_by": [],
        "repealed_by": None,
        "sections": sections,
        "source_url": source_url,
        "source_hash": f"sha256:{source_hash}",
        "fetched_at": utc_now(),
        "parser_version": PARSER_VERSION,
        "notes": None
    }

    return record_id, record


def save_record(record_id, record):
    out_dir = os.path.join("records", "acts")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{record_id}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
    return out_path


def update_sqlite(records):
    db_path = "corpus.sqlite"
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

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
            record["title"], record["citation"],
            record.get("date_of_assent") or "2010",
            1 if record["in_force"] else 0,
            record["source_url"], record["source_hash"],
            record["fetched_at"], record["parser_version"],
            section_count, json_path
        ))

        c.execute("INSERT OR REPLACE INTO records_fts(id, title, citation) VALUES (?, ?, ?)",
                  (record_id, record["title"], record["citation"]))

    conn.commit()
    conn.close()


def integrity_check(records):
    errors = []

    ids = [r[0] for r in records]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate IDs in batch")

    for record_id, record, json_path in records:
        raw_path = os.path.join("raw", "acts", f"{record_id}.pdf")
        if os.path.exists(raw_path):
            with open(raw_path, "rb") as f:
                actual_hash = hashlib.sha256(f.read()).hexdigest()
            expected_hash = record["source_hash"].replace("sha256:", "")
            if actual_hash != expected_hash:
                errors.append(f"{record_id}: source_hash mismatch")

        for field in ["id", "type", "jurisdiction", "title", "citation",
                      "source_url", "source_hash", "fetched_at", "parser_version"]:
            if not record.get(field):
                errors.append(f"{record_id}: missing required field '{field}'")

        # Validate ID format
        if not re.match(r'^[a-z0-9][a-z0-9-]*[a-z0-9]$', record_id):
            errors.append(f"{record_id}: invalid ID format")

    return errors


def main():
    print(f"=== Batch {BATCH_NUM:04d} START: {utc_now()} ===")
    print("Target: 2010 Acts No. 28-36")
    print()

    # Get existing 2010 act numbers
    existing = set()
    for f in os.listdir("records/acts"):
        m = re.match(r'act-zm-2010-(\d+)', f)
        if m:
            existing.add(int(m.group(1)))
    print(f"Existing 2010 acts: {sorted(existing)}")

    # Target range
    target_range = list(range(28, 37))  # 28-36
    needed = [n for n in target_range if n not in existing]
    print(f"Needed from range 28-36: {needed}")

    # Discover from index
    print("\nDiscovering 2010 acts from parliament index...")
    discovered = discover_2010_acts_from_index()
    print(f"\nDiscovered {len(discovered)} total 2010 acts on index")

    # Filter to needed
    available = {n: info for n, info in discovered.items() if n in needed}
    print(f"Available for ingestion: {sorted(available.keys())}")

    batch_records = []
    gaps = []

    for act_num in sorted(available.keys()):
        if len(batch_records) >= MAX_RECORDS:
            break

        info = available[act_num]
        print(f"\n--- Processing 2010 Act No. {act_num} ---")
        print(f"  Node: {info['node_url']}")

        # Get PDF URL from node page
        pdf_url, pdf_text = find_pdf_on_node_page(info["node_url"])
        if not pdf_url:
            print(f"  No PDF found")
            gaps.append({
                "act": f"Act No. {act_num} of 2010",
                "title": info["title"],
                "reason": "No PDF on node page",
                "node_url": info["node_url"]
            })
            continue

        print(f"  PDF: {pdf_url}")

        # Clean title from index
        title = info["title"]
        title = re.sub(r'\s+', ' ', title).strip()

        # Download PDF
        raw_dir = os.path.join("raw", "acts")
        os.makedirs(raw_dir, exist_ok=True)
        slug = slugify(title)
        preview_id = f"act-zm-2010-{act_num:03d}-{slug}"
        if len(preview_id) > 128:
            preview_id = preview_id[:128].rstrip('-')
        raw_path = os.path.join(raw_dir, f"{preview_id}.pdf")

        result = do_fetch(pdf_url, out_path=raw_path)
        if not result or result["error"]:
            gaps.append({
                "act": f"Act No. {act_num} of 2010",
                "title": title,
                "reason": f"PDF download failed: {result['error'] if result else 'no response'}",
                "url": pdf_url
            })
            continue

        source_hash = result["sha256"]
        print(f"  Downloaded: {result['body_len']} bytes, sha256:{source_hash[:16]}...")

        # Parse PDF
        sections = parse_pdf_to_sections(raw_path)
        print(f"  Parsed: {len(sections)} sections")

        # Try to extract cleaner title from PDF
        try:
            with pdfplumber.open(raw_path) as pdf:
                first_page = pdf.pages[0].extract_text() or ""
                title_match = re.search(
                    r'(?:The\s+)?(.+?(?:Act|Amendment)\s*,?\s*(?:No\.?\s*\d+\s+of\s+)?\d{4})',
                    first_page, re.IGNORECASE
                )
                if title_match:
                    clean = title_match.group(0).strip()
                    if 10 < len(clean) < 200:
                        title = re.sub(r'\s+', ' ', clean).strip()
        except:
            pass

        # Remove "The " prefix for consistency
        title = re.sub(r'^The\s+', '', title).strip()

        # Build and save record
        record_id, record = build_record(act_num, 2010, title, sections, pdf_url, source_hash)
        json_path = save_record(record_id, record)
        batch_records.append((record_id, record, json_path))
        records_added.append({
            "id": record_id,
            "title": record["title"],
            "citation": record["citation"],
            "sections": len(sections)
        })
        print(f"  Record: {record_id} ({len(sections)} sections)")

    # Check for acts in the target range that weren't on the index
    for act_num in needed:
        if act_num not in available and not any(
            r["citation"] == f"Act No. {act_num} of 2010" for r in records_added
        ):
            gaps.append({
                "act": f"Act No. {act_num} of 2010",
                "title": "Unknown",
                "reason": "Not found on parliament.gov.zm index pages 20-25"
            })

    print(f"\n=== Batch {BATCH_NUM:04d} FETCH COMPLETE: {len(batch_records)} records ===")
    print(f"Total fetches: {fetch_count}")

    if not batch_records:
        print("No records to commit. Logging gaps.")
        if gaps:
            with open("gaps.md", "a") as f:
                f.write(f"\n### Batch {BATCH_NUM:04d} — 2010 Acts gaps (No. 28-36)\n")
                for g in gaps:
                    f.write(f"- **{g['act']}** ({g.get('title', 'unknown')}): {g['reason']}\n")
        with open("worker.log", "a") as f:
            f.write(f"[{utc_now()}] Phase 4 Batch {BATCH_NUM:04d}: 0 records added. {len(gaps)} gaps. See gaps.md.\n")
        return

    # Integrity check
    print("\nRunning integrity checks...")
    errors = integrity_check(batch_records)
    if errors:
        print(f"INTEGRITY CHECK FAILED: {len(errors)} errors")
        for e in errors:
            print(f"  - {e}")
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

    # Update SQLite
    update_sqlite(batch_records)
    print("SQLite updated")

    # Count totals
    total_2010 = len([x for x in os.listdir("records/acts") if "2010" in x])
    total_all = len(os.listdir("records/acts"))
    total_judgments = len(os.listdir("records/judgments")) if os.path.isdir("records/judgments") else 0

    # Batch report
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
        f.write(f"- 2010 Acts progress: {total_2010}/~51 ingested\n")
        f.write(f"- Total fetches this batch: {fetch_count}\n")
        if gaps:
            f.write(f"- Gaps: {len(gaps)} acts not found\n")
            for g in gaps:
                f.write(f"  - {g['act']}: {g['reason']}\n")
        notable = [r for r in records_added if r["sections"] > 50]
        if notable:
            notable_str = ", ".join(r["title"] + " (" + str(r["sections"]) + " sections)" for r in notable)
            f.write(f"- Notable: {notable_str}\n")

    # Log gaps
    if gaps:
        with open("gaps.md", "a") as f:
            f.write(f"\n### Batch {BATCH_NUM:04d} — 2010 Acts gaps (No. 28-36)\n")
            for g in gaps:
                f.write(f"- **{g['act']}** ({g.get('title', 'unknown')}): {g['reason']}\n")

    # Worker log
    act_nums_added = [str(n) for n in sorted(available.keys()) if any(
        r['citation'] == f'Act No. {n} of 2010' for r in records_added
    )]
    with open("worker.log", "a") as f:
        f.write(
            f"[{utc_now()}] Phase 4 Batch {BATCH_NUM:04d} COMPLETE: "
            f"+{len(batch_records)} acts (2010 No. {', '.join(act_nums_added)}). "
            f"Fetches: {fetch_count}, total today: ~{96 + fetch_count}/2000. "
            f"Integrity checks: ALL PASS. Batch report: {report_path}. "
            f"2010 Acts: {total_2010}/~51 ingested. "
            f"B2 sync skipped — rclone not available in sandbox.\n"
        )

    print(f"\n=== Batch {BATCH_NUM:04d} DONE: +{len(batch_records)} records ===")
    print(f"Report: {report_path}")


if __name__ == "__main__":
    main()
