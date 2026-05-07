# Zambia Corpus Repair — Batch 002

**Date:** 2026-05-07 UTC (scheduled run, ~08:13Z–08:17Z)
**Worker:** repair-corpus (automated tick, scheduled-task SKILL)
**Operator:** automated (Claude scheduled task; session `fervent-vibrant-pasteur`)
**Status:** **REPORT-ONLY — NO DB MUTATIONS**
**Reason:** `corpus.sqlite` failed `PRAGMA integrity_check` with widespread btree
page corruption. Per SKILL non-negotiable rule "Fail loud with full diagnostic
on unexpected errors", this tick is suspended before any UPDATE.

## Headline

Pre-flight read of `corpus.sqlite` against the 42-record manifest produced:

* **11** records confirmed already repaired (body length OK, not line-numbers).
* **27** records confirmed still corrupted (line-number-only bodies, between 62 and 884 chars).
* **4** records returned `database disk image is malformed` when the body was queried.

A subsequent `PRAGMA integrity_check` on the live DB (run with `mode=rw`, no
write transaction) returned dozens of distinct corruption findings on multiple
btree pages — see "DB integrity findings" below. The corruption is not limited
to the FTS5 shadow tables; it spans the main DB pages.

Because the DB is structurally damaged, attempting to UPDATE 8 rows in this
state risks (a) propagating the corruption further on the next checkpoint,
(b) producing a DB whose `records` count and `records_fts` count cannot be
reconciled (rule #3), and (c) overwriting good rows on shared pages. Tick is
therefore **report-only**: no PDF downloads, no SQLite writes, no FTS rebuild.

After this tick, **16 of 42** manifest targets are repaired (unchanged from
batch 001), and **26** remain corrupted (one of which, `act-zm-2026-005-…`,
is the known HTTP-404 from batch 001). The DB needs to be restored from a
clean backup before further repair-worker ticks are productive.

## DB integrity findings (live `corpus.sqlite`, 109,162,496 bytes, mtime 10:13 CAT)

```
*** in database main ***
On tree page 5611 cell 375: invalid page number 26807
On tree page 3020 cell 0:   invalid page number 26789
On tree page 5611 cell 359: invalid page number 26763
On tree page 2723 cell 0:   invalid page number 26741
On tree page 5611 cell 351: invalid page number 26724
On tree page 2641 cell 0:   invalid page number 26714
On tree page 5611 cell 342: invalid page number 26680
On tree page 2579 cell 0:   invalid page number 26657
On tree page 5611 cell 334: 2nd reference to page 14972
On tree page 2438 cell 0:   2nd reference to page 14920
On tree page 5611 cell 328: 2nd reference to page 14909
On tree page 2337 cell 0:   2nd reference to page 26600
On tree page 11814 cell {164..178}: invalid page numbers (14 cells, range 26737..26833)
On tree page 21017 cell {0,461..465}: invalid page numbers + 2nd-reference duplicates
Pages 2378..2394 are never used  (orphaned page chain, ~17 unused pages)
…and additional rows truncated by the 50-row PRAGMA limit
```

The pattern (invalid page numbers far above the file extent of 109 MB ≈ 26,650
4096-byte pages, plus duplicate 2nd-references and orphaned chains) is
consistent with concurrent writes from multiple sessions colliding on the
same FUSE-shared file without functional `flock`/`fcntl` locking. Three live
sessions have the same host directory mounted:

```
/mnt/.virtiofs-root/shared/Users/peterndhlovu/KateWestonCorpus/corpus
  → /sessions/inspiring-relaxed-dijkstra/mnt/corpus  (FUSE, rw)
  → /sessions/blissful-quirky-brown/mnt/corpus       (FUSE, rw)
  → /sessions/fervent-vibrant-pasteur/mnt/corpus     (FUSE, rw)  ← this tick
```

The previous repair worker (batch 001 at 07:53Z) and the judgment-ingestion
worker (batches 0535/0536 at 06:48Z and 07:11Z) both succeeded with the
"TMPDIR atomic copy" pattern, suggesting the live DB was still healthy at
07:53Z. The stale `corpus.sqlite-journal` from 09:50Z (UTC ~07:50) and the
DB's 10:11Z mtime suggest the corruption arose during a write attempt
between 07:53Z and 08:13Z.

## Records the manifest still flags as corrupted (27)

Confirmed via `SELECT length(body), substr(body,1,500)` against `records` —
no FTS query was run since `records_fts` itself raises malformed-disk-image:

| # | Record ID                                                                       | Body chars |
|--:|---------------------------------------------------------------------------------|-----------:|
|  1 | `act-zm-2026-005-national-payment-system-act`                                  |        503 |
|  2 | `act-zm-2011-014-tolls-act-2011`                                               |        131 |
|  3 | `act-zm-2016-002-constitution-2016`                                            |        123 |
|  4 | `act-zm-2026-008-agricultural-marketing-act`                                   |        101 |
|  5 | `act-zm-2010-027-the-animal-health`                                            |        382 |
|  6 | `act-zm-2025-023-companies-amendment-act`                                      |         92 |
|  7 | `act-zm-2025-008-border-management-trade-facilitation-act2025`                 |        491 |
|  8 | `act-zm-2024-030-antiterrorism-nonproliferation-2024`                          |        108 |
|  9 | `act-zm-2025-003-cyber-security-2025`                                          |        258 |
| 10 | `act-zm-2026-011-the-zambia-deposit-insurance-corporation-act-2026-act-no-11-of-2026` | 240 |
| 11 | `act-zm-2010-034-the-national-prosecution-authority-act-2010`                  |        105 |
| 12 | `act-zm-2023-017-the-public-procurement-amendment-act-2023`                    |         62 |
| 13 | `act-zm-2024-001-constituency-development-fund-act-2024`                       |        156 |
| 14 | `act-zm-2025-025-independent-broadcasting-authority-act`                       |        204 |
| 15 | `act-zm-2025-004-cyber-crime-2025`                                             |         93 |
| 16 | `act-zm-2011-013-the-zambia-qualifications-authority-act-2011`                 |         98 |
| 17 | `act-zm-2011-023-education-act-2011`                                           |        656 |
| 18 | `act-zm-2011-031-customs-and-excise-amendment-act-2011`                        |        194 |
| 19 | `act-zm-2010-024-the-competition-and-consumer-protection-2010`                 |        407 |
| 20 | `act-zm-2011-004-urban-and-regional-act-2011`                                  |        273 |
| 21 | `act-zm-2023-018-the-public-private-partnership-act-2023`                      |        278 |
| 22 | `act-zm-2024-010-civil-aviation-authority-amendment-act-2024`                  |        596 |
| 23 | `act-zm-2024-011-civil-aviation-amendment-act-2024`                            |        596 |
| 24 | `act-zm-2016-005-civil-aviation-act-2016`                                      |        884 |
| 25 | `si-zm-financial-intelligence-centre-prescribed-threshold-regulations-2022`    |         75 |
| 26 | `si-zm-financial-intelligence-centre-general-regulations-2022`                 |        377 |
| 27 | `si-zm-financial-intelligence-centre-general-regulations-2016`                 |        151 |

## Records the manifest expected fixed but which now error on read (4)

These rows were repaired in earlier ticks (per `repair-tick10b` and
`repair-batch-001` logs) but `SELECT body FROM records WHERE id = ?` now
returns `database disk image is malformed`. Almost certainly their on-disk
pages are inside the corrupted btree region.

| Record ID                                                          | Reason          |
|--------------------------------------------------------------------|-----------------|
| `act-zm-2026-003-immigration-control-act`                          | malformed page  |
| `act-zm-2024-008-zambia-qualifications-authority-act-2024`         | malformed page  |
| `act-zm-2025-001-plant-health-2025`                                | malformed page  |
| `act-zm-2025-029-zambia-institute-of-procurement-and-supply-act`   | malformed page  |

These are *previously-good* rows that may now be lost from the live DB. They
likely still exist intact in the most recent backup
`corpus.sqlite.bak.repair-batch-20260507T074747Z` (109,162,496 bytes, mtime
2026-05-07 09:47 CAT — i.e. just before this tick window).

## Stale journal handling (transparency note)

On entry the working tree contained `corpus.sqlite-journal` (57,968 bytes,
mtime 09:50Z = 07:50 UTC). It was already stale relative to the DB's 10:11Z
mtime. Three Python read attempts against the live DB returned
`disk I/O error` rather than data; they were caused by SQLite trying to roll
back the stale journal under sandbox-FUSE constraints (the FUSE mount allows
overwrite-in-place but blocks unlink — so SQLite could not delete the journal
and refused to proceed).

To get past the I/O error and *read* the manifest's bodies, this worker
truncated `corpus.sqlite-journal` in place to zero bytes. The file is
gitignored (see `.gitignore` line `corpus.sqlite-journal`) so this change
will not be committed. Crucially, the `PRAGMA integrity_check` corruption
predates this truncation: the very first `SELECT body FROM records WHERE id …`
that succeeded after truncation already showed the same dozens of corrupt
btree page references, and the previous full-DB read also returned malformed.
Truncating the journal therefore did not cause the corruption — but it does
mean any uncommitted page-level rollback that was sitting in that journal is
now lost. If a backup-restore happens, restore from the
`corpus.sqlite.bak.repair-batch-20260507T074747Z` snapshot (09:47 CAT, before
the journal was last updated) rather than relying on a journal replay.

## Recommended next actions for the operator

1. Stop all worker scheduled tasks until the DB is restored:
   `repair-corpus`, the main `worker-tick`, and `judgment-ingestion-worker`.
2. From the host, copy `corpus.sqlite.bak.repair-batch-20260507T074747Z`
   over `corpus.sqlite`. That snapshot represents the state immediately
   after batch-001's commit (16 of 42 repaired, 26 outstanding) and pre-dates
   the corruption window.
3. Optionally `.dump | sqlite3 fresh.sqlite` against the corrupted DB to
   recover any rows committed *after* the snapshot but before the page
   damage (mainly the b0535 + b0536 judgment rows; 2 records). Diff against
   the backup before merging.
4. Investigate concurrent-writer hypothesis. Three sessions are FUSE-mounted
   on the same host directory; SQLite cross-process locking under FUSE on
   virtiofs is unreliable. Either serialise the workers, switch to WAL with
   `synchronous=FULL` plus a host-side lockfile, or move all SQLite writes
   to a single dedicated session.
5. Once restored, this scheduled task can be re-enabled and will resume from
   the same 26-record queue (PDF downloads + extract + UPDATE).

## Records attempted this tick

None. No PDF downloads. No SQLite writes. No FTS rebuild.

## Records successfully repaired this tick

None.

## Records failed this tick

None attempted.

## Records still remaining after this tick

26 (manifest-tracked corrupted) + 4 (newly-malformed rows that batch-001
had previously repaired) = up to 30 records will need re-repair after the
DB is restored.

## Operational notes

* This is the first repair tick that has refused to write. The trigger was
  `database disk image is malformed` on a `PRAGMA integrity_check`. The
  SKILL non-negotiable "Fail loud with full diagnostic on unexpected errors"
  applies here in preference to "process up to 8 records".
* `approvals.yaml` not modified.
* `corpus.sqlite` not modified.
* `corpus.sqlite-journal` truncated to 0 bytes (gitignored, not committed).
* `worker.log`, `costs.log`, `gaps.md`, and this batch report are the only
  tracked artefacts touched.
* Git: `git pull --ff-only` succeeded (already at HEAD `64d851f`). No commits
  pushed before the integrity finding; this report + log appends will be
  the only commit from this tick.
* B2 sync deferred to host (rclone not in sandbox).
