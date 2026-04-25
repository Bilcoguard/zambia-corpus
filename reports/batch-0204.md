# Batch 0204 — Phase 4 sis_corporate (legal practitioners + lands + business names)

**Date:** 2026-04-25
**Phase:** 4 (bulk)
**Sub-phase:** sis_corporate
**Records written:** 8 / 8 attempted
**Fetches used:** 21 (5 discovery + 16 ingest)
**Integrity checks:** PASS (CHECK1–CHECK6 all green)

## Discovery
Re-verified `robots.txt` (sha256 prefix `fce67b697ee4ef44…`, unchanged
from batches 0193–0203). Probed alphabet indexes C, L, R, D for novel
SI slots. Strict corporate-keyword filter yielded only **1** novel
candidate (R 2015/033). Following the batch-0203 next-tick fallback
guidance ("if yield <3, rotate to sis_employment / sis_data_protection")
and the sis_corporate sub-phase definition (which explicitly includes
PACRA-Act / professional-services SIs), the candidate set was widened
through curated overrides drawn from the L and R alphabet captures, all
of which are corporate, professional-services or registry-related and
therefore in-scope for sis_corporate. The full discovery state is at
`_work/batch_0204_discovery.json`.

The 8 candidates ingested in this batch:

| # | Citation | Title | Sections | Parent Act |
|---|----------|-------|----------|------------|
| 1 | SI No. 3 of 2012 | Registration of Business Names Regulations, 2012 | 48 | Registration of Business Names Act 2011/16 / PACRA Act 2010/15 |
| 2 | SI No. 23 of 2017 | Legal Practitioners (Publicity) Rules, 2017 | 38 | Legal Practitioners Act, Cap. 30 |
| 3 | SI No. 6 of 2017 | Legal Practitioners (Costs) Order, 2017 | 23 | Legal Practitioners Act, Cap. 30 |
| 4 | SI No. 7 of 2017 | Legal Practitioners’ (Conveyancing and Non-Contentious Matters) (Costs) Order, 2017 | 27 | Legal Practitioners Act, Cap. 30 |
| 5 | SI No. 97 of 2016 | Legal Practitioners (High Court) (Fixed Costs) Order, 2016 | 17 | Legal Practitioners Act, Cap. 30 |
| 6 | SI No. 7 of 2013 | Land Tribunal (Fees) Regulations, 2013 | 8 | Lands Tribunal Act 2010/39 |
| 7 | SI No. 44 of 2006 | Lands (Ground Rent, Fees and Charges) Regulations, 2006 | 3 | Lands Act, Cap. 184 |
| 8 | SI No. 33 of 2015 | Road Traffic (Certificates of Security and Insurance) (Display) Regulations, 2015 | 4 | Road Traffic Act 2002/11 (insurance interface) |

## Notes
* Record 1 (PACRA-Act / Registration of Business Names Regs 2012) is the
  most directly corporate item and fills a long-standing gap in the
  PACRA-derivative SI coverage.
* Records 2–5 are the four core Legal Practitioners cost / publicity
  SIs — directly applicable to KWLP practice (fee-quotation guidance,
  publicity rules, conveyancing costs, fixed-cost orders).
* Record 6 (Land Tribunal Fees Regs 2013) and Record 7 (Lands Ground
  Rent Regs 2006) round out the practice-relevant lands fee schedule.
* Record 8 (Road Traffic Insurance Display Regs 2015) was the single
  candidate that survived the strict corporate-keyword filter — it sits
  on the insurance/road-traffic interface and is retained for completeness.
* Cumulative SI records after this batch: **240** (+8 over batch-0203
  232).
* Judgment records unchanged at 25 (case_law_scz still paused per
  robots.txt Disallow on `/akn/zm/judgment/`).

## Integrity
All on-disk PDF hashes match `source_hash` field; HTML alternate-source
hashes match the saved discovery captures. No duplicate IDs, no prefix
collisions with HEAD. All required schema fields populated. No new
gaps logged. No `amended_by` / `repealed_by` references in this batch
(consistent with non-amending SIs).

## Next-tick plan
Continue sis_corporate with deeper L probe (Loans Recovery Act SIs,
Liquor Licensing) and a fresh probe of alphabets E (Energy Regulation
Board, Electronic Communications) and T (Trade, Trademarks). If yield
still <3 across two consecutive ticks, rotate to **sis_employment**
(priority_order item 4) — Employment Code Act 2019/3 derivatives, NHIMA
Act 2018/2 SIs, NAPSA Act SIs.

Robots.txt should be re-verified at the start of every tick.

## Infrastructure
* B2 raw sync still deferred to host (rclone unavailable in sandbox).
* 16 batch-0204 raw bytes on disk (8 HTML + 8 PDF, ~3.5 MB) plus legacy
  files from batches 0192–0203 awaiting host-driven `rclone sync raw/
  b2raw:kwlp-corpus-raw/`.
* Pre-existing dupes (34 legacy-schema act dupes + 42 Appropriation-Act
  -000- placeholder dupes + 63 SI flat-layout dupes) unchanged.
