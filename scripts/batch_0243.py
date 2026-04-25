"""Phase 4 batch 0243 - sis_corporate FIRST cluster from year=2024 page=3 listing
(priority_order item 2 unlocked) + sis_governance + sis_transport extension.

Discovery: probed alphabet G=0/U=0/X=0/Y=0/Z=0 (all probed exhausted of novel
modern); then year=2024 p2=0 novel, year=2024 p3=13 novel modern. Plus carry
forward 2 unprocessed residuals from batch 0242's year=2025 listing cache
(1992/9 + 1985/45) as in-batch substitutes.

Picks (8 + 2 substitutes):
    1. 2019/14 Companies (General) Regulations, 2019 [sis_corporate - FIRST cluster]
    2. 2019/15 Companies (Fees) Regulations, 2019 [sis_corporate]
    3. 2019/21 Companies (Prescribed Forms) Regulations, 2019 [sis_corporate]
    4. 2019/40 Corporate Insolvency (Insolvency Practitioner Accreditation) Regulations, 2019 [sis_corporate]
    5. 2017/50 Citizenship of Zambia Regulations, 2017 [sis_governance]
    6. 2022/27 Citizenship of Zambia (Amendment) Regulations, 2022 [sis_governance]
    7. 2025/16 Civil Aviation (Designated Provincial and Strategic Airports) Regulations, 2025 [sis_transport]
    8. 2020/73 Civil Aviation Authority (Search and Rescue) Regulations, 2020 [sis_transport]
    sub-a: 1992/9  Air Passenger Service Charge (Charging) Order, 1992 [sis_transport]
    sub-b: 1985/45 Air Services (Aerial Application Permit) Regulations, 1985 [sis_transport]

Sub-phase footprint: sis_corporate FIRST cluster +4 (priority_order item 2 advanced),
sis_governance +2 (Citizenship Act parent-Act linkage with amendment chain),
sis_transport +2 (Civil Aviation Act parent-Act linkage). 1 first-instance
sub-phase this tick: sis_corporate.

Per-record cost: 2 fetches (HTML+PDF) x 8 picks = 16 fresh ingest fetches.
Plus 1 robots reverify + 9 discovery probes (G/U/X/Y/Z + year2024 + year2024p2 + year2024p3 + year2023) = 26 total tick fetches.
"""
import sys, os, json, hashlib, time, urllib.request, re
from datetime import datetime, timezone
from bs4 import BeautifulSoup

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6.0
PARSER_VERSION = "0.5.0"

PICKS = [
    {'yr_num':'2019/14','year':'2019','num':'14',
     'title':'Companies (General) Regulations, 2019',
     'sub_phase':'sis_corporate','parent_act':'Companies Act',
     'eng_date':'2019-03-01'},
    {'yr_num':'2019/15','year':'2019','num':'15',
     'title':'Companies (Fees) Regulations, 2019',
     'sub_phase':'sis_corporate','parent_act':'Companies Act',
     'eng_date':'2019-03-01'},
    {'yr_num':'2019/21','year':'2019','num':'21',
     'title':'Companies (Prescribed Forms) Regulations, 2019',
     'sub_phase':'sis_corporate','parent_act':'Companies Act',
     'eng_date':'2019-03-07'},
    {'yr_num':'2019/40','year':'2019','num':'40',
     'title':'Corporate Insolvency (Insolvency Practitioner Accreditation) Regulations, 2019',
     'sub_phase':'sis_corporate','parent_act':'Corporate Insolvency Act',
     'eng_date':'2019-07-26'},
    {'yr_num':'2017/50','year':'2017','num':'50',
     'title':'Citizenship of Zambia Regulations, 2017',
     'sub_phase':'sis_governance','parent_act':'Citizenship of Zambia Act',
     'eng_date':'2022-01-01'},
    {'yr_num':'2022/27','year':'2022','num':'27',
     'title':'Citizenship of Zambia (Amendment) Regulations, 2022',
     'sub_phase':'sis_governance','parent_act':'Citizenship of Zambia Act',
     'eng_date':'2022-04-01'},
    {'yr_num':'2025/16','year':'2025','num':'16',
     'title':'Civil Aviation (Designated Provincial and Strategic Airports) Regulations, 2025',
     'sub_phase':'sis_transport','parent_act':'Civil Aviation Act',
     'eng_date':'2025-04-17'},
    {'yr_num':'2020/73','year':'2020','num':'73',
     'title':'Civil Aviation Authority (Search and Rescue) Regulations, 2020',
     'sub_phase':'sis_transport','parent_act':'Civil Aviation Authority Act',
     'eng_date':'2020-08-28'},
    # idx 8 = in-batch substitute A
    {'yr_num':'1992/9','year':'1992','num':'9',
     'title':'Air Passenger Service Charge (Charging) Order, 1992',
     'sub_phase':'sis_transport','parent_act':'Air Passenger Service Charge Act',
     'eng_date':'1992-01-31'},
    # idx 9 = in-batch substitute B
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
