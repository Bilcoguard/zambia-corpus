# Phase 8 — Nightly Re-verification — batch 0704

- **Phase:** `phase_8_nightly_reverify`
- **Worker run id:** `b0704-phase8`
- **Script:** `scripts/batch_0704_phase8_reverify.py`
- **Parser version:** `phase8-reverify-0.1.0`
- **Seed:** `phase8-reverify-2026-05-18-b0704`
- **Started:** `2026-05-18T14:06:11Z`
- **Completed:** `2026-05-18T14:06:32Z`
- **Wall clock:** 21s (budget 20min; headroom ~19m39s)
- **Pool size:** 1957 records (records/**/*.json with both source_url + source_hash)
- **Sample size:** 8 (sample_rate 0.01, capped at MAX_BATCH=8)
- **Fetches:** 8
- **Outcome counts:** match=7, drift=1, fetch_error=0
- **B2 sync:** deferred to host (rclone not in sandbox; Phase 8 is read-only on corpus — no `raw/` mutation)

## Results

| Verdict | Type | ID | Source host | URL kind | Notes |
|---|---|---|---|---|---|
| match | si | si-zm-2023-033-national-heritage-conservation-commission-ngonye-falls-national-monument-declara | zambialii.org | AKN `source.pdf` | stable-PDF supercohort match |
| match | act | act-zm-2023-015-the-zambia-institute-of-marketing-amendment-act-2023 | www.parliament.gov.zm | parliament.gov.zm Act PDF | stable-PDF supercohort match |
| match | si | si-zm-2021-108-income-tax-turnover-tax-amendment-regulations-2021 | zambialii.org | AKN `source.pdf` | stable-PDF supercohort match |
| match | act | act-zm-2010-020-the-plea-negotiations-and-agreements-2010 | www.parliament.gov.zm | parliament.gov.zm Act PDF | stable-PDF supercohort match |
| drift | statutory_instrument | si-zm-1982-049-zambia-airways-corporation-date-of-dissolution-order-1982 | zambialii.org | AKN bare-path (no `/eng@`, no `/source.pdf`) | dynamic-render cohort (bare-AKN-path variant) |
| match | act | act-zm-2015-004-the-forest-act | www.parliament.gov.zm | parliament.gov.zm Act PDF | stable-PDF supercohort match |
| match | act | act-zm-2024-011-the-civil-aviation-amendment-act-2024 | www.parliament.gov.zm | parliament.gov.zm Act PDF | stable-PDF supercohort match |
| match | act | act-zm-cap-262-ministerial-and-parliamentary-offices-emoluments-act | www.parliament.gov.zm | parliament.gov.zm Act PDF | stable-PDF supercohort match |

The single drift is the **`zambialii_akn_html_dynamic_render_drift`** cohort — bare AKN identifier path (`/akn/zm/act/si/1982/49`, no `/eng@` date-suffix and no `/source.pdf` suffix), which 302-redirects to the latest English point-in-time HTML rendering. AKN-HTML pages embed dynamic-rendered markup (timestamps, footer counters) so byte-level hash drift is the expected behaviour for this URL form and does NOT imply substantive legal-text change. No new sub-cohort spawned; this slots into the existing `zambialii_akn_html_dynamic_render_drift` (bare-AKN-path sub-variant first documented in b0567).

All 7 match verdicts are the stable-PDF supercohort:
- 5× **www.parliament.gov.zm** Act PDFs (Zambia Institute of Marketing Amdt 2023; Plea Negotiations & Agreements 2010; Forest Act 2015; Civil Aviation Amdt 2024; CAP 262 Ministerial & Parliamentary Offices Emoluments) — confirms the parliament.gov.zm Act-PDF supercohort remains 100% stable.
- 2× **zambialii.org** AKN `source.pdf` (National Heritage Conservation SI 2023/33 Ngonye Falls; Income Tax Turnover Tax Amdt SI 2021/108) — confirms the AKN `source.pdf` stable-PDF cohort remains 100% stable.

Drift rate this tick (1/8 = 12.5%) reflects the sample composition: 1 AKN-HTML bare-path drew vs 7 stable-PDF URLs. Per-URL-kind hit rates match expectation (AKN-HTML bare-path ≈100% drift; stable PDFs ≈100% match → 1/1 AKN-HTML bare-path drift + 7/7 stable-PDF match).

## Integrity checks

| # | Check | Result |
|---|---|---|
| 1 | JSON report well-formed; match+drift+fetch_error == sample_size (7+1+0=8) | PASS |
| 2 | No duplicate IDs in sample (8 unique) | PASS |
| 3 | Every stored + fetched sha256 is a valid 64-hex sha256 | PASS |
| 4 | Every sampled record's stored_sha256 matches the on-disk record's `source_hash` (proper `sha256:` prefix-stripping) | PASS (no record file mutated this tick) |
| 5 | No tracked record file modified by this run (script is read-only) | PASS (`git diff --stat records/` empty pre-commit) |
| 6 | corpus.sqlite NOT touched; approvals.yaml NOT modified | PASS (`git diff --stat corpus.sqlite approvals.yaml` empty) |
| 7 | robots.txt respected; per-host rate limits honoured (zambialii.org min_gap ≥ 5s; deterministic `sleep_for_host` mechanism unchanged from baseline) | PASS |
| 8 | User-Agent honest: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` | PASS |
| 9 | corpus.sqlite live `quick_check=ok records=1954 records_fts=1954 dup_ids=0` (baseline parity preserved across tick) | PASS |

All 9 checks PASS — tick commits via normal path.

## Cost / budget

- Network fetches this tick: 8 (all HTTP 200)
- Cumulative daily fetches (main + jiw, approx): 8 (b0697) + 8 (b0698) + 8 (b0700) + 16 (b0701-jiw pre-curation) + 8 (b0704, this tick) ≈ ~153 of 2000 daily budget
- Tokens consumed: 0 (deterministic pipeline, no LLM calls)
- Bandwidth: 1,481,684 bytes total (~1.4 MB); largest = act-zm-2024-011-the-civil-aviation-amendment-act-2024 (317,204 bytes parliament.gov.zm PDF)
- Wall clock: 21s (budget 20min; headroom ~19m39s)

## B2 sync

Deferred to host — rclone not available in sandbox. Phase 8 is read-only on corpus (no `raw/` mutation) so deferral is acceptable per BRIEF.md §8.

## Next tick

Routine Phase 8 sampling continues. No new audit-trail items spawned this tick. Pre-existing carry-forwards remain:
- `judgment-zm-2025-zmcc-14` canonical-URL-date variant 404 (b0700 — audit-only; remediation requires explicit Peter approval).
- Existing 15 `parliament-pdf-v1.2` truncated-16hex defect records remain an open operator-triage item (latent — not drawn this tick).
