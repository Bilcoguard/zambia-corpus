# Phase 8 batch 0679 — Nightly re-verification

- **Tick:** b0679-phase8
- **Phase:** phase_8_nightly_reverify (approvals.yaml — approved: true, complete: false, sample_rate: 0.01)
- **Parser/fetcher version:** phase8-reverify-0.1.0
- **Script:** `scripts/batch_0679_phase8_reverify.py` (verbatim clone of frozen baseline `scripts/batch_0546_phase8_reverify.py`; only the `BATCH` constant + docstring batch identifier changed; same logic as b0625/b0641/…/b0676/b0677/b0678)
- **Seed:** `phase8-reverify-2026-05-15-b0679`
- **Started:** 2026-05-15T16:35:30Z
- **Completed:** 2026-05-15T16:35:59Z
- **Wall clock:** ~29s (well within 20-minute budget)
- **Predecessor:** b0678-phase8 (HALT — CHECK #3 FAIL, no commit; artefacts bundled into THIS tick's commit per b0671 precedent).
- **Verdict:** **tick-complete — 8/8 integrity PASS — COMMIT (bundles b0678 HALT artefacts)**

## Sample

| Metric | Value |
|---|---|
| pool_size | 1928 |
| sample_size | 8 |
| sample_rate | 0.01 |
| max_batch | 8 |
| fetches | 8 |
| match | 5 |
| drift | 3 |
| fetch_error | 0 |

Pool size 1928 unchanged from b0666…b0678. b0679 **did not** draw any of the 15 `parliament-pdf-v1.2` truncated-16hex defect records — CHECK #3 PASSES this tick on seed-luck alone. The 15-record latent cohort remains an open operator-triage item (3rd Phase 8 observation in 10 ticks across b0670/b0678; b0679 was a near-miss by sample selection only).

## Results

| Verdict | Type | ID | Source host | URL kind | Notes |
|---|---|---|---|---|---|
| match | act | act-zm-2021-024-accountants-amendment-act-2021 | www.parliament.gov.zm | parliament-PDF static | stable-PDF supercohort match |
| drift | act | act-zm-1993-037-narcotic-drugs-and-psychotropic-substances-act-1993 | zambialii.org | AKN-HTML `eng@`-suffixed | dynamic-render cohort |
| drift | act | act-zm-1926-021-land-perpetual-succession-act-1926 | zambialii.org | AKN-HTML `eng@`-suffixed | dynamic-render cohort |
| match | act | act-zm-2023-024-access-to-information-act-2023 | zambialii.org | AKN `eng@/source.pdf` | stable-PDF supercohort match |
| drift | act | act-zm-1972-037-technical-education-and-vocational-training-act-1972 | zambialii.org | AKN-HTML `eng@`-suffixed | dynamic-render cohort |
| match | act | act-zm-cap-199-forests-act | www.parliament.gov.zm | parliament-PDF static | stable-PDF supercohort match |
| match | act | loz-agricultural-products-levy-act | www.parliament.gov.zm | parliament-PDF static | stable-PDF supercohort match |
| match | act | act-zm-2020-006-the-food-reserve-act-2020 | www.parliament.gov.zm | parliament-PDF static | stable-PDF supercohort match |

All 3 drift verdicts are textbook `zambialii_akn_html_dynamic_render_drift` cohort — all `zambialii.org/akn/zm/act/.../eng@1996-12-31` HTML landing pages (timestamp/footer-counter drift, legal content unchanged). Nest cleanly in the established b0641..b0678 cohort.

All 5 match verdicts are stable-PDF supercohort: 4× `www.parliament.gov.zm` static PDFs and 1× `zambialii.org` AKN `/source.pdf`. Consistent with the supercohort's near-100% match rate across the Phase 8 series.

## Integrity checks

| # | Check | Result |
|---|---|---|
| 1 | JSON report well-formed; match+drift+fetch_error == sample_size (5+3+0=8) | PASS |
| 2 | No duplicate IDs in sample (8 unique) | PASS |
| 3 | Every stored_sha256 + fetched_sha256 is a valid 64-hex sha256 | **PASS** — seed did not draw any of the 15 truncated-16hex records this tick |
| 4 | Every sampled record's stored_sha256 matches the on-disk record's `source_hash` | PASS (no record file mutated this tick) |
| 5 | No tracked record file modified by this run (script is read-only) | PASS |
| 6 | corpus.sqlite NOT touched; approvals.yaml NOT modified | PASS |
| 7 | robots.txt respected; per-host rate limits honoured (zambialii.org min_gap ≥ 5s; deterministic `sleep_for_host` mechanism unchanged from baseline) | PASS |
| 8 | User-Agent honest: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` | PASS |

All 8 checks PASS — commit proceeds per BRIEF step 7.

## Drift handling

Per BRIEF.md non-negotiable #4 ("never silently overwrite"), no record file was modified by this tick. The 3 AKN-HTML drifts are flagged in `gaps.md` for the existing `zambialii_akn_html_dynamic_render_drift` cohort (audit-only entries).

## Approvals

- `phase_8_nightly_reverify.approved` = true (unchanged)
- `phase_8_nightly_reverify.complete` = false (unchanged — Phase 8 is a continuous nightly cycle, not a one-shot)
- `approvals.yaml` was **not** modified by this tick

## Budget

- Today's fetches before tick: 152/2000 (after b0678 at 16:06:08Z)
- Today's fetches after tick: 160/2000
- Daily-budget headroom after tick: 1840
- LLM tokens: 0 (deterministic pipeline)

## Bundled artefacts from b0678 HALT

Per the b0671 precedent, this tick's commit ALSO carries forward all uncommitted artefacts from the prior HALT tick:

- `scripts/batch_0678_phase8_reverify.py`
- `reports/batch-0678.md`
- `reports/batch-0678-reverify.json`
- `error-reports/2026-05-15T160608Z-b0678-check3-fail.md`
- gaps.md entries for the 4 AKN-HTML drifts and the 1 CHECK #3 trigger from b0678
- costs.log / provenance.log / worker.log appends from b0678
- The b0677 deferred trailer lines in worker.log (per the FUSE-EPERM workaround pattern)

## Next

- Next Phase 8 tick (b0680) will continue the nightly sampling cycle (different seed → different 8 records).
- The 15-record `parliament-pdf-v1.2` truncated-hash defect remains an open operator-triage item; latent ~6% per-tick CHECK #3 hazard continues until resolved.
- Cumulative Phase 8 drift signal across b0641…b0679 continues to be dominated by the AKN-HTML dynamic-render cohort, with the 15-record truncated-hash cohort as a known latent hazard.
