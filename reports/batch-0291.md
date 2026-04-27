# Batch 0291 Report

**Phase:** 4 — bulk (priority_order pivot probe — sis_corporate exhaustion + sis_tax candidates triage)
**Tick:** 2026-04-27 (UTC) — scheduled tick, 30-min cadence
**Yield:** 0 records committed
**Wall-clock:** ~12 min
**Parser version:** 0.5.0 (sis_tax ingest skeleton; 0 records materialised)

## Summary

Inherited from batch 0290: acts_in_force chronological-first sweep at upstream steady state through 2026/11. Per `approvals.yaml.phases.phase_4_bulk.priority_order`, item 2 is `sis_corporate` and item 3 is `sis_tax`. This tick probes upstream for novel modern (>=2017) SIs across both sub-phases.

**Result:** zero records committed. Three sis_tax candidates were discovered but all three are scanned-image PDFs (pdfplumber returned 0 text chars); they have been added to the OCR backlog. Zero novel modern SIs exist upstream for sis_corporate.

## Probes (9 alphabet sweeps)

| Alphabet | Total SI links | Modern (>=2017) | Novel (not on disk) | Notes |
|---|---|---|---|---|
| A | 20  | 12 | 0 | — |
| B | 4   | 1  | 0 | sparse listing |
| C | 245 | 18 | 1 | 2025/20 Compulsory Standards (sis_industry) |
| I | 98  | 31 | 2 | 2017/43, 2019/25 Income Tax (sis_tax) |
| M | 24  | 10 | 0 | — |
| P | 33  | 9  | 0 | — |
| S | 17  | 9  | 2 | 2022/12 Societies (sis_governance); 2017/68 Standards (sis_industry) |
| T | 56  | 12 | 0 | — |
| V | 15  | 7  | 1 | 2022/4 VAT (sis_tax) |

robots.txt sha256 (zambialii): `fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0` (unchanged from b0193..0290; re-verified at tick start).

## sis_corporate (priority_order item 2) — modern era exhausted

Across the 9 alphabets probed (covering all corporate-relevant first letters: Banking, Companies, Co-operative, Citizens-Economic-Empowerment, Insurance, Pensions, Securities, plus broad-coverage T/V/M/A), **zero novel modern SIs** match Companies/Corporate/Co-operative/Banking/Insurance/Pensions/Securities title patterns. The on-disk sis_corporate cluster (6 records: 2017/001, 2019/014, 2019/015, 2019/021, 2019/040, 2016/003) is at upstream steady state for the modern (>=2017) era.

Pre-2017 era SIs may exist on zambialii under sis_corporate sub-phase, but no human-defined scope for that has been documented; deferred per the b0290 recommendation.

## sis_tax (priority_order item 3) — 3 candidates, all OCR-required

Three novel modern sis_tax SIs discovered:

| Year/Num | Title | Parent Act | PDF size | pdfplumber result |
|---|---|---|---|---|
| 2017/43 | Income Tax (Suspension of Tax on Payments to Non-Resident Contractors)(Batoka Hydro-Electric Scheme) Regulations, 2017 | Income Tax Act | 475,677 B | 0 text chars (scanned image) |
| 2019/25 | Income Tax Act (Suspension of tax on payment of interest to non-resident)(Treasury Bill and Bond) Regulations, 2019 | Income Tax Act | 303,419 B | 0 text chars (scanned image) |
| 2022/4  | Value Added Tax (Zero-Rating)(Amendment) Order, 2022 | Value Added Tax Act | 343,193 B | 0 text chars (scanned image) |

All three: HTML page sha256 verified; source.pdf fetched cleanly; raw HTML+PDF retained at `raw/zambialii/si/{2017,2019,2022}/`. pdfplumber returns empty text — these are scanned-image PDFs requiring OCR. Per BRIEF non-negotiable #1 (no fabrication) and BRIEF tooling constraint ("requests, beautifulsoup4, pdfplumber, sqlite3, pyyaml" only; no OCR), no record JSON was written.

These three SIs join the OCR backlog (was 18 items, now 21).

## Out-of-priority_order discoveries (reserved)

Three additional novel modern SIs were discovered but their sub-phases are not in `approvals.yaml.phases.phase_4_bulk.priority_order`:

| Year/Num | Title | Sub-phase |
|---|---|---|
| 2025/20 | Compulsory Standards (Declaration) Order, 2025 | sis_industry |
| 2017/68 | Standards (Compulsory Standards)(Declaration) Order, 2017 | sis_industry |
| 2022/12 | Societies (Amendment) Rules, 2021 | sis_governance |

These remain unpicked. If a human reviewer adds `sis_industry` or `sis_governance` to priority_order (or accepts ad-hoc ingestion), a future tick can pick these up via the cached HTML/discover state in `_work/batch_0291_*.json`.

## Integrity

This tick performed no record writes; CHECK1..CHECK6 do not apply (no batch). Three pick-ingest attempts (`_work/batch_0291_one_{0,1,2}.json`) returned `status=fail, error=pdf_parse_empty` — no record JSON files written, no fabrication risk.

Pool refresh diff verification (alphabet-listing vs on-disk): novel set fully enumerated above (6 items); 4 cannot be processed by current toolset (3 OCR + 1 sis_governance off-priority + 1 sis_industry off-priority + the 2025/20 sis_industry off-priority).

## Provenance

User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
Crawl-delay: 6 s on zambialii (>= robots 5 s)
robots.txt sha256: `fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0`

## Budget

- Today (2026-04-27 UTC) fetches at tick start: ~37/2,000 (~1.85%) — last batch 0290 closed at this level
- Today (2026-04-27 UTC) fetches at tick end:   ~52/2,000 (~2.6%)
  - Breakdown: 1 robots + 9 alphabet listings + 3 HTML records + 3 PDFs (all retained for OCR) = 16 fetches this tick. Discover/probe scripts wrote `_work/batch_0291_alphabet_*.html` for each.
- Tokens within budget

## Cumulative

- Acts on disk: 1,169 (unchanged)
- SI records on disk: 539 (unchanged)
- Multi-act-gazette retry queue: 1 (unchanged: 2024/9)
- Oversize-pdf queue: 6 (unchanged: 2002/6, 2005/21, 2008/5, 2009/10, 2009/30, 2012/16)
- OCR section-tolerant retry queue: 6 (unchanged: 1988/32, 1994/40, 1995/33, 2004/6, 2008/9, 2009/7)
- OCR backlog: **21** (was 18; added si-2017/43, si-2019/25, si-2022/4)
- Off-priority reserve: 3 (si-2025/20, si-2017/68 sis_industry; si-2022/12 sis_governance)

## SQLite

Not modified (no record writes; established disposition).

## B2 sync

Deferred to host (rclone not available in sandbox).

## Phase 4 status

`approvals.yaml -> phase_4_bulk -> complete` remains `false`. Worker does NOT flip the flag.

The acts_in_force chronological sub-phase, the sis_corporate-modern sub-phase, and the sis_tax-modern (text-extractable) sub-phase have all reached upstream steady-state with respect to current zambialii listings and the worker's current toolset.

## Recommended next move (for human reviewer)

The worker has now exhausted all ZambiaLII modern (>=2017) sub-phase pools that can be ingested with `requests + beautifulsoup4 + pdfplumber`. Three productive directions remain:

1. **Add an OCR pipeline** (Tesseract or equivalent) to the worker toolset. This would unblock the OCR backlog (now 21 items: 18 prior acts + the 3 sis_tax SIs identified this tick) and likely enable a substantial fraction of pre-2017 SI ingestion.
2. **Approve a host-side rclone+chunked-PDF pipeline** for the 6-item oversize-pdf queue (Appropriation Acts and Cotton Act 2005). Raw HTMLs are already cached.
3. **Approve a multi-Act gazette splitter** for the 1-item multi-act-gazette retry queue (2024/9 Supplementary Appropriation Act).
4. **Define pre-2017 sis_corporate scope.** The corpus has only 6 records tagged `sis_corporate`, all 2016+. Pre-2017 Companies/Banking/Insurance/Securities Act SIs likely exist in the C/B/I/S alphabet listings but are below the modern-only filter the worker has been using. A scope definition would unlock alphabet=C/B/I/S pre-2017 modern (>=year_X) ingestion.
5. **Add `sis_industry` and `sis_governance` to priority_order** (or accept ad-hoc ingestion), unlocking the 3 reserve items identified this tick.

Until one of the above is actioned, future ticks (b0292+) will continue to idle on phase_4_bulk with probe-only refresh checks.

## Disposition

Commit this tick:
- `scripts/batch_0291.py` (PICKS skeleton, documentation)
- `_work/batch_0291_*` (probe scripts and outputs, ingest_one + 3 fail diagnostics)
- `gaps.md` updated (3 new OCR-deferred SIs)
- `reports/batch-0291.md` (this file)
- `worker.log` appended
- `costs.log` appended (16 fetches recorded)

No record JSON files written. corpus.sqlite unchanged. raw/zambialii/si/{2017,2019,2022}/ each gain one HTML+PDF pair (kept for future OCR pipeline; no record references them yet).
