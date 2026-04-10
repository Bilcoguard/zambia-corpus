#!/usr/bin/env python3
"""
B-POL-3 Step 2 — pilot judgment parser for Konkola Copper Mines PLC v
Attorney General + 2 Others, SCZ Appeal No. 09 of 2024.

Reads the cached OCR text from B-POL-2d gate (d) and produces a rich
intermediate parse artefact at parse.json. NOT a generic parser — calibrated
to this single document only. Phase 4 will generalise.

Cleanup discipline (per B-POL-3 directive Step 2):
  - Apply only substitutions in the calibration set or obvious cover-page
    glyph corrections. Log every substitution to cleanup_log.
  - Do NOT introduce content not in the raw OCR.
  - Preserve raw OCR verbatim in body_text_raw.
"""

import json
import re
import os
import datetime
import hashlib
import sys

RAW_PATH = "/tmp/konkola01-full.txt"
P1_PATH = "/tmp/konkola01-p1.txt"
SLUG_DIR = "raw/pilot/judiciary-zm/appeal-no-09-2024-konkola-copper-mins-plc-vs-attorney-general-2-others-mar-2026-coram-musonda-kaoma-and-mutuna-jjs"
PDF_PATH = os.path.join(SLUG_DIR, "Appeal-No-09-2024-Konkola-Copper-Mins-PLC-Vs-Attorney-General-2-Others-Mar-2026-Coram-Musonda-Kaoma-And-Mutuna-JJS.pdf")
OUT_PATH = os.path.join(SLUG_DIR, "parse.json")
PARSER_VERSION = "0.2.0"

# ---------------------------------------------------------------------------
# Read raw OCR
# ---------------------------------------------------------------------------
with open(RAW_PATH, encoding="utf-8") as f:
    raw_text = f.read()
with open(P1_PATH, encoding="utf-8") as f:
    p1_text = f.read()

raw_chars = len(raw_text)
raw_words = len(re.findall(r"\b[\w'-]+\b", raw_text))

# ---------------------------------------------------------------------------
# OCR cleanup — calibration set + obvious cover-page glyph fixes
# ---------------------------------------------------------------------------
cleanup_log = []

def sub_literal(text, pattern, replacement, reason, calibration):
    n = text.count(pattern)
    if n:
        cleanup_log.append({
            "pattern": pattern,
            "replacement": replacement,
            "count": n,
            "reason": reason,
            "calibration_source": calibration,
            "regex": False,
        })
        text = text.replace(pattern, replacement)
    return text

def sub_regex(text, pattern, replacement, reason, calibration):
    matches = re.findall(pattern, text)
    n = len(matches)
    if n:
        cleanup_log.append({
            "pattern": pattern,
            "replacement": replacement,
            "count": n,
            "reason": reason,
            "calibration_source": calibration,
            "regex": True,
        })
        text = re.sub(pattern, replacement, text)
    return text

clean = raw_text

# 1. Cover page glyph corruptions (calibration set from B-POL-2d page-1 excerpt)
clean = sub_literal(clean, "RPEAL NO.", "APPEAL NO.",
    "Leading-A glyph truncation on docket line",
    "B-POL-2d page-1 OCR excerpt")
clean = sub_literal(clean, "AYPELLANT", "APPELLANT",
    "Leading-A truncation + glyph corruption on appellant designation",
    "B-POL-2d page-1 OCR excerpt")
clean = sub_literal(clean, "PL¢ ib", "PLC",
    "PLC glyph corruption to 'PL¢ ib' on cover party block",
    "B-POL-2d page-1 OCR excerpt")
clean = sub_literal(clean, "Ple v", "PLC v",
    "PLC glyph corruption to 'Ple' in case citations (Konkola Copper Mines Ple)",
    "Calibration extension: same KCM party name as cover page")
clean = sub_literal(clean, "KAKOSA METALS LEACH LIMITED", "KAKOSO METALS LEACH LIMITED",
    "Cover page 'KAKOSA' OCR variant; post title spells 'Kakoso'",
    "Post title and B-POL-2d nomenclature analysis")
clean = sub_literal(clean, "Kakosa Tailing Dump", "Kakoso Tailing Dump",
    "Body 'Kakosa' OCR variant of 'Kakoso' tailing dump (third respondent's licensed area)",
    "Post title; consistent with cover-page correction")
clean = sub_literal(clean, "38D RESPONDENT", "3RD RESPONDENT",
    "Glyph '38D' → '3RD' on cover party block",
    "Visual context: ordinal sequence 1ST/2ND/3RD")
clean = sub_literal(clean, "Ist Respondent", "1st Respondent",
    "Glyph 'Ist' → '1st' in counsel block",
    "Visual context: ordinal sequence")
clean = sub_literal(clean, "374 Respondents", "3rd Respondents",
    "Glyph '374' → '3rd' in counsel block",
    "Visual context: '2nd and 3rd Respondents'")

# 2. Hyphenated line-break collapse (lowercase only — preserves real
#    end-of-line hyphens like 'large-\nscale' which should become 'large-scale'
#    NOT 'largescale'. We collapse only when both halves are lowercase letters
#    AND there is a clearly broken word.)
# Conservative form: only collapse when the line break splits letters with no
# trailing space.
def hyphen_collapse(m):
    return m.group(1) + m.group(2)
hyphen_pattern = r"([a-z])-\n([a-z])"
n = len(re.findall(hyphen_pattern, clean))
if n:
    cleanup_log.append({
        "pattern": hyphen_pattern,
        "replacement": "\\1\\2",
        "count": n,
        "reason": "Hyphenated line-break collapse for words split across line wraps",
        "calibration_source": "Universal OCR cleanup; calibration set notes 'large-scale' → keep but 'appel-\\nlant' → 'appellant'",
        "regex": True,
    })
    clean = re.sub(hyphen_pattern, hyphen_collapse, clean)

# Note: substitutions NOT applied (logged for audit but left raw):
not_applied = [
    {"raw": "Patel, i as she then was", "candidate": "Patel, J as she then was",
     "reason": "Likely 'J' (Justice) → 'i' OCR error, but not in calibration set; left raw to honour 'no introduced content' rule"},
    {"raw": "{ike appellant", "candidate": "the appellant",
     "reason": "Likely '{ike' is an OCR garble of 'the', but inferential; left raw"},
    {"raw": "sertaumieation should be in writing", "candidate": "communication should be in writing",
     "reason": "OCR garble; inferential; left raw"},
    {"raw": "appeal sbaiint such decision", "candidate": "appeal against such decision",
     "reason": "OCR garble; inferential; left raw"},
    {"raw": "fora company", "candidate": "for a company",
     "reason": "Common OCR space loss; not in cover-page calibration set; left raw"},
]

clean_chars = len(clean)
clean_words = len(re.findall(r"\b[\w'-]+\b", clean))

# ---------------------------------------------------------------------------
# Structured field extraction
# ---------------------------------------------------------------------------

# Court / jurisdiction / venue
court = "Supreme Court of Zambia"   # verbatim from page 1: "IN THE SUPREME COURT OF ZAMBIA"
court_division = "Civil Jurisdiction"  # verbatim from page 1: "(Civil Jurisdiction)"
holden_at = "Lusaka"                # verbatim from page 1: "HOLDEN AT LUSAKA"
case_number_verbatim_p1 = "APPEAL NO. 09/2024"  # cover page docket (post-cleanup)
case_number_normalised = "Appeal No. 09 of 2024"  # per B-POL-3 ruling 3 (verbatim style)
proceeding_type = "judgment"  # gate (a) confirmed page-1 heading is JUDGMENT

# Parties (structured form for parse.json; flat string lists for record)
parties_struct = {
    "appellants": [
        {"ordinal": 1, "name": "Konkola Copper Mines PLC"}
    ],
    "respondents": [
        {"ordinal": 1, "name": "Attorney General"},
        {"ordinal": 2, "name": "Shenzen Resources Limited"},
        {"ordinal": 3, "name": "Kakoso Metals Leach Limited"},
    ],
}
parties_flat_for_record = {
    "appellant": ["Konkola Copper Mines PLC"],
    "respondent": [
        "Attorney General",
        "Shenzen Resources Limited",
        "Kakoso Metals Leach Limited",
    ],
    "applicant": [],
    "plaintiff": [],
    "defendant": [],
}

# Coram (structured + flat string list for record)
coram_struct = [
    {"name": "Musonda", "title": "DCJ", "honorific": "SC", "long_title": "Deputy Chief Justice"},
    {"name": "Kaoma", "title": "JS", "honorific": None, "long_title": "Supreme Court Judge", "initials": "R. M. C."},
    {"name": "Mutuna", "title": "JS", "honorific": None, "long_title": "Supreme Court Judge"},
]
judges_flat_for_record = ["Musonda DCJ", "Kaoma JS", "Mutuna JS"]
delivered_by = {"name": "Mutuna", "title": "JS",
                "source_quote": "Mutuna, JS delivered the judgment of the Court."}

# Dates from page-1 coram block: "On 4th February, 2026 and 31st March, 2026"
hearing_dates_iso = ["2026-02-04"]   # first sitting (hearing)
delivery_date_iso = "2026-03-31"     # second sitting (delivery), per Zambian SC convention
hearing_dates_source_quote = "On 4th February, 2026 and 31st March, 2026"
hearing_date_interpretation_note = (
    "Two sitting dates listed in the coram block. By Zambian SC convention the "
    "earlier date is the hearing and the later date is delivery. Recorded as "
    "hearing 2026-02-04, delivery 2026-03-31. Closing signature block does not "
    "carry a separate date stamp; delivery date is taken from the coram line."
)

# Counsel block — structured per party (verbatim from page 1, post-cleanup)
counsel = {
    "for_the_appellant": {
        "names": ["Mr. T. Chibeleka", "Ms C. Mukuka",
                  "Mr. G. Chipoya", "Mr. N. Chaleka"],
        "firms": ["Messrs ECB Legal Practitioners (Chibeleka, Mukuka)",
                  "Konkola Copper Mines PLC In-House Counsel (Chipoya, Chaleka)"],
    },
    "for_the_1st_respondent": {
        "names": ["Mr. M. Muchende SC (Solicitor General)",
                  "Mr. P. S. Phiri", "Mr. Mundia Mukelebai", "Ms Mudenda Hamasamo"],
        "firms": ["Attorney General's Chambers"],
    },
    "for_the_2nd_and_3rd_respondents": {
        "names": ["Mr. R. Musumali", "Mrs. S. Phiri-Hinji", "Ms M. V. Chilembo"],
        "firms": [
            "Messrs SLM Legal Practitioners (Musumali)",
            "Messrs Chifumu Banda and Associates (Phiri-Hinji)",
            "Messrs T. S. Chilembo Chambers (Chilembo)",
        ],
    },
}
counsel_source_quote = (
    "For the Appellant: Mr. T. Chibeleka and Ms C. Mukuka of Messrs ECB Legal "
    "Practitioners; Mr. G. Chipoya and Mr. N. Chaleka, In-House Counsel "
    "Konkola Copper Mines PLC. "
    "For the 1st Respondent: Mr. M. Muchende SC - Solicitor General, "
    "Mr. P. S. Phiri, Mr. Mundia Mukelebai and Ms Mudenda Hamasamo of the "
    "Attorney General's Chambers. "
    "For the 2nd and 3rd Respondents: Mr. R. Musumali of Messrs SLM Legal "
    "Practitioners; Mrs. S. Phiri-Hinji of Messrs Chifumu Banda and Associates; "
    "Ms M. V. Chilembo of Messrs T. S. Chilembo Chambers."
)

# ---------------------------------------------------------------------------
# Cases referred to / Legislation referred to (free-text — parse.json only,
# no schema home in v0.4)
# ---------------------------------------------------------------------------
cases_cited = [
    {"index": 1,
     "verbatim": "Konkola Copper Mines PLC v Rephidim Mining and Technical Supplies Limited and Others - CAZ Appeal No. 74 of 2018",
     "court": "Court of Appeal of Zambia",
     "case_number": "CAZ Appeal No. 74 of 2018"},
    {"index": 2,
     "verbatim": "Konkola Copper Mines PLC v Sensele Enterprises Limited - CAZ Appeal No. 133 of 2018",
     "court": "Court of Appeal of Zambia",
     "case_number": "CAZ Appeal No. 133 of 2018"},
    {"index": 3,
     "verbatim": "Chikuta v Chipata Rural Council (1974) ZR 241 (SC)",
     "court": "Supreme Court of Zambia",
     "reporter": "(1974) ZR 241"},
    {"index": 4,
     "verbatim": "New Plast Industries v Commissioner of Lands and Attorney General (2001) ZR 51 (SC)",
     "court": "Supreme Court of Zambia",
     "reporter": "(2001) ZR 51"},
    {"index": 5,
     "verbatim": "Kalymnos Processing Limited & Another v Konkola Copper Mines - CAZ Appeal No. 74 of 2023",
     "court": "Court of Appeal of Zambia",
     "case_number": "CAZ Appeal No. 74 of 2023"},
    {"index": 6,
     "verbatim": "Antonio Ventriglia and Emmanuela Ventriglia v Finsbury Investments Limited - SCZ Appeal No. 2 of 2019",
     "court": "Supreme Court of Zambia",
     "case_number": "SCZ Appeal No. 2 of 2019"},
]

statutes_cited = [
    {"index": 1,
     "verbatim": "The Mines and Minerals Development Act, No. 11 of 2013",
     "title": "Mines and Minerals Development Act",
     "act_number": "No. 11 of 2013",
     "sections_referenced_in_body": ["16", "52(2)", "96", "97", "97(1)", "98"]},
    {"index": 2,
     "verbatim": "Rules of the Supreme Court 1965",
     "title": "Rules of the Supreme Court (white book)",
     "year": 1965,
     "sections_referenced_in_body": ["Order 14A rule 1", "Order 33"]},
    {"index": 3,
     "verbatim": "The Lands and Deeds Registry Act, Chapter 185 of the Laws of Zambia.",
     "title": "Lands and Deeds Registry Act",
     "chapter": "Cap. 185"},
]

# ---------------------------------------------------------------------------
# Paragraphs — judgment body, numbered 1) through 56) per the source
# ---------------------------------------------------------------------------
# Strategy: scan the cleaned text for lines starting with "<num>)" where num
# is 1-56, capture everything from that marker until the next marker (or until
# the signature block). Strip pagination markers (~Jn~) and trailing
# whitespace.

PARA_HEADER_RE = re.compile(r"^\s*(\d{1,2})\)\s*(.*)$", re.MULTILINE)

def extract_paragraphs(text):
    """Extract numbered judgment paragraphs 1) through 56), plus subparagraphs
    of the form 39.1), 39.2), 40.1), etc.
    Returns (paragraphs_struct, paragraph_count).
    """
    # Drop pagination markers like '~ J5 ~' or '~J5~'
    no_pag = re.sub(r"~\s*J\s*\d+\s*~", " ", text)

    # We'll find all paragraph markers (top-level only first: 1) through 56)).
    # Sub-paragraph markers (39.1, 40.1 etc) are kept inline within their
    # parent paragraph's text.
    # Use a regex that requires the marker to start a line (after whitespace).
    marker_re = re.compile(r"(?m)^\s*(\d{1,2})\)\s")
    matches = list(marker_re.finditer(no_pag))

    # Filter out matches whose number is implausible (>56) and de-duplicate
    # consecutive duplicates from page-break re-prints.
    valid = []
    seen_numbers = set()
    last_num = 0
    for m in matches:
        num = int(m.group(1))
        if 1 <= num <= 56 and num >= last_num and num not in seen_numbers:
            valid.append((num, m.start(), m.end()))
            seen_numbers.add(num)
            last_num = num

    paras = []
    for i, (num, start, end) in enumerate(valid):
        next_start = valid[i + 1][1] if i + 1 < len(valid) else len(no_pag)
        body = no_pag[end:next_start].strip()
        # Remove signature block residue if it bled into the last paragraph
        if num == 56:
            body = re.split(r"\n\s*M\.\s*MUSONDA", body)[0].strip()
        # Normalise whitespace within paragraph but preserve line structure
        body = re.sub(r"[ \t]+", " ", body)
        body = re.sub(r"\n[ \t]+", "\n", body)
        body = re.sub(r"\n{3,}", "\n\n", body)
        paras.append({"number": str(num), "text": body})
    return paras

paragraphs = extract_paragraphs(clean)

# Disposition / orders — paragraph 56 (canonical, last paragraph before signature)
disposition_para = next((p for p in paragraphs if p["number"] == "56"), None)
disposition = {
    "paragraph_number": "56",
    "verbatim": disposition_para["text"] if disposition_para else None,
    "summary_of_orders": [
        "Appeal allowed.",
        "Decision of the Court of Appeal set aside.",
        "Matter remitted to the High Court for determination of the dispute.",
        "Costs to the appellant in this Court and in the Court of Appeal, to be taxed in default of agreement.",
    ],
    "source_quote": "We accordingly allow the appeal and set aside the decision of the Court of Appeal. In doing so, we remit the matter back to the High Court for determination of the dispute properly deployed before it. The appellant will have its costs, in this and Court of Appeal, which will be taxed in default of agreement.",
}

# Section headings (judgment body structure — informational)
section_headings = [
    {"number": None, "title": "Introduction", "first_paragraph": "1"},
    {"number": None, "title": "Background", "first_paragraph": "4"},
    {"number": None, "title": "The matter in the High Court", "first_paragraph": "7"},
    {"number": None, "title": "Decision by the Learned High Court Judge", "first_paragraph": "10"},
    {"number": None, "title": "Decision of the Court of Appeal", "first_paragraph": None},
    {"number": None, "title": "Appeal to this Court and arguments by parties", "first_paragraph": None},
    {"number": None, "title": "Consideration and decision of the Court", "first_paragraph": "42"},
    {"number": None, "title": "Conclusion", "first_paragraph": "56"},
]

# ---------------------------------------------------------------------------
# Source / provenance metadata (from B-POL-2d Step 3 GET)
# ---------------------------------------------------------------------------
with open(PDF_PATH, "rb") as f:
    pdf_bytes = f.read()
pdf_sha256 = hashlib.sha256(pdf_bytes).hexdigest()
assert pdf_sha256 == "2f790701cc6c882bd58881ad3e1b760a407d34a35b0231e2f70c45f81ceaa0ee", \
    f"PDF sha256 drift! got {pdf_sha256}"

source_metadata = {
    "url": "https://judiciaryzambia.com/wp-content/uploads/2026/03/Appeal-No-09-2024-Konkola-Copper-Mins-PLC-Vs-Attorney-General-2-Others-Mar-2026-Coram-Musonda-Kaoma-And-Mutuna-JJS.pdf",
    "publisher": "judiciaryzambia.com",
    "sha256": pdf_sha256,
    "content_length": len(pdf_bytes),
    "pdf_pages": 33,
    "last_modified": "Tue, 31 Mar 2026 13:38:18 GMT",
    "etag": '"69cbce4a-f5fa2b"',
    "fetched_at": "2026-04-10T00:23:55Z",
    "fetcher_version": "0.2.0",
    "retrieved_under_policy": "B-POL-2c (revised content-length envelope, 500 KB-50 MB for judiciaryzambia.com Supreme Court PDFs); fetch authorised under B-POL-2d fallback to candidate #01",
    "post_html_path": "raw/discovery/judiciary-zm/supreme-court/posts/post-01-konkola-appeal-09-2024.html",
    "post_html_sha256": "2b27bc3c10d195093ec3c1d2df8ed726b826248c87815924aafea15cac8623ef",
}

ocr_metadata = {
    "ocr_engine": "tesseract 4.1.1",
    "ocr_engine_wrapper": "pytesseract 0.3.13",
    "pdf_renderer": "pdftoppm 22.02.0 (poppler) via pdf2image",
    "ocr_render_dpi_page1": 300,
    "ocr_render_dpi_body": 200,
    "ocr_languages": ["eng"],
    "ocr_word_count_raw": raw_words,
    "ocr_char_count_raw": raw_chars,
    "ocr_word_count_clean": clean_words,
    "ocr_char_count_clean": clean_chars,
    "ocr_pages_processed": 33,
    "ocr_run_provenance": "B-POL-2d gate (d) full-document OCR; cached at /tmp/konkola01-full.txt and re-loaded for parse",
    "text_layer_present_in_source_pdf": False,
}

# ---------------------------------------------------------------------------
# Sensitive-data category scan (informational — final value ratified by human)
# ---------------------------------------------------------------------------
def scan_for(text, terms):
    found = []
    for t in terms:
        for m in re.finditer(t, text, re.IGNORECASE):
            ctx_start = max(0, m.start() - 60)
            ctx_end = min(len(text), m.end() + 60)
            found.append({"term": t, "context": text[ctx_start:ctx_end].strip()})
    return found

sensitive_scan = {
    "health":             scan_for(clean, [r"\bmedical\b", r"\bhealth\b", r"\bdiagnos", r"\billness\b", r"\bpatient\b", r"\bphysician\b", r"\bhospital\b", r"\binjury\b", r"\bdisability\b"]),
    "criminal":           scan_for(clean, [r"\bconvict", r"\bcriminal\b", r"\bsentence\b", r"\bprosecution\b", r"\boffence\b", r"\barrest\b", r"\bguilty\b"]),
    "political":          scan_for(clean, [r"\bpolitical (?:opinion|affiliation|party)", r"\btrade union\b"]),
    "religious":          scan_for(clean, [r"\breligio", r"\bfaith\b", r"\bchurch\b", r"\bworship\b"]),
    "ethnic":             scan_for(clean, [r"\bethnic\b", r"\brace\b", r"\btribe\b", r"\bnationality\b"]),
    "biometric":          scan_for(clean, [r"\bbiometric\b", r"\bfingerprint\b", r"\bdna\b", r"\bfacial recogn"]),
    "genetic":            scan_for(clean, [r"\bgenetic\b", r"\bDNA\b", r"\bhereditary\b"]),
    "sexual":             scan_for(clean, [r"\bsexual\b", r"\bsex life\b", r"\borientation\b"]),
    "financial_distress": scan_for(clean, [r"\binsolven", r"\bbankrupt", r"\bfinancial distress\b", r"\bdebts? owed\b"]),
    "family_status":      scan_for(clean, [r"\bmarried\b", r"\bdivorce", r"\bspouse\b", r"\bchildren\b", r"\bcustody\b"]),
}

sensitive_scan_summary = {
    cat: ("no matches" if not hits else f"{len(hits)} match(es)")
    for cat, hits in sensitive_scan.items()
}

# Worker recommendation (NOT a final value — human ratifies in Step 4):
sensitive_categories_recommendation = ["none"]
sensitive_categories_rationale = (
    "Commercial mining-rights dispute between a corporate appellant (Konkola "
    "Copper Mines PLC) and the state plus two corporate respondents (Shenzen "
    "Resources Limited, Kakoso Metals Leach Limited). No natural persons appear "
    "as parties. The judgment turns on statutory interpretation of sections 16, "
    "52(2), 96 and 97 of the Mines and Minerals Development Act, 2013. No "
    "health, criminal, political-affiliation, religious, ethnic, biometric, "
    "genetic, sexual-life, family-status, or personal financial-distress data "
    "is disclosed on the face of the judgment. Worker recommends [\"none\"]; "
    "human operator ratifies."
)

# ---------------------------------------------------------------------------
# Title and citation (per B-POL-3 rulings)
# ---------------------------------------------------------------------------
title_for_record = "Konkola Copper Mines PLC v Attorney General, Shenzen Resources Limited and Kakoso Metals Leach Limited"
citation_for_record = "Appeal No. 09 of 2024"
id_for_record = "judgment-zm-2026-scz-09-konkola-v-ag"

# ---------------------------------------------------------------------------
# Ambiguities flagged for human review
# ---------------------------------------------------------------------------
ambiguities = [
    {
        "field": "title",
        "issue": "How to render the case title for the schema 'title' field — full party list vs short form 'Konkola Copper Mines PLC v Attorney General & Others'",
        "worker_proposal": "Konkola Copper Mines PLC v Attorney General, Shenzen Resources Limited and Kakoso Metals Leach Limited (full)",
    },
    {
        "field": "hearing_dates vs delivery_date",
        "issue": "The coram block lists two sitting dates (4 Feb 2026 and 31 Mar 2026). No separate date stamp on the signature block. Convention is that the second date is delivery; the first is hearing.",
        "worker_proposal": "hearing 2026-02-04, delivery 2026-03-31. delivery_date populates schema field date_of_assent (per schema field description repurposing for non-Acts).",
    },
    {
        "field": "Musonda DCJ honorific 'SC'",
        "issue": "Signature block reads 'M. MUSONDA, SC / DEPUTY CHIEF JUSTICE'. 'SC' here is State Counsel (a Zambian designation), not Senior Counsel. Worth recording but no schema slot.",
        "worker_proposal": "Carry in parse.json coram_struct only; flatten to 'Musonda DCJ' for schema judges array.",
    },
    {
        "field": "cited_authorities (corpus IDs)",
        "issue": "Schema cited_authorities requires corpus IDs that resolve. Corpus has only the Companies Act, which is not cited. So cited_authorities = []. Free-text case and statute lists live in parse.json only.",
        "worker_proposal": "Final record cited_authorities = []. Parse.json carries cases_cited and statutes_cited as audit trail.",
    },
    {
        "field": "rights_notice",
        "issue": "Per B-POL-3 directive Step 3, populate with the proposed text from the directive (Cap. 406 fair-dealing). The publisher source page itself carries no copyright notice (J-POL-3b finding). Schema permits null where no notice is present.",
        "worker_proposal": "Populate with proposed text from directive. Alternative: leave null because publisher asserts no notice. Awaiting human ruling at Step 3 (record build).",
    },
    {
        "field": "OCR garble not in calibration set",
        "issue": "Several inferential corrections were NOT applied to body_text_clean (Patel J vs Patel i; '{ike' vs 'the'; 'sertaumieation' vs 'communication'; 'sbaiint' vs 'against'). These are listed in cleanup_log_not_applied for audit. Re-OCR at higher DPI or human transcription would likely resolve them.",
        "worker_proposal": "Leave raw in body_text_clean. Phase 4 may apply a higher-DPI re-OCR pass.",
    },
]

# ---------------------------------------------------------------------------
# Assemble parse.json
# ---------------------------------------------------------------------------
parse_doc = {
    "$schema_note": "This is the rich intermediate parse artefact for B-POL-3 Step 2. It is NOT validated against record.schema.json — that is the job of the cherry-picked record built in Step 3. parse.json is the unabridged audit trail of what the parser saw.",
    "parser": {
        "name": "scripts/parse_konkola_pilot.py",
        "version": PARSER_VERSION,
        "calibration": "single-document, calibrated to Konkola SCZ Appeal No. 09 of 2024 only",
        "run_at_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    },
    "proposed_record_identity": {
        "id": id_for_record,
        "title": title_for_record,
        "citation": citation_for_record,
        "type": "judgment",
        "jurisdiction_country": "ZM",
    },
    "court": court,
    "court_division": court_division,
    "holden_at": holden_at,
    "case_number_verbatim_p1": case_number_verbatim_p1,
    "case_number_normalised": case_number_normalised,
    "proceeding_type": proceeding_type,
    "parties_struct": parties_struct,
    "parties_flat_for_record": parties_flat_for_record,
    "coram_struct": coram_struct,
    "judges_flat_for_record": judges_flat_for_record,
    "delivered_by": delivered_by,
    "hearing_dates_iso": hearing_dates_iso,
    "delivery_date_iso": delivery_date_iso,
    "hearing_dates_source_quote": hearing_dates_source_quote,
    "hearing_date_interpretation_note": hearing_date_interpretation_note,
    "counsel": counsel,
    "counsel_source_quote": counsel_source_quote,
    "section_headings": section_headings,
    "paragraphs_count": len(paragraphs),
    "paragraphs": paragraphs,
    "disposition": disposition,
    "cases_cited_freetext": cases_cited,
    "statutes_cited_freetext": statutes_cited,
    "sensitive_data_scan": {
        "summary": sensitive_scan_summary,
        "details": sensitive_scan,
        "worker_recommendation": sensitive_categories_recommendation,
        "worker_rationale": sensitive_categories_rationale,
    },
    "source_metadata": source_metadata,
    "ocr_metadata": ocr_metadata,
    "cleanup_log_applied": cleanup_log,
    "cleanup_log_not_applied": not_applied,
    "ambiguities_flagged_for_human": ambiguities,
    "body_text_raw_chars": raw_chars,
    "body_text_clean_chars": clean_chars,
    "body_text_raw": raw_text,
    "body_text_clean": clean,
}

with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(parse_doc, f, ensure_ascii=False, indent=2)

print(f"wrote: {OUT_PATH}")
print(f"size:  {os.path.getsize(OUT_PATH)} bytes")
print(f"paragraphs extracted: {len(paragraphs)}")
print(f"cleanup substitutions applied: {len(cleanup_log)}")
print(f"ambiguities flagged: {len(ambiguities)}")
