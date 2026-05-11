# Zambia Corpus Repair — Batch 019

**Date:** 2026-05-10 16:14 UTC (scheduled run)
**Worker:** repair-corpus (automated tick, scheduled-task SKILL v3 manifest, 48 records)
**Operator:** automated (Claude scheduled task; session `lucid-intelligent-heisenberg`)
**Status:** **IDLE — all 48 repair targets verified clean (8th consecutive idle tick: b012/b013/b014/b015/b016/b017/b018/b019)**
**Headline:** Repair worker re-verified the v3 manifest. All 48 records still pass the v3 corruption test (>50% line-numbers-only with >10 lines). records / records_fts integrity remains closed (delta=0). Pool now 1862 (was 1859 at b018; +3 since b018, attributable to judgment-ingestion-worker activity between b018 and b019, including b0573 ZMCC 2017 Malembeka v AG ingestion). Note: main worker logs report `pool=1865` at b0569/b0570 — this metric appears to count more than just `records` table rows; the repair worker uses `SELECT COUNT(*) FROM records` which returned 1861 at first read (16:14Z) and 1862 at re-read (18:40Z, after b0573 ingestion). No repair work performed.

## Pre-flight

* Pre-step `find .git -name "*.lock" -delete` and `find .git -name "*.lock.bak" -delete` ran. Persistent `.git/ORIG_HEAD.lock` and `.git/objects/maintenance.lock` orphans rejected unlink (FUSE/virtiofs `Operation not permitted`, same constraint observed since b011 and reproduced this tick at 16:13:00Z). Non-fatal for an idle tick.
* `git pull --ff-only` returned `Already up to date.` Local HEAD already at `56a6ae0` (b0570 post-push close).

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

Per Step 2 of the v3 SKILL.md: **"If zero remain corrupted, write 'All 48 repair targets fixed — repair worker idle' to worker.log with timestamp and stop."** That is what this tick does. Timestamp written: `2026-05-10T16:14:04Z`.

## Step 3 — Skipped

No corrupted records to process. Step 3 (download / extract / OCR / quality-gate / normalise / DB update) entirely skipped per Step 2 termination rule.

## Step 4 — Integrity check

```
records      = 1862  (re-read at 18:40Z post b0573 ingestion; was 1861 at 16:14Z first read)
records_fts  = 1862
delta        = 0
```

Type breakdown at first read (16:14Z): act=1151, judgment=171, si=539 (total 1861). Re-read at 18:40Z showed records=1862 owing to judgment-ingestion-worker b0573 ZMCC 2017 Malembeka v AG ingestion. Integrity preserved at both reads. Pool grew by +3 since b018 (1859 → 1862) — attributable to judgment-ingestion-worker activity between b018 (06:12Z) and tick close (b0571 reparse, b0573 +1 ZMCC 2017, b0574 +0 close). The v3 manifest targets are unaffected (judgment-ingestion writes new judgment records — never updates existing Act/SI bodies in the v3 manifest).

## Step 5 — B2 sync

`rclone` not present in sandbox. Logged "B2 sync deferred to host" per SKILL.md fallback.

## Step 6 — Commit and push

* Appended idle entry to `costs.log`.
* Wrote this report (`reports/repair-batch-019.md`).
* Appended idle marker + tick-close lines to `worker.log`.
* Will attempt commit & push. If the `.git/index.lock` virtiofs orphan blocks the commit (same FUSE/virtiofs constraint as b013/b014/b015/b016/b017/b018), the staged tree will be swept on the next worker-tick (sweep-on-next-commit pattern, established b011/b012/b014/b015/b016/b017/b018).

## Step 7 — Stop

Tick complete. Idle, no DB writes, integrity preserved at `records = records_fts = 1862` (post b0573). Next tick runs on schedule.

## Notes for next tick

* Pool grew +3 from b018 to b019 owing to judgment-ingestion-worker activity (b0571 reparse, b0573 +1 ZMCC 2017 Malembeka v AG, b0574 +0 close). v3 manifest targets are unaffected.
* Manifest stability: b012 → b019 (eight consecutive idle ticks) confirms the v3 manifest's 48 targets remain repaired under the v3 corruption test. No regression observed.
* No new repair targets have been added to the manifest. Operator should consider whether the repair worker's job is complete and the schedule can be reduced or paused, given eight consecutive idle ticks against an unchanged manifest.
* Pool/records discrepancy: main worker reports `pool=1865` at b0569/b0570 while `SELECT COUNT(*) FROM records` returns 1861 — non-blocking for repair worker function, but flagged for operator awareness.
* Local index remains diverged from working tree (many staged-deletions for files that exist on disk, due to prior writable-copy commit pattern). Index sync recommended on next non-idle commit.
