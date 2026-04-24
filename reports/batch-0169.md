# Batch 0169 Report

**Date:** 2026-04-24T05:16:34Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 0
**Repeal-chain links applied:** 0
**Fetches (script):** 5
**Integrity:** PASS

## Strategy

Alphabetical-fallback probe pass per the batch-0168 next-tick plan. Five unresolved Cap. parents (Juveniles, Hire Purchase, Stamp Duties, Sale of Goods, Bills of Exchange) — already tried as nature=Act probes with 0 yield — are re-probed WITHOUT the nature=Act filter. Any /akn/zm/act/ links surfaced this way are screened against HEAD + the B-POL-ACT-1 title filter. PDF fallback disabled. MAX_RECORDS=2.

## Per-query results

| # | Query | ZambiaLII total-count | /akn/zm/act/ links in page 1 |
|---|-------|----------------------:|-----------------------------:|
| 1 | `juveniles act` | 163 | 3 |
| 2 | `hire purchase act` | 79 | 17 |
| 3 | `stamp duties act` | 130 | 32 |
| 4 | `sale of goods act` | 663 | 0 |
| 5 | `bills of exchange act` | 79 | 19 |

## Committed records

None — zero novel primary-Act candidates survived HEAD + title filters after the no-nature-filter alphabetical-fallback probe rotation.

## Novel candidates surviving filters

No novel /akn/zm/act/ primary-parent candidates surfaced for any of the five probe queries.

## Rejected candidates (novel but filtered)

| # | Year/Num | Title | Reason |
|---|----------|-------|--------|
| 1 | 2011/3 | Juveniles (Amendment) Act , 2011 | title contains 'amendment' (via query 'juveniles act') |
| 2 | 1994/17 | Stamp Duty (Repeal) Act , 1994 | title contains 'repeal' (via query 'stamp duties act') |
| 3 | 1990/32 | Stamp Duty (Amendment) Act , 1990 | title contains 'amendment' (via query 'stamp duties act') |
| 4 | 1992/8 | Stamp Duty (Amendment) Act , 1992 | title contains 'amendment' (via query 'stamp duties act') |
| 5 | 1984/3 | Stamp Duty (Amendment) Act , 1984 | title contains 'amendment' (via query 'stamp duties act') |

## Integrity checks
- CHECK 1 (batch unique IDs): PASS (no records to check)
- CHECK 2 (no HEAD collision): PASS (no records to check)
- CHECK 3 (source_hash matches raw on disk): PASS (no raw written)
- CHECK 4 (amended_by / repealed_by reference resolution): PASS (no records to check)
- CHECK 5 (required fields present): PASS (no records to check)

## Interpretation

Removing the `nature=Act` filter did NOT surface primary Cap. parents for Juveniles, Hire Purchase, Stamp Duties, Sale of Goods, or Bills of Exchange on ZambiaLII. Combined with the prior nature=Act probe-rotation 0-yield (batches 0167 – 0168), this strongly suggests these five pre-independence Cap. parents are **not indexed on ZambiaLII as standalone AKN documents**. ZambiaLII's current coverage concentrates on post-1964 Acts of Parliament; several pre-1964 English-derived Caps (e.g., Sale of Goods 1893 imperial, Bills of Exchange 1882 imperial) appear to have no dedicated AKN landing page.

## Next-tick plan

Pivot the Phase-4 acts-in-force sweep away from the five unresolved ZambiaLII-missing Cap. parents and toward the **Parliament of Zambia** acts listing (`https://www.parliament.gov.zm/acts-of-parliament`), which has already been used as a seed source in earlier batches. Alternative fallbacks: (a) Government Printer bound-volume lookups (no known web index), (b) deferring the five Caps to Phase-7 re-verification. Preserve gaps entries so the human reviewer can flag a policy decision.

## Raw snapshots

No raw record files written this batch (probe-only). B2 sync deferred to host (rclone not available in sandbox).

