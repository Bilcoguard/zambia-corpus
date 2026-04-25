# Batch 0238 Report

**Phase:** 4 — bulk ingest (sis_elections E-residual drain cohort 4)
**Tick start:** ~2026-04-25T21:05Z (this run)
**Generated:** 2026-04-25T21:11:11Z

## Summary

- Attempted: 9
- OK: 8
- Fail: 1
- Yield: 8/9 = 88%
- Cumulative SI records (post-batch): 490 (+8 over batch 0237's 482)

## Records (OK)

- **2017/18** — Local Government By-Elections (Election Dates and Times of Poll) Order, 2017
  - id: `si-zm-2017-018-local-government-by-elections-election-dates-and-times-of-poll-order-2017`
  - effective_date: 2017-02-24
  - pdf_pages: 2, pdf_text_chars: 1849
  - source_hash: `c4d6a5bbba7dc0e3…`
  - source_url: https://zambialii.org/akn/zm/act/si/2017/18

- **2017/54** — Electoral Process (Local Government By-Elections) (Election Date and Times of Poll) Order,
  - id: `si-zm-2017-054-electoral-process-local-government-by-elections-election-date-and-times-of-poll-order-2017`
  - effective_date: 2017-07-14
  - pdf_pages: 2, pdf_text_chars: 2016
  - source_hash: `2bc24337fbe299eb…`
  - source_url: https://zambialii.org/akn/zm/act/si/2017/54

- **2018/21** — Electoral Process (Local Government By-Election) (Election Date and Time of Poll) Order, 2
  - id: `si-zm-2018-021-electoral-process-local-government-by-election-election-date-and-time-of-poll-order-2018`
  - effective_date: 2018-03-23
  - pdf_pages: 2, pdf_text_chars: 2129
  - source_hash: `840bafd4b6b51588…`
  - source_url: https://zambialii.org/akn/zm/act/si/2018/21

- **2018/33** — Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) Order, 
  - id: `si-zm-2018-033-electoral-process-local-government-by-elections-election-date-and-time-of-poll-order-2018`
  - effective_date: 2018-04-20
  - pdf_pages: 2, pdf_text_chars: 1741
  - source_hash: `994fb2fd033b617e…`
  - source_url: https://zambialii.org/akn/zm/act/si/2018/33

- **2018/46** — Electoral Process (Local Government By Elections) (Election Date and Time of Poll) (No. 3)
  - id: `si-zm-2018-046-electoral-process-local-government-by-elections-election-date-and-time-of-poll-no-3-order-2018`
  - effective_date: 2018-06-15
  - pdf_pages: 2, pdf_text_chars: 1857
  - source_hash: `0ce248eafcda7622…`
  - source_url: https://zambialii.org/akn/zm/act/si/2018/46

- **2018/56** — National Assembly By-Election (Kasenengwa Constituency No. 41) (Election Date and Time of 
  - id: `si-zm-2018-056-national-assembly-by-election-kasenengwa-constituency-no-41-election-date-and-time-of-poll-no-2-order-2018`
  - effective_date: 2018-08-03
  - pdf_pages: 4, pdf_text_chars: 3819
  - source_hash: `d405f9242b908eee…`
  - source_url: https://zambialii.org/akn/zm/act/si/2018/56

- **2018/57** — Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) (No. 4)
  - id: `si-zm-2018-057-electoral-process-local-government-by-elections-election-date-and-time-of-poll-no-4-order-2018`
  - effective_date: 2018-08-03
  - pdf_pages: 4, pdf_text_chars: 3819
  - source_hash: `d405f9242b908eee…`
  - source_url: https://zambialii.org/akn/zm/act/si/2018/57

- **2018/81** — Electoral Process (Local Governments By-Elections) (Election Date and Time of Poll) (No. 6
  - id: `si-zm-2018-081-electoral-process-local-governments-by-elections-election-date-and-time-of-poll-no-6-order-2018`
  - effective_date: 2018-10-19
  - pdf_pages: 2, pdf_text_chars: 1890
  - source_hash: `84b377dfaef35030…`
  - source_url: https://zambialii.org/akn/zm/act/si/2018/81

## Failures

- **2018/75** — National Assembly By-Election (Mangango Constituency No. 141) (Election Date and: `pdf_parse_empty` (raw HTML+PDF preserved on disk for OCR retry)

## Discovery

- 1 robots.txt re-verify (sha256 prefix `fce67b697ee4ef44` unchanged from batches 0193-0237)
- 0 fresh alphabet probes (drain mode against batch_0233 E-probe cache)
- E-residuals before tick: 31; after tick (8 ingested + 1 fail): ~22 left

## Sub-phase footprint

- sis_elections +8 (drain only — no first-instance sub-phases)

## Integrity

ALL PASS — 8 records:
- CHECK1a_unique: True
- CHECK1b_on_disk: True
- CHECK2_amended_by: True
- CHECK3_repealed_by: True
- CHECK4_sha256_match: True
- CHECK5_required_fields: True
- CHECK6_cited_authorities: True
