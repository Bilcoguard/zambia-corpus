# Phase 8 batch 0689 — Nightly re-verification

- **Tick:** b0689-phase8
- **Phase:** phase_8_nightly_reverify (approvals.yaml — approved: true, complete: false, sample_rate: 0.01)
- **Parser/fetcher version:** phase8-reverify-0.1.0
- **Script:** `scripts/batch_0689_phase8_reverify.py` (verbatim clone of `scripts/batch_0687_phase8_reverify.py`; only the `BATCH` constant changed `"0687"`→`"0689"`; same logic as b0625/b0641/…/b0684/b0687)
- **Seed:** `phase8-reverify-2026-05-18-b0689`
- **Started:** 2026-05-18T00:33:55Z
- **Completed:** 2026-05-18T00:34:17Z
- **Wall clock:** ~22s (well within 20-minute budget)
- **Predecessor:** b0687-phase8 (committed d44205f); intervening commits b0687-jiw judgment-ingestion + b0688 repair (commit 1e52dca) grew the pool from 1931 → 1939
- **Verdict:** **tick-complete — 8/8 integrity PASS — COMMIT (normal path)**

## Sample

| Metric | Value |
|---|---|
| pool_size | 1939 |
| sample_size | 8 |
| sample_rate | 0.01 |
| max_batch | 8 |
| fetches | 8 |
| match | 5 |
| drift | 3 |
| fetch_error | 0 |

Pool size 1939 reflects b0687-jiw (+8 ZMCC 2025 hand-curated reparse) and b0688 repair (no record-count delta). b0689 did **not** draw any of the 15 `parliament-pdf-v1.2` truncated-16hex defect records — CHECK #3 PASSES this tick on seed-luck alone. The latent 15-record cohort remains an open operator-triage item.

## Results

| Verdict | Type | ID | Source host | URL kind | Notes |
|---|---|---|---|---|---|
| match | si  | si-zm-2019-062-income-tax-konoike-construction-company-limited-approval-and-exemption-order-2019 | media.zambialii.org | source.pdf static | stable-PDF supercohort match |
| match | si  | si-zm-2012-005-property-transfer-tax-exemption-order-2012 | zambialii.org | AKN source.pdf static | stable-PDF supercohort match |
| drift | si  | si-zm-2021-072-public-holidays-declaration-no-3-notice-2021 | zambialii.org | AKN-HTML (no `eng@` suffix) | dynamic-render cohort |
| match | act | act-zm-cap-189-lands-acquisition-act | www.parliament.gov.zm | parliament-PDF static | stable-PDF supercohort match |
| drift | judgment | judgment-zm-2024-zmsc-02-mabvuto-mwale-and-anor-v-the-people | zambialii.org | AKN-HTML `eng@`-suffixed | dynamic-render cohort |
| match | act | act-zm-2024-018-the-green-economy-and-climate-change-act-2024 | www.parliament.gov.zm | parliament-PDF static | stable-PDF supercohort match |
| drift | act | act-zm-1965-023-national-flag-and-armorial-ensigns-act-1965 | zambialii.org | AKN-HTML `eng@`-suffixed | dynamic-render cohort |
| match | act | act-zm-1991-019-investment-act-1991 | media.zambialii.org | source.pdf static | stable-PDF supercohort match |

All 3 drift verdicts are textbook `zambialii_akn_html_dynamic_render_drift` cohort — `zambialii.org/akn/zm/...` HTML landing pages (timestamp/footer-counter drift, legal content unchanged). 2 are `eng@`-suffixed and 1 is bare AKN-HTML — both variants nest in the established b0641..b0687 cohort. No new sub-cohort spawned.

All 5 match verdicts are stable-PDF supercohort: 2× `www.parliament.gov.zm` static PDF + 2× `media.zambialii.org` source.pdf + 1× `zambialii.org/akn/.../source.pdf`. Consistent with the supercohort's near-100% match rate across the Phase 8 series.

## Integrity checks

| # | Check | Result |
|---|---|---|
| 1 | JSON report well-formed; match+drift+fetch_error == sample_size (5+3+0=8) | PASS |
| 2 | No duplicate IDs in sample (8 unique) | PASS |
| 3 | Every stored_sha256 + fetched_sha256 is a valid 64-hex sha256 | **PASS** — seed did not draw any of the 15 truncated-16hex records this tick |
| 4 | Every sampled record's stored_sha256 matches the on-disk record's `source_hash` (proper `sha256:` prefix-stripping) | PASS (no record file mutated this tick) |
| 5 | No tracked record file modified by this run (script is read-only) | PASS |
| 6 | corpus.sqlite NOT touched; approvals.yaml NOT modified | PASS |
| 7 | robots.txt respected; per-host rate limits honoured (zambialii.org min_gap ≥ 5s; deterministic `sleep_for_host` mechanism unchanged from baseline) | PASS |
| 8 | User-Agent honest: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` | PASS |
| 9 | corpus.sqlite live `quick_check=ok records=1936 records_fts=1936 dup_ids=0` (baseline parity preserved across tick) | PASS |

All 9 checks PASS — commit proceeds per BRIEF step 7.

## Bandwidth

- total_bytes: 6,240,042 (~5.95 MiB)
- avg_kb_per_fetch: 761.7
- largest: act-zm-1991-019-investment-act-1991 (5,268,696 B; media.zambialii.org source.pdf)
- hosts: zambialii.org:4, media.zambialii.org:2, www.parliament.gov.zm:2

## Drift handling

Per BRIEF.md non-negotiable #4, no record file was modified by this tick. The 3 AKN-HTML drifts are flagged in `gaps.md` for the existing `zambialii_akn_html_dynamic_render_drift` cohort (audit-only entries).

## Approvals

- `phase_8_nightly_reverify.approved` = true (unchanged)
- `phase_8_nightly_reverify.complete` = false (unchanged — Phase 8 is a continuous nightly cycle, not a one-shot)
- `approvals.yaml` was **not** modified by this tick

## Budget

- Today's cumulative fetches before tick: 16/2000 (b0687-phase8 + b0688 repair, all 2026-05-18 UTC)
- Today's cumulative fetches after tick: 24/2000
- Daily-budget headroom after tick: 1976
- LLM tokens: 0 (deterministic pipeline)

## Bundled trailer commits

This commit also bundles the deferred `TRAILER_COMMIT_DEFERRED` worker.log lines from **b0688 repair** (deferred 2026-05-18T00:18:00Z per established FUSE-EPERM on `.git/index.lock` pattern from b0676..b0688) — specifically the b0687-jiw POSTRECOVERY trailer at 2026-05-18T02:18:00Z.

## Next

- Next Phase 8 tick (b0690 or later, depending on intervening JIW/repair) will continue the nightly sampling cycle (different seed → different 8 records).
- The 15-record `parliament-pdf-v1.2` truncated-hash defect remains an open operator-triage item; latent ~6% per-tick CHECK #3 hazard continues until resolved.
- Cumulative Phase 8 drift signal across b0641…b0689 continues to be dominated by the AKN-HTML dynamic-render cohort.
