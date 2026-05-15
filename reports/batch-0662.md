# Phase 8 batch 0662 — Nightly re-verification

- **Tick:** b0662-phase8
- **Phase:** phase_8_nightly_reverify (approvals.yaml — approved: true, complete: false, sample_rate: 0.01)
- **Parser/fetcher version:** phase8-reverify-0.1.0
- **Script:** `scripts/batch_0662_phase8_reverify.py` (verbatim clone of frozen baseline `scripts/batch_0546_phase8_reverify.py`; only the `BATCH` constant + docstring batch identifier changed; same logic as b0625/b0641/b0652/b0653/b0655/b0660)
- **Seed:** `phase8-reverify-2026-05-15-b0662`
- **Started:** 2026-05-15T08:35:26Z
- **Completed:** 2026-05-15T08:36:01Z
- **Wall clock:** ~35s (well within 20-minute budget)

## Sample

| Metric | Value |
|---|---|
| pool_size | 1928 |
| sample_size | 8 |
| sample_rate | 0.01 |
| max_batch | 8 |
| fetches | 8 |
| match | 3 |
| drift | 5 |
| fetch_error | 0 |

Pool size 1928 unchanged from b0660 (no JIW ingestions between b0660 at 08:05Z and b0662 at 08:35Z; the b0661 repair tick reparsed 8 existing SI bodies but did not add new records).

## Results

| Verdict | Type | ID | Source host |
|---|---|---|---|
| drift | si | si-zm-2020-061-electoral-process-local-government-by-election-election-date-and-time-of-poll-no-5-order-2020 | zambialii.org (AKN-HTML, bare path) |
| drift | act | act-zm-1985-016-appropriation-act-1985 | zambialii.org (AKN-HTML, eng@-suffixed) |
| match | si | si-zm-2013-007-land-tribunal-fees-regulations-2013 | zambialii.org (AKN source.pdf) |
| drift | act | act-zm-2005-008-supplementary-appropriation-2003-act | zambialii.org (AKN-HTML, eng@-suffixed) |
| drift | act | act-zm-1961-015-bills-of-sale-registration-act-1961 | zambialii.org (AKN-HTML, eng@-suffixed) |
| match | act | act-zm-2021-010-the-petroleum-exploration-and-production-amendment-act-2021 | www.parliament.gov.zm |
| drift | si | si-zm-2020-043-electoral-process-local-government-by-election-election-date-and-time-of-poll-no-4-order-2020 | zambialii.org (AKN-HTML, bare path) |
| match | act | act-zm-2021-009-the-national-institute-of-public-administration-amendment-act-2021 | www.parliament.gov.zm |

All 5 drift verdicts are on **ZambiaLII AKN-HTML** pages (dynamic-content rendering — known pattern from b0641/b0642/b0652/b0653/b0655/b0660: rendered timestamps and footer counters drift the response sha256 across re-fetches even though the legal content is unchanged). All 3 match verdicts are on static PDFs (parliament.gov.zm + zambialii AKN source.pdf). Pattern consistent with prior Phase 8 batches.

## Integrity checks

| # | Check | Result |
|---|---|---|
| 1 | JSON report well-formed; match+drift+fetch_error == sample_size (3+5+0=8) | PASS |
| 2 | No duplicate IDs in sample (8 unique) | PASS |
| 3 | Every stored_sha256 + fetched_sha256 is a valid 64-hex sha256 | PASS |
| 4 | Every sampled record's stored_sha256 matches the on-disk record's `source_hash` | PASS |
| 5 | No record file mutated by this run (all mtimes < started_at) | PASS |
| 6 | corpus.sqlite NOT touched; records/ NOT touched; approvals.yaml NOT modified | PASS |
| 7 | robots.txt respected; per-host rate limits honoured (zambialii=5s, parliament=2s) | PASS |
| 8 | User-Agent honest: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` | PASS |

## Drift handling

Per BRIEF.md non-negotiable #4 ("never silently overwrite"), drift on dynamically-rendered AKN-HTML pages is **flagged** in `gaps.md`, not auto-overwritten. A separate human-approved remediation tick would be required to either (a) re-snapshot the affected records and update `source_hash`, or (b) switch the canonical `source_url` to the static `source.pdf` Akoma Ntoso publication PDF on media.zambialii.org. None of the drift records' `source_hash` values on disk were modified by this tick.

## Approvals

- `phase_8_nightly_reverify.approved` = true (unchanged)
- `phase_8_nightly_reverify.complete` = false (unchanged — Phase 8 is a continuous nightly cycle, not a one-shot)
- `approvals.yaml` was **not** modified by this tick

## Budget

- Today's fetches before tick: 16/2000 (from b0655-phase8 03:10Z + b0660-phase8 08:05Z)
- Today's fetches after tick: 24/2000
- LLM tokens: 0 (deterministic pipeline)

## Next

- Next Phase 8 tick will continue the nightly sampling cycle (different seed → different 8 records).
- Cumulative Phase 8 drift signal across b0641/b0642/b0652/b0653/b0655/b0660/b0662: every drift verdict so far has been a ZambiaLII AKN-HTML page; static PDFs (parliament.gov.zm + media.zambialii.org source.pdf) remain 100% match. The pattern is stable enough that a Peter-approved bounded remediation tick — either re-snapshot AKN-HTML records or switch canonical URLs to source.pdf — would clear most outstanding drift entries in `gaps.md`.
