# Batch 0199 — Phase 4 sis_tax continuation (Provisional Charging Order backlog 1997-2003)

**Started:** 2026-04-24T21:34:30Z
**Completed:** 2026-04-24T21:39:30Z
**Batch size:** 7 targets / 7 records written / 7 sis_tax ok
**Fetches (this tick):** 15 (1 discovery robots.txt + 14 ingest HTML+PDF pairs)

## Rationale

Continuing sis_tax per batch-0198 next-tick plan: "finish the Taxation
(Provisional Charging) Order backlog (1997/015, 1998/016, 1999/014,
2000/007, 2001/015, 2002/016, 2003/017) from the already-cached
alphabet=T page — 7 targets, all pre-discovered."

All 7 are principal Orders made under the Provisional Collection of
Revenue Act Cap. 324, the annual Finance-Act companion that gives the
Minister authority to charge taxes provisionally between the Budget
speech and Royal Assent of the year's Income Tax / Customs / VAT
amendment Acts. With the 6-Order contiguous slice 2004-2009 captured
in batch-0198, this batch closes the 1997-2009 series — a contiguous
13-year run from the start of the AKN-Z slug coverage on ZambiaLII for
this SI series.

Discovery this tick:
- robots.txt re-verified live (sha256 prefix `fce67b697ee4ef44`,
  unchanged from batches 0193-0198; `/akn/zm/judgment/` and
  `/akn/zm/officialGazette/` remain Disallowed for `User-agent: *`;
  Crawl-delay 5s; worker uses 6s with margin).
- alphabet=T page already cached from batch-0198
  (`_work/batch_0198_alphabet_T.html`); all 7 backlog targets
  pre-discovered there. No new alphabet probe needed this tick.

## Records written

| SI | Title | sections | PDF bytes | sha256 prefix |
|----|-------|----------|-----------|---------------|
| 1997/015 | Taxation (Provisional Charging) Order, 1997 | 7 | 106 273 | 5756836f2dc30885… |
| 1998/016 | Taxation (Provisional Charging) Order, 1998 | 7 | 124 286 | 540620db60955336… |
| 1999/014 | Taxation (Provisional Charging) Order, 1999 | 2 | 106 495 | e1e86306fb0ec6e3… |
| 2000/007 | Taxation (Provisional Charging) Order, 2000 | 2 | 647 600 | c18c43135bacbcd4… |
| 2001/015 | Taxation (Provisional Charging) Order, 2001 | 2 | 321 420 | 234eaa2bdbad48e2… |
| 2002/016 | Taxation (Provisional Charging) Order, 2002 | 3 | 746 760 | 782175d66e40cfcd… |
| 2003/017 | Taxation (Provisional Charging) Order, 2003 | 2 | 137 598 | edec5c7697d09b58… |

## Integrity checks

- **CHECK1** (no duplicate IDs, all 7 record files on disk): PASS — 7
  unique batch ids, all present in HEAD (`records/sis/**/*.json` =
  211 total post-batch).
- **CHECK2** (amended_by / repealed_by references resolve): PASS —
  all 7 records have empty xref lists (none asserted).
- **CHECK3** (cited_authorities reference resolves): n/a — parser
  0.5.0 does not emit this field.
- **CHECK4** (source_hash == sha256 of on-disk raw PDF): PASS — all 7
  PDF SHA-256 values match.
- **CHECK5** (required fields populated): PASS — all of id, type,
  jurisdiction, title, citation, sections, source_url, source_hash,
  fetched_at, parser_version are non-empty.

## Execution note

Executed in 4 slices of 2/2/2/1 targets (0:2 with `--log-robots`, 2:4,
4:6, 6:7 with `--final`) so each `python3 scripts/batch_0199.py`
invocation fits inside the sandbox's 45-second bash timeout.
Crawl-delay 6s enforced between all live fetches; monotonic `fetch_n`
continuation across slices.

## Cumulative status (post-batch)

- SI records: 211 (+7 over batch 0198's 204).
- Judgment records: 25 (unchanged — `case_law_scz` still paused per
  robots.txt Disallow on `/akn/zm/judgment/`).
- sis_tax sub-phase: 72 records (+7 this batch).
- Provisional Charging Order series coverage (under Provisional
  Collection of Revenue Act Cap. 324): 1997, 1998, 1999, 2000, 2001,
  2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009 — a contiguous
  13-year slice. Series exhausted on the alphabet=T page (no
  additional Orders earlier than 1997 listed there).

Today ~346/2000 fetches used (17.3 %). Inside budget.

## Next-tick plan

Provisional Charging Order series exhausted in AKN-Z coverage. Per
batch-0198 fallback rule, sis_tax yield will drop sharply on the next
tick — rotate to **sis_employment** (priority_order item 4):

- Re-verify robots.txt at start of tick.
- Probe alphabet=E (Employment Code Act 2019/003 derivative SIs,
  Employment Statutory Orders) and alphabet=M (Minimum Wages and
  Conditions of Employment orders for General Workers, Shop Workers,
  Domestic Workers).
- Parent-Act back-reference probe on Employment Code Act
  /akn/zm/act/2019/3 for derivative SIs.
- If sis_employment yield ≥ 3 select up to 8; otherwise rotate to
  sis_data_protection (priority_order item 6) via Data Protection Act
  2021/3 derivative SIs.

## Infrastructure follow-up (non-blocking)

- 14 raw files on disk from batch 0199 (7 HTML + 7 PDF) plus the
  batch-0199 robots.txt cache awaiting host-driven
  `rclone sync raw/ b2raw:kwlp-corpus-raw/` (rclone unavailable in
  tick sandbox).
- `corpus.sqlite` stale rollback-journal still blocks in-sandbox
  FTS rebuild.
- 34 legacy-schema act JSON dupes under `records/acts/` remain
  unresolved.
- 42 Appropriation-Act `-000-` placeholder duplicates remain for a
  future cleanup tick.
- 63 SI records still living at the top level of `records/sis/`
  (legacy flat layout) rather than `records/sis/<year>/` — does not
  affect integrity but flagged for a future re-shelving tick.
