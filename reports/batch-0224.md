# Batch 0224 — Phase 4 Bulk

**Started:** 2026-04-25T12:34:33Z
**Completed:** 2026-04-25T12:38:00Z
**Phase:** phase_4_bulk
**Mode:** cache_drain_C_M_P_alphabet_modern_residual
**Yield:** 8 / 8 (100%)
**Integrity:** PASS

## Summary

Drained the residual modern (>=2017) text-extractable candidates from batch 0223's
C/M/P alphabet discovery cache (228 novel pre-keyword candidates; 16 modern;
8 already ingested in batch 0223; 8 remaining — picked all). No fresh discovery
fetches required for record selection — only the standard tick-start robots.txt
re-verification.

## Records

| ID | Sub-phase | Parent Act |
|----|-----------|------------|
| si-zm-2017-053-constitution-of-zambia-act-proclamation-declaration-of-threatened-state-of-public-security-2017 | sis_security | Constitution of Zambia Act |
| si-zm-2017-055-preservation-of-public-security-regulations-2017 | sis_security | Preservation of Public Security Act |
| si-zm-2017-027-control-of-goods-import-and-export-forest-produce-regulations-2017 | sis_trade | Control of Goods Act |
| si-zm-2017-031-control-of-goods-import-and-export-forest-produce-prohibition-of-importation-order-2017 | sis_trade | Control of Goods Act |
| si-zm-2019-064-control-of-goods-import-and-export-agriculture-prohibition-of-export-order-2019 | sis_trade | Control of Goods Act |
| si-zm-2017-077-national-markets-and-bus-stations-development-fund-regulations-2017 | sis_local_government | Markets and Bus Stations Act |
| si-zm-2021-114-provincial-and-district-boundaries-division-amendment-no-2-order-2021 | sis_local_government | Provincial and District Boundaries Act |
| si-zm-2021-109-plant-variety-and-seeds-amendment-regulations-2021 | sis_agriculture | Plant Variety and Seeds Act |

## Sub-phase footprint expansion

- **sis_security** — first records in corpus (Constitution Threatened-Security
  Proclamation 2017/53; Preservation of Public Security Regs 2017/55).
- **sis_trade** — first records in corpus (3 Control of Goods Act SIs covering
  forest produce import/export 2017/27 + 2017/31 and agriculture export
  prohibition 2019/64).
- **sis_local_government** — second cluster (markets-and-bus-stations
  development fund 2017/77; provincial/district boundaries division order
  2021/114).
- **sis_agriculture** — adds Plant Variety and Seeds Amendment Regs 2021/109,
  building on batch 0223's sis_agriculture parent record (2018/023).

## Integrity checks (all PASS)

- CHECK1a (batch unique IDs): 8/8
- CHECK1b (corpus presence on disk): 8/8
- CHECK2/3 (amended_by/repealed_by refs): 0 refs (auto-PASS)
- CHECK4 (source_hash sha256 verified against on-disk raw PDFs): 8/8
- CHECK5 (required fields x10 across 8 records): 8/8
- CHECK6 (cited_authorities refs): 0 refs (auto-PASS)

## Robots.txt re-verification

Fetched at tick start (2026-04-25T12:34:33Z). sha256 prefix `fce67b697ee4ef44`
unchanged from batches 0193-0223. Crawl-delay 5s honoured at 6s margin.
Disallow on `/akn/zm/judgment/` and `/akn/zm/officialGazette/` enforced
(case_law_scz remains paused).

## Cost

- Fetches this tick: 17 (1 robots reverify + 8 SI HTML + 8 source PDFs)
- Today's running total: 449 / 2000 (22.45%)
- All on zambialii.org under robots-declared 5s crawl-delay

## MAX_BATCH_SIZE

8 records committed (= 8 cap, honoured).

## Next-tick plan

Batch 0223's C/M/P modern-cache is now fully drained. Options for batch 0225:

1. Fresh alphabet probes — recommend V/S/B/F (haven't been re-probed in
   batches 0220-0224) or W/J/I/T/N (cached in batch 0222 — 71 novel
   pre-keyword candidates may still hold value if filtered for modern).
2. Rotate to **acts_in_force** (priority_order item 1, first-time SI->Acts
   shift since priority_order was set). Would require Acts-listing endpoint
   discovery rather than `?alphabet=X&subleg=true`.
3. Continue cross-sub_phase fill of sis_courts (2014/022 Legal Reform;
   2015/025; 2016/072 Inquiries Acts) or sis_tourism (multiple Tourism and
   Hospitality Act derivatives 2016+).

## Infrastructure follow-up (non-blocking)

- 16 batch-0224 raw SI files on disk + 1 robots.txt re-verify (~657 + 2 KB)
  plus accumulated batches 0192-0223 raw files awaiting host-driven B2 sync
  (rclone unavailable in sandbox).
- corpus.sqlite stale rollback-journal still blocks in-sandbox FTS rebuild.
- Persistent virtiofs unlink-failure warnings non-fatal (workaround stable
  across batches 0192-0224 — write-tree/commit-tree path bypasses lock).
- 34 pre-existing flat-vs-year-subdir duplicate paths under records/acts/
  unchanged from prior ticks (queued for future cleanup tick).

## Tick wall-clock

~5 min (tick begin 12:34:33Z; last record committed 12:38:00Z; commit + push
to follow). Well under 20-min cap.
