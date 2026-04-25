# Phase 4 — Batch 0240 Report

**Tick start:** 2026-04-25T22:05:09Z
**Batch:** 0240
**Phase:** 4 (bulk ingest)
**Cohort:** sis_energy first cluster + sis_elections E-residual drain (cohort 6)
**Cap honoured:** MAX_BATCH_SIZE=8, attempted=9 (1 in-batch substitute), committed=8

## Outcome
- **OK:** 8 records committed (yield 8/8 of cap; 8/9 attempted = 89%).
- **Skip:** 1 (2026/004 Electricity (Transmission) (Grid Code) Regulations 2026 — 28.18 MB > 4.5 MB defensive cap; raw PDF preserved on disk for OCR/manual processing).
- **Fail:** 0.

## Sub-phase footprint expansion
- **FIRST sis_energy cluster** in corpus (3 records) — Electricity Act SIs:
  - 2026/002 Electricity (Wayleave and Clearances) Regulations 2026 [44pp / 85,659 chars]
  - 2021/024 Electricity (Common Carrier) (Declaration) Regulations 2021 [4pp / 4,598 chars]
  - 2021/094 Electricity (Common Carrier) (Declaration) (Revocation) Order 2021 [2pp / 810 chars]
- **sis_elections drain +5** (Electoral Process Act LG By-Election orders):
  - 2023/036, 2023/040, 2023/046, 2024/002, 2024/006

## Discovery cost
- 1 new fetch (robots.txt re-verify only — sha256 prefix `fce67b697ee4ef44` unchanged from batches 0193-0239).
- Drained from batch_0233 E-probe cache (15 candidates remaining → 7 after this tick: includes 3 known scanned-image OCR backlog items + 4 unprocessed novel candidates).

## Robots.txt compliance
- Re-verified at tick start: `fce67b697ee4ef44…` (unchanged).
- Crawl-delay: 5s declared, 6s margin honoured between every fetch.
- Disallow on `/akn/zm/judgment/` and `/akn/zm/officialGazette/` enforced (no requests issued to those paths).
- UA `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` is not in any named-disallow rule.

## Integrity (all PASS)
- CHECK1a (batch unique IDs): 8/8 unique
- CHECK1b (corpus presence on disk): 8/8 present
- CHECK2 amended_by refs: 0 (none required to resolve)
- CHECK3 repealed_by refs: 0
- CHECK4 source_hash sha256 verified vs `raw/zambialii/si/{2021,2023,2024,2026}/`: 8/8 match
- CHECK5 required fields (10 × 8): all present
- CHECK6 cited_authorities refs: 0

## Records committed (8)
| # | yr/num | sub-phase | parent act | pages | chars |
|---|--------|-----------|-----------|-------|-------|
| 1 | 2026/002 | sis_energy | Electricity Act | 44 | 85,659 |
| 2 | 2021/024 | sis_energy | Electricity Act | 4 | 4,598 |
| 3 | 2021/094 | sis_energy | Electricity Act | 2 | 810 |
| 4 | 2023/036 | sis_elections | Electoral Process Act | 2 | 1,713 |
| 5 | 2023/040 | sis_elections | Electoral Process Act | 2 | 1,778 |
| 6 | 2023/046 | sis_elections | Electoral Process Act | 2 | 2,062 |
| 7 | 2024/002 | sis_elections | Electoral Process Act | 2 | 1,797 |
| 8 | 2024/006 | sis_elections | Electoral Process Act | 2 | 1,778 |

## Cumulative SI records after this batch: **506** (+8 over batch 0239's 498)

## Budgets
- Today (2026-04-25 UTC) fetches: ~688 / 2000 (34%; under cap).
- Tokens within budget.

## OCR / large-file backlog (carry-over)
- Existing 7 items from batches 0225 + 0235 + 0238 + 0239: 2017/068, 2018/011, 2018/075, 2018/093, 2022/004, 2022/007, 2022/008, 2022/012.
- **+1 new (oversize)**: 2026/004 Electricity Grid Code Regulations 2026 (28.18 MB, raw PDF preserved at `raw/zambialii/si/2026/si-zm-2026-004-electricity-transmission-grid-code-regulations-2026.pdf`) — needs split or out-of-band processing.
- New backlog total: 9 items.

## Next-tick plan options
- (a) Drain remaining batch-0233 E-probe cache: 4 unprocessed novel candidates (2023, 2024 LG By-Election orders) — ~50% expected yield given short-order pattern.
- (b) Fresh alphabet probes from unprobed set (no probes since batch 0233/0231/0232) — likely H/K/O/Q/R rotation.
- (c) Rotate to acts_in_force priority_order item 1 — would require Acts-listing endpoint discovery.
- (d) OCR retry on backlog (8 items) once tesseract is wired into sandbox.

## Infrastructure follow-up (non-blocking)
- batch-0240 raw files (16 = 8 HTML + 8 PDF for ok records + 1 HTML + 1 PDF for skip + 1 robots.txt) awaiting host-driven B2 sync (rclone unavailable in sandbox).
- Persistent virtiofs `unable to unlink` warnings non-fatal — workaround stable across batches 0192-0240 (write-tree/commit-tree path bypasses lock).
- corpus.sqlite stale rollback-journal still blocks in-sandbox FTS rebuild — tick-time presence check uses on-disk `records/sis/{yr}/` JSON glob fallback.
- Pre-existing infrastructure backlog unchanged: 34 acts/ flat-vs-year-subdir duplicates + 488+ untracked records on disk.
