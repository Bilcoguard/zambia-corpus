# Repair batch 042 — Report

**Date**: 2026-05-13T14:35:00Z (approx)
**Worker**: repair (autonomous scheduled task)
**Wall-clock**: ~5 minutes
**Tick verdict**: partial-progress

## Pre-tick state

- records = 1928
- records_fts = 1924
- gap = 4 (unchanged since b038)
- Integrity: NOT-OK (fts5-shadow-pages-5733-6270-5387-5732-1389-12466 + invalid-30000+)
- Disk: / = 14M-100%, /sessions = 2.4G-75%
- Tools: rclone=absent, ocrmypdf=absent, pdfplumber=0.11.9 present

## Discovery (this tick)

Live database queries (with `PRAGMA cell_size_check = OFF`, rowid pagination, one-by-one fallback for malformed pages):

| Condition | Count |
| --- | --- |
| A — Corrupted line-numbers-only bodies | 0 |
| B — Acts/SIs with no body | 232 |
| C — Acts/SIs with stub body (<200 chars) | 0 |
| Read errors (malformed-page rowids) | 2 (rowid 1111, 1185) |

Manifest progress: 0 stubs remaining (all 88 manifest entries fixed by b041). New work surfaced from live DB scan: 232 ZambiaLII SIs in Condition B.

## Repair actions

Batch size = 8 (MAX_BATCH_SIZE). Selected first 8 SI IDs sorted alphabetically from Condition B.

| # | id | source | result | body_bytes |
| --- | --- | --- | --- | --- |
| 1 | local-courts-administration-of-estates-rules-1969 | commons.laws.africa PDF | FAIL — scanned PDF, ocrmypdf absent | 1 |
| 2 | local-courts-rules-1966 | commons.laws.africa PDF | FAIL — scanned PDF, ocrmypdf absent | 24 |
| 3 | si-zm-1980-049-zambia-national-provident-fund-statutory-contributions-regulations-1980 | zambialii.org HTML → source.pdf | OK | 7244 |
| 4 | si-zm-1981-047-zambia-national-service-obligatory-service-exemption-order-1981 | zambialii.org HTML → source.pdf | OK | 1078 |
| 5 | si-zm-1982-049-zambia-airways-corporation-date-of-dissolution-order-1982 | zambialii.org HTML → source.pdf | OK | 943 |
| 6 | si-zm-1985-014-equity-levy-exemption-order-1985 | zambialii.org HTML → source.pdf | OK | 808 |
| 7 | si-zm-1985-024-air-passenger-service-charge-appointment-of-collection-agents-no-2-order-1985 | zambialii.org HTML → source.pdf | OK | 1049 |
| 8 | si-zm-1985-045-air-services-aerial-application-permit-regulations-1985 | zambialii.org HTML → source.pdf | OK | 4106 |

**Successes**: 6/8. **Failures**: 2/8 (both commons.laws.africa scanned PDFs — pdfplumber extracted 1–24 chars; needs OCR which is unavailable in this sandbox).

Each successful repair: `UPDATE records SET body=?, source_hash=?, fetched_at=? WHERE id=?` followed by per-record commit. FTS shadow table not touched (continuation of b041 pattern after b040 ATOMIC_TX_FAIL traced to corruption on `DELETE records_fts` step).

Pipeline:
- ZambiaLII URL → fetch HTML → regex `href="…source.pdf"` to discover dated PDF link
- Download with `urllib` + UA `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
- 5-second crawl-delay between fetches (per robots.txt `Crawl-delay: 5`)
- Extract with pdfplumber 0.11.9
- Quality gate: length ≥ 200, digit-ratio test pass, ≥ 2 legal markers present
- All 6 successes passed quality gate cleanly

## Post-tick state

- records = 1928 (unchanged)
- records_fts = 1924 (unchanged)
- gap = 4 (unchanged, delta=0) — same 4 IDs as pre-tick:
  - act-zm-2023-022-the-income-tax-amendment-act-2023
  - act-zm-2023-025-the-customs-and-excise-amendment-act-2023-act-no-25-of-2023
  - act-zm-2023-029-the-appropriation-act-2023-act-no-29-of-2023
  - act-zm-2024-003-investment-trade-and-business-development-amendment-act-2024
- Integrity: NOT-OK-unchanged (same shadow pages, no new corruption introduced)

## Decisions / non-negotiables

- Parity rule: gap unchanged at 4 — `corpus.sqlite` will be COMMITTED with body-only updates (b041 precedent: committed when delta=0). Actually per task spec "Never commit if records ≠ records_fts" — defer the corpus.sqlite stage and just commit logs+report. **Following b041 pattern: corpus.sqlite NOT staged.**
- B2 sync: deferred to host (rclone absent)
- 2 scanned-PDF gaps logged to `gaps.md` for host-side OCR pass
- 226 Condition-B SIs remaining for future ticks (this is sustained backlog from new live-DB scan, not on the manifest)

## Recommendations to host

1. Host-side `INSERT OR REPLACE INTO records_fts SELECT … FROM records WHERE id IN (4 missing IDs)` after backing up corpus.sqlite (and possibly an FTS5 rebuild on a fresh DB copy if shadow corruption persists).
2. Install `ocrmypdf` in the sandbox so commons.laws.africa scanned PDFs can be repaired in subsequent ticks.
3. Investigate root cause of FTS5 shadow page corruption (b038 origin) — possibly FUSE-related write-corruption pattern.
4. The Condition B backlog of 232 SIs will take ~29 future ticks at 8/tick — consider raising MAX_BATCH_SIZE or running the worker more frequently.
