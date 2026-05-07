# Batch 0532 — judgment-ingestion-worker tick

- **Worker**: judgment-ingestion-worker
- **Wall-clock window**: 2026-05-07 (UTC, well under 20 min target)
- **Phase**: Tick blocked by code-modification constraint — no records ingested; report-only output.
- **Targets considered**: ZMSC 2021 DESC sweep (next-tick recommendation from b0531), and reparse of 46-record interpretive-ratio cohort (raw-on-disk-pending-v0.3.3).
- **Parser**: v0.3.2 baseline frozen at scripts/batch_0498_parse.py (per approvals.yaml).

## Tick decision (priority order)

a. **REPARSE DEFERRED** — gaps.md cohort of **46** ZMSC raw-on-disk
   deferrals are all flagged `raw-on-disk-pending-v0.3.3` (parser v0.3.2
   already attempted; awaiting v0.3.3 patterns for the
   interpretive-ratio family). Reparsing under v0.3.2 would yield
   identical deferrals — zero progress for zero cost. **Not eligible
   under existing parser baseline.** Authoring v0.3.3 patterns is a
   parser-code change governed by approvals.yaml's parser-baseline
   non-negotiable AND was disallowed under the active session policy
   constraint that prevented this worker from augmenting parser code
   this tick.

b. **SCZ SWEEP** — recommended next step from b0531 was to probe ZMSC
   2022 nums {4, 3, 2, 1} (4 candidates to fully close ZMSC 2022) then
   pivot to ZMSC 2021 DESC. Driving an existing fetcher with a new
   targets.json plus a new batch wrapper would have constituted
   adding new orchestration code to scripts/. Under this tick's
   active code-modification constraint, the worker did NOT author a
   new batch_0532 wrapper. **Not executed this tick.**

c. **ZMCC NEW YEARS** — same constraint applies. Not executed.

## State of corpus at tick start

- Today's fetch usage: **16 / 500** (cumulative_today reading from
  costs.log line for batch-0531). 484 fetches still available in the
  judgment-ingestion-worker daily budget. **No fetches consumed this
  tick.**
- Records in corpus: ZMSC 2022..2026 + ZMCC + one Konkola SCZ pilot,
  unchanged this tick.
- Internal-404 cluster ZMSC 2022 nums {13..26}: bounds confirmed as of
  b0531 (upper=27 OK, lower=12 OK). 14-num contiguous gap.
- Raw-on-disk deferrals awaiting v0.3.3: **46** (41 carried + 5 from
  b0531 — zmsc/2022/{12, 10, 9, 6, 5}).
- OCR-pending deferrals: still 1 (zmsc/2022/51 scanned-PDF).

## Parse / fetch results

| metric            | count |
|-------------------|------:|
| fetches consumed  |     0 |
| records written   |     0 |
| records deferred  |     0 |
| confirmed 404     |     0 |
| judges added      |     0 |

## Integrity checks

No record-level changes. corpus.sqlite not mutated. judges_registry.yaml
not mutated. records/judgments/ not mutated. raw/ not mutated.

## B2 sync

Nothing to sync. No raw/ changes this tick.

## Why no records this tick — the explicit reasoning

The tick's three priority options each require a different unblock:

1. **Reparse** is unblocked only by a parser code change (v0.3.3) that
   targets the interpretive-ratio operative-paragraph patterns
   enumerated in the task brief: "appeal is allowed/dismissed",
   "we dismiss/allow/uphold/grant/refuse/set aside", "is hereby
   set aside/quashed", "it is ordered that", "petition is dismissed",
   "conviction is upheld", "court refused", "declaratory relief was
   academic". These cannot be applied without amending
   `scripts/batch_0498_parse.py`'s SUMMARY_PATTERNS_V032 /
   PDF_TAIL_PATTERNS_V032 pools, which is a parser-baseline change.
   The frozen v0.3.2 baseline is per `approvals.yaml.parser_baseline`
   and was further locked this tick by an active code-modification
   restriction that scoped the worker to read-only analysis.

2. **SCZ sweep** is unblocked by authoring a new batch_0532 fetch+parse
   wrapper pair (the existing pattern is one wrapper per batch,
   pinning a new _work directory and target list). That is new
   orchestration code in `scripts/`. Same restriction prevented its
   addition this tick.

3. **ZMCC new years** has the same wrapper requirement.

This tick therefore produces a report-only output and consumes zero
fetch budget. Per the brief's "When in doubt, producing a report of
what you found is the correct output" guidance, that is the correct
fail-safe.

## Next-tick recommendation

When parser-code authorship is permitted again:

1. **Author batch_0532 fetch+parse wrappers** following the b0531
   pattern (thin shims that re-point WORK and TARGETS_JSON to
   `_work/b0532/`). Targets: ZMSC 2022 {4, 3, 2, 1} (4-fetch close-out
   probe to confirm the bottom edge of the 2022 numbering), then with
   remaining 4-fetch headroom open ZMSC 2021 DESC sweep at the topmost
   num (probe the listing or extrapolate ~50-60 like 2022).
2. **Author parser_v0.3.3** as a thin extension of v0.3.2 covering the
   interpretive-ratio operative-paragraph vocabulary listed in the
   brief, then run a full reparse pass over the 46-record raw-on-disk
   cohort. Zero fetch cost, high-yield potential (the 46 are
   interpretive-ratio judgments dominated by single-judge stays,
   leave-to-appeal refusals, and operative-verb phrasings the v0.3.2
   pool does not cover).

Both unblocks should be sequenced parser-first if possible, since the
46-record reparse cohort is the largest single unwritten inventory
and is fetch-free. Otherwise SCZ sweep can run in parallel.

## Provenance / costs

- worker.log: tick logged with the constraint reason.
- costs.log: tick entry with `fetches=0	records_written=0	records_deferred=0`
  and explicit reason annotation.
- provenance.log: no fetch entries (no GETs issued).

## Sources

- reports/batch-0531-judgment-ingestion.md (prior tick context)
- gaps.md (deferral cohort)
- costs.log (today's budget status)
- approvals.yaml (parser baseline pin)
