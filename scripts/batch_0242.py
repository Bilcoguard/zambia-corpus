"""Phase 4 batch 0242 - alphabet R probe yields sis_transport (Road/Rail) cluster +
year=2025 listing yields sis_agriculture (Animal Health) cluster + sis_transport
(Air Services) coverage.

Discovery: probed K=0 SIs, R=4 modern novel, O=0 SIs, Q=0 SIs, year=2025 listing=7
novel (pre-2017 mix). Total fresh candidates: 11. Probes consumed: 4 fetches.

Picks (8 + 1 substitute):
    1. 2018/7    Railways (Transportation of Heavy Goods) Regulations, 2018 [sis_transport - FIRST cluster]
    2. 2020/50   Road Traffic (Driving Licence) Regulations, 2020 [sis_transport]
    3. 2021/112  Road Traffic (Fees) Regulations, 2021 [sis_transport]
    4. 2020/7    Road Traffic (Speed Limits) Regulations, 2019 [sis_transport]
    5. 2014/16   Animal Health (Livestock Cleansing) Order, 2014 [sis_agriculture - FIRST cluster]
    6. 2014/24   Animal Health (Control and Prevention of Animal Disease) Order, 2014 [sis_agriculture]
    7. 2014/59   Agricultural Credits (Appointment of Authorised Agency) Order, 2014 [sis_agriculture]
    8. 2001/32   Air Services (Permit Fees) Regulations, 2001 [sis_transport]
    sub: 1985/24 Air Passenger Service Charge (Appointment of Collection Agents) (No. 2) Order, 1985 [sis_transport]

Sub-phase footprint: sis_transport +5 (FIRST cluster: Railways + 3 Road Traffic +
Air Services), sis_agriculture +3 (FIRST cluster: 2 Animal Health + 1 Agricultural
Credits). 2 first-instance sub-phases this tick.

Per-record cost: 2 fetches (HTML+PDF) x 8 = 16 fresh ingest fetches.
Plus 1 robots reverify + 4 discovery probes = 21 total tick fetches.
"""
import sys, os, json, hashlib, time, urllib.request, re
from datetime import datetime, timezone
from bs4 import BeautifulSoup

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6.0
PARSER_VERSION = "0.5.0"

PICKS = [
    {'yr_num':'2018/7','year':'2018','num':'7',
     'title':'Railways (Transportation of Heavy Goods) Regulations, 2018',
     'sub_phase':'sis_transport','parent_act':'Railways Act',
     'eng_date':'2018-02-02'},
    {'yr_num':'2020/50','year':'2020','num':'50',
     'title':'Road Traffic (Driving Licence) Regulations, 2020',
     'sub_phase':'sis_transport','parent_act':'Road Traffic Act',
     'eng_date':'2020-05-15'},
    {'yr_num':'2021/112','year':'2021','num':'112',
     'title':'Road Traffic (Fees) Regulations, 2021',
     'sub_phase':'sis_transport','parent_act':'Road Traffic Act',
     'eng_date':'2021-12-31'},
    {'yr_num':'2020/7','year':'2020','num':'7',
     'title':'Road Traffic (Speed Limits) Regulations, 2019',
     'sub_phase':'sis_transport','parent_act':'Road Traffic Act',
     'eng_date':'2020-01-24'},
    {'yr_num':'2014/16','year':'2014','num':'16',
     'title':'Animal Health (Livestock Cleansing) Order, 2014',
     'sub_phase':'sis_agriculture','parent_act':'Animal Health Act',
     'eng_date':'2014-02-14'},
    {'yr_num':'2014/24','year':'2014','num':'24',
     'title':'Animal Health (Control and Prevention of Animal Disease) Order, 2014',
     'sub_phase':'sis_agriculture','parent_act':'Animal Health Act',
     'eng_date':'2014-03-21'},
    {'yr_num':'2014/59','year':'2014','num':'59',
     'title':'Agricultural Credits (Appointment of Authorised Agency) Order, 2014',
     'sub_phase':'sis_agriculture','parent_act':'Agricultural Credits Act',
     'eng_date':'2014-11-07'},
    {'yr_num':'2001/32','year':'2001','num':'32',
     'title':'Air Services (Permit Fees) Regulations, 2001',
     'sub_phase':'sis_transport','parent_act':'Aviation Act',
     'eng_date':'2001-03-09'},
    # idx 8 = in-batch substitute
    {'yr_num':'1985/24','year':'1985','num':'24',
     'title':'Air Passenger Service Charge (Appointment of Collection Agents) (No. 2) Order, 1985',
     'sub_phase':'sis_transport','parent_act':'Air Passenger Service Charge Act',
     'eng_date':'1985-02-01'},
]

def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+","-",s).strip('-')
    return s[:120]

def fetch(url, sleep=True):
    if sleep: time.sleep(CRAWL)
    req = urllib.request.Request(url, headers=HEADERS)
    return urllib.request.urlopen(req, timeout=45).read()
