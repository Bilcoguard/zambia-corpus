# Batch 0203 Report — Phase 4 sis_corporate continuation

- **Batch:** 0203
- **Phase:** 4 (Bulk ingestion)
- **Sub-phase:** sis_corporate
- **Started:** 2026-04-24T23:33:15Z
- **Completed:** 2026-04-24T23:36:05Z
- **Records written:** 7 / 9 targets attempted (within MAX_BATCH_SIZE = 8)
- **Fetches used (this batch):** 23 (5 discovery [robots + alphabets I/N/F/A] + 18 ingest HTML+PDF pairs)
- **Cumulative today:** ~416 / 2000 (20.8%) — well within budget
- **Robots.txt re-verified:** sha256 prefix `fce67b697ee4ef44` (unchanged from batches 0193–0202)
- **Integrity checks:** all batch-scoped checks PASS (CHECK1 batch IDs unique, CHECK2 cross-refs resolve, CHECK3 source_hash matches on-disk, CHECK4 required fields populated, CHECK5 provenance entries present for every batch URL)
- **Gaps:** 2 logged (pdf_parse_empty for SI 2019/025 + SI 2017/043 — both income-tax suspension SIs with image-only scanned PDFs; OCR backfill deferred)

## Sandbox-bash execution note

Same constraint as batch-0202: bwrap-isolated bash with 45 s call cap forces splitting into multiple invocations. This batch ran as 1 discovery call + 5 ingest slices (slices 0_2, 2_4, 4_6, 6_8, 8_10), each fitting inside 45 s with the 6 s crawl-delay margin (vs. robots.txt-declared 5 s).

## Discovery

Per batch-0202 next-tick plan: alphabets I (Insurance Act / IPEC SIs), N (National Pension Scheme / National Payment Systems / NCCO derivatives), F (Financial Intelligence Centre post-2022), A (Anti-Money Laundering / Co-operative Societies Audit).

- robots.txt re-verify (sha256 `fce67b697ee4ef44…`, unchanged)
- alphabet=I → 98 SI candidates
- alphabet=N → 60 SI candidates
- alphabet=F → 23 SI candidates
- alphabet=A → 20 SI candidates
- Total unique SI candidates discovered: ~201; after HEAD subtraction + corporate-keyword filter: 9 candidates curated.

## Targets ingested

| # | SI               | Sub-phase     | Title (truncated)                                                       | Status            |
|---|------------------|---------------|--------------------------------------------------------------------------|-------------------|
| 1 | SI 053 of 2022 | sis_corporate | Financial Intelligence Centre (Prescribed Threshold) Regulat | ok |
| 2 | SI 054 of 2022 | sis_corporate | Financial Intelligence Centre (General) Regulations, 2022 | ok |
| 3 | SI 038 of 2021 | sis_corporate | Insurance (Fidelity Fund) Regulations, 2021 | ok |
| 4 | SI 025 of 2019 | sis_corporate |  | pdf_parse_empty |
| 5 | SI 043 of 2017 | sis_corporate |  | pdf_parse_empty |
| 6 | SI 071 of 2015 | sis_corporate | Insurance (Minimum Paid-Up Share Capital) Regulations, 2015 | ok |
| 7 | SI 012 of 2010 | sis_corporate | Income Tax (Tazama Petroleum Products Company Limited) (Appr | ok |
| 8 | SI 042 of 2007 | sis_corporate | National Payment Systems Act (Commencement) Order, 2007 | ok |
| 9 | SI 047 of 1991 | sis_corporate | Insurance Levy (Exemption) Order, 1991 | ok |

## Parent-Act mapping (qualitative)

- **SI 2022/053 + 2022/054** — Financial Intelligence Centre Act, 2010 (Act No. 46/2010) derivatives. The Prescribed Threshold Regulations and General Regulations together form the operational backbone of FIC reporting obligations on cash transactions and reporting entities.
- **SI 2021/038** — Insurance Act, 2021 (Act No. 38/2021) Fidelity Fund Regulations. Operationalises the broker fidelity fund mechanism under the new Insurance Act.
- **SI 2015/071** — Insurance Act, 1997 (Act No. 27/1997) Minimum Paid-Up Share Capital Regulations. Sets capital adequacy thresholds for insurers and reinsurers; superseded but remains relevant for legacy cases.
- **SI 2010/012** — Income Tax Act, Cap. 323 derivative — Tazama Petroleum Products Company Limited approval & exemption order (mineral-exploration concession).
- **SI 2007/042** — National Payment Systems Act, 2007 (Act No. 1/2007) Commencement Order — establishes effective date for NPS regulatory framework.
- **SI 1991/047** — Insurance Levy (Exemption) Order, 1991 — colonial-era insurance levy exemption (corporate finance heritage).

## Integrity checks (batch-scoped)

- **CHECK1 (id uniqueness within batch):** PASS — 7 unique record IDs, none collide with HEAD records or other batch records.
- **CHECK2 (cross-references):** PASS — no `amended_by` / `repealed_by` / `cited_authorities` references emitted (parent-Act linking deferred to a later schema-uplift pass).
- **CHECK3 (source_hash ↔ raw bytes):** PASS — all 7 records' `source_hash` recomputed against on-disk raw PDF and matched.
- **CHECK4 (required schema fields populated):** PASS — all 7 records have id/type/jurisdiction/title/citation/sections/source_url/source_hash/fetched_at/parser_version populated.
- **CHECK5 (provenance entries present):** PASS — provenance.log has entries with `batch=0203` for all 14 ingest URLs (HTML + PDF for each of 7 records) plus 5 discovery URLs (robots.txt + 4 alphabets).

**Note on legacy duplicates:** the corpus-wide ID uniqueness sweep still surfaces 34 pre-existing legacy `act-…` duplicates under `records/acts/` (flat-layout migration not yet completed) — these are unchanged from batches 0192–0202 and are not introduced by this batch.

## Gaps logged

- `si/2019/025` — Income Tax Act (Suspension of Tax on Payment of Interest to Non-Resident) (Treasury Operations) Order — pdf_parse_empty; image-only scanned PDF; OCR backfill deferred.
- `si/2017/043` — Income Tax (Suspension of Tax on Payments to Non-Resident Contractors) (Batoka Hydro) Order — pdf_parse_empty; image-only scanned PDF; OCR backfill deferred.

## Next tick plan

Yield = 7 (≥ 3) → continue sis_corporate. Probes for next tick: alphabet=C (Co-operative Societies / Credit Reference Agency), alphabet=L (Law Reform / Loans / Leasing), alphabet=R (Registrar of Companies / Receivership), alphabet=D (Deposit-Taking / Development Bank). Parent-Act probes: Banking and Financial Services Act 2017/7, Insurance Act 2021/38 (for further derivatives), Securities Act 2016/41 (any post-2021 IPO/Tribunal SIs missed).

Re-verify robots.txt at start of next tick.

If sis_corporate yield <3 next tick, rotate to sis_employment (priority_order item 4) via Employment Code Act 2019/3 derivatives, then sis_data_protection (priority_order item 6) for IBA / Postal Services / Cyber-related SIs.

## Infrastructure follow-up (non-blocking)

- 14 batch-0203 raw SI files on disk (7 HTML + 7 PDF) plus prior unsynced raw bytes from batches 0192–0202 awaiting host-driven `rclone sync raw/ b2raw:kwlp-corpus-raw/`.
- corpus.sqlite stale rollback-journal still blocks in-sandbox FTS rebuild.
- 34 legacy-schema act JSON dupes under records/acts/ + 42 Appropriation-Act -000- placeholder dupes + 63 SI records at top level of records/sis/ (legacy flat layout) remain unresolved.
