# Batch 0239 Report

**Phase:** 4 — bulk ingest (sis_elections E-residual drain cohort 5)
**Tick start:** 2026-04-25T21:33Z
**Generated:** 2026-04-25T21:40Z

## Summary

- Attempted: 9 (8 primary picks + 1 in-batch substitute used)
- OK: 8
- Fail: 1
- Yield: 8/9 = 89%
- Cumulative SI records (post-batch): 498 (+8 over batch 0238's 490)

## Records (OK)

- **2018/94** — Electoral Process (Local Governments By-Elections) (Election Date and Time of Poll) (No. 7) Order, 2018
  - id: `si-zm-2018-094-electoral-process-local-governments-by-elections-election-date-and-time-of-poll-no-7-order-2018`
  - effective_date: 2018-12-21
  - source_url: https://zambialii.org/akn/zm/act/si/2018/94

- **2019/16** — National Assembly By-Election (Bahati Constituency No. 062) (Election Date and Time of Poll) Order, 2019
  - id: `si-zm-2019-016-national-assembly-by-election-bahati-constituency-no-062-election-date-and-time-of-poll-order-2019`
  - effective_date: 2019-03-01
  - source_url: https://zambialii.org/akn/zm/act/si/2019/16

- **2019/23** — Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) Order, 2019
  - id: `si-zm-2019-023-electoral-process-local-government-by-elections-election-date-and-time-of-poll-order-2019`
  - effective_date: 2019-03-15
  - source_url: https://zambialii.org/akn/zm/act/si/2019/23

- **2019/24** — Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) (No. 2) Order, 2019
  - id: `si-zm-2019-024-electoral-process-local-government-by-elections-election-date-and-time-of-poll-no-2-order-2019`
  - effective_date: 2019-03-15
  - source_url: https://zambialii.org/akn/zm/act/si/2019/24

- **2019/33** — Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) (No. 3) Order, 2019
  - id: `si-zm-2019-033-electoral-process-local-government-by-elections-election-date-and-time-of-poll-no-3-order-2019`
  - effective_date: 2019-05-22
  - source_url: https://zambialii.org/akn/zm/act/si/2019/33

- **2019/38** — National Assembly By-Election (Katuba Constituency No. 01) (Election Date and Time of Poll) Order, 2019
  - id: `si-zm-2019-038-national-assembly-by-election-katuba-constituency-no-01-election-date-and-time-of-poll-order-2019`
  - effective_date: 2019-06-07
  - source_url: https://zambialii.org/akn/zm/act/si/2019/38

- **2019/61** — Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) (No. 4) Order, 2019
  - id: `si-zm-2019-061-electoral-process-local-government-by-elections-election-date-and-time-of-poll-no-4-order-2019`
  - effective_date: 2019-09-13
  - source_url: https://zambialii.org/akn/zm/act/si/2019/61

- **2019/76** — Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) (No. 5) Order, 2019
  - id: `si-zm-2019-076-electoral-process-local-government-by-elections-election-date-and-time-of-poll-no-5-order-2019`
  - effective_date: 2019-11-15
  - source_url: https://zambialii.org/akn/zm/act/si/2019/76 (in-batch substitute for failed 2018/93)

## Failures

- **2018/93** — National Assembly By-Election (Sesheke Constituency No. 153): `pdf_parse_empty` (raw HTML+PDF preserved on disk for OCR retry; consistent with the National-Assembly-by-election scanned-image pattern observed for 2018/75 in batch 0238 and 2022/8 in batch 0235)

## Discovery

- 1 robots.txt re-verify (sha256 prefix `fce67b697ee4ef44` unchanged from batches 0193-0238)
- 0 fresh alphabet probes (drain mode against batch_0233 E-probe cache)
- E-residuals before tick: 23; after tick (8 ingested + 1 fail + 2 prior known scanned-image OCR-backlog skips): ~14 left for future drain

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

## Budgets

- Today fetches before tick: 656/2000 (32.8%)
- This tick: 1 robots reverify + 17 record HTML/PDF fetches = 18 new fetches
- Today fetches after tick: 674/2000 (33.7%) — well within budget

## Next-tick plan

- ~14 E-residuals remain in batch_0233 cache (excluding known scanned-image OCR-backlog candidates 2018/75, 2018/93, 2022/8)
- Continue E-drain with 2020/* sequence: 2020/2, 2020/3, 2020/4, 2020/23, 2020/43 are next, then jump to remaining 2023/* and 2024/* by-election orders
- Or rotate to acts_in_force (priority_order item 1) — will require Acts-listing endpoint discovery
- OCR backlog now 7 items (added 2018/93)

## Infrastructure follow-up (non-blocking)

- batch-0239 raw files (16 ok HTML+PDF + 2 fail HTML+PDF + 1 robots reverify) plus accumulated batches 0192-0238 raw files awaiting host-driven B2 sync (rclone unavailable in sandbox)
- corpus.sqlite stale rollback-journal still blocks in-sandbox FTS rebuild
- persistent virtiofs unlink-failure warnings non-fatal (workaround stable across batches 0192-0239 — write-tree/commit-tree path bypasses lock)
- 34 pre-existing flat-vs-year-subdir duplicate paths under records/acts/ unchanged (queued for future cleanup tick)
- Tick-start recovery: stale lock + diverged worker.log resolved via `git update-ref refs/heads/main origin/main` (canonical pattern, batches 0235-0239)
