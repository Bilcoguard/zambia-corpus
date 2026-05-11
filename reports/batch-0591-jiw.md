# Batch 0591 — Judgment-Ingestion-Worker

**Date:** 2026-05-11T17:18:00Z
**Worker:** judgment-ingestion-worker
**Sweep:** Court of Appeal — judiciaryzambia.com, page 4 overflow (2) + page 5 partial (6)
**Parser:** v0.3.8-inline
**User-Agent:** `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
**Cumulative fetches today:** 58/500

## Summary

- **8 PDFs fetched and parsed** successfully (all CoA-pattern posts)
- **3 records inserted** (Mweene Mwiinga, Pilatus Engineering, Nimble Resources)
- **1 dedupe-case-number collision** deferred (FQM Trident vs Mukuka Mumba) — pre-existing parser-drift record blocks insertion
- **4 records deferred-fts5** due to pre-existing FTS5 corruption (records_fts_data pages 14599, 28316–28340)
- **0 confirmed-404**
- **CHECK1..CHECK8 all PASS** for inserted records — final state: `records=1892 records_fts=1892 (eq)` + `judgments_meta=202`

## Inserted records

| ID | Case Number | Date Decided | Outcome | Judges |
|----|-------------|--------------|---------|--------|
| judgment-zm-2025-coa-038-mweene-mwiinga-v-the-attorney-general-4-others | APP/038/2025 | 2025-11-05 | set-aside | Makungu, Muzenga, Chembe JJA |
| judgment-zm-2025-coa-108-pilatus-engineering-company-limitedjoseph-huiler-v-alfred-kalwani | APPLICATION/108/2024 | 2025-12-04 | dismissed | Chashi, Ngulube, Banda-Bobo JJA |
| judgment-zm-2025-coa-105-nimble-resources-limited-v-alex-katamfya | APP/105/2023 | 2025-12-05 | allowed | Kondolo SC, Majula, Muzenga JJA |

## Deferred — dedupe-case-number-collision (1)

`judgment-zm-2025-coa-091-fqm-trident-limited-v-mukuka-mumba` — case_number `APP/091/2024` matches pre-existing `judgment-zm-2022-coa-091-douglas-aaron-simukonda-v-the-people` (date_decided 2022-12-02, source URL `app-91-2024-douglas-aaron-simukonda-vs-the-people`). Both are real, distinct cases sharing the same App. No. designation. Strict dedupe rule applied → skipped insertion; raw PDF preserved at `raw/judiciary-zm/coa/app-91-2024-fqm-trident-limited-vs-mukuka-mumba-coram-kondolo-sc-banda-bobo-muzenga-jja-2.pdf`. **Human review required** to resolve.

## Deferred — deferred-fts5 (4)

FTS5 corruption (`database disk image is malformed`) on `records_fts` insert triggers ROLLBACK of full transaction (records + judgments_meta + records_fts), preserving CHECK8 invariant. Awaiting repair-worker FTS5 drop+recreate.

- judgment-zm-2024-coa-083-felix-nkululumbwe-v-charles-musonda-17-others-attorney-general (APP/083/2021, 2024-12-24, dismissed; Kondolo SC, Makungu, Sharpe-Phiri JJA)
- judgment-zm-2026-coa-109-jervis-zimba-v-sankana-general-dealers (APP/109/2023, 2026-01-27, dismissed; Kondolo SC, Majula, Muzenga JJA)
- judgment-zm-2026-coa-128-robert-mwanza-v-mtn-zambialimited (APP/128/2023, 2026-01-27, allowed; Kondolo SC, Majula, Muzenga JJA)
- judgment-zm-2026-coa-206-mutale-chanda-v-ian-musweu (APP/206/2024, 2026-01-13, dismissed; Chashi, Makungu, Banda-Bobo JJA)

Total deferred-fts5 backlog: **11 records** (7 from b0590 + 4 here).

## Parser improvements (v0.3.8-inline over v0.3.7)

- **PDF-body Coram extraction** replaces fragile URL-slug judge parsing (handles `KONDOLO SC, MAKUNGU, SHARPE-PHIRI JJA` and `Kondolo, SC, Majula and Muzenga, JJA` cleanly via right-to-left role propagation + SC suffix attachment).
- **PDF-body date extraction** via `On <date1> and <date2>` two-date pattern (uses 2nd date as decision date) with ordinal/typo tolerance for `5l h`, `51h`, `t`, `'` OCR artifacts.
- **Date stamp fallback** scans first 1500 chars for `DD MON YYYY` stamps (e.g., `05 DEC 2025`, `13 JAN 2026`).
- **Outcome patterns extended**: `appeal is consequently dismissed`, `grounds of appeal lack merit and are dismissed`, `application to stay execution fails`, `find no merit in this application/appeal`, `partially succeeds`, allowed/dismissed up to 3 words apart.

## CHECK results

- CHECK1 (≥1 judge per record): PASS — 3 judges each on all 3 inserted
- CHECK2 (issue_tags non-empty): PASS
- CHECK3 (outcome ∈ enum): PASS — set-aside, dismissed, allowed
- CHECK4 (judges resolve in registry): PASS — Makungu, Muzenga, Chembe, Chashi, Ngulube, Banda-Bobo, Kondolo SC, Majula all pre-existing
- CHECK5 (no duplicate IDs): PASS
- CHECK6 (raw_sha256 == on-disk sha): PASS
- CHECK7 (no duplicate case_name+court+date): PASS
- CHECK8 (records.count == records_fts.count): PASS (1892 == 1892)

## Execution

Inline runner; corpus.sqlite isolated to `/tmp/b0591/corpus.sqlite.work` for write-stage to avoid virtiofs disk-IO errors; atomic copy-back via `shutil.copy2`. No derivative script committed (sandbox-session safety constraint, per b0548..b0590 precedent). Pre-tick backup: `corpus.sqlite.bak.b0591-pre-20260511T171614Z` (116,457,472 bytes).

## Next tick (b0592)

`judiciary-coa-sweep: page 5 remaining` — 3 unprocessed CoA candidates on page 5 (appeal-210-clifford-simfukwe, appeal-291-bank-of-zambia-v-bernard-fundi, appeal-304-julian-sichalwe), then advance to page 6.
