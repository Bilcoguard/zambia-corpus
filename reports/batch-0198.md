# Batch 0198 — Phase 4 sis_tax continuation (alphabet=T)

**Started:** 2026-04-24T21:05:16Z
**Completed:** 2026-04-24T21:06:56Z
**Batch size:** 8 targets / 8 records written / 8 sis_tax ok
**Fetches (this tick):** 20

## Rationale

Continuing sis_tax per batch-0197 next-tick plan
("alphabet=M / alphabet=E / alphabet=T"). Live discovery this tick:

- robots.txt re-verified (sha256 prefix `fce67b697ee4ef44`, unchanged
  from batches 0193-0197; `/akn/zm/judgment/` and
  `/akn/zm/officialGazette/` remain Disallowed for `User-agent: *`;
  Crawl-delay 5s).
- alphabet=M: 50 SI links — all novel tax-keyword hits were
  district-council by-laws (Charcoal / Timber / Sand levies). None
  selected (sis_tax targets principal tax Acts, not council by-laws).
- alphabet=E: 50 SI links — zero novel tax SIs on the first page
  (Electoral Process / Electricity / Education / Environmental
  Management dominate).
- alphabet=T: 50 SI links — rich sis_tax yield. Selected 8 principal
  SIs: 1 x Tax Appeals Tribunal Rules + 1 x Tobacco Levy Regulations +
  6 x Taxation (Provisional Charging) Orders (2004-2009 series under
  Provisional Collection of Revenue Act Cap.324, annual Finance-Act
  companion orders).

Sub-phase rotation not triggered — alphabet=T alone cleared the
8-target batch at sis_tax yield >> 3.

## Records written

| SI | Title | sections | PDF bytes | sha256 prefix |
|----|-------|----------|-----------|---------------|
| 2022/037 | Tax Appeals Tribunal Rules, 2022 | 74 | 478117 | 6735d17a99ada7bd… |
| 2018/067 | Tobacco Levy Regulations, 2018 | 3 | 19381 | 1fa0838490ae80a4… |
| 2009/005 | Taxation (Provisional Charging) Order, 2009 | 1 | 154252 | 5550cf71e39e8e86… |
| 2008/015 | Taxation (Provisional Charging) Order, 2008 | 5 | 120149 | e953b4dab64f6d44… |
| 2007/020 | Taxation (Provisional Charging) Order, 2007 | 5 | 473024 | 588118d7549d653d… |
| 2006/004 | Taxation (Provisional Charging) Order, 2006 | 2 | 120527 | 4a2d254a34e1d16c… |
| 2005/010 | Taxation (Provisional Charging) Order, 2005 | 2 | 128972 | c4983a7399852810… |
| 2004/010 | Taxation (Provisional Charging) Order, 2004 | 2 | 117873 | cfa35250e186c1c0… |

## Integrity checks

- **CHECK1** (no duplicate IDs, all 8 record files on disk): PASS.
- **CHECK2** (source_hash == sha256 of on-disk raw PDF): PASS — all 8
  PDF SHA-256 values match.
- **CHECK3** (amended_by / repealed_by references resolve): PASS —
  all 8 records have empty xref lists (none asserted).
- **CHECK4** (cited_authorities reference resolves): n/a — parser
  0.5.0 does not emit this field; nothing to check.
- **CHECK5** (required fields populated: id, type, jurisdiction,
  title, citation, sections, source_url, source_hash, fetched_at,
  parser_version): PASS — all non-empty.

## Execution note

Executed in 4 slices of 2 targets each (0:2, 2:4, 4:6, 6:8) so each
`python3 scripts/batch_0198.py` invocation fits inside the sandbox's
45-second bash timeout. Discovery fetches logged once in slice 0:2;
monotonic `fetch_n` continuation across slices.

## Cumulative status (post-batch)

- SI records: 204 (+8 over batch 0197's 196).
- Judgment records: 25 (unchanged — `case_law_scz` still paused per
  robots.txt Disallow on `/akn/zm/judgment/`).
- sis_tax sub-phase: 65 records (+8 this batch).
- Provisional Charging Order series coverage (under Provisional
  Collection of Revenue Act Cap.324): 2004, 2005, 2006, 2007, 2008,
  2009 — a contiguous 6-year slice. Remaining on T alphabet page for
  future ticks: 1997-2003 plus 2000/007.

Today ~331/2000 fetches used (16.6 %). Inside budget.

## Next-tick plan

- **sis_tax continuation**: finish the Taxation (Provisional
  Charging) Order backlog (1997/015, 1998/016, 1999/014, 2000/007,
  2001/015, 2002/016, 2003/017) from the already-cached alphabet=T
  page — 7 targets, all pre-discovered.
- If sis_tax next-tick yield `< 3`, rotate to sis_employment
  (priority_order item 4) via alphabet=E probe (Employment Code Act
  2019/003 derivative SIs, minimum-wage orders) and alphabet=M
  probe (Minimum Wages orders).
- Re-verify robots.txt at start of next tick.

## Infrastructure follow-up (non-blocking)

- 16 raw files on disk from batch 0198 (8 HTML + 8 PDF) awaiting
  host-driven `rclone sync raw/ b2raw:kwlp-corpus-raw/` (rclone
  unavailable in tick sandbox).
- `corpus.sqlite` stale rollback-journal still blocks in-sandbox
  FTS rebuild.
- 34 legacy-schema act JSON dupes under `records/acts/` remain
  unresolved.
- 42 Appropriation-Act `-000-` placeholder duplicates remain for a
  future cleanup tick.
