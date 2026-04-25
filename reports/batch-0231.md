# Phase 4 — Batch 0231 (Statutory Instruments)

**Date:** 2026-04-25
**Worker:** kwlp-worker (sandbox)
**Sub-phases:** sis_planning (3) + sis_health (2 — first) + sis_legal_education (1 — first) + sis_police (1 — first) + sis_water_resources (1 — first)

## Picks (8 — MAX_BATCH_SIZE cap)

| # | Year/Num | Title | Sub-phase | Parent Act | Status | Pages | Chars | sha256 prefix |
|---|---------|-------|-----------|------------|--------|-------|-------|---------------|
| 0 | 2022/60 | URP (Designated Local Planning Authorities) Regulations, 2022 | sis_planning | Urban and Regional Planning Act | ok | 2 | 1,085 | ed3585940704feea |
| 1 | 2023/9  | URP (Designated Local Planning Authority) Regulations, 2023   | sis_planning | Urban and Regional Planning Act | ok | 2 | 1,097 | 1ae9ce244ef95859 |
| 2 | 2023/45 | URP (Designated Local Planning Authority) (No. 2) Regulations, 2023 | sis_planning | Urban and Regional Planning Act | ok | 2 | 1,150 | e8f9b93d4f4ac889 |
| 3 | 2021/37 | Zambia Medicines and Medical Supplies Agency (Re-engagement of Staff) Regulations, 2021 | sis_health | ZAMMSA Act | ok | 2 | 1,642 | 2439bace5e8e486f |
| 4 | 2021/49 | Zambia Institute of Advanced Legal Education (Students) Rules, 2021 | sis_legal_education | ZIALE Act | ok | 28 | 44,905 | a8531721eb0e7774 |
| 5 | 2022/6  | Zambia Police (Fees) Regulations, 2022 | sis_police | Zambia Police Act | ok | 4 | 3,102 | 145673dbe2d6de00 |
| 6 | 2022/58 | Zambezi River Authority (Terms and Conditions of Service) (Amendment) By-Laws, 2022 | sis_water_resources | Zambezi River Authority Act | ok | 2 | 1,472 | 03e09458050b91cd |
| 7 | 2023/14 | Zambia Medicines and Medical Supplies Agency (Administration of Fund) Regulations, 2023 | sis_health | ZAMMSA Act | ok | 4 | 5,322 | 3d8e98ce8b0c3717 |

**Yield:** 8/8 = 100% (eighth consecutive 100%-yield batch; 0% scanned-image rate).

## Discovery

- Drained final 3 U-alphabet residuals from batch 0230 cache (URP Act DLPA orders).
- Probed alphabet=X (0 SIs — no titles starting with X) and alphabet=Y (0 SIs).
- Probed alphabet=Z: 23 unique SI links surfaced; 6 modern (>=2017); 5 novel after dedup against existing corpus → all 5 picked.

## Footprint expansion (firsts)

- **FIRST sis_health records** (2): Zambia Medicines and Medical Supplies Agency Act SIs.
- **FIRST sis_legal_education record** (1): ZIALE Act (Students) Rules — 28pp / 44.9K chars (substantive).
- **FIRST sis_police record** (1): Zambia Police (Fees) Regulations, 2022.
- **FIRST sis_water_resources record** (1): Zambezi River Authority Act By-Laws.

## Cost

- Robots reverify: 1 fetch
- Discovery probes (X, Y, Z): 3 fetches
- Per-record ingest fetches: 8 picks × 2 (HTML+PDF) − 1 reused (idx 2 HTML cached from earlier interrupted run) = 15 fresh
- **Tick total:** 19 fetches (was 514 before tick → 533/2000 = 26.65% used)

## Integrity (all PASS)

- CHECK1a (batch unique IDs): 8/8 PASS
- CHECK1b (corpus presence on disk): 8/8 PASS
- CHECK2 (amended_by resolve): 0 refs — PASS
- CHECK3 (repealed_by resolve): 0 refs — PASS
- CHECK4 (source_hash sha256 match raw): 8/8 PASS
- CHECK5 (required fields 10×8): 80/80 PASS
- CHECK6 (cited_authorities resolve): 0 refs — PASS

## Cumulative SI records

- After this batch: **442** (+8 over batch 0230's 434).
- Cumulative judgments: 25 (paused per robots Disallow on /akn/zm/judgment/).

## Robots compliance

- Robots.txt re-verified at tick start; sha256 prefix `fce67b697ee4ef44` unchanged from batches 0193–0230.
- Crawl-delay 5s honoured at 6s margin.
- Disallow `/akn/zm/judgment/` and `/akn/zm/officialGazette/` enforced (no judgment fetches).
- All ingest fetches were under `/akn/zm/act/si/` (allowed for wildcard UA).
- UA: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`.

## Z-alphabet residuals reserved for next tick

- 2025/74 — Zambia Institute of Secretaries (Registration) Regulations, 2025 (already in corpus per dedup; SKIP).
- (No other modern Z residuals — Z is fully drained.)

## Next-tick options

- (a) Re-probe earlier alphabets M / A / D / E for residuals (likely-fertile, prior probes are stale beyond batches 0223/0224);
- (b) Rotate to acts_in_force (priority_order item 1) — requires Acts-listing endpoint discovery (separate path from SI ingest);
- (c) OCR backlog from batches 0225/0226 (5 items: 2017/068, 2018/011, 2022/004, 2022/007, 2022/012);
- (d) Records reconciliation (488+ pre-existing untracked records/sis + records/acts files on disk).
