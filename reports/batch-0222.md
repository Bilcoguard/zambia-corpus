# Phase 4 Batch 0222 — sis_tax discovery, modern cross-sub_phase fill

- Batch: **0222**
- Phase: phase_4_bulk
- Sub-phases (per record): sis_transport (2), sis_health (2), sis_courts (1), sis_education (1), sis_immigration (1)
- Discovery alphabets: W, J, I, T, N (5 letters + 1 robots reverify = 6 fetches)
- Started: 2026-04-25T11:34:41Z
- Completed: 2026-04-25T11:41:24Z
- Records written: **7** of 8 attempted (yield 7/8 = 87%)
- Robots SHA256: fce67b697ee4ef44... (prefix unchanged from batches 0193-0221)

## Records ingested

| Year | No. | Sub-phase | Sections | PDF bytes | Title |
|------|----:|-----------|---------:|----------:|-------|
| 2026 | 011 | sis_transport | 5 | 309908 | Tolls (Tom Mtine Toll Plaza) Regulations, 2026 |
| 2025 | 012 | sis_transport | 1 | 401932 | Tolls (Micheal Chilufya Sata Toll Plaza) Regulations, 2025 |
| 2024 | 007 | sis_health | 78 | 385098 | Ionising Radiation Protection (Nuclear Medicine) Regulations, 2024 |
| 2024 | 008 | sis_health | 94 | 460938 | Ionising Radiation Protection (Radiotherapy) Regulations, 2024 |
| 2022 | 033 | sis_courts | 13 | 291315 | Judges (Salaries and Condition of service) (Amendment) Regulations, 2022 |
| 2018 | 001 | sis_education | 49 | 42028 | Teaching Profession (Code of Ethics) Regulations, 2018 |
| 2019 | 034 | sis_immigration | 66 | 115165 | National Registration Regulations, 2019 |

## Failures (logged to gaps.md)

- 2011/129 [sis_immigration] status=`pdf_parse_empty` — immigration and deportation general regulations 2011

## Discovery & repick

- Alphabets W/J/I/T/N probed live (5 fetches + 1 robots reverify).
- 71 novel pre-keyword candidates extracted; 12 priority sub-phase + 13 adjacent sub-phase keyword hits.
- Initial slice (slice 0_2) selected 5 sis_tax candidates from priority pool — first 2 attempted (2017/043, 2019/025) both returned `pdf_parse_empty` (image-only/scanned PDFs; pdfplumber and pdfminer both extracted 0 chars).
- Repick: replaced remaining 6 sis_tax candidates with 6 modern (2018-2026) text-extractable candidates spanning 5 cross sub-phases for batch diversity.
- Final attempt set: 8 candidates; 7 succeeded (2026/011, 2025/012, 2024/007, 2024/008, 2022/033, 2018/001, 2019/034); 1 failed (2011/129 immigration regs — also image-only PDF).
- Cumulative `pdf_parse_empty` failures across batches 0208/0213/0221/0222: 6 SIs total. Pattern: ZambiaLII serves image-only/scanned PDFs for ~3-5% of older (pre-2015) and pre-2023-amended SIs. Recommend OCR pipeline (parser_version 0.6.0) as future work — out of scope for in-sandbox processing (no tesseract).

## Integrity checks

- CHECK1a (batch-scoped id uniqueness): **PASS** (7/7)
- CHECK1b (corpus-wide presence): **PASS**
- CHECK2/3 (amended_by/repealed_by ref resolution): **PASS** (0 refs)
- CHECK4 (source_hash sha256 match on disk): **PASS** (7/7)
- CHECK5 (required field completeness): **PASS** (10x7)

## Costs

- Today fetches at batch end: 399 / 2000 (19.95%)
- Crawl-delay: 6s (margin over robots-declared 5s)
- All fetches against zambialii.org + 1 against commons.laws.africa (mirror PDF)

## Next-tick plan

- 71 novel pre-keyword candidates remain in batch-0222 discovery cache; ~25 modern (2014+) text-extractable candidates available for cross-sub_phase rotation without alphabet re-probe:
  - sis_transport: 2016/057 + 2016/085 + 2008/016 + 2005/019 (Tolls + National Road Fund)
  - sis_health: 2024/007 + 2024/008 already done; check IRP series for more
  - sis_education: 2018/014 Tourism Standards + Teaching Profession derivatives
  - sis_courts: 2014/022 Legal Reform Commission + 2015/025 Inquiries Act + 2016/072 Inquiries Act 2016
  - sis_local_government/construction: 2015/039 + 2009/037 + 2004/022 (NCC series)
  - sis_tourism (new sub-phase): 2016/051+093+094+099+100+022+020+014 (Tourism and Hospitality Act derivatives)
- Recommend: next tick rotate to acts_in_force (priority_order item 1) — first time shifting from SI to consolidated Acts.
- Or: continue cross-sub_phase fill from cache (8 picks across sis_tourism + sis_courts + sis_local_government) for another 100% yield batch.
- Re-verify robots.txt at start of next tick.
