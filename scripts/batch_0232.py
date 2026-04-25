"""Batch 0232 ingest — re-probe alphabets M/A/D for residual modern (>=2017) SIs.

Per close-out plan from batch 0231, this tick re-probes M, A, and D alphabets
(stale beyond batches 0223/0224). Discovery results:
  M: 24 SIs / 10 modern / 0 novel (fully drained — all in corpus already)
  A: 20 SIs / 12 modern / 10 novel
  D: 11 SIs /  6 modern /  5 novel
Total novel modern: 15. Picks (8 — MAX_BATCH_SIZE cap, diverse sub-phase mix
incl. FIRST sis_data_protection — priority_order item 6).

Picks (8):
    1. 2018/22  Animal Health (Veterinary Services Fees) Regs, 2018  (sis_agriculture)
    2. 2018/54  Agricultural Institute of Zambia (General) Regs, 2018 (sis_agriculture)
    3. 2019/6   Disaster Management (Qualifications of National Coordinator) Regs, 2019 (sis_disaster_management)
    4. 2019/31  Defence (Regular Forces) (Officers) (Amendment) Regs, 2019 (sis_defence)
    5. 2019/81  Animal Health (Notifiable Diseases) Regs, 2019 (sis_agriculture)
    6. 2021/15  Diplomatic Immunities and Privileges (ICTA) Order, 2021 (sis_foreign_affairs)
    7. 2021/58  Data Protection (Registration and Licensing) Regs, 2021 (sis_data_protection — FIRST)
    8. 2022/70  Defence Force (UN Peacekeeping Operations) (Emoluments) Regs, 2022 (sis_defence)

Sub-phase footprint: sis_agriculture (3) + sis_defence (2) + sis_disaster_management
(1 — first) + sis_foreign_affairs (1 — first) + sis_data_protection (1 — first,
priority_order item 6).

Per-record cost: 2 fetches (HTML+PDF) x 8 = 16 fresh ingest fetches.
Plus 1 robots reverify + 3 alphabet probes (M/A/D) = 20 total tick fetches.
"""
import sys, os, json, hashlib, time, urllib.request, re
from datetime import datetime, timezone
from bs4 import BeautifulSoup

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6.0
PARSER_VERSION = "0.5.0"

PICKS = [
    {'yr_num':'2018/22','year':'2018','num':'22',
     'title':'Animal Health (Veterinary Services Fees) Regulations, 2018',
     'sub_phase':'sis_agriculture','parent_act':'Animal Health Act',
     'eng_date':None},
    {'yr_num':'2018/54','year':'2018','num':'54',
     'title':'Agricultural Institute of Zambia (General) Regulations, 2018',
     'sub_phase':'sis_agriculture','parent_act':'Agricultural Institute of Zambia Act',
     'eng_date':None},
    {'yr_num':'2019/6','year':'2019','num':'6',
     'title':'Disaster Management (Qualifications of National Coordinator) Regulations, 2019',
     'sub_phase':'sis_disaster_management','parent_act':'Disaster Management Act',
     'eng_date':None},
    {'yr_num':'2019/31','year':'2019','num':'31',
     'title':'Defence (Regular Forces) (Officers) (Amendment) Regulations, 2019',
     'sub_phase':'sis_defence','parent_act':'Defence Act',
     'eng_date':None},
    {'yr_num':'2019/81','year':'2019','num':'81',
     'title':'Animal Health (Notifiable Diseases) Regulations, 2019',
     'sub_phase':'sis_agriculture','parent_act':'Animal Health Act',
     'eng_date':None},
    {'yr_num':'2021/15','year':'2021','num':'15',
     'title':'Diplomatic Immunities and Privileges (International Centre for Tropical Agriculture) Order, 2021',
     'sub_phase':'sis_foreign_affairs','parent_act':'Diplomatic Immunities and Privileges Act',
     'eng_date':None},
    {'yr_num':'2021/58','year':'2021','num':'58',
     'title':'Data Protection (Registration and Licensing) Regulations, 2021',
     'sub_phase':'sis_data_protection','parent_act':'Data Protection Act',
     'eng_date':None},
    {'yr_num':'2022/70','year':'2022','num':'70',
     'title':'Defence Force (United Nations Peacekeeping Operations) (Emoluments) Regulations, 2022',
     'sub_phase':'sis_defence','parent_act':'Defence Act',
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
