# Batch 0293 Report

**Phase:** 4 — bulk (final-letter alphabet exhaust + upstream-acts refresh)
**Tick:** 2026-04-27 (UTC) — scheduled tick, 30-min cadence
**Yield:** 0 records committed
**Wall-clock:** ~17 min
**Parser version:** 0.5.0 (probe-only — same as b0291/0292)

## Summary

This tick closes the alphabet exhaust by probing the 7 remaining
uncovered high-yield letters (D, G, H, K, O, R, U) on zambialii and
refreshing two upstream Act listings (zambialii /legislation/recent and
parliament /acts-of-parliament page 0). 4 letters were intentionally
omitted (Q, X, Y, Z — empty/near-empty on this jurisdiction).

After this tick, **every Latin alphabet letter that produces SIs on
zambialii has been swept** for novel modern (>=2017) entries:

| Source batch | Alphabets swept |
|---|---|
| b0291 | A B C I M P S T V (9) |
| b0292 | E F J L N W (6) |
| **b0293** | **D G H K O R U (7)** |
| Total | 22 letters (Q, X, Y, Z omitted) |

**Result:** 0 in-priority candidates; 1 off-priority reserve item
(2020/7 sis_road_traffic — already in the OCR backlog from b0276).
Zero records committed.

This tick also confirms acts_in_force is at upstream steady state
through 2026/11 by re-fetching both the zambialii and parliament
upstream listings (all 13 + 20 entries already in corpus).

## Tick context — recovery from b0293-attempt-1 host-side lock

The first b0293 attempt (15:02Z) halted at `git pull --ff-only` due to
a stale `.git/refs/heads/main.lock.b0292_c_*` file inherited from the
batch-0292 commit cycle. Host operator cleared the stale locks before
this run; `git pull --ff-only` returned "Already up to date" cleanly.
No work bytes were spent in attempt 1 (probe never ran).

## Probes (zambialii alphabets — 7 letters)

| Alphabet | Total SI links | Modern (>=2017) | Novel (raw) | Novel (true*) | In-priority novel |
|---|---|---|---|---|---|
| D | 100 | 17 | 1 | 1 | 0 (off-priority sis_emoluments) |
| G | 84 | 12 | 1 | 1 | 0 (off-priority sis_climate)  |
| H | 101 | 16 | 4 | 4 | 0 (off-priority — Higher Education + High Court) |
| K | 74 | 1 | 0 | 0 | 0 |
| O | 77 | 4 | 0 | 0 | 0 |
| R | 125 | 22 | 21 | 1 | 0 (off-priority sis_road_traffic 2020/7) |
| U | 97 | 30 | 11 | 0 | 0 (all Urban-and-Regional-Planning already on disk under non-standard slugs) |

\* "Novel (true)" excludes records present on disk under non-standard
filenames (slug-only filenames lacking the canonical
`si-zm-YYYY-NNN-slug.json` form). Verified by reading
`citation` and `id` JSON fields for each on-disk SI record.

robots.txt sha256 (zambialii): `fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0` (unchanged from b0193..b0292; re-verified at tick start).
robots.txt sha256 (parliament): `278e83bcf567badfebcdea4d5d20ca9898e4449fe4eb2e3b5a08227b4ca9b762` (unchanged from b0290; re-verified at tick mid-run).

## Refresh probe — zambialii /legislation/recent

13 act links enumerated: 2025/5..9, 2025/22..29. **All 13 already in
corpus.** Steady-state preserved.

## Refresh probe — parliament /acts-of-parliament page 0

20 act references enumerated via "Act No. N of YYYY" text-pattern
scan: 2026/1..11 + 2025/21..29. **All 20 already in corpus.**

(Note: the upstream page does not embed the year/num key inside
`<a href>` attributes for individual Acts; the regex used in
b0290's parliament probe matches the rendered text rather than
href structure. Verified all 20 are mapped to corpus records by
cross-referencing `records/acts/**/act-zm-*.json` filenames + the
`Act No. N of YYYY` citation field for non-standard filenames.)

## In-priority candidates (priority_order matches): 0

After comprehensive existing-set check (regex-matched filenames + JSON
content fall-through for slug-only names), **zero** novel modern SIs
exist for any priority_order sub-phase across alphabets D/G/H/K/O/R/U.

Specifically:
- sis_corporate (item 2): empty.
- sis_tax (item 3): empty.
- sis_employment (item 4): empty.
- sis_data_protection (item 5): empty (the 2021/58 hit in raw probe is
  on disk: `records/sis/2021/si-zm-2021-058-data-protection-registration-and-licensing-regulations-2021.json`).
- case_law_scz (item 6): scope is judiciary, not zambialii SI listings;
  unaffected by this probe.
- sis_mining (item 7): empty.
- sis_family (item 8): empty.

## Off-priority reserve

| Year/Num | Title | Sub-phase | Status |
|---|---|---|---|
| 2020/7 | Road Traffic (Speed Limits) Regulations, 2019 | sis_road_traffic | **Already in OCR backlog** (b0276 — pdf_parse_empty / scanned image) |

The remaining off-priority discoveries from the raw 37-item probe set
were re-classified as already-in-corpus under non-standard filenames
(Urban and Regional Planning regulations, Diplomatic Immunities orders,
Defence Force regulations, Higher Education orders, Disaster Management
regulations, etc.). No new items added to gaps.md.

## SQLite

Not modified (no record writes; established disposition per b0192+ —
FTS5 vtable broken, journal held open). JSON records authoritative.

## B2 sync

Deferred to host (rclone not available in sandbox).

## Phase 4 status

`approvals.yaml -> phase_4_bulk -> complete` remains `false`. Worker
does NOT flip the flag.

After this tick, **every priority_order sub-phase is exhaustively
confirmed at upstream steady state** for the
`requests + beautifulsoup4 + pdfplumber` toolset, across all 22 active
alphabet listings on zambialii.org plus the chronological Acts feeds on
both zambialii and parliament.gov.zm.

## Coverage closure

Phase 4 cannot meaningfully advance further without one of:

1. **Add an OCR pipeline** (Tesseract or equivalent). Unblocks the
   OCR backlog (currently 21+ items, including 1 in-priority
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

Until one of the above is actioned, future ticks (b0294+) will continue
to idle on phase_4_bulk with re-run probes that only re-confirm steady
state.

## Integrity

`_work/batch_0293_integrity.py` — **PASS**:

- C1: `records/sis/` JSON count = 539 (unchanged).
- C2: `records/acts/` JSON count = 1169 (unchanged).
- C3: All 7 alphabet HTMLs cached and parseable (74-125 <a> links each).
- C4: zambialii robots.txt sha256 matches expected.
- C5: parliament robots.txt sha256 matches expected.
- C6: probe.picks raw = 1; probe.picks true (after comprehensive
  existing-set) = 0. (The 1 raw pick was 2021/58 sis_data_protection,
  on disk under canonical filename; key-extraction regex in
  discover.py mistakenly produced a "novel" classification — confirmed
  in corpus during integrity recheck.)
- C7: No record JSON writes in this tick.

CHECK: no_duplicate_IDs / amended_by_resolves / cited_authorities /
source_hash_matches — N/A this tick (zero record writes).

## Budget

- Today (2026-04-27 UTC) fetches at tick start: 50 (per costs.log)
- Today (2026-04-27 UTC) fetches at tick end:   ~62/2,000 (~3.1%)
  - Breakdown this tick: 1 zambialii robots + 1 zambialii recent + 7
    alphabet listings (D,G,H,K,O,R,U) + 1 parliament robots + 1
    parliament page0 + 1 robots-recovery (recovery from in-flight
    timeout in attempt 2) = 12 fetches.
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

- `scripts/batch_0293.py` (PICKS=[] documentation skeleton)
- `_work/batch_0293_*` (discover, alphabet HTMLs, probe.json,
  parliament HTML, robots caches, integrity script, log)
- `gaps.md` updated (Batch 0293 section appended — alphabet exhaust
  closure note)
- `reports/batch-0293.md` (this file)
- `worker.log` appended (includes prior 0293-attempt-1 host-lock log
  block which was on the working tree at tick start)
- `costs.log` appended (12 fetches recorded)

No record JSON files written. corpus.sqlite unchanged. raw/ unchanged.
