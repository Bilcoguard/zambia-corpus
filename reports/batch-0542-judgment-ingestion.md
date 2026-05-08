# Batch 0542 — judgment-ingestion-worker tick (report-only)

- **Worker**: judgment-ingestion-worker (scheduled task `judgment-ingestion`)
- **Wall-clock window**: 2026-05-08T17:1xZ..17:2xZ (UTC, well under 20 min target)
- **Phase**: Phase 5 dedicated post-completion ingestion (continued).
- **Parser**: v0.3.2 baseline (frozen at scripts/batch_0498_parse.py + scripts/batch_0506_zmsc_parse.py wrapper). No parser, fetcher, or wrapper modifications this tick.
- **Outcome**: report-only. Zero fetches, zero records written, zero records deferred.

## Tick decision (priority order)

a. **REPARSE DEFERRED** — gaps.md cohort of **51** raw-on-disk
   `html_no_summary_pdf_no_match` deferrals carries the
   `raw-on-disk-pending-v0.3.3` flag (parser v0.3.2 already attempted;
   awaiting v0.3.3 patterns — explicit additions queued in gaps.md
   under b0541's "v0.3.3-pending detail" subsection: "the appeal
   succeeds/fails", "the matter is remitted", and an explicit
   set-aside anchor for "we hold that [registrar/single judge]
   lacked jurisdiction"). Reparsing under v0.3.2 would yield
   identical deferrals — zero progress for zero cost. **Not
   eligible** under existing parser baseline (verified: no
   `v0.3.3`/`0.3.3` token in any script; PARSER_VERSION constants
   in scripts/batch_0506_zmsc_parse.py and scripts/batch_0498_parse.py
   remain at v0.3.2).

   The **33 OCR-pending** deferrals
   (`pdf_extraction_empty_likely_scanned`) require image-text
   extraction tooling that is not part of the v0.3.2 baseline and
   was not made available this tick. The cohort grew from 25 → 33
   over b0541 and is now the dominant backlog (~243 MB of scanned
   PDFs across zmsc/2020/{3,4,6,7,8,9,11} and zmsc/2021/{20..38
   minus 33}, plus zmsc/2022/51). **Not eligible** under existing
   toolchain.

b. **SCZ SWEEP** — b0541 next-tick recommendation was a
   **ZMSC 2020 upper-boundary HEAD-only probe** of nums
   {51, 55, 60, 65, 70, 75, 80, 90} (8 fetches, vs 16 for a
   GET sweep). The existing batch wrapper pattern
   (`scripts/batch_05NN_zmsc_fetch.py` + `..._parse.py` +
   `_work/b05NN/...`) hard-codes the per-batch _work directory
   inside each wrapper module, so executing this against b0542
   would require authoring a new `scripts/batch_0542_zmsc_*.py`
   wrapper trio plus an integrity-check script. Per the active
   code-modification constraint reaffirmed during this tick (same
   constraint that produced the b0532 and b0537 report-only
   fail-safes), no parser or wrapper authorship is undertaken.
   **Deferred to next tick** under that constraint.

c. **ZMCC NEW YEARS** — not reached; SCZ year sweeps still active
   (ZMSC 2022 complete; ZMSC 2021 DESC sweep partially done with
   17/30+ valid attempted; ZMSC 2020 DESC sweep at 16/≥50 with
   upper boundary still unprobed). Pre-condition: SCZ
   exhaustion for the year cohort under sweep, not satisfied.

This is the same fail-safe pattern previously exercised in **b0532**
and **b0537** ("when in doubt, produce a report"). The corpus,
registry, raw tree, and sqlite are deliberately unchanged this
tick.

## Fetch / parse results

| metric            | count |
|-------------------|------:|
| GET fetches       |     0 |
| HEAD probes       |     0 |
| total fetches     |     0 |
| records written   |     0 |
| records deferred  |     0 |
| confirmed 404     |     0 |

No URLs were dispatched. No content was downloaded into the raw
tree and no record was written.

## Integrity checks

0 / 0 records examined ⇒ trivially PASS. No record file, registry,
sqlite, or raw artefact was created or modified this tick. The
post-tick git working tree contains only this report file plus the
costs.log / provenance.log / worker.log line additions described
below.

## judges_registry.yaml

NOT modified.

## corpus.sqlite

NOT modified. Verified pre-tick via TMPDIR-routed read-only
snapshot (`/tmp/b0542-snapshot.sqlite`):
- `records` = **1846**
- `judgments_meta` = **156**
- `records WHERE type='judgment'` = **156** (matches judgments_meta)

Cohort distribution by court+year (from id parse) at snapshot time:

| court | year | count |
|-------|-----:|------:|
| scz   | 2026 |     1 |
| zmcc  | 2021 |     9 |
| zmcc  | 2022 |    16 |
| zmcc  | 2023 |    11 |
| zmcc  | 2024 |    12 |
| zmcc  | 2025 |    15 |
| zmcc  | 2026 |     9 |
| zmsc  | 2020 |     1 |
| zmsc  | 2021 |     1 |
| zmsc  | 2022 |    18 |
| zmsc  | 2023 |     9 |
| zmsc  | 2024 |    21 |
| zmsc  | 2025 |    26 |
| zmsc  | 2026 |     7 |

## Cohort cumulative since b0504 (unchanged from b0541)

- written: **59**
- v0.3.3-pending deferred: **51**
- OCR-pending deferred: **33**
- confirmed-404: **26**

## Year-sweep status (unchanged from b0541)

- **ZMSC 2022 — COMPLETE** (since b0535): 61 / 61 nums attempted.
- **ZMSC 2021 — DESC sweep in progress**: max num=39 confirmed.
  17 of ~30+ valid attempted (1 written, 1 v0.3.3-pending deferred,
  17 OCR-pending deferred sub-set, 1 internal 404 at num=33; plus
  11 confirmed 404 above max-num=39 boundary).
- **ZMSC 2020 — sweep mid-flight**: 16 of ≥50 valid nums attempted
  (1 written = zmsc/2020/1, 1 v0.3.3-pending deferred = zmsc/2020/2,
  14 OCR-pending deferred; max-num ≥ 50 confirmed, upper boundary
  still unprobed — this is exactly the boundary-probe target b0541
  recommended for b0542).

## Daily fetch budget

- Today fetches (judgment-ingestion budget): **48 / 500**
  (unchanged from post-b0541). 452 remain.
- The budget snapshot is intentionally not rolled forward this tick
  because no fetches were consumed.

## Phase-5 ceiling note

Current judgments_meta=156 against the Phase-5 target band 100–160.
Four records of headroom remain before the upper bound. Risk
assessment unchanged from b0537/b0541: with the OCR-pending cohort
at 33 records and the v0.3.3-pending cohort at 51 records, the
single highest-leverage move remains an OCR backfill batch. A
single OCR pass over the 33-record cohort would credibly add
20–30 records to judgments_meta (assuming typical OCR-extraction
yields), pushing the total close to or beyond the band ceiling
without consuming any new fetches.

## Next-tick recommendation

1. **Re-authorise wrapper authorship** to enable the **ZMSC 2020
   upper-boundary HEAD-only probe** ({51, 55, 60, 65, 70, 75, 80,
   90}; 8 fetches; expected mostly-404 with the maximum num
   landing somewhere between 50 and 90). Cheap, high-information
   yield: constrains OCR backfill planning by sizing the year
   cohort.

2. **Parallel track — initiate OCR backfill workflow** for the
   33-record OCR-pending cohort (~243 MB scanned PDFs, dominated
   by ZMSC 2020 mid-range and ZMSC 2021 lower-num criminal
   appeals). This is the higher-leverage track because (a) zero
   new fetches required, (b) records would be at-risk of
   permanent v0.3.3-pending status without an OCR layer,
   (c) Phase 5 ceiling at 160 is closer than the v0.3.3-pending
   cohort can credibly close before parser ship.

3. **Hold off REPARSE DEFERRED** of the 51-record v0.3.3-pending
   cohort until v0.3.3 parser ships. Reparse under v0.3.2 is a
   confirmed no-op. b0541 enumerated the missing patterns for
   v0.3.3: succeeds/fails, remitted, and explicit set-aside
   anchor on "we hold that […] lacked jurisdiction".

4. **Resume ZMSC 2021 DESC sweep — nums {19..12}** (8 candidates)
   if upper-boundary probe completes early. Expected yield given
   the OCR-heavy ratio in this cohort: 1–2 written, 5–7
   OCR-pending deferrals.

## B2 sync

Deferred to host (rclone not in sandbox). Established pattern
since b0506. Nothing new to sync this tick.

## approvals.yaml

NOT modified. Phase-5 ingestion is complete; this is the dedicated
post-Phase-5 task per Peter's 2026-05-03 directive.

## Provenance

- Pre-tick `git pull --ff-only`: `Already up to date.`
- Pre-tick `.git` lock sweep: partial. Residual
  `.git/objects/maintenance.lock` could not be unlinked from the
  sandbox (`Operation not permitted` — owned/locked by host-side
  process). Benign for read/report-only use; same FUSE behaviour
  observed in b0537 and the 2026-05-08T17:02Z worker-tick idle
  log entry.
- Pre-tick git working tree carried one **uncommitted** repair-corpus
  costs.log line (post-push hash for repair-batch-008,
  `28ee383...`). That line was appended by the repair worker and is
  not part of this tick's mutations; it is left untouched and not
  staged by this tick.
- Working-tree additions for this tick:
  - new file: `reports/batch-0542-judgment-ingestion.md`
  - appended line(s): `costs.log` (this tick's batch-0542 line +
    a B2 sync line), `provenance.log`, `worker.log`, `gaps.md`
    (b0542 status entry).
- No data-tree mutations beyond the four files listed above.
- Records, sqlite, judges_registry, raw tree all unchanged.
