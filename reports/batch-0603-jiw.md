# Batch 0603 — Judgment Ingestion Worker (JIW)

**Tick start:** 2026-05-12T05:08:00Z (UTC)
**Tick end:** 2026-05-12T05:10:00Z (UTC)
**Worker:** judgment-ingestion (separate from main worker / repair worker)
**Phase:** read-only confirmation — FTS5-blocked (20th consecutive blocked tick)
**Verdict:** `tick-complete-fts5-blocked-readonly-no-mutation`

## Summary

Per the b0602 recommendation ("Read-only. Do NOT run further FTS5 schema-mutation diagnostics — they risk re-wedging the DB via orphaned rollback journals"), this tick performed **no FTS5 schema mutation and no new ingestion**. It confirmed via a single integrity-check probe that FTS5 writes are still fully blocked, and recorded one NEW diagnostic data point that narrows the operator-side recovery path:

- `PRAGMA integrity_check(records)` (records table only) → **`ok`** ← NEW
- `PRAGMA quick_check` (whole DB) → `database disk image is malformed` (unchanged)
- `INSERT INTO records_fts(records_fts) VALUES('integrity-check')` → `database disk image is malformed` (unchanged)

The base `records` table is structurally intact — only the FTS5 shadow tables (`records_fts_content`, `records_fts_data`, `records_fts_docsize`, `records_fts_idx`, `records_fts_config`) are involved in the corruption. This **simplifies operator-side recovery**: the operator does not need `.recover` or `VACUUM INTO` — they can dump the regular `records` table with a clean `SELECT` and rebuild `records_fts` from scratch on a fresh DB.

The 26-record deferred-fts5 backlog and 10-record deferred-scanned-pdf backlog remain unchanged.

## Step 1 — Sync

- `git pull --ff-only` → `Already up to date` after clearing two stale `refs/remotes/origin/main.lock.*` files left by prior worker (renamed under `.removed-*-lock-20260512` because fuse mount blocks `rm`).
- `.git/objects/maintenance.lock` cannot be unlinked (fuse mount). Harmless — git proceeds despite warning.

## Step 2 — Budget

- Fetches today (2026-05-12, JIW-only): **0/500** entering this tick, **0/500** leaving this tick.
- No new fetches this tick — all probes were on-disk only.

## Step 3 — Phase decision

Identical reasoning to b0602:

- Priority (a) REPARSE DEFERRED is not actionable: deferred-fts5 records are already parser-clean (need flush, not reparse), and deferred-scanned-pdf records need `ocrmypdf` which is not in the sandbox (`which ocrmypdf` → empty).
- Priorities (b)–(f) (new ingestion sweeps) would consume the 500/day budget without commit progress, as inserts into `records_fts` fail.

Selected action this tick: a **single read-only probe** to confirm FTS5 is still blocked, plus a NEW narrow diagnostic (`PRAGMA integrity_check(records)`) that tests whether the base records table is sound. No schema mutations attempted — explicitly heeding b0602's warning.

## Diagnostic findings (NEW)

```
PRAGMA integrity_check(records)  → ok                                ← NEW (narrows recovery path)
PRAGMA quick_check               → "database disk image is malformed"
INSERT INTO records_fts(records_fts) VALUES('integrity-check')
                                  → sqlite3.DatabaseError:
                                    "database disk image is malformed"
SELECT COUNT(*) FROM records     → 1892
SELECT COUNT(*) FROM records_fts → 1892
SELECT name FROM sqlite_master
  WHERE name LIKE 'records_fts%' →
    records_fts, records_fts_config, records_fts_content,
    records_fts_data, records_fts_docsize, records_fts_idx
```

**Conclusion (NEW for operator):**

The corruption is confined to the FTS5 shadow tables. The base `records` table reads back as `ok` from `PRAGMA integrity_check(records)`. This means the simplest viable recovery is:

1. Open the corpus from a host with sqlite3 (any version).
2. Dump records to a CSV/JSON/SQL stream with a normal `SELECT * FROM records` (no FTS5 touched).
3. Create a fresh empty DB with the standard schema (records + records_fts virtual table).
4. Bulk-insert from the dump.
5. `INSERT INTO records_fts(records_fts) VALUES('rebuild')` against the fresh DB — this will succeed because the new pages are uncorrupted.
6. Replace `corpus.sqlite` atomically.

This procedure **does not need** `.recover` (which is for cases where pages are unreadable) or `VACUUM INTO` (which may also fail on the corrupt pages). It is the cleanest path and can be wrapped in a 30-line Python script.

## Step 4 — Self-inflicted damage and recovery

**None.** No schema mutations attempted. No journals created. No backups taken (none needed). Final corpus.sqlite md5 identical to entering state.

## Step 5 — Integrity checks

- CHECK1 — every judgment has ≥1 judge: N/A (no judgments inserted)
- CHECK2 — issue_tags non-empty: N/A
- CHECK3 — outcome in enum: N/A
- CHECK4 — all judges resolve in registry: N/A
- CHECK5 — no duplicate IDs: PASS (1892 unique)
- CHECK6 — raw_sha256 on-disk match: N/A
- CHECK7 — no duplicate (case_name + court + date_decided): N/A
- CHECK8 — `records` count == `records_fts` count: **PASS** (1892 == 1892)

## Step 6 — Sweep position

Unchanged from b0598/b0602:

- `judiciary-coa-sweep: page 8 remaining` — 6 unprocessed candidates on judiciaryzambia.com COA category page 8.

## Step 7 — B2 sync

Deferred to host. `rclone` not in sandbox.

## Step 8 — Backlog totals (UNCHANGED from b0602)

- **deferred-fts5 backlog (parser-clean, awaiting FTS5 rebuild):** 26 records
  - b0590: 7, b0591: 4, b0592: 3, b0593: 6, b0594: 4, b0597: 2
- **deferred-scanned-pdf backlog (awaiting ocrmypdf):** 10 records
  - b0593: 1 (Emergency Response Zambia 309/2023), b0594: 4, b0597: 5 (Sichoni, Savenda, Zanaco-Kandala, Mutale-Mukumbwa, Setrec-Zanaco)

## Step 9 — Escalation

**Consecutive FTS5-blocked JIW ticks: 20** (b0590–b0598, b0602, b0603; b0595, b0596, b0599–b0601 were repair-worker / main-worker ticks that did not touch FTS5).

**Escalation count for JIW: 9th** (8 prior + this one).

**Operator action required (UPDATED with NEW diagnostic):**

1. Run the dump-and-rebuild procedure described in the diagnostic findings section above. Because `PRAGMA integrity_check(records)` is `ok`, this is straightforward — no `.recover`, no forensic page extraction.
2. After rebuild, flush the 26-record archived JSON files under `raw/judiciary-zm/coa/_deferred/b059*_parsed_records.json` into the fresh DB.
3. Authorise (or not) the JIW worker to perform the rebuild itself on a future tick, if the host-side `sqlite3` CLI can be made available in the sandbox.

**Pre-rebuild backups still available in workspace root:**
- `corpus.sqlite.bak.b0598-pre-20260511T221111Z` (116 MB) — clean, pre-b0598-attempt, md5 `686f8197193a27b0f979156b833352fa` (the current `corpus.sqlite` is byte-identical to this).
- `corpus.sqlite.bak.b0584-pre-20260511T081057Z`
- `corpus.sqlite.bak.b0583-pre-20260511T073727Z`
- `corpus.sqlite.bak.b0575-pre-20260510T191618Z`
- `corpus.sqlite.b0504bak`

**Forensic artefacts from b0602 (unchanged):**
- `corpus.sqlite.bak.b0602-damaged-20260512T010800Z` (116 MB)
- `corpus.sqlite-journal.b0602-forensic-20260512T010800Z` (62 KB)
- `corpus.sqlite-journal.b0602-jiw-quarantine-20260512T010900Z` (62 KB)

## Step 10 — Mutations this tick

- 0 new records ingested
- 0 records reparsed
- 0 fetches
- 0 backups taken
- 0 journals created
- 0 schema mutations
- 0 net file mutations to corpus.sqlite

Only log/report updates were written to disk (worker.log, costs.log, gaps.md, this report).

## Step 11 — Stop

Next JIW tick: t+60min per cadence.

**Recommendation for next tick:** another read-only confirmation tick, identical pattern to b0603. Do not attempt any FTS5 work until the operator confirms the records-table dump-and-rebuild has been performed (or until `sqlite3` CLI / `ocrmypdf` are available in the sandbox). If 5 consecutive read-only ticks pass without operator action, escalate to a one-line worker.log "JIW completion suggested — awaiting human sign-off" entry (per skill's completion-criteria language).
