"""Batch 0230 ingest — drain U-alphabet residuals from batch 0229 cache.

Per close-out plan from batch 0229, the U-alphabet probe surfaced 19 modern
candidates of which 8 were ingested in batch 0229. This batch drains the
oldest 8 of the 11 remaining residuals (2017-2020) — all are short DLPA
declaration orders under the Urban and Regional Planning Act (Act No. 3 of
2015) and 100% text-extract yield is expected based on batch 0229's
experience with the same shape of order.

Picks (8 — MAX_BATCH_SIZE cap):
    1. 2017/64   URP (DLPA) (No. 2) Regulations, 2017
    2. 2018/44   URP (DLPA) (No. 2) Regulations, 2018
    3. 2019/43   URP (DLPA) (No. 2) Regulations, 2019
    4. 2019/45   URP (DLPA) (No. 3) Regulations, 2019
    5. 2019/78   URP (DLPA) Regulations, 2019
    6. 2020/9    URP (DLPA) Regulations, 2020
    7. 2020/55   URP (DLPA) Regulations, 2020
    8. 2020/108  URP (DLPA) (No.3) Regulations, 2020

Reserve (3 for next tick): 2022/60, 2023/9, 2023/45.

Sub-phase: sis_planning (continues the URP Act cluster started in batch 0229).
Parent Act: Urban and Regional Planning Act (Act No. 3 of 2015).

Per-record cost: 2 fetches (HTML + PDF) x 8 = 16. Plus 1 robots reverify
(already done at tick start) + 0 fresh discovery fetches (cache reused from
batch 0229) = 17 total fetches this tick.
"""
import sys, os, json, hashlib, time, urllib.request, re
from datetime import datetime, timezone
from bs4 import BeautifulSoup

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6.0
PARSER_VERSION = "0.5.0"

PICKS = [
    {'yr_num':'2017/64','year':'2017','num':'64',
     'title':'Urban and Regional Planning (Designated Local Planning Authorities) (No. 2) Regulations, 2017',
     'sub_phase':'sis_planning','parent_act':'Urban and Regional Planning Act'},
    {'yr_num':'2018/44','year':'2018','num':'44',
     'title':'Urban and Regional Planning (Designated Local Planning Authorities) (No. 2) Regulations, 2018',
     'sub_phase':'sis_planning','parent_act':'Urban and Regional Planning Act'},
    {'yr_num':'2019/43','year':'2019','num':'43',
     'title':'Urban and Regional Planning (Designated Local Planning Authorities) (No. 2) Regulations, 2019',
     'sub_phase':'sis_planning','parent_act':'Urban and Regional Planning Act'},
    {'yr_num':'2019/45','year':'2019','num':'45',
     'title':'Urban and Regional Planning (Designated Local Planning Authorities) (No. 3) Regulations, 2019',
     'sub_phase':'sis_planning','parent_act':'Urban and Regional Planning Act'},
    {'yr_num':'2019/78','year':'2019','num':'78',
     'title':'Urban and Regional Planning (Designated Local Planning Authorities) Regulations, 2019',
     'sub_phase':'sis_planning','parent_act':'Urban and Regional Planning Act'},
    {'yr_num':'2020/9','year':'2020','num':'9',
     'title':'Urban and Regional Planning (Designated Local Planning Authorities) Regulations, 2020',
     'sub_phase':'sis_planning','parent_act':'Urban and Regional Planning Act'},
    {'yr_num':'2020/55','year':'2020','num':'55',
     'title':'Urban and Regional Planning (Designated Local Planning Authorities) Regulations, 2020',
     'sub_phase':'sis_planning','parent_act':'Urban and Regional Planning Act'},
    {'yr_num':'2020/108','year':'2020','num':'108',
     'title':'Urban and Regional Planning (Designated Local Planning Authorities) (No.3) Regulations, 2020',
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
