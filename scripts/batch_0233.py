"""Batch 0233 ingest — re-probe alphabet E for residual modern (>=2017) SIs.

Per close-out plan from batch 0232, this tick re-probes E (high-yield
expected per close-out: ~5 novel/alphabet experience). Discovery results:
  E: 85 unique SIs / 74 modern / 64 novel modern after dedup

Picks (8 — MAX_BATCH_SIZE cap, maximally diverse sub-phase mix incl. THREE
priority_order items from approvals.yaml):
    1. 2021/40  Electoral Process (General Election) (Election Date and Time
                of Poll) Order, 2021 (sis_elections — FIRST; 12-Aug-2021 GE)
    2. 2021/57  Electoral Process (Revision of Wards) Order, 2021 (sis_elections)
    3. 2022/18  Electoral Process (General Election) (Election Date and Time
                of Poll) Order, 2022 (sis_elections)
    4. 2023/48  Employment Code (Minimum Wages and Conditions of Employment)
                (General) Order, 2023 (sis_employment — priority_order item 3)
    5. 2023/49  Employment Code (Domestic Workers Minimum Wages and Conditions
                of Employment) Order, 2023 (sis_employment — item 3)
    6. 2023/50  Employment Code (Shop Workers Minimum Wages and Conditions
                of Employment) Order, 2023 (sis_employment — item 3)
    7. 2023/41  Energy Regulation (General) Regulations, 2023 (sis_energy — FIRST)
    8. 2026/4   Electricity (Transmission) (Grid Code) Regulations, 2026
                (sis_energy)

Sub-phase footprint: sis_elections (3 — FIRST) + sis_employment (3 —
priority_order item 3) + sis_energy (2 — FIRST). 2 first-instance sub-phases.

Per-record cost: 2 fetches (HTML+PDF) x 8 = 16 fresh ingest fetches.
Plus 1 robots reverify + 1 alphabet probe (E) = 18 total tick fetches.
"""
import sys, os, json, hashlib, time, urllib.request, re
from datetime import datetime, timezone
from bs4 import BeautifulSoup

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6.0
PARSER_VERSION = "0.5.0"

PICKS = [
    {'yr_num':'2021/40','year':'2021','num':'40',
     'title':'Electoral Process (General Election) (Election Date and Time of Poll) Order, 2021',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':None},
    {'yr_num':'2021/57','year':'2021','num':'57',
     'title':'Electoral Process (Revision of Wards) Order, 2021',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':None},
    {'yr_num':'2022/18','year':'2022','num':'18',
     'title':'Electoral Process (General Election) (Election Date and Time of Poll) Order, 2022',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':None},
    {'yr_num':'2023/48','year':'2023','num':'48',
     'title':'Employment Code (Minimum Wages and Conditions of Employment) (General) Order, 2023',
     'sub_phase':'sis_employment','parent_act':'Employment Code Act',
     'eng_date':None},
    {'yr_num':'2023/49','year':'2023','num':'49',
     'title':'Employment Code (Domestic Workers Minimum Wages and Conditions of Employment) Order, 2023',
     'sub_phase':'sis_employment','parent_act':'Employment Code Act',
     'eng_date':None},
    {'yr_num':'2023/50','year':'2023','num':'50',
     'title':'Employment Code (Shop Workers Minimum Wages and Conditions of Employment) Order, 2023',
     'sub_phase':'sis_employment','parent_act':'Employment Code Act',
     'eng_date':None},
    {'yr_num':'2023/41','year':'2023','num':'41',
     'title':'Energy Regulation (General) Regulations, 2023',
     'sub_phase':'sis_energy','parent_act':'Energy Regulation Act',
     'eng_date':None},
    {'yr_num':'2023/5','year':'2023','num':'5',
     'title':'Energy Regulation (Appeals Tribunal) Rules, 2023',
     'sub_phase':'sis_energy','parent_act':'Energy Regulation Act',
     'eng_date':None},
]

def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+","-",s).strip('-')
    return s[:120]

def fetch(url, sleep=True):
    if sleep: time.sleep(CRAWL)
    req = urllib.request.Request(url, headers=HEADERS)
    return urllib.request.urlopen(req, timeout=45).read()
