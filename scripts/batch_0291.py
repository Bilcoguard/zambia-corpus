"""Batch 0291 - Phase 4 / sis_tax sub-phase advance after sis_corporate
modern-era exhaustion.

Inherited from b0290: acts_in_force chronological-first sweep at upstream
steady state through 2026/11. Per priority_order in approvals.yaml:
  acts_in_force -> sis_corporate -> sis_tax -> sis_employment -> ...

This tick probes 9 zambialii alphabets (A,B,C,I,M,P,S,T,V) for modern
(>=2017) novel SIs. Findings:

  alphabet=A: 12 modern, 0 novel
  alphabet=B: 1 modern, 0 novel
  alphabet=C: 18 modern, 1 novel  (2025/20 Compulsory Standards - sis_industry)
  alphabet=I: 31 modern, 2 novel  (2017/43, 2019/25 Income Tax - sis_tax)
  alphabet=M: 10 modern, 0 novel
  alphabet=P: 9 modern, 0 novel
  alphabet=S: 9 modern, 2 novel   (2022/12 Societies - sis_governance;
                                   2017/68 Standards - sis_industry)
  alphabet=T: 12 modern, 0 novel
  alphabet=V: 7 modern, 1 novel   (2022/4 VAT - sis_tax)

CONCLUSION
  sis_corporate (priority_order item 2) -- ZERO novel modern SIs upstream
  across all 9 corporate-relevant alphabets (Companies/Banking/Co-op/
  Citizens-Economic-Empowerment, Insurance, Pensions, Securities). The
  modern era of sis_corporate is at upstream steady state.

  sis_tax (priority_order item 3) -- 3 novel modern SIs upstream:
    - 2017/43 Income Tax (Suspension of Tax on Payments to
                          Non-Resident Contractors)(Batoka Hydro-Electric
                          Scheme) Regulations
    - 2019/25 Income Tax Act (Suspension of tax on payment of interest
                              to non-resident)(Treasury Bill and Bond)
                              Regulations
    - 2022/4  Value Added Tax (Zero-Rating)(Amendment) Order, 2022

PICKS this tick: 3 sis_tax SIs. Below MAX_BATCH_SIZE=8 — full sweep of
the available modern novel sis_tax pool.

Two further candidates (2025/20 Compulsory Standards, 2017/68 Standards
Compulsory Standards Declaration) are sis_industry — not in priority_order
but already represented in corpus (3 records). Reserved for future tick if
sis_industry is added to priority_order; otherwise listed in the report.
2022/12 Societies (Amendment) Rules is sis_governance — reserved similarly.

PARSER_VERSION: 0.5.0 (matches batches 0241+)
USER_AGENT:    KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)
robots.txt sha256 (zambialii): fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0
Crawl-delay: 6s on zambialii (>= robots 5s)
"""
import os, sys, time, hashlib, urllib.request, re

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6  # 5s robots crawl-delay + 1s margin
PARSER_VERSION = "0.5.0"

PICKS = [
    {"yr_num":"2017/43","year":"2017","num":"43",
     "title":"Income Tax (Suspension of Tax on Payments to Non-Resident Contractors) (Batoka Hydro-Electric Scheme) Regulations, 2017",
     "eng_date":"2017-06-16",
     "parent_act":"Income Tax Act",
     "sub_phase":"sis_tax"},
    {"yr_num":"2019/25","year":"2019","num":"25",
     "title":"Income Tax Act (Suspension of tax on payment of interest to non-resident) (Treasury Bill and Bond) Regulations, 2019",
     "eng_date":"2019-03-22",
     "parent_act":"Income Tax Act",
     "sub_phase":"sis_tax"},
    {"yr_num":"2022/4","year":"2022","num":"4",
     "title":"Value Added Tax (Zero-Rating) (Amendment) Order, 2022",
     "eng_date":"2022-01-11",
     "parent_act":"Value Added Tax Act",
     "sub_phase":"sis_tax"},
]

def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+","-",s).strip('-')
    return s[:120]

def fetch(url, sleep=True):
    if sleep: time.sleep(CRAWL)
    req = urllib.request.Request(url, headers=HEADERS)
    return urllib.request.urlopen(req, timeout=45).read()
