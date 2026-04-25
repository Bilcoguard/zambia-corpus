"""Phase 4 batch 0236 — sis_elections E-residual drain (cohort 2 from batch_0233 E-probe cache).

Picks: 8 sis_elections SIs not yet in corpus, drawn from the 47 remaining novel
E-alphabet candidates after batch 0235. Skips OCR-backlog 2022/008 (Kabwata).

    1. 2022/061  Electoral Process (LG By-Elections) (No. 2) Order, 2022
    2. 2021/087  National Assembly By-Election (Kabwata No. 77) (No. 3) Order, 2021
    3. 2021/075  Electoral Process (LG Elections) Order, 2021
    4. 2021/074  National Assembly (Kaumbwe No. 50) Order, 2021
    5. 2020/101  Electoral Process (LG By-Elections) (No. 8) Order, 2020
    6. 2020/079  Electoral Process (LG By-Elections) (No. 8) Order, 2020 (sept)
    7. 2020/072  Electoral Process (LG By-Elections) (No. 7) Order, 2020
    8. 2020/071  National Assembly By-Election (Mwansabombwe + Lukashya) Order, 2020

Sub-phase: sis_elections +8 (drain). 0 first-instance sub-phases.
E residuals after this tick: ~39 left from batch-0233 cache (47 - 8).
"""
import sys, os, json, hashlib, time, urllib.request, re
from datetime import datetime, timezone
from bs4 import BeautifulSoup

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6.0
PARSER_VERSION = "0.5.0"

PICKS = [
    {'yr_num':'2022/61','year':'2022','num':'61',
     'title':'Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) (No. 2) Order, 2022',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2022-09-30'},
    {'yr_num':'2021/87','year':'2021','num':'87',
     'title':'National Assembly By-Election (Kabwata Constituency No. 77) (Election Date and Time of Poll) (No. 3) Order, 2021',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2021-12-17'},
    {'yr_num':'2021/75','year':'2021','num':'75',
     'title':'Electoral Process (Local Government Elections) (Election Date and Time of Poll) Order, 2021',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2021-09-10'},
    {'yr_num':'2021/74','year':'2021','num':'74',
     'title':'National Assembly (Kaumbwe Constituency No. 50) (Election Date and Time of Poll) Order, 2021',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2021-09-10'},
    {'yr_num':'2020/101','year':'2020','num':'101',
     'title':'Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) (No. 8 ) Order, 2020',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2020-12-11'},
    {'yr_num':'2020/79','year':'2020','num':'79',
     'title':'Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) (No. 8 ) Order, 2020',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2020-09-25'},
    {'yr_num':'2020/72','year':'2020','num':'72',
     'title':'Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) (No. 7 ) Order, 2020',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2020-08-21'},
    {'yr_num':'2020/71','year':'2020','num':'71',
     'title':'National Assembly By-Election (Mwansabombwe Constituency No. 65 and Lukashya Constituency No. 98) (Election Date and Time Poll) Order, 2020',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2020-08-21'},
]

def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+","-",s).strip('-')
    return s[:120]

def fetch(url, sleep=True):
    if sleep: time.sleep(CRAWL)
    req = urllib.request.Request(url, headers=HEADERS)
    return urllib.request.urlopen(req, timeout=45).read()
