# Phase 8 batch 0678 — Nightly re-verification (HALT — CHECK #3 FAIL)

- **Tick:** b0678-phase8
- **Phase:** phase_8_nightly_reverify (approvals.yaml — approved: true, complete: false, sample_rate: 0.01)
- **Parser/fetcher version:** phase8-reverify-0.1.0
- **Script:** `scripts/batch_0678_phase8_reverify.py` (verbatim clone of frozen baseline `scripts/batch_0546_phase8_reverify.py`; only the `BATCH` constant + docstring batch identifier changed; same logic as b0625/b0641/b0652/b0653/b0655/b0660/b0662/b0663/b0665/b0666/b0668/b0669/b0670/b0671/b0672/b0673/b0674/b0675/b0676/b0677)
- **Seed:** `phase8-reverify-2026-05-15-b0678`
- **Started:** 2026-05-15T16:05:34Z
- **Completed:** 2026-05-15T16:06:08Z
- **Wall clock:** ~34s (well within 20-minute budget)
- **Predecessor:** b0677-phase8 (commit `ceb583b`, tick-complete, 2 match / 6 drift / 0 fetch_error).
- **Verdict:** **HALT — CHECK #3 FAIL — no commit, no push.** See `error-reports/2026-05-15T160608Z-b0678-check3-fail.md` for the full diagnostic.

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

Pool size 1928 unchanged from b0666…b0677. b0678 **did** draw one of the 15 `parliament-pdf-v1.2` truncated-16hex defect records (`act-zm-2020-012-companies-amendment-act-2020`) — second draw from the 15-record latent cohort since b0670 first formalised it.

## Results

| Verdict | Type | ID | Source host | URL kind | Notes |
|---|---|---|---|---|---|
| match | si | si-zm-2023-001-income-tax-double-taxation-relief-taxes-on-income-united-arab-emirates-order-202 | zambialii.org | AKN `eng@/source.pdf` | stable-PDF supercohort match |
| drift | act | act-zm-1996-014-judges-conditions-of-service-act-1996 | zambialii.org | AKN-HTML `eng@`-suffixed | dynamic-render cohort |
| drift | statutory_instrument | si-zm-2021-094-electricity-common-carrier-declaration-revocation-order-2021 | zambialii.org | AKN `eng@`-less landing | dynamic-render cohort |
| drift | act | act-zm-1988-030-excess-expenditure-appropriation-1986-act-1988 | zambialii.org | AKN-HTML `eng@`-suffixed | dynamic-render cohort |
| drift | act | **act-zm-2020-012-companies-amendment-act-2020** | www.parliament.gov.zm | parliament-PDF static | **truncated-16hex stored_hash defect (CHECK #3 FAIL trigger)** — prefix-matches fetched full digest |
| drift | act | act-zm-2019-017-supplementary-appropriation-2019-no-2-act | zambialii.org | AKN-HTML `eng@`-suffixed | dynamic-render cohort |
| match | si | si-zm-1981-048-income-tax-exempt-organisations-approval-order-1981 | zambialii.org | AKN `eng@/source.pdf` | stable-PDF supercohort match |
| match | act | act-zm-2012-001-the-penal-code-amendment-2012 | www.parliament.gov.zm | parliament-PDF static | stable-PDF supercohort match |

Of the 5 "drift" verdicts:
- **4 are zambialii_akn_html_dynamic_render_drift cohort** (timestamp/footer-counter drift on AKN HTML landing pages; legal content unchanged). Nest cleanly in the existing b0641..b0677 cohort.
- **1 is the parliament-pdf-v1.2 truncated-16hex stored_hash defect** (`act-zm-2020-012`). Re-fetched full digest `bc5fb904bb25c673a3d70db38f2a56a8331679cd43e474e5c97a0fe0b8289ec8` prefix-matches the stored 16-hex `bc5fb904bb25c673` → body content unchanged; the "drift" is purely an artefact of the truncated stored hash. This is the CHECK #3 FAIL trigger.

The 3 **match** verdicts are exactly the stable-PDF supercohort signature: one `zambialii.org` AKN `/source.pdf`, one `zambialii.org` AKN `/source.pdf`, and one `www.parliament.gov.zm` static PDF. Consistent with the supercohort's near-100% match rate across the Phase 8 series.

## Integrity checks

| # | Check | Result |
|---|---|---|
| 1 | JSON report well-formed; match+drift+fetch_error == sample_size (3+5+0=8) | PASS |
| 2 | No duplicate IDs in sample (8 unique) | PASS |
| 3 | Every stored_sha256 + fetched_sha256 is a valid 64-hex sha256 | **FAIL** — `act-zm-2020-012-companies-amendment-act-2020` stored_sha256 is only 16 hex chars (`bc5fb904bb25c673`), part of the b0670-formalised parliament-pdf-v1.2 truncated-16hex cohort |
| 4 | Every sampled record's stored_sha256 matches the on-disk record's `source_hash` | PASS (no record file mutated this tick) |
| 5 | No tracked record file modified by this run (script is read-only) | PASS |
| 6 | corpus.sqlite NOT touched; approvals.yaml NOT modified | PASS |
| 7 | robots.txt respected; per-host rate limits honoured (zambialii.org min_gap ≥ 5s; deterministic `sleep_for_host` mechanism unchanged from baseline) | PASS |
| 8 | User-Agent honest: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` | PASS |

CHECK #3 FAIL fires the BRIEF.md non-negotiable #7 gate ("Integrity checks before every commit. If any check fails, halt, do not commit, log to worker.log."). All other checks PASS — the HALT is narrowly scoped to this single record-cohort issue and does not indicate any regression in the Phase 8 pipeline.

## Drift handling

Per BRIEF.md non-negotiable #4 ("never silently overwrite"), no record file was modified by this tick. The 4 AKN-HTML drifts are flagged in `gaps.md` for the existing `zambialii_akn_html_dynamic_render_drift` cohort. The `act-zm-2020-012` CHECK #3 trigger is flagged in `gaps.md` under the `parliament_pdf_v1_2_truncated_16hex_source_hash` cohort and the full diagnostic is at `error-reports/2026-05-15T160608Z-b0678-check3-fail.md`.

## Approvals

- `phase_8_nightly_reverify.approved` = true (unchanged)
- `phase_8_nightly_reverify.complete` = false (unchanged — Phase 8 is a continuous nightly cycle, not a one-shot)
- `approvals.yaml` was **not** modified by this tick

## Budget

- Today's fetches before tick: 144/2000 (after b0677 at 15:34:59Z)
- Today's fetches after tick: 152/2000
- Daily-budget headroom after tick: 1848
- LLM tokens: 0 (deterministic pipeline)
- Bandwidth: 8 fetches, see costs.log BANDWIDTH line for this batch.

## Next

- Next Phase 8 tick (b0679) will continue the nightly sampling cycle (different seed → different 8 records).
- Per the b0671 precedent, b0679 should bundle this tick's HALT artefacts (this report, the JSON, the diagnostic, the gaps.md entries, and the b0677 trailer lines in worker.log) into its own commit if its integrity passes.
- The 15-record `parliament-pdf-v1.2` truncated-hash defect remains an open operator-triage item; this is its second Phase 8 observation in 9 ticks. The recommended remediation path is unchanged from b0670 §D.
- Cumulative Phase 8 drift signal across b0641…b0678 continues to be dominated by the AKN-HTML dynamic-render cohort, with the 15-record truncated-hash cohort as a known latent ~6% per-tick hazard.
