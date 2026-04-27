# Batch 0298 Report

**Phase:** 4 — bulk (minimal upstream-refresh tick)
**Tick:** 2026-04-27 (UTC) — scheduled tick, 30-min cadence
**Yield:** 0 records committed
**Wall-clock:** ~3 min
**Parser version:** 0.5.0 (probe-only — same as b0290..b0297)

## Summary

This tick is a minimal upstream-refresh probe of the two chronological
Act feeds:

- `zambialii.org/legislation/recent`
- `parliament.gov.zm/acts-of-parliament` (page 0)

All 22 active alphabet letters on zambialii were exhaustively swept
across b0291..b0293 (A,B,C,I,M,P,S,T,V in b0291; E,F,J,L,N,W in b0292;
D,G,H,K,O,R,U in b0293), so no alphabet sweep is performed this tick.

**Result:** 0 in-priority candidates; 0 off-priority candidates. All
upstream entries already in corpus. Steady state preserved.

## Tick context

Pre-tick lock cleanup ran cleanly (no leftover `.lock` or `.lock.bak`
files). `git pull --ff-only` returned "Already up to date" on first
attempt (benign `unable to unlink ...maintenance.lock` warning emitted
by git but pull succeeded — sandbox cannot delete files in
`.git/objects/`, this is not a recovery condition).

## Refresh probe — zambialii /legislation/recent

13 act links enumerated:

- 2025/5  National Road Fund (Amendment) Act
- 2025/6  Building Societies (Amendment) Act
- 2025/7  Animal Health (Amendment) Act
- 2025/8  Border Management and Trade Facilitation Act
- 2025/9  Supplementary Appropriation (2025) Act
- 2025/22 Mobile Money Transaction Levy (Amendment) Act
- 2025/23 Companies (Amendment) Act
- 2025/24 Registration of Business Names (Amendment) Act
- 2025/25 Independent Broadcasting Authority Act
- 2025/26 Zambia National Broadcasting Corporation Act
- 2025/27 Betting Levy Act
- 2025/28 Appropriation Act
- 2025/29 Zambia Institute of Procurement and Supply Act

Cross-check vs `records/acts/`: **all 13 already in corpus**.

## Refresh probe — parliament /acts-of-parliament page 0

20 acts enumerated (matched via `Act No. N of YYYY` text pattern):

- 2026/1..11  (eleven acts)
- 2025/21..29 (nine acts)

Cross-check vs `records/acts/`: **all 20 already in corpus**.

## In-priority candidates (priority_order matches): 0

| Sub-phase                     | Modern (>=2017) novel | Notes |
|-------------------------------|-----------------------|-------|
| acts_in_force                 | 0                     | all 33 chronological-feed entries already on disk |
| sis_corporate                 | 0                     | alphabet exhaust complete (b0291..b0293) |
| sis_tax                       | 0                     | alphabet exhaust complete |
| sis_employment                | 0                     | alphabet exhaust complete |
| case_law_scz                  | n/a                   | judiciary scope (not in this probe) |
| sis_data_protection           | 0                     | upstream steady state |
| sis_mining                    | 0                     | alphabet exhaust complete |
| sis_family                    | 0                     | alphabet exhaust complete |

## robots.txt re-verification

| Source     | sha256 | Match |
|------------|--------|-------|
| zambialii  | `fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0` | yes (unchanged from b0193..b0297) |
| parliament | `278e83bcf567badfebcdea4d5d20ca9898e4449fe4eb2e3b5a08227b4ca9b762` | yes (unchanged from b0290..b0297) |

## SQLite

Not modified (no record writes; established disposition per b0192+ —
FTS5 vtable broken, journal held open). JSON records authoritative.

## B2 sync

Deferred to host (rclone not available in sandbox).

## Phase 4 status

`approvals.yaml -> phase_4_bulk -> complete` remains `false`. Worker
does NOT flip the flag.

After b0290..b0298, **every priority_order sub-phase is exhaustively
confirmed at upstream steady state** for the
`requests + beautifulsoup4 + pdfplumber` toolset, across all 22 active
alphabet listings on zambialii.org plus the chronological Acts feeds on
both zambialii and parliament.gov.zm.

## Coverage closure

Phase 4 cannot meaningfully advance further without one of:

1. **Add an OCR pipeline** (Tesseract or equivalent). Unblocks the
   OCR backlog (currently 21 items, including 1 in-priority
   sis_employment, 3 sis_tax, plus pre-existing acts and off-priority
   reserves).
2. **Approve a host-side rclone+chunked-PDF pipeline** for the 6-item
   oversize-pdf queue.
3. **Approve a multi-Act gazette splitter** for 2024/9.
4. **Define pre-2017 scope per sub-phase.** Modern (>=2017) era is
   exhausted across all priority sub-phases AND all alphabet listings.
5. **Expand priority_order** to include sis_road_traffic, sis_planning,
   sis_education, sis_diplomacy, sis_defence, sis_higher_education,
   sis_disaster_management, sis_climate, sis_emoluments, sis_industry,
   sis_governance, sis_energy, sis_archives, sis_elections,
   sis_forests — unlocking ad-hoc ingestion (most still hit OCR gating).

Until one of the above is actioned, future ticks (b0298+) will continue
to idle on phase_4_bulk with re-run probes that only re-confirm steady
state.

## Integrity

`_work/batch_0298_integrity.py` — **PASS**:

- C1: `records/sis/` JSON count = 539 (unchanged).
- C2: `records/acts/` JSON count = 1169 (unchanged).
- C3: zambialii robots.txt sha256 matches expected.
- C4: parliament robots.txt sha256 matches expected.
- C5: probe novel_true counts = 0 (zambialii) / 0 (parliament).
- C6: `records/` tree git-clean (no record JSON writes this tick).

CHECK: no_duplicate_IDs / amended_by_resolves / cited_authorities /
source_hash_matches — N/A this tick (zero record writes).

## Budget

- Today (2026-04-27 UTC) fetches at tick start: 80 (per costs.log)
- Today (2026-04-27 UTC) fetches at tick end:   84/2,000 (~4.2%)
  - This tick: 4 fetches.
    - zambialii robots + zambialii recent + parliament robots +
      parliament page 0 = 4 fetches.
- Tokens within budget.

## Cumulative

- Acts on disk: 1,169 (unchanged)
- SI records on disk: 539 (unchanged)
- Multi-act-gazette retry queue: 1 (unchanged: 2024/9)
- Oversize-pdf queue: 6 (unchanged: 2002/6, 2005/21, 2008/5, 2009/10, 2009/30, 2012/16)
- OCR section-tolerant retry queue: 6 (unchanged: 1988/32, 1994/40, 1995/33, 2004/6, 2008/9, 2009/7)
- OCR backlog: **21** (unchanged)
- Off-priority reserve: 1 unique novel (2020/7) — already in OCR backlog

## Disposition

Commit this tick:

- `scripts/batch_0298.py` (PICKS=[] documentation skeleton)
- `_work/batch_0298_*` (discover, recent HTML, parliament HTML,
  robots caches, integrity script, probe.json)
- `reports/batch-0298.md` (this file)
- `worker.log` appended (recovery log + tick close)
- `costs.log` appended (4 fetches recorded)

No record JSON files written. corpus.sqlite unchanged. raw/ unchanged.
gaps.md unchanged (no new gaps introduced).
