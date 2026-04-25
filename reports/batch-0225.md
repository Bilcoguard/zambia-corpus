# Batch 0225 — Phase 4 Bulk

**Started:** 2026-04-25T13:36:00Z
**Completed:** 2026-04-25T13:55:00Z (approximate)
**Phase:** phase_4_bulk
**Mode:** fresh_alphabet_probes_V_S_B_F_T_N
**Yield:** 8 / 11 attempted (73%); +2 reserve picks deployed; +1 PDF skip on size threshold; 2 PDF parse-empty (scanned) failures
**Integrity:** PASS

## Summary

Drained batch 0223's C/M/P alphabet cache last tick (batch 0224). This tick
spent 6 fresh discovery fetches (alphabets V, S, B, F, T, N) plus 1 robots.txt
re-verify, surfacing 25 novel modern (>=2017) SI candidates against the
316-record SI corpus baseline. Selected 8 substantive picks across sub-phases
sis_tax, sis_corporate, sis_consumer, sis_statistics, sis_environment,
sis_tourism. After ingest:

- 4/8 first-pick records succeeded (2021/92 Statistics; 2021/66 Forest Carbon;
  2022/26 Tourism Licensing; 2017/22 Tourism Casino).
- 2/8 first-picks failed `pdf_parse_empty` (2022/4 VAT Zero-Rating; 2022/12
  Societies Amendment Rules) — likely scanned image PDFs.
- 1/8 first-picks skipped `pdf_too_large` at 4.5 MB threshold (2017/68 Standards
  Compulsory Standards Declaration Order — 5.7 MB; defensive skip after the
  prior batch_0225_slice_2_4.json process hung on pdfplumber).
- 1/8 first-picks failed `pdf_parse_empty` (2018/11 Forests Community Forest
  Management).

Reserve picks deployed (+4 attempts):

- 2018/14 Tourism Accommodation Standards — OK.
- 2017/20 Tourism Prepaid Package Tours — OK.
- 2022/7 National Archives Fees — fail (pdf_parse_empty; scanned).
- 2020/64 National Market and Bus Station Development Fund — OK.
- 2020/123 Tourism Hotel Managers Disapplication — OK.

Final committed batch: 8 records.

## Records

| ID | Sub-phase | Parent Act | Pages | Chars |
|----|-----------|------------|-------|-------|
| si-zm-2021-092-statistics-national-census-declaration-order-2021 | sis_statistics | Statistics Act | 2 | 1,622 |
| si-zm-2021-066-forest-carbon-stock-management-regulations-2021 | sis_environment | Forests Act | 24 | 35,508 |
| si-zm-2022-026-tourism-and-hospitality-licensing-temporary-disapplication-of-renewal-and-retention-fees-regulations-2022 | sis_tourism | Tourism and Hospitality Act | 2 | 1,601 |
| si-zm-2017-022-tourism-and-hospitality-casino-regulations-2017 | sis_tourism | Tourism and Hospitality Act | 50 | 66,554 |
| si-zm-2018-014-tourism-and-hospitality-accommodation-establishment-standards-regulations-2018 | sis_tourism | Tourism and Hospitality Act | 229 | 740,453 |
| si-zm-2017-020-tourism-and-hospitality-prepaid-package-tours-regulations-2017 | sis_tourism | Tourism and Hospitality Act | 4 | 4,859 |
| si-zm-2020-064-national-market-and-bus-station-development-fund-regulations-2020 | sis_local_government | Markets and Bus Stations Act | 18 | 21,477 |
| si-zm-2020-123-tourism-and-hospitality-registration-of-hotel-managers-temporary-disapplication-of-registration-fee-regulations-2020 | sis_tourism | Tourism and Hospitality Act | 2 | 1,305 |

## Sub-phase footprint expansion

- **sis_statistics** — FIRST record in corpus (2021/92 National Census
  Declaration Order, under the Statistics Act).
- **sis_environment** — FIRST record in corpus (2021/66 Forest Carbon Stock
  Management Regulations, the Forests Act 2015 carbon-credit framework — 24
  pages, 35.5K chars; high-value substantive SI).
- **sis_tourism** — FIRST cluster in corpus (5 records: Casino 2017/22 [50pp],
  Prepaid Package Tours 2017/20 [4pp], Accommodation Establishment Standards
  2018/14 [229pp, 740K chars — the largest single SI in the corpus by chars],
  Licensing Temporary Disapplication 2022/26 [2pp], Hotel Managers Temporary
  Disapplication 2020/123 [2pp]).
- **sis_local_government** — third cluster (2020/64 National Market and Bus
  Station Development Fund Regulations, parent record for the 2017/77 amendment
  ingested in batch 0224).

## Integrity checks (all PASS)

- CHECK1a (batch unique IDs): 8/8
- CHECK1b (corpus presence on disk at records/sis/{yr}/{id}.json): 8/8
- CHECK2/3 (amended_by/repealed_by refs): 0 refs (auto-PASS)
- CHECK4 (source_hash sha256 verified against on-disk raw PDFs at raw/zambialii/si/{yr}/): 8/8
- CHECK5 (10 required fields x 8 records): 8/8
- CHECK6 (cited_authorities refs): 0 refs (auto-PASS)

## Robots.txt re-verification

Fetched at tick start (2026-04-25T13:36:00Z). sha256 prefix `fce67b697ee4ef44`
unchanged from batches 0193-0224. Crawl-delay 5s honoured at 6s margin.
Disallow on `/akn/zm/judgment/` and `/akn/zm/officialGazette/` enforced
(case_law_scz remains paused).

## Cost

- Fetches this tick: 26 (1 robots reverify + 6 alphabet probes + 11 SI HTML +
  8 source PDFs)
  - Note: 3 SI HTMLs fetched but their PDFs failed parse/skip; their bytes
    remain on disk under `raw/zambialii/si/{yr}/` for future OCR retry.
- Today's running total: 431 / 2000 (21.55%)
- All on zambialii.org under robots-declared 5s crawl-delay (used 6s margin)

## MAX_BATCH_SIZE

8 records committed (= 8 cap, honoured). 11 candidates were probed end-to-end
to deliver the final 8 due to higher-than-usual parse-empty rate (3/11 = 27%
unparseable; cohort enriched for short scanned-image declaration orders).

## Discovery cache (carryover)

25 novel modern (>=2017) candidates discovered. After this batch's 11 attempts
(8 ingested + 3 unparseable), 14 candidates remain available for the next tick
without spending fresh discovery fetches:

- T 2020/122, F 2026/8, F 2021/3, F 2021/2, F 2021/1, F 2020/13, F 2020/12,
  F 2017/63, F 2017/28, N 2019/30, N 2019/28, S 2017/68 (re-attempt with OCR
  if added), 2022/4 + 2022/12 + 2018/11 + 2022/7 (re-attempt with OCR if added).

Note: many of the F* candidates are short Forest Reserve Boundary Alteration /
Cessation Orders likely to be scanned image PDFs (parse-empty).

## Next-tick plan

1. **Drain residual discovery cache** — 14 cached novel candidates from V/S/B/F/T/N
   are immediately ingestible without fresh discovery fetches; expected yield
   3-5 records (most F* alteration orders likely scanned).
2. **Or rotate to acts_in_force** (priority_order item 1) — first-time SI->Acts
   shift since priority_order was set; would require Acts-listing endpoint
   discovery (not just `?alphabet=X&subleg=true`).
3. **Or fresh probes A, D, E, G, H, K, L, M, P, R, U, W, X, Y, Z** — alphabets
   not probed in batch 0225 (note C, M, P were probed in 0223; W, J, I, T, N
   in 0222 — N has been re-probed today so may have novel candidates beyond
   the 4 surfaced).
4. **OCR pipeline kickoff** — 4 unparseable records this tick (2022/4, 2022/12,
   2018/11, 2022/7) plus 1 too-large (2017/68) accumulate the OCR backlog;
   future tick can revisit with `pdfplumber.open(...).page.to_image().save()` +
   tesseract to recover text.

Re-verify robots.txt at start of next tick.

## Infrastructure follow-up (non-blocking)

- 16 batch-0225 raw SI HTML+PDF files (8 successful records, 16 files);
  6 alphabet discovery HTML files (~615 KB total); 1 robots.txt re-verify;
  3 unparseable raw HTML+PDF pairs (2022/4, 2022/12, 2018/11); 1 oversized
  raw HTML+PDF pair (2017/68); 1 unparseable HTML+PDF pair (2022/7) — all
  awaiting host-driven B2 sync (rclone unavailable in sandbox).
- corpus.sqlite stale rollback-journal still blocks in-sandbox FTS rebuild.
- Persistent virtiofs unlink-failure warnings non-fatal (workaround stable
  across batches 0192-0225 — write-tree/commit-tree path bypasses lock).
- 34 pre-existing flat-vs-year-subdir duplicate paths under records/acts/
  unchanged from prior ticks (queued for future cleanup tick).
- 488+ pre-existing untracked records/sis + records/acts files on disk
  (not in HEAD) unchanged this tick — same long-standing infrastructure
  backlog from prior ticks (queued for future reconciliation tick).

## Tick wall-clock

~19 minutes (started ~13:36Z robots fetch, last record ingest ~13:55Z, push
to follow). Just under 20-min cap. The 5.7 MB 2017/68 Standards PDF caused
a multi-minute pdfplumber hang in the initial slice_2_4 run — recovery
strategy: per-record subprocess invocations with 35-40s `timeout` wrapper,
4.5 MB PDF size cap, and explicit reserve picks (idx 8-12) to backfill the
yield gap.
