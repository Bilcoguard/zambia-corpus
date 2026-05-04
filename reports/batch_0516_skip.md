# Batch 0516 — judgment-ingestion-worker SKIP (concurrent-worker yield)

- **Tick UTC**: 2026-05-04T06:32:25Z
- **Worker**: judgment-ingestion-worker (session `intelligent-magical-brown`, uid 1586)
- **Action**: NO-WRITE / NO-FETCH / NO-COMMIT skip — yielded to concurrent worker
- **Concurrent worker**: session `relaxed-blissful-wright` (uid 1589, PID 3459)

## Why this tick yielded

When this worker entered batch-0516 work on the b0515 next-tick recommendation
(continue ZMSC 2024 sweep, nums 26..19), the `_work/b0516/` directory was
already populated by the `relaxed-blissful-wright` session, which had:

| artifact | timestamp (local UTC+2) | content |
|---|---|---|
| `_work/b0516/head_probe.log` | 2026-05-04 08:27:54 | 8 HEAD probes (nums 26..19) all 302 → date-canonical URLs |
| `_work/b0516/fetch.log` | 2026-05-04 08:30:15 | 8/8 fetches OK (HTML + PDF for every num) |
| `_work/b0516/fetch_results.json` | 2026-05-04 08:30 | full fetch metadata |
| `_work/b0516/parse.log` | 2026-05-04 08:30 | parser_v0.3.2 ran on all 8 candidates |
| `_work/b0516/parse_summary.json` | 2026-05-04 08:30 | 6 written, 2 deferred |
| `raw/zambialii/judgments/zmsc/2024/judgment-zm-2024-zmsc-{19,20,21,22,23,24,25,26}-*.{html,pdf}` | 2026-05-04 08:28..08:30 | all 16 raw artifacts on disk |
| `records/judgments/zmsc/2024/judgment-zm-2024-zmsc-{19,20,21,23,24,25}-*.json` | 2026-05-04 08:30 | 6 record JSONs written |

Paths inside `parse_summary.json` reveal the writing session as
`/sessions/relaxed-blissful-wright/mnt/corpus/...`, confirming a different
Claude session — not this one — produced the records.

`origin/main` HEAD is still at `dfc9ccd` (b0515 idle heartbeat receipt), so
`relaxed-blissful-wright` has not yet committed/pushed; their commit is
still in flight.

## What `relaxed-blissful-wright` produced (for cross-reference)

Per `_work/b0516/parse_summary.json`:

| # | id | outcome | source |
|---|---|---|---|
| 1 | judgment-zm-2024-zmsc-25-finsbury-investments-limited-v-murray-and-roberts | dismissed | pdf-tail-2pages |
| 2 | judgment-zm-2024-zmsc-24-billis-farm-limited-and-anor-v-molosoni-chipabwamb | allowed | pdf-tail-2pages |
| 3 | judgment-zm-2024-zmsc-23-stephen-mwape-v-the-people | dismissed | summary |
| 4 | judgment-zm-2024-zmsc-21-benson-kaunda-v-the-people | dismissed | pdf-tail-2pages |
| 5 | judgment-zm-2024-zmsc-20-chanda-mwape-and-anor-v-the-people | (see file) | (see file) |
| 6 | judgment-zm-2024-zmsc-19-francis-phiri-v-the-people | (see file) | (see file) |

Deferred (parser_v0.3.2 `html_no_summary_pdf_no_match`):
- zmsc/2024/26 — Jayesh Shah v Mwenda Mwimanenwa Nyambe and Anor
- zmsc/2024/22 — George Banda v The People

These two join the standing v0.3.3-pending cohort (which would have grown
from 7 to 9 if this tick had attempted the same parse). All raw artifacts
retained on disk for future reparse under parser v0.3.3 (Peter approval
pending per BRIEF.md non-negotiable on parser vocabulary changes).

## Why duplicate workers are running

`mcp__scheduled-tasks__list_scheduled_tasks` from this session lists three
tasks:

- `zambia-corpus-tick` — main worker, every 30 min, lastRunAt
  `2026-05-04T06:24:28Z` (this is the `kind-eager-sagan` session, uid 1588)
- `judgment-ingestion` — every hour at :06, lastRunAt
  `2026-05-04T06:24:55Z` (jitter 339 s)
- `update-fuel-stock` — unrelated

Only ONE `judgment-ingestion` schedule is visible from this session, but
TWO judgment-ingestion-worker Claude sessions are running concurrently
(`intelligent-magical-brown` uid 1586 = me, and `relaxed-blissful-wright`
uid 1589 = the active worker). This means either:

1. Cowork-mode fanned out the same scheduled task into two parallel
   sessions (harmless if the workers coordinate via git, but in
   practice they collide on `_work/b0516/` and on `.git/*.lock`);
2. A second schedule exists for the same task that this session cannot
   list (perhaps registered under a different scope); or
3. Manual replay overlapped with the scheduled fire.

Recommended: Peter to audit Cowork scheduled-task configuration so that
only ONE judgment-ingestion-worker fires per hour. The duplicate
contributes to the lock-conflict and `_stale_locks_*` accumulation
problem (see also BRIEF integration-cycle observations).

## FUSE delete-deny mount (root cause of the long-standing lock-cleanup pattern)

`mount` listing for the corpus directory shows:

```
/mnt/.virtiofs-root/shared/Users/peterndhlovu/KateWestonCorpus/corpus
  → /sessions/intelligent-magical-brown/mnt/corpus
  type fuse (rw,nosuid,nodev,relatime,user_id=0,group_id=0,
             default_permissions,allow_other)
```

The `bindfs` process for the user-folder mount is launched with the
`--delete-deny` flag visible in `ps`:

```
/usr/bin/bindfs -u 1589 -g 1589 --delete-deny -o nonempty -p u=rwX:go=
  /mnt/.virtiofs-root/shared/Users/peterndhlovu/KateWestonCorpus/corpus
  /sessions/relaxed-blissful-wright/mnt/corpus
```

Effect: `rm` (and Python `os.unlink`) on existing files in the corpus
fails with `Operation not permitted`. New files created in-session can
be deleted within that session. **Importantly: `os.rename()` succeeds,
which is why the codebase's standing workaround is to rename git lock
files to `_stale_locks_b<NNNN>_<name>.bak.<ts>` rather than delete
them.** The task header's prescribed cleanup
`find .git -name ".lock" -delete` matches the literal name `.lock`
(without glob), so it never deletes anything; the *real* lock files
(`index.lock`, `HEAD.lock`, `ORIG_HEAD.lock`, `objects/maintenance.lock`)
require the rename workaround used by previous batches.

This worker successfully renamed three live locks at start of tick
(`_stale_locks_b0516_*` markers in repo root) and the `git pull` then
ran clean (already up to date with `origin/main`). Three new ghost
locks created by `git fetch`/`pull` cannot be removed; they are inert
and do not block the next tick if it again uses the rename workaround.

## Worker accounting this tick

- HTTP requests issued by this worker: **0** (all fetching done by
  `relaxed-blissful-wright`)
- Records written by this worker: **0**
- Records deferred by this worker: **0**
- Daily judgment-worker budget consumed by this worker: **0 / 500**
  (the `relaxed-blissful-wright` session will log its own ~16 fetch
  cost separately when it commits; this worker did not double-count)
- approvals.yaml: **NOT modified** (Phase 5 human-only confirmation rule)

## Integrity (sanity-only spot-check, since no records written)

- `git fetch` succeeded; `origin/main` resolves and is reachable
- corpus/.git is in a usable state after rename-based lock cleanup
  (read-only operations clean; writes will warn-on-unlink but succeed)
- 372 untracked files in repo root (mostly historical `_stale_locks_*`
  cruft from previous ticks plus this tick's three new entries) —
  unchanged contribution profile from b0515

## Recommended next tick (whichever worker fires)

1. `relaxed-blissful-wright` to complete its commit/push of batch-0516
   (6 records: zmsc/2024/{19, 20, 21, 23, 24, 25}; 2 deferred:
   zmsc/2024/{22, 26}).
2. Continue ZMSC 2024 inner-num DESC sweep on remaining nums:
   `{18, 17, 16, 15, 14, 13, 12, 11}` (8 candidates) — these are the
   next batch in the most-recent-first order. Inner gaps to be
   discovered via HEAD probes.
3. Optional concurrent: enumerate ZMSC 2024 inner gaps systematically
   (HEAD probes for nums 1..34 minus already-covered) so future batches
   skip 404s without burning fetch budget.

## Cohort cumulative (judgment-ingestion-worker since b0504, **excluding this skip**)

| tick   | written | deferred | 404 |
|:-------|--------:|---------:|----:|
| b0504/0506 | 5 | 3 | 0 |
| b0511      | 4 | 1 | 3 |
| b0515      | 5 | 3 | 0 |
| b0516 (other session) | 6 (pending push) | 2 (pending push) | 0 |
| **total**  | **20** | **9** | **3** |

Phase 5 corpus judgment count after `relaxed-blissful-wright` push will
be 111 → **117**. Still IN BAND for Phase 5 target (100–160).

## B2 sync

Deferred (rclone not in sandbox); will be picked up host-side when the
other worker logs its push receipt.
