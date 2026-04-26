"""Batch 0247 - Phase 4 bulk ingest. PICKS list and shared helpers.

Mirrors batch_0246. Targets:
  - 3 residuals from batch 0246's year=2021 p1 cache (Public Holidays Declarations 2021/69-72) -> sis_governance
  - 1 from year=2020 p1 (Public Finance Management Regs 2020/97) -> sis_governance
  - 3 from alphabet=E (Electoral Process Regs 2016) -> sis_governance (FIRST sis_electoral cluster)
  - 1 from alphabet=N (National Prosecutions Authority Regs 2016) -> sis_judicial
"""
import os, sys, time, hashlib, urllib.request, re

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6  # 5s robots crawl-delay + 1s margin
PARSER_VERSION = "v0.4-zambialii-si-2026-04-26"

PICKS = [
    {"yr_num":"2021/72","year":"2021","num":"72","title":"Public Holidays (Declaration) (No. 3) Notice, 2021","eng_date":"2021-08-20","parent_act":"Public Holidays Act","sub_phase":"sis_governance"},
    {"yr_num":"2021/71","year":"2021","num":"71","title":"Public Holidays (Declaration) (No. 2) Notice, 2021","eng_date":"2021-08-06","parent_act":"Public Holidays Act","sub_phase":"sis_governance"},
    {"yr_num":"2021/69","year":"2021","num":"69","title":"Public Holidays (Declaration) Notice, 2021","eng_date":"2021-07-30","parent_act":"Public Holidays Act","sub_phase":"sis_governance"},
    {"yr_num":"2020/97","year":"2020","num":"97","title":"Public Finance Management (General) Regulations, 2020","eng_date":"","parent_act":"Public Finance Management Act","sub_phase":"sis_governance"},
    {"yr_num":"2016/63","year":"2016","num":"63","title":"Electoral Process (General) Regulations, 2016","eng_date":"","parent_act":"Electoral Process Act","sub_phase":"sis_governance"},
    {"yr_num":"2016/62","year":"2016","num":"62","title":"Electoral Process (Code of Conduct) (Enforcement) Regulations, 2016","eng_date":"","parent_act":"Electoral Process Act","sub_phase":"sis_governance"},
    {"yr_num":"2016/70","year":"2016","num":"70","title":"Electoral Process (Local Government elections) (Election Dates and Times of Poll) Order, 2016","eng_date":"","parent_act":"Electoral Process Act","sub_phase":"sis_governance"},
    {"yr_num":"2016/49","year":"2016","num":"49","title":"National Prosecutions Authority (Witness Allowances and Expenses) Regulations, 2016","eng_date":"","parent_act":"National Prosecutions Authority Act","sub_phase":"sis_judicial"},
]

# Subs in case of failure
SUBS = [
    {"yr_num":"2015/39","year":"2015","num":"39","title":"National Council for Construction (Registration of Projects) Regulations, 2015","eng_date":"","parent_act":"National Council for Construction Act","sub_phase":"sis_industry"},
    {"yr_num":"2009/37","year":"2009","num":"37","title":"National Council for Construction (Forms and Fees) Regulations, 2009","eng_date":"","parent_act":"National Council for Construction Act","sub_phase":"sis_industry"},
    {"yr_num":"2008/16","year":"2008","num":"16","title":"National Road Fund (Charges and Fees) (Apportionment) Regulations, 2008","eng_date":"","parent_act":"National Road Fund Act","sub_phase":"sis_transport"},
    {"yr_num":"2008/24","year":"2008","num":"24","title":"National Constitutional Conference (Committees) Regulations, 2008","eng_date":"","parent_act":"National Constitutional Conference Act","sub_phase":"sis_governance"},
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
