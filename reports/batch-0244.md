# Phase 4 Batch 0244 - cache-drain residuals (sis_industry FIRST cluster)

**Date:** 2026-04-26 UTC
**Phase:** phase_4_bulk
**Strategy:** Pure cache-drain tick — drained 7 reserved residuals from
batch 0243 close-out plan (5 unused from year=2024 p3 cache + 2 unused
substitutes from year=2025 listing cache). Zero discovery probes this
tick — all candidates already discovered in prior probes.

## Records committed: 6

| Idx | ID                                                         | Yr/Num   | Sub-phase       | Parent Act                            | Pages | Chars  | Status |
|----:|------------------------------------------------------------|----------|-----------------|---------------------------------------|------:|-------:|:-------|
| 0   | si-zm-2021-035-citizens-economic-empowerment-...           | 2021/035 | sis_industry    | Citizens Economic Empowerment Act     | -     | -      | ok     |
| 1   | si-zm-2019-022-citizens-economic-empowerment-reservation-..| 2019/022 | sis_industry    | Citizens Economic Empowerment Act     | -     | -      | ok     |
| 2   | si-zm-2025-020-compulsory-standards-declaration-order-2025 | 2025/020 | sis_industry    | Compulsory Standards Act              | -     | -      | SKIP   |
| 3   | si-zm-2020-018-compulsory-standards-potable-spirits-...    | 2020/018 | sis_industry    | Compulsory Standards Act              | -     | -      | ok     |
| 4   | si-zm-2018-064-constitutional-offices-emoluments-...       | 2018/064 | sis_governance  | Constitutional Offices Emoluments Act | -     | -      | ok     |
| 5   | si-zm-1992-009-air-passenger-service-charge-charging-...   | 1992/009 | sis_transport   | Air Passenger Service Charge Act      | -     | -      | ok     |
| 6   | si-zm-1985-045-air-services-aerial-application-permit-...  | 1985/045 | sis_transport   | Aviation Act                          | -     | -      | ok     |

## Yield

- 6 ok / 7 attempted = **86%** yield
- 1 skip: 2025/020 Compulsory Standards (Declaration) Order 2025 — PDF
  88,559,047 bytes (88.5 MB) > 4.5 MB defensive cap. Raw HTML+PDF
  preserved at raw/zambialii/si/2025/ for OCR/split processing or
  raised cap retry. Largest oversized SI encountered to date in the
  corpus build.

## Sub-phase footprint

- **sis_industry FIRST cluster** in corpus (3 records, 4 attempted) —
  Citizens Economic Empowerment Act parent + Compulsory Standards Act
  parent: 2021/035 CEE Transport-Reservation + 2019/022 CEE Reservation
  Scheme + 2020/018 Compulsory Standards Potable Spirits + (skip
  2025/020 Compulsory Standards Declaration). **Priority_order item
  outside the named items 1–8** — opportunistic first-instance
  sub-phase win, second priority cluster advanced this week (after
  sis_corporate at batch 0243).
- **sis_governance +1** — 2018/064 Constitutional Offices Emoluments
  Regulations.
- **sis_transport +2** — 1992/009 Air Passenger Service Charge
  (Charging) Order + 1985/045 Air Services (Aerial Application Permit)
  Regulations. Extends 1985-2026 sis_transport coverage with two
  historic SIs.

## Cumulative SI records

- After batch 0244: **536** (+6 over batch 0243's 530)
- Judgments: 25 (paused per robots Disallow on /akn/zm/judgment/)

## Discovery cost

- 1 robots.txt re-verify (sha256 prefix `fce67b697ee4ef44` — unchanged
  from batches 0193-0243)
- 0 listing probes (pure cache-drain tick — used cached candidates from
  batch_0243 year=2024 p3 + batch_0242 year=2025)
- = **1 discovery fetch this tick**

## Per-record cost

- 6 records committed × 2 fetches (HTML+PDF) = 12 ingest fetches for ok
- 1 skip × 2 fetches (HTML+PDF preserved on disk for retry) = 2 fetches
- = **14 ingest fetches**

## Total tick fetches

- 1 robots + 14 ingest = **15 fetches** (today: 15/2000 = 0.75% of daily
  budget). Tokens within budget. All on zambialii.org under
  robots-declared 5s crawl-delay using 6s margin (CRAWL=6.0).

## Integrity checks

- CHECK1a batch unique ids: 6/6 PASS
- CHECK1b corpus presence on disk: 6/6 PASS
- CHECK2 amended_by unresolved: 0
- CHECK3 repealed_by unresolved: 0
- CHECK4 source_hash sha256 verified 6/6 against
  raw/zambialii/si/(1985,1992,2018,2019,2020,2021)/
- CHECK5 10×6 required fields all present
- CHECK6 cited_authorities unresolved: 0
- **ALL PASS**

## OCR / oversize backlog

- Now **12 items** (+1 this tick: 2025/020 Compulsory Standards
  Declaration Order, 88.5 MB).
- Full backlog: 2017/068 + 2018/011 + 2018/075 + 2018/093 + 2020/007 +
  2022/004 + 2022/007 + 2022/008 + 2022/012 + 2022/013 + 2025/020 +
  2026/004.

## Tick-start recovery

- HEAD aligned with origin/main via `git update-ref refs/heads/main
  origin/main` (origin had batch 0243 close-out commit a1dbf43 ahead of
  stale local HEAD 9caa3fa plus stale staged-deletion noise — workaround
  stable across batches 0192-0243).
- `index.lock`, `HEAD.lock`, and `objects/maintenance.lock` all present
  and unremovable per virtiofs unlink-failure pattern (Operation not
  permitted) — `GIT_INDEX_FILE` bypass used for staging.

## Next-tick plan

(a) Probe further year listings (year=2024 p4, year=2023 p2/p3,
    year=2022 deep) — likely productive given prior 13-novel yield
    on year=2024 p3.
(b) Probe alphabet letters not yet exhausted (only a few remain
    untested in the 2026-04-25 set).
(c) Rotate to `acts_in_force` priority_order item 1 — would require
    Acts-listing endpoint discovery (separate path from SI ingest).
(d) Continue priority_order item 2 (sis_corporate) drain — additional
    Companies Act SIs may exist on year=2024 deeper pages.
(e) OCR retry on backlog (12 items) once tesseract is wired.

## Infrastructure follow-up (non-blocking)

- batch-0244 raw files (~14 = 6 HTML + 6 PDF + 1 robots + 2 skip-preserved)
  plus accumulated batches 0192-0243 raw files awaiting host-driven B2
  sync (rclone unavailable in sandbox).
- corpus.sqlite stale rollback-journal still blocks in-sandbox FTS
  rebuild (JSON records authoritative; sqlite rebuild deferred to host).
- Persistent virtiofs unlink-failure warnings non-fatal (workaround
  stable across batches 0192-0244 — write-tree/commit-tree path
  bypasses lock).
