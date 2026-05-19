# Phase 8 — Nightly Re-verification — batch 0725

- **Phase:** `phase_8_nightly_reverify`
- **Worker run id:** `b0725-phase8`
- **Script:** `scripts/batch_0725_phase8_reverify.py` (clone of frozen baseline `scripts/batch_0546_phase8_reverify.py`; only `BATCH` constant changed from `scripts/batch_0724_phase8_reverify.py`, the immediately prior Phase 8 tick — b0723 was a JIW tick, b0724 was the prior Phase 8 slot)
- **Parser version:** `phase8-reverify-0.1.0`
- **Seed:** `phase8-reverify-2026-05-19-b0725`
- **Started:** `2026-05-19T08:03:51Z`
- **Completed:** `2026-05-19T08:04:34Z`
- **Wall clock:** 43s (budget 20min; headroom ~19m17s)
- **Pool size:** 1989 records (records/**/*.json with both `source_url` + `source_hash`) — pool grew by +7 since b0724 (1982 → 1989) consistent with the intervening b0723-jiw insertion of 8 ZambiaLII Supreme Court reparse-deferred judgments minus one overlap or counting variance.
- **Sample size:** 8 (`sample_rate 0.01`, capped at `MAX_BATCH=8`)
- **Fetches:** 8 (8× HTTP 200, 0× fetch error)
- **Outcome counts:** match=1, drift=7, fetch_error=0
- **B2 sync:** deferred to host (rclone not in sandbox; Phase 8 is read-only on corpus — no `raw/` mutation)

## Results

| Verdict | Type | ID | Source host | URL kind | Notes |
|---|---|---|---|---|---|
| drift | act | act-zm-2008-006-excess-expenditure-appropriation-2005 | www.parliament.gov.zm | parliament.gov.zm `documents/acts/*.pdf` | **AUDIT-ITEM** — first observed drift in `parliament.gov.zm` acts-PDF supercohort; historically this cohort has matched stably (see b0724 verdict). Stored sha256=`a09c5a90…d4693`; fetched sha256=`953f8660…ab4dd`. Filename URL points at `Supplementary%20Appropriation%20%282006%29%2C%202008.pdf` — possibly server-side file replacement (re-OCR'd / re-stamped); requires Peter's review. NOT a remediation trigger this tick. |
| drift | judgment | judgment-zm-2020-zmcc-17-mulubisha-v-attorney-general | zambialii.org | AKN-HTML `eng@`-suffixed (`/akn/zm/judgment/zmcc/2020/17/eng@2020-04-24`) | `zambialii_akn_html_dynamic_render_drift` cohort (`eng@`-suffixed sub-variant; CC judgment HTML) |
| drift | act | act-zm-2022-005-bank-of-zambia-act-2022 | zambialii.org | AKN-HTML `eng@`-suffixed (`/akn/zm/act/2022/5/eng@2022-07-29`) | `zambialii_akn_html_dynamic_render_drift` cohort (`eng@`-suffixed sub-variant; Act HTML) |
| drift | act | act-zm-1994-040-supplementary-appropriation-1992-act | zambialii.org | AKN-HTML `eng@`-suffixed (`/akn/zm/act/1994/40/eng@1994-12-31`) | `zambialii_akn_html_dynamic_render_drift` cohort (`eng@`-suffixed sub-variant; Act HTML) |
| drift | act | act-zm-1965-023-national-flag-and-armorial-ensigns-act-1965 | zambialii.org | AKN-HTML `eng@`-suffixed (`/akn/zm/act/1965/23/eng@1996-12-31`) | `zambialii_akn_html_dynamic_render_drift` cohort (`eng@`-suffixed sub-variant; Act HTML) |
| drift | statutory_instrument | si-zm-2016-041-zambia-wildlife-game-animals-order-2016 | zambialii.org | AKN bare-path SI (`/akn/zm/act/si/2016/41`) | `zambialii_akn_html_dynamic_render_drift` cohort (bare-AKN-path sub-variant; SI HTML) |
| drift | judgment | judgment-zm-2025-zmsc-06-zambia-telecommunication-company-v-felix-musonda-a | zambialii.org | AKN-HTML `eng@`-suffixed (`/akn/zm/judgment/zmsc/2025/6/eng@2025-02-12`) | `zambialii_akn_html_dynamic_render_drift` cohort (`eng@`-suffixed sub-variant; SCZ judgment HTML) |
| match | si | si-zm-2018-092-national-health-research-material-transfer-regulations-2018 | zambialii.org | zambialii.org `source.pdf` (`/akn/zm/act/si/2018/92/eng@2018-12-07/source.pdf`) | zambialii.org source.pdf supercohort match (stable PDF) |

The b0725 sample composition: 1/8 `parliament.gov.zm/documents/acts/*.pdf` Act, 1/8 zambialii.org `source.pdf` SI, 4/8 zambialii.org AKN-HTML `eng@`-suffixed records (2 Acts + 2 judgments — 1 CC + 1 SCZ), 1/8 zambialii.org AKN bare-path SI, and the parliament.gov.zm Act (counted once above). 1/2 stable-PDF cohort records matched (zambialii.org `source.pdf` supercohort) but `parliament.gov.zm` acts-PDF supercohort drifted for the first time observed in the Phase 8 window — see AUDIT-ITEM above. All 5 zambialii.org AKN-HTML records drifted (`zambialii_akn_html_dynamic_render_drift` cohort — known server-rendered timestamp / asset cache-busting behaviour; not substantive legal-text change). No fetch errors this tick.

No repeat-draws this tick: the eight IDs in b0725 do not appear in b0724's sample. (Seed is per-batch, not global; collisions are statistically expected at ~0.4% per record per tick.)

### Carry-forward audit-trail items

- `judgment-zm-2024-coa-024-kingfred-phiri-v-life-master-ltd` 404 (first observed b0717 at 20:33:55Z, single observation to date). NOT in this tick's sample — no new observation; record remains under audit-only watch pending independent corroboration in subsequent Phase 8 sweeps.
- `judgment-zm-2025-zmcc-14` canonical-URL-date variant 404 (b0700 — audit-only; remediation requires explicit Peter approval) — NOT in this tick's sample.
- **NEW (b0725):** `act-zm-2008-006-excess-expenditure-appropriation-2005` (parliament.gov.zm acts-PDF) drifted — first observation in Phase 8 window. Audit-only; remediation requires explicit Peter approval. Recorded in gaps.md.

## Integrity checks

| # | Check | Result |
|---|---|---|
| 1 | JSON report well-formed; match+drift+fetch_error == sample_size (1+7+0=8) | PASS |
| 2 | No duplicate IDs in sample (8 unique) | PASS |
| 3 | Every stored + fetched sha256 is a valid 64-hex sha256 | PASS |
| 4 | Every sampled record's `stored_sha256` matches the on-disk record's `source_hash` (proper `sha256:` prefix-stripping) | PASS (no record file mutated this tick) |
| 5 | No tracked record file modified by this run (`git diff --name-only records/` empty) | PASS (script never opens records/ for write — source-verified) |
| 6 | `corpus.sqlite` NOT touched; `approvals.yaml` NOT modified (`git status --porcelain corpus.sqlite approvals.yaml` empty) | PASS |
| 7 | robots.txt respected; per-host rate limits honoured (zambialii.org min_gap ≥ 5s; www.parliament.gov.zm min_gap ≥ 2s default; deterministic `sleep_for_host` mechanism unchanged from baseline) | PASS |
| 8 | User-Agent honest: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` | PASS |
| 9 | corpus.sqlite `PRAGMA quick_check` = ok; records=1986; records_fts=1986; dup_ids=0 | PASS |

## Bandwidth

| Resource | Bytes |
|---|---|
| 8 fetches | 1,543,332 |

Hosts: parliament.gov.zm (×1), zambialii.org (×7).

## Decision

Phase 8 is read-only on the corpus. Per the script invariants, no record JSON, no SQLite row, and no approvals state were mutated this tick. Drift outcomes are logged for trend analysis; the new parliament.gov.zm Act PDF drift is recorded as an audit-only item in `gaps.md` and surfaced here. Tick verdict: **COMMIT-normal-path** (commit the new script clone, the reverify JSON, and this markdown report only).
