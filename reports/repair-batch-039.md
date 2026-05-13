# Repair batch 039 — DEFERRED (chronic FTS5 corruption + disk-/-full)

**Timestamp**: 2026-05-13T08:11:54Z
**Worker**: repair-corpus (v4)
**Verdict**: Tick deferred — 2nd consecutive repair-worker abort on the same chronic blocker (3rd if counting b0630-jiw)
**Records repaired**: 0
**Records deferred**: 8 stub records remain (Condition C) + 8 FTS-gap records (b037 inserts that did not propagate)
**Wall clock**: ~3 minutes

## Pre-flight diagnosis

| Check | Result |
|-------|--------|
| `git pull --ff-only` | already-up-to-date (benign `maintenance.lock` EPERM warning) |
| `records` count | 1928 |
| `records_fts` count | 1920 |
| Parity gap | **8 (FAIL CHECK8)** — must defer commit per non-negotiable |
| `PRAGMA quick_check` | **FAIL** — b-tree corruption on FTS5 shadow pages (21000+ range, plus invalid page numbers 30100–30700) |
| Sandbox `/` free | **15 MB (100% full)** — blocks pdfplumber /tmp use |
| Sandbox `/sessions` free | 2.4 GB |
| `corpus.sqlite` mtime | 2026-05-13T07:11:09Z (quiescent ~60 min, last touched by b038 prep) |

## Step 2 — Records identified for repair (live DB queries)

- **Condition A (corrupted, line-numbers-only digit-ratio >0.5)**: 0
- **Condition B (empty body, acts/SIs only)**: 232 — *out of scope for v4 manifest*; only the 1 SI on the manifest is in Condition C
- **Condition C (stub body <200 chars, acts/SIs)**: **8** — exactly the manifest-remaining cohort:
  - `si-zm-fees-and-fines-fee-and-penalty-unit-value-regulations-2014`
  - `act-zm-2024-005-zambia-institute-of-advanced-legal-education-amendment-act-2024`
  - `act-zm-2024-006-matrimonial-causes-amendment-act-2024`
  - `act-zm-2024-007-lands-tribunal-amendment-act-2024`
  - `act-zm-2024-023-value-added-tax-2024`
  - `act-zm-2024-026-revenue-authority-2024`
  - `act-zm-2024-027-property-transfer-tax-2024`
  - `act-zm-2025-005-national-road-fundamendment-2025`

## FTS-gap cohort (records present but missing from `records_fts`)

Exactly the 8 b037-repair targets whose FTS inserts did not persist (per b038 forensic — FUSE swap-back swallowed FTS inserts but kept body writes):

- `act-zm-2023-019-the-criminal-procedure-code-amendment-act-2023`
- `act-zm-2023-020-the-penal-code-amendment-act-2023`
- `act-zm-2023-022-the-income-tax-amendment-act-2023`
- `act-zm-2023-025-the-customs-and-excise-amendment-act-2023-act-no-25-of-2023`
- `act-zm-2023-026-the-zambia-revenue-authority-amendment-act-2023-act-no-26-of-2023`
- `act-zm-2023-028-the-local-government-amendment-act-2023-act-no-28-of-2023`
- `act-zm-2023-029-the-appropriation-act-2023-act-no-29-of-2023`
- `act-zm-2024-003-investment-trade-and-business-development-amendment-act-2024`

## Why abort (decision matrix)

Two independent blockers — each is sufficient on its own to mandate defer:

1. **FTS5 shadow-table corruption is operational** (b038 proved this empirically — INSERT at row 3/8 raised `database disk image is malformed`). New repair writes will fail the same way; partial writes leave the corpus dirtier than before.
2. **CHECK8 fails before any work** — even if the writes succeeded, the non-negotiable rule "Never commit if records ≠ records_fts" already blocks the commit. Repairing 8 stubs would push the parity gap from 8 to 16 or worse, not close it.
3. **Sandbox `/` is 100% full (15 MB free)** — pdfplumber and ocrmypdf cannot write working files. PDF text extraction would fail before reaching the DB.

The b0627-jiw handoff rule "do not waste fetch budget on retries that will fail on commit" applies equally to the repair worker.

## Actions taken this tick

- Cleaned `.git/*.lock` files (some EPERM, benign — committer is FUSE)
- `git pull --ff-only` → already-up-to-date
- Ran all three live-DB queries (Conditions A/B/C) — see counts above
- Verified `records` vs `records_fts` parity — gap = 8
- Verified `PRAGMA quick_check` — fails on FTS5 shadow pages
- **No** body fetches, **no** PDF downloads, **no** `UPDATE` against `records`, **no** writes to `records_fts`
- This report + log appends are the only files touched

## B2 sync

`rclone` not available in sandbox → **deferred to host** (no DB mutation anyway).

## Non-negotiables checklist

- Never commit if records ≠ records_fts → **gap preserved; report-only commit (logs + this report) — not a corpus mutation**
- Never fabricate body text → **no body writes attempted**
- Never exceed 20-min wall-clock → **~3 min elapsed**
- Fail loud → **diagnostics in `worker.log` and this report**
- User-Agent / robots.txt / CA cert → **N/A (no wire fetches)**

## Manifest progress

- Start of tick: 8 / 88 manifest records still needing repair.
- End of tick: **8 / 88 manifest records still needing repair** (no change).
- This is the **5th** consecutive worker tick blocked on FTS5 corruption (b037 partial → b038 deferred → b0630-jiw aborted → b039 deferred). The chronic-blocker pattern is now well-established.

## Recommendation to operator

The repair worker cannot make forward progress until two host-side actions are completed:

1. **PRIORITY 1 — FTS5 rebuild offline**: stop all workers, DROP `records_fts`, CREATE clean FTS5 table, INSERT-SELECT from `records` (all 1928), VACUUM. Validate with `PRAGMA integrity_check` (not just `quick_check`). This is unblocked only on the host where rclone+sqlite3 CLI can run with enough disk headroom (VACUUM needs ~120 MB free, sandbox has 15 MB on /).
2. **PRIORITY 2 — sandbox `/` rotation**: tooling needs `/tmp` for pdfplumber/ocrmypdf scratch files. Either rotate the sandbox or relocate `TMPDIR` to `/sessions/affectionate-dreamy-ritchie/tmp` for the next worker tick.

Until both are resolved, both the repair worker and the JIW worker will continue to abort each tick. Suggest pausing the cron schedule for both workers until the operator confirms FTS rebuild + disk rotation, to avoid noise in `worker.log`.
