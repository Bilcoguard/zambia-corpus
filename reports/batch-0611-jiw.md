# Batch 0611 — Judgment Ingestion Worker

**Timestamp:** 2026-05-12T10:13Z
**Parser version:** 0.4.3-inline-b0611
**Phase:** priority_a_reparse_deferred + judgments_meta backfill

## Pre-flush state

- FTS5 integrity_check: ok
- records: 1899
- records_fts: 1899

## Inserted (7 new records)

- `judgment-zm-2026-coa-237-the-examination-council-of-zambia-v-christopher-mkandawire` (APP/237/2023, set-aside, panel: Chashi/Ngulube/Banda-Bobo JJA, 2026-02-11) — judicial review remitted to High Court; lower-court order set aside
- `judgment-zm-2026-coa-099-geoffrey-muyonga-sitwala-kaliki-vincent-lubinda-v-ahmed-abdulkadir-barakadle-mohammed-other` (APPLN/099/2025, struck-out, panel: Chashi/Ngulube/Banda-Bobo JJA, 2026-02-11) — application for leave to appeal struck off active list; 14-day liberty to restore
- `judgment-zm-2026-coa-279-kangwa-musenga-2-others-v-victor-muyumba-4-others` (APP/279/2023, dismissed, panel: Chashi/Makungu/Banda-Bobo JJA, 2026-02-11) — res-judicata doctrine inapplicable; appeal dismissed
- `judgment-zm-2026-coa-231-lisboa-casino-limited-v-director-of-public-prosecutions` (APP/231/2023, dismissed, panel: Kondolo SC/Makungu/Chembe JJA, 2026-02-06) — we dismiss the preliminary issue raised.
- `judgment-zm-2026-coa-317-the-university-of-zambia-v-ossie-mangani-zulu` (APP/317/2024, dismissed, panel: Kondolo SC/Makungu/Chembe JJA, 2026-01-29) — appeal is dismissed.
- `judgment-zm-2026-coa-568-chieftainess-lesa-v-mponwe-farms-limited-others` (CAZ/08/568/2025, refused, panel: Banda-Bobo JJA, 2026-02-05) — renewed application for injunction dismissed in chambers; ex-parte order discharged
- `judgment-zm-2026-coa-172-wesley-sibanda-feediness-sakala-sibanda-v-point-present-investment-limited-sasha` (APP/172/2024, dismissed, panel: Kondolo SC/Majula/Muzenga JJA, 2026-02-05) — appeal is consequently dismissed with costs to the Respondent.

## Backfilled judgments_meta (3 records)

- `judgment-zm-2026-coa-210-clifford-simfukwe-v-zesco` (APP/210/2023, Court of Appeal, 2026-01-29) — was inserted by b0610 to records+records_fts but missed judgments_meta
- `judgment-zm-2026-coa-291-bank-of-zambia-v-bernard-fundi` (APP/291/2024, Court of Appeal, 2026-01-27) — was inserted by b0610 to records+records_fts but missed judgments_meta
- `judgment-zm-2026-coa-304-julian-sichalwe-v-saturina-regna-pension-trust-limited-lumwana-mining-company-li` (APP/304/2024, Court of Appeal, 2026-01-27) — was inserted by b0610 to records+records_fts but missed judgments_meta

## Post-flush state

- records: 1906
- records_fts: 1906
- judgments_meta: 216
- Court of Appeal coverage: 39 (judgments_meta) / 39 (records id-pattern)

## Integrity checks

- check1_judges: PASS
- check2_tags: PASS
- check3_outcome: PASS
- check5_dup_ids: PASS
- check6_sha: PASS
- check7_dup_combos: PASS
- check8_records_eq_fts: PASS(1906=1906)

## Next-tick recommendation (b0612)

1. Re-parse 4 b0591 raw PDFs from `raw/judiciary-zm/coa/`
2. Re-parse 1 b0593 parser-clean record (`bright-jangazya` — case_name needs v0.4.2 cleanup; body re-extraction required)
3. If time allows, resume `judiciary-coa-sweep: page 8` (6 candidates remaining)

## Backlog

- deferred-fts5: was 19, now 12 (b0591 4, b0593 6, b0597 2, residual b0590 0)
- scanned-pdf: 10 (unchanged)
