"""Batch 0231 ingest — drain final 3 U-alphabet residuals + Z-alphabet probe.

Per close-out plan from batch 0230, the 3 remaining U-alphabet residuals
are 2022/60, 2023/9, 2023/45 — all DLPA-style declaration orders under the
Urban and Regional Planning Act 2015 (sis_planning). To fill the batch to
the MAX_BATCH_SIZE=8 cap, this tick also probes alphabet=X (0 SIs), Y (0
SIs), and Z (23 SIs total, 6 modern, 5 novel after dedup against existing
records). The 5 novel Z modern candidates are picked, spanning multiple
parent Acts — diversifying the corpus footprint into FIRST sis_health
records (Zambia Medicines and Medical Supplies Agency Act), FIRST
sis_police records (Zambia Police Act), FIRST sis_water_resources records
(Zambezi River Authority Act), FIRST sis_legal_education records (Zambia
Institute of Advanced Legal Education Act).

Picks (8 — MAX_BATCH_SIZE cap):
    1. 2022/60   URP (DLPA) Regulations, 2022          (sis_planning, drain U)
    2. 2023/9    URP (DLPA) Regulations, 2023          (sis_planning, drain U)
    3. 2023/45   URP (DLPA) (No. 2) Regulations, 2023  (sis_planning, drain U)
    4. 2021/37   ZAMRA (Re-engagement of Staff) Regs   (sis_health,    Z)
    5. 2021/49   ZIALE (Students) Rules, 2021          (sis_legal_education, Z)
    6. 2022/6    Zambia Police (Fees) Regulations, 2022 (sis_police,   Z)
    7. 2022/58   ZRA T&C of Service Amdt By-Laws, 2022 (sis_water_resources, Z)
    8. 2023/14   ZAMRA (Admin of Fund) Regs, 2023      (sis_health,    Z)

Sub-phase footprint: sis_planning (3) + sis_health (2 — first) + sis_police
(1 — first) + sis_water_resources (1 — first) + sis_legal_education (1 —
first). 4 first-instance sub-phases.

Parent Acts: Urban and Regional Planning Act (3); Zambia Medicines and
Medical Supplies Agency Act (2); Zambia Institute of Advanced Legal
Education Act (1); Zambia Police Act (1); Zambezi River Authority Act (1).

Per-record cost: 2 fetches (HTML+PDF) x 8 = 16 fresh ingest fetches.
Plus 1 robots reverify + 3 alphabet probes (X/Y/Z) = 20 total tick fetches.
"""
import sys, os, json, hashlib, time, urllib.request, re
from datetime import datetime, timezone
from bs4 import BeautifulSoup

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6.0
PARSER_VERSION = "0.5.0"

PICKS = [
    {'yr_num':'2022/60','year':'2022','num':'60',
     'title':'Urban and Regional Planning (Designated Local Planning Authorities) Regulations, 2022',
     'sub_phase':'sis_planning','parent_act':'Urban and Regional Planning Act',
     'eng_date':'2022-09-30'},
    {'yr_num':'2023/9','year':'2023','num':'9',
     'title':'Urban and Regional Planning (Designated Local Planning Authority) Regulations, 2023',
     'sub_phase':'sis_planning','parent_act':'Urban and Regional Planning Act',
     'eng_date':'2023-03-17'},
    {'yr_num':'2023/45','year':'2023','num':'45',
     'title':'Urban and Regional Planning (Designated Local Planning Authority) (No. 2) Regulations, 2023',
     'sub_phase':'sis_planning','parent_act':'Urban and Regional Planning Act',
     'eng_date':'2023-10-20'},
    {'yr_num':'2021/37','year':'2021','num':'37',
     'title':'Zambia Medicines and Medical Supplies Agency (Re-engagement of Staff) Regulations, 2021',
     'sub_phase':'sis_health','parent_act':'Zambia Medicines and Medical Supplies Agency Act',
     'eng_date':None},
    {'yr_num':'2021/49','year':'2021','num':'49',
     'title':'Zambia Institute of Advanced Legal Education (Students) Rules, 2021',
     'sub_phase':'sis_legal_education','parent_act':'Zambia Institute of Advanced Legal Education Act',
     'eng_date':None},
    {'yr_num':'2022/6','year':'2022','num':'6',
     'title':'Zambia Police (Fees) Regulations, 2022',
     'sub_phase':'sis_police','parent_act':'Zambia Police Act',
     'eng_date':None},
    {'yr_num':'2022/58','year':'2022','num':'58',
     'title':'Zambezi River Authority (Terms and Conditions of Service) (Amendment) By-Laws, 2022',
     'sub_phase':'sis_water_resources','parent_act':'Zambezi River Authority Act',
     'eng_date':None},
    {'yr_num':'2023/14','year':'2023','num':'14',
     'title':'Zambia Medicines and Medical Supplies Agency (Administration of Fund) Regulations, 2023',
     'sub_phase':'sis_health','parent_act':'Zambia Medicines and Medical Supplies Agency Act',
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
