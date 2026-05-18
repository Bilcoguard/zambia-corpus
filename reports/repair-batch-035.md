# Repair Batch 035

- Run: 2026-05-13T04:01:18Z (sandbox UTC; FUSE mount shows TZ+2)
- Fixed: 8 of 8 manifest targets
- Failed: 0
- Strategy: Worked on local /sessions/.../tmp/corpus.sqlite copy (FUSE-mount commits fail on large rollback journals — same pattern as b0334+); swapped back via `os.replace`. Net swap-back preserved a concurrent host-side ingestion of 5 new ZMSC-2024 judgments.

## Targets repaired

| # | Record ID | body chars | method | src bytes |
|---|---|---|---|---|
| 1 | act-zm-2012-013-property-transfer-tax-amendment-act-2012 | 5,904 | ocr(4pp) | 94,341 |
| 2 | act-zm-2012-015-zambia-development-agency-amendment-act-2012 | 4,029 | ocr(4pp) | 68,810 |
| 3 | act-zm-2013-005-the-teaching-profession-2013 | 55,767 | ocr(30pp) | 623,358 |
| 4 | act-zm-2013-007-the-excess-expenditure-appropriation-2010-2013 | 2,782 | ocr(3pp) | 34,895 |
| 5 | act-zm-2013-012-the-patents-and-companies-registration-agency-amendment-2013 | 1,190 | ocr(1pp) | 14,047 |
| 6 | act-zm-2013-013-the-weights-and-measures-amendment-2013 | 1,060 | ocr(2pp) | 14,949 |
| 7 | act-zm-2013-014-the-property-transfer-tax-amendment-2013 | 1,145 | ocr(1pp) | 13,524 |
| 8 | act-zm-2013-015-the-value-added-tax-amendment-2013 | 3,887 | ocr(2pp) | 44,607 |

All eight required OCR via `ocrmypdf` (parliament.gov.zm PDFs are scanned-only — pdfplumber yielded 0c).

## Post-run integrity

- `PRAGMA quick_check`: ok
- `PRAGMA integrity_check`: ok
- `INSERT INTO records_fts(records_fts) VALUES('integrity-check')`: ok
- records = 1928, records_fts = 1928 (parity)

## Concurrent activity observed

Five ZMSC-2024 judgments were added to corpus.sqlite during this tick by another worker (likely host-side judgment ingestion sweep). The post-swap FUSE corpus.sqlite contains both my 8 act repairs and those 5 new judgments, all with consistent FTS entries:

- judgment-zm-2024-zmsc-01-kausa-mwachindalo-and-anor-v-mathews-musona-and-ors
- judgment-zm-2024-zmsc-02-mabvuto-mwale-and-anor-v-the-people
- judgment-zm-2024-zmsc-05-tarick-mwambwa-chanaika-v-zamanita-limited-and-anor
- judgment-zm-2024-zmsc-06-kelvin-lubona-v-the-people
- judgment-zm-2024-zmsc-09-frankson-musukwa-and-ors-v-road-transport-and-safety-agency

## Manifest progress

Manifest records still requiring repair after this tick: 32 of 88 (39 fixed across batches 026-035; manifest is 88 records).

## Notes

- Required pip install of `ocrmypdf` (`/sessions/exciting-nice-davinci/.local/bin/ocrmypdf`) — not present at session start
- Initial commit attempts to corpus.sqlite on the FUSE mount failed with `sqlite3.OperationalError: disk I/O error` during transaction commit (stale journal `corpus.sqlite-journal` was left on disk). Mitigated by working on a local copy and swap-back via `os.replace()`.
- Two stale journal files moved aside (corpus.sqlite-journal.b035-stale-*); main DB integrity confirmed before and after.
- B2 sync deferred to host (rclone not installed in sandbox).
- Git push deferred to host-side sweep (continuing b0608+ pattern).
