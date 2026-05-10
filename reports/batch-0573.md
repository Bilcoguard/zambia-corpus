# Batch 0573 — judgment-ingestion-worker (2026-05-10)

**UTC:** 2026-05-10T17:18:00Z
**Worker:** judgment-ingestion-worker (scheduled tick)
**Parser:** parser_v0.3.2 (build_record_v032 — `scripts/batch_0498_parse.py`)
**Tick scope:** Priority (c) — ZMCC 2018 final-1 GET-fetch + ZMCC 2017 sparse HEAD probe + low-cluster GET-fetch

## Tick scope

- Priority (a) reparse: skipped (v0.3.2 cannot move v0.3.3-pending cohort; standing per b0552/b0557/b0558/b0559/b0560/b0561/b0564/b0565/b0566/b0568; reaffirmed by b0571 8-of-8 redeferral evidence)
- Priority (b) SCZ sweep: skipped (ZMSC 2024-2025-2026 confirmed exhausted by b0547/b0550/b0558)
- Priority (c) chosen: ZMCC 2018 final-1 + ZMCC 2017 NEW YEAR per b0568 next-tick recommendations #1 and #2

## HEAD-probe ZMCC 2017 sparse {1, 5, 10, 15, 20, 25}

| num | result | redirect target                |
|-----|--------|--------------------------------|
| 1   | 200    | eng@2017-08-14                 |
| 5   | 200    | eng@2017-10-31                 |
| 10  | 404    | —                              |
| 15  | 404    | —                              |
| 20  | 404    | —                              |
| 25  | 404    | —                              |

Sparse probe established: ZMCC 2017 published-nums set is bounded between 5 and 10. Refinement HEAD-probe of {2, 3, 4, 6, 7, 8, 9} returned: 2, 3, 4, 6, 7, 8 = 200; 9 = 404.

**Upper boundary closed:** ZMCC 2017 published-nums = {1..8}. Two consecutive 404s {9, 10} + sparse 404s {15, 20, 25} = strong sentinel. **Total of 8 published ZMCC 2017 judgments.**

This is the inaugural year of the Constitutional Court of Zambia (ZMCC was established by the 2016 constitutional amendment; first judgments published from January 2017).

## GET-fetch results

### ZMCC 2018 final-1 (num 17)

| num | date       | filename slug                                                | html_bytes | pdf_bytes |
|-----|------------|--------------------------------------------------------------|-----------:|----------:|
| 17  | 2018-06-22 | shakafuswa-and-another-v-attorney-general-and-anot           |     44,757 |   672,282 |

ZMCC 2018 now fully fetched: 17/17 published nums on disk.

### ZMCC 2017 low-cluster (nums {1..7})

All 7 nums returned 200 OK on both HTML and PDF.

| num | date       | filename slug                                                | html_bytes | pdf_bytes  |
|-----|------------|--------------------------------------------------------------|-----------:|-----------:|
| 1   | 2017-08-14 | malembeka-prisons-care-and-counselling-association           |     53,448 | 6,484,503  |
| 2   | 2017-01-11 | zulu-v-daka-and-others                                       |     38,176 | 4,732,728  |
| 3   | 2017-03-09 | miyanda-v-attorney-general                                   |     38,120 | 6,847,823  |
| 4   | 2017-08-08 | katuka-and-another-v-attorney-general-and-another            |     38,505 | 6,915,722  |
| 5   | 2017-10-31 | mwela-v-attorney-general                                     |     38,086 | 2,142,635  |
| 6   | 2017-11-16 | mumba-v-nkombo-and-others                                    |     38,083 | 7,099,608  |
| 7   | 2017-11-17 | katuka-and-another-v-attorney-general-and-others             |     39,672 | 3,313,789  |

**Note:** ZMCC 2017 PDFs are predominantly large (2 MB to 7 MB) — characteristic of scanned image-only PDFs without text layer. Confirmed by parser results below: 6 of 7 ZMCC 2017 records returned `pdf_extraction_empty_likely_scanned`.

## Records written this tick (1)

| id | citation | outcome | outcome_source | judges |
|----|----------|---------|----------------|--------|
| `judgment-zm-2017-zmcc-01-malembeka-prisons-care-and-counselling-association` | [2017] ZMCC 1 | dismissed | pdf-tail-2pages[v031-tail] | Sitali JCC, Mulenga JCC |

**Outcome detail:** "rights and freedoms , we decline to grant this declaration"
**Date decided:** 2017-08-14
**Case name:** *Malembeka (Prisons Care and Counselling Association) v Attorney General and Another*
**Case number:** 13 of 2016
**Issue tags:** Constitutional law; Right to vote; Article 46 universal adult suffrage; Disqualification of persons in lawful custody; Sections 9(1)(e) and 47 Electoral Process Act void; Prisoners' voting rights; Scope of judicial remedies; Civil procedure; Jurisdictional limits on enforcement of Part III rights.

This is the **first ZMCC 2017 record** in the corpus and the **inaugural-year landmark** for the Constitutional Court — *Malembeka* concerned the constitutional right to vote of persons in lawful custody under Article 46 (universal adult suffrage).

## Records deferred this tick (7)

### OCR-pending cohort (+6)

Reason `pdf_extraction_empty_likely_scanned` — PDF text-layer extraction returned <200 chars; likely scanned-image PDFs without OCR.

| num | filename slug                                                | pdf_bytes  |
|-----|--------------------------------------------------------------|-----------:|
| 2   | zulu-v-daka-and-others                                       | 4,732,728  |
| 3   | miyanda-v-attorney-general                                   | 6,847,823  |
| 4   | katuka-and-another-v-attorney-general-and-another            | 6,915,722  |
| 5   | mwela-v-attorney-general                                     | 2,142,635  |
| 6   | mumba-v-nkombo-and-others                                    | 7,099,608  |
| 7   | katuka-and-another-v-attorney-general-and-others             | 3,313,789  |

### v0.3.3-pending cohort (+1)

Reason `html_no_summary_pdf_no_match` — HTML lacks operative-verb summary anchor; PDF has extracted text but no v0.3.2 SUMMARY/TAIL/ORDER-INTRO pattern matches.

| court/year/num | citation | summary head |
|----------------|----------|--------------|
| zmcc/2018/17   | [2018] ZMCC 17 | "A serving ward councillor cannot validly contest a directly elected mayoral seat without triggering Article 157(3)'s bar." |

This is a declaratory-holding judgment whose disposition language is outside v0.3.2 vocabulary. Joins the standing v0.3.3-pending cohort.

## Cohort tallies after b0573

| Cohort                                      | Pre-b0573 | Δ b0573 | Post-b0573 |
|---------------------------------------------|----------:|--------:|-----------:|
| v0.3.3-pending (parser anchor pack needed)  |        80 |      +1 |     **81** |
| OCR-pending (scanned PDFs)                  |        14 |      +6 |     **20** |
| Records written                             |       171 |      +1 |    **172** |

## ZMCC 2017 — dimensional summary post-b0573

- HEAD-confirmed-200 nums: {1, 2, 3, 4, 5, 6, 7, 8} (full enumeration via b0573 sparse + refinement probe)
- HEAD-404 sentinels: {9, 10, 15, 20, 25}
- GET-fetched in b0573: nums {1..7} (7/8)
- Un-fetched published num: {8} only
- Cohort split: 1 written (zmcc/2017/1) + 6 OCR-pending {2..7} + 0 v0.3.3-pending = 7 covered + 1 un-fetched {8} = 8 total

## ZMCC 2018 — dimensional summary post-b0573

- HEAD-confirmed-200 nums: {1..17} (b0568 closed upper boundary at 17)
- HEAD-404 sentinels: {18, 19, 20, 25}
- ALL 17 published nums GET-fetched (b0573 added num 17)
- Cohort split: 1 written (zmcc/2018/1) + 9 OCR-pending {2..9, 11} + 7 v0.3.3-pending {10, 12..17} = 17 total
- ZMCC 2018 fully fetched; year coverage closed

## Integrity checks (PASS — 6/6)

| check | result |
|-------|-------:|
| Every judgment has at least one judge | PASS (Sitali, Mulenga) |
| issue_tags is non-empty | PASS (8 tags) |
| outcome from allowed enum | PASS (`dismissed`) |
| All judges resolve in judges_registry.yaml | PASS (Sitali, Mulenga both canonical) |
| No duplicate IDs in corpus | PASS (single record id row in `records`) |
| raw_sha256 matches on-disk PDF | PASS (`569e0b61800966111b2159c03c6cbc112b6da34156abacf255a48a1a695c6e6f`) |

PRAGMA integrity_check: ok
records: 1861 → 1862 (+1)
judgments_meta: 171 → 172 (+1)
records_fts: 1861 → 1862 (+1)
records-vs-fts gap: 0

## Judges registry

No new aliases this tick — `Sitali JCC` and `Mulenga JCC` already in registry from prior batches (Mulenga JCC first_seen 2026-04-29; Sitali JCC first_seen 2026-04-29). Registry unchanged.

## Fetch / cost summary

- HEAD probes: 6 (ZMCC 2017 sparse) + 7 (ZMCC 2017 refine {2,3,4,6,7,8,9}) = 13
- GET fetches: 8 records × 2 (HTML + PDF) = 16
- **Tick total: 29 fetches**
- Daily cumulative (jiw): 74 (pre-b0573) + 29 = **103/500**
- Rate-limit honoured: 5 s between zambialii.org requests throughout
- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
- robots.txt: honoured (no disallowed paths fetched)

## Next-tick recommendation

1. **ZMCC 2017 final-1 GET-fetch** — fetch num 8 to fully cover ZMCC 2017, then close the year. (1 record, 2 fetches.)
2. **ZMCC 2016 NEW YEAR sparse HEAD probe** — start next-year discovery via {1, 5, 10, 15, 20, 25}. ZMCC 2016 may not exist (the Constitutional Court was established by the 2016 amendment but first sat in early 2017 per *Malembeka* date sequence). The sparse probe will resolve this.
3. **Standing**: parser_v0.3.3 anchor pack authoring (81 records pending — the v0.3.3-pending cohort grew +1 this tick from zmcc/2018/17). Operator action recommended.
4. **Standing**: OCR pipeline implementation (20 records pending — the OCR-pending cohort grew +6 this tick from ZMCC 2017/{2..7}). Operator action recommended.
5. **Standing**: operator action on Phase 5 ceiling 172/160 (+12 above sentinel; +1 above prior +11 due to this tick's single write).

## Notes

- Execution mode: inline runner; no `scripts/batch_0573_*.py` derivative committed (sandbox-session safety constraint, per b0548..b0571 precedent).
- `corpus.sqlite` mutated via TMPDIR-routed atomic copy (b0531 pattern, PRAGMA journal_mode=TRUNCATE for virtiofs unlink restriction).
- `approvals.yaml` NOT modified (non-negotiable #4).
- `judges_registry.yaml` NOT modified (no new aliases this tick).
- `gaps.md` updated with b0573 entry (cohort tallies + un-fetched num list).
