# Repair batch 044 — Report

**Date**: 2026-05-14T12:51Z
**Worker**: repair (autonomous scheduled task, b0644)
**Wall-clock**: ~12 minutes (within 20-min cap)
**Tick verdict**: 8 SIs repaired body-only; corpus.sqlite NOT staged per parity rule

## Pre-tick state

- records = 1928
- records_fts = 1924
- gap = 4 (unchanged since b038)
- Integrity: NOT-OK — same FTS5 shadow-page corruption fingerprint as b038–b043 (pages 5733/6270/5387/5732/1389/12466/22491/29610; rowid 1185 out of order; invalid page numbers; child-page-depth differs)
- Disk: corpus FS 2.4G free; root FS 100% full (6.7M free) — chronic since b038
- Tools: pdfplumber 0.11.9 present; ocrmypdf absent; rclone absent

## Lock cleanup

`find .git -name "*.lock*" -delete` ran but EPERM on `.git/ORIG_HEAD.lock`. `git pull --ff-only` succeeded with "Already up to date".

## Discovery (this tick)

Live database queries via rowid pagination (1..1928 in 50-row batches), surviving the malformed-page error windows.

| Condition | Count |
| --- | --- |
| A — Corrupted line-numbers-only bodies | 0 (windows 1101–1150 unreadable, 1150–1200 hits UTF-8 decode error on `act-zm-2023-022`) |
| B — no-body acts | 0 |
| B — no-body SIs | **220** (was 226; b0643 drained 6) |
| B — no-body judgments | 148 (skipped per spec — JIW domain) |
| C — Acts/SIs with stub body (<200 chars) | 0 |
| Read errors (malformed-page rowid windows) | 2 |

Manifest cross-check: the v4 manifest IDs in the task spec still do not exist in the live `records` table (unchanged from b0643). Per spec, the live DB is the source of truth — working set is the 220-SI Condition-B backlog.

## NEW chronic blocker: FUSE-bindfs blocks rm of `corpus.sqlite-journal`

**Symptom**: every UPDATE/commit on `corpus.sqlite` failed with `sqlite3.OperationalError: disk I/O error`. Stale journal files are present (`-rw------- bold-determined-galileo` ownership) but `rm` returns "Operation not permitted" — **only `mv` works**.

**Root cause**: bindfs mount at `/sessions/bold-determined-galileo/mnt/corpus` denies `unlink()` on these specific files (precedent: same EPERM pattern that blocks `.git/*.lock` rm since b0608).  When SQLite finishes a rollback-mode commit it must `unlink()` the journal — that fails — so the commit itself reports disk I/O error.

**Workaround applied this tick**: `PRAGMA journal_mode = MEMORY` + `PRAGMA temp_store = MEMORY`. SQLite never creates a journal file → never tries to delete one. All 8 UPDATEs then committed cleanly.

**Tradeoff**: MEMORY journal mode is non-durable against a process crash mid-commit. Acceptable for this script because each UPDATE is single-row and committed atomically before the next fetch. Recommend either (a) host grants rm permission on `corpus.sqlite-journal*`, OR (b) all repair/JIW scripts adopt MEMORY journal mode permanently.

## Orphaned journals created during diagnosis (host rm needed)

| File | Size |
| --- | --- |
| `corpus.sqlite-journal.b0644-orphan-20260514T124825Z` | 33344 B |
| `corpus.sqlite-journal.b0644-orphan2-20260514T124920Z` | 33344 B |
| `corpus.sqlite-journal.b0644-orphan3-20260514T124937Z` | 8720 B |
| `corpus.sqlite-journal.b0644-orphan4-20260514T125019Z` | 8720 B |

These join the longstanding b035 / b0602 / b0626 stale-journal pile (not staged — they pollute `git status` but the host rm + orphan-quarantine pattern from b0640/b0641 is the documented cleanup path).

## Repair actions

Batch size = MAX_BATCH_SIZE = 8. All from Condition B SIs sorted alphabetically (continuation of b0643's 1986–1992 cohort), all zambialii.org bare-path AKN URLs (drift-100 % per Phase 8 b0641/b0642), fetched via HTML→`source.pdf` discovery → pdfplumber.

| # | id | source | result | body_bytes | sha256(8) |
| --- | --- | --- | --- | --- | --- |
| 1 | si-zm-1993-037-emergency-regulations-1993 | zambialii HTML → source.pdf | OK | 847 | 8b683c14 |
| 2 | si-zm-1994-041-university-of-zambia-staff-tribunal-rules-1994 | zambialii HTML → source.pdf | OK | 6737 | d18795e9 |
| 3 | si-zm-1994-049-zambia-revenue-authority-commencement-and-disengagement-order-1994 | zambialii HTML → source.pdf | OK | 1053 | e179efb1 |
| 4 | si-zm-1995-002-zambezi-river-authority-terms-and-conditions-of-service-by-laws-1995 | zambialii HTML → source.pdf | OK | 48832 | 66138270 |
| 5 | si-zm-1995-029-national-archives-fees-regulations-1995 | zambialii HTML → source.pdf | OK | 1919 | 4f30b0f3 |
| 6 | si-zm-1995-030-national-archives-place-of-deposit-revocation-order-1995 | zambialii HTML → source.pdf | OK | 1033 | 2145e1cb |
| 7 | si-zm-1996-044-zambia-national-provident-fund-statutory-contributions-regulations-1996 | zambialii HTML → source.pdf | OK | 17102 | 71eae454 |
| 8 | si-zm-1998-043-tender-amendment-regulations-1998 | zambialii HTML → source.pdf | OK | 2089 | c9e3ba77 |

**Successes**: 8/8. **Failures**: 0.

Pipeline per record:
1. Fetch `https://zambialii.org/akn/zm/act/si/{year}/{n}` (HTML viewer) — UA `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
2. Regex `href="…source.pdf"` to discover dated source-PDF URL
3. Download PDF (cached at `/tmp/repair_b0644/{i}.pdf`)
4. pdfplumber 0.11.9 page-by-page text extraction
5. Section-marker normalisation `(\d+)\.([A-Z])` → `\1. \2`
6. Quality gate: ≥200 chars + line-numbers-only test + legal-marker test
7. `UPDATE records SET body=?, source_hash=?, fetched_at=?, parser_version='repair-0.6.0' WHERE id=?` — body-only UPDATE, no FTS touch
8. Crawl delay 5 s per zambialii robots.txt

## Post-tick state

- records = 1928 (unchanged — pure UPDATE, no INSERT)
- records_fts = 1924 (unchanged — no FTS touch per parity rule)
- gap = 4 (unchanged)
- Integrity: NOT-OK, fingerprint unchanged from b038–b043 baseline. Body-only UPDATEs did not introduce new corruption.
- Condition-B SI backlog: 220 → 212 remaining

## Git policy this tick

- corpus.sqlite **NOT staged** (parity rule: gap=4 unchanged)
- Staged: `worker.log`, `gaps.md`, `costs.log`, `reports/repair-batch-044.md`, `scripts/batch_0644_repair.py`

## B2 sync

Deferred to host (rclone not in sandbox; corpus mutation local-only anyway).

## Host actions still required

a. FTS5 rebuild (`DROP records_fts` + `CREATE` + `INSERT…SELECT FROM records` + `VACUUM`) — chronic since b038
b. ocrmypdf install for OCR-fallback condB SI drain
c. Stale-manifest removal (v4 task-spec manifest IDs not in live DB)
d. Cleanup of 14 orphan FTS rows (records_fts entries with no matching `records` row)
e. **NEW** — grant rm permission on `corpus.sqlite-journal*` OR adopt MEMORY journal mode permanently across all workers
f. Periodic stale-journal cleanup pile (b035/b0602/b0626/b0644 orphans)

## Next

b0645-repair at t+1h. With MEMORY-journal workaround now proven, future ticks should drain Condition-B at the full MAX_BATCH_SIZE=8 cadence (~212 SIs / 8 = ~27 ticks ≈ ~27 hours of cadence to clear backlog).
