# Batch b0705b-jiw — CoA reparse drain + orphan recovery (+1 records)

**Worker:** Zambia Authorities Corpus judgment ingestion worker (JIW)
**Tick start:** 2026-05-18T14:48:20Z
**Parser version:** `0.3.6-jiw-b0705b-reparse-drain`
**Mode:** reparse-deferred drain from on-disk raw PDFs + b0705 orphan recovery (zero net HTTP fetches)

## Context

The immediately-preceding tick (`b0705-jiw`) wrote a record JSON to disk
and inserted into the DB transaction successfully but COMMIT failed with
`disk I/O error`. Root cause: the corpus directory is mounted via bindfs
which blocks `unlink()`. SQLite's default `journal_mode=DELETE` performs
`unlink()` on the journal file as the final step of COMMIT, which the
mount layer rejects.

This tick (`b0705b-jiw`) mitigates by setting `PRAGMA journal_mode=TRUNCATE`
which truncates the journal to 0 bytes on commit instead of deleting it.
The journal file `corpus.sqlite-journal` was manually truncated at the
start of this tick to clear b0705's failed-commit residue.

## Records inserted (1)

| ID | Case number | Outcome | Date | Judges | Note |
|---|---|---|---|---|---|
| `judgment-zm-2025-coa-170-mukamunya-homeowners-association-trust-registreed-trustees-v-leslie-szeftel-1-ot` | APP/170/2025 | allowed | 2025-04-29 | Chashi Ngulube Banda Bobo JJA | orphan-recovery |

## Records deferred (7)

- case=APP/304/2022 — reason: `quality-gate:body<200`
- case=APP/165/2024 — reason: `quality-gate:body<200`
- case=APP/024/2024 — reason: `quality-gate:body<200`
- case=APP/309/2023 — reason: `quality-gate:body<200`
- case=APP/127/2025 — reason: `operative-paragraph-undetected`
- case=APP/331/2024 — reason: `no-judges-extracted`
- case=APP/202/2023 — reason: `fuzzy-court-name-year-collision`


## Integrity checks

| Check | Result |
|---|---|
| CHECK1 (≥1 judge) | PASS |
| CHECK2 (issue_tags non-empty) | PASS |
| CHECK3 (outcome from enum) | PASS |
| CHECK5 (no dup IDs) | PASS |
| CHECK6 (raw_sha256 matches PDF on disk) | PASS |
| CHECK8 (records == records_fts) | 1958==1958 → PASS |

Errors (if any): []

## Counts

- records (DB): 1958 (+1)
- records_fts (DB): 1958 (+1)

## Fetch cost

- Network fetches: **0**
- Daily budget used: 269/500
- Reparse pool drained this tick: 7 new candidates + 1 orphans → 1 inserted, 7 deferred

## Recommendation for downstream workers

Persist `PRAGMA journal_mode=TRUNCATE` (or migrate to WAL where supported) so future commits do not fail on the bindfs unlink restriction. Truncating the journal file to 0 bytes is also a safe recovery action if a commit aborts.
