# Phase 8 batch 0655 — Nightly re-verification

- **Tick:** b0655-phase8
- **Phase:** phase_8_nightly_reverify (approvals.yaml — approved: true, complete: false, sample_rate: 0.01)
- **Parser/fetcher version:** phase8-reverify-0.1.0
- **Script:** `scripts/batch_0655_phase8_reverify.py` (verbatim clone of frozen baseline `scripts/batch_0546_phase8_reverify.py`; only the `BATCH` constant + docstring batch identifier changed)
- **Seed:** `phase8-reverify-2026-05-15-b0655`
- **Started:** 2026-05-15T03:09:45Z
- **Completed:** 2026-05-15T03:10:07Z
- **Wall clock:** ~22s (well within 20-minute budget)

## Sample

| Metric | Value |
|---|---|
| pool_size | 1925 |
| sample_size | 8 |
| sample_rate | 0.01 |
| max_batch | 8 |
| fetches | 8 |
| match | 4 |
| drift | 4 |
| fetch_error | 0 |

## Results

| Verdict | Type | ID | Source host |
|---|---|---|---|
| match | act | act-zm-2022-002-the-zambia-institute-of-marketing-act-2022 | www.parliament.gov.zm |
| match | act | act-zm-2010-044-prohibition-and-prevention-of-money-laundering-amendment | www.parliament.gov.zm |
| drift | act | act-zm-1995-023-agricultural-credits-act-1995 | zambialii.org (AKN-HTML) |
| drift | act | act-zm-1973-040-national-anthem-act-1973 | www.zambialii.org (AKN-HTML) |
| drift | act | act-zm-1973-041-supreme-court-of-zambia-act | zambialii.org (AKN-HTML) |
| drift | si  | si-zm-2025-074-zambia-institute-of-secretaries-registration-regulations-2025 | zambialii.org (AKN-HTML) |
| match | act | act-zm-1986-022-zambia-agricultural-development-bank-dissolution-act-1986 | media.zambialii.org (source.pdf) |
| match | act | act-zm-2014-003-business-regulatory-act-2014-act-no-3-of-2014 | www.parliament.gov.zm |

All 4 drift verdicts are on ZambiaLII AKN-HTML pages (dynamic-content rendering — known pattern, e.g. footer counters / rendered timestamps). All 4 match verdicts are on static PDFs (parliament.gov.zm + media.zambialii.org source.pdf). This pattern matches prior Phase 8 batches (b0641, b0642, b0652, b0653).

## Integrity checks

| # | Check | Result |
|---|---|---|
| 1 | JSON report well-formed; match+drift+fetch_error == sample_size | PASS |
| 2 | No duplicate IDs in sample (8 unique) | PASS |
| 3 | Every stored_sha256 + fetched_sha256 is a valid 64-hex sha256 | PASS |
| 4 | Every sampled record's stored_sha256 matches the on-disk record's `source_hash` | PASS |
| 5 | No record file mutated by this run (all mtimes < started_at) | PASS |
| 6 | corpus.sqlite NOT touched; records/ NOT touched; approvals.yaml NOT modified | PASS |
| 7 | robots.txt respected; per-host rate limits honoured (zambialii=5s, parliament=2s) | PASS |
| 8 | User-Agent honest: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` | PASS |

## Drift handling

Per BRIEF.md non-negotiable #4 ("never silently overwrite"), drift on dynamically-rendered AKN-HTML pages is **flagged** in `gaps.md`, not auto-overwritten. A separate human-approved remediation tick would be required to re-snapshot. None of the drift records' `source_hash` values on disk were modified by this tick.

## Approvals

- `phase_8_nightly_reverify.approved` = true (unchanged)
- `phase_8_nightly_reverify.complete` = false (unchanged — Phase 8 is a continuous nightly cycle, not a one-shot)
- `approvals.yaml` was **not** modified by this tick

## Budget

- Today's fetches before tick: 0/2000
- Today's fetches after tick: 8/2000
- LLM tokens: 0 (deterministic pipeline)

## Next

- Next Phase 8 tick will continue the nightly sampling cycle (different seed → different 8 records).
