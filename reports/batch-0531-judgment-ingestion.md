# Batch 0531 — judgment-ingestion-worker tick

- **Worker**: judgment-ingestion-worker
- **Wall-clock window**: 2026-05-07 (UTC, < 20 min target met)
- **Phase**: ZMSC 2022 most-recent-first DESC sweep continuation — lower-bound probe of inner-gap span (per b0530 next-tick recommendation)
- **Targets**: ZMSC 2022 nums {12, 11, 10, 9, 8, 7, 6, 5}
- **Parser**: v0.3.2 (scripts/batch_0506_zmsc_parse.py wrapping batch_0498_parse + batch_0360_parse)

## Tick decision (priority order)

a. **REPARSE DEFERRED** — gaps.md cohort of 41 ZMSC raw-on-disk deferrals are
   all flagged `raw-on-disk-pending-v0.3.3` (parser v0.3.2 already attempted;
   awaiting v0.3.3 patterns for the interpretive-ratio family). Not eligible
   for v0.3.2+ reparse this tick.
b. **SCZ SWEEP** — chosen. Continue ZMSC 2022 DESC sweep into nums {12..5}.
c. ZMCC NEW YEARS — not reached.

## Fetch results

| num | status | code | date       | html bytes | pdf bytes |
|-----|--------|------|-----------|----------:|----------:|
| 12  | ok     | –    | 2022-03-29 |    43,810 | 10,465,601 |
| 11  | ok     | –    | 2022-03-23 |    42,128 |  3,881,721 |
| 10  | ok     | –    | 2022-03-22 |    43,395 | 10,342,628 |
|  9  | ok     | –    | 2022-03-15 |    41,869 | 12,655,217 |
|  8  | ok     | –    | 2022-02-23 |    42,107 |  6,490,592 |
|  7  | ok     | –    | 2022-02-22 |    42,137 |  6,488,731 |
|  6  | ok     | –    | 2022-02-23 |    42,547 |  5,891,632 |
|  5  | ok     | –    | 2022-02-01 |    40,618 | 13,739,450 |

**All 8 candidates returned HTTP 200 OK.** This *closes the lower bound* of
the previously-discovered contiguous internal-404 span at nums {13..26} —
the cluster does NOT continue all the way to num=1. The bound below is
firmly num=12 (date 2022-03-29). 16 HTTP requests at 5s rate-limit
(8 dateless probes → 8 redirects to dated URLs → 8 PDFs). All polite,
robots.txt-conformant. **Fetch cost this tick: 16.**

## Internal-gap cluster — definitive bounds

- Upper boundary (last OK above): num=27 (Sampa & Anor v Patel, 2022-03-22)
- 404 span: nums **{13..26}** (14 contiguous nums confirmed across b0522, b0529, b0530)
- Lower boundary (first OK below): num=**12** (2022-03-29) — established this tick

The ZMSC/2022 numbering on ZambiaLII is therefore split: nums 1..12 (12 entries)
and nums 27..56+ (30+ entries), with a 14-num gap at {13..26}. This is consistent
with a court-internal renumbering or publication-policy boundary in early-2022;
no bytes are missing on our end.

## Parse results

- **written: 3** (parser v0.3.2)
- **deferred: 5** (all `html_no_summary_pdf_no_match` — interpretive-ratio family, same v0.3.3-pending cohort pattern)

| num | result      | outcome      | source pattern                                                | case_name (short)                          |
|-----|-------------|--------------|---------------------------------------------------------------|--------------------------------------------|
| 12  | deferred    | –            | html_no_summary_pdf_no_match                                  | jurisdiction-of-single-SCZ-judge to stay   |
| 11  | **written** | allowed      | summary[`Court (allowed\|granted)`]                          | Tembo v Chirwa and Ors (Rule 12 SCR ext.)  |
| 10  | deferred    | –            | html_no_summary_pdf_no_match                                  | partial final arbitral award / re-litigation |
|  9  | deferred    | –            | html_no_summary_pdf_no_match                                  | abuse of process — delayed nullification    |
|  8  | **written** | dismissed    | summary[`(appeal\|petition\|application\|action\|matter) ... dismissed`] | Mwachilenga v Alistair Logistics (Z) Ltd  |
|  7  | **written** | dismissed    | summary[`v032: (application\|petition\|appeal\|relief)…`]    | Mpoha and Anor v Salvator (leave refused) |
|  6  | deferred    | –            | html_no_summary_pdf_no_match                                  | renewed injunction in SCZ while CoA seised  |
|  5  | deferred    | –            | html_no_summary_pdf_no_match                                  | circumstantial evidence — murder conviction |

### Written-record details

- **judgment-zm-2022-zmsc-11-tembo-v-chirwa-and-ors** (Tembo v Chirwa and Ors;
  date 2022-03-23; outcome **allowed** — extension under Rule 12 SCR granted
  where applicant filed within 21 days of becoming aware of the ruling;
  single judge Chinyama JS).
- **judgment-zm-2022-zmsc-08-mwachilenga-v-alistair-logistics-z-ltd**
  (Mwachilenga v Alistair Logistics (Z) Ltd; date 2022-02-23; outcome
  **dismissed** — leave refused: issues private/interlocutory, no point of
  public importance; single judge Hamaundu JS).
- **judgment-zm-2022-zmsc-07-mpoha-and-anor-v-salvator** (Mpoha and Anor v
  Salvator; date 2022-02-22; outcome **dismissed** — leave to appeal refused;
  alleged smuggling did not render the contract illegal; only factual issues
  raised; single judge Hamaundu JS).

## Integrity checks

- 82/82 PASS (scripts/integrity_check_b0531.py): required fields, judges>=1,
  issue_tags non-empty, outcome enum, registry resolution (Chinyama JS,
  Hamaundu JS — both pre-existing canonical), raw_sha256 matches on-disk PDF,
  source_url is ZambiaLII canonical, zero duplicate IDs across corpus.
- corpus.sqlite: records **1840 → 1843** (+3); judgments_meta **150 → 153** (+3),
  written via TMPDIR-routed atomic copy (b0519+ precedent).
- judges_registry.yaml UNCHANGED (both judges already canonical).
- approvals.yaml UNCHANGED (per non-negotiable rule #4).
- records_fts left to host-side rebuild via batch_0504_build_fts5.py
  (b0517 precedent).

## Cohort status after b0531

ZMSC 2022 sweep: 56 of ~60 attempted
- **17 written** (was 14, +3 this tick)
- **25 v0.3.3-pending deferred** (raw on disk; awaiting interpretive-ratio
  parser update — was 20, +5 this tick: zmsc/2022/{12, 10, 9, 6, 5})
- 1 OCR-pending deferred (zmsc/2022/51 scanned PDF)
- 14 confirmed internal 404s at contiguous span {13..26}

Daily fetch budget for judgment-ingestion-worker (separate 500/day):
b0531 fetched 16 → cumulative today **16 / 500**.
(Today is 2026-05-07; fresh budget vs b0530's 56/500 on 2026-05-06.)

Cohort cumulative since b0504: **55 written, 47 deferred, 24 confirmed 404**
(+3 written, +5 deferred this tick).

## B2 sync

Deferred to host (rclone not in sandbox).

## Next-tick recommendation

ZMSC 2022 effectively complete from a sweep-coverage perspective:
- nums 1..4 still unprobed (4 candidates)
- num 51 scanned-PDF OCR-pending deferral pending resolution

Recommendations next tick (priority order):
1. **Probe nums {4, 3, 2, 1}** (4 candidates) to fully close ZMSC 2022 sweep.
   Then with remaining 4-fetch budget headroom, **start ZMSC 2021** sweep at
   the topmost num — probe ZambiaLII listing first to discover the 2021
   max-num boundary (or extrapolate ~50-60 like 2022).
2. If a v0.3.3 parser ships, prioritise **REPARSE DEFERRED** of the now
   46-record raw-on-disk cohort (interpretive-ratio family — current 41 +
   5 added this tick) before moving deeper into year sweeps.

ZMSC 2021 sweep when launched should follow the same most-recent-first DESC
pattern with 8-target ticks.
