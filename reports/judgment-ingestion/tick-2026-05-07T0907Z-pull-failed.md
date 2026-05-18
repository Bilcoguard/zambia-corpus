# Judgment-Ingestion Worker Tick Report — 2026-05-07T09:07:54Z (PULL-FAILED, no-op)

## Outcome
- **Status:** ABORTED before any work — `git pull --ff-only` failed.
- **Records written:** 0
- **Records deferred:** 0
- **Fetches consumed:** 0
- **Daily budget:** 62/500 (unchanged)
- **Corpus state:** unchanged (no commits, no DB writes, no judges_registry edits)

## Pull failure
```
fatal: bad object refs/remotes/origin/main.lock.bak.b003.1778144672
error: https://github.com/Bilcoguard/zambia-corpus.git did not send all necessary objects
```

## Root cause
Three stale lock/lock-backup ref files remain in `.git/refs/remotes/origin/` after prior batches:

| Path | Size | Notes |
|---|---|---|
| `main.lock` | 0 bytes | Stale fetch lock |
| `main.lock.bak.20260503T170054Z` | 41 bytes | Old backup |
| `main.lock.bak.b003.1778144672` | **1 byte** | Truncated → causes 'bad object' fatal |

The pre-flight `find .git -name "*.lock*" -delete` failed silently because the sandbox FUSE mount returns EPERM on `unlink()` for these specific paths. Subsequent explicit `rm` attempts confirmed: "Operation not permitted".

## Decision
Per skill rule "If the pull fails, log the error to worker.log and stop." — logged and stopped. No alternative paths attempted (no work without a successful sync; cannot risk diverging from `origin/main` while the main worker may also be pushing).

## Recommendation for host operator
From a privileged shell on the host (outside the sandbox):
```
cd ~/KateWestonCorpus/corpus
rm -f .git/refs/remotes/origin/main.lock \
      .git/refs/remotes/origin/main.lock.bak.*
git fetch origin && git status
```
Once cleaned, the next scheduled tick (T+60 min) will proceed with the queued plan from b0536:
1. Reparse deferred (50 v0.3.3-pending + 10 OCR-pending on disk) — zero fetch cost. Prefer the v0.3.3-pending cohort first.
2. ZMSC 2021 DESC sweep continuation, nums {27..20}.
3. If exhausted, ZMCC older years.

## Files touched
- `worker.log` — appended pull-failure diagnostic block.
- `reports/judgment-ingestion/tick-2026-05-07T0907Z-pull-failed.md` — this file.

approvals.yaml NOT modified (per non-negotiable rule).
