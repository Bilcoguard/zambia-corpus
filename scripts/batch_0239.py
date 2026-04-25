"""Phase 4 batch 0239 — sis_elections E-residual drain (cohort 5 from batch_0233 E-probe cache).

Picks: 8 sis_elections SIs not yet in corpus, drawn from the 23 remaining novel
E-alphabet candidates after batch 0238. This cohort takes the next 2018-2019
sequence — short by-election declaration orders.

Skipped from cache (known scanned-image failures, deferred to OCR backlog):
  - 2018/075 National Assembly By-Election (Mangango)  (failed batch 0238)
  - 2022/008 National Assembly By-Election (Kabwata)   (failed batch 0235)

    1. 2018/093  National Assembly By-Election (Sesheke No. 153) Order, 2018
    2. 2018/094  Electoral Process (LG By-Elections) Order, 2018
    3. 2019/016  National Assembly By-Election (Bahati No. 062) Order, 2019
    4. 2019/023  Electoral Process (LG By-Elections) Order, 2019
    5. 2019/024  Electoral Process (LG By-Elections) Order, 2019
    6. 2019/033  Electoral Process (LG By-Elections) Order, 2019
    7. 2019/038  National Assembly By-Election (Katuba No. 01) Order, 2019
    8. 2019/061  Electoral Process (LG By-Elections) Order, 2019

In-batch substitute slot (idx 8): 2019/076 LG By-Elections (Nov 2019).

Sub-phase: sis_elections +8 (drain). 0 first-instance sub-phases.
E residuals after this tick: ~15 left from batch-0233 cache (23 - 8 if all ok).
"""
import sys, os, json, hashlib, time, urllib.request, re
from datetime import datetime, timezone
from bs4 import BeautifulSoup

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6.0
PARSER_VERSION = "0.5.0"

PICKS = [
    {'yr_num':'2018/93','year':'2018','num':'93',
     'title':'National Assembly By-Election (Sesheke Constituency No. 153) (Election Date and Time of Poll) Order, 2018',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2018-12-21'},
    {'yr_num':'2018/94','year':'2018','num':'94',
     'title':'Electoral Process (Local Governments By-Elections) (Election Date and Time of Poll) (No. 7) Order, 2018',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2018-12-21'},
    {'yr_num':'2019/16','year':'2019','num':'16',
     'title':'National Assembly By-Election (Bahati Constituency No. 062) (Election Date and Time of Poll) Order, 2019',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2019-03-01'},
    {'yr_num':'2019/23','year':'2019','num':'23',
     'title':'Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) Order, 2019',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2019-03-15'},
    {'yr_num':'2019/24','year':'2019','num':'24',
     'title':'Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) (No. 2) Order, 2019',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2019-03-15'},
    {'yr_num':'2019/33','year':'2019','num':'33',
     'title':'Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) (No. 3) Order, 2019',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2019-05-22'},
    {'yr_num':'2019/38','year':'2019','num':'38',
     'title':'National Assembly By-Election (Katuba Constituency No. 01) (Election Date and Time of Poll) Order, 2019',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2019-06-07'},
    {'yr_num':'2019/61','year':'2019','num':'61',
     'title':'Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) (No. 4) Order, 2019',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2019-09-13'},
    # idx 8 = in-batch substitute for any pdf_parse_empty
    {'yr_num':'2019/76','year':'2019','num':'76',
     'title':'Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) (No. 5) Order, 2019',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2019-11-15'},
]

def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+","-",s).strip('-')
    return s[:120]

def fetch(url, sleep=True):
    if sleep: time.sleep(CRAWL)
    req = urllib.request.Request(url, headers=HEADERS)
    return urllib.request.urlopen(req, timeout=45).read()
