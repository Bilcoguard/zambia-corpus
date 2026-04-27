# Batch 0292 Report

**Phase:** 4 — bulk (priority_order pivot probe — sis_employment + sis_mining + sis_family)
**Tick:** 2026-04-27 (UTC) — scheduled tick, 30-min cadence
**Yield:** 0 records committed
**Wall-clock:** ~13 min
**Parser version:** 0.5.0 (sis ingest skeleton; 0 records materialised)

## Summary

Inherited from batch 0291: acts_in_force, sis_corporate-modern,
sis_tax-modern (text-extractable), case_law_scz, sis_data_protection
all at upstream steady state for the worker's current toolset. Per
`approvals.yaml.phases.phase_4_bulk.priority_order`, items 4
(sis_employment), 7 (sis_mining), 8 (sis_family) remain to be probed.

This tick probes the 6 highest-yield alphabets (E, F, J, L, N, W) on
zambialii — letters not covered in b0291's A,B,C,I,M,P,S,T,V sweep.

**Result:** zero records committed. One in-priority candidate
discovered (2022/13 sis_employment), already in the OCR backlog
(re-attempted; same pdfplumber 0-char result). Six off-priority
candidates encountered, all already in OCR backlog (reserved).

## Probes (6 alphabet sweeps)

| Alphabet | Total SI links | Modern (>=2017) | Novel (not on disk) | In-priority novel |
|---|---|---|---|---|
| E | 85 | 74 | 5 | 1 (2022/13 sis_employment)            |
| F | 23 | 15 | 1 | 0 (2018/11 sis_forests off-priority)  |
| J |  1 |  1 | 0 | 0 |
| L | 26 | 14 | 0 | 0 |
| N | 60 | 36 | 1 | 0 (2022/7 sis_archives off-priority)  |
| W |  9 |  4 | 0 | 0 |

robots.txt sha256 (zambialii): `fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0` (unchanged from b0193..0291; re-verified at tick start).

## sis_employment (priority_order item 4) — 1 candidate, OCR-required

Single novel modern sis_employment SI discovered:

| Year/Num | Title | Parent Act | PDF size | pdfplumber result |
|---|---|---|---|---|
| 2022/13 | Minimum Wages and Conditions of Employment (Truck and Bus Drivers) (Amendment) Order, 2022 | Minimum Wages and Conditions of Employment Act | 550,009 B | 0 text chars (scanned image) |

This candidate has been attempted in batches 0184, 0200, 0205, 0221
with the same pdfplumber 0-char result. It is already documented in
`gaps.md` and on the OCR backlog. Re-attempt this tick was cache-reuse
only (raw HTML and PDF on disk from b0184; no fetch bytes spent).

Per BRIEF non-negotiable #1 (no fabrication) and the worker's tooling
constraint, no record JSON was written.

## sis_mining (priority_order item 7) — modern era exhausted

Alphabet=M was probed in b0291 and returned 10 modern SIs / 0 novel.
No additional letter is likely to surface a "Mines"/"Mineral" SI.
Modern-era sis_mining is at upstream steady state.

## sis_family (priority_order item 8) — modern era exhausted

Across F, J, L, M (b0291), W: zero novel modern SIs match family-law
title patterns (Marriage, Matrimonial, Children, Juvenile, Maintenance,
Adoption, Affiliation). On-disk sis_family record count remains 0.

## Out-of-priority_order discoveries (reserved)

Six additional novel modern SIs were encountered. None are in
`approvals.yaml.phases.phase_4_bulk.priority_order`; none are picked.

| Year/Num | Title                                                            | Sub-phase     |
|----------|------------------------------------------------------------------|---------------|
| 2026/4   | Electricity (Transmission) (Grid Code) Regulations, 2026         | sis_energy    |
| 2022/7   | National Archives (Fees) Regulations, 2021                       | sis_archives  |
| 2022/8   | National Assembly By-Election (Kabwata No. 77) Order, 2022       | sis_elections |
| 2018/11  | Forests (Community Forest Management) Regulations, 2018          | sis_forests   |
| 2018/75  | National Assembly By-Election (Mangango No. 141) Order, 2018     | sis_elections |
| 2018/93  | National Assembly By-Election (Sesheke No. 153) Order, 2018      | sis_elections |

All six are already in the OCR backlog from prior ticks; their
inclusion in this report is purely informational. If a human reviewer
adds `sis_energy`, `sis_archives`, `sis_elections`, or `sis_forests`
to priority_order, future ticks can pick them up (and will hit OCR
gating regardless).

## Integrity

`_work/integrity_0292.py` was run after this tick's work:

- records/sis count: 539 (unchanged from b0291 close)
- records/acts count: 1,169 (unchanged from b0290 close)
- in-priority candidate (2022/13) raw HTML+PDF intact on disk
- 2022/13 documented in gaps.md OCR backlog (5 prior gaps.md entries verified)
- All checks PASS

CHECK1..CHECK6 do not apply this tick (no record writes).

## Provenance

User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
Crawl-delay: 6 s on zambialii (>= robots 5 s)
robots.txt sha256: `fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0`

## Budget

- Today (2026-04-27 UTC) fetches at tick start: ~52/2,000 (~2.6%) — last batch 0291 close level
- Today (2026-04-27 UTC) fetches at tick end:   ~59/2,000 (~2.95%)
  - Breakdown this tick: 1 robots + 6 alphabet listings (E, F, J, L, N, W) = 7 fetches.
  - Ingest attempt (idx 0 / 2022/13) reused cached HTML+PDF; no new bytes spent.
- Tokens within budget

## Cumulative

- Acts on disk: 1,169 (unchanged)
- SI records on disk: 539 (unchanged)
- Multi-act-gazette retry queue: 1 (unchanged: 2024/9)
- Oversize-pdf queue: 6 (unchanged: 2002/6, 2005/21, 2008/5, 2009/10, 2009/30, 2012/16)
- OCR section-tolerant retry queue: 6 (unchanged: 1988/32, 1994/40, 1995/33, 2004/6, 2008/9, 2009/7)
- OCR backlog: **21** (unchanged; 2022/13 was already a member)
- Off-priority reserve (b0291): 3 unchanged

## SQLite

Not modified (no record writes; established disposition — FTS5 vtable
broken, journal held open).

## B2 sync

Deferred to host (rclone not available in sandbox).

## Phase 4 status

`approvals.yaml -> phase_4_bulk -> complete` remains `false`. Worker
does NOT flip the flag.

The acts_in_force, sis_corporate-modern, sis_tax-modern
(text-extractable), sis_employment-modern, sis_mining-modern,
sis_family-modern, case_law_scz, and sis_data_protection sub-phases
have ALL reached upstream steady state with respect to current
zambialii listings and the worker's `requests + beautifulsoup4 +
pdfplumber` toolset.

## Recommended next move (for human reviewer)

The worker has now exhausted every priority_order sub-phase pool that
can be ingested with the current toolset. Productive directions
remain unchanged from b0290/b0291's recommendations:

1. **Add an OCR pipeline** (Tesseract or equivalent) to the worker
   toolset. This would unblock the OCR backlog (21 items including
   2022/13 sis_employment, 3 sis_tax SIs, plus pre-existing acts and
   off-priority reserves) and likely enable substantial pre-2017 SI
   ingestion.
2. **Approve a host-side rclone+chunked-PDF pipeline** for the 6-item
   oversize-pdf queue.
3. **Approve a multi-Act gazette splitter** for 2024/9.
4. **Define pre-2017 scope per sub-phase.** Modern (>=2017) era is
   exhausted across all priority sub-phases. A scope definition would
   unlock pre-2017 alphabet-listing ingestion.
5. **Add `sis_industry`, `sis_governance`, `sis_energy`, `sis_archives`,
   `sis_elections`, `sis_forests`** to priority_order (or accept ad-hoc
   ingestion), unlocking the b0291 + b0292 reserve items (most of which
   would still hit OCR gating).

Until one of the above is actioned, future ticks (b0293+) will continue
to idle on phase_4_bulk with probe-only refresh checks.

## Disposition

Commit this tick:

- `scripts/batch_0292.py` (PICKS skeleton + documentation)
- `_work/batch_0292_*` (discover, parse, ingest_one, probe outputs, fail diagnostic)
- `gaps.md` updated (Batch 0292 section appended with 2022/13 re-attempt + reserve table)
- `reports/batch-0292.md` (this file)
- `worker.log` appended
- `costs.log` appended (7 fetches recorded)

No record JSON files written. corpus.sqlite unchanged. raw/zambialii/si/2022/
unchanged on disk (cache reuse only).
