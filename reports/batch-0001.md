# Phase 4 Batch 0001 — acts_in_force (parliament.gov.zm)

**Started:** 2026-04-10T09:35:15Z
**Finished:** 2026-04-10T09:44:35Z (approx; script timed-out after producing all records)
**Fetches this batch:** 50 (7 listing pages + 21×2 node+PDF fetches, plus 1 node fetch cut off at timeout)
**Records created:** 21
**Integrity checks:** ALL PASS (run post-timeout before commit)

## Summary

Walked listing pages 1–7 of parliament.gov.zm/acts-of-parliament (pages 0, 8–12 were
cached from prior sessions). Full inventory: 259 act candidates across pages 0–12. Fetched
and parsed 21 acts from the 2024–2025 tranche plus the Constitution Amendment Act 2016.

Source note: parliament.gov.zm node pages carry only the bare act number (e.g. "24"),
not the "No. X of YYYY" form. Citations were rebuilt post-parse using the full
"Act No. X of YYYY" form extracted from the listing HTML titles. One record (Constitution
Amendment Act 2016, node/4834) lacked a matching listing-page title with the full pattern;
its citation "Act No. 2 of 2016" was extracted from the PDF via the pilot parser.

## Records Created

| ID | Citation | Title | Sections | PDF (bytes) |
|----|----------|-------|----------|-------------|
| act-zm-2016-002-constitution-2016 | Act No. 2 of 2016 | Constitution Amendment Act 2016 | 36 | 228,076 |
| act-zm-2024-022-income-tax-2024 | Act No. 22 of 2024 | Income Tax (Amendment) Act, 2024 | 16 | 321,518 |
| act-zm-2024-023-value-added-tax-2024 | Act No. 23 of 2024 | Value Added Tax (Amendment) Act, 2024 | 2 | 12,992 |
| act-zm-2024-024-customs-excise-2024 | Act No. 24 of 2024 | Customs and Excise (Amendment) Act, 2024 | 8 | 361,794 |
| act-zm-2024-025-moblie-money-transactions-levy-2024 | Act No. 25 of 2024 | The Moblie Money Transactions Levy Act, 2024 | 14 | 382,152 |
| act-zm-2024-026-revenue-authority-2024 | Act No. 26 of 2024 | Zambia Revenue Authority (Amendment) Act, 2024 | 2 | 282,729 |
| act-zm-2024-027-property-transfer-tax-2024 | Act No. 27 of 2024 | Property Transfer Tax (Amendment) Act, 2024 | 2 | 13,234 |
| act-zm-2024-028-insurance-premium-levy-2024 | Act No. 28 of 2024 | Insurance Premium Levy (Amendment) Act, 2024 | 2 | 283,984 |
| act-zm-2024-029-appropriation-2024 | Act No. 29 of 2024 | The Appropriation Act, 2024 | 1 | 336,314 |
| act-zm-2024-030-antiterrorism-nonproliferation-2024 | Act No. 30 of 2024 | The Anti-Terrorism and Non-Proliferation (Amendment) Act, 2024 | 41 | 484,097 |
| act-zm-2025-001-plant-health-2025 | Act No. 1 of 2025 | The Plant Health Act, 2025 | 76 | 227,786 |
| act-zm-2025-002-geological-minerals-development-2025 | Act No. 2 of 2025 | The Geological Minerals Development Act, 2025 | 21 | 419,927 |
| act-zm-2025-003-cyber-security-2025 | Act No. 3 of 2025 | The Cyber Security Act, 2025 | 92 | 477,682 |
| act-zm-2025-004-cyber-crime-2025 | Act No. 4 of 2025 | The Cyber Crime Act, 2025 | 35 | 350,455 |
| act-zm-2025-005-national-road-fundamendment-2025 | Act No. 5 of 2025 | The National Road Fund (Amendment) Act, 2025 | 3 | 12,113 |
| act-zm-2025-006-building-societies-2025 | Act No. 6 of 2025 | The Building Societies (Amendment) Act, 2025 | 3 | 11,577 |
| act-zm-2025-007-animal-health-act2025 | Act No. 7 of 2025 | The Animal Health (Amendment) Act, 2025 | 4 | 12,014 |
| act-zm-2025-008-border-management-trade-facilitation-act2025 | Act No. 8 of 2025 | The Border Management And Trade Facilitation Act, 2025 | 175 | 441,027 |
| act-zm-2025-009-supplementary-appropriation2025-2025 | Act No. 9 of 2025 | The Supplementary Appropriation (2025) Act, 2025 | 2 | 18,038 |
| act-zm-2025-010-income-tax-act2025 | Act No. 10 of 2025 | The Income Tax (Amendment) Act, 2025 | 5 | 13,309 |
| act-zm-2025-011-customs-exciseamendmentact | Act No. 11 of 2025 | The Customs And Excise (Amendment) Act, 2025 | 8 | 19,627 |

## Parse quality flags

Records with ≤ 2 sections extracted — generic parser may have missed section headings.
Flagged in gaps.md for re-parse pass:

- act-zm-2024-023-value-added-tax-2024 (2 sections)
- act-zm-2024-026-revenue-authority-2024 (2 sections)
- act-zm-2024-027-property-transfer-tax-2024 (2 sections)
- act-zm-2024-028-insurance-premium-levy-2024 (2 sections)
- act-zm-2024-029-appropriation-2024 (1 section — Appropriation Acts are schedule-heavy; expected)
- act-zm-2025-009-supplementary-appropriation2025-2025 (2 sections)

## Inventory status

Total act candidates discovered (pages 0–12 of 48): 259
Pages not yet walked (13–47): 35 pages, estimated 700+ further acts
Records already in corpus before batch: 2 (Companies Act 2017 pilot + Konkola judgment)
Records added this batch: 21
Acts remaining from pages 0–12 (excluding already ingested): ~237
Acts on pages 13–47 (not yet fetched): est. ~700

## Source integrity

All 21 new records passed:
- No duplicate IDs
- All source_hash values verified against on-disk raw PDF files
- All amended_by references resolve (all arrays are empty at this stage)
- All cited_authorities references resolve (not applicable — type=act)
- JSON schema validation (Draft 2020-12): PASS for all 21 records

## Next batch recommendation

Batch 0002 should continue acts_in_force from pages 0–12 inventory (approximately 237
remaining candidates) and also begin walking listing pages 13–47 to extend the inventory.
Consider a re-parse pass for the 6 low-section records above once a better section-heading
regex is developed for schedule-heavy acts (Appropriation, Amendment stubs).
