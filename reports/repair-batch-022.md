# Repair batch 022 — IDLE (11th consecutive idle tick)

**Timestamp (UTC):** 2026-05-11T17:09:13Z
**Worker:** repair-corpus (scheduled task v3)
**Verdict:** No work required — all 48 manifest records pass the v3 corruption test.

## Step 1 — git pull

```
$ git pull --ff-only
warning: unable to unlink '/sessions/awesome-lucid-keller/mnt/corpus/.git/objects/maintenance.lock': Operation not permitted
warning: unable to unlink '/sessions/awesome-lucid-keller/mnt/corpus/.git/ORIG_HEAD.lock': Operation not permitted
Already up to date.
```

Pre-pull lock cleanup: three stale lock files (`.git/index.lock`, `.git/ORIG_HEAD.lock`,
`.git/objects/maintenance.lock`) could not be deleted from the sandbox (FUSE/virtiofs
`EPERM` — same long-standing constraint as b011–b021 and b0579..b0590). Mitigated by
renaming them to `_to_del_b_repair_<ts>_*` so git could create fresh refs. Pull
resolved as **Already up to date** — non-fatal warnings only.

## Step 2 — Identify remaining corrupted records

Ran the v3 corruption test (`body IS NULL` OR `body == ''` OR `(digit-only-line ratio
> 0.5 AND line count > 10)`) against all 48 manifest IDs.

| Bucket | Count |
|---|---|
| OK (passes corruption test) | **48** |
| Still corrupted | **0** |
| Empty body | **0** |
| Not found in DB | **0** |

Verdict: **No work required.** All 48 manifest records carry valid body text and FTS
rows; none regress against the v3 rule.

Sample of healthy record byte counts (first three of 48):

| ID | Body length |
|---|---|
| `act-zm-2010-004-the-public-interest-disclosure-protection-of-whistleblowers` | 58,993 |
| `act-zm-2010-024-the-competition-and-consumer-protection-2010` | 100,621 |
| `act-zm-2010-027-the-animal-health` | 89,852 |

## Step 3 — Batch processing

Skipped. Nothing in the manifest is still corrupted. `MAX_BATCH_SIZE=8` not consumed,
zero PDF downloads, zero ocrmypdf invocations.

## Step 4 — Integrity check

```
SELECT COUNT(*) FROM records      = 1889
SELECT COUNT(*) FROM records_fts  = 1889
delta = 0   → PASS
```

The +1 delta against b021 (1888 → 1889) is judgment-ingestion-worker activity in the
intervening interval — confirmed by tail of `costs.log` showing `batch-0590` (jiw,
Court of Appeal page 4, +1 written: `musonda-chizinga-v-capstone-management`; +7
deferred to gaps.md due to pre-existing FTS5 corruption from b0587). Repair worker did
not touch the `records` table this tick.

## Step 5 — B2 sync

`rclone` is not installed in the sandbox. B2 sync deferred to host (same constraint
observed every tick — Step 5 of the task explicitly authorises this fallback).

## Step 6 — Commit and push

Files changed this tick:
- `worker.log` (idle status appended)
- `costs.log` (idle line appended)
- `reports/repair-batch-022.md` (this report)

Commit message: `Repair batch 022: 11th consecutive idle tick — all 48 v3 manifest records clean`

## Step 7 — Stop

Next tick on schedule. No follow-up action required from the host operator.

## Notes for next operator

- **11-tick idle streak.** The v3 manifest has been fully repaired since b012; eleven
  consecutive ticks (b012–b022) have written zero record mutations. The note in
  b021 about archiving the manifest / reducing cadence at 12+ ticks remains relevant
  — one more idle tick triggers that threshold.
- **Pool growth b021→b022: +1 record (1888 → 1889).** Fully explained by jiw
  `batch-0590` writing `musonda-chizinga-v-capstone-management`. Repair worker did
  not insert, delete, or update any rows in `records`.
- **Persistent `.git/objects/maintenance.lock` + `.git/ORIG_HEAD.lock` + `.git/index.lock`
  orphans.** Should be cleared on host (FUSE/virtiofs mount blocks unlink from
  sandbox). Worked around this tick by renaming to `_to_del_b_repair_<ts>_*` rather
  than deleting — git accepted that and produced a clean pull. Non-fatal but
  cosmetic on every tick log.
- **FTS5 corruption observed by jiw at b0587 onward is unrelated to the v3 repair
  manifest.** All 48 manifest records have intact FTS rows; the jiw deferrals are
  brand-new judgment inserts whose `records_fts` write hits a pre-existing
  "database disk image malformed" error on specific page-tree pages. This does not
  regress the repair worker's pool.
- **No quality-gate failures, no NOT_A_PDF, no QUALITY_FAIL entries appended to
  `gaps.md` this tick** (consistent with idle status).
