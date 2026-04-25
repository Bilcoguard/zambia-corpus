# Batch 0235 Report

**Phase:** 4 (bulk ingest, approved+incomplete)
**Tick start:** 2026-04-25T19:34Z
**Tick end:** 2026-04-25T19:48Z (approx)
**Strategy:** Continue draining E-alphabet residuals from batch 0233 probe (55 remaining at tick start, 8 picked here, 1 substitution — see below). 0 fresh discovery fetches required (cache reuse from 0233).

## Records ingested (8 — MAX_BATCH_SIZE cap)

| # | yr/num | sub_phase | parent_act | pages | chars |
|---|--------|-----------|------------|-------|-------|
| 1 | 2022/64 | sis_elections | Electoral Process Act | 2 | 2133 |
| 2 | 2022/21 | sis_elections | Electoral Process Act | 2 | 1974 |
| 3 | 2022/38 | sis_elections | Electoral Process Act | 2 | 1786 |
| 4 | 2021/67 | sis_elections | Electoral Process Act | 2 | 3111 |
| 5 | 2022/51 | sis_elections | Electoral Process Act | 2 | 1739 |
| 6 | 2021/68 | sis_elections | Electoral Process Act | 2 | 1930 |
| 7 | 2022/63 | sis_elections | Electoral Process Act | 2 | 1908 |
| 8 | 2021/88 | sis_elections | Electoral Process Act | 2 | 1840 |

All 8 records are sis_elections short Election-Date-and-Time-of-Poll declaration orders (2pp, ~2KB each).

## Substitution within batch

- **Pick 0 (2022/8 Kabwata Constituency No. 77 By-Election Order, 2022)** — failed `pdf_parse_empty`. PDF fetched cleanly but pdfplumber returned 0 chars across all pages, indicating scanned-image PDF (not text-extractable without OCR). Raw HTML+PDF preserved on disk for OCR retry. Logged to gaps.md and OCR backlog (now 6 items: 2017/068, 2018/011, 2022/004, 2022/007, 2022/012, **2022/008**).
- **Replaced with 2021/88 Local Government By-Elections (No. 4) Order, 2021** — parsed cleanly (2pp, 1840 chars).

## Sub-phase footprint

- sis_elections +8 — extends established sub-phase from batch 0233 (first-instance 2021/40+57+2022/18) and 0234 (drain 2021/7).
- 0 first-instance sub-phases this tick.
- 0 priority_order items advanced this tick (sis_elections is not in approvals.yaml priority_order list — but it is a valid sub_phase category for SI ingest under phase_4_bulk).

## Discovery cost

- 1 robots.txt re-verification (sha256 prefix `fce67b697ee4ef44` unchanged from batches 0193-0234)
- 0 fresh alphabet probes (using batch 0233 E-probe cache)

## Per-record fetches

- 9 picks × 2 (HTML+PDF) = 18 fetches attempted
- 17 actual (1 fewer because pick 0 PDF was 4-page scanned image fetched once successfully)
- Today's total: 605/2000 (30.25%) — well within budget

## Integrity check (ALL PASS)

| Check | Status | Detail |
|-------|--------|--------|
| CHECK1a (batch unique IDs) | PASS | 8/8 unique |
| CHECK1b (corpus presence on disk) | PASS | 8/8 present |
| CHECK2 (amended_by refs) | PASS | 0 refs |
| CHECK3 (repealed_by refs) | PASS | 0 refs |
| CHECK4 (source_hash sha256) | PASS | 8/8 verified against raw/zambialii/si/(2021,2022)/ |
| CHECK5 (required fields 10×8) | PASS | all present |
| CHECK6 (cited_authorities refs) | PASS | 0 refs |

## Robots compliance

- robots.txt sha256 prefix: `fce67b697ee4ef44` (unchanged from batches 0193-0234)
- Crawl-delay: 5s declared, observed at 6s margin (CRAWL=6.0)
- Disallow rules honoured: /akn/zm/judgment/ + /akn/zm/officialGazette/ — no judgment URLs in this batch

## Yield

- 8 ok / 9 attempted = **88.89%** (the 11-batch streak of 100% yields ends here due to one scanned-image substitution; strict yield 8/8 ok-on-first-attempt for the picks committed)

## Cumulative

- SI records after this batch: **466** (+8 over batch 0234's 458)
- Judgments: 25 (paused per robots Disallow on /akn/zm/judgment/)

## Next-tick plan

- (a) Continue draining E residuals (~47 left after this tick — bulk Electoral Process by-elections cohort)
- (b) Fresh alphabet re-probes G/H/K/P (likely fertile per E's 64-novel result)
- (c) Drain A residuals (0 remaining after batch 0234)
- (d) Rotate to acts_in_force (priority_order item 1) — requires Acts-listing endpoint discovery
- (e) OCR backlog (6 items)
- (f) Records reconciliation (488+ pre-existing untracked records files)
- (g) 2026/4 cap-raise / chunk-fetch for 28MB grid code (substantive)

## Infrastructure follow-up (non-blocking)

- batch-0235 raw files (~17 = 8 HTML + 8 PDF + 1 fail HTML + 1 fail PDF + 1 robots ~700 KB total) plus accumulated batches 0192-0234 raw files awaiting host-driven B2 sync (rclone unavailable in sandbox)
- corpus.sqlite stale rollback-journal still blocks in-sandbox FTS rebuild — JSON records authoritative; sqlite rebuild deferred to host
- Persistent virtiofs unlink-failure warnings non-fatal (workaround stable across batches 0192-0235 — write-tree/commit-tree path bypasses lock)
- 34 pre-existing flat-vs-year-subdir duplicate paths under records/acts/ unchanged
- 488+ pre-existing untracked records/sis + records/acts files unchanged
- OCR backlog: 6 items (5 carryover + 1 new from this tick)

Tick wall-clock: ~14 min (under 20-min cap).
