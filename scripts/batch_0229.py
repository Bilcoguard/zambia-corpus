"""Batch 0229 ingest — fresh U-alphabet probe (per close-out plan from batch 0228).

Surfaced 19 novel modern (>=2017) candidates, all sis_planning under the
Urban and Regional Planning Act (Act No. 3 of 2015).

Picks (8 — MAX_BATCH_SIZE cap):
  Mix of substantive Regulations + DLPA short orders across years 2017-2025.

    1. 2017/60  Urban and Regional Planning (Designated Local Planning
                Authorities) Regulations, 2017  [DLPA, earliest]
    2. 2018/43  Urban and Regional Planning (Designated Local Planning
                Authorities) Regulations, 2018  [DLPA]
    3. 2019/42  Urban and Regional Planning (Designated Local Planning
                Authorities) Regulations, 2019  [DLPA]
    4. 2020/5   Urban and Regional Planning (Designated Local Planning
                Authority) Regulations, 2020  [DLPA]
    5. 2020/56  Urban and Regional Planning (General) Regulations, 2020
                [substantive — General Regulations under URP Act]
    6. 2022/57  Urban and Regional Planning (Designated Local Planning
                Authorities) Regulations, 2022  [DLPA]
    7. 2023/21  Urban and Regional Planning (Development Plans Guidelines
                and Exempted Development Classes) Regulations, 2023
                [substantive]
    8. 2025/65  Urban and Regional Planning (Administration of Planning
                Appeals Tribunal) Regulations, 2025  [substantive]

Sub-phase: sis_planning (FIRST sis_planning records in corpus history).
Parent Act: Urban and Regional Planning Act (Act No. 3 of 2015).

Per-record cost: 2 fetches (HTML + PDF) x 8 = 16. Plus 1 robots reverify already done
+ 1 alphabet=U probe = 18 discovery+ingest fetches total this tick.
"""
import sys, os, json, hashlib, time, urllib.request, re
from datetime import datetime, timezone
from bs4 import BeautifulSoup

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6.0
PARSER_VERSION = "0.5.0"

PICKS = [
    {'yr_num':'2017/60','year':'2017','num':'60',
     'title':'Urban and Regional Planning (Designated Local Planning Authorities) Regulations, 2017',
     'sub_phase':'sis_planning','parent_act':'Urban and Regional Planning Act'},
    {'yr_num':'2018/43','year':'2018','num':'43',
     'title':'Urban and Regional Planning (Designated Local Planning Authorities) Regulations, 2018',
     'sub_phase':'sis_planning','parent_act':'Urban and Regional Planning Act'},
    {'yr_num':'2019/42','year':'2019','num':'42',
     'title':'Urban and Regional Planning (Designated Local Planning Authorities) Regulations, 2019',
     'sub_phase':'sis_planning','parent_act':'Urban and Regional Planning Act'},
    {'yr_num':'2020/5','year':'2020','num':'5',
     'title':'Urban and Regional Planning (Designated Local Planning Authority) Regulations, 2020',
     'sub_phase':'sis_planning','parent_act':'Urban and Regional Planning Act'},
    {'yr_num':'2020/56','year':'2020','num':'56',
     'title':'Urban and Regional Planning (General) Regulations, 2020',
     'sub_phase':'sis_planning','parent_act':'Urban and Regional Planning Act'},
    {'yr_num':'2022/57','year':'2022','num':'57',
     'title':'Urban and Regional Planning (Designated Local Planning Authorities) Regulations, 2022',
     'sub_phase':'sis_planning','parent_act':'Urban and Regional Planning Act'},
    {'yr_num':'2023/21','year':'2023','num':'21',
     'title':'Urban and Regional Planning (Development Plans Guidelines and Exempted Development Classes) Regulations, 2023',
     'sub_phase':'sis_planning','parent_act':'Urban and Regional Planning Act'},
    {'yr_num':'2025/65','year':'2025','num':'65',
     'title':'Urban and Regional Planning (Administration of Planning Appeals Tribunal) Regulations, 2025',
     'sub_phase':'sis_planning','parent_act':'Urban and Regional Planning Act'},
]

def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+","-",s).strip('-')
    return s[:120]

def fetch(url, sleep=True):
    if sleep: time.sleep(CRAWL)
    req = urllib.request.Request(url, headers=HEADERS)
    return urllib.request.urlopen(req, timeout=45).read()
