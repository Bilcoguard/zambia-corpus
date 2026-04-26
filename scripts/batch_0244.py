"""Phase 4 batch 0244 - drain reserved residuals from batch 0243's
year=2024 p3 cache (5 unused) + batch 0242's year=2025 listing cache
(2 unused substitutes carried via batch 0243). 7 records, no fresh
discovery fetches needed (cache-only tick).

Picks (7 cache-drain, no substitutes — 7 record target):
    1. 2021/35 Citizens Economic Empowerment (Transportation of Heavy and Bulk
       Commodities by Road) (Reservation) Regulations, 2021 [sis_industry FIRST]
    2. 2019/22 Citizens Economic Empowerment (Reservation Scheme) Regulations,
       2019 [sis_industry]
    3. 2025/20 Compulsory Standards (Declaration) Order, 2025 [sis_industry]
    4. 2020/18 Compulsory Standards (Potable Spirits) (Declaration) Order, 2020
       [sis_industry]
    5. 2018/64 Constitutional Offices Emoluments Regulations, 2018 [sis_governance]
    6. 1992/9  Air Passenger Service Charge (Charging) Order, 1992 [sis_transport]
    7. 1985/45 Air Services (Aerial Application Permit) Regulations, 1985 [sis_transport]

Sub-phase footprint: sis_industry FIRST cluster +4 (Citizens Economic
Empowerment Act + Compulsory Standards Act parent-Act linkage), sis_governance
+1 (Constitutional Offices Emoluments Act), sis_transport +2 (Air Passenger
Service Charge Act + Aviation Act historic SIs).

Per-record cost: 2 fetches (HTML+PDF) x 7 picks = 14 fresh ingest fetches.
Plus 1 robots reverify = 15 total tick fetches. Zero discovery probes
(pure cache drain).
"""
import sys, os, json, hashlib, time, urllib.request, re
from datetime import datetime, timezone
from bs4 import BeautifulSoup

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6.0
PARSER_VERSION = "0.5.0"

PICKS = [
    {'yr_num':'2021/35','year':'2021','num':'35',
     'title':'Citizens Economic Empowerment (Transportation of Heavy and Bulk Commodities by Road) (Reservation) Regulations, 2021',
     'sub_phase':'sis_industry','parent_act':'Citizens Economic Empowerment Act',
     'eng_date':'2021-05-04'},
    {'yr_num':'2019/22','year':'2019','num':'22',
     'title':'Citizens Economic Empowerment (Reservation Scheme) Regulations, 2019',
     'sub_phase':'sis_industry','parent_act':'Citizens Economic Empowerment Act',
     'eng_date':'2019-03-15'},
    {'yr_num':'2025/20','year':'2025','num':'20',
     'title':'Compulsory Standards (Declaration) Order, 2025',
     'sub_phase':'sis_industry','parent_act':'Compulsory Standards Act',
     'eng_date':'2025-05-09'},
    {'yr_num':'2020/18','year':'2020','num':'18',
     'title':'Compulsory Standards (Potable Spirits) (Declaration) Order, 2020',
     'sub_phase':'sis_industry','parent_act':'Compulsory Standards Act',
     'eng_date':'2020-02-28'},
    {'yr_num':'2018/64','year':'2018','num':'64',
     'title':'Constitutional Offices Emoluments Regulations, 2018',
     'sub_phase':'sis_governance','parent_act':'Constitutional Offices Emoluments Act',
     'eng_date':'2018-08-17'},
    {'yr_num':'1992/9','year':'1992','num':'9',
     'title':'Air Passenger Service Charge (Charging) Order, 1992',
     'sub_phase':'sis_transport','parent_act':'Air Passenger Service Charge Act',
     'eng_date':'1992-01-31'},
    {'yr_num':'1985/45','year':'1985','num':'45',
     'title':'Air Services (Aerial Application Permit) Regulations, 1985',
     'sub_phase':'sis_transport','parent_act':'Aviation Act',
     'eng_date':'1985-04-04'},
]

def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+","-",s).strip('-')
    return s[:120]

def fetch(url, sleep=True):
    if sleep: time.sleep(CRAWL)
    req = urllib.request.Request(url, headers=HEADERS)
    return urllib.request.urlopen(req, timeout=45).read()
