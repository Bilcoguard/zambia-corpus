# Phase 8 batch 0669 — Nightly re-verification

- **Tick:** b0669-phase8
- **Phase:** phase_8_nightly_reverify (approvals.yaml — approved: true, complete: false, sample_rate: 0.01)
- **Parser/fetcher version:** phase8-reverify-0.1.0
- **Script:** `scripts/batch_0669_phase8_reverify.py` (verbatim clone of frozen baseline `scripts/batch_0546_phase8_reverify.py`; only the `BATCH` constant + docstring batch identifier changed; same logic as b0625/b0641/b0652/b0653/b0655/b0660/b0662/b0663/b0665/b0666/b0668)
- **Seed:** `phase8-reverify-2026-05-15-b0669`
- **Started:** 2026-05-15T11:04:29Z
- **Completed:** 2026-05-15T11:05:07Z
- **Wall clock:** ~38s (well within 20-minute budget)

## Sample

| Metric | Value |
|---|---|
| pool_size | 1928 |
| sample_size | 8 |
| sample_rate | 0.01 |
| max_batch | 8 |
| fetches | 8 |
| match | 7 |
| drift | 1 |
| fetch_error | 0 |

Pool size 1928 unchanged from b0666/b0668 (b0667 was a repair tick that updated existing record bodies in place without changing record count, so the Phase 8 pool selection is identical at 1928).

## Results

| Verdict | Type | ID | Source host |
|---|---|---|---|
| match | statutory_instrument | si-zm-2022-059-value-added-tax-zero-rating-amendment-no-2-order-2022 | zambialii.org (AKN source.pdf) |
| match | statutory_instrument | si-zm-2020-048-employment-code-exemption-regulations-2020 | zambialii.org (AKN source.pdf) |
| match | statutory_instrument | si-zm-2015-035-property-transfer-tax-exemption-no-2-order-2015 | zambialii.org (AKN source.pdf) |
| match | statutory_instrument | si-zm-1987-009-income-tax-foreign-organisations-exemption-approval-order-1987 | zambialii.org (AKN source.pdf) |
| drift | judgment | judgment-zm-2021-zmcc-16-sampa-v-mundubile-and-anor | zambialii.org (AKN-HTML, eng@-suffixed) |
| match | statutory_instrument | si-zm-2015-085-education-teacher-training-college-boards-establishment-order-2015 | zambialii.org (AKN source.pdf) |
| match | act | act-zm-2012-002-the-aviation-amendment-act-2012 | www.parliament.gov.zm (static PDF) |
| match | statutory_instrument | si-zm-2021-102-customs-and-excise-electronic-machinery-and-equipment-suspension-regulations-2021 | zambialii.org (AKN source.pdf) |

The single **drift** verdict is on a **ZambiaLII AKN-HTML** judgment page — the well-known dynamic-content rendering pattern documented across b0641/b0642/b0652/b0653/b0655/b0660/b0662/b0663/b0665/b0666/b0668 (rendered timestamps and footer counters drift the response sha256 across re-fetches even though the legal content is unchanged). All seven **match** verdicts are on static PDFs (six on `zambialii.org` AKN `source.pdf` Akoma Ntoso publication PDFs and one on `www.parliament.gov.zm`) — consistent with the standing observation that static-PDF canonical URLs are 100% match while dynamic AKN HTML pages drift.

## Integrity checks

| # | Check | Result |
|---|---|---|
| 1 | JSON report well-formed; match+drift+fetch_error == sample_size (7+1+0=8) | PASS |
| 2 | No duplicate IDs in sample (8 unique) | PASS |
| 3 | Every stored_sha256 + fetched_sha256 (where present) is a valid 64-hex sha256 | PASS |
| 4 | Every sampled record's stored_sha256 matches the on-disk record's `source_hash` | PASS |
| 5 | No record file mutated by this run (script is read-only) | PASS |
| 6 | corpus.sqlite NOT touched; records/ NOT touched; approvals.yaml NOT modified | PASS |
| 7 | robots.txt respected; per-host rate limits honoured (zambialii.org min_gap=5.0s ≥ required 5s; www.parliament.gov.zm single-fetch — no intra-host gap to enforce) | PASS |
| 8 | User-Agent honest: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` | PASS |

## Drift handling

Per BRIEF.md non-negotiable #4 ("never silently overwrite"), drift on dynamically-rendered HTML pages is **flagged** in `gaps.md`, not auto-overwritten. The drift record's `source_hash` on disk was NOT modified by this tick; the discrepancy is logged as an audit signal only.

## Approvals

- `phase_8_nightly_reverify.approved` = true (unchanged)
- `phase_8_nightly_reverify.complete` = false (unchanged — Phase 8 is a continuous nightly cycle, not a one-shot)
- `approvals.yaml` was **not** modified by this tick

## Budget

- Today's fetches before tick: 72/2000 (after b0668 at 10:34Z)
- Today's fetches after tick: 80/2000
- LLM tokens: 0 (deterministic pipeline)
- Bandwidth: ~961 KB down (largest: si-zm-1987-009 ≈ 329 KB; smallest: si-zm-2020-048 ≈ 12 KB)

## Next

- Next Phase 8 tick will continue the nightly sampling cycle (different seed → different 8 records).
- Cumulative Phase 8 drift signal across b0641…b0669 remains: every drift verdict has been a dynamic-render HTML page (overwhelmingly zambialii AKN-HTML, plus one judiciaryzambia.com in b0665). Static PDFs (parliament.gov.zm + zambialii AKN source.pdf + media.zambialii.org source.pdf) remain 100% match where the upstream URL is still reachable. The b0668 fetch_error on the 2026 NPS Act parliament.gov.zm URL remains the only non-dynamic-render anomaly observed and awaits Peter-approved bounded remediation.
