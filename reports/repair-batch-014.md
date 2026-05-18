# Zambia Corpus Repair — Batch 014

**Date:** 2026-05-09 14:38 UTC (scheduled run)
**Worker:** repair-corpus (automated tick, scheduled-task SKILL v3 manifest, 48 records)
**Operator:** automated (Claude scheduled task; session `loving-sweet-bohr`)
**Status:** **IDLE — all 48 repair targets verified clean**
**Headline:** Repair worker re-verified the v3 manifest. All 48 records pass the corruption test (>50% line-numbers-only) and the records / records_fts integrity gap that was outstanding at b013 has now closed (delta=0). No work performed; no git commit needed.

## Pre-flight

* Pre-step `find .git -name "*.lock" -delete` and `find .git -name "*.lock.bak" -delete` ran. FUSE mount silently rejected unlink on the persistent `.git/HEAD.lock`, `.git/index.lock`, and `.git/ORIG_HEAD.lock` orphans (same pre-existing constraint as every prior repair batch — `Operation not permitted`). Non-fatal for an idle tick.
* `git pull --ff-only` returned `fatal: update_ref failed for ref 'ORIG_HEAD'` due to the persistent `.git/ORIG_HEAD.lock`. This mirrors b013 and prior ticks; since this tick performs zero writes, it has no effect on the outcome.

## Step 2 — manifest re-verification

Iterated all 48 manifest record IDs and applied the v3 corruption test:

```python
lines = body.strip().split('\n')
num_lines = sum(1 for l in lines if l.strip().isdigit())
is_corrupted = (num_lines > len(lines) * 0.5 and len(lines) > 10)
```

Result:

| Bucket | Count |
|---|---|
| OK (passes corruption test) | **48** |
| Still corrupted | **0** |
| Not found in DB | **0** |

All 45 Acts and 3 SIs in the manifest now hold real legislative text bodies. The b013 repairs (5 records: whistleblowers 2010, management services board 2011, cannabis 2021, mobile money levy 2024, disaster management amendment 2026) have not regressed.

Per Step 2 of the v3 SKILL.md: **"If zero remain corrupted, write 'All 48 repair targets fixed — repair worker idle' to worker.log with timestamp and stop."** That is what this tick does.

## Step 3 — Process batch

SKIPPED (idle tick — nothing to repair).

## Step 4 — Integrity check

```text
records      = 1853
records_fts  = 1853
delta        = 0
```

The 5-row pre-existing FTS gap that blocked b013's commit has CLOSED. records=1853 (was 1851 at b013) and records_fts=1853 (was 1846 at b013). The judgment-ingestion-worker added 2 more records since b013 and back-filled the 5 missing FTS rows + the 2 new ones in batches b0556→b0559 (per worker.log entries between 09:15Z and 11:14Z today). PRAGMA integrity_check = `ok`.

This means b013's deferred body repairs were swept into the next git commit window cleanly (per b013 recommendation #1 to the operator).

## Step 5 — B2 sync

SKIPPED — idle tick has no DB write to sync.

## Step 6 — Commit and push

SKIPPED — idle tick has no DB or report changes to commit beyond this report itself and the single worker.log line. The persistent `.git/*.lock` orphans (which this sandbox cannot unlink) would block any push attempt regardless. The host-side cron / manual operator can sweep this report into the next ingestion-worker commit on its next tick (matches the b011/b012 idle-tick pattern).

## Records attempted (0)

None — idle.

## Records successfully repaired (0)

None — idle.

## Records failed (0)

None — idle.

## Records still remaining (0)

```text
Total manifest: 48
Still corrupted: 0
Fixed: 48
```

## Live-DB integrity snapshot

* `records` = **1853** (+2 since b013 from judgment-ingestion-worker)
* `records_fts` = **1853** (+7 since b013: 5-row gap closed + 2 new judgment FTS rows added)
* Δ = **0** (was 5 at b013 — gap fully closed by judgment-ingestion-worker between b013 and this tick)
* PRAGMA integrity_check = `ok`
* All 48 manifest record bodies confirmed not-corrupted

## Tick budget

* Wall clock: ~3 minutes (well under 20-min limit)
* PDF fetches: 0 (idle)
* Records updated: 0 (idle)
* OCR invocations: 0
* B2 sync: deferred (no rclone)
* Git commit: not attempted (idle tick + persistent .lock orphans)

## Recommendation

* Repair worker continues to be useful as a watchdog. Recommend keeping it scheduled even though this is the second idle-tick after b013's success — it caught the b013 work originally and will catch any new corrupted ingestions from the main worker.
* The persistent `.git/HEAD.lock`, `.git/index.lock`, and `.git/ORIG_HEAD.lock` orphans (`Operation not permitted` to unlink) are cowork-mount-level FUSE issues that the host should clear out-of-band; they have not blocked any write so far because every committing worker uses the cowork-allowed delete path, but this scheduled sandbox cannot. Idle ticks like this one don't care.
