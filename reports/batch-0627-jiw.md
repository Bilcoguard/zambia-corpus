# Batch b0627-jiw — Judgment Ingestion Worker Tick Report

**Date**: 2026-05-13T06:08:34Z  
**Worker**: judgment-ingestion-worker  
**Verdict**: TICK ABORTED — no wire fetch, no db write, no git commit  
**Wall clock**: ~3 minutes

## Summary

This tick aborted before any wire fetch or database write, following the explicit
handoff rule from b0626-jiw: when sandbox `/` is at ≥ 99 % capacity, do not waste
budget on retries that will fail on commit.

One low-cost cleanup action was performed: the b0626-jiw orphan JSON for
`judgment-zm-2024-zmsc-11-frankson-musukwa-…` was renamed from the canonical
`records/judgments/zmsc/2024/` tree into `raw/zambialii/zmsc/2024/_orphan_b0626/`,
where it is preserved for audit but no longer pollutes the records tree.

## Disk state

```
Filesystem      Size  Used Avail Use% Mounted on
/ (sandbox)     9.6G  9.5G   15K 100% /
corpus mount    229G  217G   12G  95% /sessions/optimistic-epic-bohr/mnt/corpus
```

Zero bytes freed from `/` since b0626-jiw 50 minutes prior. All large `/tmp/`
artefacts are owned by prior-session UIDs and cannot be deleted by the current
session UID (`optimistic-epic-bohr`, uid=1849).

## Database state

| Metric            | Value      |
|-------------------|------------|
| `records`         | 1928       |
| `records_fts`     | 1928       |
| Parity (CHECK8)   | ✓ PASS     |
| Integrity         | ok (via `file:corpus.sqlite?mode=ro&immutable=1`) |
| `corpus.sqlite` mtime | 2026-05-13T06:07:51Z (43 s pre-tick) |
| `corpus.sqlite-journal` size | 57968 bytes (stale or recent commit, benign) |
| Read-write open attempts | all FAIL `disk I/O error` |

## Budget

| Metric                   | Value     |
|--------------------------|-----------|
| Fetches this tick        | 0         |
| Cumulative today (JIW)   | 21 / 500  |
| Records inserted         | 0         |
| Records deferred         | 0 new (b0626-jiw zmsc-11 orphan relocated, not re-deferred) |
| Bytes downloaded         | 0         |

## Actions taken

1. `git pull --ff-only` — already up to date (stale `.git/objects/maintenance.lock` could not be removed due to FUSE EPERM, but pull succeeded regardless).
2. `df /` — confirmed 100 % full, 15 kB free.
3. Sqlite read-only immutable probe — confirmed 1928/1928 parity preserved.
4. **Orphan relocation**: `records/judgments/zmsc/2024/judgment-zm-2024-zmsc-11-…json` → `raw/zambialii/zmsc/2024/_orphan_b0626/`. ✓ ok.
5. Appended diagnostic entries to `worker.log`, `costs.log`, `gaps.md`.
6. Stopped per b0626-jiw handoff rule #1.

## Actions deliberately NOT taken

- No new wire fetch (would have wasted budget on guaranteed-fail commit).
- No PDF download (same).
- No db write of any kind (records_fts triplet commits guaranteed to fail).
- No git commit, no git push (no corpus mutation worth committing).

## Next tick (b0628-jiw)

See gaps.md section "Next-tick (b0628-jiw) action items" for prioritised guidance.

The fundamental blocker (host-side `/tmp/` retention across worker sessions) is
**chronic** — observed for two consecutive ticks now (b0626-jiw, b0627-jiw) with
zero host-side intervention between them. Operator action recommended.
