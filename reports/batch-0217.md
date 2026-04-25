# Batch 0217 Report — sis_mining (NHCC national monument declarations cluster, continuation)

- Generated: 2026-04-25T07:10:00Z
- Phase: phase_4_bulk
- Sub-phase: sis_mining (priority_order item 7 — second consecutive sis_mining tick, NHCC monument cluster continuation)
- Records written: 8/8 ok (100%)
- Discovery: REUSED `_work/batch_0216_discovery.json` (no new alphabet probes spent — 17 candidates remained from batch 0216 cache; 8 ingested this tick, 9 deferred to batch 0218)
- Robots.txt re-verified: sha256 prefix fce67b697ee4ef44 (unchanged from batches 0193-0216)
- MAX_BATCH_SIZE cap honoured: 8 records (=cap)
- Crawl delay: 6 s (margin over robots-declared 5 s)

## Records Added

| Year | No. | Sub-phase | Title |
|------|-----|-----------|-------|
| 2023 | 035 | sis_mining | National Heritage Conservation Commission (Mumbotuta Falls) (National Monument) (Declaration) Order, 2023 |
| 2019 | 048 | sis_mining | National Heritage Conservation Commission (Longola Hot Springs) (National Monument) (Provisional Declaration) Order, 2019 |
| 2019 | 049 | sis_mining | National Heritage Conservation Commission (Mulungushi Rock of Authority) (National Monument) (Provisional Declaration) Order, 2019 |
| 2019 | 050 | sis_mining | National Heritage Conservation Commission (Chinyunyu Hot Springs) (National Monument) (Declaration) Order, 2019 |
| 2019 | 051 | sis_mining | National Heritage Conservation Commission (Mukuku Bridge) (National Monument) (Provisional Declaration) Order, 2019 |
| 2019 | 052 | sis_mining | National Heritage Conservation Commission (Mpezeni Royal Burial) (National Monument) (Provisional Declaration) Order, 2019 |
| 2019 | 053 | sis_mining | National Heritage Conservation Commission (Tarbuttite Site) (National Monument) (Provisional Declaration) Order, 2019 |
| 2019 | 054 | sis_mining | National Heritage Conservation Commission (Kavalamanja-Kakaroo Liberation Heritage) (Declaration) Order, 2019 |

Parent Act for all 8: NHCC Act Cap.173 (national monument declaration / preservation series under sections 25-26). Continuation of the NHCC monument declaration cluster opened by batch 0215 (2023/026 Zambezi Source) and extended by batch 0216 (2023/027-034 cluster). 2023/035 (Mumbotuta Falls) closes the 2023 NHCC cluster; 2019/048-054 are the first wave of the 2019 NHCC preservation/declaration series (Longola Hot Springs, Mulungushi Rock of Authority, Chinyunyu Hot Springs, Mukuku Bridge, Mpezeni Royal Burial, Tarbuttite Site, Kavalamanja-Kakaroo Liberation Heritage).

## Provenance

- **2023/035**: PDF sha256=ba3b01ace68ed9d6985e5a1e21e80d845e4be135dd69c5efd3ae65b31a7d7e1c (292683 bytes); record at `/sessions/cool-gallant-cannon/mnt/corpus/records/sis/2023/si-zm-2023-035-national-heritage-conservation-commission-mumbotuta-falls-national-monument-decl.json`
- **2019/048**: PDF sha256=243ce18bf736833a5a1a9ac13af4c02035ceb1874a8d9079a9f36cfd80979c18 (12366 bytes); record at `/sessions/cool-gallant-cannon/mnt/corpus/records/sis/2019/si-zm-2019-048-national-heritage-conservation-commission-longola-hot-springs-national-monument-.json`
- **2019/049**: PDF sha256=ec308e867e7281c7c3ec5cac9fbd931966d0e200edb71ed6a97f846daaa46bda (15093 bytes); record at `/sessions/cool-gallant-cannon/mnt/corpus/records/sis/2019/si-zm-2019-049-national-heritage-conservation-commission-mulungushi-rock-of-authority-national-.json`
- **2019/050**: PDF sha256=8dd280064b39e20dc8a9dd68033921ab8f5cafb0e443e9383932d04c55329b16 (15030 bytes); record at `/sessions/cool-gallant-cannon/mnt/corpus/records/sis/2019/si-zm-2019-050-national-heritage-conservation-commission-chinyunyu-hot-springs-national-monumen.json`
- **2019/051**: PDF sha256=95d2894838a01910b73c6463f41323ae6f5640b09855043f7183dd8ec68f1c1c (12365 bytes); record at `/sessions/cool-gallant-cannon/mnt/corpus/records/sis/2019/si-zm-2019-051-national-heritage-conservation-commission-mukuku-bridge-national-monument-provis.json`
- **2019/052**: PDF sha256=62f80db5994fb5bf636486e8b8d284c505c2a9b29e8128238b32eb48b5cabd3d (118380 bytes); record at `/sessions/cool-gallant-cannon/mnt/corpus/records/sis/2019/si-zm-2019-052-national-heritage-conservation-commission-mpezeni-royal-burial-national-monument.json`
- **2019/053**: PDF sha256=4207b720d23ae9b29e5ba0a3f5f4041d443e4032c6d634a038cb26c2bb0eb76d (11703 bytes); record at `/sessions/cool-gallant-cannon/mnt/corpus/records/sis/2019/si-zm-2019-053-national-heritage-conservation-commission-tarbuttite-site-national-monument-prov.json`
- **2019/054**: PDF sha256=38730c3e22d2526434fe440d873c3abf70bbc96c300d49fee84062b8ef1290a8 (13668 bytes); record at `/sessions/cool-gallant-cannon/mnt/corpus/records/sis/2019/si-zm-2019-054-national-heritage-conservation-commission-kavalamanja-kakaroo-liberation-heritag.json`

All raw HTML+PDF pairs persisted under `raw/zambialii/si/{2019,2023}/` for B2 sync (deferred to host — rclone unavailable in sandbox).

## Integrity Checks

- CHECK1a (batch-scoped id uniqueness): PASS — 8 distinct record IDs, no batch-internal collisions
- CHECK1b (vs HEAD-tracked records): PASS — 0 collisions with prior corpus
- CHECK2 (amended_by refs resolve): PASS — 0 refs (declaration orders carry no amendment chain)
- CHECK3 (repealed_by refs resolve): PASS — 0 refs
- CHECK4 (cited_authorities refs resolve): PASS — 0 refs
- CHECK5 (source_hash matches on-disk raw): PASS — 8/8 PDF sha256 verified against raw/zambialii/si/{2019,2023}/

Note: a corpus-wide audit ran during this tick surfaced ~30 pre-existing flat-vs-year-subdir duplicate paths under records/acts/ for the same record ID (unchanged from prior ticks; not introduced by this batch). Issue logged for future cleanup tick — not blocking.

## Budget

- Today's fetches before tick: 280
- Tick fetches used: 17 (1 robots re-verify + 16 record HTML+PDF pairs)
- Today's fetches after tick: ~297 / 2000 (14.9%)
- Tokens within budget

## Cumulative Counters

- SI records: 333 (was 325 at end of batch 0216; +8 = 333)
- Judgment records: 25 (case_law_scz still paused per robots.txt Disallow on /akn/zm/judgment/)

## Next Tick Plan

- Continue **sis_mining** by re-using `_work/batch_0217_discovery.json` (9 NHCC candidates remain: 2019/055-057, 2019/075, 2017/071, 2010/006, 2009/049-050, 1997/049). Next tick should ingest 8 of them without spending discovery fetches.
- After NHCC cluster fully drains, fall back to alphabet probes M (Mines, Mining, Minerals), P (Prospecting, Petroleum), Q (Quarry), G (Geological) for Mines and Minerals Development Act 2015/11 derivatives.
- Cross-sub_phase fill remains: sis_courts (Industrial Relations Court, more HC rules), sis_health (medicines and allied substances Act SIs), sis_family (Wills + Marriage Act derivatives).
- Re-verify robots.txt at start of next tick.

## Infrastructure Notes

- B2 sync: rclone unavailable in sandbox; raw files (16 HTML+PDF for batch 0217, ~2.5 MB) await host-driven sync
- corpus.sqlite: stale rollback-journal still blocks in-sandbox FTS rebuild (disk I/O error on read) — host-driven repair pending
- Persistent virtiofs unlink-failure warnings on .git/index.lock (workaround: GIT_INDEX_FILE override stable across batches 0192-0216)
- Sandbox-bash 45s-call cap forced ingest into 4 invocations (slice 0_3 + slice 3_5 + slice 5_7 + slice 7_8 + finalize)
- 100% yield is the fourth consecutive tick at full-cap (batches 0214, 0215, 0216, 0217)
