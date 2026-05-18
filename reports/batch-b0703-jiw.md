# Batch b0703-jiw — CoA hand-curated drain (+3 records)

**Worker:** Zambia Authorities Corpus judgment ingestion worker (JIW)

**Tick start:** 2026-05-18T14:09:42Z

**Parser version:** `0.3.6-jiw-b0703-hand-curated`

**Mode:** hand-curated from on-disk raw PDFs (zero net HTTP fetches)

**Implementing:** b0701-jiw report's recommended priority #1 — Court of Appeal NEW records from judiciaryzambia.com (Mtonga, Skab Merchants, Tulambo Kumwenda)

## Records inserted (3)

| ID | Case number | Outcome | Judges |
|---|---|---|---|
| `judgment-zm-2026-coa-110-josias-mtonga-v-the-people` | APP/110/2024 | allowed | Mchenga DJP, Majula JJA, Muzenga JJA |
| `judgment-zm-2026-coa-344-skab-merchants-ltd-v-emilmark-construction` | APP/344/2023 | allowed | Siavwapa JP, Chishimba JJA, Patel JJA |
| `judgment-zm-2026-coa-047-tulambo-kumwenda-v-solwezi-dairy-farm-and-ors` | APP/047/2025 | dismissed | Chashi JJA, Ngulube JJA, Banda-Bobo JJA |

## Records deferred (0)

None.

## Integrity checks

| Check | Result | Notes |
|---|---|---|
| CHECK1 (≥1 judge) | PASS | 3-judge panels for all three |
| CHECK2 (issue_tags non-empty) | PASS | criminal/commercial/property cohorts |
| CHECK3 (outcome from enum) | PASS | quashed, allowed, dismissed |
| CHECK6 (raw_sha256 matches PDF on disk) | PASS | All hashes re-verified post-insert |
| CHECK8 (records == records_fts; quick_check=ok) | PASS | DB integrity maintained |

## Outcome detection methodology

Parser v0.3.6-jiw-b0703 applied a 3-tier outcome scan:

1. **Operative section slice** — from the last `CONCLUSION`/`ORDERS`/`DISPOSITION` anchor to EOF.
2. **Last 4 pages** — fallback for judgments where operative paragraph is on penultimate page.
3. **Tail 12,000 chars** — final fallback.


## Source attribution

All three PDFs were originally fetched from judiciaryzambia.com during prior CoA sweep ticks (raw files on disk). This tick performs zero net HTTP requests.

## Fetch cost

- Network fetches: **0**
- JIW daily budget: 0 / 500 used today
- Bandwidth: 0 bytes

## Recommended priority for next JIW tick

1. **Continue CoA judiciaryzambia.com sweep** from page 1 (most recent) — survey remaining unaddressed PDFs on disk.
2. **SCZ judiciaryzambia.com sweep** from page 2 (cursor unchanged) — Supreme Court coverage is light.
3. **ZMCC judiciaryzambia.com sweep** — not yet started; complements existing ZambiaLII ZMCC coverage.
4. **Maintainer action** (human-only): dedup-policy decision on `case_number-collision-multiple-rulings-same-petition` cohort.

## Notes

- **Mtonga**: Criminal appeal. Conviction and sentence quashed; appellant acquitted. Coded `quashed`.
- **Skab Merchants**: Commercial appeal re sale of goods. Appeal substantially succeeds on all grounds except special damages. Coded `allowed`.
- **Tulambo Kumwenda**: Land/civil appeal re Solwezi Dairy Farm. Sole ground failed; appeal dismissed with costs. Coded `dismissed`.
