#!/usr/bin/env python3
"""
parse_companies_act_2017.py — pilot parser for the Companies Act, 2017.

Pipeline:
  1. pdfplumber text extraction (page-by-page)
  2. respace_pdf_text.respace() applied page-wise
  3. ARRANGEMENT OF SECTIONS skeleton parse (pages 1-12)
        → list of {part, part_title, number, title, page_start}
  4. Cross-reference each section title against its operative page (P_s1+).
  5. Golden section extraction: section 3 ("Interpretation"),
     PDF pages 14 → mid-26.
  6. Emit a v0.2-conformant pilot record JSON.

Parser version: 0.1.1
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pdfplumber

sys.path.insert(0, str(Path(__file__).parent))
from respace_pdf_text import respace, PARSER_VERSION as RESPACE_VERSION  # noqa

PARSER_VERSION = "0.1.1"

PDF_PATH = Path(
    "raw/pilot/parliament-zm/companies-act-2017/companies-act-2017.pdf"
)
RECORD_PATH = Path("records/acts/act-zm-2017-010-companies.json")

# Page boundaries from A-POL-14 structural scan.
P_ARRANGEMENT_START = 1
P_ARRANGEMENT_END = 12
P_BODY_START = 13
P_BODY_END = 196
P_SCHEDULE_START = 197
P_TOTAL = 240

# Header lines that should be stripped before parsing.
HEADER_RE = re.compile(
    r"^\s*(?:"
    r"Companies\s*\[\s*No\.?\s*1?0?\s*of\s*2017\s*\d+"
    r"|\d+\s+No\.?\s*1?0?\s*of\s*2017\s*\]\s*Companies"
    r")\s*$"
)

# Roman-numeral PART line.
PART_RE = re.compile(r"^\s*PART\s+([IVXLCDM]+)\s*$")

# Section start line: "<num>. <title...>"
SECTION_LINE_RE = re.compile(r"^\s*(\d+)\.\s+(.+?)\s*$")


@dataclass
class SectionEntry:
    number: str
    title: str
    part: str
    part_title: str
    body: Optional[str] = None
    page_start: Optional[int] = None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def extract_pages(pdf_path: Path) -> List[str]:
    """Extract raw (un-respaced) text per page (1-indexed list[0] = pdf p1)."""
    pages: List[str] = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text() or "")
    return pages


def strip_headers(lines: List[str]) -> List[str]:
    return [ln for ln in lines if not HEADER_RE.match(ln)]


# ---------------------------------------------------------------------------
# Skeleton parse
# ---------------------------------------------------------------------------


def parse_arrangement(pages_respaced: List[str]) -> List[SectionEntry]:
    """Parse pages 1-12 (ARRANGEMENT OF SECTIONS) into SectionEntry list."""
    text = "\n".join(pages_respaced[P_ARRANGEMENT_START - 1:P_ARRANGEMENT_END])
    lines = [ln for ln in text.split("\n")]
    lines = strip_headers(lines)

    sections: List[SectionEntry] = []
    cur_part = ""
    cur_part_title = ""
    pending_part_title_lines: List[str] = []
    expecting_part_title = False
    cur_section: Optional[SectionEntry] = None

    def flush_section():
        nonlocal cur_section
        if cur_section:
            cur_section.title = re.sub(r"\s+", " ", cur_section.title).strip()
            sections.append(cur_section)
            cur_section = None

    for raw_ln in lines:
        ln = raw_ln.strip()
        if not ln:
            continue
        if ln.upper().replace(" ", "") in (
            "ARRANGEMENTOFSECTIONS",
            "THECOMPANIESACT,2017",
        ):
            continue
        if ln.lower() == "section":
            continue

        m_part = PART_RE.match(ln)
        if m_part:
            flush_section()
            cur_part = m_part.group(1)
            cur_part_title = ""
            expecting_part_title = True
            continue

        if expecting_part_title:
            # The next non-blank line(s) form the Part title — stop when we
            # see a numbered section line.
            if SECTION_LINE_RE.match(ln):
                expecting_part_title = False
                # fall through to section parsing
            else:
                pending_part_title_lines.append(ln)
                # heuristic: a Part title that contains lowercase letters
                # has wrapped. Continue accumulating until next section line
                # or PART line.
                continue

        if pending_part_title_lines:
            cur_part_title = " ".join(pending_part_title_lines).strip()
            pending_part_title_lines = []

        m_sec = SECTION_LINE_RE.match(ln)
        if m_sec:
            flush_section()
            cur_section = SectionEntry(
                number=m_sec.group(1),
                title=m_sec.group(2),
                part=cur_part,
                part_title=cur_part_title,
            )
            continue

        # Stop accumulating once we hit the SCHEDULES marker — that
        # signals the end of the operative-section arrangement.
        if ln.upper().strip() in ("SCHEDULES", "SCHEDULE"):
            flush_section()
            break

        # Continuation of a section title (wrapped to next line)
        if cur_section is not None:
            cur_section.title += " " + ln

    flush_section()
    return sections


# ---------------------------------------------------------------------------
# Cross-reference page_start by scanning operative pages
# ---------------------------------------------------------------------------


def scan_section_starts(
    pages_respaced: List[str], sections: List[SectionEntry]
) -> Tuple[int, int]:
    """Walk forward through concatenated body text, matching each declared
    section number to the next plausible '<n>. <Capital>' occurrence."""
    body_text = ""
    page_offsets: List[Tuple[int, int, int]] = []
    for p in range(P_BODY_START, P_BODY_END + 1):
        start = len(body_text)
        body_text += pages_respaced[p - 1] + "\n"
        page_offsets.append((p, start, len(body_text)))

    def offset_to_page(off: int) -> Optional[int]:
        for (p, s, e) in page_offsets:
            if s <= off < e:
                return p
        return None

    matched = 0
    pos = 0
    for s in sections:
        n = int(s.number)
        pat = re.compile(
            rf"(?<![A-Za-z0-9.,])\b{n}\.\s+(?=[(A-Z])"
        )
        m = pat.search(body_text, pos)
        if m:
            s.page_start = offset_to_page(m.start())
            matched += 1
            pos = m.end()
    return matched, len(sections)


# ---------------------------------------------------------------------------
# Golden section extraction (section 3 — Interpretation)
# ---------------------------------------------------------------------------


def extract_golden_section_3(pages_respaced: List[str]) -> str:
    """Extract section 3 ('Interpretation') body, pages 14-26."""
    chunks: List[str] = []
    for p in range(14, 27):
        chunks.append(pages_respaced[p - 1])
    text = "\n".join(chunks)
    # Strip running headers
    text = "\n".join(strip_headers(text.split("\n")))
    # Find "3." section start and "4." section start
    start_re = re.compile(r"\b3\.\s+In\s+this\s+Act", re.I)
    end_re = re.compile(r"\b4\.\s+In\s+this\s+Act", re.I)
    m_start = start_re.search(text)
    m_end = end_re.search(text)
    if not m_start or not m_end:
        raise RuntimeError(
            f"could not locate s.3/s.4 boundaries (start={m_start}, "
            f"end={m_end})"
        )
    body = text[m_start.start():m_end.start()].rstrip()
    # Drop the marginal-heading word "Interpretation" if it appears alone
    # on a line just before the section start.
    body = re.sub(r"^\s*Interpretation\s*\n", "", body)
    # Drop the marginal-heading "Definition in" / "Definition" that bleeds
    # in from the next section (s.4) at the very tail.
    body = re.sub(r"\n\s*Definition(?:\s+in)?\s*$", "", body)
    # Collapse runs of >2 newlines and trailing whitespace
    body = re.sub(r"\n{3,}", "\n\n", body)
    body = re.sub(r"[ \t]+\n", "\n", body)
    return body.strip()


# ---------------------------------------------------------------------------
# Record builder
# ---------------------------------------------------------------------------


GOLDEN_SECTION_NUMBER = "3"


def build_record(
    sections: List[SectionEntry],
    golden_body: str,
    source_url: str,
    source_hash: str,
    fetched_at: str,
) -> Dict:
    sections_payload = []
    for s in sections:
        body = golden_body if s.number == GOLDEN_SECTION_NUMBER else None
        sections_payload.append(
            {
                "number": s.number,
                "title": s.title,
                "part": s.part,
                "part_title": s.part_title,
                "page_start": s.page_start,
                "body": body,
            }
        )
    notes = (
        "Part of the 2017 reform package enacted alongside Corporate "
        "Insolvency Act, Act No. 9 of 2017 (parliament.gov.zm/node/7268). "
        "Bill ancestor: Companies Bill 2017 (parliament.gov.zm/node/6565). "
        "Landing page: parliament.gov.zm/node/7264. "
        "Commencement SI-deferred: section 1 provides that the Act comes "
        "into operation on a date appointed by the Minister by statutory "
        "instrument. commencement_date left null pending discovery of the "
        "appointing SI. in_force is also null (not true) for the same "
        "reason: until the appointing SI is source-discovered, the Act's "
        "operative status cannot be source-asserted from the four corners "
        "of the as-enacted instrument. Phase 4 will source-assert this. "
        "Repeals Companies Act 1994 (Chapter 388 of the Laws of Zambia). "
        "Bound-volume publication pages 393-634 (Government Printer); "
        "242 publication pages vs 240 PDF pages (2-page discrepancy noted). "
        "Source preserves typographical error 'PRELIMINARY PROVISONS' in "
        "Part I heading (should read 'PRELIMINARY PROVISIONS'). "
        "Pilot record: skeleton parse (all 17 Parts, all section numbers "
        "and titles) plus one golden section (s.3 Interpretation, full "
        "body) as pipeline validation. Remaining section bodies are null, "
        "pending Phase 4 bulk parse. "
        "Parliament does not maintain forward amendment chains. Known "
        "amendments observed via sibling pager pages but not source-asserted "
        "on this Act's landing page: Companies (Amendment) Act 2020 "
        "(No. 12 of 2020) at /node/8635; Companies (Amendment) Act 2025 "
        "(No. 23 of 2025) at /node/12826. amended_by left empty for pilot "
        "— Phase 4 will source-assert these."
    )
    return {
        "id": "act-zm-2017-010-companies",
        "type": "act",
        "jurisdiction": "ZM",
        "title": "The Companies Act, 2017",
        "citation": "Act No. 10 of 2017",
        "version_type": "as_enacted",
        "consolidated_as_of": None,
        "court": None,
        "date_of_assent": "2017-11-17",
        "commencement_date": None,
        "in_force": None,
        "amended_by": [],
        "sections": sections_payload,
        "source_url": source_url,
        "source_hash": "sha256:" + source_hash,
        "fetched_at": fetched_at,
        "parser_version": PARSER_VERSION,
        "notes": notes,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    raw_pages = extract_pages(PDF_PATH)
    respaced_pages = [respace(p) for p in raw_pages]

    sections = parse_arrangement(respaced_pages)
    matched, total = scan_section_starts(respaced_pages, sections)

    golden_body = extract_golden_section_3(respaced_pages)

    # Find provenance from existing provenance.log entry for this PDF.
    fetched_at = "2026-04-09T17:39:10Z"  # set externally
    sha = "5e6acc13c0b47ba52314b8f47d9cf4093de31a2315996480f0926e33ee520fe3"
    url = (
        "https://www.parliament.gov.zm/sites/default/files/documents/"
        "acts/Companies%20Act%2C%202017.pdf"
    )

    record = build_record(sections, golden_body, url, sha, fetched_at)

    RECORD_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(RECORD_PATH, "w") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # Stats
    parts = sorted(set(s.part for s in sections), key=lambda p: (len(p), p))
    by_part: Dict[str, int] = {}
    for s in sections:
        by_part[s.part] = by_part.get(s.part, 0) + 1
    print("== skeleton parse stats ==")
    print(f"  total sections : {len(sections)}")
    print(f"  parts found    : {len(parts)}")
    for p in parts:
        print(f"    PART {p:<6} : {by_part[p]:>3} sections")
    print(f"  cross-ref hits : {matched}/{total}")
    print()
    print("== golden section ==")
    print(f"  s.{GOLDEN_SECTION_NUMBER} body chars: {len(golden_body)}")
    print(f"  first 500 chars:")
    print("  " + "\n  ".join(golden_body[:500].split("\n")))
    print()
    print(f"== record written to {RECORD_PATH} ==")
    return 0


if __name__ == "__main__":
    sys.exit(main())
