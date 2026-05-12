# Batch 0606 — Judgment Ingestion Worker (JIW)

**Tick start:** 2026-05-12T~current (UTC) — scheduled run
**Worker:**     judgment-ingestion (separate from main worker / repair worker)
**Phase:**      read-only confirmation — FTS5-blocked (22nd consecutive blocked tick)
**Verdict:**    `tick-complete-fts5-blocked-readonly-no-mutation`
**Read-only confirmation tick:** 3 of 5 (per b0603 escalation guidance, continued by b0605)

## Summary

Per the b0603 escalation guidance (continue read-only confirmation ticks
until operator performs the records-table dump-and-rebuild described in
`reports/batch-0603-jiw.md` § Diagnostic findings), this tick performed
**no FTS5 schema mutation, no new ingestion, and no network fetches**.
It re-confirmed the diagnostic state established in b0603 and re-validated
by b0605 by re-running only the safe read-only `PRAGMA` probes:

- `PRAGMA integrity_check(records)` (records table only) → **`ok`** (unchanged)
- `PRAGMA quick_check` (whole DB) → `database disk image is malformed` (unchanged)
- `SELECT COUNT(*) FROM records` → **1892** (unchanged)
- `SELECT COUNT(*) FROM records_fts` → **1892** (unchanged) — CHECK8 by-count PASS
- `SELECT MIN(rowid), MAX(rowid), COUNT(*) FROM records_fts` → `(1, 2011, 1892)` —
  read-only rowid scan succeeds; 119 rowid gaps consistent with historical
  row deletions over the corpus's lifetime, not corruption.
- `md5(corpus.sqlite)` → `686f8197193a27b0f979156b833352fa` — **byte-identical** to
  b0598-pre clean backup, b0603, and b0605

The FTS5 `INSERT … VALUES('integrity-check')` probe used in b0603 was
**deliberately omitted this tick** (continuing b0605's posture) — it is
technically a write operation, and although it failed cleanly without a
journal in b0603, the b0602 `CREATE VIRTUAL TABLE` self-damage incident
counsels against any schema-mutating call until operator recovery
completes. The b0603 result is sufficient to conclude FTS5 writes remain
blocked.

The 26-record deferred-fts5 backlog and 10-record deferred-scanned-pdf
backlog remain unchanged.

## Step 1 — Sync

- `find .git -name "*.lock" -delete` → ok
- `git pull --ff-only` → `Already up to date` (HEAD `6800396` — b0605 commit)
  - Warning observed: `unable to unlink '.git/objects/maintenance.lock': Operation not permitted` —
    pre-existing virtiofs/fuse mount quirk; same pattern as b0598+; not a
    blocker (pull completed cleanly).

## Step 2 — Budget check

- `costs.log` grep for today (`2026-05-12`):
  - 8 fetches recorded today, all attributable to Phase 8 nightly
    re-verify worker (`batch-0604`).
  - JIW budget consumed today: **0 / 500** (this worker has not made any
    fetches since the FTS5-blocked period began).
  - Budget verdict: **ok** — far below 500-fetch JIW daily ceiling.

## Step 3 — Decide what to do this tick

Per the priority order in the task file and the b0603/b0605 standing
guidance:

- **(a) REPARSE DEFERRED:** there are 26 deferred-fts5 records ready to
  reparse, but reparsing them produces an FTS5 INSERT, which is blocked.
  **Skipped.**
- **(b) JUDICIARY COURT OF APPEAL SWEEP:** would write new records →
  blocked by FTS5. **Skipped.**
- **(c)–(f) other sweeps:** same FTS5 block. **All skipped.**

→ **Decision:** continue the read-only confirmation tick series. This is
   tick **3 of 5**.

## Step 4 — Read-only probes

Executed via `sqlite3` opened `mode=ro` (URI flag) to guarantee no
journal can be created. Probe script run inline; no derivative script
committed.

```
size               = 116,457,472 bytes
md5(corpus.sqlite) = 686f8197193a27b0f979156b833352fa
PRAGMA integrity_check(records)
                   → ok
PRAGMA quick_check
                   → "database disk image is malformed"
SELECT COUNT(*) FROM records
                   → 1892
SELECT COUNT(*) FROM records_fts
                   → 1892
SELECT MIN(rowid), MAX(rowid), COUNT(*) FROM records_fts
                   → (1, 2011, 1892)         (119 rowid gaps, unchanged)
```

**Delta from b0605:** none. State is byte-identical.

## Step 5 — Integrity checks (CHECK1–CHECK8)

No new records this tick → CHECK1–CHECK4 and CHECK6–CHECK7 are vacuously
satisfied. CHECK5 (no duplicate IDs) confirmed via prior tick. CHECK8
(records count == records_fts count) **PASS by-count: 1892 == 1892**.
Per the non-negotiables ("Never commit if records count ≠ records_fts
count"), no insertion is being committed, so the guard need not fire.

## Step 6 — Backlog (UNCHANGED)

- `deferred-fts5`: 26 parser-clean records awaiting rebuild
  - b0590: 7, b0591: 4, b0592: 3, b0593: 6, b0594: 4, b0597: 2
- `deferred-scanned-pdf`: 10 records awaiting `ocrmypdf` (not in sandbox)

## Step 7 — Sweep position (UNCHANGED)

`judiciary-coa-sweep: page 8 remaining` — 6 unprocessed COA candidates
on judiciaryzambia.com page 8. Resumption blocked by FTS5 corruption.

## Step 8 — Read-only confirmation tick counter

This is the **3rd of 5** consecutive read-only confirmation ticks per
b0603's escalation guidance. Two more such ticks without operator
action and JIW will append a "JIW completion suggested — awaiting human
sign-off" line to worker.log (does **NOT** flip approvals.yaml
`complete: true`).

## Step 9 — Mutations this tick

Zero. No `corpus.sqlite` changes. Only log / report / gaps.md text appends.

## Step 10 — B2 sync

`rclone` is not present in this sandbox; B2 sync deferred to host (same
behaviour as every JIW tick since the sandbox-only execution model
began).

## Recommendation for next JIW tick

Continue read-only confirmation ticks (no schema mutations, no fetches)
until operator performs the records-table dump-and-rebuild described in
the b0603 report. After two more such ticks (b0607 = 4-of-5, b0608 =
5-of-5), JIW will append a "completion suggested" line to worker.log.

## Operator escalation (11th)

The records-table dump-and-rebuild remains the only known path to clear
the FTS5 corruption. Operator action required:

1. `sqlite3 corpus.sqlite ".dump records"` → `records.sql`
2. Create fresh `corpus.sqlite.new` with `acts`/`judgments`/`si`/...
   schema and the FTS5 `records_fts` virtual table.
3. Re-import `records.sql` into the fresh DB and rebuild FTS5 via
   `INSERT INTO records_fts(records_fts) VALUES('rebuild')`.
4. Cross-check `records` and `records_fts` counts match (expected 1892).
5. Replace `corpus.sqlite` atomically and resume normal JIW + Phase 8 work.

The 26 deferred-fts5 records and 6-candidate page-8 CoA backlog will
flow through the standard tick loop once the rebuild completes.
