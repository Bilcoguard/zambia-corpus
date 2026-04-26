"""Phase 4 batch 0246 - drain year=2022 p1 residuals + year=2021 p1 novel.

Discovery (this tick): year=2022 p2 = 404 (year=2022 listing exhausted at p1);
year=2021 p2 = 404; year=2021 p1 = 47 unique, 7 novel after filter.

Picks (8) - mixes 4 cached residuals from batch-0245 year=2022 p1 cache and
4 fresh from year=2021 p1 novel:
  1. 2022/17 Customs and Excise (Electronic Machinery and Equipment)
            (Suspension) (Amendment) Regulations, 2022 [sis_tax]
  2. 2022/20 Public Holidays (Declaration) Notice, 2022 [sis_governance]
  3. 2022/36 Customs and Excise (Ports of Entry and Routes) (Amendment)
            Order, 2022 [sis_tax]
  4. 2022/46 Customs and Excise (Machinery and Equipment) (Suspension)
            (Amendment) Regulations, 2022 [sis_tax]
  5. 2021/52 Cyber Security and Cyber Crimes (National Cyber Security,
            Advisory and Coordination Council) Regulations, 2021
            [sis_data_protection FIRST - priority_order item 6]
  6. 2021/60 Zambia Development Agency (Jiangxi Multi-Facility Economic
            Zone) (Declaration) Order, 2021 [sis_industry]
  7. 2021/62 Customs and Excise (Ports of Entry and Routes) (Amendment)
            Order, 2021 [sis_tax]
  8. 2021/73 Public Holidays (Declaration) (No. 4) Notice, 2021
            [sis_governance]

Sub-phase footprint: sis_tax +5 (Customs and Excise Act -- continuing
priority_order item 3 cluster from batch 0245); sis_data_protection FIRST +1
(Cyber Security and Cyber Crimes Act -- priority_order item 6 advanced from
0); sis_governance +2 (Public Holidays Act notices); sis_industry +1
(Zambia Development Agency Act).

Per-record cost: 2 fetches (HTML+PDF) x 8 picks = 16 fresh ingest fetches.
Plus 1 robots reverify + 3 listing probes (year=2022 p2 = 404, year=2021 p2 =
404, year=2021 p1 = 47) = 20 total tick fetches.
"""
import sys, os, json, hashlib, time, urllib.request, re
from datetime import datetime, timezone
from bs4 import BeautifulSoup

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6.0
PARSER_VERSION = "0.5.0"

PICKS = [
    {'yr_num':'2022/17','year':'2022','num':'17',
     'title':'Customs and Excise (Electronic Machinery and Equipment) (Suspension) (Amendment) Regulations, 2022',
     'sub_phase':'sis_tax','parent_act':'Customs and Excise Act',
     'eng_date':'2022-03-04'},
    {'yr_num':'2022/20','year':'2022','num':'20',
     'title':'Public Holidays (Declaration) Notice, 2022',
     'sub_phase':'sis_governance','parent_act':'Public Holidays Act',
     'eng_date':'2022-03-16'},
    {'yr_num':'2022/36','year':'2022','num':'36',
     'title':'Customs and Excise (Ports of Entry and Routes) (Amendment) Order, 2022',
     'sub_phase':'sis_tax','parent_act':'Customs and Excise Act',
     'eng_date':'2022-05-27'},
    {'yr_num':'2022/46','year':'2022','num':'46',
     'title':'Customs and Excise (Machinery and Equipment) (Suspension) (Amendment) Regulations, 2022',
     'sub_phase':'sis_tax','parent_act':'Customs and Excise Act',
     'eng_date':'2022-06-28'},
    {'yr_num':'2021/52','year':'2021','num':'52',
     'title':'Cyber Security and Cyber Crimes (National Cyber Security, Advisory and Coordination Council) Regulations, 2021',
     'sub_phase':'sis_data_protection','parent_act':'Cyber Security and Cyber Crimes Act',
     'eng_date':'2021-05-14'},
    {'yr_num':'2021/60','year':'2021','num':'60',
     'title':'Zambia Development Agency (Jiangxi Multi-Facility Economic Zone) (Declaration) Order, 2021',
     'sub_phase':'sis_industry','parent_act':'Zambia Development Agency Act',
     'eng_date':'2021-05-14'},
    {'yr_num':'2021/62','year':'2021','num':'62',
     'title':'Customs and Excise (Ports of Entry and Routes) (Amendment) Order, 2021',
     'sub_phase':'sis_tax','parent_act':'Customs and Excise Act',
     'eng_date':'2021-05-28'},
    {'yr_num':'2021/73','year':'2021','num':'73',
     'title':'Public Holidays (Declaration) (No. 4) Notice, 2021',
     'sub_phase':'sis_governance','parent_act':'Public Holidays Act',
     'eng_date':'2021-08-20'},
]

def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+","-",s).strip('-')
    return s[:120]

def fetch(url, sleep=True):
    if sleep: time.sleep(CRAWL)
    req = urllib.request.Request(url, headers=HEADERS)
    return urllib.request.urlopen(req, timeout=45).read()
