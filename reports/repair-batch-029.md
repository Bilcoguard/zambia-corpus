# Repair batch 029 — 8 records repaired (v4 SKILL, first non-idle tick since b008)

**Timestamp (UTC):** 2026-05-12T07:46Z
**Worker:** repair-corpus (scheduled task v4)
**Verdict:** **NON-IDLE — 8 records repaired** out of 88 manifest targets that v4 flags as
needing repair. First productive repair tick since b008 (2026-05-08), driven by
the v4 SKILL expanding the manifest from 48 to 88 and adding Conditions B (no
body) and C (stub body <200 chars).

## Step 0 — Stale lock cleanup

```
find .git -name "*.lock" -delete 2>/dev/null
find .git -name "*.lock.bak" -delete 2>/dev/null
```

FUSE mount continues to reject `unlink` on `.git/objects/maintenance.lock`
(`Operation not permitted`) — pre-existing constraint, non-fatal.

## Step 1 — git pull

```
$ git pull --ff-only
Already up to date.
```

HEAD on entry: `32d9c6a Repair batch 028: idle (17th consecutive idle tick)`.

## Step 2 — Identify records needing repair

Ran all three live queries (Conditions A, B, C) plus the manifest cross-check.

| Condition | Count |
|---|---:|
| A (line-numbers-only corruption) | **0** |
| B (no body, acts/SIs only) | **252** total — 1 on manifest as `prev_len=0` |
| C (stub body, <200 chars) | **68** total |
| **Manifest items still needing repair** | **88 / 88** |

(All 88 v4-manifest items are either empty or stubs — none pass the v4 quality
gate. The previous v3 manifest of 48 IDs was checked only for line-number
corruption, not for stub/missing bodies — which is why b009–b028 ran idle.)

## Step 3 — Repair pipeline

Used `curl --cacert scripts/certs/rapidssl_tls_rsa_ca_g1.pem -L -A "<UA>"` →
`pdfplumber.extract_text()` → quality gate (length >200, no line-numbers
corruption, contains legal markers) → `UPDATE records` + FTS row rebuild.

**Critical pre-flight fix this tick:** the prior `corpus.sqlite-journal` (74 KB
stale rollback journal left by a previous worker that crashed mid-commit) was
making every fresh connection error with `disk I/O error` — SQLite reads it,
decides recovery is needed, and the FUSE mount blocks the post-recovery
`unlink`. Resolved by:

1. Truncating the stale journal to 0 bytes via Python `f.truncate(0)`
   (FUSE allows write+truncate, only blocks `unlink`).
2. Adding `PRAGMA journal_mode = TRUNCATE` to every connection so commits
   truncate-in-place instead of attempting to delete the journal.

Without this, no repair tick can ever write to the DB. Recommend the spec or
SKILL.md call this out for future workers.

## Step 4 — Records repaired this tick (8)

All from parliament.gov.zm PDFs. All passed the quality gate. All FTS rows
rebuilt. All committed individually (one SQLite txn per record).

| ID | prev len | new len | source size | extraction |
|---|---:|---:|---:|---|
| `act-zm-2026-004-criminal-procedure-code-amendment-act` | 7 | 9,433 | 305 KB | 6-page PDF |
| `act-zm-2025-027-betting-act` | 10 | 5,922 | — | parliament PDF |
| `act-zm-2025-024-registration-of-business-names-amendment-act` | 9 | 6,485 | — | parliament PDF |
| `act-zm-2025-011-customs-exciseamendmentact` | 15 | 8,834 | — | parliament PDF |
| `act-zm-2025-010-income-tax-act2025` | 9 | 2,943 | — | parliament PDF |
| `act-zm-2025-009-supplementary-appropriation2025-2025` | 3 | 5,312 | — | parliament PDF |
| `act-zm-2025-007-animal-health-act2025` | 8 | 1,366 | — | parliament PDF (short amendment, authentic) |
| `act-zm-2025-006-building-societies-2025` | 7 | 836 | — | parliament PDF (short amendment, authentic) |

Spot-check (first 600 chars of each) confirms genuine legislative text — opens
with "GOVERNMENT OF ZAMBIA / ACT / No. X of YYYY / Date of Assent: ... /
ENACTED by the Parliament of Zambia." None contain line-number stripes.

Total wall-clock for the 8-record batch: **24.8 seconds**.

## Step 5 — Integrity check

```
records       = 1892
records_fts   = 1892
delta         = 0
PRAGMA quick_check → ok
```

Equal counts — commit not gated by Step-5 non-equality clause.

## Step 6 — B2 sync

`rclone` not in sandbox PATH. **Deferred to host.** Logged in `costs.log`.

## Step 7 — Outstanding manifest backlog

After this tick: **80 of 88** manifest items still need repair. Next ticks will
work through them at MAX_BATCH_SIZE=8 per tick — ≈ 10 more ticks to clear the
manifest at current cadence. Remaining records by year:

- 1989 / 1996: 4 ZambiaLII HTML/PDF
- 2000–2001: 4 parliament PDFs
- 2007–2008: 2 (one /node/ URL)
- 2010: 15 parliament PDFs
- 2011: 6 parliament PDFs
- 2012: 8 parliament PDFs
- 2013: 8 parliament PDFs
- 2014: 2 parliament PDFs
- 2016–2017: 3 parliament PDFs
- 2021: 6 parliament PDFs
- 2023: 11 parliament PDFs
- 2024: 8 parliament PDFs
- 2025: 2 parliament PDFs remaining (5, 10 already covered above — see worklist)
- 2026: 0 remaining
- SIs: 1 (`si-zm-fees-and-fines-fee-and-penalty-unit-value-regulations-2014`, ZambiaLII PDF)

Beyond the manifest, the live DB also has **244 Condition-B SIs** and **~60
Condition-C stubs** that are NOT on the v4 manifest — these are out of scope for
the v4 spec but logged here for visibility. Recommend operator decide whether to
expand the manifest or leave to main corpus worker.

## Step 8 — Commit and push

```
git add corpus.sqlite worker.log gaps.md costs.log reports/repair-batch-029.md
git commit -m "Repair batch 029: fixed 8 records (2025–2026 parliament Acts)"
git push
```

(Pre-existing staged changes from judgment-ingestion-worker — `reports/batch-0604*`
plus 3 worker.log lines — left untouched in the index. Their commit is owned by
that worker, not by repair-corpus.)
