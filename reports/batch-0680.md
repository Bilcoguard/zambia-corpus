# Phase 8 batch 0680 — Nightly re-verification

- **Tick:** b0680-phase8
- **Phase:** phase_8_nightly_reverify (approvals.yaml — approved: true, complete: false, sample_rate: 0.01)
- **Parser/fetcher version:** phase8-reverify-0.1.0
- **Script:** `scripts/batch_0680_phase8_reverify.py` (verbatim clone of frozen baseline `scripts/batch_0546_phase8_reverify.py`; only the `BATCH` constant changed; same logic as b0625/b0641/…/b0677/b0678/b0679)
- **Seed:** `phase8-reverify-2026-05-15-b0680`
- **Started:** 2026-05-15T17:04:29Z
- **Completed:** 2026-05-15T17:05:07Z
- **Wall clock:** ~38s (well within 20-minute budget)
- **Predecessor:** b0679-phase8 (committed e1cd58f, bundled b0678 HALT artefacts)
- **Verdict:** **tick-complete — 8/8 integrity PASS — COMMIT (normal path)**

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

Pool size 1928 unchanged from b0666…b0679. b0680 **did not** draw any of the 15 `parliament-pdf-v1.2` truncated-16hex defect records — CHECK #3 PASSES this tick on seed-luck alone (third consecutive lucky draw after b0676/b0677/b0679; b0678 was the most recent CHECK #3 trigger). The 15-record latent cohort remains an open operator-triage item.

## Results

| Verdict | Type | ID | Source host | URL kind | Notes |
|---|---|---|---|---|---|
| drift | act | act-zm-1960-059-land-survey-act-1960 | zambialii.org | AKN-HTML `eng@`-suffixed | dynamic-render cohort |
| drift | act | act-zm-1997-001-mineral-royalty-repeal-act-1997 | www.zambialii.org | AKN-HTML `eng@`-suffixed | dynamic-render cohort |
| drift | si  | si-zm-2022-046-customs-and-excise-machinery-and-equipment-suspension-amendment-regulations-2022 | zambialii.org | AKN-HTML (no `eng@` suffix) | dynamic-render cohort |
| drift | si  | si-zm-2019-077-chembe-town-council-sugar-cane-levy-by-laws-2019 | zambialii.org | AKN-HTML (no `eng@` suffix) | dynamic-render cohort |
| drift | act | act-zm-1994-035-parliamentary-and-ministerial-code-of-conduct-act | zambialii.org | AKN-HTML `eng@`-suffixed | dynamic-render cohort |
| match | judgment | judgment-zm-2025-zmsc-15-the-v-metro | zambialii.org | AKN `eng@/source.pdf` | stable-PDF supercohort match |
| match | si  | si-zm-2021-061-protection-of-traditional-knowledge-genetic-resources-and-expressions-of-folklor | zambialii.org | AKN `eng@/source.pdf` | stable-PDF supercohort match |
| match | act | act-zm-2024-019-zambia-institute-of-quantity-surveyors-act-2024 | www.parliament.gov.zm | parliament-PDF static | stable-PDF supercohort match |

All 5 drift verdicts are textbook `zambialii_akn_html_dynamic_render_drift` cohort — `zambialii.org/akn/zm/...` HTML landing pages (timestamp/footer-counter drift, legal content unchanged). Both the `eng@`-suffixed and bare AKN-HTML URL variants are represented; both nest in the established b0641..b0679 cohort. No new sub-cohort spawned.

All 3 match verdicts are stable-PDF supercohort: 2× `zambialii.org` AKN `/source.pdf` and 1× `www.parliament.gov.zm` static PDF. Consistent with the supercohort's near-100% match rate across the Phase 8 series.

## Integrity checks

| # | Check | Result |
|---|---|---|
| 1 | JSON report well-formed; match+drift+fetch_error == sample_size (3+5+0=8) | PASS |
| 2 | No duplicate IDs in sample (8 unique) | PASS |
| 3 | Every stored_sha256 + fetched_sha256 is a valid 64-hex sha256 | **PASS** — seed did not draw any of the 15 truncated-16hex records this tick |
| 4 | Every sampled record's stored_sha256 matches the on-disk record's `source_hash` | PASS (no record file mutated this tick) |
| 5 | No tracked record file modified by this run (script is read-only) | PASS |
| 6 | corpus.sqlite NOT touched; approvals.yaml NOT modified | PASS |
| 7 | robots.txt respected; per-host rate limits honoured (zambialii.org min_gap ≥ 5s; deterministic `sleep_for_host` mechanism unchanged from baseline) | PASS |
| 8 | User-Agent honest: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` | PASS |

All 8 checks PASS — commit proceeds per BRIEF step 7.

## Drift handling

Per BRIEF.md non-negotiable #4 ("never silently overwrite"), no record file was modified by this tick. The 5 AKN-HTML drifts are flagged in `gaps.md` for the existing `zambialii_akn_html_dynamic_render_drift` cohort (audit-only entries).

## Approvals

- `phase_8_nightly_reverify.approved` = true (unchanged)
- `phase_8_nightly_reverify.complete` = false (unchanged — Phase 8 is a continuous nightly cycle, not a one-shot)
- `approvals.yaml` was **not** modified by this tick

## Budget

- Today's fetches before tick: 160/2000 (after b0679 at 16:35:59Z)
- Today's fetches after tick: 168/2000
- Daily-budget headroom after tick: 1832
- LLM tokens: 0 (deterministic pipeline)

## Next

- Next Phase 8 tick (b0681) will continue the nightly sampling cycle (different seed → different 8 records).
- The 15-record `parliament-pdf-v1.2` truncated-hash defect remains an open operator-triage item; latent ~6% per-tick CHECK #3 hazard continues until resolved.
- Cumulative Phase 8 drift signal across b0641…b0680 continues to be dominated by the AKN-HTML dynamic-render cohort.
