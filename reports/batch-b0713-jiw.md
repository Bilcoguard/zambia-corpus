# Judgment batch b0713-jiw — CoA reparse-deferred drain

- date: 2026-05-18T18:54:22Z
- worker: judgment-ingestion-worker
- parser: 0.4.4-jiw-b0713-inline
- mode: reparse-on-disk (zero network fetches)
- candidates considered: 8
- inserted: 2
- deferred: 6
- pre-state: records=1961 fts=1961
- post-state: records=1963 fts=1963
- integrity: pass=True

## Inserted

- `judgment-zm-2023-coa-203-caz-08-242-2023-deton-engineering-pvt-v-konkola-copper-mines-plc` — APP/203/2023 — other — date=None — judges=[chashi ngulube banda bobo JJA]
- `judgment-zm-2024-coa-108-pilatus-engineering-company-limitedjoseph-huiler-v-alfred-kalwani` — APPLN/108/2024 — remitted — date=None — judges=[chashi ngulube banda bobo JJA, 2 JJA]

## Deferred

- `APP/304/2022` — APP-304-2022-Setrec-Steel-and-Wood-Processing-Limited-vs-Zambia-National-Commercial-Bank-Plc-31-Jan-2025-Coram-Chashi-Makungu-Sichinga-JJA.pdf — body-too-short:32
- `APP/309/2023` — App-309-2023-Emergency-Response-Zambia-Limited-2-Others-Vs-Betternow-Finance-Company-LimitedInde-Credit-Company-Limited-Coram-Ngulube-Muzenga-And-Chembe-JJA.pdf — body-too-short:19
- `APP/165/2024` — App-165-2024-Savenda-Management-Services-Limited-vs-Lumwana-Mining-Company-Limited-31-Dec-2024-Coram-Mchenga-DJP-Muzenga-Chembe-JJA.pdf — body-too-short:19
- `APP/024/2024` — App-24-2024-Peter-Mutale-vs-Davies-Mukumbwa-24-Jan-2025-Coram-Siavwapa-JP-Chishimba-Patel-JJA.pdf — body-too-short:20
- `APP/202/2023` — app-202-2023-maambo-simukuni-vs-tenyiwe-sibindi-coram-justice-siavwapa-jp-chishimba-patel-jja.pdf — duplicate-fingerprint
- `APP/123/2023` — App-123-2023-Patson-Kabungo-Sichoni-vs-The-People-Coram-Mchenga-DJP-Muzenga-Chembe-JJA.pdf — body-too-short:15

## Notes

Reparse-deferred drain of CoA PDFs already on disk in `raw/judiciary-zm/coa/`. Filename-based case_name + coram extraction (v0.4.4 inline). Multi-tier outcome detection (operative section, tail-4k, tail-12k).
