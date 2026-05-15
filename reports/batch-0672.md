# Phase 8 batch 0672 — Nightly re-verification

- **Tick:** b0672-phase8
- **Phase:** phase_8_nightly_reverify (approvals.yaml — approved: true, complete: false, sample_rate: 0.01)
- **Parser/fetcher version:** phase8-reverify-0.1.0
- **Script:** `scripts/batch_0672_phase8_reverify.py` (verbatim clone of frozen baseline `scripts/batch_0546_phase8_reverify.py`; only the `BATCH` constant + docstring batch identifier changed; same logic as b0625/b0641/b0652/b0653/b0655/b0660/b0662/b0663/b0665/b0666/b0668/b0669/b0670/b0671)
- **Seed:** `phase8-reverify-2026-05-15-b0672`
- **Started:** 2026-05-15T12:34:29Z
- **Completed:** 2026-05-15T12:35:07Z
- **Wall clock:** ~38s (well within 20-minute budget)
- **Predecessor:** b0671-phase8 (commit `133fc67`, tick-complete, 5 match / 3 drift / 0 fetch_error).

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

Pool size 1928 unchanged from b0666/b0668/b0669/b0670/b0671 (no record write/delete since b0669 commit `794363c`; the b0670 halt diagnostic and b0671 audit-trail commit added no records).

## Results

| Verdict | Type | ID | Source host | URL kind |
|---|---|---|---|---|
| drift | act | act-zm-1993-028-zambia-revenue-authority-act-1993 | zambialii.org | AKN-HTML `eng@`-suffixed (dynamic-render cohort) |
| drift | act | act-zm-cap-88-criminal-procedure-code | zambialii.org | AKN-HTML `eng@`-suffixed (dynamic-render cohort) |
| drift | act | act-zm-1993-029-supplementary-appropriation-1991-act | zambialii.org | AKN-HTML `eng@`-suffixed (dynamic-render cohort) |
| match | act | act-zm-1996-021-actions-for-smoke-damage-prohibition-repeal-1996 | zambialii.org | AKN `eng@/source.pdf` (stable-PDF supercohort match) |
| drift | act | act-zm-2023-029-appropriation-act | zambialii.org | AKN-HTML `eng@`-suffixed (dynamic-render cohort) |
| match | act | act-zm-2010-037-bretton-woods-agreements-ammendment | www.parliament.gov.zm | static PDF |
| match | act | act-zm-cap-250-cattle-slaughter-control-act | www.parliament.gov.zm | static PDF |
| drift | act | act-zm-2011-032-appropriation-act | zambialii.org | AKN-HTML `eng@`-suffixed (dynamic-render cohort) |

All five drift verdicts are the well-known ZambiaLII AKN-HTML `eng@`-suffixed dynamic-render pattern (documented across b0641/b0642/b0652/b0653/b0655/b0660/b0662/b0663/b0665/b0666/b0668/b0669/b0670/b0671) — rendered timestamps and footer counters drift the response sha256 across re-fetches even though the legal content is unchanged. No new drift signatures this tick.

The three **match** verdicts: two static PDFs on `www.parliament.gov.zm` (consistent with that host's near-100% match record across the Phase 8 series), and one zambialii AKN `/source.pdf` (stable-PDF supercohort). All three are routine confirmations of the canonical cohort classifications.

## Integrity checks

| # | Check | Result |
|---|---|---|
| 1 | JSON report well-formed; match+drift+fetch_error == sample_size (3+5+0=8) | PASS |
| 2 | No duplicate IDs in sample (8 unique) | PASS |
| 3 | Every stored_sha256 + fetched_sha256 (where present) is a valid 64-hex sha256 | PASS |
| 4 | Every sampled record's stored_sha256 matches the on-disk record's `source_hash` | PASS |
| 5 | No record file mutated by this run (script is read-only) | PASS |
| 6 | corpus.sqlite NOT touched; records/ NOT touched; approvals.yaml NOT modified | PASS |
| 7 | robots.txt respected; per-host rate limits honoured (zambialii.org min_gap ≥ 5s; www.parliament.gov.zm 2s default; deterministic `sleep_for_host` mechanism unchanged from baseline) | PASS |
| 8 | User-Agent honest: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` | PASS |

CHECK#3 PASS — none of the 8 sampled records hit the 15-record `parliament-pdf-v1.2` truncated-16-hex stored-hash defect surfaced by the b0670 HALT. (Probability of a future Phase 8 tick hitting at least one defective record on a random 8-of-1928 sample remains ≈ 6.1% until Peter authorises remediation per `error-reports/2026-05-15T113700Z-b0670-check3-fail.md`.)

## Drift handling

Per BRIEF.md non-negotiable #4 ("never silently overwrite"), drift on dynamically-rendered HTML pages is **flagged** in `gaps.md`, not auto-overwritten. The five drift records' `source_hash` on disk were NOT modified by this tick; the discrepancies are logged as audit signals only.

All five drifts are in the established `zambialii_akn_html_dynamic_render_drift` cohort. No first-observation or cross-cohort signals this tick.

## Approvals

- `phase_8_nightly_reverify.approved` = true (unchanged)
- `phase_8_nightly_reverify.complete` = false (unchanged — Phase 8 is a continuous nightly cycle, not a one-shot)
- `approvals.yaml` was **not** modified by this tick

## Budget

- Today's fetches before tick: 96/2000 (after b0671 at 12:11Z)
- Today's fetches after tick: 104/2000
- Daily-budget headroom after tick: 1896
- LLM tokens: 0 (deterministic pipeline)
- Bandwidth: ~1.85 MB down (largest: `act-zm-cap-88-criminal-procedure-code` ≈ 1.4 MB AKN-HTML render; smallest: `act-zm-2023-029` ≈ 13 KB)

## Next

- Next Phase 8 tick will continue the nightly sampling cycle (different seed → different 8 records).
- The 15-record `parliament-pdf-v1.2` truncated-hash defect remains a latent ~6% per-tick CHECK#3 hazard. The `zambialii_source_pdf_first_observation_drift` signal on `si-zm-2009-042` (b0671) also remains pending operator triage.
- Cumulative Phase 8 drift signal across b0641…b0672 continues to be dominated by the AKN-HTML dynamic-render cohort. Static PDFs on parliament.gov.zm, media.zambialii.org, and zambialii.org (no `www`) AKN `/source.pdf` continue to dominate the match column.
