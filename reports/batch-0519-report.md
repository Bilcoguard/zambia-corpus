# Batch 0519 — Judgment Ingestion Report

**Date:** 2026-05-04 (UTC)
**Worker:** judgment-ingestion-worker (7th substantive tick)
**Time budget:** within 20-minute tick window
**Fetch budget today:** 70/500 (well within budget)

## Summary

- **Records written:** 1
- **Records deferred:** 7 (all `html_no_summary_pdf_no_match` — interpretive-ratio family)
- **404 confirmed:** 0 (within sweep) + 17 boundary probes
- **Judges added/updated:** 0 new canonical (3 existing re-confirmed: Hamaundu, Mutuna, Chisanga JJS)
- **Integrity assertions:** 30/30 PASS
- **corpus.sqlite:** records 1816→1817, judgments_meta 127→128

## Work performed

### (a) ZMSC 2024 closeout
Fetched the final 2 nums {2, 1}:
- `zmsc/2024/2` (2024-04-19) — abuse-of-office interpretive ratio (Director using government vehicle for private consultancy) → **deferred**
- `zmsc/2024/1` (2024-03-20) — chieftaincy declaratory question (Bundabunda succession) → **deferred**

ZMSC 2024 final tally: 22 written / 12 deferred / 1 404 across 35 attempts (target nums 1..34, num 4 confirmed gap in cadastre numbering).

### (b) ZMSC 2023 upper-boundary probe
17 HEAD probes confirmed `max_num = 23` for ZMSC 2023:
- 200 OK: nums 1, 10, 20, 21, 22, 23
- 404: nums 24, 25, 26, 27, 28, 29, 30, 35, 38, 40, 42, 44, 45, 47, 48, 49, 50

### (c) ZMSC 2023 most-recent-first sweep
Fetched 6 nums {23, 22, 21, 20, 19, 18}; all 200 OK.

| Num | Date | Outcome | Status |
|-----|------|---------|--------|
| 23 | 2023-12-13 | — | deferred (stay-application post-CoA-creation) |
| 22 | 2023-07-30 | — | deferred (stay-of-possession civil) |
| 21 | 2023-02-09 | — | deferred (variation-acceptance ratio) |
| 20 | 2023-11-16 | dismissed | **WRITTEN** (Mbuzakosi v The People) |
| 19 | 2023-04-20 | — | deferred (credit-life-master-policy interpretation) |
| 18 | 2023-12-06 | — | deferred (Subordinate Court jurisdiction under Intestate Succession Act) |

## Single record written

`judgment-zm-2023-zmsc-20-augustine-mwamba-mbuzakosi-and-ors-v-the-people`
- Citation: [2023] ZMSC 20
- Case: Augustine Mwamba Mbuzakosi and Ors v The People (aggravated-robbery + death-penalty triple-consolidation)
- Date: 2023-11-16
- Judges: Hamaundu, Mutuna, Chisanga (all JJS)
- Outcome: dismissed (matched via `pdf-tail-2pages[v031-tail]` pattern: "we dismiss it")
- Issue tags: 5 (criminal law / circumstantial evidence / common intention / aggravated robbery / death penalty under s.294(2))
- raw_sha256: a9aeb626c36ce…0b88693

## Deferral cohort

7 records joining the standing v0.3.3-pending interpretive-ratio cohort.
Cohort cumulative since b0504: **31 written / 21 deferred / 4 confirmed 404**.

## Next tick recommendation

Continue ZMSC 2023 sweep with nums {17..10} (8 candidates) — boundary already confirmed.
