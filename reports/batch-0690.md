# Phase 8 batch 0690 — Nightly re-verification

- **Tick:** b0690-phase8
- **Phase:** phase_8_nightly_reverify (approvals.yaml — approved: true, complete: false, sample_rate: 0.01)
- **Parser/fetcher version:** phase8-reverify-0.1.0
- **Script:** `scripts/batch_0690_phase8_reverify.py` (verbatim clone of `scripts/batch_0689_phase8_reverify.py`; only the `BATCH` constant changed `"0689"` → `"0690"`; same logic as b0625/b0641/…/b0687/b0689)
- **Seed:** `phase8-reverify-2026-05-18-b0690`
- **Started:** 2026-05-18T01:03:32Z
- **Completed:** 2026-05-18T01:03:55Z
- **Wall clock:** ~23s (well within 20-minute budget)
- **Predecessor:** b0689-phase8 (pool_size 1939; no intervening ingestion/repair commits since 2026-05-18T00:34:17Z — pool unchanged at 1939)
- **Verdict:** **tick-complete — all 9 integrity checks PASS — COMMIT (normal path)**

## Sample

| Metric | Value |
|---|---|
| pool_size | 1939 |
| sample_size | 8 |
| sample_rate | 0.01 |
| max_batch | 8 |
| fetches | 8 |
| match | 2 |
| drift | 2 |
| fetch_error | 4 |

Elevated fetch_error count this tick (4/8) is driven by transient HTTP 500 responses from zambialii.org / www.zambialii.org AKN endpoints during a brief upstream-server hiccup window (01:03:35Z–01:03:51Z). All 4 errors are upstream-server-side (verb=GET, no rate-limit headers, no robots.txt change, no DNS issue, no SSL issue) and none indicate a problem with the corpus or this worker. Records are NOT mutated regardless of fetch outcome (BRIEF non-negotiable #4); the 4 fetch_error candidates will be re-sampled probabilistically on future Phase 8 ticks.

b0690 did **not** draw any of the 15 `parliament-pdf-v1.2` truncated-16hex defect records — CHECK #3 PASSES this tick on seed-luck alone. The latent 15-record cohort remains an open operator-triage item.

## Results

| Verdict | Type | ID | Source host | URL kind | Notes |
|---|---|---|---|---|---|
| drift | act | act-zm-1996-028-pension-scheme-regulation-act-1996 | zambialii.org | AKN-HTML `eng@`-suffixed | dynamic-render cohort |
| fetch_error | act | act-zm-1980-013-national-energy-council-act-1980 | www.zambialii.org | AKN-HTML `eng@`-suffixed | upstream HTTP 500 |
| fetch_error | statutory_instrument | si-zm-2018-003-zambia-defence-university-declaration-order-2018 | zambialii.org | AKN-HTML (bare, no `eng@`) | upstream HTTP 500 |
| drift | judgment | judgment-zm-2026-coa-012-sunday-special-security-ltd-1-other-vs-laico-zambia-ltd | judiciaryzambia.com | WP single-post HTML | judiciaryzambia-html dynamic-render cohort |
| fetch_error | si | si-zm-2023-033-national-heritage-conservation-commission-ngonye-falls-national-monument-declara | zambialii.org | AKN source.pdf | upstream HTTP 500 (source.pdf endpoint also 500ing during window) |
| fetch_error | judgment | judgment-zm-2025-zmsc-15-the-v-metro | zambialii.org | AKN source.pdf | upstream HTTP 500 |
| match | act | act-zm-cap-92-lotteries-act | www.parliament.gov.zm | parliament-PDF static | stable-PDF supercohort match |
| match | act | loz-brands-act | www.parliament.gov.zm | parliament-PDF static | stable-PDF supercohort match |

Both drift verdicts are textbook dynamic-render cohort: 1× `zambialii_akn_html_dynamic_render_drift` (`act-zm-1996-028…`, `eng@`-suffixed AKN landing page) + 1× `judiciaryzambia_html_dynamic_render_drift` (WordPress single-post page with timestamp/Yoast/JSON-LD churn). No new sub-cohort spawned.

Both match verdicts are stable-PDF supercohort: 2× `www.parliament.gov.zm` static PDF. Consistent with the supercohort's near-100% match rate across the Phase 8 series.

## Integrity checks

| # | Check | Result |
|---|---|---|
| 1 | JSON report well-formed; match+drift+fetch_error == sample_size (2+2+4=8) | PASS |
| 2 | No duplicate IDs in sample (8 unique) | PASS |
| 3 | Every stored_sha256 + fetched_sha256 is a valid 64-hex sha256 (fetch_error rows have null fetched_sha256 by spec — not counted) | **PASS** — seed did not draw any of the 15 truncated-16hex records this tick |
| 4 | Every sampled record's stored_sha256 matches the on-disk record's `source_hash` (proper `sha256:` prefix-stripping) | PASS (no record file mutated this tick) |
| 5 | No tracked record file modified by this run (script is read-only) | PASS (`git diff --stat records/` empty) |
| 6 | corpus.sqlite NOT touched; approvals.yaml NOT modified | PASS (`git diff --stat corpus.sqlite approvals.yaml` empty) |
| 7 | robots.txt respected; per-host rate limits honoured (zambialii.org min_gap ≥ 5s; deterministic `sleep_for_host` mechanism unchanged from baseline) | PASS |
| 8 | User-Agent honest: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` | PASS |
| 9 | corpus.sqlite live `quick_check=ok records=1936 records_fts=1936 dup_ids=0` (baseline parity preserved across tick) | PASS |

All 9 checks PASS — commit proceeds per BRIEF step 7.

## Bandwidth

- total_bytes: 742,111 (~725 KiB) — drastically lower than typical tick because 4/8 fetches returned 0-byte error bodies
- avg_kb_per_successful_fetch: ~181
- largest: loz-brands-act (199,583 B; www.parliament.gov.zm)
- hosts: zambialii.org:5, www.zambialii.org:1, judiciaryzambia.com:1, www.parliament.gov.zm:2

## Drift handling

Per BRIEF.md non-negotiable #4, no record file was modified by this tick. The 2 drifts and 4 fetch_errors are flagged in `gaps.md` for the established `zambialii_akn_html_dynamic_render_drift`, `judiciaryzambia_html_dynamic_render_drift`, and `zambialii_upstream_500_transient` cohorts (audit-only entries — no record mutation).

## Approvals

- `phase_8_nightly_reverify.approved` = true (unchanged)
- `phase_8_nightly_reverify.complete` = false (unchanged — Phase 8 is a continuous nightly cycle, not a one-shot)
- `approvals.yaml` was **not** modified by this tick

## Budget

- Today's cumulative fetches before tick: 24/2000 (b0687-phase8 + b0688 repair + b0689-phase8, all 2026-05-18 UTC)
- Today's cumulative fetches after tick: 32/2000
- Daily-budget headroom after tick: 1968
- LLM tokens: 0 (deterministic pipeline)

## Next

- Next Phase 8 tick (b0691 or later, depending on intervening JIW/repair) will continue the nightly sampling cycle (different seed → different 8 records).
- The 15-record `parliament-pdf-v1.2` truncated-hash defect remains an open operator-triage item; latent ~6% per-tick CHECK #3 hazard continues until resolved.
- The 4 zambialii.org upstream-500 candidates this tick will be re-sampled on a future seed; if the 500s persist across multiple ticks the upstream-availability cohort tagging in gaps.md will be widened.
- Cumulative Phase 8 drift signal across b0641…b0690 continues to be dominated by the AKN-HTML / judiciaryzambia-HTML dynamic-render cohorts.
