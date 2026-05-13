# Batch b0640-jiw — Judgment Ingestion Worker

**Tick start:** 2026-05-13T21:07:56Z
**Worker:** judgment-ingestion-worker
**Verdict:** TICK ABORTED (14th consecutive JIW abort since b0626-jiw)
**Wall-clock:** ~4 min
**Budget used this tick:** 0 fetches (cumulative today: 21 / 500)

## Summary

No fetch, no parse, no write, no DB mutation. Chronic host-side blockers
unchanged since b0639-jiw. Logs and this report are the only mutations
committed this tick.

## Preflight observations

| Metric | Value |
| --- | --- |
| `records` count | 1928 |
| `records_fts` count | 1924 |
| Parity gap | **4** (CHECK8 FAIL) |
| `judgments` count | 238 |
| Coverage vs target | 238 / 800 = **30 %** |
| `corpus.sqlite` mtime | 2026-05-13T12:36:48Z |
| Host-side quiescent for | ~8.5 h |
| Sandbox `/` free | 14 MB (100 % full) |
| `/sessions` free | 2.4 GB |
| Corpus FS free | 15 GB |
| `PRAGMA quick_check` | NOT OK |
| `PRAGMA integrity_check` | NOT OK |

## Persistent FTS5 shadow-table corruption (unchanged since b037/b038)

```
On tree page 5733 cell 71: 2nd reference to page 21836
On tree page 5733 cell 69: Rowid 1185 out of order
On tree page 6270 cell 0: 2nd reference to page 24604
On tree page 5387 cell 0: overflow list length is 1 but should be 3
On tree page 5732 cell 455: 2nd reference to page 24606
On tree page 5732 cell 439: 2nd reference to page 21821
On tree page 5732 cell 262: 2nd reference to page 21850
On tree page 1389 cell 1: 2nd reference to page 24628
On tree page 1204 cell 1: 2nd reference to page 24603
On tree page 12466 cell 7: invalid page number 30645
...
```

## Missing FTS rows (unchanged since repair-040)

| ID | Domain |
| --- | --- |
| `act-zm-2023-022-the-income-tax-amendment-act-2023` | acts (not JIW scope) |
| `act-zm-2023-025-the-customs-and-excise-amendment-act-2023-act-no-25-of-2023` | acts (not JIW scope) |
| `act-zm-2023-029-the-appropriation-act-2023-act-no-29-of-2023` | acts (not JIW scope) |
| `act-zm-2024-003-investment-trade-and-business-development-amendment-act-2024` | acts (not JIW scope) |

All four missing IDs are in the **acts** namespace, owned by the main
corpus worker / repair worker. JIW cannot fix these. But the global
`records_fts` table is shared — any new INSERT touching the shadow
tables risks propagating the existing corruption. Per CHECK8 protocol,
this worker MUST defer all commits while the gap is open.

## Sweep position (unchanged — preserved for resume)

| Sweep | Position | Status |
| --- | --- | --- |
| `judiciary-coa-sweep` | page 1 | not yet started — new source, zero coverage |
| `judiciary-scz-sweep` | page 1 | not yet started |
| `judiciary-zmcc-sweep` | page 1 | not yet started |
| `judiciary-zmhc-sweep` | page 1 | not yet started |

## Git / refs status

- `git pull --ff-only` succeeded. HEAD = `e9dedad` = origin/main.
- Bogus lock-style refs in `.git/refs/remotes/origin/` still present
  (sandbox cannot `rm` them — EPERM). SHA-reseed from b0638-jiw still
  intact, so `git pull` works through them.
- No new bogus refs created this tick.
- Standard commit + push will proceed for the log files only.

## CHECK1–CHECK8 status (read-path)

| Check | Status |
| --- | --- |
| CHECK1 (judges present) | n/a — no new records |
| CHECK2 (issue_tags non-empty) | n/a — no new records |
| CHECK3 (outcome enum) | n/a — no new records |
| CHECK4 (judges registry resolution) | n/a — not iterated |
| CHECK5 (duplicate IDs) | n/a — no new records |
| CHECK6 (raw_sha256 match) | n/a — no new raw files |
| CHECK7 (duplicate case_name/court/date) | n/a — no new records |
| **CHECK8 (records == records_fts)** | **FAIL — gap=4** → defer commit per protocol |

## Recommended operator (host-side) actions

1. **Rebuild FTS5** on host:
   ```
   DROP TABLE records_fts;
   CREATE VIRTUAL TABLE records_fts USING fts5(...);
   INSERT INTO records_fts SELECT id, body, ... FROM records;
   VACUUM;
   ```
2. **Permanent `rm`** of bogus lock-style refs:
   ```
   rm .git/refs/remotes/origin/main.lock*
   rm .git/objects/maintenance.lock
   ```
3. **Rotate sandbox `/`** — currently 14 MB free, blocks pdfplumber
   cache and VACUUM headroom.
4. **Install `ocrmypdf`** in sandbox — `condB` SI backlog drain still
   blocked without it.

## Handoff

- Next tick: **b0641-jiw** at t+60 min.
- If host-side rebuild has happened by then, b0641 should resume from
  `judiciary-coa-sweep page 1` (highest-priority new source).
- If chronic blockers remain, b0641 will abort with the same pattern.
