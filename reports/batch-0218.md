# Batch 0218 Report — sis_mining (NHCC monument cluster — 2019 wave 2 + 2017/2010/2009 monument tail)

- Generated: 2026-04-25T07:34:00Z
- Phase: phase_4_bulk
- Sub-phase: sis_mining (priority_order item 7 — third consecutive sis_mining tick)
- Records written: 8/8 ok (100%)
- Discovery: REUSED `_work/batch_0217_discovery.json` (no new alphabet probes; 9 candidates remained from batch 0217 cache after HEAD filter; 8 ingested this tick, 1 deferred — 1997/049 night-game-drives is sis_environment scope, kept for cross-sub_phase rotation next tick)
- Robots.txt re-verified: sha256 prefix fce67b697ee4ef44 (unchanged from batches 0193-0217)
- MAX_BATCH_SIZE cap honoured: 8 records (=cap)
- Crawl delay: 6 s (margin over robots-declared 5 s)

## Records Added

| Year | No. | Sub-phase | Title |
|------|-----|-----------|-------|
| 2019 | 055 | sis_mining | National Heritage Conservation Commission (Chipota Falls) (National Monument) (Provisional Declaration) Order, 2019 |
| 2019 | 056 | sis_mining | National Heritage Conservation Commission (Broken Hill Man) (National Monument) (Declaration) Order, 2019 |
| 2019 | 057 | sis_mining | National Heritage Conservation Commission (Kabwe Mine Museum) (National Monument) (Provisional Declaration) Order, 2019 |
| 2019 | 075 | sis_mining | National Heritage Conservation Commission (Kalonga Gawa Undi-Dole Royal Cemetery) (National Monument) (Declaration) Order, 2019 |
| 2017 | 071 | sis_mining | National Heritage Conservation Commission (Oliver Tambo House) (National Monument) (Declaration) Order, 2017 |
| 2010 | 006 | sis_mining | National Monuments (Entry and User Fees) Regulation, 2010 |
| 2009 | 049 | sis_mining | National Heritage Conservation Commission (National Monument) (Mulobezi Open Air Railway Museum) (Declaration) Order, 2009 |
| 2009 | 050 | sis_mining | Conservation Commission (National Monument) (Libala Limestone) (Declaration) Order, 2009 |

Parent Act for all 8: NHCC Act Cap.173 (national monument declaration / preservation series under sections 25-26). Continuation of the NHCC monument cluster: closes the 2019 NHCC declaration/preservation series (055-057, 075), captures a 2017 cluster member (071 Oliver Tambo House — heritage figure), 2010/006 (NHCC user fees regime — non-declaratory but Cap.173 fee schedule), and the 2009 Mulobezi/Libala monument pair (049+050).

Note: 2009/050 (Libala Limestone) is filed on ZambiaLII with the truncated short-form title "Conservation Commission ..." (the canonical "National Heritage Conservation Commission" prefix was elided on-source). Title preserved verbatim from PDF.

## Provenance

- **2019/055**: PDF sha256=4866e3448bf9112a12f211787e0a1f9d825c929074d05990b29837ec14fdf19b (12110 bytes); record at `/sessions/wizardly-pensive-sagan/mnt/corpus/records/sis/2019/si-zm-2019-055-national-heritage-conservation-commission-chipota-falls-national-monument-provis.json`
- **2019/056**: PDF sha256=b7ab6eafd97c2e9dd6295c4f18533b5382e4fa444adf3b2990334367287d2ebe (12866 bytes); record at `/sessions/wizardly-pensive-sagan/mnt/corpus/records/sis/2019/si-zm-2019-056-national-heritage-conservation-commission-broken-hill-man-national-monument-decl.json`
- **2019/057**: PDF sha256=c22824cf8d3f6ac4315e80d141a1f6b3af1e24467f43cfb7dc81afce7ff0b90d (11582 bytes); record at `/sessions/wizardly-pensive-sagan/mnt/corpus/records/sis/2019/si-zm-2019-057-national-heritage-conservation-commission-kabwe-mine-museum-national-monument-pr.json`
- **2019/075**: PDF sha256=2b0391945049182f4d65a92bfe505e3cd7cd485a9bb17e41cdd2085f91557fd5 (12673 bytes); record at `/sessions/wizardly-pensive-sagan/mnt/corpus/records/sis/2019/si-zm-2019-075-national-heritage-conservation-commission-kalonga-gawa-undi-dole-royal-cemetery-.json`
- **2017/071**: PDF sha256=093a2bc383034888f347e3e80c153a07f703e2c4ac12b4ac38f621f78b977fe5 (180500 bytes); record at `/sessions/wizardly-pensive-sagan/mnt/corpus/records/sis/2017/si-zm-2017-071-national-heritage-conservation-commission-oliver-tambo-house-national-monument-d.json`
- **2010/006**: PDF sha256=39bdf85a7109eeac2743358571536d6d584062f9456234925363fc58a158a263 (799306 bytes); record at `/sessions/wizardly-pensive-sagan/mnt/corpus/records/sis/2010/si-zm-2010-006-national-monuments-entry-and-user-fees-regulation-2010.json`
- **2009/049**: PDF sha256=de7538a915c923ff5f091e90dc2e310b4e8cfb628f8d2483de90ccd9c41bd5bf (276376 bytes); record at `/sessions/wizardly-pensive-sagan/mnt/corpus/records/sis/2009/si-zm-2009-049-national-heritage-conservation-commission-national-monument-mulobezi-open-air-ra.json`
- **2009/050**: PDF sha256=8f47180fefcf6a95c2d007a9586473973093c4ee52f67fa3e21bf623f721d41c (200747 bytes); record at `/sessions/wizardly-pensive-sagan/mnt/corpus/records/sis/2009/si-zm-2009-050-conservation-commission-national-monument-libala-limestone-declaration-order-200.json`

All raw HTML+PDF pairs persisted under `raw/zambialii/si/{2009,2010,2017,2019}/` for B2 sync (deferred to host — rclone unavailable in sandbox).

## Integrity Checks

- CHECK1a (batch-scoped id uniqueness): PASS — 8 distinct record IDs, no batch-internal collisions
- CHECK1b (vs HEAD-tracked records): PASS — 0 collisions with prior corpus
- CHECK2 (amended_by refs resolve): PASS — 0 refs (declaration orders / fee regulations carry no amendment chain in records produced)
- CHECK3 (repealed_by refs resolve): PASS — 0 refs
- CHECK4 (cited_authorities refs resolve): PASS — 0 refs
- CHECK5 (source_hash matches on-disk raw): PASS — 8/8 PDF sha256 verified against raw/zambialii/si/

## Budget

- Today's fetches before tick: 297
- Tick fetches used: 17 (1 robots re-verify + 16 record HTML+PDF pairs)
- Today's fetches after tick: ~314 / 2000 (15.7%)
- Tokens within budget

## Cumulative Counters

- SI records: 341 (was 333 at end of batch 0217; +8 = 341)
- Judgment records: 25 (paused per robots Disallow on /akn/zm/judgment/)

## Next-tick plan

The NHCC monument cluster cached from batches 0216/0217 is now FULLY DRAINED for sis_mining. Remaining cached candidate (1997/049 night-game-drives regs) is sis_environment scope — eligible for cross-sub_phase rotation if sis_mining alphabet probes yield <3 next tick.

Plan: probe alphabets M (Mines, Mining, Minerals), P (Prospecting, Petroleum), Q (Quarry), G (Geological), E (Explosives) for Mines and Minerals Development Act 2015/11 derivatives + Petroleum (Exploration and Production) Act SIs + Geological Survey Act + Explosives Act SIs not yet ingested.

Fallback if sis_mining yield <3: rotate via cross-sub_phase fill — sis_environment (water resources Acts SIs deep, EIA derivatives), sis_courts (Industrial Relations Court rules, more HC rules), sis_health (medicines and allied substances Act SIs), sis_family (Wills + Marriage Act derivatives) — plus the cached 1997/049 night-game-drives slot.

Re-verify robots.txt at start of next tick.

## Infrastructure follow-up (non-blocking)

- 16 batch-0218 raw SI files on disk (8 HTML + 8 PDF, ~0.5 MB given small declaration PDFs) plus accumulated batches 0192-0217 raw files awaiting host-driven B2 sync (rclone unavailable in sandbox)
- corpus.sqlite stale rollback-journal still blocks in-sandbox FTS rebuild (disk I/O error on read)
- Persistent virtiofs unlink-failure warnings non-fatal (workaround stable across batches 0192-0217 — write-tree/commit-tree path bypasses lock)
