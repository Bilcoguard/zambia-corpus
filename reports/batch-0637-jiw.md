# Batch report: b0637-jiw (judgment-ingestion-worker abort)

**Timestamp**: 2026-05-13T18:07:52Z
**Verdict**: Tick aborted — **11th consecutive JIW abort** since b0626-jiw
**Records written**: 0
**Records deferred**: 0
**Wall clock**: ~2 minutes
**Budget consumed this tick**: 0 fetches (cumulative_today = 21/500)

## Blockers (unchanged from b0626 → b0636, plus one NEW item this tick)

1. **CHECK8 fails**: `records` = 1928, `records_fts` = 1924, gap = 4.
   The 4 missing FTS rows correspond to:
   - `act-zm-2023-022-the-income-tax-amendment-act-2023`
   - `act-zm-2023-025-the-customs-and-excise-amendment-act-2023-act-no-25-of-2023`
   - `act-zm-2023-029-the-appropriation-act-2023-act-no-29-of-2023`
   - `act-zm-2024-003-investment-trade-and-business-development-amendment-act-2024`

   These are *acts* — outside the JIW's write surface. JIW only reads
   parity; it cannot repair them. Repair-040 reduced gap 8→4;
   repair-041 confirmed deterministic FTS5 INSERT failure for the
   residual 4 IDs; repair-042 ran condition-B body updates (6/8 SI
   bodies) but did not touch the parity gap. Gap unchanged for ~8 hours.

2. **FTS5 shadow-table corruption** (unchanged signature since b037/b038):
   - `2nd reference to page 24604/21836/21821/21850/24628/24603/24606`
   - `Rowid 1185 out of order` on page 5733 cell 69
   - `overflow list length is 1 but should be 3` on page 5387 cell 0
   - `invalid page number 30000+` on pages 12466/22491/29610
   - `PRAGMA quick_check` returns "database disk image is malformed"
   - `PRAGMA integrity_check` likewise NOT OK

3. **Sandbox `/` is 100 % full** (14 MB free; `/sessions` has 2.4 GB free).
   Blocks new `pdfplumber` cache and a VACUUM-rebuild on sandbox disk.

4. **Host-side FTS5 rebuild still pending**: corpus.sqlite mtime
   `2026-05-13T14:36:48Z`, quiescent ~3.5 h. No evidence of DROP +
   CREATE + INSERT-SELECT + VACUUM since handoff at b0631-jiw.

5. **NEW this tick — bogus lock-style refs in `.git/refs/remotes/origin/`**:
   `main.lock.bak.b0636` plus older `main.lock.b0611-*` cluster cause
   `git pull --ff-only` to fail with `fatal: bad object
   refs/remotes/origin/main.lock.bak.b0636`. The refs are EPERM from
   the sandbox UID (cannot `rm` them here). They are remote-tracking
   only, so local HEAD remains in sync with origin/main (cccdeb3) and
   `git push` still works. Operator must clean them on host:
   `rm .git/refs/remotes/origin/main.lock*`.

6. **Pattern**: 11 consecutive JIW aborts since b0626-jiw at
   2026-05-13T05:18Z. Logs/reports for b0630..b0636 already pushed to
   origin/main (last commit `cccdeb3`).

## Read-path state

- `corpus.sqlite` mtime: 2026-05-13T14:36:48Z (quiescent ~3.5 h).
- `corpus.sqlite-journal`: not present.
- HEAD: `cccdeb3` == origin/main (no divergence).
- CHECK1–CHECK7 pass on the read path (no iteration of new records;
  no inserts attempted).
- CHECK8 fails (records=1928 ≠ records_fts=1924).

## Decision

Abort tick. Do **not** fetch / parse / write any new judgments. Per the
non-negotiable rule *"Never commit if `records` count ≠ `records_fts`
count — log the gap and defer"*, attempting an ingestion this tick would
either fail at commit time or compound the existing FTS5 corruption.
Continue the read-only abort pattern established at b0627-jiw.

The pull failure introduced this tick (bogus lock-style refs) is
non-blocking for the abort path: local HEAD already equals origin/main,
and `git push` is unaffected by stale remote-tracking refs. Logs and
this report will be pushed as in prior abort ticks.

## Actions taken

- `git pull --ff-only` — **failed** (bad object on
  `refs/remotes/origin/main.lock.bak.b0636`); verified local HEAD =
  origin/main = `cccdeb3` via `git rev-parse`, so no divergence.
- Attempted `rm` of bogus lock-style refs — EPERM (operator must clean
  from host).
- Verified parity gap and FTS5 corruption with live SQLite queries
  (read-only).
- Logged abort to `worker.log`, `costs.log`, `gaps.md`.
- Wrote this report.
- No fetch, no parse, no write to `corpus.sqlite`.
- Logs + report will be committed (parity rule: corpus.sqlite NOT staged).

## Recommendations (operator) — **URGENT**, unchanged + one new item

1. **NEW — clean bogus lock-style remote-tracking refs**:
   `rm .git/refs/remotes/origin/main.lock*` on the host so JIW workers
   can `git pull` again. The refs are remote-tracking only; deleting
   them is safe.

2. **Highest priority — host-side FTS5 rebuild**: `DROP TABLE
   records_fts;` → `CREATE VIRTUAL TABLE records_fts USING fts5(...)`
   → `INSERT INTO records_fts SELECT ... FROM records;` → `VACUUM;`
   outside the sandbox. Until this is repaired, all corpus writers
   are blocked.

3. **Second priority — sandbox `/` rotation** so the next JIW UID has
   `/tmp` working room for `pdfplumber`.

4. **Third priority — install `ocrmypdf`** in repair-worker
   environment to drain the remaining condition-B scanned-PDF
   backlog (~226 SI bodies).

5. **Completion-criteria note**: this is the 11th consecutive aborted
   tick on the same chronic host-side blockers. This satisfies the
   "5 consecutive zero-discovery ticks across all court sweeps"
   abstract threshold but the abort is **NOT** due to source
   exhaustion — it is due to unrepaired upstream corruption. **DO NOT
   flip `complete: true`**; surface as urgent chronic-blocker escalation.
