# Phase 8 batch 0697 — Nightly re-verification

- **Tick:** b0697-phase8
- **Phase:** phase_8_nightly_reverify (approvals.yaml — approved: true, complete: false, sample_rate: 0.01)
- **Parser/fetcher version:** phase8-reverify-0.1.0
- **Script:** `scripts/batch_0697_phase8_reverify.py` (verbatim clone of `scripts/batch_0690_phase8_reverify.py`; only the `BATCH` constant changed `"0690"` → `"0697"`; same logic as b0625/b0641/…/b0687/b0689/b0690)
- **Seed:** `phase8-reverify-2026-05-18-b0697`
- **Started:** 2026-05-18T11:58:32Z
- **Completed:** 2026-05-18T11:59:14Z
- **Wall clock:** ~42s (well within 20-minute budget)
- **Predecessor:** b0690-phase8 (pool_size 1939). Pool grew to 1949 via intervening commits b0691 (logs-only, no records), b0694 (repair: +8 SI records re-added with body), b0695 (repair: +8 SI body repairs; JIW: +3 ZMCC 2025 records), b0696-jiw (+7 ZMCC reparse). Net record-file delta: 1949 − 1939 = +10 (b0694: +8 net, b0696-jiw: +7 net minus existing-id reparses).
- **Verdict:** **tick-complete — all 9 integrity checks PASS — COMMIT (normal path)**

## Sample

| Metric | Value |
|---|---|
| pool_size | 1949 |
| sample_size | 8 |
| sample_rate | 0.01 |
| max_batch | 8 |
| fetches | 8 |
| match | 2 |
| drift | 6 |
| fetch_error | 0 |

All 8 fetches returned HTTP 200 — the zambialii.org HTTP 500 outage observed in b0691/b0692 (started 2026-05-18T01:14:50Z) has resolved.

b0697 did **not** draw any of the 15 `parliament-pdf-v1.2` truncated-16hex defect records — CHECK #3 PASSES this tick on seed-luck alone. The latent 15-record cohort remains an open operator-triage item (carry-over from b0670 diagnosis).

## Results

| Verdict | Type | ID | Source host | URL kind | Notes |
|---|---|---|---|---|---|
| drift | judgment | judgment-zm-2022-zmcc-05-moyo-v-attorney-general | zambialii.org | AKN-HTML `eng@`-suffixed | dynamic-render cohort |
| match | si | si-zm-2019-029-employment-code-act-commencement-order-2019 | zambialii.org | AKN source.pdf | stable-PDF supercohort match |
| match | act | act-zm-2021-041-electronic-government-act-2021 | media.zambialii.org | source_file PDF | stable-PDF supercohort match |
| drift | act | act-zm-1965-056-prisons-act-1965 | zambialii.org | AKN-HTML `eng@`-suffixed | dynamic-render cohort |
| drift | act | act-zm-1954-037-african-war-memorial-fund-act-1954 | zambialii.org | AKN-HTML `eng@`-suffixed | dynamic-render cohort |
| drift | act | act-zm-1968-005-gwembe-district-special-fund-dissolution-act-1968 | zambialii.org | AKN-HTML `eng@`-suffixed | dynamic-render cohort |
| drift | statutory_instrument | si-zm-2020-108-urban-and-regional-planning-designated-local-planning-authorities-no-3-regulations-2020 | zambialii.org | AKN-HTML bare (no `eng@`) | dynamic-render cohort |
| drift | statutory_instrument | si-zm-2019-042-urban-and-regional-planning-designated-local-planning-authorities-regulations-2019 | zambialii.org | AKN-HTML bare (no `eng@`) | dynamic-render cohort |

All 6 drift verdicts are textbook `zambialii_akn_html_dynamic_render_drift` cohort — AKN-HTML landing pages whose dynamic-rendered HTML carries embedded timestamps/footer counters that change between fetches. Both `eng@`-suffixed and bare-`/akn/...` variants are represented. No new sub-cohort spawned.

Both match verdicts are stable-PDF supercohort: 1× zambialii AKN source.pdf + 1× media.zambialii.org source_file PDF. Consistent with the supercohort's near-100% match rate across the Phase 8 series.

Drift rate this tick (6/8 = 75%) is elevated because the seed drew 6 ZambiaLII AKN-HTML candidates (whose dynamic-render cohort has ≈100% drift rate) and only 2 PDFs (whose stable-PDF supercohort has ≈100% match rate). This is consistent with the Phase 8 series long-run cohort-mix expectation and does not indicate any change in source-content stability.

## Integrity checks

| # | Check | Result |
|---|---|---|
| 1 | JSON report well-formed; match+drift+fetch_error == sample_size (2+6+0=8) | PASS |
| 2 | No duplicate IDs in sample (8 unique) | PASS |
| 3 | Every stored_sha256 + fetched_sha256 is a valid 64-hex sha256 (fetch_error rows have null fetched_sha256 by spec — none this tick) | **PASS** — seed did not draw any of the 15 truncated-16hex records this tick |
| 4 | Every sampled record's stored_sha256 matches the on-disk record's `source_hash` (proper `sha256:` prefix-stripping) | PASS (no record file mutated this tick) |
| 5 | No tracked record file modified by this run (script is read-only) | PASS (`git diff --stat records/` empty) |
| 6 | corpus.sqlite NOT touched; approvals.yaml NOT modified | PASS (`git diff --stat corpus.sqlite approvals.yaml` empty) |
| 7 | robots.txt respected; per-host rate limits honoured (zambialii.org min_gap ≥ 5s; deterministic `sleep_for_host` mechanism unchanged from baseline) | PASS |
| 8 | User-Agent honest: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` | PASS |
| 9 | corpus.sqlite live `quick_check=ok records=1946 records_fts=1946 dup_ids=0` (baseline parity preserved across tick) | PASS |

## Cost / budget

- Network fetches this tick: 8 (all HTTP 200; 6× zambialii.org AKN-HTML, 1× zambialii.org AKN source.pdf, 1× media.zambialii.org source_file PDF)
- Cumulative daily fetches: well under 2000/day budget (b0691: 81, b0692: 0, b0693-jiw: probe-only, b0694: ~16, b0695: ~16, b0696-jiw: 0, b0697: 8 → ≈121 of 2000)
- Tokens consumed: 0 (deterministic pipeline, no LLM calls)
- Bandwidth: 985,826 bytes total (~963 KB); largest = act-zm-1965-056-prisons-act-1965 (619,495 bytes)
- Wall clock: 42s (budget 20min; headroom ~19m18s)

## B2 sync

Deferred to host — rclone not available in sandbox. Phase 8 is read-only on corpus (no raw/ mutation) so deferral is acceptable per BRIEF.md §8.

## Next tick

Routine Phase 8 sampling continues. The 15 `parliament-pdf-v1.2` truncated-16hex defect records remain an open operator-triage item (latent — not drawn this tick).
