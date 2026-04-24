#!/usr/bin/env python3
"""
Batch 0175 — Phase 4 sis_corporate: ingest 2 known corporate SIs from
batch-0174 discovery, plus continue /legislation/subsidiary listing sweep
(pages 5 and 6) to surface more corporate candidates for next tick.

Ingest targets (from batch 0174 page-4 discovery):
  1. si/2020/27  Income Tax (Remission) (Ndola Lime Company Limited) Order, 2020
  2. si/2020/28  Mines and Minerals Development (Remission) (Ndola Lime
                 Company Limited) Regulations, 2020

Both were filtered as corporate-adjacent (keyword "compan"), are novel vs
HEAD (records/sis), and reside at zambialii.org/akn/zm/act/si/2020/NN.

Additional discovery: fetch /legislation/subsidiary?page=5 and page=6 for
next-tick corporate-keyword candidate surfacing.

Robots.txt: /akn/zm/act/si/ and /legislation/subsidiary both Allow: / under
zambialii.org robots. Crawl-delay: 5s honoured. No /search/ or /api/.

Wall-clock guard: ~8 minutes of processing inside the 20-min tick.

Workspace path uses os.getcwd() per batch-0173 next-tick fix.
"""

import hashlib
import io
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from html.parser import HTMLParser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch_one import fetch, log_provenance  # noqa: E402

BATCH_NUM = "0175"
USER_AGENT = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
PARSER_VERSION = "0.5.0"
RATE_LIMIT_ZAMBIALII = 5
MAX_RECORDS = 8
WALL_CLOCK_BUDGET_SECS = 8 * 60

WORKSPACE = os.getcwd()
RAW_SI_DIR = os.path.join(WORKSPACE, "raw", "zambialii", "si")
RAW_DISC_DIR = os.path.join(WORKSPACE, "raw", "zambialii", "discovery")
RECORDS_DIR = os.path.join(WORKSPACE, "records", "sis")
COSTS_LOG = os.path.join(WORKSPACE, "costs.log")
REPORTS_DIR = os.path.join(WORKSPACE, "reports")
STATE_PATH = os.path.join(WORKSPACE, f".batch_{BATCH_NUM}_state.json")

os.makedirs(RAW_SI_DIR, exist_ok=True)
os.makedirs(RAW_DISC_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

CORPORATE_KEYWORDS = [
    "compan", "corporate", "pacra", "patent", "trademark", "trade mark",
    "intellectual property", "bank", "financial", "securities",
    "stock exchange", "capital market", "insur", "pension", "procurement",
    "anti-money", "money launder", "financial intelligence", "competition",
    "consumer protection", "investment",
]

# Ingest candidates selected from batch-0174 page-4 discovery
CANDIDATES = [
    (2020, 27,
     "Income Tax (Remission) (Ndola Lime Company Limited) Order, 2020",
     "income-tax-remission-ndola-lime-company-limited-order-2020",
     "corporate-tax-remission"),
    (2020, 28,
     "Mines and Minerals Development (Remission) (Ndola Lime Company Limited) Regulations, 2020",
     "mines-and-minerals-development-remission-ndola-lime-company-limited-regulations-2020",
     "corporate-tax-remission"),
]

# Additional discovery pages (pages 5 and 6; page 4 was batch 0174)
DISCOVERY_PAGES = [5, 6]

fetch_count = 0
_last_fetch_ts = 0.0


def utc_now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def rate_limit():
    global _last_fetch_ts
    if _last_fetch_ts:
        elapsed = time.time() - _last_fetch_ts
        remaining = RATE_LIMIT_ZAMBIALII - elapsed
        if remaining > 0:
            time.sleep(remaining)


def do_fetch(url, batch_tag=None, fetch_n_override=None):
    global fetch_count, _last_fetch_ts
    rate_limit()
    result = fetch(url)
    _last_fetch_ts = time.time()
    fetch_count += 1
    log_provenance(result)
    entry = {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "url": url,
        "bytes": result["body_len"],
        "batch": batch_tag or BATCH_NUM,
        "fetch_n": fetch_n_override if fetch_n_override is not None else fetch_count,
    }
    with open(COSTS_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return result


def slugify(title):
    s = title.lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    s = re.sub(r"-+", "-", s)
    return s


def parse_html_sections(html_text):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_text, "html.parser")
    title_el = soup.find("h1") or soup.find("title")
    title = title_el.get_text(strip=True) if title_el else ""

    sections = []
    akn_sections = soup.find_all(
        ["section", "div"], class_=re.compile(r"akn-section")
    )
    if not akn_sections:
        akn_sections = soup.find_all(id=re.compile(r"sec_|chp_"))
    for sec in akn_sections:
        num_el = sec.find(class_=re.compile(r"akn-num"))
        heading_el = sec.find(class_=re.compile(r"akn-heading"))
        num = num_el.get_text(strip=True).rstrip(".") if num_el else ""
        heading = heading_el.get_text(strip=True) if heading_el else ""
        text_parts = []
        for child in sec.find_all(
            class_=re.compile(r"akn-content|akn-intro|akn-paragraph|akn-subsection")
        ):
            t = child.get_text(" ", strip=True)
            if t and t not in text_parts:
                text_parts.append(t)
        if not text_parts:
            text = sec.get_text(" ", strip=True)
            if heading and text.startswith(heading):
                text = text[len(heading):].strip()
            if num and text.startswith(num):
                text = text[len(num):].strip()
        else:
            text = "\n".join(text_parts)
        if num or heading or text:
            sections.append({"number": num, "heading": heading, "text": text[:5000]})
    return title, sections


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
    title = lines[0].strip() if lines else ""
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
    return title, sections


def extract_og_title(html_text):
    m = re.search(r'<meta\s+property="og:title"\s+content="([^"]+)"', html_text)
    return m.group(1).strip() if m else ""


def build_record(year, number, title, sections, source_url, source_hash, fetched_at):
    slug = slugify(title) if title else f"si-{year}-{number}"
    record_id = f"si-zm-{year}-{number:03d}-{slug}"
    if len(record_id) > 128:
        record_id = record_id[:128].rstrip("-")
    return {
        "id": record_id,
        "type": "si",
        "jurisdiction": "ZM",
        "title": title,
        "citation": f"Statutory Instrument No. {number} of {year}",
        "enacted_date": None,
        "commencement_date": None,
        "in_force": True,
        "amended_by": [],
        "repealed_by": None,
        "sections": sections,
        "source_url": source_url,
        "source_hash": f"sha256:{source_hash}",
        "fetched_at": fetched_at,
        "parser_version": PARSER_VERSION,
    }


def process_si(year, number, title_hint, slug_hint, try_pdf_fallback=True):
    html_url = f"https://zambialii.org/akn/zm/act/si/{year}/{number}"
    print(f"\n--- {slug_hint} (si/{year}/{number}) ---")
    print(f"  Fetching HTML: {html_url}")
    r = do_fetch(html_url)

    if r["status"] != 200 or r["body_len"] < 1000:
        return None, None, f"HTML fetch failed: status={r['status']} len={r['body_len']}"

    html_body = r["_body_bytes"]
    html_hash = r["sha256"]
    source_url = r["final_url"] or html_url
    source_hash = html_hash
    fetched_at = r["started_at"]
    used_source = "html"
    html_text = html_body.decode("utf-8", errors="replace")

    og = extract_og_title(html_text)
    parsed_title, sections = parse_html_sections(html_text)
    title = og or parsed_title or title_hint
    title = re.sub(r"\s+", " ", title).strip()

    def token_set(t):
        return set(re.findall(r"[a-z0-9]+", t.lower()))

    if title_hint:
        expected = token_set(title_hint)
        actual = token_set(title)
        overlap = len(expected & actual)
        if overlap < max(3, len(expected) // 4):
            return None, None, (
                f"title_hint/og_title mismatch: hint={title_hint!r} "
                f"og={title!r} overlap={overlap}"
            )

    pdf_body = None
    pdf_hash = None
    pdf_url_used = None
    if try_pdf_fallback and len(sections) < 2:
        pdf_url = (r["final_url"] or html_url).rstrip("/") + "/source.pdf"
        print(f"  HTML sparse (sections={len(sections)}), trying PDF: {pdf_url}")
        pr = do_fetch(pdf_url)
        if pr["status"] == 200 and pr["body_len"] > 500:
            pdf_body = pr["_body_bytes"]
            pdf_hash = pr["sha256"]
            pdf_url_used = pr["final_url"] or pdf_url
            ptitle, psections = parse_pdf_sections(pdf_body)
            if psections:
                sections = psections
                source_url = pdf_url_used
                source_hash = pdf_hash
                used_source = "pdf"
                fetched_at = pr["started_at"]

    if not sections:
        return None, None, "no parseable sections in HTML or PDF"

    slug = slugify(title) if title else slug_hint
    record_id = f"si-zm-{year}-{number:03d}-{slug}"
    if len(record_id) > 128:
        record_id = record_id[:128].rstrip("-")

    raw_subdir = os.path.join(RAW_SI_DIR, str(year))
    os.makedirs(raw_subdir, exist_ok=True)

    html_path = os.path.join(raw_subdir, f"{record_id}.html")
    with open(html_path, "wb") as f:
        f.write(html_body)
    print(f"  Saved HTML raw: {html_path} ({len(html_body)} bytes)")

    pdf_path = None
    if pdf_body is not None:
        pdf_path = os.path.join(raw_subdir, f"{record_id}.pdf")
        with open(pdf_path, "wb") as f:
            f.write(pdf_body)
        print(f"  Saved PDF raw: {pdf_path} ({len(pdf_body)} bytes)")

    raw_path = pdf_path if used_source == "pdf" else html_path

    record = build_record(year, number, title, sections, source_url, source_hash, fetched_at)

    record_subdir = os.path.join(RECORDS_DIR, str(year))
    os.makedirs(record_subdir, exist_ok=True)
    record_path = os.path.join(record_subdir, f"{record['id']}.json")
    with open(record_path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
    print(f"  Saved record: {record_path}")
    print(f"  Title: {title!r}")
    print(f"  Sections: {len(sections)} (source={used_source})")
    return record, raw_path, None


class SubsidiaryListingParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_a = False
        self.cur_href = None
        self.cur_text_parts = []
        self.results = []

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


def discover_page(page_num):
    url = f"https://zambialii.org/legislation/subsidiary?page={page_num}"
    print(f"\n[discovery] FETCH {url}", flush=True)
    r = do_fetch(url, fetch_n_override=f"discovery-p{page_num}")
    if r["error"] or r["status"] != 200:
        return {"page": page_num, "error": f"status={r['status']} err={r['error']}"}
    body = r["_body_bytes"]
    raw_path = os.path.join(RAW_DISC_DIR, f"subsidiary-page-{page_num:02d}.html")
    with open(raw_path, "wb") as f:
        f.write(body)
    parser = SubsidiaryListingParser()
    parser.feed(body.decode("utf-8", errors="replace"))
    listings = parser.results
    seen = {}
    for y, n, t, h in listings:
        if (y, n) not in seen:
            seen[(y, n)] = (t, h)
    return {
        "page": page_num,
        "raw_path": raw_path,
        "sha256": r["sha256"],
        "bytes": len(body),
        "raw_a_tags": len(listings),
        "unique_yn": len(seen),
        "seen": seen,
    }


def main():
    start = time.time()
    started_iso = utc_now_iso()
    print(f"[{started_iso}] batch_0175 starting in {WORKSPACE}", flush=True)

    # 1. Ingest known corporate candidates
    committed = []
    gapped = []
    for (year, number, title_hint, slug_hint, theme) in CANDIDATES[:MAX_RECORDS]:
        if time.time() - start > WALL_CLOCK_BUDGET_SECS:
            print(f"  Wall-clock budget exhausted before ingest, stopping")
            break
        try:
            record, raw_path, err = process_si(year, number, title_hint, slug_hint)
        except Exception as e:
            import traceback
            traceback.print_exc()
            err = f"exception: {e}"
            record, raw_path = None, None
        if err:
            gapped.append((year, number, slug_hint, err))
            print(f"  GAP: {err}")
        else:
            committed.append((record, raw_path, theme))

    # 2. Discovery sweep (pages 5, 6)
    existing = existing_si_keys()
    discovery_results = []
    all_novel_corporate = []
    all_novel_other = []
    for p in DISCOVERY_PAGES:
        if time.time() - start > WALL_CLOCK_BUDGET_SECS:
            print(f"  Wall-clock budget exhausted before page {p}, stopping")
            break
        try:
            d = discover_page(p)
        except Exception as e:
            import traceback
            traceback.print_exc()
            d = {"page": p, "error": f"exception: {e}"}
        discovery_results.append(d)
        if "seen" in d:
            for (year, num), (title, href) in d["seen"].items():
                if (year, num) in existing:
                    continue
                tl = title.lower()
                matched = [kw for kw in CORPORATE_KEYWORDS if kw in tl]
                entry = {
                    "year": year, "num": num, "title": title,
                    "href": href, "page": p, "matched_keywords": matched,
                }
                if matched:
                    all_novel_corporate.append(entry)
                else:
                    all_novel_other.append(entry)

    # 3. Write state
    state = {
        "batch_num": BATCH_NUM,
        "fetch_count": fetch_count,
        "started_at": started_iso,
        "completed_at": utc_now_iso(),
        "committed": [
            {
                "id": rec["id"],
                "year": int(rec["id"].split("-")[2]),
                "number": int(rec["id"].split("-")[3]),
                "raw_path": rp,
                "record_path": os.path.join(
                    RECORDS_DIR, str(int(rec["id"].split("-")[2])),
                    f"{rec['id']}.json"
                ),
                "sections": len(rec["sections"]),
                "title": rec["title"],
                "theme": theme,
                "source_url": rec["source_url"],
                "source_hash": rec["source_hash"],
            }
            for rec, rp, theme in committed
        ],
        "gapped": [
            {"year": y, "number": n, "slug_hint": sh, "error": e}
            for (y, n, sh, e) in gapped
        ],
        "discovery": [
            {k: v for k, v in d.items() if k != "seen"} for d in discovery_results
        ],
        "novel_corporate_candidates": all_novel_corporate,
        "novel_other_candidates_count": len(all_novel_other),
    }
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)
    print(f"\nState written: {STATE_PATH}")
    print(f"Committed: {len(committed)}  Gapped: {len(gapped)}  Fetches: {fetch_count}")
    print(f"Discovery: {len(discovery_results)} pages; "
          f"{len(all_novel_corporate)} novel corporate / "
          f"{len(all_novel_other)} novel other")


if __name__ == "__main__":
    main()
