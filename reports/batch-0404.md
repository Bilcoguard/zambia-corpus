# Batch 0404 — Phase 5 Audit-Only Idle Tick

**Tick start (UTC):** 2026-05-01T12:33:16Z
**Tick id:** batch-0404
**Phase:** phase_5_judgments (approved+incomplete)
**Yield:** 0 records / audit-only (no parser run)
**Fresh fetches:** 0
**Cumulative today:** 0 / 2000
**Wall-clock:** under 5 min — well inside 20-min budget

## Status

This is the **29th consecutive substantive audit-only tick** (b0375..b0383 plus
b0385..b0404). The Phase 5 v0.3.1 reparse inventory remains fully exhausted.
The BRIEF.md five-consecutive-zero-discovery completion criterion remains fired
(originally fired b0379 and re-affirmed every substantive tick since).
`approvals.yaml` has not been touched since 2026-04-30T15:36:40Z (commit b24a938
by Peter, ~20h 56m at tick start, per `git log -1 --format=%cI -- approvals.yaml`).
No human approval has yet arrived for the three queued unblocks
(parser_v0.3.2 / OCR pipeline / ZMSC fresh-DESC-sweep).

Per the Phase 5 human-only confirmation rule (BRIEF.md non-negotiable §4 and
tick protocol step 10), the worker does not flip `approved` or `complete`
flags itself.

## Reparse-first inventory audit (step 5 of approvals.yaml `reparse_first` policy)

| Source | raw HTML | raw PDF | records | missing |
|---|---|---|---|---|
| ZMCC  | 142 | 141 | 53 | 89 (all already-deferred under v0.3.1) |
| ZMSC  |  25 |  24 | 24 |  0 (1 HTML stem is the `zmsc-index-page-1-20260424.html` index, non-blocking) |
| SCZ   |   1 (record-only, raw under `raw/pilot/judiciary-zm/`) |   — |  1 |  0 |
| **Total records** | | | **78** | |

No new addressable v0.3.1 candidates have appeared since b0378. Inventory is
byte-for-byte identical to b0386–b0403.

## gaps.md frequency cross-check (unchanged since b0379)

| Reason code | line count |
|---|---|
| html_no_summary_pdf_no_match | 114 |
| parser_v0.3.1_judges_no_comma_unhandled | 14 |
| pdf_extraction_empty_likely_scanned | 10 |
| multi_judge_separate_opinions_no_clear_majority_disposition | 2 |
| outcome_not_inferable_under_tightened_policy *(v0.3.0 generic, retained for historical accuracy; banned for new deferrals per approvals.yaml `deferral_reasons_locked`)* | 49 |
| parser_v0.3.1_token_unhandled | 0 |
| outcome_inferred_but_detail_unsafe | 0 |

`gaps.md` mtime: 2026-04-30T21:39:41+00:00 (last commit touching the file:
61d666e 2026-04-30T21:40:59Z). No write since b0379.

## Integrity check

Trivial PASS: no records written or deleted, so the schema/registry/hash/
cited_authorities clauses are not exercised against new material. Phase 5
repository-wide spot check this tick (seed=404):

- 78 record JSONs parsed cleanly (0 parse errors).
- 78/78 unique IDs (no duplicates within Phase 5 records/judgments/).
- 78/78 records carry the four required provenance fields (`source_url`,
  `source_hash`, `fetched_at`, `parser_version`) — 0 missing.
- 6/6 random-sample `source_hash` recompute matches against on-disk raw bytes
  — Sample seed=404:
  judgment-zm-2022-zmcc-26-michelo-v-sampa-and-anor (HTML),
  judgment-zm-2026-zmcc-08-munir-zulu-v-the-attorney-general-and-or (HTML),
  judgment-zm-2026-scz-09-konkola-v-ag (PDF, raw/pilot/judiciary-zm/),
  judgment-zm-2025-zmsc-21-joseph-v-the (PDF; ID slug-truncated, source_url
  resolves to /source.pdf — recomputed hash matches),
  judgment-zm-2026-zmsc-10-first-v-zubao (PDF; ID slug-truncated, source_url
  resolves to /source.pdf — recomputed hash matches),
  judgment-zm-2022-zmcc-28-kolala-v-zambia-postal-services-corporation (HTML).
- **Full-corpus pass:** 78/78 source_hash values resolve to a raw file on disk
  (sha256-indexed across `raw/zambialii/` and `raw/pilot/`). 0 orphans.
- 0 unresolved in-corpus `cited_authorities` / `amended_by` / `repealed_by` /
  `key_statutes` references among Phase 5 records.

## Fresh DESC sweep — still deferred

Fresh DESC sweep continues to be deferred per b0376–b0403 rationale:

1. ~85% of the existing ZMCC backlog defers `html_no_summary_pdf_no_match` — a
   parser-vocabulary limitation a fresh sweep would only reproduce while
   consuming fetch budget that v0.3.2 will be far more efficient with.
2. The ZMSC backlog is tiny and already in inventory; a fresh DESC sweep would
   only yield duplicates until a new judgment is published.
3. SCZ is on a separate platform (judiciary.gov.zm via judiciaryzambia.com),
   schema-mixing hazard not yet retired — needs explicit approval for a
   bespoke ingestion path before the worker spends fetch budget there.

## What the worker is waiting on

(unchanged recommendation from b0376–b0403 — still pending Peter approval)

1. **parser_v0.3.2 vocabulary widening** — handle the 14 already-deferred
   `parser_v0.3.1_judges_no_comma_unhandled` candidates and likely a chunk of
   the 114 `html_no_summary_pdf_no_match` cases by widening the
   SUMMARY/PDF_TAIL pattern set. Highest yield-per-effort.
2. **OCR pipeline** — recover the 10 `pdf_extraction_empty_likely_scanned`
   candidates (scanned PDFs where pdfplumber returned no text). Independent
   of (1).
3. **ZMSC fresh-DESC-sweep approval** — once 78→100 record gap can no longer
   be closed by v0.3.2 reparse, fetch beyond the existing 25 ZMSC HTML stems.
   Only ~22 records away from the lower bound of the Phase 5 target.

## Side-loads

- **B2 sync:** `rclone` not in this sandbox; logged
  `B2 sync deferred to host (rclone not in sandbox)` and continued (per BRIEF
  step 8 fallback).
- **SQLite ingestion:** the `corpus.sqlite` FTS5 malformed-disk-image
  carry-forward from b0379 remains the canonical defer reason; record JSONs
  under `records/judgments/` remain the authoritative source until the host
  rebuild lands.

## Next tick

The next tick is scheduled to run in ~30 minutes. If `approvals.yaml` is still
unchanged at that point, expect another audit-only no-write idle tick
(b0405). The completion criterion will continue to be re-affirmed every tick
until Peter either flips `phase_5_judgments.complete: true` or approves one
of the three queued unblocks.
