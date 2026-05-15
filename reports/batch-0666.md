# Phase 8 batch 0666 — Nightly re-verification

- **Tick:** b0666-phase8
- **Phase:** phase_8_nightly_reverify (approvals.yaml — approved: true, complete: false, sample_rate: 0.01)
- **Parser/fetcher version:** phase8-reverify-0.1.0
- **Script:** `scripts/batch_0666_phase8_reverify.py` (verbatim clone of frozen baseline `scripts/batch_0546_phase8_reverify.py`; only the `BATCH` constant + docstring batch identifier changed; same logic as b0625/b0641/b0652/b0653/b0655/b0660/b0662/b0663/b0665)
- **Seed:** `phase8-reverify-2026-05-15-b0666`
- **Started:** 2026-05-15T10:04:51Z
- **Completed:** 2026-05-15T10:05:19Z
- **Wall clock:** ~28s (well within 20-minute budget)

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

Pool size 1928 unchanged from b0663/b0665 (no JIW ingestions between b0665 at 09:35Z and b0666 at 10:05Z; b0664 repair tick mutated existing records in place but did not add new records).

## Results

| Verdict | Type | ID | Source host |
|---|---|---|---|
| drift | act | act-zm-2022-030-appropriation-act | zambialii.org (AKN-HTML, eng@-suffixed) |
| match | act | act-zm-1997-020-national-assembly-speakers-retirement-benefits-act-1997 | www.zambialii.org (AKN source.pdf) |
| drift | act | act-zm-1994-030-excess-expenditure-appropriation-1991-act-1994 | zambialii.org (AKN-HTML, eng@-suffixed) |
| drift | judgment | judgment-zm-2023-zmsc-06-sakala-v-people | zambialii.org (AKN-HTML, eng@-suffixed) |
| match | act | act-zm-2025-008-border-management-trade-facilitation-act2025 | www.parliament.gov.zm (static PDF) |
| match | si | si-zm-2021-107-income-tax-transfer-pricing-amendment-regulations-2021 | zambialii.org (AKN source.pdf) |
| match | si | si-zm-2007-019-value-added-tax-taxable-value-regulations-2007 | zambialii.org (AKN source.pdf) |
| match | act | act-zm-2019-003-employment-code-act-2019 | www.parliament.gov.zm (static PDF) |

All three drift verdicts are on **ZambiaLII AKN-HTML** pages — known dynamic-content rendering pattern from b0641/b0642/b0652/b0653/b0655/b0660/b0662/b0663/b0665 (rendered timestamps and footer counters drift the response sha256 across re-fetches even though the legal content is unchanged). All five match verdicts are on static PDFs — three on `zambialii.org`/`www.zambialii.org` AKN `source.pdf` Akoma Ntoso publication PDFs, two on `www.parliament.gov.zm` static PDFs — consistent with the long-running observation that static-PDF canonical URLs are 100% match while dynamic AKN HTML pages drift. This batch contains no `judiciaryzambia.com` or `media.zambialii.org` candidates.

## Integrity checks

| # | Check | Result |
|---|---|---|
| 1 | JSON report well-formed; match+drift+fetch_error == sample_size (5+3+0=8) | PASS |
| 2 | No duplicate IDs in sample (8 unique) | PASS |
| 3 | Every stored_sha256 + fetched_sha256 is a valid 64-hex sha256 | PASS |
| 4 | Every sampled record's stored_sha256 matches the on-disk record's `source_hash` | PASS |
| 5 | No record file mutated by this run (all mtimes < started_at) | PASS |
| 6 | corpus.sqlite NOT touched; records/ NOT touched; approvals.yaml NOT modified | PASS |
| 7 | robots.txt respected; per-host rate limits honoured (zambialii.org=5s gaps observed; www.zambialii.org=5s single-host gap; www.parliament.gov.zm two fetches with rate-default 2s gap) | PASS |
| 8 | User-Agent honest: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` | PASS |

## Drift handling

Per BRIEF.md non-negotiable #4 ("never silently overwrite"), drift on dynamically-rendered HTML pages is **flagged** in `gaps.md`, not auto-overwritten. A separate human-approved remediation tick would be required to either (a) re-snapshot the affected records and update `source_hash`, or (b) switch the canonical `source_url` to a static `source.pdf` Akoma Ntoso publication PDF (where available on `media.zambialii.org`/`www.zambialii.org`). None of the drift records' `source_hash` values on disk were modified by this tick.

## Approvals

- `phase_8_nightly_reverify.approved` = true (unchanged)
- `phase_8_nightly_reverify.complete` = false (unchanged — Phase 8 is a continuous nightly cycle, not a one-shot)
- `approvals.yaml` was **not** modified by this tick

## Budget

- Today's fetches before tick: 40/2000 (after b0665-phase8 09:35Z)
- Today's fetches after tick: 48/2000
- LLM tokens: 0 (deterministic pipeline)
- Bandwidth: ~1.77 MB down (2 parliament.gov.zm static PDFs ≈ 742 KB + 3 zambialii AKN source.pdf ≈ 998 KB + 3 zambialii AKN-HTML payloads ≈ 119 KB)

## Next

- Next Phase 8 tick will continue the nightly sampling cycle (different seed → different 8 records).
- Cumulative Phase 8 drift signal across b0641/b0642/b0652/b0653/b0655/b0660/b0662/b0663/b0665/b0666: every drift verdict so far has been a dynamic-render HTML page (predominantly zambialii AKN-HTML, plus one judiciaryzambia.com in b0665); static PDFs (parliament.gov.zm + zambialii AKN source.pdf + media.zambialii.org source.pdf) remain 100% match. b0666 is the first Phase 8 batch in this series with majority-match verdicts (5/8) — driven by an even mix of static-PDF candidates in this sample; the drift rate on the AKN-HTML subset remains 3/3 = 100%, consistent with prior batches. A Peter-approved bounded remediation tick — either re-snapshot dynamic-render records or switch canonical URLs to source.pdf where available — would clear most outstanding drift entries in `gaps.md`.
