# Batch 0143 Report

**Date:** 2026-04-19T16:33:01Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 8
**Fetches (script):** 8
**Integrity:** PASS

## Strategy

Fresh discovery block targeting courts / professions / old-colonial primary statutes not resolved in batches 0140–0142. Candidate (year, num) pairs were obtained by parsing the `results_html` payload of the ZambiaLII search API (`/search/api/documents/?search=<q>&nature=Act`) — the JSON `results` field is empty in current ZambiaLII builds, but the rendered-HTML fragment exposes first-result AKN URLs that can be matched against `/akn/zm/act/YYYY/NN`. Screening queries: 'Small Claims Courts', 'Subordinate Courts', 'Legal Practitioners', 'Societies', 'Mental Disorders', 'Witchcraft', 'Inquests', 'Births and Deaths'. Each top pick was dereferenced to its AKN page to fetch the canonical title and re-screen for amendment / appropriation markers (rejected if `(amendment)`, `amendment`, `appropriation`, or `repeal` appeared in the title). Eight primary-statute targets passed, all verified as NOT in HEAD by (year, num) tuple against `git ls-tree -r HEAD records/acts/`. Fetched via AKN URL pattern with PDF fallback when HTML returned fewer than 2 parsed sections.

## Committed records

| # | ID | Title | Citation | Sections | Source |
|---|----|-------|----------|----------|--------|
| 1 | `act-zm-1992-023-small-claims-courts-act-1992` | Small Claims Courts Act, 1992 | Act No. 23 of 1992 | 43 | HTML/AKN |
| 2 | `act-zm-1933-036-subordinate-courts-act-1933` | Subordinate Courts Act, 1933 | Act No. 36 of 1933 | 58 | HTML/AKN |
| 3 | `act-zm-1973-022-legal-practitioners-act-1973` | Legal Practitioners Act, 1973 | Act No. 22 of 1973 | 94 | HTML/AKN |
| 4 | `act-zm-1957-065-societies-act-1957` | Societies Act, 1957 | Act No. 65 of 1957 | 38 | HTML/AKN |
| 5 | `act-zm-1949-021-mental-disorders-act-1949` | Mental Disorders Act, 1949 | Act No. 21 of 1949 | 39 | HTML/AKN |
| 6 | `act-zm-1914-005-witchcraft-act-1914` | Witchcraft Act, 1914 | Act No. 5 of 1914 | 13 | HTML/AKN |
| 7 | `act-zm-1938-052-inquests-act-1938` | Inquests Act, 1938 | Act No. 52 of 1938 | 37 | HTML/AKN |
| 8 | `act-zm-1929-040-legitimacy-act-1929` | Legitimacy Act, 1929 | Act No. 40 of 1929 | 16 | HTML/AKN |

**Total sections:** 338

## Integrity checks
- CHECK 1 (batch unique IDs): PASS
- CHECK 2 (no HEAD collision): PASS
- CHECK 3 (source_hash matches raw on disk): PASS
- CHECK 4 (amended_by / repealed_by reference resolution): PASS — no cross-refs in this batch
- CHECK 5 (required fields present): PASS

## Raw snapshots

All raw bytes saved to `raw/zambialii/<year>/<id>.{html|pdf}`. B2 sync deferred to host (rclone not available in sandbox).

## Notes

- Small Claims Courts Act 1992/23 is the enabling statute for the small-claims division of the Subordinate Courts; still in force.
- Subordinate Courts Act 1933/36 is the parent statute for all subordinate (magistrates') courts — the base Cap 28 authority in the Laws of Zambia. Deeply cited in procedural case law.
- Legal Practitioners Act 1973/22 is the governing statute for LAZ, admissions, and the Disciplinary Committee. Cap 30 base.
- Societies Act 1957/65 governs registration of voluntary associations (Cap 119 base). Pre-independence but in force.
- Mental Disorders Act 1949/21 remains the principal mental-health statute absent a modern replacement — relevant to capacity questions in family and criminal law.
- Witchcraft Act 1914/5 is pre-independence colonial legislation but is still cited (Cap 90) — primary historical authority.
- Inquests Act 1938/52 governs coroners' inquests (Cap 36). Primary source for inquest procedure.
- Legitimacy Act 1929/40 — primary pre-independence Act governing legitimation of children; still referenced alongside the Affiliation and Maintenance of Children Act.
- Next tick: continue the pre-independence primary-statute sweep (Marriage Act variants, Chieftaincy / Chiefs Act, Public Order Act parent, Matrimonial Causes Act 2007, Industrial & Labour Relations Act parent), plus resume the N-P-R post-independence block (Postal Services Act 2009, Probate and Administration of Estates Act, Registered Designs parent Act if distinct from the 2010 statute already in HEAD).

