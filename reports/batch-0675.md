# Phase 8 batch 0675 — Nightly re-verification

- **Tick:** b0675-phase8
- **Phase:** phase_8_nightly_reverify (approvals.yaml — approved: true, complete: false, sample_rate: 0.01)
- **Parser/fetcher version:** phase8-reverify-0.1.0
- **Script:** `scripts/batch_0675_phase8_reverify.py` (verbatim clone of frozen baseline `scripts/batch_0546_phase8_reverify.py`; only the `BATCH` constant + docstring batch identifier changed; same logic as b0625/b0641/b0652/b0653/b0655/b0660/b0662/b0663/b0665/b0666/b0668/b0669/b0670/b0671/b0672/b0673/b0674)
- **Seed:** `phase8-reverify-2026-05-15-b0675`
- **Started:** 2026-05-15T14:34:41Z
- **Completed:** 2026-05-15T14:35:22Z
- **Wall clock:** ~41s (well within 20-minute budget)
- **Predecessor:** b0674-phase8 (commit `1016fe5`, tick-complete, 3 match / 5 drift / 0 fetch_error).

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

Pool size 1928 unchanged from b0666…b0674. b0675 did not draw any of the 15 `parliament-pdf-v1.2` truncated-hash defect records (CHECK#3 hazard not triggered).

## Results

| Verdict | Type | ID | Source host | URL kind |
|---|---|---|---|---|
| match | act | act-zm-2017-002-agricultural-institute-of-zambia-act-2017 | zambialii.org | AKN `eng@/source.pdf` (stable-PDF supercohort match) |
| match | si | si-zm-2008-015-taxation-provisional-charging-order-2008 | zambialii.org | AKN `eng@/source.pdf` (stable-PDF supercohort match) |
| drift | act | act-zm-1967-001-suicide-act-1967 | zambialii.org | AKN-HTML `eng@`-suffixed (dynamic-render cohort) |
| drift | statutory_instrument | si-zm-2018-043-urban-and-regional-planning-designated-local-planning-authorities-regulations-2018 | zambialii.org | AKN-HTML un-suffixed (dynamic-render cohort) |
| match | act | act-zm-2012-001-the-penal-code-amendment-2012 | www.parliament.gov.zm | parliament-PDF (stable-PDF supercohort match) |
| drift | act | act-zm-2015-023-appropriation-act | zambialii.org | AKN-HTML `eng@`-suffixed (dynamic-render cohort) |
| drift | judgment | judgment-zm-2025-zmsc-06-zambia-telecommunication-company-v-felix-musonda-a | zambialii.org | AKN-HTML `eng@`-suffixed (dynamic-render cohort) |
| drift | statutory_instrument | si-zm-2020-018-compulsory-standards-potable-spirits-declaration-order-2020 | zambialii.org | AKN-HTML un-suffixed (dynamic-render cohort) |

All five drift verdicts are the well-known ZambiaLII AKN-HTML dynamic-render pattern (documented across b0641…b0674) — rendered timestamps and footer counters drift the response sha256 across re-fetches even though the legal content is unchanged. The judgment-type drift on `judgment-zm-2025-zmsc-06-zambia-telecommunication-company-v-felix-musonda-a` is the second-this-week judgment-type AKN-HTML drift (after `judgment-zm-2022-zmsc-29` in b0673) — both nest cleanly in the existing cohort.

The three **match** verdicts span all three stable-PDF subcohort hosts represented this tick: two `zambialii.org` AKN `/source.pdf` (act-zm-2017-002, si-zm-2008-015) and one `www.parliament.gov.zm` PDF (act-zm-2012-001, The Penal Code (Amendment) Act 2012). Consistent with the stable-PDF supercohort's near-100% match rate across the Phase 8 series.

A 5/8 drift mix matches b0674 (3 match / 5 drift) exactly and is well within the empirical Phase 8 distribution.

## Integrity checks

| # | Check | Result |
|---|---|---|
| 1 | JSON report well-formed; match+drift+fetch_error == sample_size (3+5+0=8) | PASS |
| 2 | No duplicate IDs in sample (8 unique) | PASS |
| 3 | Every stored_sha256 + fetched_sha256 is a valid 64-hex sha256 | PASS |
| 4 | Every sampled record's stored_sha256 matches the on-disk record's `source_hash` | PASS |
| 5 | No tracked record file modified by this run (script is read-only) | PASS |
| 6 | corpus.sqlite NOT touched; approvals.yaml NOT modified | PASS |
| 7 | robots.txt respected; per-host rate limits honoured (zambialii.org min_gap ≥ 5s; deterministic `sleep_for_host` mechanism unchanged from baseline) | PASS |
| 8 | User-Agent honest: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` | PASS |

CHECK#3 PASS — none of the 8 sampled records hit the 15-record `parliament-pdf-v1.2` truncated-16-hex stored-hash defect surfaced by the b0670 HALT. (Latent ≈ 6.1% per-tick hazard until Peter authorises remediation per `error-reports/2026-05-15T113700Z-b0670-check3-fail.md`.)

## Drift handling

Per BRIEF.md non-negotiable #4 ("never silently overwrite"), drift on dynamically-rendered HTML pages is **flagged** in `gaps.md`, not auto-overwritten. The five drift records' `source_hash` on disk were NOT modified by this tick; the discrepancies are logged as audit signals only.

All five drifts are in the established `zambialii_akn_html_dynamic_render_drift` cohort. The judgment-type drift `judgment-zm-2025-zmsc-06-zambia-telecommunication-company-v-felix-musonda-a` is the second-this-week judgment-type AKN-HTML drift — nests cleanly in the existing cohort (no new sub-cohort spawned).

## Approvals

- `phase_8_nightly_reverify.approved` = true (unchanged)
- `phase_8_nightly_reverify.complete` = false (unchanged — Phase 8 is a continuous nightly cycle, not a one-shot)
- `approvals.yaml` was **not** modified by this tick

## Budget

- Today's fetches before tick: 120/2000 (after b0674 at 14:14:58Z)
- Today's fetches after tick: 128/2000
- Daily-budget headroom after tick: 1872
- LLM tokens: 0 (deterministic pipeline)
- Bandwidth: ~448 KB down across 8 fetches (largest: `si-zm-2008-015-taxation-provisional-charging-order-2008` AKN /source.pdf at 120,149 B; AKN-HTML responses 25–110 KB each)

## Next

- Next Phase 8 tick will continue the nightly sampling cycle (different seed → different 8 records).
- The 15-record `parliament-pdf-v1.2` truncated-hash defect (b0670 discovery) remains a latent ~6% per-tick CHECK#3 hazard, pending Peter triage.
- The `zambialii_source_pdf_first_observation_drift` signal on `si-zm-2009-042` (b0671 discovery) also remains pending operator triage.
- Cumulative Phase 8 drift signal across b0641…b0675 continues to be dominated by the AKN-HTML dynamic-render cohort. Stable PDFs on `parliament.gov.zm`, `media.zambialii.org`, and zambialii.org AKN `/source.pdf` continue to dominate the match column.
