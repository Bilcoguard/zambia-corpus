#!/usr/bin/env python3
"""Batch 0488 parser — parser_v0.3.2 reparse pass.

This is the FROZEN baseline for parser_version 0.3.2 per Peter's
2026-05-03 instruction (Cowork interactive session). It IMPORTS the
v0.3.1 baseline (`scripts/batch_0360_parse.py`) and EXTENDS it with:

    1. Widened outcome vocabulary (24 explicit phrase patterns the
       user listed, expressed as 11 regex additions covering all of
       them with adverb-tolerant forms).
    2. JJS-title-token / judges-no-comma fix in `parse_judges`. When
       `judges_text` contains no commas BUT contains ≥2 trailing
       judicial-title tokens (PC|DPC|CJ|DCJ|JCC|JJC|JJS|JS|JC|JA|
       JJA|JJ|J), split on the boundary AFTER each title token.
    3. PDF order-intro resolution: when the closing pages contain
       "we order that …" / "it is ordered that …" / "we make the
       following order(s)", look in the ~600-char window after the
       intro for an operative verb (uses the v0.3.2 SUMMARY_PATTERNS
       union with v0.3.1 PDF_TAIL_PATTERNS).

v0.3.1's `_detail_is_safe` filter is reused unchanged so v0.3.2
cannot regress safety on detail extraction.

This file IS the parser_baseline reference for parser_version 0.3.2
per `approvals.yaml.parser_baseline` (post-amendment).

Targets are NOT hard-coded. The script reads a JSON list of
(court, year, num) triples from `_work/b0490/targets.json` (written
by the tick wrapper after scanning gaps.md and records/judgments/
for missing-record candidates with raw on disk).
"""

import hashlib
import json
import os
import pathlib
import re
import sys
from datetime import datetime, timezone

import yaml
from bs4 import BeautifulSoup

# ----------------------------------------------------------------------
# Import v0.3.1 frozen baseline
# ----------------------------------------------------------------------

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import batch_0360_parse as v031  # noqa: E402

PARSER_VERSION = "0.3.2"
RAW_DIR = ROOT / "raw" / "zambialii" / "judgments"
RECORDS_DIR = ROOT / "records" / "judgments"
WORK = ROOT / "_work" / "b0492"
WORK.mkdir(parents=True, exist_ok=True)
JUDGES_REG = ROOT / "judges_registry.yaml"
TARGETS_JSON = WORK / "targets.json"

# Reuse v0.3.1 helpers verbatim
sha_bytes = v031.sha_bytes
slugify = v031.slugify
now_iso = v031.now_iso
_detail_is_safe = v031._detail_is_safe
_extract_detail_around = v031._extract_detail_around
extract_pdf_text = v031.extract_pdf_text
update_judges_registry = v031.update_judges_registry

# ----------------------------------------------------------------------
# v0.3.2 vocabulary additions
# ----------------------------------------------------------------------

# Adverb tolerance, mirrors v0.3.1
_ADV = r"(?:(?:hereby|forthwith|accordingly|entirely|finally|herein)\s+){0,3}"

# 24 explicit phrases from Peter's 2026-05-03 instruction, expressed
# as 11 regex additions covering passive/active/adverb-tolerant forms.
SUMMARY_PATTERNS_V032 = [
    # Refusal as outcome (Peter: "application is refused", "we refuse")
    (re.compile(rf"\b(?:application|petition|appeal|relief|stay|prayer)\s+(?:is\s+)?{_ADV}refused\b", re.I), "dismissed"),
    (re.compile(r"\bwe\s+(?:hereby\s+|therefore\s+|accordingly\s+|now\s+){0,3}refuse\s+(?:to\s+grant\s+)?(?:the\s+\w+\s+){0,3}(?:relief|application|petition|appeal|stay|prayer|leave|order)\b", re.I), "dismissed"),
    # Granting (Peter: "application is granted", "we grant")
    (re.compile(rf"\b(?:application|petition|appeal|leave|relief)\s+(?:is\s+)?{_ADV}granted\b", re.I), "allowed"),
    # Conviction / sentence affirmation (Peter: "conviction is upheld",
    # "sentence is confirmed")
    (re.compile(rf"\bconviction\s+(?:is\s+)?{_ADV}(?:upheld|confirmed|affirmed)\b", re.I), "upheld"),
    (re.compile(rf"\bsentence\s+(?:is\s+)?{_ADV}(?:upheld|confirmed|affirmed)\b", re.I), "upheld"),
    # Case withdrawn (Peter: "case is withdrawn")
    (re.compile(rf"\bcase\s+(?:is\s+)?{_ADV}withdrawn\b", re.I), "withdrawn"),
    # Quashed / set aside ACTIVE only at SUMMARY stage (Peter:
    # "we set aside"). The PASSIVE forms ("judgment is hereby
    # quashed/set aside") are TAIL-ONLY because flynote summaries
    # commonly mention "costs order set aside" or "single ground
    # set aside" as a sub-finding while the case-level disposition
    # is something else (e.g. zmcc/2022/21: appeal dismissed but
    # costs order set aside). Empirically false-positive prone in
    # b0488 — moved to PDF_TAIL_PATTERNS_V032 only.
    (re.compile(r"\bwe\s+(?:hereby\s+|therefore\s+|accordingly\s+|now\s+){0,3}set\s+aside\s+(?:the\s+\w+\s+){0,3}(?:judgment|order|decision|finding|ruling|verdict|sentence|conviction)\b(?!\s+for\s+costs)", re.I), "overturned"),
    # Procedural-refusal / declaratory-academic (Peter: "declaratory
    # relief was academic", "single-judge declined", "court refused stay")
    (re.compile(r"\bdeclaratory\s+relief\s+(?:was|is)\s+academic\b", re.I), "dismissed"),
    (re.compile(r"\bsingle[-\s]judge\s+declined\b", re.I), "dismissed"),
    (re.compile(r"\bcourt\s+refused\s+(?:a\s+)?(?:to\s+grant\s+)?(?:the\s+)?stay\b", re.I), "dismissed"),
    # Discontinuance (Peter: "discontinuance allowed")
    (re.compile(r"\bdiscontinuance\s+(?:is\s+)?(?:hereby\s+)?allowed\b", re.I), "withdrawn"),
    # Dismissed-for-X procedural patterns (Peter: "challenge … dismissed
    # for lack", "application … dismissed for failing")
    (re.compile(r"\b(?:application|petition|appeal|challenge|matter|action)\s+(?:to\s+\w+(?:\s+\w+){0,4}\s+)?(?:was\s+|is\s+)?dismissed\s+for\s+(?:lack|failing|want|failure)\b", re.I), "dismissed"),
    # Matter struck off (Peter: "matter is struck off")
    (re.compile(rf"\bmatter\s+(?:is\s+)?{_ADV}struck\s+off\b", re.I), "struck-out"),
]

# Active-voice operative verbs in the closing pages (Peter: "we dismiss",
# "we allow", "we uphold", "we grant"). Most are already covered by
# v0.3.1 PDF_TAIL_PATTERNS but the v0.3.1 forms wrap the noun in
# `(?:the\s+\w+\s+)?` which fails on "we accordingly dismiss the
# appeal and uphold the declaration" (the optional group consumes
# "the appeal " greedily and then can't match the conjunction). v0.3.2
# adds simpler `we <verb> the <noun>` variants that don't have that
# backtracking pathology, plus broader noun coverage. These are
# critical to ensure the LAST operative line in a multi-issue
# judgment beats a stray "ground X of appeal succeeds" earlier in
# the tail.
PDF_TAIL_PATTERNS_V032 = [
    # Simpler "we <verb> the <noun>" forms — fixes the v0.3.1 backtracking gap
    (re.compile(r"\bwe\s+(?:hereby\s+|therefore\s+|accordingly\s+|now\s+){0,3}dismiss\s+the\s+(?:petition|appeal|application|matter|action|claim|case|cross[-\s]appeal)\b", re.I), "dismissed"),
    (re.compile(r"\bwe\s+(?:hereby\s+|therefore\s+|accordingly\s+|now\s+){0,3}allow\s+the\s+(?:petition|appeal|application|cross[-\s]appeal)\b", re.I), "allowed"),
    (re.compile(r"\bwe\s+(?:hereby\s+|therefore\s+|accordingly\s+|now\s+){0,3}uphold\s+the\s+(?:petition|appeal|application|judgment|decision|finding|conviction|sentence|declaration|ruling)\b", re.I), "upheld"),
    (re.compile(r"\bwe\s+(?:hereby\s+|therefore\s+|accordingly\s+|now\s+){0,3}grant\s+the\s+(?:petition|appeal|application|relief|reliefs|prayer|order|leave)\b", re.I), "allowed"),
    # We refuse the relief / petition / stay / application / prayer
    (re.compile(r"\bwe\s+(?:hereby\s+|therefore\s+|accordingly\s+|now\s+){0,3}refuse\s+(?:to\s+grant\s+)?(?:the\s+\w+\s+){0,3}(?:relief|application|petition|appeal|stay|prayer|leave|order|joinder)\b", re.I), "dismissed"),
    # Hereby quashed / set aside (passive object expansion)
    (re.compile(rf"\b(?:judgment|order|decision|conviction|sentence|finding|ruling|verdict|the\s+\w+)\s+(?:is\s+)?{_ADV}(?:quashed|set\s+aside)\b", re.I), "overturned"),
    # Conviction/sentence/case
    (re.compile(rf"\bconviction\s+(?:is\s+)?{_ADV}(?:upheld|confirmed|affirmed)\b", re.I), "upheld"),
    (re.compile(rf"\bsentence\s+(?:is\s+)?{_ADV}(?:upheld|confirmed|affirmed)\b", re.I), "upheld"),
    (re.compile(rf"\bcase\s+(?:is\s+)?{_ADV}withdrawn\b", re.I), "withdrawn"),
    # Refused / granted at end of clause
    (re.compile(rf"\b(?:application|petition|appeal|relief|stay|prayer|leave)\s+(?:is\s+)?{_ADV}refused\b", re.I), "dismissed"),
    (re.compile(rf"\b(?:application|petition|appeal|relief|leave)\s+(?:is\s+)?{_ADV}granted\b", re.I), "allowed"),
    # Dismissed-for procedural
    (re.compile(r"\b(?:application|petition|appeal|challenge|matter|action)\s+(?:to\s+\w+(?:\s+\w+){0,4}\s+)?(?:was\s+|is\s+)?dismissed\s+for\s+(?:lack|failing|want|failure)\b", re.I), "dismissed"),
    # Discontinuance
    (re.compile(r"\bdiscontinuance\s+(?:is\s+)?(?:hereby\s+)?allowed\b", re.I), "withdrawn"),
    # Matter struck off
    (re.compile(rf"\bmatter\s+(?:is\s+)?{_ADV}struck\s+off\b", re.I), "struck-out"),
]

# Order-intro phrases (Peter: "we order that", "it is ordered that",
# "we make the following order"). When found in the PDF tail, look in
# the ~600 char window after the intro for any v031-or-v032 outcome
# pattern. The intro itself is not an outcome — it INTRODUCES the
# operative verb.
ORDER_INTRO_RE = re.compile(
    r"\b(?:we\s+order\s+that|it\s+is\s+(?:hereby\s+)?ordered\s+that|"
    r"we\s+(?:hereby\s+|therefore\s+|accordingly\s+){0,3}make\s+the\s+following\s+orders?)\b",
    re.I,
)


# ----------------------------------------------------------------------
# v0.3.2 outcome resolution (chains v0.3.2 then v0.3.1)
# ----------------------------------------------------------------------

def find_outcome_in_text_v032(text):
    """Try v0.3.2 SUMMARY_PATTERNS first, then v0.3.1 SUMMARY_PATTERNS."""
    if not text:
        return None, None, None
    for pat, out in SUMMARY_PATTERNS_V032:
        m = pat.search(text)
        if m:
            detail = _extract_detail_around(text, m)
            if _detail_is_safe(detail):
                return out, detail, f"v032:{pat.pattern[:40]}"
    # Fall back to v0.3.1
    return v031.find_outcome_in_text(text)


def find_outcome_in_pdf_tail_v032(pdf_tail_text):
    """v0.3.2 PDF tail resolver. Combines v0.3.2 + v0.3.1 patterns
    into a single pool and returns the LAST safe match by position.
    This is critical to handle multi-issue judgments where a stray
    earlier match (e.g. "Ground 4 of appeal succeeds") would
    otherwise beat the final operative line ("we accordingly
    dismiss the appeal …"). When neither pool matches, falls back
    to ORDER_INTRO + window-scan over v0.3.2/v0.3.1 SUMMARY
    patterns.
    """
    if not pdf_tail_text:
        return None, None, None

    # Stage 1: combined v0.3.2 + v0.3.1 tail patterns, LAST match wins.
    best = None  # (start, out, detail, pat_str, source_tag)
    for pat, out in PDF_TAIL_PATTERNS_V032:
        for m in pat.finditer(pdf_tail_text):
            detail = _extract_detail_around(pdf_tail_text, m)
            if not _detail_is_safe(detail):
                continue
            if best is None or m.start() > best[0]:
                best = (m.start(), out, detail, pat.pattern, "v032-tail")
    for pat, out in v031.PDF_TAIL_PATTERNS:
        for m in pat.finditer(pdf_tail_text):
            detail = _extract_detail_around(pdf_tail_text, m)
            if not _detail_is_safe(detail):
                continue
            if best is None or m.start() > best[0]:
                best = (m.start(), out, detail, pat.pattern, "v031-tail")
    if best is not None:
        return best[1], best[2], f"{best[4]}:{best[3][:40]}"

    # Stage 2: ORDER_INTRO + window-scan over v0.3.2 then v0.3.1
    # SUMMARY patterns. (The intro itself is not an outcome — it
    # introduces the operative verb.)
    last_intro = None
    for m in ORDER_INTRO_RE.finditer(pdf_tail_text):
        last_intro = m
    if last_intro is not None:
        window = pdf_tail_text[last_intro.start():last_intro.start() + 800]
        for pat, out in SUMMARY_PATTERNS_V032:
            m = pat.search(window)
            if m:
                detail = _extract_detail_around(window, m)
                if _detail_is_safe(detail):
                    return out, detail, f"v032-order-intro:{last_intro.group(0)[:30]}"
        for pat, out in v031.SUMMARY_PATTERNS:
            m = pat.search(window)
            if m:
                detail = _extract_detail_around(window, m)
                if _detail_is_safe(detail):
                    return out, detail, f"v032-order-intro+v031:{last_intro.group(0)[:30]}"

    return None, None, None


def infer_outcome_v032(summary_para, pdf_text, pdf_tail_text=None):
    """v0.3.2 chain: SUMMARY (v032→v031) → PDF_ANCHOR (v031) →
    PDF_TAIL (v032→order-intro→v031)."""
    out, detail, src = find_outcome_in_text_v032(summary_para or "")
    if out:
        return out, detail, f"summary[{src or 'v031'}]"
    if pdf_text:
        out, detail, kw = v031.find_outcome_in_pdf(pdf_text)
        if out:
            return out, detail, f"pdf-anchor:{kw}"
    if pdf_tail_text:
        out, detail, src = find_outcome_in_pdf_tail_v032(pdf_tail_text)
        if out:
            return out, detail, f"pdf-tail-2pages[{src}]"
    return None, None, "none"


# ----------------------------------------------------------------------
# v0.3.2 judges parsing — judges-no-comma fix
# ----------------------------------------------------------------------

# The COMPLETE list of judicial title tokens (mirror of v0.3.1's
# parse_one_judge regex). Used both for matching titles and for
# splitting space-separated judge runs.
TITLE_TOKENS = "PC|DPC|CJ|DCJ|JCC|JJC|JJS|JC|JS|JA|JJA|JJ|J"

# "<Surname (mixed-case)> <Title>" — captures one judge in a no-comma
# run. Surname is case-restricted to a leading capital + lowercase
# tail to avoid accidentally matching all-caps section headings.
JUDGE_NO_COMMA_RE = re.compile(
    rf"\b([A-Z][a-z][A-Za-z\-']*(?:\s+[A-Z](?:[a-z][A-Za-z\-']*|\.))*)"
    rf"\s+({TITLE_TOKENS})\b\.?",
)


def parse_judges_v032(judges_text):
    """v0.3.2 parse_judges. If `judges_text` has commas, defer to
    v0.3.1 verbatim. Otherwise, look for the no-comma format
    (e.g. "Sitali JCC Mulenga JCC Mulonda JCC") and split on the
    boundary after each <Surname Title> pair.
    """
    if not judges_text:
        return []

    if "," in judges_text:
        # Old comma-separated path — v0.3.1 baseline handles this fine.
        return v031.parse_judges(judges_text)

    # No-comma path: extract every <Surname Title> pair.
    pairs = JUDGE_NO_COMMA_RE.findall(judges_text)
    if len(pairs) < 2:
        # Single judge or unrecognised format — defer to v0.3.1.
        return v031.parse_judges(judges_text)

    out = []
    for i, (name_blob, title) in enumerate(pairs):
        # name_blob may be multi-token ("Hilda Chibomba"); v0.3.1's
        # last-word-as-surname rule applies for canonical_name. Build
        # an alias string ("Sitali JCC") so the registry update path
        # can preserve the title.
        alias = f"{name_blob.strip()} {title}"
        # Reuse v0.3.1's `parse_one_judge` to keep canonicalisation
        # rules identical for the surname extraction step.
        parsed = v031.parse_one_judge(alias)
        if not parsed:
            continue
        canonical, parsed_title, dissented, _alias = parsed
        if not canonical:
            continue
        role = "presiding" if i == 0 else "concurring"
        out.append({
            "name": canonical,
            "role": role,
            "dissented": dissented,
            "_alias": alias,
            "_title": parsed_title or title,
        })
    return out


# ----------------------------------------------------------------------
# v0.3.2 build_record — wraps v0.3.1 with v0.3.2 outcome+judges
# ----------------------------------------------------------------------

def build_record_v032(court_code, year, num, html_path, pdf_path, html_url, pdf_url):
    """v0.3.2 record builder. Mirrors v0.3.1 structure but uses
    parse_judges_v032 and infer_outcome_v032. Always emits
    parser_version='0.3.2' on success."""
    html_bytes = html_path.read_bytes()
    pdf_bytes = pdf_path.read_bytes()
    soup = BeautifulSoup(html_bytes.decode("utf-8", "ignore"), "html.parser")

    meta = {}
    summary_dd = None
    for dl in soup.find_all("dl"):
        items = dl.find_all(["dt", "dd"])
        for i in range(0, len(items) - 1, 2):
            if items[i].name == "dt" and items[i + 1].name == "dd":
                k = items[i].get_text(" ", strip=True)
                v = items[i + 1].get_text(" ", strip=True)
                if v.endswith(" Copy"):
                    v = v[:-5].strip()
                meta[k] = v
                if k == "Summary":
                    summary_dd = items[i + 1]

    h1 = soup.find("h1")
    title = h1.get_text(" ", strip=True) if h1 else ""
    citation = meta.get("Media Neutral Citation", "") or f"[{year}] ZMCC {num}"
    case_number = meta.get("Case number", "")
    court_full = "Constitutional Court of Zambia"
    judges_text = meta.get("Judges", "")
    judgment_date = meta.get("Judgment date", "")

    date_decided = None
    m = re.match(r"^(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})$", judgment_date)
    if m:
        d, mo, y = m.groups()
        months = "January February March April May June July August September October November December".split()
        try:
            mn = months.index(mo) + 1
            date_decided = f"{y}-{mn:02d}-{int(d):02d}"
        except ValueError:
            pass

    summary_para = ""
    flynote_text = ""
    if summary_dd:
        divs = [d for d in summary_dd.find_all("div", recursive=True) if d.get_text(" ", strip=True)]
        if divs:
            summary_para = divs[0].get_text(" ", strip=True)
        full_text = summary_dd.get_text("\n", strip=True)
        if "Flynote" in full_text:
            tail = full_text.split("Flynote", 1)[1]
            tail = tail.split("Read full summary", 1)[0]
            flynote_text = tail.strip()

    issue_tags = []
    if flynote_text:
        parts = re.split(r"\s+[–—\-]\s+", flynote_text)
        issue_tags = [p.strip() for p in parts if p and len(p.strip()) > 1]

    pdf_text, pdf_tail_text = extract_pdf_text(pdf_path)
    if pdf_text is None and pdf_tail_text is None:
        return None, {"reason": "pdf_extraction_empty_likely_scanned",
                      "summary_head": (summary_para or "")[:300]}
    if pdf_text and len(pdf_text.strip()) < 200:
        return None, {"reason": "pdf_extraction_empty_likely_scanned",
                      "summary_head": (summary_para or "")[:300]}

    outcome, outcome_detail, src = infer_outcome_v032(summary_para, pdf_text, pdf_tail_text)
    if outcome is None:
        return None, {"reason": "html_no_summary_pdf_no_match",
                      "summary_head": (summary_para or "")[:300]}
    if not outcome_detail:
        return None, {"reason": "outcome_inferred_but_detail_unsafe",
                      "src": src,
                      "summary_head": (summary_para or "")[:300]}

    cn = title
    cn = re.sub(r"\s*\([^)]*\)\s*\[[^\]]*\][^()]*\([^)]*\)\s*$", "", cn).strip()
    cn = re.sub(r"\s*\([^)]*\)\s*$", "", cn).strip()
    cn = re.sub(r"\s*\[[^\]]*\]\s*ZMCC.*$", "", cn).strip()

    judges = parse_judges_v032(judges_text)
    if not judges:
        return None, {"reason": "parser_v0.3.2_token_unhandled",
                      "judges_text": judges_text}
    judges_clean = [{k: v for k, v in j.items() if not k.startswith("_")} for j in judges]

    slug = slugify(cn, 50)
    rec_id = f"judgment-zm-{year}-{court_code}-{num:02d}-{slug}"

    record = {
        "id": rec_id,
        "type": "judgment",
        "jurisdiction": "ZM",
        "title": title,
        "citation": citation,
        "court": court_full,
        "case_name": cn,
        "case_number": case_number,
        "date_decided": date_decided,
        "judges": judges_clean,
        "issue_tags": issue_tags or [cn[:80]],
        "outcome": outcome,
        "outcome_detail": outcome_detail,
        "reasoning_tags": [],
        "key_statutes": [],
        "raw_sha256": sha_bytes(pdf_bytes),
        "source_url": html_url,
        "source_hash": "sha256:" + sha_bytes(html_bytes),
        "fetched_at": now_iso(),
        "parser_version": PARSER_VERSION,
    }
    debug = {
        "outcome_source": src,
        "summary_para": summary_para[:500],
        "judges_raw": [j["_alias"] for j in judges],
        "judges_titles": [j["_title"] for j in judges],
    }
    return record, debug


# ----------------------------------------------------------------------
# Main — reads TARGETS_JSON and runs the v0.3.2 reparse
# ----------------------------------------------------------------------

def load_targets():
    if not TARGETS_JSON.exists():
        print(f"FATAL: targets file missing at {TARGETS_JSON}", file=sys.stderr)
        sys.exit(2)
    raw = json.loads(TARGETS_JSON.read_text())
    out = []
    for t in raw:
        out.append((t["court"], int(t["year"]), int(t["num"]), t.get("date_decided")))
    return out


def main():
    targets = load_targets()
    written = []
    deferred = []
    new_aliases = []

    for (court, year, num, dt) in targets:
        out_dir = RECORDS_DIR / court / str(year)
        out_dir.mkdir(parents=True, exist_ok=True)
        existing = list(out_dir.glob(f"judgment-zm-{year}-{court}-{num:02d}-*.json"))
        if existing:
            print(f"SKIP {court} {year}/{num}: already in corpus")
            continue

        raw_year_dir = RAW_DIR / court / str(year)
        html_files = list(raw_year_dir.glob(f"judgment-zm-{year}-{court}-{num:02d}-*.html"))
        pdf_files = list(raw_year_dir.glob(f"judgment-zm-{year}-{court}-{num:02d}-*.pdf"))
        if not html_files or not pdf_files:
            deferred.append({"court": court, "year": year, "num": num,
                             "reason": "raw_bytes_not_on_disk"})
            continue
        html_path = html_files[0]
        pdf_path = pdf_files[0]

        # Reconstruct the canonical URL from the html filename if no dt provided.
        # The fetched HTML is from /eng@YYYY-MM-DD canonical URL.
        if not dt:
            # Recover the expression date from the raw HTML.
            # ZambiaLII pages embed `/akn/zm/judgment/<court>/<year>/<num>/eng@YYYY-MM-DD`
            # in canonical links, breadcrumb links, and the AKN URL. Take the
            # first eng@ date that appears for THIS year/num.
            html_bytes = html_path.read_bytes()
            url_pat = re.compile(
                rf"/akn/zm/judgment/{re.escape(court)}/{year}/{num}/eng@(\d{{4}}-\d{{2}}-\d{{2}})".encode()
            )
            mm = url_pat.search(html_bytes)
            if mm:
                dt = mm.group(1).decode("utf-8", "ignore")
            else:
                # Fallback: any eng@YYYY-MM-DD on the page.
                mm = re.search(rb"eng@(\d{4}-\d{2}-\d{2})", html_bytes)
                if mm:
                    dt = mm.group(1).decode("utf-8", "ignore")
        if not dt:
            deferred.append({"court": court, "year": year, "num": num,
                             "reason": "canonical_url_date_unrecoverable"})
            continue

        html_url = f"https://zambialii.org/akn/zm/judgment/{court}/{year}/{num}/eng@{dt}"
        pdf_url = html_url + "/source.pdf"

        try:
            record, debug = build_record_v032(court, year, num, html_path, pdf_path, html_url, pdf_url)
        except Exception as e:
            deferred.append({"court": court, "year": year, "num": num,
                             "reason": f"parser_exception: {type(e).__name__}: {str(e)[:200]}"})
            continue

        if record is None:
            deferred.append({"court": court, "year": year, "num": num,
                             "reason": debug.get("reason"),
                             "summary": (debug.get("summary_head") or debug.get("summary_para") or "")[:300],
                             "html_url": html_url})
            continue

        for alias, title, j_clean in zip(debug["judges_raw"], debug["judges_titles"], record["judges"]):
            new_aliases.append((j_clean["name"], title, alias, record["id"]))

        out_path = out_dir / f"{record['id']}.json"
        out_path.write_text(json.dumps(record, indent=2, ensure_ascii=False))
        written.append({"id": record["id"],
                        "citation": record["citation"],
                        "outcome": record["outcome"],
                        "outcome_detail": record["outcome_detail"],
                        "outcome_source": debug.get("outcome_source"),
                        "date": record["date_decided"],
                        "case_name": record["case_name"],
                        "judges": [j["name"] for j in record["judges"]],
                        "judges_raw": debug.get("judges_raw"),
                        "html_path": str(html_path),
                        "pdf_path": str(pdf_path),
                        "html_sha": record["source_hash"],
                        "raw_sha": record["raw_sha256"],
                        "html_url": html_url})

    if new_aliases:
        update_judges_registry(new_aliases)

    summary = {
        "parser_version": PARSER_VERSION,
        "parser_baseline": "scripts/batch_0488_parse.py",
        "v031_baseline_imported": "scripts/batch_0360_parse.py",
        "ts_utc": now_iso(),
        "targets_count": len(targets),
        "written": written,
        "deferred": deferred,
        "judges_added": new_aliases,
    }
    (WORK / "parse_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    print(json.dumps({
        "parser_version": PARSER_VERSION,
        "targets_count": len(targets),
        "written_count": len(written),
        "deferred_count": len(deferred),
        "deferred": [(d["court"], d["year"], d["num"], d.get("reason")) for d in deferred],
        "written_ids": [w["id"] for w in written],
    }, indent=2))


if __name__ == "__main__":
    main()
