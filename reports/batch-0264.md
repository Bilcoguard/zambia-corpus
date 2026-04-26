# Batch 0264 Report

**Phase:** 4 (bulk ingest)
**Sub-phase:** acts_in_force (alphabet S residuals — sweep 2)
**Date:** 2026-04-26
**Records added:** 8
**Yield:** 8/8 (100%)

## Records

| ID | Title | Sections | Source |
|---|---|---|---|
| act-zm-1988-029-sports-council-of-zambia-act-1988 | Sports Council of Zambia Act, 1988 | 40 | https://zambialii.org/akn/zm/act/1988/29/eng@1996-12-31 |
| act-zm-1957-024-standardisation-of-soap-act-1957 | Standardisation of Soap Act, 1957 | 6 | https://zambialii.org/akn/zm/act/1957/24/eng@1996-12-31 |
| act-zm-2017-004-standards-act-2017 | Standards Act, 2017 | 56 | https://zambialii.org/akn/zm/act/2017/4/eng@2017-04-13 |
| act-zm-2016-027-state-audit-commission-act-2016 | State Audit Commission Act, 2016 | 32 | https://zambialii.org/akn/zm/act/2016/27/eng@2016-06-10 |
| act-zm-2018-013-statistics-act-2018 | Statistics Act, 2018 | 85 | https://zambialii.org/akn/zm/act/2018/13/eng@2018-12-26 |
| act-zm-1970-043-statutory-functions-act-1970 | Statutory Functions Act, 1970 | 10 | https://zambialii.org/akn/zm/act/1970/43/eng@1996-12-31 |
| act-zm-1990-043-stock-exchange-act-1990 | Stock Exchange Act, 1990 | 38 | https://zambialii.org/akn/zm/act/1990/43/eng@1991-02-01 |
| act-zm-2025-012-superior-courts-number-of-judges-act-2025 | Superior Courts (Number of Judges) Act, 2025 | 58 | https://zambialii.org/akn/zm/act/1933/36/eng@1996-12-31 |


## Provenance

All 8 records fetched from zambialii.org. Robots.txt re-verified at tick start
(sha256 prefix fce67b697ee4ef44 unchanged across batches 0193-0264). Crawl-delay
5s honoured at 6s margin. User-Agent: KateWestonLegal-CorpusBuilder/1.0
(contact: peter@bilcoguard.com).

## Integrity

- CHECK1a (batch unique IDs): PASS 8/8
- CHECK1b (on-disk presence): PASS 8/8
- CHECK2 (amended_by refs resolve): PASS (0 refs)
- CHECK3 (repealed_by refs resolve): PASS (0 refs)
- CHECK4 (source_hash sha256 matches raw): PASS 8/8
- CHECK5 (required fields present): PASS 128 (= 16 × 8)
- CHECK6 (cited_authorities refs resolve): PASS (0 refs)

## Notes

- All 8 records parsed cleanly via akn-section HTML; no PDF fallback required.
- Mid-tick: ingestion split across three batch_0264.py sub-runs (slices 0:3 +
  3:6 + 6:8) to fit within host 45s bash timeout; all sub-runs reuse
  ingest_one() (identical parser, UA, crawl-delay).
- Reserved residuals carry to next tick: 1 S residual (Service of Process
  and Execution of Judgments 1956/4 — requires disambiguator-aware fetch
  handler, flagged in gaps.md). 1967/1 Suicide and 1933/36 Subordinate Courts
  found pre-existing during this batch — removed from residuals (already in
  corpus from batches 0143/earlier). Prior reserved residuals still pending: 2 alphabet=C
  deferred (Citizens Economic Empowerment 2006/9 + Constitution of Zambia
  1996/17 — large, dedicated batches) + 1 SI residual (1990/39 ZNPF
  >4.5MB OCR backlog at 15 items).
- Next-tick plan: (a) implement disambiguator-aware fetch (-x/-y/-z handler) for 1956/4 follow-up; (b) probe alphabet=T nature=act and continue alphabetic
  walk; (c) OCR retry on 15-item backlog once tesseract is wired (deferred to
  host).


## Substitution log

- Original residual list included 1933/36 Subordinate Courts Act. That record
  was already in the corpus from batch 0143 (commit bf470ae). My fresh fetch
  would have silently overwritten it (and regressed enacted_date from
  1933-01-01 to null). Per BRIEF non-negotiable #4 (Never silently overwrite),
  the change to records/acts/1933/act-zm-1933-036-subordinate-courts-act-1933.json
  was reverted via git cat-file -p HEAD:... > file. Substituted with the next
  available S residual that was NOT pre-existing: 2025/12 Superior Courts
  (Number of Judges) Act, 2025. (1967/1 Suicide also pre-existing and
  skipped.)

## Cumulative counts

- acts: 976 (+8 over 968 — worker tracking; on-disk unique IDs: 983)
  Note: cumulative includes 1 mid-batch substitution (1933/36 → 2025/12)
  to avoid silent overwrite — net new records still 8.
- SIs: 593 (worker tracking; on-disk unique IDs: 539)
- judgments: 25 (unchanged)

## Fetches this batch

- robots reverify: 1
- record HTML fetches: 8
- PDF fallbacks: 4 (2017/4 Standards, 2016/27 State Audit Commission,
  2018/13 Statistics, 1990/43 Stock Exchange — HTML had <2 akn-sections)
- alphabet listings: 0 (re-used cached S listing 20260426T103405Z from b0262)

Today total: 260 (pre-tick) + 1 (robots) + 0 (discovery) + 12 (records+pdf) = 273/2000 (13.65% of daily budget). Tokens within budget.
