# Phase 8 — Nightly Re-verification — batch 0714

- **Phase:** `phase_8_nightly_reverify`
- **Worker run id:** `b0714-phase8`
- **Script:** `scripts/batch_0714_phase8_reverify.py` (clone of frozen baseline `scripts/batch_0546_phase8_reverify.py`; only `BATCH` constant and docstring header differ from `scripts/batch_0712_phase8_reverify.py`)
- **Parser version:** `phase8-reverify-0.1.0`
- **Seed:** `phase8-reverify-2026-05-18-b0714`
- **Started:** `2026-05-18T19:04:03Z`
- **Completed:** `2026-05-18T19:04:45Z`
- **Wall clock:** 42s (budget 20min; headroom ~19m18s)
- **Pool size:** 1965 records (records/**/*.json with both `source_url` + `source_hash`) — up by +1 from b0712 (`pool_size=1964`) reflecting the net b0713-jiw + b0713-jiw-cleanup change (2 records inserted, 1 deduped). corpus.sqlite live count is 1962 (delta to pool is unchanged: 3 records-without-source_hash continue to be excluded from the Phase 8 pool by design).
- **Sample size:** 8 (`sample_rate 0.01`, capped at `MAX_BATCH=8`)
- **Fetches:** 8 (all HTTP 200)
- **Outcome counts:** match=2, drift=6, fetch_error=0
- **B2 sync:** deferred to host (rclone not in sandbox; Phase 8 is read-only on corpus — no `raw/` mutation)

## Results

| Verdict | Type | ID | Source host | URL kind | Notes |
|---|---|---|---|---|---|
| drift | act | act-zm-1964-036-apprenticeship-act-1964 | zambialii.org | AKN-HTML `eng@`-suffixed (`/akn/zm/act/1964/36/eng@1996-12-31`) | `zambialii_akn_html_dynamic_render_drift` cohort (`eng@`-suffixed sub-variant) |
| match | judgment | judgment-zm-2026-zmsc-10-first-v-zubao | zambialii.org | ZambiaLII `source.pdf` (`/akn/zm/judgment/zmsc/2026/10/eng@2026-04-17/source.pdf`) | stable-PDF supercohort (ZambiaLII source.pdf sub-variant) |
| drift | judgment | judgment-zm-2018-zmcc-01-chilombo-v-hamaleke | zambialii.org | AKN-HTML `eng@`-suffixed (`/akn/zm/judgment/zmcc/2018/1/eng@2018-01-18`) | `zambialii_akn_html_dynamic_render_drift` cohort (`eng@`-suffixed sub-variant; judgment-HTML) |
| drift | statutory_instrument | si-zm-2020-087-animal-health-designated-border-inspection-posts-regulations-2020 | zambialii.org | AKN bare-path (`/akn/zm/act/si/2020/87`; no `/eng@`, no `/source.pdf`) | `zambialii_akn_html_dynamic_render_drift` cohort (bare-AKN-path sub-variant) |
| drift | statutory_instrument | si-zm-2022-051-electoral-process-local-government-by-elections-election-date-and-time-of-poll-order-2022 | zambialii.org | AKN bare-path (`/akn/zm/act/si/2022/51`) | `zambialii_akn_html_dynamic_render_drift` cohort (bare-AKN-path sub-variant) |
| drift | act | act-zm-2002-018-supplementary-appropriation-1999-act | zambialii.org | AKN-HTML `eng@`-suffixed (`/akn/zm/act/2002/18/eng@2002-12-31`) | `zambialii_akn_html_dynamic_render_drift` cohort (`eng@`-suffixed sub-variant) |
| drift | act | act-zm-2000-019-arbitration-act-2000 | zambialii.org | AKN-HTML `eng@`-suffixed (`/akn/zm/act/2000/19/eng@2000-12-29`) | `zambialii_akn_html_dynamic_render_drift` cohort (`eng@`-suffixed sub-variant) |
| match | act | act-zm-2019-017-supplementary-appropriation-2019-no-2-act-2019 | www.parliament.gov.zm | parliament.gov.zm Act PDF | stable-PDF supercohort match |

The b0714 sample composition: 7/8 zambialii.org (1 `source.pdf` PDF + 6 dynamic-HTML AKN pages; 4 `eng@`-suffixed + 2 bare-path) and 1/8 parliament.gov.zm Act PDF. Both stable-PDF records matched (1 ZambiaLII `source.pdf` + 1 parliament.gov.zm PDF). All 6 dynamic-HTML AKN records drifted — 4 `eng@`-suffixed (3 acts + 1 judgment) and 2 bare-AKN-path SIs. Per-URL-kind behaviour remains consistent with all prior Phase 8 ticks (stable PDFs ≈100% match; dynamic HTML ≈100% drift due to server-rendered timestamps / asset cache-busting), so the drift verdicts here do NOT imply substantive legal-text change.

Overall match rate this tick (2/8 = 25%) is below b0712 (6/8 = 75%) and b0711 (6/8 = 75%); the swing is purely a function of sample composition under the b0714 seed (only 2/8 records drawn from the stable-PDF supercohort) and not a corpus-health signal. Cumulative Phase 8 telemetry across recent ticks remains in line with the documented per-URL-kind hit rates (parliament.gov.zm PDFs ≈100% match; zambialii.org `source.pdf` ≈100% match; AKN-HTML `eng@`-suffixed ≈100% drift; AKN landing/bare-path HTML ≈100% drift).

## Integrity checks

| # | Check | Result |
|---|---|---|
| 1 | JSON report well-formed; match+drift+fetch_error == sample_size (2+6+0=8) | PASS |
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
- Cumulative daily fetches across all workers today (per costs.log fetches= sum): ~397 pre-tick; + 8 (this tick) = ~405 of 2000 daily budget. Plenty of headroom.
- Tokens consumed: 0 (deterministic pipeline, no LLM calls). LLM budget 0/1,000,000 today.
- Bandwidth: 589,757 bytes total (~576 KB); largest = `judgment-zm-2026-zmsc-10-first-v-zubao` (224,515 B, ZambiaLII `source.pdf` — SCZ judgment PDF dominated bandwidth this tick).
- Wall clock: 42s (budget 20min; headroom ~19m18s).

## B2 sync

Deferred to host — rclone not available in sandbox. Phase 8 is read-only on corpus (no `raw/` mutation) so deferral is acceptable per BRIEF.md §8.

## Next tick

Routine Phase 8 sampling continues. No new audit-trail items spawned this tick. Pre-existing carry-forwards remain:
- `judgment-zm-2025-zmcc-14` canonical-URL-date variant 404 (b0700 — audit-only; remediation requires explicit Peter approval).
- Existing 15 `parliament-pdf-v1.2` truncated-16hex defect records remain an open operator-triage item (latent — not drawn this tick).
