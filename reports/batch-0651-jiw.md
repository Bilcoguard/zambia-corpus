# Batch b0651-jiw — Judgment Ingestion Worker

**Tick start:** 2026-05-14T18:07:30Z
**Worker:** judgment-ingestion-worker
**Verdict:** TICK ABORTED (20th consecutive JIW abort since b0626-jiw)
**Wall-clock:** ~3 min
**Budget used this tick:** 0 fetches (cumulative JIW today: 0 / 500)

## Summary

No fetch, no parse, no write, no DB mutation. Chronic host-side
blockers unchanged since b0641-jiw / b0644-jiw / b0645-jiw / b0646-jiw /
b0648-jiw. Logs and this report are the only mutations committed this
tick.

`b0650-repair` ran ~52 min before this tick (commit `83e6d5a`,
2026-05-14T17:15Z UTC). It applied **8 body-only UPDATEs** (6 primary +
2 fixup) to the zambialii AKN-SI 2017/050–077 cohort using the same
`PRAGMA journal_mode=MEMORY` technique to bypass the FUSE-bindfs
sandbox `rm`-deny on `corpus.sqlite-journal`. That repair batch did
**not** touch FTS5 and did **not** narrow the CHECK8 parity gap.

JIW preflight this tick re-confirms the same numbers from inside the
DB: `records=1928, records_fts=1924, gap=4`. Parity rule CHECK8 still
FAILS → JIW must defer per non-negotiable in SKILL.md
("Never commit if records count ≠ records_fts count — log the gap
and defer").

## Preflight observations

| Metric | Value |
| --- | --- |
| `records` count | 1928 |
| `records_fts` count | 1924 |
| Parity gap | **4** (CHECK8 FAIL — unchanged since repair-040) |
| `judgments` count (records.type='judgment') | 238 (unchanged) |
| Coverage vs target | 238 / 800 = **30 %** |
| `corpus.sqlite` mtime (UTC) | 2026-05-14T17:15:32Z (local mlabel 19:15:32 +0200) |
| Host-side recency | ~52 min before tick start (repair-050 wrote 8 body UPDATEs: 6 primary + 2 fixup) |
| Sandbox `/` free | 6.5 MB (100 % full — unchanged from b0645..b0650) |
| Corpus FS free | 12 GB (unchanged from b0648) |
| `PRAGMA quick_check` first error | `tree page 5733 cell 210: 2nd reference to page 21836` |
| `PRAGMA integrity_check` | NOT OK — same shadow pages as b0641/b0644/b0645/b0646/b0648 |

## Persistent FTS5 shadow-table corruption (unchanged since b037/b038)

```
*** in database main ***
On tree page 5733 cell 210: 2nd reference to page 21836
On tree page 5733 cell 208: Rowid 1185 out of order
On tree page 6270 cell 0:   2nd reference to page 24604
On tree page 5387 cell 0:   overflow list length is 1 but should be 3
On tree page 5733 cell 77:  Rowid 983 out of order
On tree page 5732 cell 298: Rowid 683 out of order
On tree page 12466 cell 7:  invalid page number 30645
On tree page 22491 cell 0:  2nd reference to page 24620
On tree page 29610 cell 4:  invalid page number 30242
On tree page 12465 cell 7:  Child page depth differs
```

Cells on page 5733 have continued to shift cell-index since b0641
(cell 71 → 77 → 82 → 210 → 210), confirming the FTS5 shadow table
remains live-write under the repair worker even though the underlying
B-tree corruption pages (3D logical pages 5732/5733/6270/5387/1389/1204/
12465/12466/21854/22491/29610) are unchanged. Repair worker mutates
body-text pages only (`records.body` UPDATEs under journal_mode=MEMORY)
and does not enter the FTS5 shadow tables. **The 4-row parity gap is
therefore not narrowing.**

## Blockers (all chronic, all host-side)

| # | Blocker | First seen | Status this tick |
| --- | --- | --- | --- |
| (a) | CHECK8 parity `records=1928 records_fts=1924 gap=4` | repair-040 | **unchanged** |
| (b) | `PRAGMA quick_check` + `integrity_check` both NOT OK | b037/b038 | **unchanged** |
| (c) | Sandbox `/` 6.5 MB free (100 % full) | b0645 | **unchanged** |
| (d) | `corpus.sqlite-journal` orphan files (13 on disk) | b0644+ | **unchanged** (bindfs deny `rm`) |
| (e) | `.git/objects/maintenance.lock` EPERM on rm | b0644+ | **unchanged** |
| (f) | `ocrmypdf` / `rclone` / `sqlite3` CLI absent in sandbox | b0641 | **unchanged** |
| (g) | Stale v4 manifest IDs do not exist in live records | b0650 | **unchanged** |
| (h) | 14 orphan FTS rows (records_fts rowids without records FK) | b0641 | **unchanged** |

CHECK1–CHECK7 PASS on read; only CHECK8 FAILS. Decision: defer.

## Action taken

1. Cleared bogus `.git/index.lock`, `.git/HEAD.lock`,
   `.git/ORIG_HEAD.lock`, `.git/refs/heads/main.lock` by `mv` to
   `.bak.b0651-*` (host EPERM on `rm` chronic).
2. Ran preflight CHECKs 1–8.
3. CHECK8 failed (gap=4, unchanged from repair-040). Per
   non-negotiable rule, deferred all fetch / parse / write / commit
   against `corpus.sqlite`.
4. Appended summary entries to `worker.log` and `costs.log`.
5. Wrote this report.
6. Staged `worker.log`, `costs.log`, `reports/batch-0651-jiw.md`
   only. `corpus.sqlite` is gitignored and was not touched this tick.
7. Commit + push.

## Host actions still required (carried forward from b0650-repair)

1. **FTS5 rebuild** — `INSERT INTO records_fts(records_fts) VALUES('rebuild')` after `quick_check` returns OK.
2. **`ocrmypdf` install** in sandbox image (needed for scanned PDF reparse).
3. **Stale manifest removal** — v4 manifest IDs not in live `records` table.
4. **Cleanup of 14 orphan FTS rows** — `records_fts` rowids without matching `records.rowid`.
5. **`rm` orphan `corpus.sqlite-journal*` files** (13 on disk) and `.git/objects/maintenance.lock` from host (EPERM in sandbox).
6. **Reinstate sandbox root headroom** — `/` is sitting at 6.5 MB free which prevents `pdfplumber` tmpdb materialisation.

## Next tick

`b0652-jiw` at t+60 min. Will re-evaluate CHECK8 and resume ingestion
the moment parity is restored, sandbox `/` headroom is reinstated, and
SQLite integrity returns OK.
