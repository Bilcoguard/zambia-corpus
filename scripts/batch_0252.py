"""Batch 0252 - Phase 4 bulk ingest. PICKS list and shared helpers.

Pure cache-drain tick: 2 of the 3 reserved residuals from batch 0251
close-out. Both picks are Tender Board Act SIs (FIRST sis_governance
parent-Act linkage for Tender Board Act expected). The third reserved
residual (1990/39 ZNPF) remains in the OCR backlog at >4.5MB MAX_PDF_BYTES
cap and is not attempted here.

This is a small, conservative batch (2 records) following BRIEF.md
guidance "do one bounded unit of work" — preferring a clean small
commit over a speculative larger one within the 20-minute wall-clock
cap. No fresh discovery probes this tick (deferring acts_in_force
endpoint discovery to next tick).

Title fields are intentionally hinted from the alphabet=Z listing snippet
(carried over from batch 0250); ingest_one re-extracts authoritative
title from <h1> / og:title. parent_act is inferred from naming
conventions; ingest_one falls back to the breadcrumb if incorrect.

Reserved residuals carry to next tick: 1 (1990/39 ZNPF — OCR backlog,
total backlog now 15 items unchanged).
"""
import os, sys, time, hashlib, urllib.request, re

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6  # 5s robots crawl-delay + 1s margin
PARSER_VERSION = "v0.4-zambialii-si-2026-04-26"

# 2 picks. Both from batch 0251 reserved residuals (Tender Board Act).
PICKS = [
    {"yr_num":"1991/35","year":"1991","num":"35","title":"","parent_act":"Tender Board Act","sub_phase":"sis_governance"},
    {"yr_num":"1998/43","year":"1998","num":"43","title":"","parent_act":"Tender Board Act","sub_phase":"sis_governance"},
]


def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")[:120]


def fetch(url, sleep=True):
    if sleep:
        time.sleep(CRAWL)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()
