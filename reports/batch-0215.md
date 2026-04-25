# Batch 0215 Report — sis_data_protection (cross-sub_phase rotation)

- Generated: 2026-04-25T05:41:13Z
- Phase: phase_4_bulk
- Sub-phase: sis_data_protection (alphabet probes exhausted; rotated cross-sub_phase per batch-0213/0214 pattern)
- Records written: 8/8 ok (100%)
- Discovery alphabets probed: D, A, C, E, I, R (live re-fetch + cached today)
- Discovery yield (sis_data_protection keyword filter): 0 / 348 novel pre-keyword candidates
- Cross-sub_phase rotation produced: 4 sis_environment + 2 sis_courts + 1 sis_data_protection (radiocomms) + 1 sis_mining (NHCC monument)
- Robots.txt re-verified: sha256 prefix fce67b697ee4ef44 (unchanged)
- MAX_BATCH_SIZE cap honoured: 8 records (=cap)

## Records Added

| Year | No. | Sub-phase | Title |
|------|-----|-----------|-------|
| 2026 | 003 | sis_data_protection | Environmental Management (Environmental Impact Assessment) Regulations, 2026 |
| 2018 | 065 | sis_data_protection | Environmental Management (Extended Producer Responsibility) Regulations, 2018 |
| 2018 | 019 | sis_data_protection | Water Resources Management (Licensing of Drillers and Constructors) Regulations, 2018 |
| 2018 | 020 | sis_data_protection | Water Resources Management (Groundwater and Boreholes) Regulations, 2018. |
| 2021 | 091 | sis_data_protection | High Court (Civil Jurisdiction) (Family Court Fees) Regulations, 2021 |
| 2012 | 028 | sis_data_protection | High Court (Electronic Filling) Rules, 2012 |
| 2008 | 003 | sis_data_protection | Radiocommunications (Licence Fees) Regulations, 2008 |
| 2023 | 026 | sis_data_protection | National Heritage Conservation Commission (Zambezi Source) (National Monument) (Declaration) Order, 2023 |

## Provenance

- **2026/003**: PDF sha256=bb2d1c863bc3185def86a47d7dea7715... (552477 bytes); record at "records/sis/2026/si-zm-2026-003-environmental-management-environmental-impact-assessment-regulations-2026.json"
- **2018/065**: PDF sha256=3d1df61061f7e7987f3ab29bf46c4cd3... (2498439 bytes); record at "records/sis/2018/si-zm-2018-065-environmental-management-extended-producer-responsibility-regulations-2018.json"
- **2018/019**: PDF sha256=ef3fc1741373c8b1b8d50395f69e898d... (122850 bytes); record at "records/sis/2018/si-zm-2018-019-water-resources-management-licensing-of-drillers-and-constructors-regulations-20.json"
- **2018/020**: PDF sha256=59a66f0fc6408ba9ffa26a79783c13ae... (2144914 bytes); record at "records/sis/2018/si-zm-2018-020-water-resources-management-groundwater-and-boreholes-regulations-2018.json"
- **2021/091**: PDF sha256=d04f2e74c7414bb7d582c11839a58095... (311229 bytes); record at "records/sis/2021/si-zm-2021-091-high-court-civil-jurisdiction-family-court-fees-regulations-2021.json"
- **2012/028**: PDF sha256=d3b612d8254fb13a6984c994410ca802... (799303 bytes); record at "records/sis/2012/si-zm-2012-028-high-court-electronic-filling-rules-2012.json"
- **2008/003**: PDF sha256=0ed3910588f98cebe88f12a52ab4e744... (329778 bytes); record at "records/sis/2008/si-zm-2008-003-radiocommunications-licence-fees-regulations-2008.json"
- **2023/026**: PDF sha256=017af2d05e5b3d0a6707cce1ff7325fd... (395058 bytes); record at "records/sis/2023/si-zm-2023-026-national-heritage-conservation-commission-zambezi-source-national-monument-decla.json"

## Integrity Checks

- CHECK1 (id uniqueness): PASS
- CHECK2 (slot-prefix uniqueness): PASS
- CHECK3 (raw-file sha256 match): PASS
- CHECK4 (no broken cross-refs): PASS (no amended_by/repealed_by populated)
- CHECK5 (required fields populated): PASS

## Notes

- sis_data_protection alphabet sweep returned 0 keyword matches (only "radio*"-tagged ICT-adjacent items qualified, of which only 1 [2008/003 Radiocommunications Licence Fees] was retained as in-scope; "ionising radiation" and "education district offices" rejected as false positives at curation).
- Sub-phase rotation pattern follows batch-0213 and batch-0214 precedent: cached alphabet HTML re-used to identify 7 cross-sub_phase candidates, no additional fetches needed for discovery beyond initial 7 (robots + 6 alphabets).
- Cross-sub_phase records cover: 4 environmental management/water (high investor + ESG relevance: 2026 EIA Regs are the newly-promulgated successor regime; EPR Regs reflect Zambia's 2018 producer-pays adoption; water drillers + groundwater regs underpin all borehole/water-rights work for mining clients), 2 sis_courts (HC family court fees + HC e-filing rules — both procedural rules clients must comply with), 1 sis_mining (NHCC Zambezi Source monument — relevant for any extractive activity near declared heritage), 1 sis_data_protection (radiocomms licence fees — telecoms tariff regulator).
- No new gaps logged (all 8 PDFs parsed cleanly).
- Cumulative SI records after this batch: 317 (+8 over batch-0214's 309).
- Today fetch cost: ~258/2000 (12.9%) — well within budget.
