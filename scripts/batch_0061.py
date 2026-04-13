#!/usr/bin/env python3
"""Batch 0061: Continue 2004 and earlier Acts from parliament.gov.zm pages 27+"""

import requests
import hashlib
import json
import os
import re
import time
import sqlite3
import pdfplumber
from datetime import datetime, timezone
from bs4 import BeautifulSoup

WORKSPACE = "/sessions/upbeat-confident-gauss/corpus-work"
os.chdir(WORKSPACE)

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
PARSER_VERSION = "0.3.0"
MAX_BATCH = 8
RATE_LIMIT = 2  # seconds between requests

session = requests.Session()
session.headers.update(HEADERS)
session.verify = False  # parliament.gov.zm SSL chain issues

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

fetches_today = 0
records_added = []
gaps = []

def log_fetch(url, nbytes):
    global fetches_today
    fetches_today += 1
    with open("costs.log", "a") as f:
        f.write(json.dumps({
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "url": url,
            "bytes": nbytes,
            "fetch_n": fetches_today
        }) + "\n")

def fetch_page(url):
    time.sleep(RATE_LIMIT)
    resp = session.get(url, timeout=30)
    resp.raise_for_status()
    log_fetch(url, len(resp.content))
    return resp

def fetch_pdf(url):
    time.sleep(RATE_LIMIT)
    resp = session.get(url, timeout=60)
    resp.raise_for_status()
    log_fetch(url, len(resp.content))
    return resp.content

def sha256_hash(data):
    return "sha256:" + hashlib.sha256(data).hexdigest()

def extract_sections(pdf_path):
    """Extract sections from PDF using pdfplumber"""
    sections = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
            
            if not full_text.strip():
                return sections  # scanned PDF, needs OCR
            
            # Try to find sections with pattern "N. Heading text"
            # or "PART N" patterns
            section_pattern = re.compile(
                r'^(\d+)\.\s+(.+?)(?=\n\d+\.\s|\nPART\s|\nSCHEDULE|\Z)',
                re.MULTILINE | re.DOTALL
            )
            
            matches = list(section_pattern.finditer(full_text))
            if matches:
                for i, m in enumerate(matches):
                    num = m.group(1)
                    rest = m.group(2).strip()
                    # First line is heading, rest is text
                    lines = rest.split('\n', 1)
                    heading = lines[0].strip()
                    text = lines[1].strip() if len(lines) > 1 else ""
                    sections.append({
                        "number": num,
                        "heading": heading,
                        "text": text[:5000]  # cap text length
                    })
            else:
                # Fallback: store as single section
                sections.append({
                    "number": "1",
                    "heading": "Full text",
                    "text": full_text[:10000]
                })
    except Exception as e:
        print(f"  PDF parse error: {e}")
    return sections

def make_id(year, number, title):
    """Generate a record ID"""
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')[:80]
    return f"act-zm-{year}-{number:03d}-{slug}"

def load_existing_ids():
    ids = set()
    conn = sqlite3.connect("corpus.sqlite")
    c = conn.cursor()
    c.execute("SELECT id FROM records")
    for row in c.fetchall():
        ids.add(row[0])
    conn.close()
    return ids

# Load existing IDs to avoid duplicates
existing_ids = load_existing_ids()
print(f"Existing records: {len(existing_ids)}")

# Discover acts from parliament.gov.zm listing pages
# Previous batches covered pages 0-26. Continue from page 27.
discovered = []

for page_num in range(27, 35):  # scan a range of pages
    url = f"https://www.parliament.gov.zm/acts-of-parliament?page={page_num}"
    try:
        resp = fetch_page(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Find act links - they're in td elements or div.view-content
        links = soup.find_all('a', href=re.compile(r'/node/\d+'))
        
        page_acts = []
        for link in links:
            href = link.get('href', '')
            title = link.get_text(strip=True)
            if not title or len(title) < 5:
                continue
            if '/node/' not in href:
                continue
            # Skip navigation links
            if title.lower() in ('first', 'last', 'next', 'previous', '«', '»'):
                continue
            
            node_url = f"https://www.parliament.gov.zm{href}"
            
            # Try to extract year from title
            year_match = re.search(r',?\s*(\d{4})\s*$', title)
            if not year_match:
                year_match = re.search(r'\b(19\d{2}|20[0-2]\d)\b', title)
            
            year = int(year_match.group(1)) if year_match else None
            
            page_acts.append({
                'title': title,
                'node_url': node_url,
                'year': year
            })
        
        print(f"Page {page_num}: found {len(page_acts)} act links")
        discovered.extend(page_acts)
        
        # If page returns no acts, we've gone past the end
        if len(page_acts) == 0:
            print(f"Page {page_num} empty, stopping discovery")
            break
            
    except Exception as e:
        print(f"Page {page_num} error: {e}")
        break

print(f"\nTotal discovered: {len(discovered)} act links")

# Filter to acts we haven't ingested yet (focus on 2004 and earlier, plus any missed)
# and deduplicate by node URL
seen_urls = set()
candidates = []
for act in discovered:
    if act['node_url'] in seen_urls:
        continue
    seen_urls.add(act['node_url'])
    candidates.append(act)

print(f"Unique candidates: {len(candidates)}")

# Now fetch node pages and PDFs for up to MAX_BATCH acts
ingested = 0
for act in candidates:
    if ingested >= MAX_BATCH:
        break
    
    print(f"\nProcessing: {act['title']}")
    
    try:
        # Fetch node page to find PDF link and metadata
        resp = fetch_page(act['node_url'])
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Find PDF link
        pdf_link = None
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.endswith('.pdf') or '.pdf' in href:
                if 'parliament.gov.zm' in href or href.startswith('/'):
                    if href.startswith('/'):
                        href = f"https://www.parliament.gov.zm{href}"
                    pdf_link = href
                    break
        
        if not pdf_link:
            print(f"  No PDF found on node page")
            gaps.append(f"No PDF on {act['node_url']} for: {act['title']}")
            continue
        
        # Try to extract act number from title or page
        num_match = re.search(r'(?:No\.?\s*|Act\s+)(\d+)\s+of\s+(\d{4})', act['title'], re.IGNORECASE)
        if not num_match:
            # Try from page content
            page_text = soup.get_text()
            num_match = re.search(r'(?:No\.?\s*|Act\s+)(\d+)\s+of\s+(\d{4})', page_text, re.IGNORECASE)
        
        if num_match:
            act_number = int(num_match.group(1))
            act_year = int(num_match.group(2))
        elif act['year']:
            act_number = 0
            act_year = act['year']
        else:
            print(f"  Could not determine act number/year")
            gaps.append(f"Could not parse number/year for: {act['title']} at {act['node_url']}")
            continue
        
        # Generate ID and check for duplicates
        record_id = make_id(act_year, act_number, act['title'])
        
        if record_id in existing_ids:
            print(f"  Already exists: {record_id}")
            continue
        
        # Fetch PDF
        print(f"  Fetching PDF: {pdf_link}")
        pdf_data = fetch_pdf(pdf_link)
        
        if len(pdf_data) < 100:
            print(f"  PDF too small ({len(pdf_data)} bytes), skipping")
            gaps.append(f"PDF too small for {act['title']}: {pdf_link}")
            continue
        
        # Save raw PDF
        raw_dir = f"raw/bulk/parliament-zm"
        os.makedirs(raw_dir, exist_ok=True)
        raw_path = f"{raw_dir}/{record_id}.pdf"
        with open(raw_path, 'wb') as f:
            f.write(pdf_data)
        
        source_hash = sha256_hash(pdf_data)
        
        # Extract sections
        sections = extract_sections(raw_path)
        needs_ocr = len(sections) == 0
        
        # Extract enacted_date from title or page
        enacted_date = None
        date_match = re.search(r'(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})', 
                              soup.get_text())
        if date_match:
            try:
                enacted_date = datetime.strptime(f"{date_match.group(1)} {date_match.group(2)} {date_match.group(3)}", "%d %B %Y").strftime("%Y-%m-%d")
            except:
                pass
        
        # Clean up title
        clean_title = re.sub(r'\s*\|.*$', '', act['title']).strip()
        clean_title = re.sub(r',?\s*\d{4}\s*$', '', clean_title).strip()
        if clean_title.startswith('The '):
            clean_title_for_display = clean_title
        else:
            clean_title_for_display = clean_title
        
        # Build record
        record = {
            "id": record_id,
            "type": "act",
            "jurisdiction": "ZM",
            "title": clean_title_for_display,
            "citation": f"Act No. {act_number} of {act_year}" if act_number > 0 else f"Act of {act_year}",
            "enacted_date": enacted_date,
            "commencement_date": None,
            "in_force": True,
            "amended_by": [],
            "repealed_by": None,
            "sections": sections,
            "source_url": pdf_link,
            "source_hash": source_hash,
            "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "parser_version": PARSER_VERSION
        }
        
        # Save JSON record
        record_dir = f"records/acts"
        os.makedirs(record_dir, exist_ok=True)
        record_path = f"{record_dir}/{record_id}.json"
        with open(record_path, 'w') as f:
            json.dump(record, f, indent=2)
        
        existing_ids.add(record_id)
        records_added.append({
            'id': record_id,
            'title': clean_title_for_display,
            'year': act_year,
            'number': act_number,
            'sections': len(sections),
            'needs_ocr': needs_ocr,
            'source_url': pdf_link
        })
        
        # Log provenance
        with open("provenance.log", "a") as f:
            f.write(json.dumps({
                "id": record_id,
                "source_url": pdf_link,
                "source_hash": source_hash,
                "fetched_at": record["fetched_at"],
                "parser_version": PARSER_VERSION,
                "sections_extracted": len(sections)
            }) + "\n")
        
        ingested += 1
        print(f"  Ingested: {record_id} ({len(sections)} sections)")
        
    except Exception as e:
        print(f"  Error: {e}")
        gaps.append(f"Error processing {act['title']}: {e}")
        continue

print(f"\n=== Batch 0061 Summary ===")
print(f"Records added: {len(records_added)}")
print(f"Fetches this batch: {fetches_today}")
print(f"Gaps: {len(gaps)}")

# Write results for post-processing
with open("/tmp/batch_0061_results.json", "w") as f:
    json.dump({
        "records_added": records_added,
        "gaps": gaps,
        "fetches": fetches_today
    }, f, indent=2)

print("\nDone.")
