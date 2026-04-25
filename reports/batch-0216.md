# Batch 0216 Report — sis_mining (NHCC national monument declarations cluster)

- Generated: 2026-04-25T06:38:00Z
- Phase: phase_4_bulk
- Sub-phase: sis_mining (priority_order item 7 — first attempt; rotation per batch-0215 next-tick plan)
- Records written: 8/8 ok (100%)
- Discovery alphabets probed: M, N, P (live re-fetch from cached HTML + zambialii.org/legislation/?alphabet=N)
- Discovery yield (sis_mining keyword filter): 25 / 80 novel pre-keyword candidates kept post-keyword
- Robots.txt re-verified: sha256 prefix fce67b697ee4ef44 (unchanged from batches 0193-0215)
- MAX_BATCH_SIZE cap honoured: 8 records (=cap)
- Crawl delay: 6 s (margin over robots-declared 5 s)

## Records Added

| Year | No. | Sub-phase | Title |
|------|-----|-----------|-------|
| 2023 | 027 | sis_mining | National Heritage Conservation Commission (Ng'wena Village) (National Monument) (Declaration) Order, 2023 |
| 2023 | 028 | sis_mining | National Heritage Conservation Commission (Nalupembe Falls) (National Monument) (Declaration) Order, 2023 |
| 2023 | 029 | sis_mining | National Heritage Conservation Commission (Chembe Island) (National Monument) (Declaration) Order, 2023 |
| 2023 | 030 | sis_mining | National Heritage Conservation Commission (Mambilima Cataracts) (National Monument) (Declaration) Order, 2023 |
| 2023 | 031 | sis_mining | National Heritage Conservation Commission (Musonda Falls) (National Monument) (Declaration) Order, 2023 |
| 2023 | 032 | sis_mining | National Heritage Conservation Commission (Kabwe Katenda) (National Monument) (Declaration) Order, 2023 |
| 2023 | 033 | sis_mining | National Heritage Conservation Commission (Ngonye Falls) (National Monument) (Declaration) Order, 2023 |
| 2023 | 034 | sis_mining | National Heritage Conservation Commission (Membo Caves) (National Monument) (Declaration) Order, 2023 |

Parent Act for all 8: NHCC Act Cap.173 (national monument declaration series under section 25). Continuation of the 2023 monument declaration cluster begun by batch 0215 (which added 2023/026 Zambezi Source).

## Provenance

- **2023/027**: PDF sha256=1ed1c60a7b5e61a7ac2a12d1208ef36cb5b650535e4b24aed477adfc1ae83c7d (472623 bytes); record at `records/sis/2023/si-zm-2023-027-national-heritage-conservation-commission-ngwena-village-national-monument-decla.json`
- **2023/028**: PDF sha256=67c7e3e45382dd8cf353cda617f51cd47ed79a42e0353dc5bdd7bfbde17b7ac4 (289219 bytes); record at `records/sis/2023/si-zm-2023-028-national-heritage-conservation-commission-nalupembe-falls-national-monument-decl.json`
- **2023/029**: PDF sha256=0d1466656413f90118185a1b357e79e98fc00518c19037bfe47a0eddb8280827 (290069 bytes); record at `records/sis/2023/si-zm-2023-029-national-heritage-conservation-commission-chembe-island-national-monument-declar.json`
- **2023/030**: PDF sha256=39403d7282658b93cbd88fa3e9865f36f86353fc9068e59dde1052620fad2f9a (295978 bytes); record at `records/sis/2023/si-zm-2023-030-national-heritage-conservation-commission-mambilima-cataracts-national-monument-.json`
- **2023/031**: PDF sha256=370ad4730c5aa6d708f8f737239e023346ed4378de53c051c472c438c65287a9 (288598 bytes); record at `records/sis/2023/si-zm-2023-031-national-heritage-conservation-commission-musonda-falls-national-monument-declar.json`
- **2023/032**: PDF sha256=e3ec53d250d86d065b99300ec353c12eae2d388c6ad14fc0ed5e556d3088040b (292861 bytes); record at `records/sis/2023/si-zm-2023-032-national-heritage-conservation-commission-kabwe-katenda-national-monument-declar.json`
- **2023/033**: PDF sha256=cc6084abd4c4db844e2c50eac12445509a2b2ecfd3d851663a6deb8e51e53bad (289681 bytes); record at `records/sis/2023/si-zm-2023-033-national-heritage-conservation-commission-ngonye-falls-national-monument-declara.json`
- **2023/034**: PDF sha256=ad03b26806807d03ff00855f840bd50f3f5fc818a0a2fbf87ca58b3cad212fe3 (287199 bytes); record at `records/sis/2023/si-zm-2023-034-national-heritage-conservation-commission-membo-caves-national-monument-declarat.json`

All raw HTML+PDF pairs persisted under `raw/zambialii/si/2023/` for B2 sync (deferred to host — rclone unavailable in sandbox).

## Integrity Checks

- CHECK1a (batch-scoped id uniqueness): PASS — 8 distinct record IDs, no batch-internal collisions
- CHECK1b (vs HEAD-tracked records): PASS — 0 collisions with prior corpus
- CHECK2 (amended_by refs resolve): PASS — 0 refs (declaration orders carry no amendment chain)
- CHECK3 (repealed_by refs resolve): PASS — 0 refs
- CHECK4 (cited_authorities refs resolve): PASS — 0 refs
- CHECK5 (source_hash matches on-disk raw): PASS — 8/8 PDF sha256 verified against raw/zambialii/si/2023/

## Budget

- Today's fetches before batch: 259
- Batch fetches used: 21 (4 discovery: robots + alphabets M/N/P; 16 record HTML+PDF pairs + 1 retry)
- Today's fetches after batch: ~280 / 2000 (14.0%)
- Tokens within budget

## Cumulative Counters

- SI records: 325 (was 317 at end of batch 0215; +8 = 325)
- Judgment records: 25 (case_law_scz still paused per robots.txt Disallow on /akn/zm/judgment/)

## Next Tick Plan

- Continue **sis_mining** with deeper N-alphabet probe (NHCC monuments 2023/035 plus 2019 NHCC declarations 048-057, 075 still pending; 2017/071 Oliver Tambo House; 2009-2010 monument series; 1997/049 night game drives) — there are at least 17 more candidates already discovered in this batch's discovery file, so next tick should re-use the cached `_work/batch_0216_discovery.json` and ingest the next 8.
- Cross-sub_phase fallback if NHCC cluster is exhausted: probe Mines and Minerals Development Act 2015/11 derivatives via alphabet M/P; try Petroleum Act SIs.
- Re-verify robots.txt at start of next tick.
- Cross-sub_phase fill remains: sis_courts (Industrial Relations Court, more HC rules), sis_health (medicines and allied substances Act SIs), sis_family (Wills + Marriage Act derivatives).

## Infrastructure Notes

- B2 sync: rclone unavailable in sandbox; raw files (16 HTML+PDF for batch 0216, ~2.5 MB) await host-driven sync
- corpus.sqlite: stale rollback-journal still blocks in-sandbox FTS rebuild (disk I/O error on read) — host-driven repair pending
- Persistent virtiofs unlink-failure warnings (workaround stable across batches 0192-0216)
- Sandbox-bash 45s-call cap forced ingest into 4 invocations (slice 0_3 from prior tick + slice 3_5 + slice 5_7 + slice 7_8 + finalize this tick)
- 100% yield is the third consecutive tick at full-cap (batches 0214, 0215, 0216)
