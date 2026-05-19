# Batch 0732 — Phase 8 nightly re-verification

- **Tick**: b0732-phase8
- **Started**: 2026-05-19T16:07:14Z
- **Completed**: 2026-05-19T16:07:49Z
- **Seed**: `phase8-reverify-2026-05-19-b0732`
- **Parser**: `phase8-reverify-0.1.0`
- **Pool**: 2022 records (sample_rate 0.01, max_batch 8)
- **Sample**: 8 records (1× SI source.pdf, 2× parliament.gov.zm static PDF — well, 1 SI + 1 act PDF actually, 4× ZambiaLII AKN-HTML eng@-suffixed, 1× ZambiaLII non-AKN slug)
- **Verdicts**: 3 match, 4 drift, 1 fetch_error
- **Integrity**: 9/9 PASS
- **Records mutated**: 0 (Phase 8 is read-only)
- **Fetches today (cumulative)**: 24 / 2000

## Outcome
Audit-only tick. Drift cohort breakdown:
- 3× `zambialii_akn_html_dynamic_render_drift` (eng@-suffixed sub-variant; 2× `eng@1996-12-31` consolidated-snapshot, 1× `eng@2006-03-31` point-in-time)
- 1× `parliament_gov_zm_acts_pdf_stored_hash_truncated` (carry-forward of known data-quality issue on `act-zm-2020-018-zambia-academy-of-sciences-act-2020` — fetched hash matches 16-char stored prefix exactly, confirming upstream byte-stability; the drift is solely the truncated stored hash)

Fetch error:
- 1× NEW carry-forward audit item: `judgment-zm-2022-zmsc-53-stella-mumba-chibanda-and-ors-v-the-people` returns HTTP 404 at its stored source_url. The URL is non-AKN (root-path slug rather than `/akn/zm/judgment/zmsc/2022/53/...`), suggesting a JIW worker URL-construction anomaly at ingest time (record was added today by b0726-jiw at 09:11:54Z). Flagged audit-only; remediation out of scope for Phase 8.

All other carry-forward audit items (`judgment-zm-2024-coa-024-kingfred-phiri-v-life-master-ltd`, `judgment-zm-2025-zmcc-14`) were not in this tick's sample.

## Provenance
- Report JSON: `reports/batch-0732-reverify.json`
- Audit entries: `gaps.md` §"b0732-phase8 — Phase 8 nightly re-verification" + `gaps.md` §"phase8_reverify_drift" (batch 0732)
- Script: `scripts/batch_0732_phase8_reverify.py` (clone of frozen baseline `scripts/batch_0546_phase8_reverify.py`; only BATCH constant changed)
