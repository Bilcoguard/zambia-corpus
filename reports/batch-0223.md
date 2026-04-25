# Batch 0223 Report

**Date:** 2026-04-25  
**Phase:** phase_4_bulk  
**Started:** 2026-04-25T12:05:44Z  
**Completed:** 2026-04-25T12:13:08Z  
**Status:** PASS  
**Records added:** 8 (yield 8/8 = 100%)  

## Records ingested

| # | yr_num | sub_phase | parent_act | pages | text chars |
|---|--------|-----------|------------|-------|------------|
| 1 | 2021/055 | sis_consumer | Metrology Act | 40 | 68328 |
| 2 | 2021/056 | sis_consumer | Metrology Act | 50 | 81348 |
| 3 | 2021/059 | sis_consumer | Metrology Act | 18 | 19236 |
| 4 | 2020/052 | sis_consumer | Metrology Act | 10 | 13903 |
| 5 | 2020/069 | sis_agriculture | Plant Pests and Diseases Act | 10 | 14082 |
| 6 | 2020/070 | sis_agriculture | Plant Pests and Diseases Act | 4 | 3226 |
| 7 | 2018/023 | sis_agriculture | Plant Variety and Seeds Act | 78 | 94508 |
| 8 | 2017/001 | sis_corporate | Citizens Economic Empowerment Act | 2 | 1925 |


## Sub-phases covered
sis_agriculture, sis_consumer, sis_corporate

## Discovery
- Method: live alphabet probe
- Alphabets probed this tick: C, M, P
- Robots.txt re-verified: sha256 prefix `fce67b697ee4ef44...` (unchanged from batches 0193-0222)
- Crawl-delay honoured: 6.0s margin (robots-declared 5s)

## Fetches
- Total this batch: 20 (1 robots reverify + 3 alphabet probes + 16 ingest HTML+PDF)
- Cumulative today: 432/2000 (21.6%)
- Tokens: within budget

## Integrity checks
- CHECK1a (batch unique ids): PASS 8/8
- CHECK1b (corpus presence): PASS 8/8
- CHECK2 (amended_by refs): PASS (0 refs)
- CHECK3 (repealed_by refs): PASS (0 refs)
- CHECK4 (source_hash sha256 vs raw): PASS 8/8 against raw/zambialii/si/(2017,2018,2020,2021)/
- CHECK5 (required fields): PASS 10×8 all present
- CHECK6 (cited_authorities refs): PASS (0 refs)

## Sub-phase footprint expansion
- First **sis_consumer** records in corpus history (4 Metrology SIs under Metrology Act)
- First **sis_agriculture** records in corpus history (3 Plant SIs: Plant Variety and Seeds Act + Plant Pests and Diseases Act)
- First **sis_corporate**-adjacent record (Citizens Economic Empowerment Reservation Scheme Regulations 2017/1)

## Notes
- All 8 PDFs text-extractable (no pdf_parse_empty failures this tick — recovers from batch 0222's 87.5% yield).
- Sandbox bash 45s call cap forced ingest into 5 invocations (slices 0_2 + 2_4 + 4_6 + a 6_7 retry after 6_8 timeout on 3.8MB Plant Variety PDF + 7_8). Slice 6_7 reconstructed from on-disk artefacts after slice 6_8 bash timeout — record + raw HTML + raw PDF all written before timeout.
- B2 sync deferred to host (rclone unavailable in sandbox).

## Next-tick plan
- 220+ novel candidates remain in batch_0223 cache (alphabets C/M/P): rotate sis_consumer / sis_agriculture / sis_local_government / sis_security continuation, OR shift to acts_in_force (priority_order item 1, first-time SI→Acts rotation).
- Recommended fresh probes if cache exhausted: V (VAT, Veterinary), S (Securities, Skills), B (Banks, Business Names), F (Financial).
