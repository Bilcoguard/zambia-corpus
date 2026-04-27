"""Batch 0292 - Phase 4 / sis_employment, sis_mining, sis_family probe sweep.

Inherited from b0291: sis_corporate-modern, sis_tax (text-extractable),
acts_in_force-chronological, case_law_scz, sis_data_protection all at upstream
steady state. Per priority_order, items 4 (sis_employment), 7 (sis_mining),
8 (sis_family) remain. b0291 probed alphabets A,B,C,I,M,P,S,T,V — leaving
the most-relevant employment/mining/family letters (E,L,N,W,J,F) uncovered
this batch cycle.

This tick probes 6 zambialii alphabets (E, F, J, L, N, W) for novel modern
(>=2017) SIs across the three remaining sub-phases. Picks (if any) are
filtered to titles matching:

  sis_employment -> Employment | Labour | NAPSA | National Pension Scheme |
                    Workers Compensation | Minimum Wage | Industrial
                    Relations | Factories | Apprenticeship
  sis_mining     -> Mines | Mineral | (any letter — M already covered b0291)
  sis_family     -> Marriage | Matrimonial | Children | Juvenile |
                    Maintenance | Adoption | Affiliation

Existing on-disk:
  sis_employment: 3 records (2023/48, 49, 50)
  sis_mining:     1 record  (2022/66)
  sis_family:     0 records

PARSER_VERSION: 0.5.0
USER_AGENT:    KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)
robots.txt sha256 (zambialii): fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0
Crawl-delay: 6s on zambialii (>= robots 5s)

PICKS are populated by the discovery probe in _work/batch_0292_discover.py.
If discovery yields no novel modern candidates, PICKS=[] and this tick is
probe-only.
"""
import os, sys, time, hashlib, urllib.request, re

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6  # 5s robots crawl-delay + 1s margin
PARSER_VERSION = "0.5.0"

# Discovery findings (see _work/batch_0292_probe.json):
#   In-priority candidates:
#     - 2022/13 [sis_employment] Minimum Wages and Conditions of Employment
#       (Truck and Bus Drivers) (Amendment) Order, 2022
#   Off-priority (reserved):
#     - 2026/4  Electricity (Transmission) (Grid Code) Regulations, 2026   [sis_energy]
#     - 2022/7  National Archives (Fees) Regulations, 2021                 [sis_archives]
#     - 2022/8  National Assembly By-Election (Kabwata) Order              [sis_elections]
#     - 2018/11 Forests (Community Forest Management) Regulations, 2018    [sis_forests]
#     - 2018/75 National Assembly By-Election (Mangango) Order             [sis_elections]
#     - 2018/93 National Assembly By-Election (Sesheke) Order              [sis_elections]
PICKS = [
    {"yr_num": "2022/13", "year": "2022", "num": "13",
     "title": "Minimum Wages and Conditions of Employment (Truck and Bus Drivers) (Amendment) Order, 2022",
     "eng_date": "2022-01-28",
     "parent_act": "Minimum Wages and Conditions of Employment Act",
     "sub_phase": "sis_employment"},
]

def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip('-')
    return s[:120]

def fetch(url, sleep=True):
    if sleep: time.sleep(CRAWL)
    req = urllib.request.Request(url, headers=HEADERS)
    return urllib.request.urlopen(req, timeout=45).read()
