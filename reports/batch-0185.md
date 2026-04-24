# Batch 0185 — Phase 4 (sis_employment sub-phase, NAPSA/Pensions/Workers Comp/Factories expansion)

**Batch:** 0185
**Phase:** phase_4_bulk
**Sub-phase:** sis_employment (priority_order item 4, continued)
**Started:** 2026-04-24T14:32Z (discovery) / 2026-04-24T14:34Z (ingest)
**Completed:** 2026-04-24T14:41Z (executed as three slices to fit 45 s bash-tool timeout)
**Records written:** 8
**Fetches used:** 21 total (5 discovery alphabet pages + 16 ingest = 8 × AKN HTML + 8 × PDF). Today's running fetch count ~171/2000 (8.6% of daily budget).
**Integrity:** ALL PASS (CHECK1 unique IDs within batch, CHECK2 all batch IDs now in HEAD, CHECK3 source_hash matches on-disk raw for all 8, CHECK4 no unresolved cross-refs, CHECK5 required fields present)

## Records

| ID | Title | Sections | PDF bytes |
|---|---|---:|---:|
| si-zm-2024-003-national-pension-scheme-penalty-waiver-regulations-2024 | National Pension Scheme (Penalty Waiver) Regulations, 2024 | 26 | see provenance.log |
| si-zm-2021-090-national-pension-scheme-pensionable-earnings-amendment-regulations-2021 | National Pension Scheme (Pensionable Earnings) (Amendment) Regulations, 2021 | 2 | see provenance.log |
| si-zm-2021-050-pension-scheme-investment-guidelines-regulations-2021 | Pension Scheme (Investment Guidelines) Regulations, 2021 | 43 | see provenance.log |
| si-zm-2018-008-factories-plant-inspection-and-examination-fees-regulations-2018 | Factories (Plant Inspection and Examination Fees) Regulations, 2018 | 12 | see provenance.log |
| si-zm-2014-001-national-pension-scheme-exemption-variation-order-2014 | National Pension Scheme (Exemption) (Variation) Order, 2014 | 2 | see provenance.log |
| si-zm-2011-004-workers-compensation-permanent-disablementcommutation-of-pension-regulation-2011 | Workers Compensation (Permanent Disablement)(Commutation of Pension) Regulation, 2011 | 5 | see provenance.log |
| si-zm-2005-025-workers-compensation-assessment-of-earnings-regulations | Workers' Compensation (Assessment of Earnings) Regulations | 3 | see provenance.log |
| si-zm-2002-041-pension-scheme-returns-regulations-2002 | Pension Scheme (Returns) Regulations, 2002 | 7 | see provenance.log |

## Substance
Eight Statutory Instruments filling the NAPSA / Pensions and Insurance Authority / Workers' Compensation Fund / Factories Act corner of employment-and-social-security law that batch 0184 flagged for follow-up. These are the operative SIs practitioners reach for when advising on pension contributions, exemptions, investment compliance, workplace-injury benefits, and statutory plant-inspection levies:

- **NAPSA penalty waiver and pensionable-earnings framework.** `si-zm-2024-003` is the 2024 NAPSA penalty-waiver regime (26 sections — the largest SI in this batch), pairing with `si-zm-2021-090` (pensionable-earnings cap amendment) and the existing `si-zm-2019-072` Informal Sector Membership and Benefits Regulations to reconstruct the full NAPSA contribution-and-enforcement architecture.
- **Pension scheme investment compliance.** `si-zm-2021-050` Pension Scheme (Investment Guidelines) Regulations 2021 (43 sections) is the PIA's binding investment-mandate framework for pension-fund trustees and investment managers — load-bearing for trustee-duty, prudent-person-rule, and asset-allocation disputes. Pairs with `si-zm-2002-041` Pension Scheme (Returns) Regulations 2002 (statutory-return filing obligations) and the existing `si-zm-2017-019` National Pension Scheme Investment Regulations.
- **Historical NAPSA-exemption variations.** `si-zm-2014-001` National Pension Scheme (Exemption) (Variation) Order 2014 supplements the existing `si-zm-2019-072` body of Informal Sector Regulations, giving the historical exemption-contour for pre-2019 disputes.
- **Workers' Compensation.** `si-zm-2011-004` (commutation of permanent-disablement pension) and `si-zm-2005-025` (assessment of earnings) are the operative WCFCB benefit-calculation SIs for workplace-injury claims under the Workers' Compensation Act (Cap. 271). The 2005 Assessment of Earnings Regulations govern how pre-accident earnings are computed for lump-sum and pension compensation.
- **Factories Act.** `si-zm-2018-008` Factories (Plant Inspection and Examination Fees) Regulations 2018 sets the statutory fee schedule for the Factories Inspectorate, relevant to compliance audits and employer cost-of-compliance calculations.

## Gaps logged
None on this tick. All eight PDFs parsed cleanly to structured sections — no OCR fallback required, no `pdf_parse_empty` failures.

## Discovery channel
Fresh discovery pass for this tick — `_work/batch_0185_discover.py` fetched five ZambiaLII legislation index pages (`/legislation/?alphabet={N,P,W,F,O}`) and filtered anchor texts on the keywords `napsa`, `national pension scheme`, `pensions and insurance`, `pension scheme`, `workers' compensation`, `workmen's compensation`, `occupational safety/health`, `factories act`, `minimum wages`, `employment code/act`, and `labour`, skipping any year/number pair already present in HEAD as `si-zm-{year}-{number:03d}-…`.

13 novel candidates surfaced; top 8 (newest-first sort) were targeted this tick. Output saved to `_work/batch_0185_candidates.json`. 5 residual candidates deferred to the next tick:

- si/2002/039 Pension Scheme (Offshore Investments) Regulations 2002
- si/2000/037 Pension Scheme Regulation (Investment) (Exemption) Order 2000
- si/2000/034 National Pension Scheme (Transfer of Employees) Order 2000
- si/2000/022 National Pension Scheme (Pensionable Earnings) Regulations 2000
- si/1994/039 Workmen's Compensation (Assessment of Earnings) Regulations 1994

## Fetch detail
All 21 fetches honoured ZambiaLII robots.txt `Crawl-delay: 5` (6 s pacing with +1 s margin). User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`. Endpoints used: `/legislation/?alphabet={N,P,W,F,O}`, `/akn/zm/act/si/YYYY/NN` (HTML title/PDF-link discovery), and `/akn/zm/act/si/YYYY/NN/eng@DATE/source.pdf` (operative text).

## Operational note
Ingest script (`_work/batch_0185.py`) sliced into three invocations (`--slice=0:3`, `3:6`, `6:8`) to fit the sandbox's 45 s bash-tool timeout. Each invocation checkpoints to `_work/batch_0185_summary.json` and `.batch_0185_state.json`. All eight targets attempted; all eight succeeded first try.

The `WORKSPACE` constant in `_work/batch_0185.py` hard-codes this tick's sandbox mount path (`/sessions/clever-cool-johnson/mnt/corpus`) — the same per-session mount-path substitution pattern used by every prior batch script. Next tick must re-home the constant if executed in a new sandbox session.

## Next-tick plan
sis_employment sub-phase now has **18 records** in HEAD (10 pre-existing + 8 written this batch). Residual queue for the next sis_employment tick (5 candidates from this discovery + additional gaps flagged in batch 0184):

- 5 pre-2002 pension / workmen's compensation SIs listed in "Discovery channel" above
- si/2012 Truck & Bus Drivers base order (referenced by amendments in HEAD: si-zm-2020-106 and si-zm-2021-093) — requires targeted year/number discovery since 2012 is not surfaced by current alphabet scans
- OCR backlog: si/2022/013 (from batch 0184) plus scanned-image tax SIs from batches 0179 and 0183 — defer for a consolidated OCR pre-pass

Alternatively, the next tick may rotate to an earlier priority_order item (acts_in_force, sis_corporate, sis_tax) given that ~150 fetches of today's 2000-fetch budget have already been spent and these sub-phases have greater legal-practice density per record. priority_order selection is not this tick's decision.
