# Batch report: b0630-jiw (judgment-ingestion-worker abort)

**Timestamp**: 2026-05-13T08:08:00Z
**Verdict**: Tick aborted — 4th consecutive JIW abort
**Records written**: 0
**Records deferred**: 0
**Wall clock**: ~2 minutes
**Budget consumed this tick**: 0 fetches (cumulative_today = 21/500)

## Blockers

1. **CHECK8 fails**: `records` = 1928, `records_fts` = 1920, gap = 8.
   The 8 missing FTS rows correspond to b037-repair targets (2023-019, 020, 022, 025, 026, 028, 029 + 2024-003) per b038 forensic.
2. **FTS5 shadow-table corruption** (per b038 finding) — blocks the write path. `PRAGMA quick_check` returns "database disk image is malformed" with B-tree pages 5733/6270 holding 2nd references to FTS shadow pages 21836/21821/24604/etc.
3. **Sandbox `/` is 100 % full** (15 MB free; `/sessions` has 2.4 GB free). Blocks `pdfplumber` /tmp use and multi-row FTS5 commits per b0626-jiw forensic.
4. **Pattern**: 4 consecutive JIW aborts since b0626-jiw at 2026-05-13T05:18Z.

## Read-path state

- `corpus.sqlite` mtime: 2026-05-13T07:11:09Z (quiescent ~57 min).
- `corpus.sqlite-journal`: 0 bytes, stale.
- CHECK1–CHECK7 pass on the read path (no iteration of new records; no inserts attempted).
- CHECK8 fails (records ≠ records_fts).

## Actions taken

- Logged abort to `worker.log`, `costs.log`, `gaps.md`.
- Wrote this report to `reports/`.
- Read-only diagnostics only — no fetch, no parse, no write to `corpus.sqlite`.
- No git commit of corpus mutation (this report + log appends will be committed as the only non-mutating bookkeeping).

## Recommendations (operator)

- **Highest priority**: host-side rebuild of FTS5 shadow tables (DROP/CREATE/INSERT-SELECT/VACUUM). Until this is repaired, all corpus writers are blocked.
- Second priority: sandbox `/tmp` rotation so the next JIW UID can write to `/tmp` for `pdfplumber` working files.
- The "5 consecutive zero-discovery / aborted ticks" threshold for the JIW worker stands at 4 of 5 — this should NOT flip `complete: true`; surface as a chronic-blocker handoff.
