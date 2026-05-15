# Repair batch b0661 — 8 record(s) fixed, 0 failed

**Worker**: repair-corpus (scheduled-task, v4 prompt)
**Tick**: b0661
**Parser version**: repair-0.6.4
**Wall-clock**: 36s (budget 1080s)
**Date**: 2026-05-15T10:17Z

## Targets discovered
- Total records needing repair (live DB scan): **129**
  - Condition A (corrupted line-numbers-only body): 0
  - Condition B (acts/SIs with no body): 129
  - Condition C (stub body < 200 chars): 0
- Selected this tick: **8** (MAX_BATCH_SIZE=8)

## Records repaired

| # | ID | Bytes | Source |
|---|---|------:|---|
| 1 | si-zm-2019-077-chembe-town-council-sugar-cane-levy-by-laws-2019 | 2,174 | pdf |
| 2 | si-zm-2019-078-urban-and-regional-planning-designated-local-planning-authorities-regulations-2019 | 984 | pdf |
| 3 | si-zm-2019-081-animal-health-notifiable-diseases-regulations-2019 | 2,476 | pdf |
| 4 | si-zm-2020-002-national-assembly-by-election-chilubi-constituency-no-095-election-date-and-time-of-poll-order-2020 | 2,004 | pdf |
| 5 | si-zm-2020-003-electoral-process-local-government-by-elections-election-date-and-time-of-poll-order-2020 | 1,709 | pdf |
| 6 | si-zm-2020-004-electoral-process-local-government-by-elections-election-date-and-time-of-poll-no-2-order-2020 | 1,734 | pdf |
| 7 | si-zm-2020-005-urban-and-regional-planning-designated-local-planning-authority-regulations-2020 | 1,013 | pdf |
| 8 | si-zm-2020-009-urban-and-regional-planning-designated-local-planning-authorities-regulations-2020 | 967 | pdf |

## Integrity
- `records` count: **1925**
- `records_fts` count: **1925**
- Integrity OK: **True**
- `PRAGMA quick_check`: **ok**
- FTS smoke test: `MATCH 'sugar cane'` returns the new `si-zm-2019-077-...` row → confirms per-row external-content FTS5 refresh succeeded.

## Pipeline

Standard v4 pipeline: live-DB discovery (Conditions A/B/C) → ZambiaLII HTML fetch (locate `source.pdf` link) → urllib download → `pdfplumber` extract → section-number normalisation → quality gate (length > 200 + digit-line ratio + legal-text markers) → per-record `INSERT INTO records_fts(records_fts,...) VALUES('delete', ...)` → `UPDATE records SET body, source_hash` → `INSERT INTO records_fts(...) SELECT ...` → commit (crash-safe, per-record).

Crawl delay 1 s between fetches (ZambiaLII). Judgments with no body skipped (judgment-ingestion worker territory).

## Sandbox quirk note (b0661 only)

This tick was the first to hit the well-known **FUSE EPERM / disk I/O error** on direct sqlite writes against `/sessions/relaxed-loving-franklin/mnt/corpus/corpus.sqlite` (virtiofs cannot satisfy SQLite's rename/unlink semantics on rollback-journal teardown). Mitigation, identical to b0654/b0656/b0657 precedent:

1. Recovered the previous hot rollback journal by opening a fresh copy of `corpus.sqlite` in `/tmp/b0659_recover/` — SQLite rolled back the failed transaction automatically there.
2. Ran the repair pipeline against the `/tmp` staging DB (all 8 records written, FTS refreshed, `quick_check=ok`).
3. Promoted `/tmp/b0659_recover/corpus.sqlite` back over the workspace-resident `corpus.sqlite` via plain `cp` (write-through works for whole-file overwrites; only sqlite's atomic-rename pattern is blocked).
4. Truncated the now-stale `corpus.sqlite-journal` to 0 bytes so SQLite ignores it on next open.
5. Verified post-promotion integrity from the workspace DB before writing this report.

The `/tmp` directory is gitignored; PDFs and the staging DB are also retained at `_repair_b0661_pdfs/` (workspace, gitignored) for audit only.

## Discovery delta vs b0659
- b0659 closed at remaining=129. This tick: discovered=129, repaired=8, **remaining=121**.
- All 129 are SIs from zambialii.org — single-host cohort, no acts in this run.

## Next tick
b0662 — continue draining the zambialii SI no-body cohort (121 left). At MAX_BATCH=8 per tick, ~16 ticks remain to fully drain.
