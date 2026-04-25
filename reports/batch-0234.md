# Batch 0234 — Phase 4 (acts_in_force / sis_*)

**Tick start:** 2026-04-25T19:04:12Z
**Tick end:**   2026-04-25T19:09:34Z

## Plan
Drain A-alphabet residuals from batch 0232's M/A/D probe (7 left, all
sis_agriculture under Animal Health / Animal Identification & Traceability
Acts) plus 1 cheap declaration order from E-alphabet residuals from batch
0233's E probe to fill the batch to MAX_BATCH_SIZE=8.

Discovery cost: 0 fresh probes + 1 robots.txt re-verify = 1 discovery
fetch. Per-record fetches: 8 × 2 (HTML + PDF) = 16 fresh ingest fetches.

## Discovery / Compliance
robots.txt re-verified 2026-04-25T19:04:12Z — sha256
`fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0`
prefix `fce67b697ee4ef44` unchanged from batches 0193–0233.
Crawl-delay 5s honoured at 6s margin. Disallow on `/akn/zm/judgment/` +
`/akn/zm/officialGazette/` enforced (no judgment fetches this tick).

## Picks (8) — all sourced from prior-tick discovery caches; no fresh probes

| # | id (yr/num) | sub_phase | parent_act | pages | chars |
|---|-------------|-----------|------------|------:|------:|
| 1 | 2020/84 | sis_agriculture | Animal Identification and Traceability Act | 22 | 23,138 |
| 2 | 2020/85 | sis_agriculture | Animal Health Act | 2 | 1,903 |
| 3 | 2020/86 | sis_agriculture | Animal Health Act | 2 | 1,283 |
| 4 | 2020/87 | sis_agriculture | Animal Health Act | 2 | 1,503 |
| 5 | 2020/93 | sis_agriculture | Animal Health Act | 20 | 23,310 |
| 6 | 2020/94 | sis_agriculture | Animal Health Act | 24 | 26,826 |
| 7 | 2021/25 | sis_agriculture | Animal Health Act | 4 | 4,274 |
| 8 | 2021/7  | sis_elections   | Electoral Process Act | 2 | 1,933 |

## Sub-phase footprint
- sis_agriculture +7 (Animal Health / Animal Identification cluster — drains
  all 7 A-residuals from batch 0232's probe).
- sis_elections +1 (drains 1 of 56 E-residuals from batch 0233's E probe —
  small Local Government By-Elections declaration order, 2021/01/29).

No new first-instance sub-phases this tick (sis_agriculture and
sis_elections both already established in prior batches).

## Yield
8 ok / 8 attempted = **100%** — 11th-consecutive 100%-yield batch (extends
streak across 0223/0224/0226/0227/0228/0229/0230/0231/0232/0233/0234; 0225
was 73% due to scanned-image cohort). 0% scanned-image rate this tick.

## Per-record cost
- 1 robots reverify (cumulative `fetch_n` 572)
- 15 ingest fetches (1 HTML reused from in-flight earlier subprocess
  attempt for idx 2 = 2020/86 — sha verified): cumulative `fetch_n` 587
- Today fetches: 587 / 2000 (29.35%) — well under daily budget
- Tokens within budget

## Integrity (CHECK1a–CHECK6) — ALL PASS
- CHECK1a: 8 / 8 unique batch IDs
- CHECK1b: 8 / 8 records present on disk under `records/sis/{year}/{id}.json`
- CHECK2:  0 unresolved `amended_by` refs (all empty as expected)
- CHECK3:  0 unresolved `repealed_by` refs (all empty as expected)
- CHECK4:  8 / 8 source_hash sha256 verified against
  `raw/zambialii/si/(2020,2021)/`
- CHECK5:  10 × 8 required fields present (id, type, jurisdiction, year,
  number, title, source_url, source_hash, fetched_at, parser_version)
- CHECK6:  0 unresolved `cited_authorities` refs (all empty as expected)

## Cap honour
8 records committed (= MAX_BATCH_SIZE 8 cap).

## Next-tick plan
- (a) Continue alphabet re-probes — G / H / K / P (haven't been re-probed
      since earlier ticks — likely-fertile per E's 64-novel result and M's
      0-novel drain)
- (b) Drain E residuals — 55 left after this tick (bulk Electoral Process
      by-elections cohort + Employment Code amendments + Energy/Electricity)
- (c) Rotate to acts_in_force priority_order item 1 (requires Acts-listing
      endpoint discovery — separate path from SI ingest)
- (d) OCR backlog from batches 0225/0226 (5 items: 2017/068, 2018/011,
      2022/004, 2022/007, 2022/012)
- (e) Records reconciliation tick (488+ pre-existing untracked records
      files on disk)
- (f) Future-tick: raise cap or chunk-fetch for 2026/4 28 MB grid code
      (substantive, currently substituted away in batch 0233)

## Infrastructure follow-up (non-blocking)
- batch-0234 raw files (~17 = 8 HTML + 7 fresh PDF + 1 reused HTML +
  1 robots reverify, ~580 KB total) plus accumulated batches 0192–0233
  raw files awaiting host-driven B2 sync (rclone unavailable in sandbox)
- corpus.sqlite stale rollback-journal still blocks in-sandbox FTS rebuild
  (insert error: 'disk I/O error' — JSON records authoritative; sqlite
  rebuild deferred to host)
- persistent virtiofs unlink-failure warnings non-fatal (workaround stable
  across batches 0192–0234 — write-tree/commit-tree path bypasses lock)
- 34 pre-existing flat-vs-year-subdir duplicate paths under `records/acts/`
  unchanged from prior ticks (queued for future cleanup tick)
- 488+ pre-existing untracked records/sis + records/acts files on disk
  unchanged this tick (queued for future reconciliation tick)
- OCR backlog at 5 items (carryover from batches 0225/0226)
