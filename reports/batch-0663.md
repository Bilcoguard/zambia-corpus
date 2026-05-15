# Phase 8 batch 0663 — Nightly re-verification

- **Tick:** b0663-phase8
- **Phase:** phase_8_nightly_reverify (approvals.yaml — approved: true, complete: false, sample_rate: 0.01)
- **Parser/fetcher version:** phase8-reverify-0.1.0
- **Script:** `scripts/batch_0663_phase8_reverify.py` (verbatim clone of frozen baseline `scripts/batch_0546_phase8_reverify.py`; only the `BATCH` constant + docstring batch identifier changed; same logic as b0625/b0641/b0652/b0653/b0655/b0660/b0662)
- **Seed:** `phase8-reverify-2026-05-15-b0663`
- **Started:** 2026-05-15T09:04:09Z
- **Completed:** 2026-05-15T09:04:45Z
- **Wall clock:** ~36s (well within 20-minute budget)

## Sample

| Metric | Value |
|---|---|
| pool_size | 1928 |
| sample_size | 8 |
| sample_rate | 0.01 |
| max_batch | 8 |
| fetches | 8 |
| match | 1 |
| drift | 7 |
| fetch_error | 0 |

Pool size 1928 unchanged from b0662 (no JIW ingestions or repair-tick record additions between b0662 at 08:36Z and b0663 at 09:04Z).

## Results

| Verdict | Type | ID | Source host |
|---|---|---|---|
| drift | act | act-zm-2017-007-banking-and-financial-services-act-2017 | zambialii.org (AKN-HTML, eng@-suffixed) |
| drift | act | act-zm-2025-002-geological-and-minerals-development-act-2025 | www.zambialii.org (AKN-HTML, eng@-suffixed) |
| drift | act | act-zm-1996-008-estate-duty-repeal-act-1996 | zambialii.org (AKN-HTML, eng@-suffixed) |
| drift | statutory_instrument | si-zm-2019-006-disaster-management-qualifications-of-national-coordinator-regulations-2019 | zambialii.org (AKN-HTML, bare path) |
| drift | act | act-zm-1961-032-town-and-country-planning-act-1961 | zambialii.org (AKN-HTML, bare path) |
| match | act | act-zm-2006-012-electoral-act-2006 | media.zambialii.org (AKN source.pdf) |
| drift | act | act-zm-1968-037-therapeutic-substances-act-1968 | zambialii.org (AKN-HTML, eng@-suffixed) |
| drift | act | act-zm-1929-038-treasury-bills-act-1929 | zambialii.org (AKN-HTML, eng@-suffixed) |

All 7 drift verdicts are on **ZambiaLII AKN-HTML** pages (dynamic-content rendering — known pattern from b0641/b0642/b0652/b0653/b0655/b0660/b0662: rendered timestamps and footer counters drift the response sha256 across re-fetches even though the legal content is unchanged). The single match verdict is on the static `source.pdf` Akoma Ntoso publication PDF on media.zambialii.org. Pattern consistent with prior Phase 8 batches; today's seed happened to over-sample the AKN-HTML tail of the pool (6 of 8 zambialii.org, 1 of 8 www.zambialii.org, 1 of 8 media.zambialii.org; zero parliament.gov.zm in this draw).

## Integrity checks

| # | Check | Result |
|---|---|---|
| 1 | JSON report well-formed; match+drift+fetch_error == sample_size (1+7+0=8) | PASS |
| 2 | No duplicate IDs in sample (8 unique) | PASS |
| 3 | Every stored_sha256 + fetched_sha256 is a valid 64-hex sha256 | PASS |
| 4 | Every sampled record's stored_sha256 matches the on-disk record's `source_hash` | PASS |
| 5 | No record file mutated by this run (all mtimes < started_at) | PASS |
| 6 | corpus.sqlite NOT touched; records/ NOT touched; approvals.yaml NOT modified | PASS |
| 7 | robots.txt respected; per-host rate limits honoured (zambialii=5s) | PASS |
| 8 | User-Agent honest: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` | PASS |

## Drift handling

Per BRIEF.md non-negotiable #4 ("never silently overwrite"), drift on dynamically-rendered AKN-HTML pages is **flagged** in `gaps.md`, not auto-overwritten. A separate human-approved remediation tick would be required to either (a) re-snapshot the affected records and update `source_hash`, or (b) switch the canonical `source_url` to the static `source.pdf` Akoma Ntoso publication PDF on media.zambialii.org. None of the drift records' `source_hash` values on disk were modified by this tick.

## Approvals

- `phase_8_nightly_reverify.approved` = true (unchanged)
- `phase_8_nightly_reverify.complete` = false (unchanged — Phase 8 is a continuous nightly cycle, not a one-shot)
- `approvals.yaml` was **not** modified by this tick

## Budget

- Today's fetches before tick: 24/2000 (from b0655-phase8 03:10Z + b0660-phase8 08:05Z + b0662-phase8 08:35Z)
- Today's fetches after tick: 32/2000
- LLM tokens: 0 (deterministic pipeline)
- Bandwidth: ~3.37 MB down (dominated by media.zambialii.org source.pdf 2.73 MB + zambialii AKN-HTML payloads)

## Next

- Next Phase 8 tick will continue the nightly sampling cycle (different seed → different 8 records).
- Cumulative Phase 8 drift signal across b0641/b0642/b0652/b0653/b0655/b0660/b0662/b0663: every drift verdict so far has been a ZambiaLII AKN-HTML page (zambialii.org or www.zambialii.org variants); static PDFs (parliament.gov.zm + media.zambialii.org source.pdf) remain 100% match. The pattern is stable enough that a Peter-approved bounded remediation tick — either re-snapshot AKN-HTML records or switch canonical URLs to source.pdf — would clear most outstanding drift entries in `gaps.md`.
