"""Batch 0227 ingest — fresh L-alphabet probe (4 sis_local_government picks)
plus drain of batch 0226's 4 unused Forest reserves (sis_environment).

Discovery cost: 1 fetch (alphabet L probe). Robots reverify 1 fetch.
Per-record cost: 2 fetches (HTML + PDF) x 8 = 16. Total ~18 fetches.

Picks (8):
  L-alphabet (sis_local_government, parent: Local Government Act / Pensions Act):
    1. 2022/16 Local Authorities Superannuation Fund (Pension Management) Rules
    2. 2021/10 Kasama Municipal Council (Vehicle Loading and Parking Levy) By-laws
    3. 2020/14 Local Government (Fire Services) Order, 2020
    4. 2019/44 Local Government (Fire Inspectors and Fire Officers) Order, 2019
  Forest reserves drain (sis_environment, parent: Forests Act):
    5. 2020/13 National Forest No. F.12 Luano (Alteration of Boundaries) Order
    6. 2021/3  National Forest No. F31 Kabwe (Alteration of Boundaries) Order
    7. 2021/2  Kasama National Forest No. P. 47 (Alteration of Boundaries) Order
    8. 2021/1  Forest Reserve No. 4 Maposa (Cessation) Order
"""
import sys, os, json, hashlib, time, urllib.request, re
from datetime import datetime, timezone
from bs4 import BeautifulSoup

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6.0
PARSER_VERSION = "0.5.0"

PICKS = [
    {'yr_num':'2022/16','year':'2022','num':'16',
     'title':'Local Authorities Superannuation Fund (Pension Management) Rules, 2022',
     'sub_phase':'sis_local_government','parent_act':'Local Authorities Superannuation Fund Act'},
    {'yr_num':'2021/10','year':'2021','num':'10',
     'title':'Kasama Municipal Council (Vehicle Loading and Parking Levy) By-laws, 2021',
     'sub_phase':'sis_local_government','parent_act':'Local Government Act'},
    {'yr_num':'2020/14','year':'2020','num':'14',
     'title':'Local Government (Fire Services) Order, 2020',
     'sub_phase':'sis_local_government','parent_act':'Local Government Act'},
    {'yr_num':'2019/44','year':'2019','num':'44',
     'title':'Local Government (Fire Inspectors and Fire Officers) Order, 2019',
     'sub_phase':'sis_local_government','parent_act':'Local Government Act'},
    {'yr_num':'2020/13','year':'2020','num':'13',
     'title':'National Forest No. F.12 Luano (Alteration of Boundaries) Order, 2020',
     'sub_phase':'sis_environment','parent_act':'Forests Act'},
    {'yr_num':'2021/3','year':'2021','num':'3',
     'title':'National Forest No. F31 Kabwe (Alteration of Boundaries) Order, 2021',
     'sub_phase':'sis_environment','parent_act':'Forests Act'},
    {'yr_num':'2021/2','year':'2021','num':'2',
     'title':'Kasama National Forest No. P. 47 (Alteration of Boundaries) Order, 2021',
     'sub_phase':'sis_environment','parent_act':'Forests Act'},
    {'yr_num':'2021/1','year':'2021','num':'1',
     'title':'Forest Reserve No. 4 Maposa (Cessation) Order, 2021',
     'sub_phase':'sis_environment','parent_act':'Forests Act'},
]

def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+","-",s).strip('-')
    return s[:120]

def fetch(url, sleep=True):
    if sleep: time.sleep(CRAWL)
    req = urllib.request.Request(url, headers=HEADERS)
    return urllib.request.urlopen(req, timeout=45).read()
