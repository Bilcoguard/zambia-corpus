# Batch 0549 — Phase 8 nightly re-verification (2026-05-09 UTC, third tick of day)

- **Phase:** `phase_8_nightly_reverify`
- **Tick number (Phase 8):** 7
- **UTC date:** 2026-05-09
- **Tick-of-day:** 3 (after b0546 at 05:59Z and b0548 at 06:13Z)
- **Started at:** 2026-05-09T06:34:32Z
- **Completed at:** 2026-05-09T06:35:01Z
- **Wall-clock duration:** ~30 s fetch loop + ~2 min total tick
- **Worker:** worker-tick (corpus integrity, Phase 8)
- **Parser/fetcher version:** `phase8-reverify-0.1.0`
- **Execution mode:** inline runner (per b0548 precedent — no derivative
  `scripts/batch_0549_phase8_reverify.py` committed this tick due to
  sandbox-session safety constraint)

## Sample selection

- Pool size: **1853** (records with both `source_url` and `source_hash`).
  Unchanged since b0548.
- Sample rate: **0.01** (1% from `approvals.yaml: phase_8_nightly_reverify`).
- Hard cap: **8** (`MAX_BATCH_SIZE`).
- Sample size: **8**.
- Seed: `phase8-reverify-2026-05-09-b0549` (deterministic; tick-suffixed
  because this is the third tick of the UTC date and the date-only seed
  had already been used by b0546). Re-running the script with the same
  seed produces the same sample.

## Verdict counts

| Verdict | Count |
|---------|------:|
| match | 4 |
| drift | 4 |
| fetch_error | 0 |
| truncated_stored_hash_false_drift | 0 |
| **total** | **8** |

## Drift entries (4) — all zambialii.org `/akn/...` HTML URLs

| Record id | URL | Sub-kind |
|-----------|-----|----------|
| `act-zm-1940-038-pharmacy-and-poisons-act-1940` | `https://zambialii.org/akn/zm/act/1940/38/eng@1996-12-31` | `content_changed_full_drift` |
| `act-zm-1965-008-provincial-and-district-boundaries-act-1965` | `https://zambialii.org/akn/zm/act/1965/8/eng@1996-12-31` | `content_changed_full_drift` |
| `act-zm-1995-004-value-added-tax-act-1995` | `https://zambialii.org/akn/zm/act/1995/4/eng@1996-12-31` | `content_changed_full_drift` |
| `act-zm-cap-268-employment-act` | `https://zambialii.org/akn/zm/act/1965/32/eng@1996-12-31` | `content_changed_full_drift` |

All four point at HTML rendering URLs (no `/source.pdf` suffix);
established `content_changed_full_drift` pattern reproduces.

## Match entries (4) — stable PDF endpoints

| Record id | URL | Endpoint kind |
|-----------|-----|---------------|
| `act-zm-2011-018-trades-licensing-repeal-act-2011` | parliament.gov.zm static PDF | static PDF |
| `act-zm-2018-011-the-constituency-development-fund-act-2018` | parliament.gov.zm static PDF | static PDF |
| `act-zm-2019-009-zambia-medicines-and-medical-supplies-agency-act-2` | parliament.gov.zm static PDF | static PDF |
| `si-zm-1997-015-taxation-provisional-charging-order-1997` | zambialii.org `/source.pdf` (redirects to `media.zambialii.org/.../source_file/`) | source_file PDF |

## Cross-tick statistics

- Cumulative `/akn/` HTML drifts across 7 Phase 8 ticks: **34/34** (100%).
- Cumulative stable PDF matches across 7 Phase 8 ticks: **21/21** (100%).
- Cumulative truncated-stored-hash findings: **1** (b0546 only;
  `act-zm-2020-023-vat-amendment`).
- Records re-encountered across ticks: 1 (`act-zm-cap-268-employment-act`),
  three distinct fetched hashes observed across the corpus' full Phase 8
  history — counter-example to the b0545 within-window stability
  observation. Reinforces "content-equivalence vs. byte-equality" as a
  future Phase 8 design refinement; not a record-data-quality issue.

## Records mutated

**None.** Phase 8 is read-only by design. `corpus.sqlite`,
`judges_registry.yaml`, `records/`, and `raw/` are all unchanged this
tick. `approvals.yaml` was NOT modified.

## Integrity check

PASS. No records mutated, so corpus duplicate-id, amended_by/repealed_by,
cited_authorities, and source_hash↔raw-file invariants are trivially
preserved. The 8 sampled record JSON files remain on disk unchanged.

## Daily fetch budget

24 + 8 = **32 / 2000** worker-tick fetches today. Well within budget.

## Provenance

- Detailed per-fetch report: `reports/batch-0549-reverify.json`
- This summary: `reports/batch-0549-report.md`
- Inline runner log appended to `provenance.log` and `costs.log`
- gaps.md entry: `## Phase 8 — Nightly re-verification, batch 0549 …`

## Recommendation for future ticks

The `/akn/` HTML drift pattern is now reproduced across 7 consecutive
Phase 8 ticks (34/34 = 100%). Treating each one as a fresh "drift" is
no longer informative. Recommend Peter consider one of:

1. Switch Phase 8 to **content-equivalence** (e.g. extract main `<article>`
   text and compare normalised SHA, or compare primary `<a href>` PDF
   target URL stability) for `/akn/` HTML records.
2. Restrict Phase 8 sampling to **stable PDF endpoints** (parliament.gov.zm
   plus zambialii `/source_file/` and `/source.pdf` URLs), excluding the
   `/akn/` HTML rendering surface. This keeps Phase 8 focused on detecting
   real corpus integrity issues vs. CMS rendering noise.
3. Add a per-record `phase8_skip: true` annotation on records whose
   `source_url` is a `/akn/` HTML rendering URL, with a backfill task to
   re-discover the canonical `/source.pdf` for each such record (a known
   subset already shows the `/akn/.../eng@DATE/source.pdf` form is
   reachable for at least the post-1996 acts; see e.g.
   `act-zm-1998-015` which is in the matching `/source.pdf` cohort).

These are recommendations only; **no `approvals.yaml` modification has
been made**, per the human-only-flips rule.
