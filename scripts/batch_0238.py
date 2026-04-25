"""Phase 4 batch 0238 — sis_elections E-residual drain (cohort 4 from batch_0233 E-probe cache).

Picks: 8 sis_elections SIs not yet in corpus, drawn from the 31 remaining novel
E-alphabet candidates after batch 0237. This cohort takes the oldest 8 entries
(2017-2018) — short by-election declaration orders that recent batches
(0233-0237) have shown to text-extract cleanly.

    1. 2017/018  Local Government By-Elections Order, 2017
    2. 2017/054  Electoral Process (LG By-Elections) Order, 2017
    3. 2018/021  Electoral Process (LG By-Election) Order, 2018
    4. 2018/033  Electoral Process (LG By-Elections) Order, 2018
    5. 2018/046  Electoral Process (LG By-Elections) (No. 3) Order, 2018
    6. 2018/056  National Assembly By-Election (Kasenengwa No. 41) (No. 2) Order, 2018
    7. 2018/057  Electoral Process (LG By-Elections) (No. 4) Order, 2018
    8. 2018/075  National Assembly By-Election (Mangango No. 141) Order, 2018

Sub-phase: sis_elections +8 (drain). 0 first-instance sub-phases.
E residuals after this tick: ~23 left from batch-0233 cache (31 - 8).
"""
import sys, os, json, hashlib, time, urllib.request, re
from datetime import datetime, timezone
from bs4 import BeautifulSoup

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6.0
PARSER_VERSION = "0.5.0"

PICKS = [
    {'yr_num':'2017/18','year':'2017','num':'18',
     'title':'Local Government By-Elections (Election Dates and Times of Poll) Order, 2017',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2017-02-24'},
    {'yr_num':'2017/54','year':'2017','num':'54',
     'title':'Electoral Process (Local Government By-Elections) (Election Date and Times of Poll) Order, 2017',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2017-07-14'},
    {'yr_num':'2018/21','year':'2018','num':'21',
     'title':'Electoral Process (Local Government By-Election) (Election Date and Time of Poll) Order, 2018',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2018-03-23'},
    {'yr_num':'2018/33','year':'2018','num':'33',
     'title':'Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) Order, 2018',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2018-04-20'},
    {'yr_num':'2018/46','year':'2018','num':'46',
     'title':'Electoral Process (Local Government By Elections) (Election Date and Time of Poll) (No. 3) Order, 2018',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2018-06-15'},
    {'yr_num':'2018/56','year':'2018','num':'56',
     'title':'National Assembly By-Election (Kasenengwa Constituency No. 41) (Election Date and Time of Poll) (No. 2) Order, 2018',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2018-08-03'},
    {'yr_num':'2018/57','year':'2018','num':'57',
     'title':'Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) (No. 4) Order, 2018',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2018-08-03'},
    {'yr_num':'2018/75','year':'2018','num':'75',
     'title':'National Assembly By-Election (Mangango Constituency No. 141) (Election Date and Time of Poll) Order, 2018',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2018-10-05'},
    # idx 8 = in-batch substitute for failed idx 7 (2018/75 pdf_parse_empty scanned image)
    {'yr_num':'2018/81','year':'2018','num':'81',
     'title':'Electoral Process (Local Governments By-Elections) (Election Date and Time of Poll) (No. 6) Order, 2018',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2018-10-26'},
]

def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+","-",s).strip('-')
    return s[:120]

def fetch(url, sleep=True):
    if sleep: time.sleep(CRAWL)
    req = urllib.request.Request(url, headers=HEADERS)
    return urllib.request.urlopen(req, timeout=45).read()
