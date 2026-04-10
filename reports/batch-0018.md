# Batch Report 0018

**Date:** 2026-04-10
**Phase:** 4 (Bulk Acts Ingest)
**Batch:** 0018
**Records:** +8 acts (2026 No. 2-9)

## Acts Processed

| Citation | Title | Sections | Source Hash |
|----------|-------|----------|-------------|
| Act No. 2 of 2026 | The Disaster Management (Amendment) Act, 2026 | 13 | `sha256:de031aac5c16bc1a1e` |
| Act No. 3 of 2026 | The Immigration Control Act, 2026 | 78 | `sha256:e83676cd9a163bfdbf` |
| Act No. 4 of 2026 | The Criminal Procedure Code (Amendment) Act, 2026 | 4 | `sha256:abefa37079c088026f` |
| Act No. 5 of 2026 | The National Payment System Act, 2026 | 153 | `sha256:dac92c5d4b57373480` |
| Act No. 6 of 2026 | The Food Reserve Act, 2026 | 33 | `sha256:4f00fef61365c9c149` |
| Act No. 7 of 2026 | The Agricultural Credits and Warehouse Receipts Act, 2026 | 85 | `sha256:f0f5932c1b5cf2cfc9` |
| Act No. 8 of 2026 | The Agricultural Marketing Act, 2026 | 37 | `sha256:27991e63e65ba59739` |
| Act No. 9 of 2026 | The Banking and Financial Services Act, 2026 | 214 | `sha256:9b9baf44e4ecd683e5` |

## Parse Quality Notes

- **act-zm-2026-004-criminal-procedure-code-amendment-act** (4 sections): Amendment act — short form expected; flagged for re-parse to verify completeness.

## Budget

- Fetches this batch: 16 (8 node pages + 8 PDFs)
- robots.txt crawl-delay: 10s honoured
- Total fetches today (2026-04-11): 16/2000

## Integrity Checks

- No duplicate IDs: ✓
- Source hash verification: ✓ (all 8 PDFs verified)
- Provenance fields complete: ✓
- No fabricated citations: ✓

## Notable Acts

- **The Banking and Financial Services Act, 2026 (Act No. 9 of 2026)**: 214 sections — major financial legislation (123 PDF pages, 1.4MB)
- **The National Payment System Act, 2026 (Act No. 5 of 2026)**: 153 sections — comprehensive payment system regulation
- **The Agricultural Credits and Warehouse Receipts Act, 2026 (Act No. 7 of 2026)**: 85 sections
- **The Immigration Control Act, 2026 (Act No. 3 of 2026)**: 78 sections

## Workaround Note

git pull --ff-only failed on mounted workspace (FUSE/APFS lock file issue — same as all prior ticks).
Used /tmp clone at HEAD=09e84ca (batch 0017 confirmed). This is the established workaround;
the main workspace .git lock files cannot be deleted from the sandbox.
