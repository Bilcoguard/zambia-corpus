"""Batch 0235 ingest — drain E-alphabet residuals from batch 0233 probe.

Per close-out plan from batch 0234, this tick continues draining the
E-residual cohort first surfaced in batch 0233's E alphabet probe (64
novel candidates, 9 already picked across 0233+0234 = 55 remaining as of
batch 0235 start). Picks 8 from the remaining cohort — all sis_elections
short declaration orders (1-3 pp text PDFs typical of Electoral Process
date-and-time-of-poll orders).

Discovery cost this tick: 1 robots reverify + 0 fresh alphabet probes = 1
discovery fetch. Per-record fetches: 8 picks x 2 (HTML+PDF) = 16 fresh
ingest fetches. Total tick fetches: ~17.

Picks (8 — MAX_BATCH_SIZE cap):
    1. 2022/8   National Assembly By-Election (Kabwata Constituency No. 77)
                (Election Date and Time of Poll) Order, 2022 (sis_elections)
    2. 2022/64  National Assembly By-Elections (Kabushi Constituency No. 36
                and Kwacha Constituency No. 22) (Election Date and Time of
                Poll) (No. 3) Order, 2022 (sis_elections)
    3. 2022/21  Electoral Process (Local Government By-Elections) (Election
                Date and Time of Poll) Order, 2022 (sis_elections)
    4. 2022/38  Electoral Process (Local Government By-Elections) (Election
                Date and Time of Poll) (No. 3) Order, 2022 (sis_elections)
    5. 2021/67  National Assembly General Elections (Mandevu Constituency
                No. 80, Kasenengwa Constituency No. 41, Lusaka Central
                Constituency No. 79, Chawama Constituency No. 76, Mafinga
                Constituency No. 89 and Mpulungu Constituency No. 105)
                (Election Date and Time of Poll) Order, 2021 (sis_elections)
    6. 2022/51  Electoral Process (Local Government By-Elections) (Election
                Date and Time of Poll) Order, 2022 (sis_elections)
    7. 2021/68  Electoral Process (Local Government Elections) (Election
                Date and Time of Poll) (No. 2) Order, 2021 (sis_elections)
    8. 2022/63  Electoral Process (Local Government By-Elections) (Election
                Date and Time of Poll) Order, 2022 (sis_elections)

Sub-phase footprint: sis_elections +8 (drains E residual cohort by 8;
extends established sub-phase from batch 0233 first-instance + 0234 drain).
0 first-instance sub-phases this tick (sis_elections established).

E residuals after this tick: ~47 left for future drain ticks.
"""
import sys, os, json, hashlib, time, urllib.request, re
from datetime import datetime, timezone
from bs4 import BeautifulSoup

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6.0
PARSER_VERSION = "0.5.0"

PICKS = [
    {'yr_num':'2022/8','year':'2022','num':'8',
     'title':'National Assembly By-Election (Kabwata Constituency No. 77) (Election Date and Time of Poll) Order, 2022',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2022-01-14'},
    {'yr_num':'2022/64','year':'2022','num':'64',
     'title':'National Assembly By-Elections (Kabushi Constituency No. 36 and Kwacha Constituency No. 22) (Election Date and Time of Poll) (No. 3) Order, 2022',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2022-10-12'},
    {'yr_num':'2022/21','year':'2022','num':'21',
     'title':'Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) Order, 2022',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2022-03-14'},
    {'yr_num':'2022/38','year':'2022','num':'38',
     'title':'Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) (No. 3) Order, 2022',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2022-06-10'},
    {'yr_num':'2021/67','year':'2021','num':'67',
     'title':'National Assembly General Elections (Mandevu Constituency No. 80, Kasenengwa Constituency No. 41, Lusaka Central Constituency No. 79, Chawama Constituency No. 76, Mafinga Constituency No. 89 and Mpulungu Constituency No. 105) (Election Date and Time of Poll) Order, 2021',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2021-07-30'},
    {'yr_num':'2022/51','year':'2022','num':'51',
     'title':'Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) Order, 2022',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2022-08-12'},
    {'yr_num':'2021/68','year':'2021','num':'68',
     'title':'Electoral Process (Local Government Elections) (Election Date and Time of Poll) (No. 2) Order, 2021',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2021-07-30'},
    {'yr_num':'2022/63','year':'2022','num':'63',
     'title':'Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) Order, 2022',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2022-10-12'},
    {'yr_num':'2021/88','year':'2021','num':'88',
     'title':'Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) (No. 4) Order, 2021',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2021-11-12'},
]

def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+","-",s).strip('-')
    return s[:120]

def fetch(url, sleep=True):
    if sleep: time.sleep(CRAWL)
    req = urllib.request.Request(url, headers=HEADERS)
    return urllib.request.urlopen(req, timeout=45).read()
