# Phase 8 batch 0674 — Nightly re-verification

- **Tick:** b0674-phase8
- **Phase:** phase_8_nightly_reverify (approvals.yaml — approved: true, complete: false, sample_rate: 0.01)
- **Parser/fetcher version:** phase8-reverify-0.1.0
- **Script:** `scripts/batch_0674_phase8_reverify.py` (verbatim clone of frozen baseline `scripts/batch_0546_phase8_reverify.py`; only the `BATCH` constant + docstring batch identifier changed; same logic as b0625/b0641/b0652/b0653/b0655/b0660/b0662/b0663/b0665/b0666/b0668/b0669/b0670/b0671/b0672/b0673)
- **Seed:** `phase8-reverify-2026-05-15-b0674`
- **Started:** 2026-05-15T14:10:53Z
- **Completed:** 2026-05-15T14:11:28Z
- **Wall clock:** ~35s (well within 20-minute budget)
- **Predecessor:** b0673-phase8 (commit `1c72de9`, tick-complete, 2 match / 6 drift / 0 fetch_error). b0673 left an uncommitted-but-tracked worker.log trailer (FINAL/GIT_COMMIT/GIT_PUSH summary lines) due to FUSE-EPERM on `.git/index.lock`; this tick bundles that trailer into its own first commit, mirroring the b0667-repair/b0672 trailer-resolution pattern.

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

Pool size 1928 unchanged from b0666…b0673. b0674 did not draw any of the 8 b0667-repair-touched SI records, nor any of the 15 `parliament-pdf-v1.2` truncated-hash defect records.

## Results

| Verdict | Type | ID | Source host | URL kind |
|---|---|---|---|---|
| drift | statutory_instrument | si-zm-2014-024-animal-health-control-and-prevention-of-animal-disease-order-2014 | zambialii.org | AKN-HTML un-suffixed (dynamic-render cohort) |
| drift | act | act-zm-1952-005-victoria-memorial-institute-repeal-act-1952 | zambialii.org | AKN-HTML `eng@`-suffixed (dynamic-render cohort) |
| match | act | act-zm-2018-013 | parliament.gov.zm | parliament-PDF (stable-PDF supercohort match) |
| drift | statutory_instrument | si-zm-2014-059-agricultural-credits-appointment-of-authorised-agency-order-2014 | zambialii.org | AKN-HTML un-suffixed (dynamic-render cohort) |
| match | si | si-zm-1997-015-taxation-provisional-charging-order-1997 | zambialii.org | AKN `eng@/source.pdf` (stable-PDF supercohort match) |
| match | si | si-zm-2021-009-public-procurement-supplier-registration-and-renewal-fees-regulations-2021 | media.zambialii.org | media-PDF (stable-PDF supercohort match) |
| drift | statutory_instrument | si-zm-2017-077-national-markets-and-bus-stations-development-fund-regulations-2017 | zambialii.org | AKN-HTML un-suffixed (dynamic-render cohort) |
| drift | act | act-zm-1947-031-printed-publications-act-1947 | zambialii.org | AKN-HTML `eng@`-suffixed (dynamic-render cohort) |

All five drift verdicts are the well-known ZambiaLII AKN-HTML dynamic-render pattern (documented across b0641…b0673) — rendered timestamps and footer counters drift the response sha256 across re-fetches even though the legal content is unchanged. No first-observation or cross-cohort drift signatures this tick.

The three **match** verdicts span all three stable-PDF subcohorts: one `parliament.gov.zm` PDF (act-zm-2018-013, The Statistics Act 2018), one `zambialii.org` AKN `/source.pdf` (si-zm-1997-015), and one `media.zambialii.org` direct-PDF (si-zm-2021-009). Consistent with the stable-PDF supercohort's near-100% match rate across the Phase 8 series.

A 5/8 drift mix is well within the empirical Phase 8 distribution — the seeded random sampler can favour AKN-HTML over stable-PDF on any given draw. No alarm.

## Integrity checks

| # | Check | Result |
|---|---|---|
| 1 | JSON report well-formed; match+drift+fetch_error == sample_size (3+5+0=8) | PASS |
| 2 | No duplicate IDs in sample (8 unique) | PASS |
| 3 | Every stored_sha256 + fetched_sha256 is a valid 64-hex sha256 | PASS |
| 4 | Every sampled record's stored_sha256 matches the on-disk record's `source_hash` | PASS |
| 5 | No tracked record file modified by this run (script is read-only; 12 pre-existing untracked judgment files in working tree are from a separate judgment-ingest task and are NOT staged by this tick) | PASS |
| 6 | corpus.sqlite NOT touched; approvals.yaml NOT modified | PASS |
| 7 | robots.txt respected; per-host rate limits honoured (zambialii.org/www.zambialii.org/media.zambialii.org min_gap ≥ 5s; deterministic `sleep_for_host` mechanism unchanged from baseline) | PASS |
| 8 | User-Agent honest: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` | PASS |

CHECK#3 PASS — none of the 8 sampled records hit the 15-record `parliament-pdf-v1.2` truncated-16-hex stored-hash defect surfaced by the b0670 HALT. (Latent ≈ 6.1% per-tick hazard until Peter authorises remediation per `error-reports/2026-05-15T113700Z-b0670-check3-fail.md`.)

CHECK#5 NOTE — `git status` reports 12 pre-existing untracked files under `records/judgments/zmcc/2026/` and `records/judgments/zmsc/2024/` + `records/judgments/zmsc/2025/`. These are output from a separate (concurrent) judgment-ingest scheduled task and are **NOT** caused by this Phase 8 tick. The reverify script is strictly read-only on `records/`; no tracked record file was modified by this run. The untracked files are deliberately left unstaged by this tick (they belong to the other task's commit lineage).

## Drift handling

Per BRIEF.md non-negotiable #4 ("never silently overwrite"), drift on dynamically-rendered HTML pages is **flagged** in `gaps.md`, not auto-overwritten. The five drift records' `source_hash` on disk were NOT modified by this tick; the discrepancies are logged as audit signals only.

All five drifts are in the established `zambialii_akn_html_dynamic_render_drift` cohort. No first-observation or cross-cohort signals this tick.

## Approvals

- `phase_8_nightly_reverify.approved` = true (unchanged)
- `phase_8_nightly_reverify.complete` = false (unchanged — Phase 8 is a continuous nightly cycle, not a one-shot)
- `approvals.yaml` was **not** modified by this tick

## Budget

- Today's fetches before tick: 112/2000 (after b0673 at 14:07Z)
- Today's fetches after tick: 120/2000
- Daily-budget headroom after tick: 1880
- LLM tokens: 0 (deterministic pipeline)
- Bandwidth: ~2.36 MB down across 8 fetches (largest: `act-zm-cap-470-postal-services-act` size pattern not drawn this tick; largest this tick: `act-zm-2018-013` parliament-PDF ≈ ~? KB; AKN-HTML responses 25-100 KB each)

## Next

- Next Phase 8 tick will continue the nightly sampling cycle (different seed → different 8 records).
- The 15-record `parliament-pdf-v1.2` truncated-hash defect (b0670 discovery) remains a latent ~6% per-tick CHECK#3 hazard, pending Peter triage.
- The `zambialii_source_pdf_first_observation_drift` signal on `si-zm-2009-042` (b0671 discovery) also remains pending operator triage.
- Cumulative Phase 8 drift signal across b0641…b0674 continues to be dominated by the AKN-HTML dynamic-render cohort. Stable PDFs on `parliament.gov.zm`, `media.zambialii.org`, and zambialii.org AKN `/source.pdf` continue to dominate the match column.
