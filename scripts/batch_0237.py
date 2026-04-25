"""Phase 4 batch 0237 — sis_elections E-residual drain (cohort 3 from batch_0233 E-probe cache).

Picks: 8 sis_elections SIs not yet in corpus, drawn from the 38 remaining novel
E-alphabet candidates after batch 0236.

    1. 2020/063  Electoral Process (LG By-Elections) (No. 6) Order, 2020
    2. 2020/061  Electoral Process (LG By-Election) (No. 5) Order, 2020
    3. 2020/043  Electoral Process (LG By-Election) (No. 4) Order, 2020
    4. 2020/023  Electoral Process (LG By-Elections) (No. 3) Order, 2020
    5. 2020/004  Electoral Process (LG By-Elections) (No. 2) Order, 2020
    6. 2020/003  Electoral Process (LG By-Elections) Order, 2020
    7. 2020/002  National Assembly By-Election (Chilubi No. 095) Order, 2020
    8. 2023/008  Electoral Process (LG By-Elections) Order, 2023

Sub-phase: sis_elections +8 (drain). 0 first-instance sub-phases.
E residuals after this tick: ~30 left from batch-0233 cache (38 - 8).
"""
import sys, os, json, hashlib, time, urllib.request, re
from datetime import datetime, timezone
from bs4 import BeautifulSoup

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6.0
PARSER_VERSION = "0.5.0"

PICKS = [
    {'yr_num':'2020/63','year':'2020','num':'63',
     'title':'Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) (No. 6) Order, 2020',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2020-07-17'},
    {'yr_num':'2020/61','year':'2020','num':'61',
     'title':'Electoral Process (Local Government By-Election) (Election Date and Time of Poll) (No. 5) Order, 2020',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2020-06-26'},
    {'yr_num':'2020/43','year':'2020','num':'43',
     'title':'Electoral Process (Local Government By-Election) (Election Date and Time of Poll) (No. 4) Order, 2020',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2020-04-30'},
    {'yr_num':'2020/23','year':'2020','num':'23',
     'title':'Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) (No. 3) Order, 2020',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2020-03-20'},
    {'yr_num':'2020/4','year':'2020','num':'4',
     'title':'Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) (No. 2) Order, 2020',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2020-01-10'},
    {'yr_num':'2020/3','year':'2020','num':'3',
     'title':'Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) Order, 2020',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2020-01-03'},
    {'yr_num':'2020/2','year':'2020','num':'2',
     'title':'National Assembly By-Election (Chilubi Constituency No. 095) (Election date and time of Poll) Order, 2020',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2020-01-03'},
    {'yr_num':'2023/8','year':'2023','num':'8',
     'title':'Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) Order, 2023',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2023-03-10'},
]

def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+","-",s).strip('-')
    return s[:120]

def fetch(url, sleep=True):
    if sleep: time.sleep(CRAWL)
    req = urllib.request.Request(url, headers=HEADERS)
    return urllib.request.urlopen(req, timeout=45).read()
