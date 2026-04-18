# Batch 0133 Report

**Date:** 2026-04-18T07:44:22Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 8
**Fetches:** 10 (8 HTML + 2 PDF fallback)
**Integrity:** PASS (all 5 checks)

## Committed records

Targets drawn from batch 0132's next-tick list (O/P-block Acts) plus complementary oaths and probate/lotteries Acts. All located via direct ZambiaLII AKN URLs `/akn/zm/act/<year>/<num>` with PDF fallback where the AKN HTML returned zero sections.

| # | Title | Citation | Year | Sections | Source |
|---|-------|----------|------|----------|--------|
| 1 | Commissioners for Oaths Act, 1938 | Act No. 44 of 1938 | 1938 | 7 | ZambiaLII HTML |
| 2 | Official Oaths Act, 1990 | Act No. 4 of 1990 | 1990 | 12 | ZambiaLII HTML |
| 3 | Plant Breeder's Rights Act, 2007 | Act No. 18 of 2007 | 2007 | 78 | ZambiaLII PDF (HTML empty) |
| 4 | Occupational Health and Safety Act, 2010 | Act No. 36 of 2010 | 2010 | 62 | ZambiaLII PDF (HTML empty) |
| 5 | Probation of Offenders Act, 1953 | Act No. 15 of 1953 | 1953 | 18 | ZambiaLII HTML |
| 6 | Probates (Resealing) Act, 1936 | Act No. 22 of 1936 | 1936 | 8 | ZambiaLII HTML |
| 7 | Pharmacy and Poisons Act, 1940 | Act No. 38 of 1940 | 1940 | 27 | ZambiaLII HTML |
| 8 | State Lotteries Act, 1970 | Act No. 7 of 1970 | 1970 | 24 | ZambiaLII HTML |

**Total sections:** 236

## Integrity checks (batch scope)

- CHECK 1 (batch unique IDs): PASS — 8 distinct IDs
- CHECK 2 (no HEAD collision): PASS — none of the 8 IDs exist in HEAD tree
- CHECK 3 (source_hash matches raw on disk): PASS for all 8 records (6 against HTML, 2 against PDF)
- CHECK 4 (amended_by / repealed_by / cited_authorities reference resolution): PASS — no cross-references in this batch
- CHECK 5 (required fields present): PASS

## Record paths

- `records/acts/1938/act-zm-1938-044-commissioners-for-oaths-act-1938.json`
- `records/acts/1990/act-zm-1990-004-official-oaths-act-1990.json`
- `records/acts/2007/act-zm-2007-018-plant-breeders-rights-act-2007.json`
- `records/acts/2010/act-zm-2010-036-occupational-health-and-safety-act-2010.json`
- `records/acts/1953/act-zm-1953-015-probation-of-offenders-act-1953.json`
- `records/acts/1936/act-zm-1936-022-probates-resealing-act-1936.json`
- `records/acts/1940/act-zm-1940-038-pharmacy-and-poisons-act-1940.json`
- `records/acts/1970/act-zm-1970-007-state-lotteries-act-1970.json`

## Raw snapshots

All raw bytes saved to `raw/zambialii/<year>/<id>.{html|pdf}`. B2 sync deferred to host (rclone not available in sandbox).

## Fetch accounting

- 8 AKN HTML fetches (one per target)
- 2 PDF fetches (targets 3 & 4 where HTML returned zero AKN sections — Plant Breeder's Rights Act 2007 and Occupational Health and Safety Act 2010)
- Total: 10 content fetches this batch → today 30/2000 (well under cap).

## Notes / next tick

- Direct AKN URL construction (`/akn/zm/act/<year>/<num>`) proved effective for all 8 targets this batch, with ZambiaLII redirecting to the canonical `eng@<date>` URL.
- Two targets (Plant Breeder's Rights, Occupational Health and Safety 2010) returned AKN HTML with no parseable sections, but their `source.pdf` fallback (redirects to `media.zambialii.org` CDN) yielded complete structured text via pdfplumber.
- The original 2010 Occupational Health and Safety Act is the predecessor of the already-ingested 2025 replacement Act (act-zm-2025-016). A future tick should link `repealed_by` between them.
- Next batch targets (continuing through O/P-block and unfinished batch-0132 carryovers):
  - National Water Supply and Sanitation Act (retry — not present on `/legislation/?q=` under any query tried in batches 0132/0133; try subject-browse index or parliament.gov.zm)
  - Optometry Act (direct URL guessing or subject browse)
  - Open University Act (direct URL guessing or subject browse)
  - Organs of Government (Dispersal) Act
  - Oaths and Affirmations Act (if distinct from Commissioners for Oaths 1938 / Official Oaths 1990 ingested this batch)
  - Zambia Institute for Tourism and Hospitality Studies Act 2016 (Act No. 42 of 2016)
  - Patents Act 2016 (Act No. 40 of 2016)
  - Patents and Companies Registration Agency Act 2020 (Act No. 4 of 2020)

## Script note

The batch script `scripts/batch_0133.py` raised an integrity check FAIL exit code after records were already written — the script's `raw_map` lookup keyed on the literal substring `source.pdf`, but ZambiaLII redirects PDF fallback requests to `media.zambialii.org/.../<slug>-publication-document.pdf` URLs (no `source.pdf` substring). Re-ran integrity check inline with corrected raw-file lookup (endswith `.pdf` OR contains `source.pdf`). All 5 checks PASSED. Fix to be folded into the next batch script.

## Dirty-tree advisory (carry-forward)

The working tree continues to carry ~219 orphan untracked record JSONs and stale "deleted" index entries from pre-0130 ticks. This batch again used the `GIT_INDEX_FILE=<tmp>` workaround, seeding from HEAD and adding only this batch's outputs plus updated log files. Host-side cleanup still recommended per batch 0131 diagnostic in `worker.log`.

