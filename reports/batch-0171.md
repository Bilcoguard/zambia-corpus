# Batch 0171 — Phase 4 bulk ingestion

Run: 2026-04-24T07:09:35Z

## Summary

+1 Act via parliament.gov.zm direct PDF ingest (ZambiaLII AKN 404 pivot).

| id | title | year/num | sections | source |
|---|---|---|---|---|
| act-zm-2021-038-the-insurance-act-2021 | The Insurance Act, 2021 | 2021/038 | 210 | parliament.gov.zm PDF |

## Discovery

Re-parse of cached raw/discovery/parliament-zm/acts-of-parliament-page-1..12.html against refreshed existing_acts.txt (898 Acts in HEAD) surfaced 19 novel (year,num) slots not in HEAD. After B-POL-ACT-1 title filter (+OCR variants) only 1 survived as primary Act: 2021/038 Insurance Act, 2021.

18 rejects by B-POL-ACT-1: 13× amendment, 3× appropriation/supplementary, and 2× (not rejected but already gapped by 0170).

## Ingest

- HTML: https://www.parliament.gov.zm/node/9009  
  sha256: 35d603cca165c125cb1a87fc7665808b9344c31108ef33f2122f562ed9473f42  
  fetched_at: 2026-04-24T07:07:17Z
- PDF : https://www.parliament.gov.zm/sites/default/files/documents/acts/Act%20No.%2038%20OF%202021%2C%20THE%20INSURANCE%20ACTpdf_0.pdf  
  sha256: 60bdde20bff76395633c2805df443bafd7c968d27a1daec1844980d70da007b0  
  fetched_at: 2026-04-24T07:07:41Z

Authoritative title taken from parliament.gov.zm node <title> element ("The Insurance Act, 2021"); PDF header-line text contained the running header "Insurance [No. 38 of 2021 415" and was therefore not authoritative for the title claim.

## Integrity checks

- CHECK 1 (id uniqueness): PASS — act-zm-2021-038-the-insurance-act-2021 not in HEAD.
- CHECK 2 (year/num prefix uniqueness): PASS — no act-zm-2021-038-* in HEAD.
- CHECK 3 (source_hash matches raw/): PASS — sha256:60bdde20bff76395... on disk.
- CHECK 4 (amended_by / repealed_by / cited_authorities resolution): PASS — no cross-refs in this record.
- CHECK 5 (required fields): PASS — all present; 210 sections.

## Gaps

2021/38 formerly a gap (batch 0170, ZambiaLII AKN 404). This batch closes that gap via parliament.gov.zm primary-source fallback.

## Next tick

Parliament.gov.zm listing (12 pages, 238 unique Acts, fetched 2026-04-10) is now exhausted of primary-Act candidates against HEAD. Remaining 18 rejects are Amendment / Appropriation / Supplementary instruments, out of scope under B-POL-ACT-1.

Pivot options (in order of preference):
  1. Resume ZambiaLII probe with new keyword families (education, health services, social welfare, land tenure, customary property, mining variants, environmental variants).
  2. Try government printer (printer.gov.zm) or MOJ (moj.gov.zm) Acts catalogue.
  3. Try judiciary.gov.zm legislation tab.
  4. Expand cadastre/sector-specific ministry catalogues (MMMD, MOF, MCTI, MOH).

Also: recent parliament.gov.zm listing page 1 may have updates — consider a single HEAD-probe of page 1 to detect post-2021/53 additions (Acts passed in 2022-2025 that may not appear in the April-10 cache).
