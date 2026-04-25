"""Batch 0226 ingest — drain V/S/B/F/T/N cache from batch 0225.

12 cached modern (>=2017) novel candidates remaining from batch 0225's
V/S/B/F/T/N alphabet probes. No fresh discovery fetches needed (cache reuse).

Priority picks (likely text-extractable, similar-shape to ones already ingested):
  1. 2022/25 Tourism Hotel Managers Disapplication 2022 — sis_tourism (parallel of 2020/123 ok in 0225)
  2. 2020/122 Tourism Licensing Disapplication 2020 — sis_tourism (parallel of 2022/26 ok in 0225)
  3. 2019/30 National Dialogue Forum (Extension) (No. 2) Order — sis_governance
  4. 2019/28 National Dialogue Forum (Extension) Order — sis_governance
  5. 2026/8 Fisheries (Management Area) (Declaration) Order — sis_fisheries (FIRST sis_fisheries record if ok)
  6. 2017/28 Dambwa Local Forest Alteration of Boundaries Order — sis_environment
  7. 2017/63 Local Forest No. 42: Kawena (Cessation) Order — sis_environment
  8. 2020/12 Local Forest No. P. 320: Mpande Hills (Alteration) — sis_environment
Reserves (idx 8+):
  9. 2020/13 National Forest No. F.12: Luano (Alteration of Boundaries) Order
 10. 2021/3  National Forest No. F31: Kabwe (Alteration of Boundaries) Order
 11. 2021/2  Kasama National Forest No. P.47: (Alteration of Boundaries) Order
 12. 2021/1  Forest Reserve No. 4: Maposa (Cessation) Order

Expected cohort: 5-8 records OK depending on Forest scanned-image rate.
"""
import sys, os, json, hashlib, time, urllib.request, re
from datetime import datetime, timezone
from bs4 import BeautifulSoup

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6.0
PARSER_VERSION = "0.5.0"

PICKS = [
    {'yr_num':'2022/25','year':'2022','num':'25','title':'Tourism and Hospitality (Registration of Hotel Managers) (Temporary Disapplication of Registration Fee) Regulations, 2022','sub_phase':'sis_tourism','parent_act':'Tourism and Hospitality Act'},
    {'yr_num':'2020/122','year':'2020','num':'122','title':'Tourism and Hospitality (Licensing) (Temporary Disapplication of Renewal and Retention Fee) Regulations, 2020','sub_phase':'sis_tourism','parent_act':'Tourism and Hospitality Act'},
    {'yr_num':'2019/30','year':'2019','num':'30','title':'National Dialogue Forum (Extension) (No. 2) Order, 2019','sub_phase':'sis_governance','parent_act':'National Dialogue (Constitution, Electoral Process, Public Order and Political Parties Acts) Act'},
    {'yr_num':'2019/28','year':'2019','num':'28','title':'National Dialogue Forum (Extension) Order, 2019','sub_phase':'sis_governance','parent_act':'National Dialogue (Constitution, Electoral Process, Public Order and Political Parties Acts) Act'},
    {'yr_num':'2026/8','year':'2026','num':'8','title':'Fisheries (Management Area) (Declaration) Order, 2025','sub_phase':'sis_fisheries','parent_act':'Fisheries Act'},
    {'yr_num':'2017/28','year':'2017','num':'28','title':'Dambwa Local Forest No. F22 (Alteration of Boundaries) Order, 2017','sub_phase':'sis_environment','parent_act':'Forests Act'},
    {'yr_num':'2017/63','year':'2017','num':'63','title':'Local Forest No. 42 Kawena (Cessation) Order, 2017','sub_phase':'sis_environment','parent_act':'Forests Act'},
    {'yr_num':'2020/12','year':'2020','num':'12','title':'Local Forest No. P. 320 Mpande Hills (Alteration of Boundaries) Order, 2020','sub_phase':'sis_environment','parent_act':'Forests Act'},
    # Reserves
    {'yr_num':'2020/13','year':'2020','num':'13','title':'National Forest No. F.12 Luano (Alteration of Boundaries) Order, 2020','sub_phase':'sis_environment','parent_act':'Forests Act'},
    {'yr_num':'2021/3','year':'2021','num':'3','title':'National Forest No. F31 Kabwe (Alteration of Boundaries) Order, 2021','sub_phase':'sis_environment','parent_act':'Forests Act'},
    {'yr_num':'2021/2','year':'2021','num':'2','title':'Kasama National Forest No. P. 47 (Alteration of Boundaries) Order, 2021','sub_phase':'sis_environment','parent_act':'Forests Act'},
    {'yr_num':'2021/1','year':'2021','num':'1','title':'Forest Reserve No. 4 Maposa (Cessation) Order, 2021','sub_phase':'sis_environment','parent_act':'Forests Act'},
]

def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+","-",s).strip('-')
    return s[:120]

def fetch(url, sleep=True):
    if sleep: time.sleep(CRAWL)
    req = urllib.request.Request(url, headers=HEADERS)
    return urllib.request.urlopen(req, timeout=45).read()
