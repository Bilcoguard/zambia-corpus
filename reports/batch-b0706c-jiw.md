# Judgment batch b0706c-jiw

- date: 2026-05-18T15:16:51Z
- worker: judgment-ingestion-worker
- mode: finalise rollback of b0706-jiw + reparse with parser v0.4.1 (filename-based case_name)
- network fetches: 0
- stubs overwritten: 3
- candidates parsed: 3
- inserted: 3
- deferred: 0
- pre-state: records=1958 fts=1958
- post-state: records=1961 fts=1961

## Background

Tick b0706-jiw extracted case names via a `BETWEEN ... CORAM` block parser that captured OCR-like noise from PDF text and produced corrupted ID slugs (e.g. `judgment-zm-2024-coa-024-z-kingfred-phiri-l-appellant-civil-rgi5tjy-...`). Subsequent rollback (b0706b-jiw) deleted those rows from `records` + `records_fts`, but the on-disk JSON files could not be removed (bindfs blocks `unlink(2)`).

This tick (b0706c-jiw) overwrites the orphan JSON files with deprecation-stub markers and re-ingests the three PDFs with parser v0.4.1-inline, which derives `case_name` directly from the publisher filename and extracts judges from the `Coram-...` filename suffix.

## Deprecation stubs written

- `records/judgments/coa/2024/judgment-zm-2024-coa-024-z-kingfred-phiri-l-appellant-civil-rgi5tjy-2-and-0x-5ofl7-life-master-limited-re.json` (cn=APP/024/2024)
- `records/judgments/coa/2020/judgment-zm-2020-coa-113-chisumpa-liandisha-appellant-and-the-people-respondent.json` (cn=APP/113/2020)
- `records/judgments/coa/2024/judgment-zm-2024-coa-211-rotor-moulder-enterprises-timite-appellant-and-stanley-jordan-1st-respondent-jos.json` (cn=APP/211/2022)

## Inserted (clean slugs)

- `judgment-zm-2024-coa-024-kingfred-phiri-v-life-master-ltd` — APP/024/2024 — other
  - case_name: Kingfred Phiri v Life Master Ltd
  - date_decided: 2024-12-10
  - judges: Siavwapa Mchenga DJPChashi Kondolo Makungu ChishimbaSichingaNgulubeBanda BoboSharpe PhiriMuzengaPatel Chembe JJA
- `judgment-zm-2020-coa-113-chisumpa-liandisha-v-the-people` — APP/113/2020 — other
  - case_name: Chisumpa Liandisha v The People
  - date_decided: 2020-02-18
  - judges: Mchenga Chishimba Majula JJA
- `judgment-zm-2024-coa-211-rotor-moulder-enterprises-limited-v-stanley-jordan-6-others` — APP/211/2022 — set-aside
  - case_name: Rotor Moulder Enterprises Limited v Stanley Jordan 6 Others
  - date_decided: 2024-12-31
  - judges: Makungu Muzenga Chembe JJA
