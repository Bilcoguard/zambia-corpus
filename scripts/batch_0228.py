"""Batch 0228 ingest — drain the 7 L-alphabet residuals surfaced by batch 0227's
fresh L probe (no fresh discovery probe this tick — 0 discovery cost).

Picks (7):
  L-alphabet residuals, all sis_local_government (parent: Local Government Act
  except 2020/34 which is sis_governance):

    1. 2020/34  Laws of Zambia (Revised Edition) Act (Specified Date) Notice 2020
                — parent_act: Laws of Zambia (Revised Edition) Act; sub_phase: sis_governance
    2. 2022/71  Local Government (Appointment of Local Government Administrator)
                (Kafue Town Council) Order, 2022
    3. 2020/95  Local Government (Appointment of Local Government Administrator)
                (Kalumbila Town Council) Order, 2020
    4. 2020/67  Local Government (Appointment of Local Government Administrator)
                (Kitwe City Council) Order, 2020
    5. 2020/66  Local Government (Appointment of Local Government Administrator)
                (Lusaka City Council) Order, 2020
    6. 2019/77  Chembe Town Council (Sugar Cane Levy) By-laws, 2019
    7. 2019/47  Local Government (Fire Services) Order, 2019

Per worker.log close-out of batch 0227, the Appointment-of-LG-Administrator orders
(2022/71, 2020/95, 2020/67, 2020/66) are likely short scanned-image declarations
— expected yield 1-3 of 7. Honour MAX_BATCH_SIZE=8 cap (we attempt 7 < 8).

Per-record cost: 2 fetches (HTML + PDF) x 7 = 14. Plus 1 robots reverify already done.
"""
import sys, os, json, hashlib, time, urllib.request, re
from datetime import datetime, timezone
from bs4 import BeautifulSoup

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6.0
PARSER_VERSION = "0.5.0"

PICKS = [
    {'yr_num':'2020/34','year':'2020','num':'34',
     'title':'Laws of Zambia (Revised Edition) Act (Specified Date) Notice, 2020',
     'sub_phase':'sis_governance','parent_act':'Laws of Zambia (Revised Edition) Act'},
    {'yr_num':'2022/71','year':'2022','num':'71',
     'title':'Local Government (Appointment of Local Government Administrator) (Kafue Town Council) Order, 2022',
     'sub_phase':'sis_local_government','parent_act':'Local Government Act'},
    {'yr_num':'2020/95','year':'2020','num':'95',
     'title':'Local Government (Appointment of Local Government Administrator) (Kalumbila Town Council) Order, 2020',
     'sub_phase':'sis_local_government','parent_act':'Local Government Act'},
    {'yr_num':'2020/67','year':'2020','num':'67',
     'title':'Local Government (Appointment of Local Government Administrator) (Kitwe City Council) Order, 2020',
     'sub_phase':'sis_local_government','parent_act':'Local Government Act'},
    {'yr_num':'2020/66','year':'2020','num':'66',
     'title':'Local Government (Appointment of Local Government Administrator) (Lusaka City Council) Order, 2020',
     'sub_phase':'sis_local_government','parent_act':'Local Government Act'},
    {'yr_num':'2019/77','year':'2019','num':'77',
     'title':'Chembe Town Council (Sugar Cane Levy) By-laws, 2019',
     'sub_phase':'sis_local_government','parent_act':'Local Government Act'},
    {'yr_num':'2019/47','year':'2019','num':'47',
     'title':'Local Government (Fire Services) Order, 2019',
     'sub_phase':'sis_local_government','parent_act':'Local Government Act'},
]

def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+","-",s).strip('-')
    return s[:120]

def fetch(url, sleep=True):
    if sleep: time.sleep(CRAWL)
    req = urllib.request.Request(url, headers=HEADERS)
    return urllib.request.urlopen(req, timeout=45).read()
