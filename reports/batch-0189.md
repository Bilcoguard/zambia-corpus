# Batch 0189 Report

**Phase:** 4 (bulk ingestion)
**Sub-phase:** case_law_scz (priority_order item 5) — mid-2025 ZMSC corridor
**Commit target:** Phase 4 batch 0189: +8 SCZ judgments (case_law_scz continuation — ZMSC 2025/17-24)
**Completed:** 2026-04-24 (UTC)

## Summary

Continues `case_law_scz` per the batch 0188 next-tick plan. Ingested **8**
Supreme Court of Zambia judgments from the mid-2025 corridor (ZMSC
2025/17 — 2025/24), discovered via the cached ZambiaLII ZMSC index
(`raw/zambialii/judgments/zmsc/zmsc-index-page-1-20260424.html`).

| # | Citation | Date | Title (short) | Paragraphs |
|---|---|---|---|---|
| 1 | [2025] ZMSC 24 | 2025-09-19 | Occupational Health and Safety Institute v James Mataliro (APPEAL NO. 12/2025) | 4* |
| 2 | [2025] ZMSC 23 | 2025-04-03 | The Securities and Exchange Commission v Zambia Breweries Plcs and 2 Ors | 46 |
| 3 | [2025] ZMSC 22 | 2025-08-19 | Chama Cheelemu and Ors v Odile Loukombo 'Chelemu' | 61 |
| 4 | [2025] ZMSC 21 | 2025-08-20 | Joseph Chanda v The People | 11 |
| 5 | [2025] ZMSC 20 | 2025-08-20 | Zambia Revenue Authority v Nestlé Zambia Limited | 195 |
| 6 | [2025] ZMSC 19 | 2025-08-13 | Roanbeat Investment Limited v MTN (Zambia) Limited and Anor | 7* |
| 7 | [2025] ZMSC 18 | 2025-08-14 | Emmanuel Tumba and 6 Ors v Zambia Bata Shoe Company Plc | 14 |
| 8 | [2025] ZMSC 17 | 2025-08-13 | Ronald Kaoma Chitotela v Anti-Corruption Commission and 3 Ors | 10 |

*Low paragraph counts (2025/24 = 4, 2025/19 = 7) reflect the pdfplumber
fallback path where the strict `\d+. ` numbered-paragraph regex did not
match the PDF's layout. The records still contain the full extracted
body text segmented by double-newline. No gap was logged because content
was captured; layout-aware re-segmentation is a Phase 5 follow-up.

## Fetches

* 16 fetches (8 AKN HTML + 8 `source.pdf`) from zambialii.org
* Cumulative for 2026-04-24: **216 / 2000** (10.8%)
* User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
* Crawl delay: 6 s (5 s robots.txt + 1 s margin); all requests spaced per `approvals.yaml`

## Provenance

Each record carries:

* `source_url` — `source.pdf` AKN URL
* `source_hash` — `sha256:<64hex>` of the PDF bytes on disk
* `alternate_sources[].source_url` — the AKN HTML landing page used for metadata
* `alternate_sources[].source_hash` — sha256 of the HTML bytes
* `fetched_at` — ISO-8601 UTC at the time of each fetch
* `parser_version` — `0.5.0` (shared with batches 0187-0188)

## Integrity checks (batch-scoped)

| Check | Result | Notes |
|---|---|---|
| CHECK1 batch-id collisions | PASS | 0 new dupes; 34 pre-existing legacy-schema dupes in records/acts/* remain (documented in batch-0187/0188 reports — infrastructure follow-up) |
| CHECK2 cross-refs (amended_by/repealed_by/cited_authorities) | PASS | `cited_authorities` empty this batch per scope |
| CHECK3 source_hash ↔ on-disk PDF | PASS | sha256 re-hashed against raw/zambialii/judgments/zmsc/2025/*.pdf |
| CHECK4 HEAD slot clash | PASS | 8 new (year, number) slots; did not overlap pre-existing ZMSC slots |
| CHECK5 required fields | PASS | id, type, jurisdiction, title, citation, paragraphs, source_url, source_hash, fetched_at, parser_version, court all populated |

## Artefacts written this batch

* 8 JSON records under `records/judgments/zmsc/2025/`
* 16 raw files under `raw/zambialii/judgments/zmsc/2025/` (HTML + PDF pairs)
* `_work/batch_0189_summary.json` and `.batch_0189_state.json`
* `scripts/batch_0189.py`
* `reports/batch-0189.md` (this file)
* Appends to `costs.log`, `provenance.log`, `worker.log`

## Sub-phase status after this batch

* case_law_scz judgment records: **17** total (9 pre-existing + 8 this batch)
* Next tick plan: continue case_law_scz corridor (ZMSC 2025/16, 15, 13, 12,
  11, 10, 9, 8, 7, 6 and the 2024/34-25 block — all discoverable in the
  cached page-1 index), then rotate to sis_data_protection per
  priority_order item 6 once case_law_scz passes ~25 records.

## Non-blocking infrastructure items (unchanged from batch 0188)

* `corpus.sqlite` stale rollback-journal continues to block in-sandbox FTS
  rebuild — human-driven rebuild from `records/` JSON required for Phase 5.
* 34 legacy-schema act dupes at `records/acts/{id}.json` AND
  `records/acts/{year}/{id}.json` remain unresolved (duplicate layout
  detected in batch-0187 pre-scan; not introduced by case_law_scz batches).
* rclone still not available in tick sandbox — B2 raw sync (step 8)
  deferred to host.

## Budgets used

* Daily fetches: 216 / 2000 (10.8%)
* Daily tokens: <<< budget (rough estimate: ~<15k for this tick)

No gaps logged this batch.
