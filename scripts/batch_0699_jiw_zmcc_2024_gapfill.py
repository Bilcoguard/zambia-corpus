"""batch_0698_jiw_zmcc_2024_gapfill.py — JIW b0698 tick.

ZMCC 2024 gap-fill (priority-a): 8 records (02, 04, 05, 06, 07, 08, 10, 13) from
raw files already on disk at raw/zambialii/judgments/zmcc/2024/. Zero net HTTP
fetches. Hand-curated metadata parsing identical methodology to b0696-jiw.

Per BRIEF: MAX_BATCH_SIZE=8, JIW budget 500/day separate from main worker.
parser_version: 0.3.2-jiw-b0698-hand-curated
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from pathlib import Path

import pdfplumber

REPO = Path("/sessions/keen-pensive-davinci/mnt/corpus")
RAW_DIR = REPO / "raw/zambialii/judgments/zmcc/2024"
PARSER_VERSION = "0.3.2-jiw-b0698-hand-curated"
FETCHED_AT = "2026-05-18T14:05:00Z"

SLUGS = [
    "judgment-zm-2024-zmcc-02-institute-of-law-policy-research-and-human-rights",
    "judgment-zm-2024-zmcc-04-moses-sakala-v-the-attorney-general-and-anor",
    "judgment-zm-2024-zmcc-05-milingo-lungu-v-the-attorney-general-and-anor",
    "judgment-zm-2024-zmcc-06-conservation-advocates-zambia-limited-v-the-attorn",
    "judgment-zm-2024-zmcc-07-sandras-samakayi-v-attorney-general",
    "judgment-zm-2024-zmcc-08-dr-godfrey-hampwaye-and-ors-v-the-council-of-the-u",
    "judgment-zm-2024-zmcc-10-moses-sakala-v-attorney-general-and-ors",
    "judgment-zm-2024-zmcc-13-elijah-simbai-v-the-zambia-institute-of-advanced-l",
]

# Hand-curated overrides for outcomes the regex parser cannot reliably infer
# AND issue_tags lists derived from each judgment's first-page subject matter
# and operative section. Keys: short suffix of slug; values: dict with keys
# `outcome` (optional override), `outcome_detail`, `issue_tags`.
OVERRIDES = {
    "zmcc-02": {
        # Regex matched "application is granted" — joinder application granted.
        "outcome": "granted",
        "outcome_detail": (
            "Interlocutory application for joinder under Order IV rule 2(2) of the "
            "Constitutional Court Rules, 2016. Chisunka JJC sitting alone granted the "
            "Intended Interested Party (Brian Mundubile) leave to join the main "
            "originating-summons proceedings as an interested party. Court issued "
            "directions for filing of skeleton arguments, status conference, and hearing "
            "of the main matter. Each party to bear their own costs."
        ),
        "issue_tags": [
            "joinder of interested party — Order IV rule 2(2) Constitutional Court Rules",
            "Article 74(2) — interpretation (substantive originating summons)",
            "Articles 1(1), 2 and 128 — constitutional jurisdiction",
            "interlocutory application — sufficient interest test",
            "Constitutional Court (Amendment) Act No. 2 of 2016",
        ],
    },
    "zmcc-04": {
        "outcome": "granted",
        "outcome_detail": (
            "Mulife JC (sitting alone) granted the Intended Party (Brian Mundubile) "
            "leave to join Moses Sakala v Attorney General and Anor as 3rd Respondent. "
            "The Court applied the test that no order can be made to the detriment of "
            "an individual unless he is a party to the proceedings (following Mulenga v "
            "Mumbi ex parte Mhango and Stanbic Bank v Micoquip Zambia Ltd). Directions "
            "for filing pleadings issued; parties to bear their respective costs."
        ),
        "issue_tags": [
            "joinder — non-party to be heard before adverse order",
            "Article 60(2)(d) and (e) — political parties and selection of leader of opposition",
            "Article 74(2) — election of Leader of the Opposition in the National Assembly",
            "Rule 43 — Parliamentary Standing Orders, 2021",
            "section 30 Constitutional Court Act and Order XIII rule 1 CCR — costs discretion",
            "Mulenga v Mumbi ex parte Mhango — followed",
            "Stanbic Bank v Micoquip Zambia Ltd — followed",
        ],
    },
    "zmcc-05": {
        "outcome": "set-aside",
        "outcome_detail": (
            "Full bench of the Constitutional Court (Munalula PCC; Shilimi DPCC; "
            "Mulonda, Mulenga, Chisunka, Mwandenga and Mulife JJC) discharged the "
            "single-Judge order that had stayed criminal proceedings against the "
            "Petitioner (Milingo Lungu) in the Subordinate Courts. The Court made no "
            "order for costs. Outcome coded `set-aside` because the operative order "
            "vacated (discharged) the prior single-Judge stay order."
        ),
        "issue_tags": [
            "stay of criminal proceedings — discharge of single-Judge order",
            "review of single-Judge order by full bench of the Constitutional Court",
            "Subordinate Court criminal proceedings — petitioner",
            "constitutional jurisdiction — interlocutory relief",
        ],
    },
    "zmcc-06": {
        # Regex incorrectly fell through to "each-party-bear-own-costs" → other.
        # Manual reading of paragraphs [40]–[41] makes clear the Court found for
        # the petitioner: DNPW's actions held unconstitutional under Articles
        # 255(l)(m), 256(c) and 257(d). Outcome = allowed.
        "outcome": "allowed",
        "outcome_detail": (
            "Constitutional Court (five-Judge panel) found in favour of Conservation "
            "Advocates Zambia Limited. Held at paragraphs [40]–[41] that the Department "
            "of National Parks and Wildlife (DNPW) breached Articles 255(l) and (m) and "
            "257(d) of the Constitution by failing to provide the Petitioner with "
            "environmental information requested in letters dated 2 and 26 June 2023. "
            "The Court held the petition had merit and the Respondent's actions were "
            "unconstitutional. Each party ordered to bear own costs."
        ),
        "issue_tags": [
            "environmental rights — access to environmental information",
            "Article 255(l) and (m) — environment and natural resources principles",
            "Article 256(c) — conservation duty",
            "Article 257(d) — public participation in environmental management",
            "Zambia Wildlife Act No. 14 of 2015 — sections 4(d), 5(2)(q), 7(1), 29",
            "Lower Zambezi, South Luangwa and Kafue National Park tourism block concessions",
            "DNPW — failure to provide environmental information",
            "doctrine of constitutional avoidance — limits in environmental cases",
            "transformative constitutionalism — environmental adjudication",
        ],
    },
    "zmcc-07": {
        "outcome": "other",
        "outcome_detail": (
            "Originating Summons under section 8(1)(a) of the Constitutional Court Act "
            "No. 8 of 2016 for interpretation of Article 145 of the Constitution "
            "(Amendment) Act No. 2 of 2016 (retirement age of judicial officers). "
            "Three-Judge bench (Chisunka, Kawimbe and Mulife JJC) answered the sole "
            "question in the affirmative: a judicial officer who does not opt to retire "
            "at the age of fifty-five years can only retire at the age of sixty-five "
            "years and not at any age in between. Each party to bear their own costs. "
            "Classified `other` because the outcome is a declaratory interpretation, "
            "consistent with b0696 treatment of [2024] ZMCC 22."
        ),
        "issue_tags": [
            "Article 145(3) and (4) — retirement age of judicial officers",
            "literal interpretation of constitutional provisions",
            "Originating Summons — section 8(1)(a) Constitutional Court Act No. 8 of 2016",
            "judicial officer retirement — fifty-five vs sixty-five years",
            "constitutional interpretation — declaratory answer",
        ],
    },
    "zmcc-08": {
        "outcome": "dismissed",
        "outcome_detail": (
            "Three-Judge bench (Sitali, Chisunka and Kawimbe JJC) dismissed the "
            "Respondent's notice of motion seeking summary determination of the "
            "petition under Order 14A of the Rules of the Supreme Court (RSC). The "
            "Court held at paragraph [6.1] that the questions raised were not suitable "
            "for determination under Order 14A without a trial, and remitted the matter "
            "to the single Judge for the continued scheduling of the petition. Each "
            "party to bear their own costs."
        ),
        "issue_tags": [
            "Order 14A RSC — summary determination of points of law",
            "Article 187 — Constitution (UNZA Council and public-service obligations)",
            "Article 189(1) and (2) — administrative justice and fair process",
            "Local Authorities Superannuation Fund Act, Chapter 284 (as amended by Act No. 8 of 2015)",
            "University of Zambia 'First In First Out' policy — pension entitlements",
            "interlocutory motion — remittal to single Judge",
        ],
    },
    "zmcc-10": {
        "outcome": "dismissed",
        "outcome_detail": (
            "Full bench of the Constitutional Court (eleven Judges including Munalula "
            "PCC, Shilimi DPCC, and JJC Sitali, Mulonda, Mulenga, Musaluke, Chisunka, "
            "Mulongoti, Mwandenga, Kawimbe and Mulife) dismissed the petition "
            "challenging the appointment/election of the Leader of the Opposition in "
            "the National Assembly. Held at paragraph [7.21] that the petition has no "
            "merit and is hereby dismissed. Final Order [8.1]: parties to bear their "
            "own costs. Key holdings: (i) election of Leader of Opposition is purely "
            "an internal political-party affair (caucus / party polls / structures); "
            "(ii) the Speaker has no role beyond receiving written notification of the "
            "elected leader under Article 74(2) of the Constitution and Rule 43 of the "
            "National Assembly Standing Orders, 2021; (iii) the Petitioner failed to "
            "prove exclusion of other PF MPs from the selection process."
        ),
        "issue_tags": [
            "Article 74(2) — Leader of the Opposition election by largest opposition party",
            "Rule 43 — National Assembly Standing Orders, 2021",
            "Article 60(2)(d) and (e) — political parties and internal democracy",
            "Speaker's role — receipt of written notification only",
            "intra-party political affairs — judicial non-interference",
            "petition lacks merit — burden of proof on petitioner",
        ],
    },
    "zmcc-13": {
        "outcome": "dismissed",
        "outcome_detail": (
            "Three-Judge bench (Mulenga, Musaluke and Mwandenga JJC) dismissed the "
            "petition at paragraph [4.31] holding that the Petitioner failed to prove "
            "his claims of constitutional breaches against ZIALE Council and "
            "associated respondents. Specific allegations under Articles 119(2) and "
            "122(2) were found to lack merit and were dismissed at paragraphs [4.28]–"
            "[4.29]. Each party to bear own costs."
        ),
        "issue_tags": [
            "Article 119(2) — judicial functions of the courts",
            "Article 122(2) — non-interference with judicial function",
            "ZIALE — Zambia Institute of Advanced Legal Education — professional ethics",
            "judicial review proceedings — High Court parallel litigation",
            "burden of proof — constitutional breach allegations",
            "declaratory relief — failure to entitle Petitioner",
        ],
    },
}


def parse_html_metadata(html_path: Path) -> dict:
    """Return {title, citation, court, case_number, judges_text, date_decided, akn_url}."""
    h = html_path.read_text()
    m_title = re.search(r"<title>\s*(.+?)\s*–\s*ZambiaLII\s*</title>", h, re.S)
    title = m_title.group(1).strip() if m_title else ""

    md = {"title": title}

    block_m = re.search(
        r'<dl class="document-metadata-list[^"]*">(.+?)</dl>', h, re.S
    )
    if block_m:
        block_html = block_m.group(1)
        rows = re.findall(r"<dt[^>]*>(.+?)</dt>\s*<dd[^>]*>(.+?)</dd>", block_html, re.S)
        for label_html, value_html in rows:
            label = re.sub(r"<[^>]+>", "", label_html).strip().rstrip(":").lower()
            # Pull plain text from value, also keep judge anchors separately
            judge_links = re.findall(
                r'href="/judgments/all/\?judges=[^"]*"[^>]*>([^<]+)</a>', value_html
            )
            text = re.sub(r"<[^>]+>", " ", value_html)
            text = re.sub(r"\s+", " ", text).strip()
            if label.startswith("media neutral citation"):
                md["citation"] = text.split()[0:3]
                # Normalize as "[2024] ZMCC N"
                cm = re.match(r"(\[\d{4}\]\s+ZMCC\s+\d+)", text)
                md["citation"] = cm.group(1) if cm else text
            elif label == "court":
                md["court"] = text
            elif label == "case number":
                md["case_number"] = text
            elif label == "judges":
                md["judges_raw"] = judge_links if judge_links else [text]
            elif label == "judgment date":
                # Parse "17 January 2024" → 2024-01-17
                date_m = re.match(r"(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})", text)
                if date_m:
                    months = {
                        "January": "01", "February": "02", "March": "03", "April": "04",
                        "May": "05", "June": "06", "July": "07", "August": "08",
                        "September": "09", "October": "10", "November": "11", "December": "12",
                    }
                    d, mo, y = date_m.groups()
                    md["date_decided"] = f"{y}-{months[mo]}-{int(d):02d}"
                else:
                    md["date_decided"] = text

    # Source PDF URL — Akoma Ntoso publication
    src_pdf_m = re.search(r'href="(/akn/zm/judgment/zmcc/2024/\d+/eng@[^"]+/source\.pdf)"', h)
    if src_pdf_m:
        md["pdf_url"] = "https://zambialii.org" + src_pdf_m.group(1)
    # AKN HTML landing page URL
    akn_m = re.search(r'<link rel="canonical" href="(https://zambialii\.org/akn/[^"]+)"', h)
    if akn_m:
        md["akn_url"] = akn_m.group(1)
    else:
        # derive from pdf_url
        if "pdf_url" in md:
            md["akn_url"] = md["pdf_url"].replace("/source.pdf", "")

    return md


def parse_pdf_body(pdf_path: Path) -> tuple[str, list[str]]:
    """Return (full_body_text, last_four_pages_text_list)."""
    pages_text = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for pg in pdf.pages:
            pages_text.append(pg.extract_text() or "")
    body = "\n".join(pages_text)
    last_n = pages_text[-4:] if len(pages_text) >= 4 else pages_text
    return body, last_n


def operative_section(body: str) -> str:
    """Slice from the last 'CONCLUSION' / 'ORDERS' anchor to EOF for outcome scan."""
    anchors = [
        r"\b(?:5|6|7|8|9|10|11|12|13)\.0\.?\s+(?:CONCLUSION|ORDERS?|CONCLUSIONS?\s+AND\s+ORDERS?|DISPOSITION)\b",
        r"\bCONCLUSIONS?\s+AND\s+ORDERS?\b",
        r"\bORDERS?\s*$",
        r"\bFinal\s+Order\b",
        r"\bDISPOSITION\b",
        r"\bIN\s+CONCLUSION\b",
    ]
    best = -1
    for pat in anchors:
        for m in re.finditer(pat, body, re.IGNORECASE | re.MULTILINE):
            if m.start() > best:
                best = m.start()
    if best > 0:
        return body[best:]
    return body[-6000:]


OUTCOME_PATTERNS = [
    # appeal verbs
    (r"\bappeal\s+is\s+(?:hereby\s+)?allowed\b", "allowed"),
    (r"\bappeal\s+is\s+(?:hereby\s+)?dismissed\b", "dismissed"),
    (r"\bappeal\s+is\s+(?:hereby\s+)?upheld\b", "upheld"),
    (r"\bappeal\s+is\s+(?:hereby\s+)?granted\b", "granted"),
    # application verbs
    (r"\bapplication\s+is\s+(?:hereby\s+)?granted\b", "granted"),
    (r"\bapplication\s+is\s+(?:hereby\s+)?refused\b", "refused"),
    (r"\bapplication\s+is\s+(?:hereby\s+)?dismissed\b", "dismissed"),
    # petition verbs (handles "petition is hereby dismissed" and "petition...
    # has no merit and it is hereby dismissed")
    (r"\bpetition\s+(?:has\s+no\s+merit\s+and\s+)?(?:it\s+)?is\s+(?:hereby\s+)?dismissed\b", "dismissed"),
    (r"\bpetition\s+is\s+(?:hereby\s+)?allowed\b", "allowed"),
    (r"\bpetition\s+is\s+(?:hereby\s+)?granted\b", "granted"),
    (r"\bpetition\s+is\s+(?:hereby\s+)?upheld\b", "upheld"),
    # "notice of motion" patterns
    (r"\b(?:we\s+(?:hereby\s+)?)?dismiss\s+the\s+notice\s+of\s+motion\b", "dismissed"),
    # procedural rulings (joinder, stay etc.)
    (r"\bprayer\s+for\s+(?:an\s+)?order\s+for\s+joinder\s+is\s+granted\b", "granted"),
    (r"\bjoinder\s+is\s+(?:hereby\s+)?granted\b", "granted"),
    (r"\border\s+(?:.{0,80})staying\s+(?:criminal\s+)?proceedings\s+.{0,80}\bis\s+hereby\s+discharged\b", "set-aside"),
    (r"\bis\s+hereby\s+discharged\b", "set-aside"),
    # set-aside / quashed
    (r"\bis\s+hereby\s+set\s+aside\b", "set-aside"),
    (r"\bis\s+hereby\s+quashed\b", "quashed"),
    # generic "we ..." (with optional hereby)
    (r"\bwe\s+(?:hereby\s+)?dismiss\b", "dismissed"),
    (r"\bwe\s+(?:hereby\s+)?allow\b", "allowed"),
    (r"\bwe\s+(?:hereby\s+)?uphold\b", "upheld"),
    (r"\bwe\s+(?:hereby\s+)?grant\b", "granted"),
    (r"\bwe\s+(?:hereby\s+)?refuse\b", "refused"),
    (r"\bwe\s+(?:hereby\s+)?set\s+aside\b", "set-aside"),
    # holding language
    (r"\bwe\s+hold\s+that\s+the\s+petition\s+(?:has\s+no\s+merit|fails)\b", "dismissed"),
    (r"\bclaim\s+fails\b", "dismissed"),
    # other
    (r"\bconviction\s+is\s+(?:hereby\s+)?upheld\b", "upheld"),
    (r"\bcourt\s+refused\b", "refused"),
    (r"\bstruck\s+out\b", "struck-out"),
    (r"\bwithdrawn\b", "withdrawn"),
]


def detect_outcome(last_pages: list[str], full_body: str) -> tuple[str, str]:
    """Return (outcome, evidence_snippet). Returns ('unknown','') if no match.

    Search strategy: (1) operative-section slice of full body, (2) last 4 pages,
    (3) full body as last resort. Apply patterns in order; first match wins.
    """
    op_section = operative_section(full_body)
    last_pages_text = " ".join(last_pages)
    candidates = [
        ("operative_section", op_section),
        ("last_pages", last_pages_text),
        ("full_body_tail", full_body[-12000:]),
    ]
    for source_name, text in candidates:
        text_norm = re.sub(r"\s+", " ", text.lower())
        for pattern, code in OUTCOME_PATTERNS:
            m = re.search(pattern, text_norm)
            if m:
                i = m.start()
                snippet = text_norm[max(0, i - 80) : i + 200]
                return code, f"[{source_name}] {snippet.strip()}"
    # Originating Summons / constitutional interpretation pattern → 'other'
    last_text = re.sub(r"\s+", " ", last_pages_text.lower())
    if re.search(r"originating\s+summons", last_text):
        return "other", "originating-summons (Order IV r 2(2) CCR) — constitutional interpretation"
    if re.search(r"each\s+party\s+(?:to\s+)?bear", last_text) and not re.search(
        r"(?:dismiss|allow|grant|refuse|set\s+aside|quash|uphold)", last_text
    ):
        return "other", "each-party-bear-own-costs only; no operative verb detected — procedural ruling"
    return "unknown", ""


def quality_gate(body: str) -> tuple[bool, str]:
    if len(body) < 200:
        return False, f"body-too-short ({len(body)} chars)"
    digits = sum(c.isdigit() for c in body)
    ratio = digits / max(1, len(body))
    if ratio > 0.5:
        return False, f"digit-ratio-too-high ({ratio:.2%}); likely line-numbers-only scan"
    return True, "ok"


def normalize_judge(raw: str) -> dict:
    """Convert 'Chisunka JJC' or 'Munalula PC' to {name, role}.

    Suffix mapping (ZMCC context):
        CJ = Chief Justice
        DCJ = Deputy Chief Justice
        PCC = President of the Constitutional Court
        DPCC = Deputy President of the Constitutional Court
        JJC = Justice of the Constitutional Court (judge of the Constitutional Court)
        JC = Justice of the Constitutional Court
        JCC = Justice of the Constitutional Court
        PC = President of the (Constitutional) Court (used in some ZMCC records)
        JS = Justice of the Supreme Court (rare in ZMCC)
        JA = Justice of Appeal
    """
    raw = raw.strip()
    role_map = {
        "CJ": "Chief Justice",
        "DCJ": "Deputy Chief Justice",
        "PCC": "President of the Constitutional Court",
        "DPCC": "Deputy President of the Constitutional Court",
        "JJC": "Justice of the Constitutional Court",
        "JCC": "Justice of the Constitutional Court",
        "JC": "Justice of the Constitutional Court",
        "PC": "President of the Constitutional Court",
        "JS": "Justice of the Supreme Court",
        "JA": "Justice of Appeal",
        "J": "Judge",
    }
    # Sort role suffixes by descending length so longer ones match first.
    suffixes = sorted(role_map.keys(), key=len, reverse=True)
    name = raw
    role = "Judge"
    for sfx in suffixes:
        m = re.search(rf"\b{sfx}\b\s*$", raw)
        if m:
            name = raw[: m.start()].strip().rstrip(",")
            role = role_map[sfx] + f" ({sfx})"
            break
    return {"name": raw, "role": role, "dissented": False, "surname": name}


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    print(f"# b0698-jiw — ZMCC 2024 gap-fill — parser {PARSER_VERSION}")
    results = {"records": [], "deferred": []}
    for slug in SLUGS:
        html_path = RAW_DIR / f"{slug}.html"
        pdf_path = RAW_DIR / f"{slug}.pdf"
        if not html_path.exists() or not pdf_path.exists():
            results["deferred"].append({"slug": slug, "reason": "raw-files-missing"})
            print(f"DEFER {slug}: raw files missing")
            continue

        md = parse_html_metadata(html_path)
        body, last_pages = parse_pdf_body(pdf_path)

        qg_ok, qg_reason = quality_gate(body)
        if not qg_ok:
            results["deferred"].append(
                {"slug": slug, "reason": qg_reason, "cohort": "quality-gate-fail"}
            )
            print(f"DEFER {slug}: {qg_reason}")
            continue

        outcome, evidence = detect_outcome(last_pages, body)
        if outcome == "unknown":
            results["deferred"].append(
                {
                    "slug": slug,
                    "reason": "outcome-pattern-not-matched",
                    "cohort": "operative-paragraph-undetected",
                    "tail_excerpt": (last_pages[-1] if last_pages else "")[-400:],
                }
            )
            print(f"DEFER {slug}: outcome unknown")
            continue

        # Build judges list
        judges = []
        for raw_j in md.get("judges_raw", []):
            j = normalize_judge(raw_j)
            judges.append({"name": j["name"], "role": j["role"], "dissented": False})

        # Extract case_name from title — title format:
        #   "Case Name (CASENO) [YYYY] ZMCC N (DD Month YYYY)"
        case_name = md.get("title", slug)
        case_name = re.sub(r"\s*\(.*?\)\s*\[\d{4}\]\s*ZMCC.*$", "", case_name).strip()

        # Apply per-record overrides (hand-curated outcome + issue_tags)
        ov_key = next(
            (k for k in OVERRIDES if k in slug), None
        )
        if ov_key:
            ov = OVERRIDES[ov_key]
            if "outcome" in ov:
                outcome = ov["outcome"]
            outcome_detail = ov.get("outcome_detail", evidence)
            issue_tags = ov.get("issue_tags", [])
        else:
            outcome_detail = (
                f"Outcome inferred from operative paragraph on final pages "
                f"(parser {PARSER_VERSION}). Evidence excerpt: '{evidence[:280]}'"
            )
            issue_tags = []

        record = {
            "id": slug,
            "type": "judgment",
            "jurisdiction": "ZM",
            "title": md.get("title", ""),
            "citation": md.get("citation", ""),
            "court": "Constitutional Court of Zambia",
            "case_name": case_name,
            "case_number": md.get("case_number", ""),
            "date_decided": md.get("date_decided", ""),
            "judges": judges,
            "outcome": outcome,
            "outcome_detail": outcome_detail,
            "source_url": md.get("akn_url", ""),
            "raw_sha256": sha256_of(pdf_path),
            "source_hash": "sha256:" + sha256_of(pdf_path),
            "fetched_at": FETCHED_AT,
            "parser_version": PARSER_VERSION,
            "issue_tags": issue_tags,
            "reasoning_tags": [],
            "key_statutes": [],
            "key_paragraphs": [],
            "paragraph_count_estimate": body.count("\n\n"),
            "body_length": len(body),
            "_pdf_path": str(pdf_path.relative_to(REPO)),
            "_pdf_url": md.get("pdf_url", ""),
            "_body_excerpt_first": body[:800],
            "_body_excerpt_last": body[-800:],
        }
        results["records"].append(record)
        print(f"OK    {slug}: judges={len(judges)} outcome={outcome} body={len(body)}b")

    out_path = REPO / "scripts/_b0698_jiw_parsed.json"
    out_path.write_text(json.dumps(results, indent=2))
    print(f"\nWrote {out_path}")
    print(f"records={len(results['records'])} deferred={len(results['deferred'])}")


if __name__ == "__main__":
    main()
