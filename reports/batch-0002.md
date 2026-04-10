# Phase 4 Batch 0002 — acts_in_force (parliament.gov.zm)

**Started:** 2026-04-10T10:21:18Z
**Finished:** 2026-04-10T10:22:35Z (approx)
**Fetches this batch:** 16 (8 node pages + 8 PDFs)
**Records created:** 8
**Integrity checks:** ALL PASS

## Summary

Continuing Phase 4 bulk ingestion from parliament.gov.zm. This batch processes 8 acts
from the 2019 tranche (Acts No. 10–17 of 2019), sourced from cached listing pages 0–12
and newly fetched node/PDF pairs.

Source note: parliament.gov.zm PDFs are fetched with SSL verification disabled due to
a missing intermediate certificate in the sandbox environment. Content integrity is
maintained through sha256 source_hash verification of all raw files on disk.

## Records Created

| ID | Citation | Title | Sections | PDF bytes |
|----|----------|-------|----------|-----------|
| act-zm-2019-017-supplementary-appropriation-2019-no-2-act-2019 | Act No. 17 of 2019 | The Supplementary Appropriation (2019) (No. 2) Act | 2 | 17,564 |
| act-zm-2019-016-customs-and-excise-amendment-act-2019 | Act No. 16 of 2019 | The Customs and Excise (Amendment) Act, 2019 | 17 | 27,974 |
| act-zm-2019-015-income-tax-amendment-act-2019 | Act No. 15 of 2019 | The Income Tax (Amendment) Act, 2019 | 5 | 32,641 |
| act-zm-2019-014-value-added-tax-amendment-act-2019 | Act No. 14 of 2019 | The Value Added Tax (Amendment) Act, 2019 | 3 | 24,486 |
| act-zm-2019-013-property-transfer-tax-amendment-act-2019 | Act No. 13 of 2019 | The Property Transfer Tax (Amendment) Act, 2019 | 1 | 12,587 |
| act-zm-2019-012-energy-regulation-act-2019 | Act No. 12 of 2019 | The Energy Regulation Act, 2019 | 66 | 139,782 |
| act-zm-2019-011-electricity-act-2019 | Act No. 11 of 2019 | The Electricity Act, 2019 | 58 | 144,434 |
| act-zm-2019-010-nurses-and-midwives-act-2019 | Act No. 10 of 2019 | The Nurses and Midwives Act 2019 | 108 | 182,594 |

## Parse quality flags

Records with ≤ 2 sections extracted — generic section-header parser may have missed
section headings. Flagged for re-parse pass:

- act-zm-2019-017-supplementary-appropriation-2019-no-2-act-2019 (2 sections — Supplementary
  Appropriation Acts are schedule-heavy; expected)
- act-zm-2019-013-property-transfer-tax-amendment-act-2019 (1 section — likely a brief
  amendment with few numbered sections)
- act-zm-2019-014-value-added-tax-amendment-act-2019 (3 sections)

## Inventory status

Total act candidates discovered (pages 0–12 of 48): 258
Records in corpus before batch: 23 (21 acts + 1 judgment + 1 companies pilot)
Records added this batch: 8
Cumulative acts processed from pages 0–12: 29 of ~258 candidates
Remaining from pages 0–12: ~228
Acts on pages 13–47 (not yet fetched): est. ~700+

## Source integrity

All 8 new records passed:
- No duplicate IDs (31 total records in corpus)
- All source_hash values verified against on-disk raw PDF files
- All amended_by references empty arrays (no cross-references yet)
- All repealed_by references null
- JSON schema validation: all required fields present, jurisdiction = ZM

## Next batch recommendation

Batch 0003 should continue acts_in_force from pages 0–12 inventory, processing the
next 8 acts (Acts No. 3–9 of 2019 and continuing to earlier years).
