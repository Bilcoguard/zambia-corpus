# Batch 0190 Report

**Phase:** 4 (bulk ingestion)
**Sub-phase:** case_law_scz (priority_order item 5) — mid-2025 ZMSC corridor (block 3)
**Commit target:** Phase 4 batch 0190: +8 SCZ judgments (case_law_scz continuation — ZMSC 2025/16, 15, 13, 12, 11, 10, 9, 8)
**Completed:** 2026-04-24 (UTC)

## Summary

Continues `case_law_scz` per the batch 0189 next-tick plan. Ingested **8**
Supreme Court of Zambia judgments from the mid-2025 corridor (ZMSC
2025/8 through ZMSC 2025/16, skipping 2025/14 which is absent from the
cached ZambiaLII ZMSC index), discovered via
`raw/zambialii/judgments/zmsc/zmsc-index-page-1-20260424.html`.

| # | Citation | Date | Title (short) | Paragraphs |
|---|---|---|---|---|
| 1 | [2025] ZMSC 16 | 2025-07-24 | The Attorney General v Rajan Mahthani (Appeal No. 4 of 2020) | 81 |
| 2 | [2025] ZMSC 15 | 2025-07-25 | The Attorney General and Anor v Metro Investments Limited and Ors | 16 |
| 3 | [2025] ZMSC 13 | 2025-05-19 | Zambia China Economic Trade Cooperation Development Ltd v Zambia Jihai Agriculture Co Ltd | 57 |
| 4 | [2025] ZMSC 12 | 2025-05-21 | Pemba Lapidaries Limited and Anor v William Saunders | 20 |
| 5 | [2025] ZMSC 11 | 2025-04-29 | Henry Nyambe and 9 Ors v Lumwana Mining Company Limited | 28 |
| 6 | [2025] ZMSC 10 | 2025-04-17 | Thelma Maunga (admin estate Suzyo Nyika) and Ors — judgment | 50 |
| 7 | [2025] ZMSC 9  | 2025-04-08 | Attorney General v Rajan Mahthani (Appeal No. 4 of 2020) | 120 |
| 8 | [2025] ZMSC 8  | 2025-03-28 | Faustine Kabwe and Anor v Ndola Trust School Limited and Anor | 28 |

Note on 2025/9 vs 2025/16: both neutral citations arise from the same
appeal docket (Supreme Court Appeal No. 4 of 2020 — Attorney General v
Rajan Mahthani) but deliver distinct rulings on 2025-04-08 and
2025-07-24 respectively (a preliminary decision and a later
substantive/costs ruling). Record IDs are kept distinct via the ZMSC
number prefix (`-zmsc-09-` vs `-zmsc-16-`); no slot collision in HEAD.

ZMSC 2025/14 is not present in the cached page-1 index and is skipped
rather than probed blindly — the AKN URL scheme requires a known
delivery date slug, and attempting to fetch an unlisted slot would
incur a speculative 404. If ZambiaLII later publishes 2025/14, it will
be picked up by a subsequent discovery refresh.

## Fetches

* 16 fetches (8 AKN HTML + 8 `source.pdf`) from zambialii.org
* Cumulative for 2026-04-24: **232 / 2000** (11.6%) after this batch
* User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
* Crawl delay: 6 s (5 s robots.txt + 1 s margin); all requests spaced per `approvals.yaml`

## Provenance

Each record carries:

* `source_url` — `source.pdf` AKN URL
* `source_hash` — `sha256:<64hex>` of the PDF bytes on disk
* `alternate_sources[].source_url` — the AKN HTML landing page used for metadata
* `alternate_sources[].source_hash` — sha256 of the HTML bytes
* `fetched_at` — ISO-8601 UTC at the time of each fetch
* `parser_version` — `0.5.0` (shared with batches 0187-0189)

## Integrity checks (batch-scoped)

| Check | Result | Notes |
|---|---|---|
| CHECK1 no-dup-ids (batch) | PASS | 8 unique record IDs within this batch |
| CHECK2 xref resolve | PASS | `cited_authorities` empty this batch per scope; `amended_by`/`repealed_by` N/A for judgments |
| CHECK3 source_hash ↔ on-disk PDF | PASS | sha256 re-hashed against `raw/zambialii/judgments/zmsc/2025/*.pdf` — 8/8 match |
| CHECK4 required fields | PASS | id, type, jurisdiction, title, citation, paragraphs, source_url, source_hash, fetched_at, parser_version, court — all populated |
| CHECK5 slot uniqueness | PASS | 8 unique (year, number) slots; no overlap with HEAD's 17 pre-existing ZMSC slots |

## Artefacts written this batch

* 8 JSON records under `records/judgments/zmsc/2025/`
* 16 raw files under `raw/zambialii/judgments/zmsc/2025/` (HTML + PDF pairs)
* `_work/batch_0190_summary.json` and `.batch_0190_state.json`
* `scripts/batch_0190.py`
* `reports/batch-0190.md` (this file)
* Appends to `costs.log`, `provenance.log`, `worker.log`

## Sub-phase status after this batch

* case_law_scz judgment records: **25** total (17 pre-existing + 8 this batch)
* Coverage window now unbroken from ZMSC 2025/8 up through 2025/25, 27,
  29, 30 and 2026/1, 4, 7, 10 (plus the batch-3 pilot at
  `judgment-zm-2026-scz-09-konkola-v-ag`).
* Gaps in 2025 ZMSC corridor per current ZambiaLII page-1 index:
  2025/14 (not listed), 2025/26 (not listed), 2025/28 (not listed).
  These will be documented in `gaps.md` on the next discovery refresh
  that includes pages 2+ of the ZMSC index; for now they remain in
  an "unlisted upstream" state and not logged as worker gaps.
* Next tick plan: per BRIEF.md — rotate from case_law_scz (25 records
  now crosses the ~25-record threshold flagged in batch-0189) to
  `sis_data_protection` (priority_order item 6). Discovery step needed:
  fetch the ZambiaLII subsidiary-legislation index filtered for the
  Data Protection Act, 2021 parent act, probably via
  `https://zambialii.org/legislation/subsidiary-legislation?parent=...`
  — the exact filter URL is to be confirmed in batch 0191's first sub-tick.

## Non-blocking infrastructure items (unchanged from batch 0189)

* `corpus.sqlite` stale rollback-journal continues to block in-sandbox
  FTS rebuild — human-driven rebuild from `records/` JSON required for
  Phase 5.
* 34 legacy-schema act dupes at `records/acts/{id}.json` AND
  `records/acts/{year}/{id}.json` remain unresolved (duplicate layout
  detected in batch-0187 pre-scan; not introduced by case_law_scz
  batches).
* rclone still not available in tick sandbox — B2 raw sync (step 8)
  deferred to host.

## Budgets used

* Daily fetches: 232 / 2000 (11.6%) after this batch
* Daily tokens: <<< budget

No gaps logged this batch.
