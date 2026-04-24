# Batch 0201 Report — Phase 4 sis_data_protection rotation + sis_corporate fallthrough

- **Batch:** 0201
- **Phase:** 4 (Bulk ingestion)
- **Started:** 2026-04-24T22:38:17Z
- **Completed:** 2026-04-24T22:39:30Z
- **Records written:** 6 / 6 targets attempted
- **Sub-phase yield:** sis_data_protection = 2, sis_corporate = 4
- **Fetches used (this batch):** 22 (10 discovery + 12 ingest HTML+PDF pairs)
- **Cumulative today:** ~384 / 2000 (19.2%) — within budget
- **Robots.txt re-verified:** sha256 prefix `fce67b697ee4ef44` (unchanged from batches 0193–0200)
- **Integrity checks:** all PASS (id uniqueness, no cross-refs to resolve, on-disk hash match, required-fields populated, 12 provenance.log entries)
- **Gaps:** none

## Rotation rationale

Batch-0200 closed sis_employment with yield = 2 (< 3 threshold) and instructed the
next tick to rotate to sis_data_protection (priority_order item 6) via Data
Protection Act 2021/3 derivative SI probes, with a fallthrough to sis_corporate
(priority_order item 2) via Companies Act 2017/10 derivatives if sis_data_protection
yield < 3.

That fallthrough fired this tick: only two novel sis_data_protection candidates
turned up (the two ICT Act-derived "Administration of Authority" Regulations).
Adding sis_corporate yield brought the batch total to 6 — still well under
MAX_BATCH_SIZE = 8.

## Discovery

Live discovery probes this tick:

- robots.txt re-verify (sha256 `fce67b697ee4ef44…`, unchanged)
- Parent-Act probes:
    - `/akn/zm/act/2009/15` (ICT Act) → 2 SI links: 2015/021, 2022/028
    - `/akn/zm/act/2002/17` (IBA Act) → no SI links extracted
    - `/akn/zm/act/2009/22` (Postal Services Act) → no SI links extracted
    - `/akn/zm/act/2017/10` (Companies Act) → 1 SI link: 2018/047
    - `/akn/zm/act/2017/9` (Corporate Insolvency Act) → no SI links
    - `/akn/zm/act/2010/15` (PACRA Act) → no SI links
    - `/akn/zm/act/2016/41` (Securities Act) → no SI links
- Subsidiary-index probes:
    - `alphabet=B` → 4 BFS-tagged candidates; 1 already in HEAD (2025/009 BoZ
      Withdrawal/Exchange) and 3 novel: 2009/044, 2006/003, 2003/038
    - `alphabet=S` → 0 novel Securities-tagged candidates

Cached discovery re-used (no fresh fetch):
- `alphabet=D` from batch-0192 (no novel data-protection SIs since)
- `alphabet=I` from batch-0196 (all novel ICT/info-comm SIs already ingested)
- `alphabet=C` from batch-0192 / batch-0197 (all novel Companies/Corporate SIs
  already ingested)
- 2021/2 (Cyber Security), 2021/3 (Data Protection), 2021/4 (ECT) parent-Act
  HTMLs from batch-0192 (Commencement Orders only — already ingested batch-0192)

## Targets ingested

| # | SI                  | Sub-phase           | Sections | PDF bytes | Status |
|---|---------------------|---------------------|----------|-----------|--------|
| 1 | SI 21 of 2015       | sis_data_protection | 3        |   107,628 | ok     |
| 2 | SI 28 of 2022       | sis_data_protection | 8        |   324,246 | ok     |
| 3 | SI 47 of 2018       | sis_corporate       | 2        |    11,677 | ok     |
| 4 | SI 44 of 2009       | sis_corporate       | 10       |   357,672 | ok     |
| 5 | SI 3  of 2006       | sis_corporate       | 144      | 3,913,168 | ok     |
| 6 | SI 38 of 2003       | sis_corporate       | 110      | 3,708,035 | ok     |

### sis_data_protection (2)

1. **SI 21 of 2015** — *Information and Communication Technologies (Administration of Authority) Regulations, 2015*
   - Parent: Information and Communication Technologies Act, No. 15 of 2009
   - Source PDF: https://zambialii.org/akn/zm/act/si/2015/21/eng@2015-04-30/source.pdf
   - sha256: `19a6c9902de98579565428881ab7350b7bca0cdf9a4382d6cac41e1ae2b7919e`

2. **SI 28 of 2022** — *Information and Communication Technologies (Administration of Authority) Regulations, 2022*
   - Parent: Information and Communication Technologies Act, No. 15 of 2009
   - Source PDF: https://zambialii.org/akn/zm/act/si/2022/28/eng@2022-04-04/source.pdf
   - sha256: `d3013cd5ede5afe3ce577265c743f393054443c15596659c0a163f7d1a3622dd`

### sis_corporate (4)

3. **SI 47 of 2018** — *Companies Act (Commencement) Order, 2018*
   - Parent: Companies Act, No. 10 of 2017 (the pilot statute — see Phase 2)
   - Source PDF: https://zambialii.org/akn/zm/act/si/2018/47/eng@2018-06-15/source.pdf
   - sha256: `c7c13165af174cebe0e563ef18dfad3b8312f02aa99a4693e1db78fef8dc9571`

4. **SI 44 of 2009** — *Banking and Financial Services (Restriction on Kwacha Lending to Non-Residents) Regulations, 2009*
   - Source PDF: https://zambialii.org/akn/zm/act/si/2009/44/eng@2009-07-17/source.pdf
   - sha256: `91fe62c91876786629bee2a758955e56412b46a3acbdda753952a2a1814afce5`

5. **SI 3 of 2006** — *Banking and Financial Services (Microfinance) Regulations, 2006*
   - Source PDF: https://zambialii.org/akn/zm/act/si/2006/3/eng@2006-01-30/source.pdf
   - sha256: `d0f70d998a86e955a7d3b17088ecba1e53b1c489a6ba4fdfb27f9be88652e065`

6. **SI 38 of 2003** — *Banking and Financial Services (Bureau de Change) Regulations, 2003*
   - Source PDF: https://zambialii.org/akn/zm/act/si/2003/38/eng@2003-04-11/source.pdf
   - sha256: `a6a495b129abe98c579ae0d21fda54cd12b33e7d80adb1a12c0cba45a47b9466`

## Integrity (CHECK1–CHECK5 + provenance audit)

- **CHECK1 (id uniqueness, batch + HEAD)** — PASS. 6 unique IDs; pre-write
  collision guards in `process_target` rejected any HEAD prefix clash.
- **CHECK2 (cross-refs)** — PASS. All `amended_by` empty, all `repealed_by`
  null. Nothing to resolve.
- **CHECK3 (cited_authorities)** — N/A. Field not present in SI record schema
  (only on judgments).
- **CHECK4 (source_hash matches on-disk raw)** — PASS. All 6 PDFs re-hashed
  from `raw/zambialii/si/{year}/<stem>.pdf` and matched record `source_hash`.
- **CHECK5 (required fields)** — PASS. All of `id`, `type`, `jurisdiction`,
  `title`, `citation`, `sections`, `source_url`, `source_hash`, `fetched_at`,
  `parser_version` populated and non-empty.
- **provenance.log audit** — 12 entries appended for batch=0201 (6 records
  × 2 fetches: AKN HTML page + PDF), as expected.

## Sub-phase running totals (post-batch)

- sis_corporate: now includes 4 new BFS / Companies Commencement records
- sis_data_protection: +2 (ICT Admin of Authority pair)
- sis_employment: unchanged (last touched batch-0200)
- sis_tax: unchanged (last touched batch-0199)
- sis_mining: unchanged (last touched batch-0194)
- sis_family: unchanged (last touched batch-0196)
- case_law_scz: paused per robots.txt Disallow on `/akn/zm/judgment/`
- acts_in_force: unchanged

Cumulative SI records on disk after this batch: 219 (+6 vs. batch-0200's 213).

## Next-tick plan

Yield this tick = 6 (well above 3-rotation threshold). Default rule says
**continue sis_corporate** next tick, with these probes:

- `alphabet=B` re-scan (already cached) for any BFS Regulations missed —
  e.g. BFS Capital Adequacy, BFS Disclosure of Lending Rates, BFS Liquidity
- Patents and Companies Registration Agency (PACRA) Act 2010/15 derivatives
  via `alphabet=P`
- Securities Act 2016/41 derivatives via `alphabet=S`
- Money Lenders Act / Building Societies Act SIs

Fallback if sis_corporate yield < 3:
- rotate to **sis_data_protection** for a deeper IBA Act / Postal Services Act
  parent-act probe (those returned 0 SI links this tick — likely the SIs are
  catalogued under different akn slugs; try alphabet=B for "Broadcasting"
  and alphabet=P for "Postal").

Re-verify robots.txt at start of next tick.

## Infrastructure follow-up (non-blocking)

- 12 batch-0201 raw files on disk (6 HTML + 6 PDF, ~8.4 MB) plus legacy files
  from batches 0192–0200 awaiting host-driven `rclone sync` to B2.
- `corpus.sqlite` stale rollback-journal still blocks in-sandbox FTS rebuild.
- 34 legacy-schema act JSON dupes under `records/acts/` + 42 Appropriation-Act
  `-000-` placeholder dupes + 63 SI records at top level of `records/sis/`
  (legacy flat layout) remain unresolved.
