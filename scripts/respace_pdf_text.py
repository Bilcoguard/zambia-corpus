#!/usr/bin/env python3
"""
respace_pdf_text.py — re-space text extracted from a PageMaker→ScanSoft PDF.

Background
----------
Some Zambian government statutes (e.g. Companies Act 2017) were typeset
in Adobe PageMaker and converted to PDF via ScanSoft PDF Create! 7. The
resulting text layer drops many word boundaries:

    "Shorttitleandcommencement"   → should be "Short title and commencement"
    "InthisAct,unlessthecontext"  → should be "In this Act, unless the context"

This script segments runs of letters using a unigram language model backed
by `wordfreq` plus a small legal vocabulary, then re-emits text with the
original capitalization and punctuation preserved.

Usage:
    python3 respace_pdf_text.py < input.txt > output.txt
    python3 respace_pdf_text.py --self-test

Parser version: 0.1.1
"""

from __future__ import annotations

import re
import sys
from typing import List, Tuple

try:
    from wordfreq import zipf_frequency
except ImportError as e:
    print("Missing dependency: wordfreq. Install with: pip install wordfreq",
          file=sys.stderr)
    raise

PARSER_VERSION = "0.1.1"

# ---------------------------------------------------------------------------
# Vocabulary: pyspellchecker English dictionary (~160k full forms).
# This is preferred over hunspell .dic stems alone because hunspell stores
# stems with affix rules, so common forms like "conversion" or "injunction"
# are missing from a flag-strip-only load.
# ---------------------------------------------------------------------------


def _load_english_vocab() -> set:
    try:
        from spellchecker import SpellChecker  # type: ignore
        sp = SpellChecker()
        return set(sp.word_frequency.dictionary.keys())
    except Exception:
        return set()


ENGLISH_VOCAB = _load_english_vocab()

# Zipf threshold for "known" word.
ZIPF_KNOWN = 2.5

# Penalty for an unknown segment (negative score).
UNKNOWN_PENALTY = -12.0

# Cap on individual segment length to bound DP.
MAX_SEG_LEN = 25

# Domain-specific legal vocabulary that may be sparse in general corpora.
LEGAL_EXTRAS = {
    # Act/parliament
    "act", "acts", "section", "sections", "subsection", "subsections",
    "schedule", "schedules", "part", "parts", "paragraph", "paragraphs",
    "subparagraph", "clause", "clauses", "preamble",
    # Roles
    "minister", "registrar", "agency", "parliament", "president",
    "court", "high", "judge",
    # Concepts
    "commencement", "interpretation", "preliminary", "provisions",
    "provisons",  # source typo preserved
    "statutory", "instrument", "instruments", "regulation", "regulations",
    "prescribed", "prescribe", "prescribes",
    "incorporation", "incorporated", "incorporate", "incorporates",
    "corporate", "corporates",
    "company", "companies", "company's", "companies'",
    "shareholder", "shareholders", "shareholders'",
    "director", "directors", "directors'",
    "secretary", "secretaries",
    "debenture", "debentures", "debentureholder", "debentureholders",
    "subsidiary", "subsidiaries",
    "amalgamation", "amalgamations", "amalgamated", "amalgamating",
    "amalgamate",
    "shares", "share", "stock", "stocks", "stockholder", "stockholders",
    "incorporate", "registered", "register", "registers", "registration",
    "registrations",
    "auditor", "auditors", "audit", "auditing",
    "liability", "liabilities", "shareholder",
    "winding", "wound", "winding-up",
    "deregistration", "deregister", "deregisters", "deregistered",
    "deregistering", "compromise", "incorporator", "incorporators",
    # Geography
    "zambia", "zambian",
    # Abbreviations and small forms
    "plc", "ltd", "cap", "no", "of", "and", "or", "the", "a", "an",
    "in", "on", "by", "to", "as", "is", "be",
    # Date words
    "january", "february", "march", "april", "may", "june", "july",
    "august", "september", "october", "november", "december",
    # Misc legal
    "thereto", "therein", "thereon", "thereof", "therefor", "thereunder",
    "hereto", "herein", "hereon", "hereof", "hereby", "hereunder",
    "whatsoever", "whomsoever", "wheresoever",
    "incorporator", "applicant", "applicants",
    "fluctuating", "perpetual", "fixed", "movable", "immovable",
    "indemnity", "indemnities",
    "promoter", "promoters",
    "proxy", "proxies", "ballot", "ballots",
    "convertible", "redeemable", "preference",
    "alteration", "alterations",
    "filing", "filings", "filed",
    "lodge", "lodged", "lodging",
    "consolidated", "consolidation",
    "non-executive", "executive",
    "twenty-five", "seventy-five", "fifty",
    "members", "membership",
    # ZM-specific
    "kwacha", "ngwee",
    "pacra",
}


# Allowed 1- and 2-letter segments. Anything else short is forbidden.
SHORT_OK = {
    "a", "i",
    "an", "as", "at", "be", "by", "do", "go", "he", "if", "in", "is",
    "it", "me", "my", "no", "of", "on", "or", "so", "to", "up", "us",
    "we", "am", "pm",
    # Ordinal suffixes — appear after digits ("17th") and may end up in
    # letter-only tokens after extraction splits the digit off.
    "st", "nd", "rd", "th",
}


def is_known(word: str) -> bool:
    if not word:
        return False
    if word in LEGAL_EXTRAS:
        return True
    if word in ENGLISH_VOCAB:
        return True
    # Backstop for any words missing from the wordlist; 4.5 is high enough
    # to exclude common scanno bigrams like "ofthe" (3.33).
    if zipf_frequency(word, "en") >= 4.5:
        return True
    return False


def is_valid_segment(seg_lower: str) -> bool:
    if seg_lower in SHORT_OK:
        return True
    if len(seg_lower) < 3:
        return False
    return is_known(seg_lower)


def segment(token: str) -> List[str]:
    """DP segmentation: minimise pieces, tiebreak on max total zipf.

    Returns list of original-case slices, or [token] if no all-known
    segmentation exists.
    """
    n = len(token)
    if n == 0:
        return []
    lower = token.lower()
    INF = (10 ** 9, 0.0)
    best = [INF] * (n + 1)
    parent = [0] * (n + 1)
    best[0] = (0, 0.0)
    for i in range(1, n + 1):
        for j in range(max(0, i - MAX_SEG_LEN), i):
            if best[j] == INF:
                continue
            seg = lower[j:i]
            if not is_valid_segment(seg):
                continue
            z = zipf_frequency(seg, "en")
            if seg in LEGAL_EXTRAS and z < 1.0:
                z = 4.0  # synthetic floor for in-house terms
            cand = (best[j][0] + 1, best[j][1] - z)
            if cand < best[i]:
                best[i] = cand
                parent[i] = j
    if best[n] == INF:
        return [token]
    spans: List[Tuple[int, int]] = []
    i = n
    while i > 0:
        spans.append((parent[i], i))
        i = parent[i]
    spans.reverse()
    return [token[a:b] for (a, b) in spans]


def respace_token(token: str) -> str:
    """Re-space a single letter-only token."""
    if not re.fullmatch(r"[A-Za-z]+", token):
        return token
    lower = token.lower()
    if lower in LEGAL_EXTRAS:
        return token
    if is_known(lower):
        # Already a known word — leave alone.
        return token
    pieces = segment(token)
    if len(pieces) < 2:
        return token
    # Require every piece to be known.
    for p in pieces:
        if not is_known(p.lower()):
            return token
    return " ".join(pieces)


def insert_letter_digit_spaces(text: str) -> str:
    """Insert spaces at letter↔digit boundaries; preserve ordinals like 17th."""
    text = re.sub(r"(\d)([A-Za-z])", r"\1 \2", text)
    text = re.sub(r"([A-Za-z])(\d)", r"\1 \2", text)
    # Re-glue ordinals: "17 th" → "17th"
    text = re.sub(r"\b(\d+)\s+(st|nd|rd|th)\b", r"\1\2", text, flags=re.I)
    return text


def respace_text(text: str) -> str:
    """Re-space arbitrary text. Preserves whitespace and punctuation."""
    parts = re.split(r"([A-Za-z]+)", text)
    out = []
    for p in parts:
        if p and re.fullmatch(r"[A-Za-z]+", p):
            out.append(respace_token(p))
        else:
            out.append(p)
    return "".join(out)


def insert_post_punct_spaces(text: str) -> str:
    """Insert a single space after a comma, semicolon, or colon when the
    next character is a letter or digit and there is not already a space.

    Period (`.`) is intentionally excluded — it is ambiguous between
    sentence terminator, abbreviation marker (Cap.), section enumerator
    (12.1), and decimal point. Section enumerators are handled by the
    body parser, not here.

    Numeric thousands separators are preserved: a comma flanked on both
    sides by digits (e.g. ``1,000``) is left untouched. The same rule
    leaves decimal-style colons (``12:30``, ``Cap:5``) untouched.

    Idempotent: applying the function twice is identical to applying it
    once, because the lookahead requires the next character to be a
    non-space letter/digit.
    """
    # Comma: insert a space before letter, OR before a digit IF the
    # preceding character is not also a digit (i.e. not a thousands
    # separator like "1,000").
    text = re.sub(r",(?=[A-Za-z])", ", ", text)
    text = re.sub(r"(?<!\d),(?=\d)", ", ", text)
    # Semicolon: always insert before letter or digit.
    text = re.sub(r";(?=[A-Za-z0-9])", "; ", text)
    # Colon: insert before a letter; skip when both sides are digits
    # (e.g. "12:30").
    text = re.sub(r":(?=[A-Za-z])", ": ", text)
    text = re.sub(r"(?<!\d):(?=\d)", ": ", text)
    return text


def respace(text: str) -> str:
    """Top-level pipeline: letter-token segmentation + digit boundary fix
    + post-punctuation space insertion."""
    return insert_post_punct_spaces(
        insert_letter_digit_spaces(respace_text(text))
    )


SELF_TESTS = [
    ("Shorttitleandcommencement", "Short title and commencement"),
    ("ApplicationofAct", "Application of Act"),
    ("InthisAct,unlessthecontextotherwiserequires",
     "In this Act, unless the context otherwise requires"),
    ("DateofAssent:17thNovember,2017",
     "Date of Assent: 17th November, 2017"),
    ("PRELIMINARYPROVISONS", "PRELIMINARY PROVISONS"),
    ("Companies[No.10of 2017", "Companies[No.10 of 2017"),
    ("Privatecompanies", "Private companies"),
    ("repealedAct", "repealed Act"),
    ("CompaniesAct,1994", "Companies Act, 1994"),
    ("subsidiariesoftheholdingcompany",
     "subsidiaries of the holding company"),
    ("statutoryinstrument", "statutory instrument"),
    # v0.1.1 — punctuation post-pass tests.
    ("Act,2010", "Act, 2010"),
    ("Act,unless", "Act, unless"),
    ("1,000 kwacha", "1,000 kwacha"),
]


def run_self_test() -> int:
    fails = 0
    for src, expected in SELF_TESTS:
        got = respace(src)
        ok = got == expected
        marker = "ok " if ok else "FAIL"
        print(f"  [{marker}] {src!r} -> {got!r}")
        if not ok:
            print(f"          expected {expected!r}")
            fails += 1
    print(f"\n{len(SELF_TESTS) - fails}/{len(SELF_TESTS)} passed")
    return 0 if fails == 0 else 1


def main() -> int:
    if "--self-test" in sys.argv:
        return run_self_test()
    text = sys.stdin.read()
    sys.stdout.write(respace(text))
    return 0


if __name__ == "__main__":
    sys.exit(main())
