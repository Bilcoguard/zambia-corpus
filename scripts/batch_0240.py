"""Phase 4 batch 0240 - sis_energy first cluster + sis_elections E-residual drain (cohort 6 from batch_0233 E-probe).

Picks: drains the remaining 15-record E-probe cache (batch_0233) in priority order,
selecting 8 + 1 in-batch substitute. Cohort biased toward FIRST sis_energy cluster
(Electricity Act SIs - first-time sub-phase) plus the next batch of sis_elections
LG By-Election orders.

Skipped from cache (known scanned-image failures, deferred to OCR backlog):
  - 2018/075 National Assembly By-Election (Mangango)  (failed batch 0238)
  - 2018/093 National Assembly By-Election (Sesheke)   (failed batch 0239)
  - 2022/008 National Assembly By-Election (Kabwata)   (failed batch 0235)

    1. 2026/002  Electricity (Wayleave and Clearances) Regulations, 2026  [FIRST sis_energy]
    2. 2026/004  Electricity (Transmission) (Grid Code) Regulations, 2026
    3. 2021/024  Electricity (Common Carrier) (Declaration) Regulations, 2021
    4. 2021/094  Electricity (Common Carrier) (Declaration) (Revocation) Order, 2021
    5. 2023/036  Electoral Process (LG By-Elections) Order, 2023
    6. 2023/040  Electoral Process (LG By-Elections) (No. 2) Order, 2023
    7. 2023/046  Electoral Process (LG By-Elections) (No. 3) Order, 2023
    8. 2024/002  Electoral Process (LG By Elections) Order, 2024

In-batch substitute slot (idx 8): 2024/006 Electoral Process (LG By-Elections) Order, 2024.

Sub-phases: FIRST sis_energy cluster (4 records) + sis_elections drain (4 records).
After this tick: ~7 left in batch-0233 E-probe cache (15 - 8 if all ok).
"""
import sys, os, json, hashlib, time, urllib.request, re
from datetime import datetime, timezone
from bs4 import BeautifulSoup

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6.0
PARSER_VERSION = "0.5.0"

PICKS = [
    {'yr_num':'2026/2','year':'2026','num':'2',
     'title':'Electricity (Wayleave and Clearances) Regulations, 2026',
     'sub_phase':'sis_energy','parent_act':'Electricity Act',
     'eng_date':'2026-01-02'},
    {'yr_num':'2026/4','year':'2026','num':'4',
     'title':'Electricity (Transmission) (Grid Code) Regulations, 2026',
     'sub_phase':'sis_energy','parent_act':'Electricity Act',
     'eng_date':'2026-01-09'},
    {'yr_num':'2021/24','year':'2021','num':'24',
     'title':'Electricity (Common Carrier) (Declaration) Regulations, 2021',
     'sub_phase':'sis_energy','parent_act':'Electricity Act',
     'eng_date':'2021-04-09'},
    {'yr_num':'2021/94','year':'2021','num':'94',
     'title':'Electricity (Common Carrier) (Declaration) (Revocation) Order, 2021',
     'sub_phase':'sis_energy','parent_act':'Electricity Act',
     'eng_date':'2021-12-31'},
    {'yr_num':'2023/36','year':'2023','num':'36',
     'title':'Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) Order, 2023',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2023-08-25'},
    {'yr_num':'2023/40','year':'2023','num':'40',
     'title':'Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) (No. 2) Order, 2023',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2023-09-08'},
    {'yr_num':'2023/46','year':'2023','num':'46',
     'title':'Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) (No. 3) Order, 2023',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2023-11-03'},
    {'yr_num':'2024/2','year':'2024','num':'2',
     'title':'Electoral Process (Local Government By Elections) (Election Date and Time of Poll) Order, 2024',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2024-01-05'},
    # idx 8 = in-batch substitute for any pdf_parse_empty
    {'yr_num':'2024/6','year':'2024','num':'6',
     'title':'Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) Order, 2024',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2024-01-12'},
]

def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+","-",s).strip('-')
    return s[:120]

def fetch(url, sleep=True):
    if sleep: time.sleep(CRAWL)
    req = urllib.request.Request(url, headers=HEADERS)
    return urllib.request.urlopen(req, timeout=45).read()
