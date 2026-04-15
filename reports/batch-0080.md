# Batch 0080 Report

**Date:** 2026-04-15T10:20:00Z
**Phase:** 4 (Bulk Ingestion)
**Source:** ZambiaLII (zambialii.org)
**Records added:** 8
**Total sections:** 1,029
**Fetches:** 11 (8 HTML + 3 PDF fallbacks)

## Records

| ID | Title | Sections | Citation | Notes |
|----|-------|----------|---------|-------|
| act-zm-2021-033-cannabis-act | Cannabis Act, 2021 | 45 | Act No. 33 of 2021 | HTML extraction |
| act-zm-2022-012-children-s-code-act | Children's Code Act, 2022 | 298 | Act No. 12 of 2022 | HTML extraction |
| act-zm-2006-009-citizens-economic-empowerment-act | Citizens Economic Empowerment Act, 2006 | 0 | Act No. 9 of 2006 | Scanned PDF — 0 sections; logged to gaps.md |
| act-zm-2016-033-citizenship-of-zambia-act | Citizenship of Zambia Act, 2016 | 47 | Act No. 33 of 2016 | HTML extraction |
| act-zm-2016-005-civil-aviation-act | Civil Aviation Act, 2016 | 263 | Act No. 5 of 2016 | PDF extracted (pdfplumber) |
| act-zm-2012-007-civil-aviation-authority-act | Civil Aviation Authority Act, 2012 | 148 | Act No. 7 of 2012 | PDF extracted (pdfplumber) |
| act-zm-1970-063-co-operative-societies-act | Co-operative Societies Act, 1970 | 172 | Chapter 502 | HTML extraction |
| act-zm-1989-024-coffee-act | Coffee Act, 1989 | 56 | Chapter 235 | HTML extraction |

## Integrity Checks

- No duplicate IDs (batch and global): PASS
- Required fields present: PASS
- Source hashes match raw files: PASS (all 8 records)
- amended_by/repealed_by references: PASS (empty in this batch)
- Section structure valid: PASS

## Gaps / Notes

- **Citizens Economic Empowerment Act 2006**: ZambiaLII serves a scanned image PDF with no extractable text. 0 sections captured. Logged to gaps.md. Consider OCR or parliament.gov.zm for this act.
- **Civil Aviation Act 2016** and **Civil Aviation Authority Act 2012**: HTML pages have no AKN-structured sections; PDFs extracted successfully via pdfplumber.

## Corpus Totals

- **Total records:** 600 (acts + 1 judgment)
- **Total sections this batch:** 1,029
- **Fetches today:** 109/2000
- **ZambiaLII catalogue acts remaining:** ~382

## Next Batch Candidates

Cold Storage Board of Zambia (Dissolution) Act 1985, Combined Cadet Force Act 1964, Commercial Travellers (Special Provisions) Act 1966, Commissioners for Oaths Act 1938, Common Leasehold Schemes Act 1994, Companies (Certificates Validation) Act 1969, Companies Act 2017, Compensation Fund Act 2016
