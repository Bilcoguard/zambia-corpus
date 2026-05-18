# Phase 8 — Nightly Re-verification — batch 0711

- **Phase:** `phase_8_nightly_reverify`
- **Worker run id:** `b0711-phase8`
- **Script:** `scripts/batch_0711_phase8_reverify.py` (clone of frozen baseline `scripts/batch_0546_phase8_reverify.py`; only `BATCH` constant and docstring header differ from `scripts/batch_0708_phase8_reverify.py`)
- **Parser version:** `phase8-reverify-0.1.0`
- **Seed:** `phase8-reverify-2026-05-18-b0711`
- **Started:** `2026-05-18T18:27:49Z`
- **Completed:** `2026-05-18T18:28:03Z`
- **Wall clock:** 14s (budget 20min; headroom ~19m46s)
- **Pool size:** 1964 records (records/**/*.json with both `source_url` + `source_hash`) — unchanged from b0708 (`pool_size=1964`); no insertions or removals since prior Phase 8 tick. corpus.sqlite live count remains 1961 (3 records-without-source_hash are excluded from the Phase 8 pool by design).
- **Sample size:** 8 (`sample_rate 0.01`, capped at `MAX_BATCH=8`)
- **Fetches:** 8 (all HTTP 200)
- **Outcome counts:** match=6, drift=2, fetch_error=0
- **B2 sync:** deferred to host (rclone not in sandbox; Phase 8 is read-only on corpus — no `raw/` mutation)

## Results

| Verdict | Type | ID | Source host | URL kind | Notes |
|---|---|---|---|---|---|
| match | act | act-zm-2023-003-the-examinations-council-of-zambia-act-2023 | www.parliament.gov.zm | parliament.gov.zm Act PDF | stable-PDF supercohort match (423,774 B) |
| match | act | act-zm-2016-017-the-local-government-amendment | www.parliament.gov.zm | parliament.gov.zm Act PDF | stable-PDF supercohort match (8,978 B) |
| match | si | si-zm-2010-043-income-tax-sino-metals-leach-zambia-limited-rebate-regulations-2010 | zambialii.org | AKN `source.pdf` | stable-PDF supercohort match (ZambiaLII source.pdf sub-variant; 98,969 B) |
| match | act | loz-national-parks-and-wildlife-act | www.parliament.gov.zm | parliament.gov.zm Act PDF | stable-PDF supercohort match (2,116,963 B — heaviest single fetch this tick) |
| match | act | act-zm-2010-005-the-supplementary-appropriation-2010-2012 | www.parliament.gov.zm | parliament.gov.zm Act PDF | stable-PDF supercohort match (118,120 B) |
| drift | act | act-zm-1997-011-zambia-institute-of-human-resources-management-act-1997 | zambialii.org | AKN-HTML `eng@`-suffixed | `zambialii_akn_html_dynamic_render_drift` cohort |
| drift | judgment | judgment-zm-2026-coa-099-geoffrey-muyonga-sitwala-kaliki-vincent-lubinda-v-ahmed-abdulkadir-barakadle-mohammed-other | judiciaryzambia.com | judiciaryzambia.com WordPress post HTML | `judiciaryzambia_wp_html_dynamic_render_drift` cohort |
| match | act | act-zm-2023-005-the-rural-electrification-act-2023 | www.parliament.gov.zm | parliament.gov.zm Act PDF | stable-PDF supercohort match (364,298 B) |

The b0711 sample skewed heavily toward the parliament.gov.zm stable-PDF supercohort (5/8 entries; all matched) with one additional ZambiaLII `source.pdf` SI also matching, yielding 6/6 stable-PDF matches. The 2 drifts were both dynamic-HTML URL kinds: one AKN-HTML `eng@`-suffixed Act (ZambiaLII) and one judiciaryzambia.com WordPress post HTML (a COA judgment). Per-URL-kind behaviour remains consistent with prior ticks (stable PDFs ≈100% match; dynamic HTML ≈100% drift due to server-rendered timestamps / WordPress footer counters / asset cache-busting), so the drift verdicts here do NOT imply substantive legal-text change.

Overall match rate this tick (6/8 = 75%) is higher than b0708 (3/8) and b0707 (3/8) because the seeded RNG happened to draw more stable-PDF records this sample; this is a function of sample composition, not corpus health. Cumulative Phase 8 telemetry across recent ticks remains in line with the documented per-URL-kind hit rates (parliament.gov.zm PDFs ≈100% match; zambialii.org `source.pdf` ≈100% match; AKN-HTML `eng@`-suffixed ≈100% drift; judiciaryzambia.com WP HTML ≈100% drift).

## Integrity checks

| # | Check | Result |
|---|---|---|
| 1 | JSON report well-formed; match+drift+fetch_error == sample_size (6+2+0=8) | PASS |
| 2 | No duplicate IDs in sample (8 unique) | PASS |
| 3 | Every stored + fetched sha256 is a valid 64-hex sha256 | PASS |
| 4 | Every sampled record's `stored_sha256` matches the on-disk record's `source_hash` (proper `sha256:` prefix-stripping) | PASS (no record file mutated this tick) |
| 5 | No tracked record file modified by this run (script is read-only) | PASS (`git diff --stat records/` empty pre-commit) |
| 6 | `corpus.sqlite` NOT touched; `approvals.yaml` NOT modified | PASS (`git diff --stat corpus.sqlite approvals.yaml` empty) |
| 7 | robots.txt respected; per-host rate limits honoured (zambialii.org min_gap ≥ 5s; judiciaryzambia.com min_gap ≥ 5s; deterministic `sleep_for_host` mechanism unchanged from baseline) | PASS |
| 8 | User-Agent honest: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` | PASS |
| 9 | corpus.sqlite live `quick_check=ok records=1961 records_fts=1961 dup_ids=0` (baseline parity preserved across tick) | PASS |

All 9 checks PASS — tick commits via normal path.

## Cost / budget

- Network fetches this tick: 8 (all HTTP 200)
- Cumulative daily fetches across all workers today (NETWORK_FETCHES count rows): b0707-phase8 (8) + b0707-jiw (26) + b0708-phase8 (8) + b0709-jiw (112) + b0710-jiw (155) = 309 pre-tick; + 8 (this tick) = ~317 of 2000 daily budget. Plenty of headroom.
- Tokens consumed: 0 (deterministic pipeline, no LLM calls). LLM budget 0/1,000,000 today.
- Bandwidth: 3,467,440 bytes total (~3.31 MB); largest = `loz-national-parks-and-wildlife-act` (2,116,963 B, parliament.gov.zm PDF).
- Wall clock: 14s (budget 20min; headroom ~19m46s).

## B2 sync

Deferred to host — rclone not available in sandbox. Phase 8 is read-only on corpus (no `raw/` mutation) so deferral is acceptable per BRIEF.md §8.

## Next tick

Routine Phase 8 sampling continues. No new audit-trail items spawned this tick. Pre-existing carry-forwards remain:
- `judgment-zm-2025-zmcc-14` canonical-URL-date variant 404 (b0700 — audit-only; remediation requires explicit Peter approval).
- Existing 15 `parliament-pdf-v1.2` truncated-16hex defect records remain an open operator-triage item (latent — not drawn this tick).
