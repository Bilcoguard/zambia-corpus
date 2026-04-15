# Batch 0088 Report
**Date:** 2026-04-15T15:11:03Z
**Phase:** 4 (Bulk Ingestion — acts_in_force)
**Source:** ZambiaLII (zambialii.org)
**Discovery:** Pagination pages 1-10 — previously untapped pages revealed ~403 new acts

## Records Added

| # | ID | Title | Sections | Source |
|---|-----|-------|----------|--------|
| 1 | act-zm-1912-016-gold-trade-act-1912 | Gold Trade Act, 1912 | 27 | PDF |
| 2 | act-zm-1914-015-lands-and-deeds-registry-act-1914 | Lands and Deeds Registry Act, 1914 | 181 | PDF |
| 3 | act-zm-1914-004-cotton-act-1914 | Cotton Act, 1914 | 3 | PDF |
| 4 | act-zm-1915-023-plumage-birds-protection-act-1915 | Plumage Birds Protection Act, 1915 | 9 | PDF |
| 5 | act-zm-1918-010-marriage-act-1918 | Marriage Act, 1918 | 69 | PDF |
| 6 | act-zm-1920-020-prevention-of-cruelty-to-animals-act-1920 | Prevention of Cruelty to Animals Act, 1920 | 26 | PDF |
| 7 | act-zm-1921-020-maintenance-orders-enforcement-act-1921 | Maintenance Orders (Enforcement) Act, 1921 | 29 | PDF |
| 8 | act-zm-1922-007-mashona-railway-company-limited-act-1922 | Mashona Railway Company Limited Act, 1922 | 10 | PDF |

**Total sections:** 354
**Fetches this batch:** 16 (8 HTML pages + 8 PDFs)
**Budget usage today:** ~227/2000 fetches

## Discovery Breakthrough
- Previous batches (0085-0087) reported ZambiaLII listing exhausted at 43 acts on page 0.
- This batch discovered that ZambiaLII pagination (?page=1 through ?page=10) is NOW WORKING, revealing 463 unique principal acts and 656 SIs across all pages.
- After cross-referencing with existing 641 records, ~403 acts remain to be ingested.
- This batch processes the first 8 from the newly-discovered pool (oldest acts first).
- All 8 acts are colonial-era legislation still on the Zambian statute books.
- SQLite rebuilt fresh (prior copy was corrupted) — 650 total records now indexed with FTS5.

## Integrity Checks
- No duplicate IDs (650 unique across corpus)
- All source_hash values match raw PDF files on disk
- No unresolved amended_by or repealed_by references
- All required fields present
- **ALL CHECKS PASS**

## B2 Sync
- rclone not available in sandbox — deferred to host
- Peter to run: rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4
