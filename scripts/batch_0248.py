"""Batch 0248 - Phase 4 bulk ingest. PICKS list and shared helpers.

Mirrors batch_0247. Pure cache-drain tick — drains 8 of 17 reserved residuals
from batch 0247 (alphabet=E + alphabet=N, 2005-2016 era favoured for
text-extractability). 9 residuals reserved for next tick (1980s/1990s era +
2004/22).
"""
import os, sys, time, hashlib, urllib.request, re

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6  # 5s robots crawl-delay + 1s margin
PARSER_VERSION = "v0.4-zambialii-si-2026-04-26"

PICKS = [
    {"yr_num":"2016/3","year":"2016","num":"3","title":"Estate Agents (General) Regulations, 2016","eng_date":"2016-01-22","parent_act":"Estate Agents Act","sub_phase":"sis_corporate"},
    {"yr_num":"2015/39","year":"2015","num":"39","title":"National Council for Construction (Registration of Projects) Regulations, 2015","eng_date":"2015-04-30","parent_act":"National Council for Construction Act","sub_phase":"sis_industry"},
    {"yr_num":"2015/89","year":"2015","num":"89","title":"National Museums (Declaration) Order, 2015","eng_date":"2015-08-21","parent_act":"National Museums Act","sub_phase":"sis_governance"},
    {"yr_num":"2016/59","year":"2016","num":"59","title":"National Museums (Entry Fees) Regulations, 2016","eng_date":"2016-07-29","parent_act":"National Museums Act","sub_phase":"sis_governance"},
    {"yr_num":"2009/37","year":"2009","num":"37","title":"National Council for Construction (Forms and Fees) Regulations, 2009","eng_date":"2009-03-13","parent_act":"National Council for Construction Act","sub_phase":"sis_industry"},
    {"yr_num":"2008/24","year":"2008","num":"24","title":"National Constitutional Conference (Committees) Regulations, 2008","eng_date":"2008-02-15","parent_act":"National Constitutional Conference Act","sub_phase":"sis_governance"},
    {"yr_num":"2008/16","year":"2008","num":"16","title":"National Road Fund (Charges and Fees) (Apportionment) Regulations, 2008","eng_date":"2008-02-08","parent_act":"National Road Fund Act","sub_phase":"sis_transport"},
    {"yr_num":"2005/19","year":"2005","num":"19","title":"National Road Fund Act (Commencement) Order, 2005","eng_date":"2005-04-15","parent_act":"National Road Fund Act","sub_phase":"sis_transport"},
]

# Subs reserved if any pick fails — pull from remaining residuals
SUBS = [
    {"yr_num":"2004/22","year":"2004","num":"22","title":"National Council for Construction (Exemption) Regulations, 2004","eng_date":"","parent_act":"National Council for Construction Act","sub_phase":"sis_industry"},
]

def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+","-",s)
    return s.strip("-")[:120]

def fetch(url, sleep=True):
    if sleep: time.sleep(CRAWL)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()
