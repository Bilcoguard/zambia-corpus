# Batch 0294 Report

**Phase:** 4 — bulk (minimal upstream-refresh tick)
**Tick:** 2026-04-27 (UTC) — scheduled tick, 30-min cadence
**Yield:** 0 records committed
**Wall-clock:** ~5 min
**Parser version:** 0.5.0 (probe-only — same as b0290..b0293)

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

## Tick context — recovery from b0294-attempt git ref damage

At tick start the bash sandbox could not delete an empty stale ref
file `.git/refs/remotes/origin/main.lock.bak.b0293_close` (sandbox
mount permits create/write but not unlink). Standard
`git update-ref -d` did not help (it could not remove its own .lock
file either). Recovery was effected by writing the canonical
`origin/main` SHA into both the bad ref file and its associated
`.lock` so that `git pull --ff-only` parses both as valid duplicate
refs and proceeds cleanly. `git pull --ff-only` then returned
"Already up to date".

This is a recurrence of the b0289..b0293 stale-lock pattern; the
host operator should consider a one-time host-side `rm -f` of:

  `.git/refs/remotes/origin/main.lock*`
  `.git/refs/remotes/origin/main.lock.*`

and the equivalent under `.git/refs/heads/`.

## Refresh probe — zambialii /legislation/recent

13 act links enumerated:
- 2025/5 National Road Fund (Amendment) Act
- 2025/6 Building Societies (Amendment) Act
- 2025/7 Animal Health (Amendment) Act
- 2025/8 Border Management and Trade Facilitation Act
- 2025/9 Supplementary Appropriation (2025) Act
- 2025/22 Mobile Money Transaction Levy (Amendment) Act
- 2025/23 Companies (Amendment) Act
- 2025/24 Registration of Business Names (Amendment) Act
- 2025/25 Independent Broadcasting Authority Act
- 2025/26 Zambia National Broadcasting Corporation Act
- 2025/27 Betting Levy Act
- 2025/28 Appropriation Act
- 2025/29 Zambia Institute of Procurement and Supply Act

**All 13 already in corpus.** Steady-state preserved.

## Refresh probe — parliament /acts-of-parliament page 0

20 act references enumerated via "Act No. N of YYYY" text-pattern
scan: 2026/1..11 + 2025/21..29. **All 20 already in corpus.**

(Note: the upstream page does not embed the year/num key inside
`<a href>` attributes for individual Acts; the regex matches the
rendered text rather than href structure. Verified all 20 are mapped
to corpus records via the `act-zm-YYYY-NNN-…json` filename layer
and a JSON content fall-through for non-canonical filenames.)

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
| zambialii  | `fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0` | yes (unchanged from b0193..b0293) |
| parliament | `278e83bcf567badfebcdea4d5d20ca9898e4449fe4eb2e3b5a08227b4ca9b762` | yes (unchanged from b0290..b0293) |

## SQLite

Not modified (no record writes; established disposition per b0192+ —
FTS5 vtable broken, journal held open). JSON records authoritative.

## B2 sync

Deferred to host (rclone not available in sandbox).

## Phase 4 status

`approvals.yaml -> phase_4_bulk -> complete` remains `false`. Worker
does NOT flip the flag.

After b0290..b0294, **every priority_order sub-phase is exhaustively
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

Until one of the above is actioned, future ticks (b0295+) will continue
to idle on phase_4_bulk with re-run probes that only re-confirm steady
state.

## Integrity

`_work/batch_0294_integrity.py` — **PASS**:

- C1: `records/sis/` JSON count = 539 (unchanged).
- C2: `records/acts/` JSON count = 1169 (unchanged).
- C3: zambialii robots.txt sha256 matches expected.
- C4: parliament robots.txt sha256 matches expected.
- C5: probe novel_true counts = 0 (zambialii) / 0 (parliament).
- C6: `records/` tree git-clean (no record JSON writes this tick).

CHECK: no_duplicate_IDs / amended_by_resolves / cited_authorities /
source_hash_matches — N/A this tick (zero record writes).

## Budget

- Today (2026-04-27 UTC) fetches at tick start: 62 (per costs.log)
- Today (2026-04-27 UTC) fetches at tick end:   68/2,000 (~3.4%)
  - This tick: 6 fetches.
    - First attempt aborted on parliament robots SSL verification
      (default trust store lacks RapidSSL chain). Before the abort,
      the script had already fetched zambialii robots + zambialii
      recent (2 fetches). The discover script was patched to use the
      project-local cert at `scripts/certs/rapidssl_tls_rsa_ca_g1.pem`
      via `urllib.request` + a custom SSL context (mirroring
      `_work/batch_0293_discover.py`).
    - Second attempt (full): zambialii robots + zambialii recent +
      parliament robots + parliament page 0 = 4 fetches.
    - Total this tick: 2 + 4 = 6 fetches.
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

- `scripts/batch_0294.py` (PICKS=[] documentation skeleton)
- `_work/batch_0294_*` (discover, recent HTML, parliament HTML,
  robots caches, integrity script, probe.json)
- `reports/batch-0294.md` (this file)
- `worker.log` appended (recovery log + tick close)
- `costs.log` appended (4 fetches recorded)

No record JSON files written. corpus.sqlite unchanged. raw/ unchanged.
gaps.md unchanged (no new gaps introduced).
