# Phase 8 batch 0677 — Nightly re-verification

- **Tick:** b0677-phase8
- **Phase:** phase_8_nightly_reverify (approvals.yaml — approved: true, complete: false, sample_rate: 0.01)
- **Parser/fetcher version:** phase8-reverify-0.1.0
- **Script:** `scripts/batch_0677_phase8_reverify.py` (verbatim clone of frozen baseline `scripts/batch_0546_phase8_reverify.py`; only the `BATCH` constant + docstring batch identifier changed; same logic as b0625/b0641/b0652/b0653/b0655/b0660/b0662/b0663/b0665/b0666/b0668/b0669/b0670/b0671/b0672/b0673/b0674/b0675/b0676)
- **Seed:** `phase8-reverify-2026-05-15-b0677`
- **Started:** 2026-05-15T15:34:25Z
- **Completed:** 2026-05-15T15:34:59Z
- **Wall clock:** ~34s (well within 20-minute budget)
- **Predecessor:** b0676-phase8 (commit `585ec2e`, tick-complete, 4 match / 4 drift / 0 fetch_error).

## Sample

| Metric | Value |
|---|---|
| pool_size | 1928 |
| sample_size | 8 |
| sample_rate | 0.01 |
| max_batch | 8 |
| fetches | 8 |
| match | 2 |
| drift | 6 |
| fetch_error | 0 |

Pool size 1928 unchanged from b0666…b0676. b0677 did not draw any of the 15 `parliament-pdf-v1.2` truncated-hash defect records (CHECK#3 hazard not triggered).

## Results

| Verdict | Type | ID | Source host | URL kind |
|---|---|---|---|---|
| drift | act | act-zm-1974-002-gaming-machines-prohibition-act-1974 | zambialii.org | AKN-HTML `eng@`-suffixed (dynamic-render cohort) |
| drift | act | act-zm-1922-007-mashona-railway-company-limited-act-1922 | zambialii.org | AKN-HTML `eng@`-suffixed (dynamic-render cohort) |
| drift | act | act-zm-1959-028-cattle-slaughter-control-act-1959 | zambialii.org | AKN-HTML `eng@`-suffixed (dynamic-render cohort) |
| match | act | act-zm-2017-003-compulsory-standards | www.parliament.gov.zm | parliament-PDF (stable-PDF supercohort match) |
| drift | act | act-zm-1958-004-minister-of-finance-incorporation-act-1958 | www.zambialii.org | AKN-HTML `eng@`-suffixed (dynamic-render cohort) |
| match | statutory_instrument | si-zm-2021-093-minimum-wages-and-conditions-of-employment-truck-and-bus-drivers-amendment-order | zambialii.org | AKN `eng@/source.pdf` (stable-PDF supercohort match) |
| drift | act | act-zm-2007-010-biosafety-act-2007 | zambialii.org | AKN-HTML `eng@`-suffixed (dynamic-render cohort) |
| drift | act | act-zm-1964-051-general-loans-guarantee-act-1964 | zambialii.org | AKN-HTML `eng@`-suffixed (dynamic-render cohort) |

All six drift verdicts are the well-known ZambiaLII AKN-HTML dynamic-render pattern (documented across b0641…b0676) — rendered timestamps and footer counters drift the response sha256 across re-fetches even though the legal content is unchanged. No new sub-cohort spawned; all six nest cleanly in the existing `zambialii_akn_html_dynamic_render_drift` cohort.

The two **match** verdicts are exactly the stable-PDF supercohort signature: one `www.parliament.gov.zm` static PDF (`act-zm-2017-003-compulsory-standards`) and one `zambialii.org` AKN `/source.pdf` (`si-zm-2021-093`). Consistent with the supercohort's near-100% match rate across the Phase 8 series.

A 2/8 match : 6/8 drift mix is on the heavier-drift end of the recent window (b0672–b0676 averaged ~3.4 match / 4.6 drift), driven by this seed drawing six AKN-HTML records vs only two stable-PDFs. No regression — the per-record verdict logic is unchanged from baseline.

## Integrity checks

| # | Check | Result |
|---|---|---|
| 1 | JSON report well-formed; match+drift+fetch_error == sample_size (2+6+0=8) | PASS |
| 2 | No duplicate IDs in sample (8 unique) | PASS |
| 3 | Every stored_sha256 + fetched_sha256 is a valid 64-hex sha256 | PASS |
| 4 | Every sampled record's stored_sha256 matches the on-disk record's `source_hash` | PASS |
| 5 | No tracked record file modified by this run (script is read-only) | PASS |
| 6 | corpus.sqlite NOT touched; approvals.yaml NOT modified | PASS |
| 7 | robots.txt respected; per-host rate limits honoured (zambialii.org min_gap ≥ 5s; deterministic `sleep_for_host` mechanism unchanged from baseline) | PASS |
| 8 | User-Agent honest: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` | PASS |

CHECK#3 PASS — none of the 8 sampled records hit the 15-record `parliament-pdf-v1.2` truncated-16-hex stored-hash defect surfaced by the b0670 HALT. (Latent ≈ 6.1% per-tick hazard until Peter authorises remediation per `error-reports/2026-05-15T113700Z-b0670-check3-fail.md`.)

## Drift handling

Per BRIEF.md non-negotiable #4 ("never silently overwrite"), drift on dynamically-rendered HTML pages is **flagged** in `gaps.md`, not auto-overwritten. The six drift records' `source_hash` on disk were NOT modified by this tick; the discrepancies are logged as audit signals only.

All six drifts are in the established `zambialii_akn_html_dynamic_render_drift` cohort.

## Approvals

- `phase_8_nightly_reverify.approved` = true (unchanged)
- `phase_8_nightly_reverify.complete` = false (unchanged — Phase 8 is a continuous nightly cycle, not a one-shot)
- `approvals.yaml` was **not** modified by this tick

## Budget

- Today's fetches before tick: 136/2000 (after b0676 at 15:05:07Z)
- Today's fetches after tick: 144/2000
- Daily-budget headroom after tick: 1856
- LLM tokens: 0 (deterministic pipeline)
- Bandwidth: see costs.log BANDWIDTH line for this batch.

## Next

- Next Phase 8 tick will continue the nightly sampling cycle (different seed → different 8 records).
- The 15-record `parliament-pdf-v1.2` truncated-hash defect (b0670 discovery) remains a latent ~6% per-tick CHECK#3 hazard, pending Peter triage.
- The `zambialii_source_pdf_first_observation_drift` signal on `si-zm-2009-042` (b0671 discovery) also remains pending operator triage.
- Cumulative Phase 8 drift signal across b0641…b0677 continues to be dominated by the AKN-HTML dynamic-render cohort. Stable PDFs on `parliament.gov.zm`, `media.zambialii.org`, and zambialii.org AKN `/source.pdf` continue to dominate the match column.
