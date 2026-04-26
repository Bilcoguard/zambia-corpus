"""Phase 4 batch 0245 - drain 8 novel SIs from year=2022 p1 listing.

Discovery (this tick): year=2024 p4 + year=2023 p2/p3 = 404 (exhausted);
year=2022 p1 = 18 novel candidates. Picked 8 for batch 0245.

Picks (8, sub-phase priorities advancing acts_in_force item 3 (sis_tax)
and item 4 (sis_employment) and item 7 (sis_mining)):
  1. 2022/2  Customs and Excise (Suspension) (Fuel) Regulations, 2022 [sis_tax]
  2. 2022/4  Value Added Tax (Zero-Rating) (Amendment) Order, 2022 [sis_tax]
  3. 2022/7  National Archives (Fees) Regulations, 2021 [sis_governance]
  4. 2022/12 Societies (Amendment) Rules, 2021 [sis_governance]
  5. 2022/13 Minimum Wages and Conditions of Employment (Truck and Bus Drivers)
            (Amendment) Order, 2022 [sis_employment FIRST]
  6. 2022/56 Zambia Development Agency (Kalumbila Multi Facility Economic Zone)
            (Declaration) Order, 2022 [sis_industry]
  7. 2022/65 Public Protector Rules, 2022 [sis_governance]
  8. 2022/66 Customs and Excise (Suspension) (Manganese Ores and Concentrates)
            Regulations, 2022 [sis_mining FIRST]

Sub-phase footprint: sis_tax FIRST cluster +2 (Customs and Excise + VAT —
priority_order item 3 advanced); sis_employment FIRST +1 (Minimum Wages Act —
priority_order item 4 advanced); sis_mining FIRST +1 (Customs and Excise on
Manganese Ores — priority_order item 7 advanced); sis_governance +3 (National
Archives, Societies, Public Protector); sis_industry +1 (Zambia Development
Agency Act).

Per-record cost: 2 fetches (HTML+PDF) x 8 picks = 16 fresh ingest fetches.
Plus 1 robots reverify + 4 listing probes (year=2024 p4 = 404, year=2023 p2 =
404, year=2023 p3 = 404, year=2022 p1 = 18 novel) = 21 total tick fetches.
"""
import sys, os, json, hashlib, time, urllib.request, re
from datetime import datetime, timezone
from bs4 import BeautifulSoup

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6.0
PARSER_VERSION = "0.5.0"

PICKS = [
    {'yr_num':'2022/2','year':'2022','num':'2',
     'title':'Customs and Excise (Suspension) (Fuel) Regulations, 2022',
     'sub_phase':'sis_tax','parent_act':'Customs and Excise Act'},
    {'yr_num':'2022/4','year':'2022','num':'4',
     'title':'Value Added Tax (Zero-Rating) (Amendment) Order, 2022',
     'sub_phase':'sis_tax','parent_act':'Value Added Tax Act'},
    {'yr_num':'2022/7','year':'2022','num':'7',
     'title':'National Archives (Fees) Regulations, 2021',
     'sub_phase':'sis_governance','parent_act':'National Archives Act'},
    {'yr_num':'2022/12','year':'2022','num':'12',
     'title':'Societies (Amendment) Rules, 2021',
     'sub_phase':'sis_governance','parent_act':'Societies Act'},
    {'yr_num':'2022/13','year':'2022','num':'13',
     'title':'Minimum Wages and Conditions of Employment (Truck and Bus Drivers) (Amendment) Order, 2022',
     'sub_phase':'sis_employment','parent_act':'Minimum Wages and Conditions of Employment Act'},
    {'yr_num':'2022/56','year':'2022','num':'56',
     'title':'Zambia Development Agency (Kalumbila Multi Facility Economic Zone) (Declaration) Order, 2022',
     'sub_phase':'sis_industry','parent_act':'Zambia Development Agency Act'},
    {'yr_num':'2022/65','year':'2022','num':'65',
     'title':'Public Protector Rules, 2022',
     'sub_phase':'sis_governance','parent_act':'Public Protector Act'},
    {'yr_num':'2022/66','year':'2022','num':'66',
     'title':'Customs and Excise (Suspension) (Manganese Ores and Concentrates) Regulations, 2022',
     'sub_phase':'sis_mining','parent_act':'Customs and Excise Act'},
]

def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+","-",s).strip('-')
    return s[:120]

def fetch(url, sleep=True):
    if sleep: time.sleep(CRAWL)
    req = urllib.request.Request(url, headers=HEADERS)
    return urllib.request.urlopen(req, timeout=45).read()
