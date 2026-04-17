# Batch 0127 Report

**Date:** 2026-04-17T14:30:00Z
**Phase:** 4 (Bulk Ingestion)
**Records:** 8
**Total sections:** 13
**Fetches:** 18 (8 HTML + 8 PDF + 2 listing pages)
**Source:** ZambiaLII (pages 8-9)

## Records

| # | Title | Type | SI No. | Sections | Source |
|---|-------|------|--------|----------|--------|
| 1 | Chiefs (Recognition) (No. 5) Order, 2003 | si | SI No. 35 of 2003 | 2 | [ZambiaLII](https://www.zambialii.org/akn/zm/act/si/2003/35/eng@2003-04-11) |
| 2 | Chiefs (Recognition) (No. 5) Order, 2004 | si | SI No. 9 of 2004 | 1 | [ZambiaLII](https://www.zambialii.org/akn/zm/act/si/2004/9/eng@2004-05-30) |
| 3 | Chiefs (Recognition) (No. 5) Order, 2005 | si | SI No. 46 of 2005 | 2 | [ZambiaLII](https://www.zambialii.org/akn/zm/act/si/2005/46/eng@2005-08-05) |
| 4 | Chiefs (Recognition) (No. 5) Order, 2006 | si | SI No. 37 of 2006 | 1 | [ZambiaLII](https://www.zambialii.org/akn/zm/act/si/2006/37/eng@2006-03-24) |
| 5 | Chiefs (Recognition) (No. 5) Order, 2007 | si | SI No. 55 of 2007 | 2 | [ZambiaLII](https://www.zambialii.org/akn/zm/act/si/2007/55/eng@2007-07-13) |
| 6 | Chiefs (Recognition) (No. 5) Order, 2008 | si | SI No. 44 of 2008 | 2 | [ZambiaLII](https://www.zambialii.org/akn/zm/act/si/2008/44/eng@2008-04-18) |
| 7 | Chiefs (Recognition) (No. 5) Order, 2009 | si | SI No. 42 of 2009 | 2 | [ZambiaLII](https://www.zambialii.org/akn/zm/act/si/2009/42/eng@2009-07-17) |
| 8 | Chiefs (Recognition) (No. 5) Order, 2010 | si | SI No. 32 of 2010 | 2 | [ZambiaLII](https://www.zambialii.org/akn/zm/act/si/2010/32/eng@2010-04-30) |

## Notes

- All 8 records are Chiefs Recognition Orders (SIs) from ZambiaLII pages 8-9. These are subsidiary legislation under the Chiefs Act, recognizing new chiefs.
- Initially classified as Acts by listing page URL pattern (`/akn/zm/act/si/`); corrected to SI type during post-processing.
- Old Act-classified files tombstoned in `records/acts/`; correct SI records saved to `records/sis/`.
- PDF sources were fetched for each order as the HTML pages had minimal section content.
- Low section counts (1-2 per record) are normal for these short gazetted orders.
- ~92 remaining unprocessed items on ZambiaLII pages 8-9, including substantive Acts (National Health Research Act 2013, National Prosecution Authority Act 2010, Non-Governmental Organisations Act 2009, National Payment Systems Act 2007, etc.) and additional Chiefs Recognition Orders.

## Integrity checks
- [x] No duplicate IDs in batch
- [x] No duplicate IDs vs corpus
- [x] All source_hash values well-formed
- [x] All required provenance fields present
- [x] No broken cross-references
