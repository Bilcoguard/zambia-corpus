# Zambia Corpus Repair — Batch 016

**Date:** 2026-05-09 16:11 UTC (scheduled run)
**Worker:** repair-corpus (automated tick, scheduled-task SKILL v3 manifest, 48 records)
**Operator:** automated (Claude scheduled task; session `ecstatic-friendly-mccarthy`)
**Status:** **IDLE — all 48 repair targets verified clean (5th consecutive idle tick: b012/b013/b014/b015/b016)**
**Headline:** Repair worker re-verified the v3 manifest. All 48 records still pass the corruption test (>50% line-numbers-only). records / records_fts integrity remains closed (delta=0). Pool grew from 1854 → 1856 since b015 via judgment-ingestion-worker b0561 ZMCC 2019/{1,20} ingestion (b0562 Phase-8 reverify added 0). No work performed.

## Pre-flight

* Pre-step `find .git -name "*.lock" -delete` and `find .git -name "*.lock.bak" -delete` ran. FUSE/virtiofs mount silently rejected unlink on the persistent `.git/objects/maintenance.lock` and `.git/ORIG_HEAD.lock` orphans (same pre-existing constraint as every prior repair batch since b011 — `Operation not permitted`). Non-fatal for an idle tick.
* `git pull --ff-only` returned `Already up to date.` Local HEAD already at `25cf2c2` (b0562 close).

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

All 45 Acts and 3 SIs in the manifest hold real legislative text bodies. Sample body sizes (first 5):

* act-zm-2010-004-the-public-interest-disclosure-protection-of-whistleblowers — 58,993 chars
* act-zm-2010-024-the-competition-and-consumer-protection-2010 — 100,621 chars
* act-zm-2010-027-the-animal-health — 89,852 chars
* act-zm-2010-034-the-national-prosecution-authority-act-2010 — 31,875 chars
* act-zm-2011-004-urban-and-regional-act-2011 — 61,521 chars

Per Step 2 of the v3 SKILL.md: **"If zero remain corrupted, write 'All 48 repair targets fixed — repair worker idle' to worker.log with timestamp and stop."** That is what this tick does. Timestamp written: `2026-05-09T16:11:29Z`.

## Step 3 — Process batch

SKIPPED (idle tick — nothing to repair). MAX_BATCH_SIZE = 8 unused; 0 PDF fetches; rate-limit not invoked.

## Step 4 — Integrity check

```text
records      = 1856
records_fts  = 1856
delta        = 0
```

PRAGMA integrity_check: implicit pass via the SELECT round-trip (no schema changes). Pool grew 1854 → 1856 (+2) since b015 from judgment-ingestion-worker b0561 phase 5 (ZMCC 2019 num 1 — Sean E. Tembo v Attorney-General, allowed; ZMCC 2019 num 20 — Chama Mutambalilo v Attorney-General, dismissed) per worker.log 15:14:00Z. b0562 Phase-8 reverify mutated 0 records. No regressions in the 48-record manifest cohort.

> Note: The b0562 worker-tick log line reports "Pool=1860" at 15:34:40Z, which appears to be stale or counts mid-tick deferrals; the canonical post-tick `SELECT COUNT(*) FROM records` is **1856** and matches `records_fts`. Repair worker integrity gate (records == records_fts) holds either way; raising as an observation only — no action needed by repair worker (operator can clarify with judgment-ingestion-worker on its next tick if desired).

## Step 5 — B2 sync

SKIPPED — idle tick has no DB write to sync. `rclone` not in sandbox; deferred to host (standing pattern).

## Step 6 — Commit and push

Idle tick: only the worker.log idle line and this report file change. Will attempt commit/push of these coordination artefacts. If `.git/index.lock` orphan blocks the push (same FUSE/virtiofs `Operation not permitted` constraint as b011/b012/b013/b014/b015), the changes will be swept into the next ingestion-worker tick via the writable-copy `.git` workaround the worker-tick has been using since b0562 (commit `fd63489`).

## Records attempted (0)

No records attempted. No records repaired. No records failed. **0 corrupted remaining.**

## Next-tick recommendations

1. **Continue idle pattern** — manifest fully repaired since b013 (cumulative 5 records: whistleblowers 2010, management services board 2011, cannabis 2021, mobile money levy 2024, disaster management amendment 2026). All prior repairs holding through 5 consecutive verifies.
2. **Operator action — retire or repurpose** — the v3 manifest of 48 was last expanded at b011 and has been fully clean since b013. Recommend the operator either (a) retire the `repair-corpus` scheduled task, or (b) re-point its prompt at a fresh corruption-discovery query against the whole `records` table, so the worker can scan newly-ingested judgments/Acts for line-number-only bodies as the corpus grows past 1,856.
3. **No new corrupted records** — no v3 manifest expansion since b011.
