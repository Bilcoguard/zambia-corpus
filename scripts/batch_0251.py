"""Batch 0251 - Phase 4 bulk ingest. PICKS list and shared helpers.

Pure cache-drain tick: 8 of 11 reserved alphabet=Z residuals from batch
0250 close-out. Picks span 1980s-2010s and seed several FIRST parent-Act
linkages (ZNPF, ZNS, Tender, ZRA, Zambia Wildlife, Zambia Police, Zambia
Airways). No fresh discovery probes this tick.

Title fields are intentionally hinted from the alphabet=Z listing snippet;
ingest_one re-extracts authoritative title from <h1> / og:title.
parent_act is inferred from naming conventions; ingest_one falls back to
the breadcrumb if the inferred value is incorrect.

Reserved residuals carry to next tick: 3 unpicked from this batch's pool
(1991/35 Tender, 1996/44 ZNPF, 1998/43 Tender) — held for next-tick
drain together with any acts_in_force pivot work.
"""
import os, sys, time, hashlib, urllib.request, re

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6  # 5s robots crawl-delay + 1s margin
PARSER_VERSION = "v0.4-zambialii-si-2026-04-26"

# 8 picks. All from batch 0250 reserved alphabet=Z residuals.
PICKS = [
    {"yr_num":"1980/49","year":"1980","num":"49","title":"","parent_act":"Zambia National Provident Fund Act","sub_phase":"sis_governance"},
    {"yr_num":"1981/47","year":"1981","num":"47","title":"","parent_act":"Zambia National Service Act","sub_phase":"sis_governance"},
    {"yr_num":"1982/49","year":"1982","num":"49","title":"","parent_act":"Zambia Airways Corporation Act","sub_phase":"sis_industry"},
    {"yr_num":"1990/39","year":"1990","num":"39","title":"","parent_act":"Zambia National Provident Fund Act","sub_phase":"sis_governance"},
    {"yr_num":"1994/49","year":"1994","num":"49","title":"","parent_act":"Zambia Revenue Authority Act","sub_phase":"sis_tax"},
    {"yr_num":"2006/10","year":"2006","num":"10","title":"","parent_act":"Zambia Police Act","sub_phase":"sis_governance"},
    {"yr_num":"2016/40","year":"2016","num":"40","title":"","parent_act":"Zambia Wildlife Act","sub_phase":"sis_governance"},
    {"yr_num":"2016/43","year":"2016","num":"43","title":"","parent_act":"Zambia Wildlife Act","sub_phase":"sis_governance"},
]

# Reserved next-tick residuals (informational; not used in this batch)
SUBS = [
    {"yr_num":"1991/35","year":"1991","num":"35","title":"","parent_act":"Tender Board Act","sub_phase":"sis_governance"},
    {"yr_num":"1996/44","year":"1996","num":"44","title":"","parent_act":"Zambia National Provident Fund Act","sub_phase":"sis_governance"},
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
