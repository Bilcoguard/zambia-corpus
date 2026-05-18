# Phase 8 — Nightly Re-verification — batch 0708

- **Phase:** `phase_8_nightly_reverify`
- **Worker run id:** `b0708-phase8`
- **Script:** `scripts/batch_0708_phase8_reverify.py` (clone of frozen baseline `scripts/batch_0546_phase8_reverify.py`; only `BATCH` constant differs from `scripts/batch_0707_phase8_reverify.py`)
- **Parser version:** `phase8-reverify-0.1.0`
- **Seed:** `phase8-reverify-2026-05-18-b0708`
- **Started:** `2026-05-18T16:03:44Z`
- **Completed:** `2026-05-18T16:04:22Z`
- **Wall clock:** 38s (budget 20min; headroom ~19m22s)
- **Pool size:** 1964 records (records/**/*.json with both `source_url` + `source_hash`) — unchanged from b0707 (`pool_size=1964`); no insertions or removals since prior Phase 8 tick.
- **Sample size:** 8 (`sample_rate 0.01`, capped at `MAX_BATCH=8`)
- **Fetches:** 8 (all HTTP 200)
- **Outcome counts:** match=3, drift=5, fetch_error=0
- **B2 sync:** deferred to host (rclone not in sandbox; Phase 8 is read-only on corpus — no `raw/` mutation)

## Results

| Verdict | Type | ID | Source host | URL kind | Notes |
|---|---|---|---|---|---|
| match | act | act-zm-2015-005-referendum | www.parliament.gov.zm | parliament.gov.zm Act PDF | stable-PDF supercohort match (10,662 B) |
| match | statutory_instrument | si-zm-2010-035-information-and-communication-technologies-electronic-communications-licensing-r | zambialii.org | AKN `source.pdf` | stable-PDF supercohort match (ZambiaLII source.pdf sub-variant; 4,150,178 B — heaviest single fetch this tick) |
| drift | act | act-zm-1991-001-constitution-of-zambia-act-1991 | zambialii.org | AKN-HTML `eng@`-suffixed | `zambialii_akn_html_dynamic_render_drift` cohort |
| drift | act | act-zm-1964-031-evidence-bankers-books-act-1964 | zambialii.org | AKN-HTML `eng@`-suffixed | `zambialii_akn_html_dynamic_render_drift` cohort |
| drift | act | act-zm-1969-013-merchant-shipping--temporary-provisions--act--1969 | www.zambialii.org | AKN-HTML `eng@`-suffixed | `zambialii_akn_html_dynamic_render_drift` cohort (`www.` host sub-variant) |
| drift | statutory_instrument | si-zm-2022-058-zambezi-river-authority-terms-and-conditions-of-service-amendment-by-laws-2022 | zambialii.org | AKN bare-path | `zambialii_akn_html_dynamic_render_drift` (bare-AKN-path sub-variant) |
| match | statutory_instrument | si-zm-2002-040-pension-fund-annual-report-regulations-2002 | zambialii.org | AKN `source.pdf` | stable-PDF supercohort match (ZambiaLII source.pdf sub-variant; 914,073 B) |
| drift | act | act-zm-2018-023-supplementary-appropriation-2018-no-2-act | zambialii.org | AKN-HTML `eng@`-suffixed | `zambialii_akn_html_dynamic_render_drift` cohort |

The b0708 sample mix mirrored b0707 numerically (5 drift / 3 match) but skewed more heavily toward the `eng@`-suffixed AKN-HTML sub-variant: 4 of 5 drifts were `eng@`-suffixed (1 each for `zambialii.org` and `www.zambialii.org` hosts), the 5th was a bare-AKN-path SI. All 5 dynamic-HTML URLs drifted and all 3 stable PDFs matched — consistent with the pre-documented per-URL-kind behaviour. AKN-HTML pages embed server-rendered timestamps and footer counters, so byte-level hash drift is the expected behaviour for these URL forms and does NOT imply substantive legal-text change.

The 3 matches confirm both branches of the stable-PDF supercohort remain stable across this tick's sample:
- **parliament.gov.zm Act PDFs:** 1/1 match (Referendum Act 5/2015 = 10,662 B).
- **ZambiaLII `source.pdf`:** 2/2 match (ICT Electronic Communications Licensing Regs 35/2010 = 4,150,178 B; Pension Fund Annual Report Regs 40/2002 = 914,073 B).

Drift rate this tick (5/8 = 62.5%) reflects sample composition, not corpus health. Per-URL-kind hit rates remain consistent with prior ticks (AKN-HTML ≈100% drift; stable PDFs ≈100% match → 5/5 dynamic-HTML drift + 3/3 stable-PDF match).

One minor variant observation: `act-zm-1969-013-merchant-shipping--temporary-provisions--act--1969` was served from `www.zambialii.org` rather than `zambialii.org` (the more common form). This is the same site, served on the host-with-`www` alias; ZambiaLII serves identical content from both. The `www.` host already has a `RATE_LIMITS` entry (5 s) and was honoured this tick. No new sub-cohort was spawned — slot under existing `zambialii_akn_html_dynamic_render_drift` (the `www.` host alias is documented from prior ticks).

## Integrity checks

| # | Check | Result |
|---|---|---|
| 1 | JSON report well-formed; match+drift+fetch_error == sample_size (3+5+0=8) | PASS |
| 2 | No duplicate IDs in sample (8 unique) | PASS |
| 3 | Every stored + fetched sha256 is a valid 64-hex sha256 | PASS |
| 4 | Every sampled record's `stored_sha256` matches the on-disk record's `source_hash` (proper `sha256:` prefix-stripping) | PASS (no record file mutated this tick) |
| 5 | No tracked record file modified by this run (script is read-only) | PASS (`git diff --stat records/` empty pre-commit) |
| 6 | `corpus.sqlite` NOT touched; `approvals.yaml` NOT modified | PASS (`git diff --stat corpus.sqlite approvals.yaml` empty) |
| 7 | robots.txt respected; per-host rate limits honoured (zambialii.org + www.zambialii.org min_gap ≥ 5s; deterministic `sleep_for_host` mechanism unchanged from baseline) | PASS |
| 8 | User-Agent honest: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` | PASS |
| 9 | corpus.sqlite live `quick_check=ok records=1961 records_fts=1961 dup_ids=0` (baseline parity preserved across tick) | PASS |

All 9 checks PASS — tick commits via normal path.

## Cost / budget

- Network fetches this tick: 8 (all HTTP 200)
- Cumulative daily fetches (all workers, NETWORK_FETCHES count rows only): ~72 (pre-tick from b0707-phase8 line; +26 from b0707-jiw NETWORK_FETCHES row) ≈ ~98 + 8 (this tick) ≈ ~106 of 2000 daily budget
- Tokens consumed: 0 (deterministic pipeline, no LLM calls)
- Bandwidth: 6,978,101 bytes total (~6.66 MB); largest = `si-zm-2010-035-information-and-communication-technologies-electronic-communications-licensing-r` (4,150,178 B, ZambiaLII `source.pdf`)
- Wall clock: 38s (budget 20min; headroom ~19m22s)

## B2 sync

Deferred to host — rclone not available in sandbox. Phase 8 is read-only on corpus (no `raw/` mutation) so deferral is acceptable per BRIEF.md §8.

## Next tick

Routine Phase 8 sampling continues. No new audit-trail items spawned this tick. Pre-existing carry-forwards remain:
- `judgment-zm-2025-zmcc-14` canonical-URL-date variant 404 (b0700 — audit-only; remediation requires explicit Peter approval).
- Existing 15 `parliament-pdf-v1.2` truncated-16hex defect records remain an open operator-triage item (latent — not drawn this tick).
