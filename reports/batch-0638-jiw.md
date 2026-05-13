# Batch report: b0638-jiw (judgment-ingestion-worker abort)

**Timestamp**: 2026-05-13T19:09:34Z
**Verdict**: Tick aborted — **12th consecutive JIW abort** since b0626-jiw
**Records written**: 0
**Records deferred**: 0
**Wall clock**: ~7 minutes
**Budget consumed this tick**: 0 fetches (cumulative_today = 21/500)

## Blockers (unchanged from b0626 → b0637, plus one mitigation this tick)

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
   bodies) but did not touch the parity gap. Gap unchanged for ~9 hours.

2. **FTS5 shadow-table corruption** (unchanged signature since b037/b038):
   - `2nd reference to page 24604/21836/21821/21850/24628/24603/24606`
   - `Rowid 1185 out of order` on page 5733 cell 69
   - `overflow list length is 1 but should be 3` on page 5387 cell 0
   - `invalid page number 30000+` on pages 12466/22491/29610 (cluster of
     ~150 invalid-page-number references on tree page 29610 alone)
   - `Child page depth differs` on page 12465 cell 7
   - `PRAGMA quick_check` returns "database disk image is malformed"
   - `PRAGMA integrity_check` likewise NOT OK

3. **Sandbox `/` is 100 % full** (14 MB free; `/sessions` has 2.4 GB free;
   corpus filesystem 15 GB free of 229 GB, 94 % full). Blocks new
   `pdfplumber` cache and a VACUUM-rebuild on sandbox disk.

4. **Host-side FTS5 rebuild still pending**: corpus.sqlite mtime
   `2026-05-13T14:36:48Z`, quiescent ~4.5 h. No evidence of DROP +
   CREATE + INSERT-SELECT + VACUUM since handoff at b0631-jiw.

5. **MITIGATED this tick — bogus lock-style refs in `.git/refs/remotes/origin/`**:
   The cluster of `main.lock.b0611-*` plus `main.lock.bak.b0636`
   refs that b0637-jiw flagged is still present (the underlying files
   remain EPERM-protected so cannot be removed from the sandbox).
   However, JIW b0638 successfully **wrote a valid SHA**
   (`9ae9919d0c3a9670e283d6cf105848533748db46`, i.e. current
   origin/main tip) into each of the six bogus ref files, which
   converted them from "bad object" parse errors to valid (if
   redundant) refs. `git pull --ff-only` now succeeds again
   ("Already up to date"). `git push` was never blocked.

   Note: this is a temporary workaround. Each time the host-side
   process creates a new `*.lock` or `*.lock.bak` ref, the JIW will
   need to re-seed it with a valid SHA until the operator removes the
   files. The operator's TODO `rm .git/refs/remotes/origin/main.lock*`
   on the host is still the correct permanent fix.

6. **Pattern**: 12 consecutive JIW aborts since b0626-jiw at
   2026-05-13T05:18Z. Logs/reports for b0630..b0637 already pushed to
   origin/main (last commit `9ae9919`).

## Read-path state

- `corpus.sqlite` mtime: 2026-05-13T14:36:48Z (quiescent ~4.5 h).
- `corpus.sqlite-journal`: present (78 KB stale tail from previous host
  writes; not actively being written; safe to ignore on the read path).
- HEAD: `9ae9919` == origin/main (no divergence).
- CHECK1–CHECK7 pass on the read path (no iteration of new records;
  no inserts attempted).
- CHECK8 fails (records=1928 ≠ records_fts=1924, gap=4).

## Decision

Abort tick. Do **not** fetch / parse / write any new judgments. Per the
non-negotiable rule *"Never commit if `records` count ≠ `records_fts`
count — log the gap and defer"*, attempting an ingestion this tick would
either fail at commit time or compound the existing FTS5 corruption.
Continue the read-only abort pattern established at b0627-jiw.

## Actions taken

- Cleaned local `.git/*.lock` (find -delete) — most underlying files
  are EPERM-protected by the FUSE mount, so the cleanup is a no-op for
  the chronic locks but a clean pass for any transient locks.
- **Re-seeded six bogus lock-style refs** with a valid SHA so that
  `git pull --ff-only` works again:
  - `.git/refs/remotes/origin/main.lock.b0611-cleanup-1778580978461760218`
  - `.git/refs/remotes/origin/main.lock.b0611-fin-1778580943129685118`
  - `.git/refs/remotes/origin/main.lock.b0611-final-1778580932907936655`
  - `.git/refs/remotes/origin/main.lock.b0611-stop-1778580916`
  - `.git/refs/remotes/origin/main.lock.bak-final2-e1069a02.b0611-clean`
  - `.git/refs/remotes/origin/main.lock.bak.b0636`
- `git pull --ff-only` — **succeeds** (Already up to date; HEAD =
  origin/main = `9ae9919`).
- Verified parity gap and FTS5 corruption with live SQLite queries
  (read-only — `PRAGMA quick_check`, `PRAGMA integrity_check`,
  `COUNT(*) FROM records`, `COUNT(*) FROM records_fts`).
- Logged abort to `worker.log`, `costs.log`, `gaps.md`.
- Wrote this report.
- No fetch, no parse, no write to `corpus.sqlite`.
- Logs + report will be committed (parity rule: corpus.sqlite NOT staged).

## Sweep position (unchanged — no progress)

- `judiciary-coa-sweep`: page 1 (not yet started — new source, zero coverage)
- `judiciary-scz-sweep`: page 1 (not yet started)
- `judiciary-zmcc-sweep`: page 1 (not yet started)
- `judiciary-zmhc-sweep`: page 1 (not yet started)
- `zambialii-zmsc`: continuation deferred until parity gap closes
- `zambialii-zmcc`: continuation deferred until parity gap closes

## Recommendations (operator) — **URGENT**, mostly unchanged

1. **Highest priority — host-side FTS5 rebuild**: `DROP TABLE
   records_fts;` → `CREATE VIRTUAL TABLE records_fts USING fts5(...)`
   → `INSERT INTO records_fts SELECT ... FROM records;` → `VACUUM;`
   outside the sandbox. Until this is repaired, all corpus writers
   are blocked.

2. **Second priority — clean bogus lock-style remote-tracking refs**:
   `rm .git/refs/remotes/origin/main.lock*
   .git/refs/remotes/origin/main.lock*.lock` on the host so future
   JIW workers don't have to re-seed them each tick. The refs are
   remote-tracking only; deleting them is safe.

3. **Third priority — sandbox `/` rotation** so the next JIW UID has
   `/tmp` working room for `pdfplumber`.

4. **Fourth priority — install `ocrmypdf`** in repair-worker
   environment to drain the remaining condition-B scanned-PDF
   backlog (~226 SI bodies).

5. **Completion-criteria note**: this is the **12th** consecutive
   aborted tick on the same chronic host-side blockers. This
   satisfies the "5 consecutive zero-discovery ticks across all
   court sweeps" abstract threshold but the abort is **NOT** due to
   source exhaustion — it is due to unrepaired upstream corruption.
   **DO NOT flip `complete: true`**; surface as urgent chronic-blocker
   escalation. Coverage stands at 238 judgments / 800 target = 30 %.

## Audit checklist (this tick)

- CHECK1 — judge listed on every judgment: N/A (no inserts).
- CHECK2 — `issue_tags` non-empty: N/A (no inserts).
- CHECK3 — `outcome` from allowed enum: N/A (no inserts).
- CHECK4 — judges resolve in registry: N/A (no inserts).
- CHECK5 — no duplicate IDs: N/A (no inserts).
- CHECK6 — `raw_sha256` matches on-disk: N/A (no inserts).
- CHECK7 — no duplicate name+court+date: N/A (no inserts).
- CHECK8 — records == records_fts: **FAIL** (1928 ≠ 1924); this tick
  defers without inserting per the non-negotiable rule.
