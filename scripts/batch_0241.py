"""Phase 4 batch 0241 - sis_elections E-residual drain (final novel) +
sis_employment E-residual + FIRST sis_education cluster + sis_judicial
single from H-probe.

Discovery: re-probe alphabet H (1 fetch) — yielded 6 novel modern SIs.
Combined with the 3 remaining unprocessed novel items from batch_0233 E-probe
cache (2024/15, 2024/29, 2022/13). Total 9 picks (8 + 1 substitute).

Picks (8 + 1 substitute):
    1. 2024/15  Electoral Process (LG By-Elections) Order, 2024 [sis_elections; E-residual]
    2. 2024/29  Electoral Process (LG By-Elections) Order, 2024 [sis_elections; E-residual]
    3. 2022/13  Minimum Wages and Conditions of Employment (Truck and Bus Drivers) (Amendment) Order, 2022 [sis_employment; E-residual]
    4. 2022/5   Economic and Financial Crimes (Division of Court) Order, 2022 [sis_judicial — FIRST sub-phase]
    5. 2022/39  Education (Public Higher Education Institution) (Declaration) Order, 2022 [sis_education — FIRST sub-phase]
    6. 2019/69  Palabana University (Declaration) Order, 2019 [sis_education]
    7. 2018/39  Levy Mwanawasa Medical University (Declaration) Order, 2018 [sis_education]
    8. 2018/3   Zambia Defence University (Declaration) Order, 2018 [sis_education]
    sub: 2018/2 Education (Military Training Establishment of Zambia Management) (Dissolution) Regulations, 2018 [sis_education]

Sub-phase footprint: sis_elections +2 (drain), sis_employment +1 (drain),
sis_judicial +1 (FIRST cluster), sis_education +4 (FIRST cluster).
2 first-instance sub-phases this tick.

Per-record cost: 2 fetches (HTML+PDF) x 8 = 16 fresh ingest fetches.
Plus 1 robots reverify + 1 alphabet H probe = 18 total tick fetches.
"""
import sys, os, json, hashlib, time, urllib.request, re
from datetime import datetime, timezone
from bs4 import BeautifulSoup

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6.0
PARSER_VERSION = "0.5.0"

PICKS = [
    {'yr_num':'2024/15','year':'2024','num':'15',
     'title':'Electoral Process (Local Government By Elections) (Election Date and Time of Poll) Order, 2024',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2024-02-02'},
    {'yr_num':'2024/29','year':'2024','num':'29',
     'title':'Electoral Process (Local Government By-elections) (Election Date and Time of Poll) Order, 2024',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2024-05-31'},
    {'yr_num':'2022/13','year':'2022','num':'13',
     'title':'Minimum Wages and Conditions of Employment (Truck and Bus Drivers) (Amendment) Order, 2022',
     'sub_phase':'sis_employment','parent_act':'Minimum Wages and Conditions of Employment Act',
     'eng_date':'2022-01-28'},
    {'yr_num':'2022/5','year':'2022','num':'5',
     'title':'Economic and Financial Crimes (Division of Court) Order, 2022',
     'sub_phase':'sis_judicial','parent_act':'Subordinate Courts Act',
     'eng_date':'2022-01-14'},
    {'yr_num':'2022/39','year':'2022','num':'39',
     'title':'Education (Public Higher Education Institution) (Declaration) Order, 2022',
     'sub_phase':'sis_education','parent_act':'Higher Education Act',
     'eng_date':'2022-06-03'},
    {'yr_num':'2019/69','year':'2019','num':'69',
     'title':'Palabana University (Declaration) Order, 2019',
     'sub_phase':'sis_education','parent_act':'Higher Education Act',
     'eng_date':'2019-10-17'},
    {'yr_num':'2018/39','year':'2018','num':'39',
     'title':'Levy Mwanawasa Medical University (Declaration) Order, 2018',
     'sub_phase':'sis_education','parent_act':'Higher Education Act',
     'eng_date':'2018-05-24'},
    {'yr_num':'2018/3','year':'2018','num':'3',
     'title':'Zambia Defence University (Declaration) Order, 2018',
     'sub_phase':'sis_education','parent_act':'Higher Education Act',
     'eng_date':'2018-01-26'},
    # idx 8 = in-batch substitute
    {'yr_num':'2018/2','year':'2018','num':'2',
     'title':'Education (Military Training Establishment of Zambia Management) (Dissolution) Regulations, 2018',
     'sub_phase':'sis_education','parent_act':'Education Act',
     'eng_date':'2018-01-26'},
]

def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+","-",s).strip('-')
    return s[:120]

def fetch(url, sleep=True):
    if sleep: time.sleep(CRAWL)
    req = urllib.request.Request(url, headers=HEADERS)
    return urllib.request.urlopen(req, timeout=45).read()
