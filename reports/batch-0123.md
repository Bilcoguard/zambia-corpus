# Batch 0123 Report

**Date:** 2026-04-17
**Phase:** 4 (Bulk ingestion)
**Records added:** 2 (6 duplicates of batch 0122 detected and excluded)
**Total sections:** 17
**Integrity:** ALL PASS (batch records only; pre-existing Appropriation Act duplicates noted for manual cleanup)

## Records

| # | ID | Type | Year | Sections | Source |
|---|-----|------|------|----------|--------|
| 1 | si-zm-2005-028-loans-and-guarantees-authorisation-delegation-of-functions-order-2005 | SI | 2005 | 3 | ZambiaLII PDF |
| 2 | act-zm-1968-034-loans-kafue-gorge-hydro-electric-power-project-act-1968 | Act | 1968 | 14 | ZambiaLII PDF |

## Notes
- Scanned ZambiaLII page 8 for unprocessed items.
- 6 of 8 initial candidates were semantic duplicates of batch 0122 records (old-format IDs vs new standardized IDs). These 6 new-format files are NOT committed — the existing batch 0122 records are authoritative.
- Duplicate new-format files left on disk but not committed: si-zm-2022-016-*, act-zm-1966-020-*, si-zm-1966-353-*, si-zm-1966-293-*, si-zm-1969-297-*, si-zm-2021-010-*
- Pre-existing Appropriation Act duplicate files (records/acts/ root vs records/acts/YYYY/) remain for manual cleanup.
- Fetches this batch: 14
- ~55 remaining unprocessed items on page 8. Pages 9-10 have additional items.
- Next batch: need to build proper dedup index of ALL existing records (by source_url) before scanning listing pages, to avoid re-fetching already-ingested items.

## Fetches
- Fetches this batch: 14
- Today's total fetches: ~119/2000
