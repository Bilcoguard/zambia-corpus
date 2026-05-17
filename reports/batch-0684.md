# Phase 8 batch 0684 — Nightly re-verification

- **Tick:** b0684-phase8
- **Phase:** phase_8_nightly_reverify (approvals.yaml — approved: true, complete: false, sample_rate: 0.01)
- **Parser/fetcher version:** phase8-reverify-0.1.0
- **Script:** `scripts/batch_0684_phase8_reverify.py` (verbatim clone of `scripts/batch_0683_phase8_reverify.py`; only the `BATCH` constant changed `"0683"`→`"0684"`; same logic as b0625/b0641/…/b0680/b0683)
- **Seed:** `phase8-reverify-2026-05-17-b0684`
- **Started:** 2026-05-17T23:33:39Z
- **Completed:** 2026-05-17T23:34:13Z
- **Wall clock:** ~34s (well within 20-minute budget)
- **Predecessor:** b0683-phase8 (committed 640b975, bundled b0682-recovery trailer)
- **Verdict:** **tick-complete — 8/8 integrity PASS — COMMIT (normal path)**

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

Pool size 1928 unchanged from b0666…b0683. b0684 **did not** draw any of the 15 `parliament-pdf-v1.2` truncated-16hex defect records — CHECK #3 PASSES this tick on seed-luck alone. The 15-record latent cohort remains an open operator-triage item.

## Results

| Verdict | Type | ID | Source host | URL kind | Notes |
|---|---|---|---|---|---|
| drift | act | act-zm-1969-024-finance-control-and-management-act-1969 | zambialii.org | AKN-HTML `eng@`-suffixed | dynamic-render cohort |
| match | act | act-zm-2021-023-higher-education-amendment-act-of-2021 | www.parliament.gov.zm | parliament-PDF static | stable-PDF supercohort match |
| drift | si  | si-zm-1986-032-national-archives-place-of-deposit-declaration-order-1986 | zambialii.org | AKN-HTML (no `eng@` suffix) | dynamic-render cohort |
| drift | act | act-zm-2005-008-supplementary-appropriation-2003-act | zambialii.org | AKN-HTML `eng@`-suffixed | dynamic-render cohort |
| drift | act | act-zm-1953-059-noxious-weeds-act | zambialii.org | AKN-HTML `eng@`-suffixed | dynamic-render cohort |
| drift | act | act-zm-cap-64-affiliation-and-maintenance-of-children-act | zambialii.org | AKN-HTML `eng@`-suffixed | dynamic-render cohort |
| drift | act | act-zm-2022-004-social-workers-association-of-zambia-act-2022 | zambialii.org | AKN-HTML `eng@`-suffixed | dynamic-render cohort |
| match | act | act-zm-cap-184-lands-act | www.parliament.gov.zm | parliament-PDF static | stable-PDF supercohort match |

All 6 drift verdicts are textbook `zambialii_akn_html_dynamic_render_drift` cohort — `zambialii.org/akn/zm/...` HTML landing pages (timestamp/footer-counter drift, legal content unchanged). 5 are `eng@`-suffixed and 1 is bare AKN-HTML — both variants nest in the established b0641..b0683 cohort. No new sub-cohort spawned.

Both match verdicts are stable-PDF supercohort: 2× `www.parliament.gov.zm` static PDF. Consistent with the supercohort's near-100% match rate across the Phase 8 series.

## Integrity checks

| # | Check | Result |
|---|---|---|
| 1 | JSON report well-formed; match+drift+fetch_error == sample_size (2+6+0=8) | PASS |
| 2 | No duplicate IDs in sample (8 unique) | PASS |
| 3 | Every stored_sha256 + fetched_sha256 is a valid 64-hex sha256 | **PASS** — seed did not draw any of the 15 truncated-16hex records this tick |
| 4 | Every sampled record's stored_sha256 matches the on-disk record's `source_hash` | PASS (no record file mutated this tick) |
| 5 | No tracked record file modified by this run (script is read-only) | PASS |
| 6 | corpus.sqlite NOT touched; approvals.yaml NOT modified | PASS |
| 7 | robots.txt respected; per-host rate limits honoured (zambialii.org min_gap ≥ 5s; deterministic `sleep_for_host` mechanism unchanged from baseline) | PASS |
| 8 | User-Agent honest: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` | PASS |

All 8 checks PASS — commit proceeds per BRIEF step 7.

## Bandwidth

- total_bytes: 1,100,316 (~1.05 MiB)
- avg_kb_per_fetch: 134.3
- largest: act-zm-cap-184-lands-act (370,573 B; www.parliament.gov.zm static PDF)
- hosts: zambialii.org:6, www.parliament.gov.zm:2

## Drift handling

Per BRIEF.md non-negotiable #4, no record file was modified by this tick. The 6 AKN-HTML drifts are flagged in `gaps.md` for the existing `zambialii_akn_html_dynamic_render_drift` cohort (audit-only entries).

## Approvals

- `phase_8_nightly_reverify.approved` = true (unchanged)
- `phase_8_nightly_reverify.complete` = false (unchanged — Phase 8 is a continuous nightly cycle, not a one-shot)
- `approvals.yaml` was **not** modified by this tick

## Budget

- Today's fetches before tick: 8/2000 (post-b0683 on 2026-05-17 UTC date)
- Today's fetches after tick: 16/2000
- Daily-budget headroom after tick: 1984
- LLM tokens: 0 (deterministic pipeline)

## Bundled trailer commits

This commit also bundles the deferred `TRAILER_COMMIT_DEFERRED` worker.log lines from **b0683-phase8** (deferred 2026-05-17T23:07:51Z per established FUSE-EPERM on `.git/index.lock` pattern from b0676..b0683).

## Next

- Next Phase 8 tick (b0685) will continue the nightly sampling cycle (different seed → different 8 records).
- The 15-record `parliament-pdf-v1.2` truncated-hash defect remains an open operator-triage item; latent ~6% per-tick CHECK #3 hazard continues until resolved.
- Cumulative Phase 8 drift signal across b0641…b0684 continues to be dominated by the AKN-HTML dynamic-render cohort.
- b0682-recovery flagged 2 operator-triage items: (a) record-count 1943-vs-1925 consistency, (b) "test append" debug line at worker.log:8519 (now committed).
