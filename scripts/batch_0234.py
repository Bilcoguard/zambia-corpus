"""Batch 0234 ingest — drain A-alphabet residuals from batch 0232 probe + 1
E-alphabet residual from batch 0233 probe.

Per close-out plan from batch 0233, this tick drains A residuals (7 left
from batch 0232 probe: 2020/84+85+86+87+93+94 + 2021/25 — Animal
Health/Animal Identification cohort, sis_agriculture) and picks 1 cheap
declaration order from E residuals (sis_elections by-elections cohort) to
fill batch to MAX_BATCH_SIZE=8.

Discovery cost this tick: 1 robots reverify + 0 fresh alphabet probes = 1
discovery fetch. Per-record fetches: 8 picks x 2 (HTML+PDF) = 16 fresh
ingest fetches. Total tick fetches: 17.

Picks (8 — MAX_BATCH_SIZE cap):
    1. 2020/84  Animal Identification (General) Regulations, 2020
                (sis_agriculture — Animal Identification & Traceability Act)
    2. 2020/85  Animal Health (Tsetse Fly Area and Tsetse Fly Control Area)
                (Declaration) Notice, 2020 (sis_agriculture — Animal Health Act)
    3. 2020/86  Animal Health (Establishment of Tsetse Control Pickets and
                Check Points) Regulations, 2020 (sis_agriculture — AHA)
    4. 2020/87  Animal Health (Designated Border Inspection Posts)
                Regulations, 2020 (sis_agriculture — AHA)
    5. 2020/93  Animal Health (Import and Export of Animal, Animal Product,
                Animal By-Product or Article) Regulations, 2020 (sis_agriculture)
    6. 2020/94  Animal Health (Bee Keeping) Regulations, 2020 (sis_agriculture)
    7. 2021/25  Animal Health (Destruction of Pigs) (Compensation) Order, 2021
                (sis_agriculture — AHA)
    8. 2021/7   Electoral Process (Local Government By-Elections) (Election
                Time and Time of Poll) Order, 2021 (sis_elections — drain E)

Sub-phase footprint: sis_agriculture +7 (Animal Health/Animal Identification
cluster — extends sis_agriculture which is now well-established) +
sis_elections +1 (drains E residual cohort by 1).
"""
import sys, os, json, hashlib, time, urllib.request, re
from datetime import datetime, timezone
from bs4 import BeautifulSoup

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6.0
PARSER_VERSION = "0.5.0"

PICKS = [
    {'yr_num':'2020/84','year':'2020','num':'84',
     'title':'Animal Identification (General) Regulations, 2020',
     'sub_phase':'sis_agriculture','parent_act':'Animal Identification and Traceability Act',
     'eng_date':'2020-10-30'},
    {'yr_num':'2020/85','year':'2020','num':'85',
     'title':'Animal Health (Tsetse Fly Area and Tsetse Fly Control Area) (Declaration) Notice, 2020',
     'sub_phase':'sis_agriculture','parent_act':'Animal Health Act',
     'eng_date':'2020-10-30'},
    {'yr_num':'2020/86','year':'2020','num':'86',
     'title':'Animal Health (Establishment of Tsetse Control Pickets and Check Points) Regulations, 2020',
     'sub_phase':'sis_agriculture','parent_act':'Animal Health Act',
     'eng_date':'2020-10-27'},
    {'yr_num':'2020/87','year':'2020','num':'87',
     'title':'Animal Health (Designated Border Inspection Posts) Regulations, 2020',
     'sub_phase':'sis_agriculture','parent_act':'Animal Health Act',
     'eng_date':'2020-10-27'},
    {'yr_num':'2020/93','year':'2020','num':'93',
     'title':'Animal Health (Import and Export of Animal, Animal Product, Animal By-Product or Article) Regulations, 2020',
     'sub_phase':'sis_agriculture','parent_act':'Animal Health Act',
     'eng_date':'2020-11-13'},
    {'yr_num':'2020/94','year':'2020','num':'94',
     'title':'Animal Health (Bee Keeping) Regulations, 2020',
     'sub_phase':'sis_agriculture','parent_act':'Animal Health Act',
     'eng_date':'2020-11-13'},
    {'yr_num':'2021/25','year':'2021','num':'25',
     'title':'Animal Health (Destruction of Pigs) (Compensation) Order, 2021',
     'sub_phase':'sis_agriculture','parent_act':'Animal Health Act',
     'eng_date':'2021-04-16'},
    {'yr_num':'2021/7','year':'2021','num':'7',
     'title':'Electoral Process (Local Government By-Elections) (Election Time and Time of Poll) Order, 2021',
     'sub_phase':'sis_elections','parent_act':'Electoral Process Act',
     'eng_date':'2021-01-29'},
]

def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+","-",s).strip('-')
    return s[:120]

def fetch(url, sleep=True):
    if sleep: time.sleep(CRAWL)
    req = urllib.request.Request(url, headers=HEADERS)
    return urllib.request.urlopen(req, timeout=45).read()
