# Batch 0138 Report

**Date:** 2026-04-19T04:35:31Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 8
**Fetches (script):** 8
**Integrity:** PASS

## Strategy

Continuation of the alphabetical-listing-first strategy from batches 0134–0137. H/I block targets picked up after "Gwembe District Special Fund (Dissolution) Act, 1968" in the ZambiaLII /legislation/ alphabetical ordering — Higher Authority for Power (Special Provisions) 1970/41, Home Guard 1971/32, Honours and Decorations (Prevention of Abuses) 1967/5, Hotels 1987/27, Human Rights Commission 1996/39, Immigration and Deportation 2010/18, Income Tax 1967/32, Industrial and Labour Relations 1993/27. Fetched via AKN URL pattern with PDF fallback when HTML returned fewer than 2 parsed sections.

## Committed records

| # | ID | Title | Citation | Sections | Source |
|---|----|-------|----------|----------|--------|
| 1 | `act-zm-1970-041-higher-authority-for-power-special-provisions-act-1970` | Higher Authority for Power (Special Provisions) Act, 1970 | Act No. 41 of 1970 | 5 | HTML/AKN |
| 2 | `act-zm-1971-032-home-guard-act-1971` | Home Guard Act, 1971 | Act No. 32 of 1971 | 33 | HTML/AKN |
| 3 | `act-zm-1967-005-honours-and-decorations-prevention-of-abuses-1967` | Honours and Decorations (Prevention of Abuses), 1967 | Act No. 5 of 1967 | 8 | HTML/AKN |
| 4 | `act-zm-1987-027-hotels-act-1987` | Hotels Act, 1987 | Act No. 27 of 1987 | 29 | HTML/AKN |
| 5 | `act-zm-1996-039-human-rights-commission-act-1996` | Human Rights Commission Act, 1996 | Act No. 39 of 1996 | 27 | HTML/AKN |
| 6 | `act-zm-2010-018-immigration-and-deportation-act-2010` | Immigration and Deportation Act, 2010 | Act No. 18 of 2010 | 63 | HTML/AKN |
| 7 | `act-zm-1967-032-income-tax-act-1967` | Income Tax Act, 1967 | Act No. 32 of 1967 | 227 | HTML/AKN |
| 8 | `act-zm-1993-027-industrial-and-labour-relations-act-1993` | Industrial and Labour Relations Act, 1993 | Act No. 27 of 1993 | 113 | HTML/AKN |

**Total sections:** 505

## Integrity checks
- CHECK 1 (batch unique IDs): PASS
- CHECK 2 (no HEAD collision): PASS
- CHECK 3 (source_hash matches raw on disk): PASS
- CHECK 4 (amended_by / repealed_by reference resolution): PASS — no cross-refs in this batch
- CHECK 5 (required fields present): PASS

## Raw snapshots

All raw bytes saved to `raw/zambialii/<year>/<id>.{html|pdf}`. B2 sync deferred to host (rclone not available in sandbox).

## Notes

- Next tick: continue alphabetical /legislation/?page= discovery through the I–L block — Income Tax (Special Provisions) 1982/3 and 1988/16, Industrial Hemp 2021/34, Industrial Relations 1990/36 (per _work/batch_0135_discovery.json), then Intestate Succession, Judicature Administration, Juries, Juveniles, Labour, Lands, Legal Practitioners if present.
- Deferred for dedicated batches: Constitution of Zambia Act, 1996 (1996/17); the full Appropriation / Excess Expenditure Appropriation series.

