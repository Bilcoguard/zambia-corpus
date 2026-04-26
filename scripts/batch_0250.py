"""Batch 0250 - Phase 4 bulk ingest. PICKS list and shared helpers.

Mixed tick: 1 reserved residual (1985/14 Equity Levy parent — last 1980s-1990s
alphabet=E item from batch 0247 reserve) + 1 alphabet=U novel (1994/41 UNZA
Staff Tribunal Rules) + 6 alphabet=Z novels (Zambezi River Authority,
ZIALE, ZNBC, ZNS, Zambia Wildlife). Discovery this tick: J/K/U/Z probed
(J=1total/0novel, K=0total/0novel, U=20/1, Z=23/17). Reserved residuals
to next tick: ~10 from alphabet-Z (1980s/1990s ZNPF + ZNS + Tender +
Zambia Wildlife extras + Zambia Police Fees).

Title intentionally hinted but ingest_one extracts authoritative title from
HTML <h1> / og:title. Parent-act inferred from naming convention; ingest_one
re-extracts from breadcrumb if the inferred value is wrong.
"""
import os, sys, time, hashlib, urllib.request, re

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6  # 5s robots crawl-delay + 1s margin
PARSER_VERSION = "v0.4-zambialii-si-2026-04-26"

# 8 picks. 1 reserved residual + 7 from alphabet U/Z probes.
PICKS = [
    {"yr_num":"1985/14","year":"1985","num":"14","title":"","parent_act":"Equity Levy Act","sub_phase":"sis_governance"},
    {"yr_num":"1994/41","year":"1994","num":"41","title":"University of Zambia (Staff Tribunal) Rules, 1994","parent_act":"University of Zambia Act","sub_phase":"sis_governance"},
    {"yr_num":"1995/2","year":"1995","num":"2","title":"Zambezi River Authority (Terms and Conditions of Service) By-laws, 1995","parent_act":"Zambezi River Authority Act","sub_phase":"sis_industry"},
    {"yr_num":"2015/86","year":"2015","num":"86","title":"Zambia Institute of Advanced Legal Education (Accreditation of Legal Education Institutions) Regulations","parent_act":"Zambia Institute of Advanced Legal Education Act","sub_phase":"sis_governance"},
    {"yr_num":"2003/49","year":"2003","num":"49","title":"Zambia National Broadcasting Corporation (Amendment) Act (Commencement) Order, 2003","parent_act":"Zambia National Broadcasting Corporation Act","sub_phase":"sis_governance"},
    {"yr_num":"2013/18","year":"2013","num":"18","title":"Zambia National Service (Combat Uniform) Regulations, 2013","parent_act":"Zambia National Service Act","sub_phase":"sis_governance"},
    {"yr_num":"2016/41","year":"2016","num":"41","title":"Zambia Wildlife (Game Animals) Order, 2016","parent_act":"Zambia Wildlife Act","sub_phase":"sis_governance"},
    {"yr_num":"2016/42","year":"2016","num":"42","title":"Zambia Wildlife (Protected Animals) Order, 2016","parent_act":"Zambia Wildlife Act","sub_phase":"sis_governance"},
]

# Substitute pool (not used in this batch — held for next-tick drain)
SUBS = [
    {"yr_num":"2016/40","year":"2016","num":"40","title":"","parent_act":"","sub_phase":"sis_governance"},
    {"yr_num":"2016/43","year":"2016","num":"43","title":"","parent_act":"","sub_phase":"sis_governance"},
    {"yr_num":"1980/49","year":"1980","num":"49","title":"","parent_act":"","sub_phase":"sis_governance"},
    {"yr_num":"1981/47","year":"1981","num":"47","title":"","parent_act":"","sub_phase":"sis_governance"},
    {"yr_num":"1982/49","year":"1982","num":"49","title":"","parent_act":"","sub_phase":"sis_governance"},
    {"yr_num":"1990/39","year":"1990","num":"39","title":"","parent_act":"","sub_phase":"sis_governance"},
    {"yr_num":"1991/35","year":"1991","num":"35","title":"","parent_act":"","sub_phase":"sis_governance"},
    {"yr_num":"1996/44","year":"1996","num":"44","title":"","parent_act":"","sub_phase":"sis_governance"},
    {"yr_num":"1998/43","year":"1998","num":"43","title":"","parent_act":"","sub_phase":"sis_governance"},
    {"yr_num":"2006/10","year":"2006","num":"10","title":"","parent_act":"","sub_phase":"sis_governance"},
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
