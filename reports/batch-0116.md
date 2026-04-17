# Batch 0116 Report

**Date:** 2026-04-17
**Phase:** 4 (Bulk Ingestion)
**Source:** ZambiaLII (zambialii.org)
**Records added:** 8
**Total sections:** 403
**Fetches:** 10
**Parser version:** 0.4.0

## Records

| # | ID | Title | Sections | Source |
|---|---|---|---|---|
| 1 | act-zm-1969-045-firearms-act-1969 | Firearms Act, 1969 | 54 | ZambiaLII HTML |
| 2 | act-zm-2020-003-food-nutrition-act-2020 | Food and Nutrition Act, 2020 | 31 | ZambiaLII HTML |
| 3 | act-zm-2010-019-forfeiture-proceeds-crime-act-2010 | Forfeiture of Proceeds of Crime Act, 2010 | 68 | ZambiaLII HTML |
| 4 | act-zm-2013-004-higher-education-act-2013 | Higher Education Act, 2013 | 108 | ZambiaLII PDF |
| 5 | act-zm-1964-060-interpretation-general-provisions-act-1964 | Interpretation and General Provisions Act, 1964 | 22 | ZambiaLII HTML |
| 6 | act-zm-1989-005-intestate-succession-act-1989 | Intestate Succession Act, 1989 | 26 | ZambiaLII HTML |
| 7 | act-zm-1973-023-law-association-zambia-act-1973 | Law Association of Zambia Act, 1973 | 12 | ZambiaLII HTML |
| 8 | act-zm-2023-003-examinations-council-zambia-act-2023 | Examinations Council of Zambia Act, 2023 | 82 | ZambiaLII PDF |

## Integrity checks

- [x] No duplicate IDs in batch
- [x] All source_hash values match raw files on disk
- [x] All required schema fields present
- [x] All amended_by / repealed_by references valid (none set)

## Notes

- Batch focused on high-value substantive Acts from ZambiaLII pages 6-7: criminal law (Firearms, Forfeiture), food/agriculture (Food & Nutrition), education (Higher Education, Examinations Council 2023), family law (Intestate Succession), legal profession (Law Association), and foundational law (Interpretation & General Provisions).
- Interpretation and General Provisions Act 1964 is a foundational statute for Zambian legal interpretation — high citation value.
- Higher Education Act 2013 and Examinations Council 2023 required PDF fallback (no AKN HTML sections available).
- 33 pre-existing Appropriation Act duplicates noted (year-subdirectory vs root-level copies). Cannot delete due to mounted filesystem permissions. Flagged for manual cleanup by Peter.

## Next batch targets

Continue with ZambiaLII pages 7-8: Judicial (Code of Conduct) Act 1999, Landlord and Tenant (Business Premises) Act 1971, Lands Act 1995, Lands Tribunal Act 2010, Ionising Radiation Protection Act 2005, Insurance (Fidelity Fund) Regulations 2021, Forfeiture of Proceeds of Crime (Fund and Property Management) Regulations 2023, Intestate Succession Rules 2023.
