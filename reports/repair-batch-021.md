# Repair batch 021 — IDLE (10th consecutive idle tick)

**Timestamp (UTC):** 2026-05-11T10:11:38Z
**Worker:** repair-corpus (scheduled task v3)
**Verdict:** No work required — all 48 manifest records pass the v3 corruption test.

## Step 1 — git pull

```
$ git pull --ff-only
warning: unable to unlink '.git/objects/maintenance.lock' (Operation not permitted)
Already up to date.
```

Persistent maintenance.lock orphan is the long-standing FUSE/virtiofs cosmetic issue
(non-fatal; the pull still resolved as "Already up to date"). No action taken.

## Step 2 — Identify remaining corrupted records

Ran the v3 corruption test (`body IS NULL` OR `body == ''` OR `(digit-only-line ratio > 0.5
AND line count > 10)`) against all 48 manifest IDs.

| Bucket | Count |
|---|---|
| OK (passes corruption test) | **48** |
| Still corrupted | **0** |
| Empty body | **0** |
| Not found in DB | **0** |

Verdict: **No work required.** All 48 manifest records carry valid body text and FTS rows;
none regress against the v3 rule.

## Step 3 — Batch processing

Skipped. Nothing in the manifest is still corrupted. `MAX_BATCH_SIZE=8` not consumed.

## Step 4 — Integrity check

```
SELECT COUNT(*) FROM records      = 1888
SELECT COUNT(*) FROM records_fts  = 1888
delta = 0   → PASS
```

The +14 delta against b020 (1874 → 1888) is judgment-ingestion-worker / main-worker
activity in the intervening interval — confirmed by tail of `costs.log` showing batches
through `b0589` (Phase 8 reverify ticks, 8 fetches/tick, no record mutations). Repair
worker did not touch the `records` table this tick.

## Step 5 — B2 sync

`rclone` is not installed in the sandbox. B2 sync deferred to host (same constraint
observed every tick — Step 5 of the task explicitly authorises this fallback).

## Step 6 — Commit and push

Files changed this tick:
- `worker.log` (idle status appended)
- `costs.log` (idle line appended)
- `reports/repair-batch-021.md` (this report)

Commit message: `Repair batch 021: 10th consecutive idle tick — all 48 v3 manifest records clean`

## Step 7 — Stop

Next tick on schedule. No follow-up action required from the host operator.

## Notes for next operator

- **10-tick idle streak.** The v3 manifest has been fully repaired since b012; ten
  consecutive ticks (b012–b021) have written zero record mutations. If the streak
  reaches 12+ ticks, consider archiving the manifest and reducing scheduled cadence to
  weekly verification, or folding the corruption test into the main worker's nightly
  QA pass.
- **Pool growth b020→b021: +14 records (1874 → 1888).** Fully explained by
  judgment-ingestion-worker / main-worker activity in costs.log (latest batch tagged
  `b0589`). Repair worker did not insert, delete, or update any rows in `records`.
- **Persistent `.git/objects/maintenance.lock` orphan.** Should be cleared on host
  (FUSE/virtiofs mount blocks unlink from sandbox). Non-fatal but cosmetic on every
  tick log.
- **No quality-gate failures, no NOT_A_PDF, no QUALITY_FAIL entries appended to
  `gaps.md` this tick** (consistent with idle status).
