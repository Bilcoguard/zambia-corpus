"""Batch 0249 - Phase 4 bulk ingest. PICKS list and shared helpers.

Pure cache-drain tick — drains 8 of 9 reserved residuals from batch 0248
(2004/22 NCC Exemption + 7 of 8 from 1980s-1990s alphabet=E/N era).
Most 1980s-1990s SIs expected to be scanned-image PDFs (pdf_parse_empty
-> OCR backlog growth).

Title is intentionally NULL; ingest_one extracts from <h1> / og:title in
the HTML page (we do not know titles a priori for these residuals — only
year/number from prior alphabet=E/N discovery).

Reserved 1 residual for next tick: whichever year/number is not picked here.
"""
import os, sys, time, hashlib, urllib.request, re

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6  # 5s robots crawl-delay + 1s margin
PARSER_VERSION = "v0.4-zambialii-si-2026-04-26"

# 8 picks chosen from the 9-residual reserve (1985/14 + 1986/32 + 1987/29 +
# 1987/36 + 1988/38 + 1993/37 + 1995/29 + 1995/30 + 2004/22). Keep one of
# the lower-yield 1980s items as residual reserve for next tick: 1985/14.
PICKS = [
    {"yr_num":"2004/22","year":"2004","num":"22","title":"","parent_act":"National Council for Construction Act","sub_phase":"sis_industry"},
    {"yr_num":"1986/32","year":"1986","num":"32","title":"","parent_act":"","sub_phase":"sis_governance"},
    {"yr_num":"1987/29","year":"1987","num":"29","title":"","parent_act":"","sub_phase":"sis_governance"},
    {"yr_num":"1987/36","year":"1987","num":"36","title":"","parent_act":"","sub_phase":"sis_governance"},
    {"yr_num":"1988/38","year":"1988","num":"38","title":"","parent_act":"","sub_phase":"sis_governance"},
    {"yr_num":"1993/37","year":"1993","num":"37","title":"","parent_act":"","sub_phase":"sis_governance"},
    {"yr_num":"1995/29","year":"1995","num":"29","title":"","parent_act":"","sub_phase":"sis_governance"},
    {"yr_num":"1995/30","year":"1995","num":"30","title":"","parent_act":"","sub_phase":"sis_governance"},
]

# Substitute pool if we want extras (not used in this batch — 1985/14 reserved)
SUBS = [
    {"yr_num":"1985/14","year":"1985","num":"14","title":"","parent_act":"","sub_phase":"sis_governance"},
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
