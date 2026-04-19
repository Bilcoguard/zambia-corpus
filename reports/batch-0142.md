# Batch 0142 Report

**Date:** 2026-04-19T08:39:35Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 8
**Fetches (script):** 11
**Integrity:** PASS

## Strategy

Continuation of the ZambiaLII AKN-URL ingestion from batches 0134–0141. Targets sourced from the leftover `_work/batch_0140_discovery.json` candidates (Road Traffic 2002/11, Local Courts 1966/20, Lotteries 1957/8, Electoral 1991/2) plus additional primary statutes resolved via the ZambiaLII search API (`/search/api/documents/?search=<q>&nature=Act`) for the N-P block (Medical and Allied Professions 1977/22, Workers' Compensation 1999/10, Employment 1965/57, Pharmaceutical 2004/14). Eight targets, all primary statutes (no amendment acts, no appropriation acts, no repeal-only acts), all verified as NOT in HEAD by (year, num) tuple against `git ls-tree -r HEAD records/acts/` before selection. Fetched via AKN URL pattern with PDF fallback when HTML returned fewer than 2 parsed sections.

## Committed records

| # | ID | Title | Citation | Sections | Source |
|---|----|-------|----------|----------|--------|
| 1 | `act-zm-2002-011-road-traffic-act-2002` | Road Traffic Act, 2002 | Act No. 11 of 2002 | 236 | PDF |
| 2 | `act-zm-1966-020-local-courts-act-1966` | Local Courts Act, 1966 | Act No. 20 of 1966 | 71 | HTML/AKN |
| 3 | `act-zm-1957-008-lotteries-act-1957` | Lotteries Act, 1957 | Act No. 8 of 1957 | 15 | HTML/AKN |
| 4 | `act-zm-1991-002-electoral-act-1991` | Electoral Act, 1991 | Act No. 2 of 1991 | 40 | HTML/AKN |
| 5 | `act-zm-1977-022-medical-and-allied-professions-act-1977` | Medical and Allied Professions Act, 1977 | Act No. 22 of 1977 | 69 | HTML/AKN |
| 6 | `act-zm-1999-010-workers-compensation-act-1999` | Workers' Compensation Act, 1999 | Act No. 10 of 1999 | 249 | PDF |
| 7 | `act-zm-1965-057-employment-act-1965` | Employment Act, 1965 | Act No. 57 of 1965 | 87 | HTML/AKN |
| 8 | `act-zm-2004-014-pharmaceutical-act-2004` | Pharmaceutical Act, 2004 | Act No. 14 of 2004 | 120 | PDF |

**Total sections:** 887

## Integrity checks
- CHECK 1 (batch unique IDs): PASS
- CHECK 2 (no HEAD collision): PASS
- CHECK 3 (source_hash matches raw on disk): PASS
- CHECK 4 (amended_by / repealed_by reference resolution): PASS — no cross-refs in this batch
- CHECK 5 (required fields present): PASS

## Raw snapshots

All raw bytes saved to `raw/zambialii/<year>/<id>.{html|pdf}`. B2 sync deferred to host (rclone not available in sandbox).

## Notes

- Road Traffic Act 2002/11 was flagged in batch 0141 as the repealer of the Roads and Road Traffic Act 1958/37 (already in HEAD). Both now in corpus — repeal-chain cross-ref links deferred to a future amendment-linking batch.
- Electoral Act 1991/2 is the direct predecessor of the Electoral Act 2006/12 (already in HEAD from batch 0141). Historical primary included for completeness — repeal-chain cross-refs deferred.
- Local Courts Act 1966/20 remains the governing statute for the subordinate local courts system; no repealer identified.
- Lotteries Act 1957/8 is pre-independence (colonial-era) legislation but remains in the Laws of Zambia (Cap 411 range) per ZambiaLII metadata.
- Medical and Allied Professions Act 1977/22 was largely superseded by the Health Professions Act 2009/24 (already in HEAD) and the Medical Laboratory Profession Act 2017; repeal-chain cross-refs deferred.
- Employment Act 1965/57 is the colonial/early-independence foundation of Zambian labour law; superseded in substantial part by the Employment Code Act 2019/3 (in HEAD). Historical primary preserved for section-level citation in legacy case law.
- Next tick: continue N-P-R block — National Assembly (Powers and Privileges) Cap 12 range, National Payment Systems 2007, Pensions and Insurance Authority Act predecessors, Postal Services Act 2009, Probate and Administration of Estates Act, Registered Designs Act, Rent Act. Discovery probes via ZambiaLII search API remain the preferred resolution path.

