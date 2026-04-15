# Batch 0087 Report

**Date:** 2026-04-15T14:45:00Z
**Phase:** 4 (Bulk Ingestion)
**Category:** acts_in_force (Appropriation Acts 1995-1999)
**Parser Version:** 0.4.2

## Records Added: 5

| # | ID | Title | Sections | Source |
|---|---|---|---|---|
| 1 | act-zm-1995-001-appropriation-act-1995 | Appropriation Act, 1995 | 3 | PDF |
| 2 | act-zm-1996-013-appropriation-act-1996 | Appropriation Act, 1996 | 1 | PDF |
| 3 | act-zm-1997-013-appropriation-act-1997 | Appropriation Act, 1997 | 2 | PDF |
| 4 | act-zm-1998-003-appropriation-act-1998 | Appropriation Act, 1998 | 2 | PDF |
| 5 | act-zm-1999-003-appropriation-act-1999 | Appropriation Act, 1999 | 2 | PDF |

**Total sections:** 10
**Fetches this batch:** 11 (5 HTML stub pages + 5 PDFs + 1 listing page)
**Budget usage today:** ~211/2000 fetches

## Notes
- Completes the Appropriation Act series 1980-1999 from ZambiaLII listing.
- All 5 acts had HTML stub pages (no AKN markup) — content extracted from PDF source files.
- Appropriation Acts are typically short (authorize expenditure from Consolidated Fund).
- ZambiaLII listing page 2 (`?page=1`) returned identical content to page 1 — no new acts discoverable via pagination.
- The current ZambiaLII listing shows only 43 principal acts. All 43 have now been ingested or attempted.
- **ZambiaLII listing exhausted for current pagination.** Future batches should explore alternative discovery: direct URL probing for known acts, Parliament of Zambia site, or Judiciary site for judgments.

## Discovery Status
- ZambiaLII listing page 0: 43 principal acts — all processed
- ZambiaLII pagination: broken (page 1 returns same as page 0)
- ~636 total acts in corpus (many discovered via prior pagination that is now broken)
- Remaining priority_order categories: sis_corporate, sis_tax, sis_employment, case_law_scz, sis_data_protection, sis_mining, sis_family
- **Recommend human review of target discovery strategy** — ZambiaLII listing pagination appears limited.

## Integrity Checks
- No duplicate IDs (642 unique across corpus)
- All source_hash values match raw PDF files on disk
- No unresolved amended_by or repealed_by references
- **ALL CHECKS PASS**

## B2 Sync
- rclone not available in sandbox — deferred to host
