# Phase 8 — Nightly Re-verification — batch 0712

- **Phase:** `phase_8_nightly_reverify`
- **Worker run id:** `b0712-phase8`
- **Script:** `scripts/batch_0712_phase8_reverify.py` (clone of frozen baseline `scripts/batch_0546_phase8_reverify.py`; only `BATCH` constant and docstring header differ from `scripts/batch_0711_phase8_reverify.py`)
- **Parser version:** `phase8-reverify-0.1.0`
- **Seed:** `phase8-reverify-2026-05-18-b0712`
- **Started:** `2026-05-18T18:37:16Z`
- **Completed:** `2026-05-18T18:37:51Z`
- **Wall clock:** 35s (budget 20min; headroom ~19m25s)
- **Pool size:** 1964 records (records/**/*.json with both `source_url` + `source_hash`) — unchanged from b0711 (`pool_size=1964`); no insertions or removals since prior Phase 8 tick. corpus.sqlite live count remains 1961 (3 records-without-source_hash are excluded from the Phase 8 pool by design).
- **Sample size:** 8 (`sample_rate 0.01`, capped at `MAX_BATCH=8`)
- **Fetches:** 8 (all HTTP 200)
- **Outcome counts:** match=6, drift=2, fetch_error=0
- **B2 sync:** deferred to host (rclone not in sandbox; Phase 8 is read-only on corpus — no `raw/` mutation)

## Results

| Verdict | Type | ID | Source host | URL kind | Notes |
|---|---|---|---|---|---|
| match | act | kasama-municipal-council-vehicle-loading-and-parking-levy-by-laws-2021 | zambialii.org | AKN `source.pdf` | stable-PDF supercohort match (ZambiaLII source.pdf sub-variant) |
| match | act | act-zm-2025-011-customs-exciseamendmentact | www.parliament.gov.zm | parliament.gov.zm Act PDF | stable-PDF supercohort match |
| match | si | si-zm-2003-022-postal-services-courier-service-licence-regulations-2003 | zambialii.org | AKN `source.pdf` | stable-PDF supercohort match |
| match | act | act-zm-2017-003-compulsory-standards | www.parliament.gov.zm | parliament.gov.zm Act PDF | stable-PDF supercohort match |
| match | si | si-zm-2013-012-education-district-education-offices-establishment-order-2013 | zambialii.org | AKN `source.pdf` | stable-PDF supercohort match |
| drift | judgment | judgment-zm-2024-zmsc-23-stephen-mwape-v-the-people | zambialii.org | AKN-HTML `eng@`-suffixed | `zambialii_akn_html_dynamic_render_drift` cohort |
| drift | statutory_instrument | si-zm-2017-060-urban-and-regional-planning-designated-local-planning-authorities-regulations-2017 | zambialii.org | AKN landing HTML (no `eng@`, no `source.pdf`) | `zambialii_akn_html_dynamic_render_drift` cohort |
| match | judgment | judgment-zm-2025-zmsc-30-sa-v-zambia | zambialii.org | AKN `source.pdf` | stable-PDF supercohort match (11,310,547 B — heaviest single fetch this tick) |

The b0712 sample composition: 6/8 ZambiaLII (4 `source.pdf` PDFs + 2 dynamic-HTML AKN pages) and 2/8 parliament.gov.zm Act PDFs. All 6 stable-PDF records matched (4 ZambiaLII `source.pdf` + 2 parliament.gov.zm PDF). Both drifts are dynamic-HTML URL kinds on ZambiaLII: one `eng@`-suffixed AKN-HTML judgment page and one AKN landing page (no `eng@`, no `source.pdf`). Per-URL-kind behaviour remains consistent with prior ticks (stable PDFs ≈100% match; dynamic HTML ≈100% drift due to server-rendered timestamps / asset cache-busting), so the drift verdicts here do NOT imply substantive legal-text change.

Overall match rate this tick (6/8 = 75%) matches b0711 (6/8 = 75%) and exceeds b0707/b0708 (3/8 each), reflecting heavier sampling of the stable-PDF supercohort under the b0712 seed — a function of sample composition, not corpus health. Cumulative Phase 8 telemetry across recent ticks remains in line with the documented per-URL-kind hit rates (parliament.gov.zm PDFs ≈100% match; zambialii.org `source.pdf` ≈100% match; AKN-HTML `eng@`-suffixed ≈100% drift; AKN landing HTML ≈100% drift).

## Integrity checks

| # | Check | Result |
|---|---|---|
| 1 | JSON report well-formed; match+drift+fetch_error == sample_size (6+2+0=8) | PASS |
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
- Cumulative daily fetches across all workers today (NETWORK_FETCHES count rows): b0707-phase8 (8) + b0707-jiw (26) + b0708-phase8 (8) + b0709-jiw (112) + b0710-jiw (155) + b0711-phase8 (8) = 317 pre-tick; + 8 (this tick) = ~325 of 2000 daily budget. Plenty of headroom.
- Tokens consumed: 0 (deterministic pipeline, no LLM calls). LLM budget 0/1,000,000 today.
- Bandwidth: 13,344,253 bytes total (~12.7 MB); largest = `judgment-zm-2025-zmsc-30-sa-v-zambia` (11,310,547 B, ZambiaLII `source.pdf` — single large SCZ judgment PDF dominated bandwidth this tick).
- Wall clock: 35s (budget 20min; headroom ~19m25s).

## B2 sync

Deferred to host — rclone not available in sandbox. Phase 8 is read-only on corpus (no `raw/` mutation) so deferral is acceptable per BRIEF.md §8.

## Next tick

Routine Phase 8 sampling continues. No new audit-trail items spawned this tick. Pre-existing carry-forwards remain:
- `judgment-zm-2025-zmcc-14` canonical-URL-date variant 404 (b0700 — audit-only; remediation requires explicit Peter approval).
- Existing 15 `parliament-pdf-v1.2` truncated-16hex defect records remain an open operator-triage item (latent — not drawn this tick).
