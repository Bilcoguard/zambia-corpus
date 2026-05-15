# Phase 8 batch 0673 — Nightly re-verification

- **Tick:** b0673-phase8
- **Phase:** phase_8_nightly_reverify (approvals.yaml — approved: true, complete: false, sample_rate: 0.01)
- **Parser/fetcher version:** phase8-reverify-0.1.0
- **Script:** `scripts/batch_0673_phase8_reverify.py` (verbatim clone of frozen baseline `scripts/batch_0546_phase8_reverify.py`; only the `BATCH` constant + docstring batch identifier changed; same logic as b0625/b0641/b0652/b0653/b0655/b0660/b0662/b0663/b0665/b0666/b0668/b0669/b0670/b0671/b0672)
- **Seed:** `phase8-reverify-2026-05-15-b0673`
- **Started:** 2026-05-15T14:01:15Z
- **Completed:** 2026-05-15T14:01:56Z
- **Wall clock:** ~41s (well within 20-minute budget)
- **Predecessor:** b0672-phase8 (commit `cb81981`, tick-complete, 3 match / 5 drift / 0 fetch_error). Note: an out-of-band repair commit `0a4b710` ("Repair batch b0667: fixed 8 SI records (zambialii 2020 cohort drainage)") landed on `origin/main` between b0672 and b0673; the b0673 tick pulled it cleanly via `git pull --ff-only`. Phase 8 is read-only and was not affected by the records repair.

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

Pool size 1928 unchanged from b0666/b0668/b0669/b0670/b0671/b0672 (the b0667 repair commit `0a4b710` rewrote in-place 8 existing SI records — it did not add or remove records, so the Phase 8 pool count is unchanged; b0673 did not draw any of those 8 repaired records in this tick's sample).

## Results

| Verdict | Type | ID | Source host | URL kind |
|---|---|---|---|---|
| drift | judgment | judgment-zm-2022-zmsc-29-mutale-v-african-banking-corporation-ltd | zambialii.org | AKN-HTML `eng@`-suffixed (dynamic-render cohort) |
| drift | statutory_instrument | si-zm-2022-006-zambia-police-fees-regulations-2022 | zambialii.org | AKN-HTML un-suffixed (dynamic-render cohort) |
| drift | act | act-zm-1912-016-gold-trade-act-1912 | zambialii.org | AKN-HTML `eng@`-suffixed (dynamic-render cohort) |
| drift | act | act-zm-cap-470-postal-services-act | zambialii.org | AKN-HTML `eng@`-suffixed (dynamic-render cohort) |
| drift | act | act-zm-1989-019-national-agricultural-marketing-act-1989 | www.zambialii.org | AKN-HTML `eng@`-suffixed (dynamic-render cohort, `www.` subdomain) |
| drift | statutory_instrument | si-zm-2019-076-electoral-process-local-government-by-elections-election-date-and-time-of-poll-no-5-order-2019 | zambialii.org | AKN-HTML un-suffixed (dynamic-render cohort) |
| match | si | si-zm-2009-049-national-heritage-conservation-commission-national-monument-mulobezi-open-air-ra | zambialii.org | AKN `eng@/source.pdf` (stable-PDF supercohort match) |
| match | si | si-zm-2019-005-customs-and-excise-nickel-and-particle-board-export-duty-remission-regulations-2019 | zambialii.org | AKN `eng@/source.pdf` (stable-PDF supercohort match) |

All six drift verdicts are the well-known ZambiaLII AKN-HTML dynamic-render pattern (documented across b0641/b0642/b0652/b0653/b0655/b0660/b0662/b0663/b0665/b0666/b0668/b0669/b0670/b0671/b0672) — rendered timestamps and footer counters drift the response sha256 across re-fetches even though the legal content is unchanged. No first-observation or cross-cohort drift signatures this tick. Notable distribution: this is the first b06xx tick this week to draw a judgment-type AKN-HTML drift (judgment-zm-2022-zmsc-29) and the first to draw a `www.`-subdomain AKN-HTML drift (act-zm-1989-019) — both nest cleanly within the existing dynamic-render cohort.

The two **match** verdicts are both zambialii AKN `/source.pdf` records on `zambialii.org` (no `www.`). Consistent with the stable-PDF supercohort's near-100% match rate across the Phase 8 series.

A high-drift tick (6/8) is within the empirical Phase 8 distribution — the seeded random sampler can favour AKN-HTML over stable-PDF on any given draw. No alarm.

## Integrity checks

| # | Check | Result |
|---|---|---|
| 1 | JSON report well-formed; match+drift+fetch_error == sample_size (2+6+0=8) | PASS |
| 2 | No duplicate IDs in sample (8 unique) | PASS |
| 3 | Every stored_sha256 + fetched_sha256 (where present) is a valid 64-hex sha256 | PASS |
| 4 | Every sampled record's stored_sha256 matches the on-disk record's `source_hash` | PASS |
| 5 | No record file mutated by this run (script is read-only) | PASS |
| 6 | corpus.sqlite NOT touched; records/ NOT touched; approvals.yaml NOT modified | PASS |
| 7 | robots.txt respected; per-host rate limits honoured (zambialii.org/www.zambialii.org min_gap ≥ 5s; deterministic `sleep_for_host` mechanism unchanged from baseline) | PASS |
| 8 | User-Agent honest: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` | PASS |

CHECK#3 PASS — none of the 8 sampled records hit the 15-record `parliament-pdf-v1.2` truncated-16-hex stored-hash defect surfaced by the b0670 HALT. (Latent ≈ 6.1% per-tick hazard until Peter authorises remediation per `error-reports/2026-05-15T113700Z-b0670-check3-fail.md`.)

## Drift handling

Per BRIEF.md non-negotiable #4 ("never silently overwrite"), drift on dynamically-rendered HTML pages is **flagged** in `gaps.md`, not auto-overwritten. The six drift records' `source_hash` on disk were NOT modified by this tick; the discrepancies are logged as audit signals only.

All six drifts are in the established `zambialii_akn_html_dynamic_render_drift` cohort. No first-observation or cross-cohort signals this tick.

## Approvals

- `phase_8_nightly_reverify.approved` = true (unchanged)
- `phase_8_nightly_reverify.complete` = false (unchanged — Phase 8 is a continuous nightly cycle, not a one-shot)
- `approvals.yaml` was **not** modified by this tick

## Budget

- Today's fetches before tick: 104/2000 (after b0672 at 12:36Z)
- Today's fetches after tick: 112/2000
- Daily-budget headroom after tick: 1888
- LLM tokens: 0 (deterministic pipeline)
- Bandwidth: ~890 KB down across 8 fetches (largest: `act-zm-cap-470-postal-services-act` ≈ 237 KB AKN-HTML render; smallest: `si-zm-2019-076` ≈ 39 KB)

## Next

- Next Phase 8 tick will continue the nightly sampling cycle (different seed → different 8 records).
- The 15-record `parliament-pdf-v1.2` truncated-hash defect (b0670 discovery) remains a latent ~6% per-tick CHECK#3 hazard, pending Peter triage.
- The `zambialii_source_pdf_first_observation_drift` signal on `si-zm-2009-042` (b0671 discovery) also remains pending operator triage.
- Cumulative Phase 8 drift signal across b0641…b0673 continues to be dominated by the AKN-HTML dynamic-render cohort. Stable PDFs on `parliament.gov.zm`, `media.zambialii.org`, and zambialii.org AKN `/source.pdf` continue to dominate the match column.
