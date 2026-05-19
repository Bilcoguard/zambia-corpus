# Phase 8 — Nightly Re-verification — batch 0715

- **Phase:** `phase_8_nightly_reverify`
- **Worker run id:** `b0715-phase8`
- **Script:** `scripts/batch_0715_phase8_reverify.py` (clone of frozen baseline `scripts/batch_0546_phase8_reverify.py`; only `BATCH` constant and docstring header differ from `scripts/batch_0714_phase8_reverify.py`)
- **Parser version:** `phase8-reverify-0.1.0`
- **Seed:** `phase8-reverify-2026-05-18-b0715`
- **Started:** `2026-05-18T19:33:05Z`
- **Completed:** `2026-05-18T19:33:26Z`
- **Wall clock:** 21s (budget 20min; headroom ~19m39s)
- **Pool size:** 1965 records (records/**/*.json with both `source_url` + `source_hash`) — unchanged from b0714 (`pool_size=1965`); corpus.sqlite live count remains 1962 (delta to pool is unchanged: 3 records-without-source_hash continue to be excluded from the Phase 8 pool by design).
- **Sample size:** 8 (`sample_rate 0.01`, capped at `MAX_BATCH=8`)
- **Fetches:** 8 (all HTTP 200)
- **Outcome counts:** match=5, drift=3, fetch_error=0
- **B2 sync:** deferred to host (rclone not in sandbox; Phase 8 is read-only on corpus — no `raw/` mutation)

## Results

| Verdict | Type | ID | Source host | URL kind | Notes |
|---|---|---|---|---|---|
| match | act | act-zm-2013-007-the-excess-expenditure-appropriation-2010-2013 | www.parliament.gov.zm | parliament.gov.zm Act PDF | stable-PDF supercohort match |
| match | act | act-zm-2016-001-the-constitution-of-zambia | www.parliament.gov.zm | parliament.gov.zm Act PDF | stable-PDF supercohort match |
| drift | judgment | judgment-zm-2022-zmcc-02-lieutenant-muchindu-v-attorney-general | zambialii.org | AKN-HTML `eng@`-suffixed (`/akn/zm/judgment/zmcc/2022/2/eng@2022-01-27`) | `zambialii_akn_html_dynamic_render_drift` cohort (`eng@`-suffixed sub-variant; judgment-HTML) |
| drift | act | act-zm-1939-029-trading-with-the-enemy-act-1939 | zambialii.org | AKN-HTML `eng@`-suffixed (`/akn/zm/act/1939/29/eng@1996-12-31`) | `zambialii_akn_html_dynamic_render_drift` cohort (`eng@`-suffixed sub-variant) |
| match | act | loz-mines-and-minerals-act | www.parliament.gov.zm | parliament.gov.zm Act PDF | stable-PDF supercohort match |
| match | act | act-zm-2022-007-the-supplementary-appropriation-2022-act-2022 | www.parliament.gov.zm | parliament.gov.zm Act PDF | stable-PDF supercohort match |
| match | act | act-zm-2000-021-estate-agents-act-no-21-of-2000 | www.parliament.gov.zm | parliament.gov.zm Act PDF | stable-PDF supercohort match |
| drift | act | act-zm-1968-034-loans-kafue-gorge-hydro-electric-power-project-act-1968 | zambialii.org | AKN-HTML `eng@`-suffixed (`/akn/zm/act/1968/34/eng@1996-12-31`) | `zambialii_akn_html_dynamic_render_drift` cohort (`eng@`-suffixed sub-variant) |

The b0715 sample composition: 5/8 parliament.gov.zm Act PDFs and 3/8 zambialii.org AKN-HTML `eng@`-suffixed pages (2 acts + 1 judgment). All 5 parliament.gov.zm PDFs matched (stable-PDF supercohort behaviour). All 3 zambialii.org AKN-HTML `eng@`-suffixed records drifted (`zambialii_akn_html_dynamic_render_drift` cohort — known server-rendered timestamp / asset cache-busting behaviour; not substantive legal-text change).

Overall match rate this tick (5/8 = 62.5%) is between b0712 (6/8 = 75%) and b0714 (2/8 = 25%); the swing is purely a function of sample composition under the b0715 seed (5/8 records drawn from the stable-PDF supercohort) and not a corpus-health signal. Cumulative Phase 8 telemetry across recent ticks remains in line with the documented per-URL-kind hit rates (parliament.gov.zm PDFs ≈100% match; zambialii.org `source.pdf` ≈100% match; AKN-HTML `eng@`-suffixed ≈100% drift; AKN landing/bare-path HTML ≈100% drift).

## Integrity checks

| # | Check | Result |
|---|---|---|
| 1 | JSON report well-formed; match+drift+fetch_error == sample_size (5+3+0=8) | PASS |
| 2 | No duplicate IDs in sample (8 unique) | PASS |
| 3 | Every stored + fetched sha256 is a valid 64-hex sha256 | PASS |
| 4 | Every sampled record's `stored_sha256` matches the on-disk record's `source_hash` (proper `sha256:` prefix-stripping) | PASS (no record file mutated this tick) |
| 5 | No tracked record file modified by this run (script is read-only) | PASS (`git diff --stat records/` empty pre-commit) |
| 6 | `corpus.sqlite` NOT touched; `approvals.yaml` NOT modified | PASS (`git diff --stat corpus.sqlite approvals.yaml` empty) |
| 7 | robots.txt respected; per-host rate limits honoured (zambialii.org min_gap ≥ 5s; deterministic `sleep_for_host` mechanism unchanged from baseline) | PASS |
| 8 | User-Agent honest: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` | PASS |
| 9 | corpus.sqlite live `quick_check=ok records=1962 records_fts=1962 dup_ids=0` (baseline parity preserved across tick) | PASS |

All 9 checks PASS — tick commits via normal path.

## Cost / budget

- Network fetches this tick: 8 (all HTTP 200)
- Cumulative daily fetches across all workers today (per costs.log fetches= sum): ~405 pre-tick; + 8 (this tick) = ~413 of 2000 daily budget. Plenty of headroom.
- Tokens consumed: 0 (deterministic pipeline, no LLM calls). LLM budget 0/1,000,000 today.
- Bandwidth: 2,566,398 bytes total (~2.5 MB); largest = `loz-mines-and-minerals-act` (1,415,405 B, parliament.gov.zm PDF — Mines and Minerals Act PDF dominated bandwidth this tick).
- Wall clock: 21s (budget 20min; headroom ~19m39s).

## B2 sync

Deferred to host — rclone not available in sandbox. Phase 8 is read-only on corpus (no `raw/` mutation) so deferral is acceptable per BRIEF.md §8.

## Next tick

Routine Phase 8 sampling continues. No new audit-trail items spawned this tick — all 3 drifts fall under the pre-existing `zambialii_akn_html_dynamic_render_drift` cohort. Pre-existing carry-forwards remain:
- `judgment-zm-2025-zmcc-14` canonical-URL-date variant 404 (b0700 — audit-only; remediation requires explicit Peter approval).
- Existing 15 `parliament-pdf-v1.2` truncated-16hex defect records remain an open operator-triage item (latent — not drawn this tick).
