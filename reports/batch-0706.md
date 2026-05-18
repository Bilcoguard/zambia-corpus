# Phase 8 — Nightly Re-verification — batch 0706

- **Phase:** `phase_8_nightly_reverify`
- **Worker run id:** `b0706-phase8`
- **Script:** `scripts/batch_0706_phase8_reverify.py`
- **Parser version:** `phase8-reverify-0.1.0`
- **Seed:** `phase8-reverify-2026-05-18-b0706`
- **Started:** `2026-05-18T15:03:52Z`
- **Completed:** `2026-05-18T15:04:26Z`
- **Wall clock:** 34s (budget 20min; headroom ~19m26s)
- **Pool size:** 1961 records (records/**/*.json with both source_url + source_hash)
- **Sample size:** 8 (sample_rate 0.01, capped at MAX_BATCH=8)
- **Fetches:** 8
- **Outcome counts:** match=1, drift=7, fetch_error=0
- **B2 sync:** deferred to host (rclone not in sandbox; Phase 8 is read-only on corpus — no `raw/` mutation)

## Results

| Verdict | Type | ID | Source host | URL kind | Notes |
|---|---|---|---|---|---|
| drift | judgment | judgment-zm-2019-zmcc-20-chama-mutambalilo-v-attorney-general | zambialii.org | AKN-HTML `eng@`-suffixed | `zambialii_akn_html_dynamic_render_drift` cohort |
| drift | act | act-zm-1989-031-supplementary-appropriation-1988-act | zambialii.org | AKN-HTML `eng@`-suffixed | `zambialii_akn_html_dynamic_render_drift` cohort |
| drift | act | act-zm-1992-013-casino-act-1992 | zambialii.org | AKN-HTML `eng@`-suffixed | `zambialii_akn_html_dynamic_render_drift` cohort |
| drift | act | act-zm-1967-026-law-reform-miscellaneous-provisions-act-1967 | zambialii.org | AKN-HTML `eng@`-suffixed | `zambialii_akn_html_dynamic_render_drift` cohort (re-sampled; same drift family as b0700) |
| drift | statutory_instrument | si-zm-1995-030-national-archives-place-of-deposit-revocation-order-1995 | zambialii.org | AKN bare-path (no `/eng@`, no `/source.pdf`) | `zambialii_akn_html_dynamic_render_drift` (bare-AKN-path sub-variant) |
| match | act | act-zm-2026-008-agricultural-marketing-act | www.parliament.gov.zm | parliament.gov.zm Act PDF | stable-PDF supercohort match |
| drift | judgment | judgment-zm-2026-coa-231-lisboa-casino-limited-v-director-of-public-prosecutions | judiciaryzambia.com | WordPress single-post HTML | `judiciaryzambia_html_dynamic_render_drift` cohort |
| drift | act | act-zm-2021-053-appropriation-act | zambialii.org | AKN-HTML `eng@`-suffixed | `zambialii_akn_html_dynamic_render_drift` cohort |

This tick the sample drew heavily from the dynamic-rendered HTML cohort: 6 of 8 URLs were ZambiaLII AKN-HTML variants (5× `eng@`-suffixed and 1× bare-AKN-path) and 1 was a judiciaryzambia.com WordPress single-post page. All 7 of those drifted — exactly as expected for the documented dynamic-render cohorts. AKN-HTML pages embed server-rendered timestamps and footer counters, and the judiciaryzambia.com WordPress template embeds equivalent dynamic markup (Yoast SEO meta, JSON-LD `dateModified`, share-counter widgets), so byte-level hash drift is the expected behaviour for these URL forms and does NOT imply substantive legal-text change.

The single match is the **stable-PDF supercohort** member from www.parliament.gov.zm (Agricultural Marketing Act No. 8 of 2026, 401,831 bytes) — confirming the parliament.gov.zm Act-PDF supercohort remains 100% stable across this tick's sample.

Drift rate this tick (7/8 = 87.5%) is high but reflects sample composition rather than corpus health: 7 of 8 URLs drawn were dynamic-rendered HTML (where ≈100% drift is expected) and only 1 was a stable PDF (which matched). Per-URL-kind hit rates remain consistent with prior ticks (AKN-HTML ≈100% drift; judiciaryzambia.com WordPress single-post ≈100% drift; stable PDFs ≈100% match → 7/7 dynamic-HTML drift + 1/1 stable-PDF match).

No new sub-cohort was spawned. All drifts slot into the two pre-existing dynamic-render cohorts (`zambialii_akn_html_dynamic_render_drift` and `judiciaryzambia_html_dynamic_render_drift`). The `act-zm-1967-026` record was also drawn in b0700; same stored sha and same fetched-hash family (each fetch yields a slightly different byte sequence due to the embedded timestamp, but the cohort verdict is identical).

## Integrity checks

| # | Check | Result |
|---|---|---|
| 1 | JSON report well-formed; match+drift+fetch_error == sample_size (1+7+0=8) | PASS |
| 2 | No duplicate IDs in sample (8 unique) | PASS |
| 3 | Every stored + fetched sha256 is a valid 64-hex sha256 | PASS |
| 4 | Every sampled record's stored_sha256 matches the on-disk record's `source_hash` (proper `sha256:` prefix-stripping) | PASS (no record file mutated this tick) |
| 5 | No tracked record file modified by this run (script is read-only) | PASS (`git diff --stat records/` empty pre-commit) |
| 6 | corpus.sqlite NOT touched; approvals.yaml NOT modified | PASS (`git diff --stat corpus.sqlite approvals.yaml` empty) |
| 7 | robots.txt respected; per-host rate limits honoured (zambialii.org min_gap ≥ 5s; deterministic `sleep_for_host` mechanism unchanged from baseline) | PASS |
| 8 | User-Agent honest: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` | PASS |
| 9 | corpus.sqlite live `quick_check=ok records=1958 records_fts=1958 dup_ids=0` (baseline parity preserved across tick) | PASS |

All 9 checks PASS — tick commits via normal path.

## Cost / budget

- Network fetches this tick: 8 (all HTTP 200)
- Cumulative daily fetches (main + jiw, approx): ~153 (pre-tick) + 8 (this tick) ≈ ~161 of 2000 daily budget
- Tokens consumed: 0 (deterministic pipeline, no LLM calls)
- Bandwidth: 990,335 bytes total (~0.97 MB); largest = act-zm-2026-008-agricultural-marketing-act (401,831 bytes parliament.gov.zm PDF)
- Wall clock: 34s (budget 20min; headroom ~19m26s)

## B2 sync

Deferred to host — rclone not available in sandbox. Phase 8 is read-only on corpus (no `raw/` mutation) so deferral is acceptable per BRIEF.md §8.

## Next tick

Routine Phase 8 sampling continues. No new audit-trail items spawned this tick. Pre-existing carry-forwards remain:
- `judgment-zm-2025-zmcc-14` canonical-URL-date variant 404 (b0700 — audit-only; remediation requires explicit Peter approval).
- Existing 15 `parliament-pdf-v1.2` truncated-16hex defect records remain an open operator-triage item (latent — not drawn this tick).
