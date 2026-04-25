# Batch 0230 — Phase 4 Bulk Ingestion

## Summary
- **Batch**: 0230
- **Phase**: 4 (bulk_ingest)
- **Sub-phase**: sis_planning (continues batch 0229's URP Act cluster)
- **Picks**: 8 (MAX_BATCH_SIZE cap)
- **Yield**: 8 ok / 8 attempted (100%)
- **Source**: zambialii.org (alphabet=U residual cache from batch 0229; no fresh discovery probe)
- **Parent Act**: Urban and Regional Planning Act (Act No. 3 of 2015)
- **Tick start**: 2026-04-25T16:33Z (robots reverify)

## Records ingested
| Yr/Num | Pages | Chars  | Title (truncated) |
|--------|-------|--------|-------------------|
| 2017/64  | 2 | 1145 | URP (DLPA) (No. 2) Regulations, 2017 |
| 2018/44  | 2 |  964 | URP (DLPA) (No. 2) Regulations, 2018 |
| 2019/43  | 1 | 1041 | URP (DLPA) (No. 2) Regulations, 2019 |
| 2019/45  | 2 | 1024 | URP (DLPA) (No. 3) Regulations, 2019 |
| 2019/78  | 2 |  984 | URP (DLPA) Regulations, 2019 |
| 2020/9   | 2 |  967 | URP (DLPA) Regulations, 2020 |
| 2020/55  | 2 |  926 | URP (DLPA) Regulations, 2020 |
| 2020/108 | 2 | 1121 | URP (DLPA) (No. 3) Regulations, 2020 |

All 8 are short Designated-Local-Planning-Authority declaration orders made
under the Urban and Regional Planning Act, 2015 (Act No. 3 of 2015) by the
Minister responsible for local government planning. They successively
designate (or amend a designation of) a council as a Local Planning
Authority for an area. Mean PDF size 2 pages / ~1000 characters,
0% scanned-image rate (all text-extractable), matching batch 0229's DLPA-order
experience.

## Sub-phase footprint
- **sis_planning**: +8 (cumulative 16, all under URP Act; combined with batch 0229's 8)

## Discovery cost
- 0 fresh alphabet probes (drained from batch 0229's U-cache)
- 1 robots.txt re-verification (sha256 prefix `fce67b697ee4ef44` unchanged from batches 0193-0229)

## Per-record cost
- 8 picks × 2 (HTML + PDF) = 16 ingest fetches

## Cumulative fetches today (after this tick)
- ~515 / 2000 (≈ 25.75%) — well within budget

## Integrity (all PASS)
- CHECK1a: 8/8 batch unique ids
- CHECK1b: 8/8 corpus presence on disk
- CHECK2/3: amended_by / repealed_by — 0 refs to resolve
- CHECK4: source_hash sha256 verified 8/8 against raw/zambialii/si/(2017,2018,2019,2020)/
- CHECK5: 10 required fields × 8 records — all present
- CHECK6: cited_authorities — 0 refs to resolve

## Cumulative SI records after this batch
- 434 SI records (+8 over batch 0229's 426)
- 25 judgments (paused per robots Disallow on /akn/zm/judgment/)

## U-alphabet cache state
- Total candidates: 19 modern (>=2017)
- Ingested: 16 (8 in batch 0229, 8 in batch 0230)
- Reserve for next tick: 3 (2022/60, 2023/9, 2023/45)

## Plan for next tick
1. Drain 3 remaining U-alphabet residuals (2022/60, 2023/9, 2023/45) — ~6 ingest fetches.
2. Begin a fresh alphabet probe (X / Y / Z still un-probed) and pick up to 5 modern candidates to fill the batch to 8.
3. Or rotate to acts_in_force priority_order item 1 (requires a separate Acts-listing endpoint discovery).
4. OCR backlog from batches 0225/0226 (5 items) remains queued.

## Infrastructure follow-up (non-blocking)
- B2 sync: rclone unavailable in sandbox; batch-0230 raw files (~15 = 8 HTML + 8 fresh PDF − 1 robots already in cache) plus accumulated batches 0192-0229 raw files awaiting host-driven `rclone sync raw/ b2raw:kwlp-corpus-raw/`.
- corpus.sqlite stale rollback-journal still blocks in-sandbox FTS rebuild.
- Persistent virtiofs unlink-failure warnings non-fatal; workaround stable across batches 0192-0230 (write-tree/commit-tree path bypasses lock).
- 34 pre-existing flat-vs-year-subdir duplicate paths under records/acts/ unchanged from prior ticks.
- 488+ pre-existing untracked records/sis + records/acts files on disk (not in HEAD) — long-standing infrastructure backlog, queued for future reconciliation tick.
- OCR backlog at 5 items (carryover from batches 0225/0226).
