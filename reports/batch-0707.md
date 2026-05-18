# Phase 8 — Nightly Re-verification — batch 0707

- **Phase:** `phase_8_nightly_reverify`
- **Worker run id:** `b0707-phase8`
- **Script:** `scripts/batch_0707_phase8_reverify.py` (clone of frozen baseline `scripts/batch_0546_phase8_reverify.py`; only `BATCH` constant differs from `scripts/batch_0706_phase8_reverify.py`)
- **Parser version:** `phase8-reverify-0.1.0`
- **Seed:** `phase8-reverify-2026-05-18-b0707`
- **Started:** `2026-05-18T15:34:17Z`
- **Completed:** `2026-05-18T15:34:55Z`
- **Wall clock:** 38s (budget 20min; headroom ~19m22s)
- **Pool size:** 1964 records (records/**/*.json with both `source_url` + `source_hash`) — up 3 from b0706 (`pool_size=1961`) reflecting the three CoA judgment inserts by `b0706c-jiw` (`judgment-zm-2024-coa-024-kingfred-phiri-v-life-master-ltd`, `judgment-zm-2020-coa-113-chisumpa-liandisha-v-the-people`, `judgment-zm-2024-coa-211-rotor-moulder-enterprises-limited-v-stanley-jordan-6-others`).
- **Sample size:** 8 (`sample_rate 0.01`, capped at `MAX_BATCH=8`)
- **Fetches:** 8 (all HTTP 200)
- **Outcome counts:** match=3, drift=5, fetch_error=0
- **B2 sync:** deferred to host (rclone not in sandbox; Phase 8 is read-only on corpus — no `raw/` mutation)

## Results

| Verdict | Type | ID | Source host | URL kind | Notes |
|---|---|---|---|---|---|
| drift | statutory_instrument | si-zm-2022-050-customs-and-excise-general-amendment-regulations-2022 | zambialii.org | AKN bare-path (no `/eng@`, no `/source.pdf`) | `zambialii_akn_html_dynamic_render_drift` (bare-AKN-path sub-variant) |
| drift | act | act-zm-1984-005-excess-expenditure-appropriation-1981-act-1984 | zambialii.org | AKN-HTML `eng@`-suffixed | `zambialii_akn_html_dynamic_render_drift` cohort |
| drift | statutory_instrument | si-zm-1980-049-zambia-national-provident-fund-statutory-contributions-regulations-1980 | zambialii.org | AKN bare-path | `zambialii_akn_html_dynamic_render_drift` (bare-AKN-path sub-variant) |
| drift | statutory_instrument | si-zm-2020-043-electoral-process-local-government-by-election-election-date-and-time-of-poll-no-4-order-2020 | zambialii.org | AKN bare-path | `zambialii_akn_html_dynamic_render_drift` (bare-AKN-path sub-variant) |
| match | act | act-zm-2001-007-export-processing-zones-act-2001 | zambialii.org | AKN `source.pdf` | stable-PDF supercohort match (ZambiaLII source.pdf sub-variant) |
| drift | judgment | judgment-zm-2024-zmcc-21-mildred-luwaile-v-attorney-general | zambialii.org | AKN-HTML `eng@`-suffixed | `zambialii_akn_html_dynamic_render_drift` cohort |
| match | act | act-zm-2025-022-mobile-money-transaction-levy-act | www.parliament.gov.zm | parliament.gov.zm Act PDF | stable-PDF supercohort match |
| match | act | act-zm-cap-215-mineral-royalty-tax-repeal-act | www.parliament.gov.zm | parliament.gov.zm Act PDF | stable-PDF supercohort match |

This tick the sample again skewed toward the dynamic-rendered HTML cohort but was more balanced than b0706: 5 of 8 URLs were ZambiaLII AKN-HTML variants (1× `eng@`-suffixed act, 1× `eng@`-suffixed judgment, and 3× bare-AKN-path SIs) and 3 were stable PDFs (1× ZambiaLII `source.pdf` + 2× parliament.gov.zm Act PDFs). All 5 dynamic-render URLs drifted and all 3 stable PDFs matched — exactly as expected for the documented cohorts. AKN-HTML pages embed server-rendered timestamps and footer counters, so byte-level hash drift is the expected behaviour for these URL forms and does NOT imply substantive legal-text change.

The 3 matches confirm both branches of the stable-PDF supercohort remain 100% stable across this tick's sample:
- **parliament.gov.zm Act PDFs:** 2/2 match (Mobile Money Transaction Levy Act 22/2025 = 289,635 B; Mineral Royalty Tax (Repeal) Act = 49,680 B).
- **ZambiaLII `source.pdf`:** 1/1 match (Export Processing Zones Act 2001 = 2,016,052 B — the heaviest single fetch this tick).

Drift rate this tick (5/8 = 62.5%) reflects sample composition, not corpus health. Per-URL-kind hit rates remain consistent with prior ticks (AKN-HTML ≈100% drift; stable PDFs ≈100% match → 5/5 dynamic-HTML drift + 3/3 stable-PDF match).

No new sub-cohort was spawned. All drifts slot into the pre-existing `zambialii_akn_html_dynamic_render_drift` cohort (3 in the bare-AKN-path sub-variant and 2 in the `eng@`-suffixed sub-variant).

## Integrity checks

| # | Check | Result |
|---|---|---|
| 1 | JSON report well-formed; match+drift+fetch_error == sample_size (3+5+0=8) | PASS |
| 2 | No duplicate IDs in sample (8 unique) | PASS |
| 3 | Every stored + fetched sha256 is a valid 64-hex sha256 | PASS |
| 4 | Every sampled record's `stored_sha256` matches the on-disk record's `source_hash` (proper `sha256:` prefix-stripping) | PASS (no record file mutated this tick) |
| 5 | No tracked record file modified by this run (script is read-only) | PASS (`git diff --stat records/` empty pre-commit) |
| 6 | `corpus.sqlite` NOT touched; `approvals.yaml` NOT modified | PASS (`git diff --stat corpus.sqlite approvals.yaml` empty) |
| 7 | robots.txt respected; per-host rate limits honoured (zambialii.org min_gap ≥ 5s; deterministic `sleep_for_host` mechanism unchanged from baseline) | PASS |
| 8 | User-Agent honest: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` | PASS |
| 9 | corpus.sqlite live `quick_check=ok records=1961 records_fts=1961 dup_ids=0` (baseline parity preserved across tick) | PASS |

All 9 checks PASS — tick commits via normal path.

## Cost / budget

- Network fetches this tick: 8 (all HTTP 200)
- Cumulative daily fetches (all workers, NETWORK_FETCHES count rows only): ~64 (pre-tick) + 8 (this tick) ≈ ~72 of 2000 daily budget
- Tokens consumed: 0 (deterministic pipeline, no LLM calls)
- Bandwidth: 2,558,769 bytes total (~2.44 MB); largest = `act-zm-2001-007-export-processing-zones-act-2001` (2,016,052 B, ZambiaLII `source.pdf`)
- Wall clock: 38s (budget 20min; headroom ~19m22s)

## B2 sync

Deferred to host — rclone not available in sandbox. Phase 8 is read-only on corpus (no `raw/` mutation) so deferral is acceptable per BRIEF.md §8.

## Next tick

Routine Phase 8 sampling continues. No new audit-trail items spawned this tick. Pre-existing carry-forwards remain:
- `judgment-zm-2025-zmcc-14` canonical-URL-date variant 404 (b0700 — audit-only; remediation requires explicit Peter approval).
- Existing 15 `parliament-pdf-v1.2` truncated-16hex defect records remain an open operator-triage item (latent — not drawn this tick).
