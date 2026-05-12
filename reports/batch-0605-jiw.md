# Batch 0605 — Judgment Ingestion Worker (JIW)

**Tick start:** 2026-05-12T05:14:00Z (UTC)
**Tick end:**   2026-05-12T05:15:30Z (UTC)
**Worker:**     judgment-ingestion (separate from main worker / repair worker)
**Phase:**      read-only confirmation — FTS5-blocked (21st consecutive blocked tick)
**Verdict:**    `tick-complete-fts5-blocked-readonly-no-mutation`
**Renumber note:** b0604 was claimed by the Phase 8 nightly re-verify worker
  (see `reports/batch-0604.md`, commit collision at 2026-05-12T05:11Z),
  same renumbering pattern as b0585 / b0591 / b0595 / b0598 / b0603.
  This JIW tick is **b0605**.

## Summary

Per the b0603 recommendation ("Continue read-only confirmation ticks (no
schema mutations) until operator performs the records-table dump-and-rebuild"),
this tick performed **no FTS5 schema mutation, no new ingestion, and no
network fetches**. It re-confirmed the diagnostic state established in
b0603 by re-running only the safe read-only `PRAGMA` probes:

- `PRAGMA integrity_check(records)` (records table only) → **`ok`** (unchanged from b0603)
- `PRAGMA quick_check` (whole DB) → `database disk image is malformed` (unchanged)
- `SELECT COUNT(*) FROM records` → **1892** (unchanged)
- `SELECT COUNT(*) FROM records_fts` → **1892** (unchanged) — CHECK8 by-count PASS
- `SELECT MAX(rowid), MIN(rowid) FROM records_fts` → `(2011, 1)` — read-only rowid scan succeeds; 119 rowid gaps consistent with historical row deletions over the corpus's lifetime, not corruption.

The FTS5 `INSERT … VALUES('integrity-check')` probe used in b0603 was
**deliberately omitted this tick** — it is technically a write operation,
and although it failed cleanly without a journal in b0603, the b0602
`CREATE VIRTUAL TABLE` self-damage incident counsels against any
schema-mutating call until operator recovery completes. The b0603 result
is sufficient to conclude FTS5 writes remain blocked.

The 26-record deferred-fts5 backlog and 10-record deferred-scanned-pdf
backlog remain unchanged.

## Step 1 — Sync

- `git pull --ff-only` → `Already up to date` at HEAD `90d20f6` (the same
  jiw-b0602 commit + intervening b0603 jiw commit + repair-027 commit
  + worker-b0604 commit are all on the local branch from the prior
  session — fresh `festive-zen-heisenberg` virtiofs mount, no stale refs
  to clean this tick).
- `.git/HEAD.lock` and `.git/objects/maintenance.lock` cannot be
  unlinked (FUSE EPERM, same pattern as prior ticks). Harmless — the
  pull succeeded with only a warning.

## Step 2 — Budget

- Fetches today (2026-05-12, JIW-only): **0/500** entering this tick,
  **0/500** leaving this tick.
- No new fetches this tick — all probes were on-disk only.

## Step 3 — Phase decision

Identical reasoning to b0602 / b0603:

- Priority (a) REPARSE DEFERRED is not actionable: deferred-fts5 records
  are already parser-clean (need flush, not reparse), and
  deferred-scanned-pdf records need `ocrmypdf` which is not in the
  sandbox (`which ocrmypdf` → empty).
- Priorities (b)–(f) (new ingestion sweeps) would consume the 500/day
  budget without commit progress, as inserts into `records_fts` fail.

Selected action this tick: read-only confirmation only — no probes
that touch FTS5 at all. Two PRAGMA probes against the records table
plus simple counts.

## Step 4 — Diagnostic findings (UNCHANGED from b0603)

```
PRAGMA integrity_check(records)  → ok                                   (unchanged)
PRAGMA quick_check               → "database disk image is malformed"   (unchanged)
SELECT COUNT(*) FROM records     → 1892                                 (unchanged)
SELECT COUNT(*) FROM records_fts → 1892                                 (unchanged)
SELECT MAX(rowid),MIN(rowid)
       FROM records_fts          → (2011, 1) — 119 rowid gaps           (read-only)
md5(corpus.sqlite)               → 686f8197193a27b0f979156b833352fa     (unchanged)
md5(corpus.sqlite.bak.b0598-pre) → 686f8197193a27b0f979156b833352fa     (byte-identical)
```

**Conclusion (unchanged from b0603):** corruption confined to FTS5
shadow tables; `records` table is structurally sound. Operator
recovery path is the simple records-dump-and-rebuild.

## Step 5 — Self-inflicted damage and recovery

**None.** No schema mutations attempted. No journals created. No
backups taken (none needed). Final corpus.sqlite md5 byte-identical
to entering state, and to the b0598-pre clean backup.

## Step 6 — Integrity checks

- CHECK1 — every judgment has ≥1 judge: N/A (no judgments inserted)
- CHECK2 — issue_tags non-empty: N/A
- CHECK3 — outcome in enum: N/A
- CHECK4 — all judges resolve in registry: N/A
- CHECK5 — no duplicate IDs: PASS (1892 unique)
- CHECK6 — raw_sha256 on-disk match: N/A
- CHECK7 — no duplicate (case_name + court + date_decided): N/A
- CHECK8 — `records` count == `records_fts` count: **PASS** (1892 == 1892)

## Step 7 — Sweep position (UNCHANGED)

- `judiciary-coa-sweep: page 8 remaining` — 6 unprocessed candidates
  on judiciaryzambia.com COA category page 8.

## Step 8 — B2 sync

Deferred to host. `rclone` not in sandbox.

## Step 9 — Backlog totals (UNCHANGED from b0603)

- **deferred-fts5 backlog (parser-clean, awaiting FTS5 rebuild):** 26 records
  - b0590: 7, b0591: 4, b0592: 3, b0593: 6, b0594: 4, b0597: 2
  - Archive paths: `raw/judiciary-zm/coa/_deferred/b059*_parsed_records.json`
- **deferred-scanned-pdf backlog (awaiting ocrmypdf):** 10 records
  - b0593: 1 (Emergency Response Zambia 309/2023)
  - b0594: 4
  - b0597: 5 (Sichoni, Savenda, Zanaco-Kandala, Mutale-Mukumbwa, Setrec-Zanaco)

## Step 10 — Corpus snapshot (read-only)

- Records by type: `act:1151, si:539, judgment:202` (sum=1892 ✓)
- Judgments by court (from `judgments_meta`):
  - Supreme Court of Zambia: 92
  - Constitutional Court of Zambia: 85
  - Court of Appeal: 25
  - (sum = 202 ✓)
- Judiciary COA contribution to date: 25 records (the b0563–b0589 sweep
  cohort) — same count as b0603. **Court of Appeal is by far the
  largest growth opportunity** (judiciaryzambia.com has ~3,100 PDFs
  including ~1,000+ COA decisions); the corpus currently holds only
  25 COA records.

## Step 11 — Escalation

**Consecutive FTS5-blocked JIW ticks: 21** (b0590–b0598, b0602, b0603,
b0605; b0595/b0596/b0599–b0601/b0604 were repair-worker / main-worker
ticks that did not touch FTS5).

**Read-only confirmation ticks since b0603 recommendation: 2** (b0603,
b0605). Per b0603 guidance, will suggest JIW completion in worker.log
after 5 consecutive read-only confirmation ticks without operator
action (i.e., in approximately 3 more ticks if state remains
unchanged). Per skill non-negotiables, will **NOT** flip
`approvals.yaml: complete: true` without human sign-off.

**Escalation count for JIW: 10th** (9 prior + this one).

**Operator action required (UNCHANGED from b0603):**

1. Run the dump-and-rebuild procedure described in
   `reports/batch-0603-jiw.md` § Diagnostic findings. Because
   `PRAGMA integrity_check(records)` is `ok`, this is straightforward
   — no `.recover`, no forensic page extraction.
2. After rebuild, flush the 26-record archived JSON files under
   `raw/judiciary-zm/coa/_deferred/b059*_parsed_records.json` into
   the fresh DB.
3. Authorise (or not) the JIW worker to perform the rebuild itself
   on a future tick, if the host-side `sqlite3` CLI can be made
   available in the sandbox.

**Pre-rebuild backups still available in workspace root (unchanged):**
- `corpus.sqlite.bak.b0598-pre-20260511T221111Z` (116 MB) — clean,
  pre-b0598-attempt, md5 `686f8197193a27b0f979156b833352fa` (the
  current `corpus.sqlite` is byte-identical to this).
- `corpus.sqlite.bak.b0584-pre-20260511T081057Z`
- `corpus.sqlite.bak.b0583-pre-20260511T073727Z`
- `corpus.sqlite.bak.b0575-pre-20260510T191618Z`
- `corpus.sqlite.b0504bak`

**Forensic artefacts from b0602 (unchanged):**
- `corpus.sqlite.bak.b0602-damaged-20260512T010800Z` (116 MB)
- `corpus.sqlite-journal.b0602-forensic-20260512T010800Z` (62 KB)
- `corpus.sqlite-journal.b0602-jiw-quarantine-20260512T010900Z` (62 KB)

## Step 12 — Mutations this tick

- 0 new records ingested
- 0 records reparsed
- 0 fetches
- 0 backups taken
- 0 journals created
- 0 schema mutations
- 0 net file mutations to corpus.sqlite

Only log/report updates were written to disk (worker.log, costs.log,
gaps.md, this report).

## Step 13 — Stop

Next JIW tick: t+60min per cadence.

**Recommendation for next tick:** another read-only confirmation tick,
identical pattern. Do not attempt any FTS5 work until the operator
confirms the records-table dump-and-rebuild has been performed (or
until `sqlite3` CLI / `ocrmypdf` are made available in the sandbox).
This is the 2nd of the 5 read-only confirmation ticks before the
worker.log "JIW completion suggested — awaiting human sign-off"
escalation language is appended.
