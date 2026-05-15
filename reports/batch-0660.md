# Phase 8 batch 0660 — Nightly re-verification

- **Tick:** b0660-phase8
- **Phase:** phase_8_nightly_reverify (approvals.yaml — approved: true, complete: false, sample_rate: 0.01)
- **Parser/fetcher version:** phase8-reverify-0.1.0
- **Script:** `scripts/batch_0660_phase8_reverify.py` (verbatim clone of frozen baseline `scripts/batch_0546_phase8_reverify.py`; only the `BATCH` constant + docstring batch identifier changed; same logic as b0625/b0641/b0652/b0653/b0655)
- **Seed:** `phase8-reverify-2026-05-15-b0660`
- **Started:** 2026-05-15T08:04:41Z
- **Completed:** 2026-05-15T08:05:05Z
- **Wall clock:** ~24s (well within 20-minute budget)

## Sample

| Metric | Value |
|---|---|
| pool_size | 1928 |
| sample_size | 8 |
| sample_rate | 0.01 |
| max_batch | 8 |
| fetches | 8 |
| match | 4 |
| drift | 4 |
| fetch_error | 0 |

Pool grew from 1925 (b0655) → 1928 (b0660), reflecting +3 judgments ingested by the b0658-jiw worker between the two ticks.

## Results

| Verdict | Type | ID | Source host |
|---|---|---|---|
| match | act | act-zm-2016-016-protection-of-traditional-knowledgegenetic-resources-express | www.parliament.gov.zm |
| match | act | act-zm-2021-016-zambia-institute-of-advanced-legal-education-amendment-act-2021 | www.parliament.gov.zm |
| drift | judgment | judgment-zm-2022-zmsc-07-mpoha-and-anor-v-salvator | zambialii.org (AKN-HTML) |
| drift | si | si-zm-2018-039-levy-mwanawasa-medical-university-declaration-order-2018 | zambialii.org (AKN-HTML) |
| match | act | act-zm-2004-014-pharmaceutical-act-2004 | media.zambialii.org (source.pdf) |
| drift | act | act-zm-1962-047-human-tissue-act-1962 | zambialii.org (AKN-HTML) |
| drift | act | act-zm-2016-049-appropriation-act | zambialii.org (AKN-HTML) |
| match | act | act-zm-cap-175-printed-publications-act | www.parliament.gov.zm |

All 4 drift verdicts are on ZambiaLII AKN-HTML pages (dynamic-content rendering — known pattern, e.g. footer counters / rendered timestamps). All 4 match verdicts are on static PDFs (parliament.gov.zm + media.zambialii.org source.pdf). Pattern matches prior Phase 8 batches (b0641, b0642, b0652, b0653, b0655) — 50/50 match/drift split tracking the AKN-HTML vs. static-PDF source mix.

## Integrity checks

| # | Check | Result |
|---|---|---|
| 1 | JSON report well-formed; match+drift+fetch_error == sample_size (4+4+0=8) | PASS |
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

- Today's fetches before tick: 8/2000 (from b0655-phase8 at 03:10Z)
- Today's fetches after tick: 16/2000
- LLM tokens: 0 (deterministic pipeline)

## Next

- Next Phase 8 tick will continue the nightly sampling cycle (different seed → different 8 records).
