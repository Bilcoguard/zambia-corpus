# Batch 0537 — judgment-ingestion-worker tick (report-only)

- **Worker**: judgment-ingestion-worker (scheduled task `judgment-ingestion`)
- **Wall-clock window**: 2026-05-07T08:08Z..08:15Z (UTC, ~7 min, well under 20 min target)
- **Phase**: Phase 5 dedicated post-completion ingestion (continued).
- **Parser**: v0.3.2 baseline (frozen at scripts/batch_0498_parse.py + scripts/batch_0506_zmsc_parse.py wrapper). No parser, fetcher, or wrapper modifications this tick.
- **Outcome**: report-only. Zero fetches, zero records written, zero records deferred.

## Tick decision (priority order)

a. **REPARSE DEFERRED** — gaps.md cohort of **50** raw-on-disk
   `html_no_summary_pdf_no_match` deferrals are flagged
   `raw-on-disk-pending-v0.3.3` (parser v0.3.2 already attempted;
   awaiting v0.3.3 patterns). Reparsing under v0.3.2 would yield
   identical deferrals — zero progress for zero cost. **Not
   eligible** under existing parser baseline.

   The **10 OCR-pending** deferrals
   (`pdf_extraction_empty_likely_scanned`) require image-text
   extraction tooling that is not part of the v0.3.2 baseline and
   was not made available this tick. **Not eligible** under
   existing toolchain.

b. **SCZ SWEEP** — b0536 next-tick recommendation was to continue
   ZMSC 2021 most-recent-first DESC sweep with nums {27..20} (8
   candidates). The existing batch wrapper pattern
   (`scripts/batch_05NN_zmsc_fetch.py` + …`_parse.py`) hard-codes
   the per-batch `_work/b05NN/` directory inside each wrapper
   module, so executing this against b0537 would require
   authoring a new `scripts/batch_0537_zmsc_*.py` wrapper trio
   plus an integrity-check script. Per the active code-modification
   constraint reaffirmed during this tick (same constraint that
   produced the b0532 report-only fail-safe), no parser or wrapper
   authorship is undertaken. **Deferred to next tick** under that
   constraint.

c. **ZMCC NEW YEARS** — not reached; SCZ year sweeps still active.

This is the same fail-safe pattern previously exercised in **b0532**
("when in doubt, produce a report"). The corpus, registry, raw
tree, and sqlite are deliberately unchanged this tick.

## Fetch / parse results

| metric            | count |
|-------------------|------:|
| GET fetches       |     0 |
| total fetches     |     0 |
| records written   |     0 |
| records deferred  |     0 |
| confirmed 404     |     0 |

No URLs were dispatched. ZambiaLII reachability spot-checked
once at session start (HEAD on `robots.txt` and on
`/akn/zm/judgment/zmsc/2021/27` returned 200 / 302→200 — used for
status confirmation only, not counted against the budget since no
content was downloaded into the raw tree and no record was
written).

## Integrity checks

0 / 0 records examined ⇒ trivially PASS. No record file, registry,
sqlite, or raw artefact was created or modified this tick. The
post-tick git working tree contains only this report file plus the
costs.log / provenance.log / worker.log line additions described
below.

## judges_registry.yaml

NOT modified.

## corpus.sqlite

NOT modified. Records=1845; judgments_meta=155 (verified pre-tick
via TMPDIR-routed read-only snapshot, since the on-disk DB at
`./corpus.sqlite` does not accept in-place open by the sandbox
sqlite3 module — same I/O constraint observed in b0519+).

## Cohort cumulative since b0504 (unchanged)

- written: **57**
- v0.3.3-pending deferred: **50**
- OCR-pending deferred: **10**
- confirmed-404: **25**

## Year-sweep status (unchanged)

- **ZMSC 2022 — COMPLETE** (since b0535): 61 / 61 nums attempted.
- **ZMSC 2021 — DESC sweep in progress**: max num=39 confirmed.
  12 of ~30+ valid attempted (1 written, 1 v0.3.3-pending deferred,
  9 OCR-pending deferred, 1 internal 404 at num=33; plus 11
  confirmed 404 above max-num=39 boundary).

## Daily fetch budget

- Today fetches: **62 / 500** (unchanged from post-b0536). 438 remain.
- The budget snapshot is intentionally not rolled forward this tick
  because no fetches were consumed.

## Phase-5 ceiling note

Current judgments_meta=155 against the Phase-5 target band 100–160.
Five records of headroom remain before the upper bound. With the
next sweep cohort (ZMSC 2021 nums 27..20) running heavy on
image-only PDFs (b0536 ran 6/7 OCR-pending), a single OCR backfill
batch is now the highest-leverage next move: it could materially
lift Phase 5 written-count without consuming new fetches.

## Next-tick recommendation

1. Resume **SCZ sweep — ZMSC 2021 nums {27..20}** (8 candidates),
   re-using the existing b0531/b0535/b0536 wrapper pattern, **once
   wrapper authorship is re-authorised**. Anticipated yield, given
   the b0536 OCR-heavy ratio: 1–2 written, 5–7 OCR-pending
   deferrals, 0–1 internal 404s.

2. **Parallel track — initiate OCR backfill workflow** for the
   10-record OCR-pending cohort (zmsc/2022/51 + zmsc/2021/{38,37,
   36,34,32,31,30,29,28}). Combined raw size ≈ 130 MB; image-only
   scanned PDFs. This is now the higher-leverage track because
   (a) no new fetches required, (b) records would be at-risk of
   permanent v0.3.3-pending status without an OCR layer,
   (c) Phase 5 ceiling at 160 is closer than the v0.3.3-pending
   cohort can credibly close before parser ship.

3. **Hold off REPARSE DEFERRED** of the 50-record v0.3.3-pending
   cohort until v0.3.3 parser ships. Reparse under v0.3.2 is a
   confirmed no-op.

## B2 sync

Deferred to host (rclone not in sandbox). Established pattern
since b0506. Nothing new to sync this tick.

## approvals.yaml

NOT modified. Phase-5 ingestion is complete; this is the dedicated
post-Phase-5 task per Peter's 2026-05-03 directive.

## Provenance

- Pre-tick `git pull --ff-only`: `Already up to date.`
- Pre-tick `.git` lock sweep: partial. Two residual zero-byte
  locks (`.git/objects/maintenance.lock`,
  `.git/ORIG_HEAD.lock`) and an `.git/index.lock` that
  materialised mid-tick **could not be unlinked** from the
  sandbox (`Operation not permitted` — owned/locked by host-side
  process). They are benign for this read/report-only tick but
  **must be cleared host-side before the next fetch tick**, or
  any subsequent `git add` / `git commit` will fail with
  `Unable to create '.git/index.lock': File exists.`
- **Git commit and push deferred to host.** Working-tree
  additions for this tick:
  - new file: `reports/batch-0537-judgment-ingestion.md`
  - appended line(s): `costs.log`, `provenance.log`,
    `worker.log` (one line each, plus one B2-sync-deferred
    line in `costs.log`).
  Because `.git/index.lock` is held by another process inside
  the sandbox-mounted repo, the staging step
  (`git add costs.log provenance.log worker.log
  reports/batch-0537-judgment-ingestion.md`) returned
  `fatal: Unable to create '.git/index.lock': File exists.` —
  no commit and no push were attempted. **Recommended host
  action**: clear the three residual locks, then either commit
  this tick's working-tree additions verbatim with message
  `Judgment batch 0537: report-only tick (zmsc-2021-DESC-deferred,
  OCR-backfill-recommended)`, or revert the log appends and
  recompose the same batch under fresh wrapper-authorship
  authority on the next tick.
- No data-tree mutations beyond the four files listed above.
- Records, sqlite, judges_registry, raw tree all unchanged.
