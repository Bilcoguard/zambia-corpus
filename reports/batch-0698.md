# Phase 8 batch 0698 — Nightly re-verification

- **Tick:** b0698-phase8
- **Phase:** phase_8_nightly_reverify (approvals.yaml — approved: true, complete: false, sample_rate: 0.01)
- **Parser/fetcher version:** phase8-reverify-0.1.0
- **Script:** `scripts/batch_0698_phase8_reverify.py` (verbatim clone of `scripts/batch_0697_phase8_reverify.py`; only the `BATCH` constant changed `"0697"` → `"0698"`; same logic as b0625/b0641/…/b0689/b0690/b0697)
- **Seed:** `phase8-reverify-2026-05-18-b0698`
- **Started:** 2026-05-18T12:10:38Z
- **Completed:** 2026-05-18T12:11:12Z
- **Wall clock:** ~34s (well within 20-minute budget)
- **Predecessor:** b0697-phase8 (pool_size 1949). No intervening record-file commits — pool unchanged at 1949.
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

All 8 fetches returned HTTP 200. No fetch errors. ZambiaLII availability remained stable through the tick.

b0698 did **not** draw any of the 15 `parliament-pdf-v1.2` truncated-16hex defect records — CHECK #3 PASSES this tick on seed-luck alone. The latent 15-record cohort remains an open operator-triage item (carry-over from b0670 diagnosis).

## Results

| Verdict | Type | ID | Source host | URL kind | Notes |
|---|---|---|---|---|---|
| drift | act | act-zm-1969-036-state-security-act-1969 | zambialii.org | AKN-HTML `eng@`-suffixed | dynamic-render cohort |
| match | act | act-zm-2024-020-supplementary-appropriation-2024-no-2-act-2024 | www.parliament.gov.zm | parliament.gov.zm Act PDF | stable-PDF supercohort match |
| drift | statutory_instrument | si-zm-2022-021-electoral-process-local-government-by-elections-election-date-and-time-of-poll-order-2022 | zambialii.org | AKN-HTML bare (no `eng@`) | dynamic-render cohort |
| drift | act | act-zm-1982-025-minimum-wages-and-conditions-of-employment--1982 | www.zambialii.org | AKN-HTML `eng@`-suffixed | dynamic-render cohort |
| match | si | si-zm-2020-011-income-tax-royal-haskoning-dhv-pty-limited-approval-and-exemption-order-2020 | zambialii.org | AKN source.pdf | stable-PDF supercohort match |
| drift | act | act-zm-2013-003-medicines-and-allied-substances-act-2013 | zambialii.org | AKN-HTML `eng@`-suffixed | dynamic-render cohort |
| drift | judgment | judgment-zm-2025-zmcc-22-sean-tembo-suing-in-his-capacity-as-spokesperson-o | zambialii.org | AKN-HTML `eng@`-suffixed | dynamic-render cohort |
| drift | act | act-zm-1981-006-excess-expenditure-appropriation-1978-act-1981 | zambialii.org | AKN-HTML `eng@`-suffixed | dynamic-render cohort |

All 6 drift verdicts are textbook `zambialii_akn_html_dynamic_render_drift` cohort — AKN-HTML landing pages (both `/akn/.../eng@<date>` and bare-`/akn/...` variants represented) whose dynamic-rendered HTML carries embedded timestamps/footer counters that change between fetches. No new sub-cohort spawned.

Both match verdicts are stable-PDF supercohort:
- 1× **www.parliament.gov.zm** Act PDF (Supplementary Appropriation Act No. 20 of 2024) — first parliament.gov.zm host appearance in a Phase 8 sample in the recent run; verifies that the parliament.gov.zm Act-PDF supercohort behaves identically to the zambialii AKN source.pdf / media.zambialii.org source_file PDF supercohorts (byte-identical hashes across fetches).
- 1× zambialii AKN source.pdf (income-tax SI 2020).

Drift rate this tick (6/8 = 75%) is consistent with the Phase 8 series long-run cohort-mix expectation (AKN-HTML ≈100% drift; stable PDFs ≈100% match). This does not indicate any change in source-content stability.

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

- Network fetches this tick: 8 (all HTTP 200; 5× zambialii.org AKN-HTML, 1× www.zambialii.org AKN-HTML, 1× zambialii.org AKN source.pdf, 1× www.parliament.gov.zm Act PDF)
- Cumulative daily fetches: well under 2000/day budget (b0691: 81, b0692: 0, b0693-jiw: probe-only, b0694: ~16, b0695: ~16, b0696-jiw: 0, b0697: 8, repair b0697: 8, b0698: 8 → ≈137 of 2000)
- Tokens consumed: 0 (deterministic pipeline, no LLM calls)
- Bandwidth: 645,797 bytes total (~631 KB); largest = act-zm-2024-020-supplementary-appropriation-2024-no-2-act-2024 (297,824 bytes parliament.gov.zm PDF)
- Wall clock: 34s (budget 20min; headroom ~19m26s)

## B2 sync

Deferred to host — rclone not available in sandbox. Phase 8 is read-only on corpus (no `raw/` mutation) so deferral is acceptable per BRIEF.md §8.

## Next tick

Routine Phase 8 sampling continues. The 15 `parliament-pdf-v1.2` truncated-16hex defect records remain an open operator-triage item (latent — not drawn this tick).
