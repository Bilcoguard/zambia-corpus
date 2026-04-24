# Batch 0184 — Phase 4 (sis_employment sub-phase)

**Batch:** 0184
**Phase:** phase_4_bulk
**Sub-phase:** sis_employment (priority_order item 4)
**Started:** 2026-04-24T14:04Z (discovery) / 2026-04-24T14:06Z (ingest)
**Completed:** 2026-04-24T14:06:54Z (executed as three 2-target slices to fit 45 s bash-tool timeout; five of six targets succeeded, one logged as PDF parse empty)
**Records written:** 5
**Fetches used:** 14 total (2 discovery + 12 ingest = 6 × AKN HTML + 6 × PDF). Today's running fetch count ~152/2000 (7.6% of daily budget).
**Integrity:** ALL PASS (CHECK1 unique IDs within batch, CHECK2 batch IDs unique in HEAD, CHECK3 source_hash matches on-disk raw for all 5, CHECK4 no unresolved cross-refs, CHECK5 required fields present)

## Records

| ID | Title | Sections | PDF bytes |
|---|---|---:|---:|
| si-zm-2021-093-minimum-wages-and-conditions-of-employment-truck-and-bus-drivers-amendment-order | Minimum Wages and Conditions of Employment (Truck and Bus Drivers) (Amendment) Order, 2021 | 3 | 290,478 |
| si-zm-2011-002-minimum-wages-and-conditions-of-employment-general-order-2010 | Minimum Wages and Conditions of Employment (General) Order, 2010 | 15 | 1,097,828 |
| si-zm-2011-001-minimum-wages-and-conditions-of-employment-shop-workers-order-2011 | Minimum Wages and Conditions of Employment (Shop Workers) Order, 2011 | 17 | 1,436,909 |
| si-zm-2002-003-minimum-wages-and-conditions-of-employment-shop-workers-order-2002 | Minimum Wages and Conditions of Employment (Shop Workers) Order, 2002 | 11 | 10,451,275 |
| si-zm-2002-002-minimum-wages-and-conditions-of-employment-general-order-2002 | Minimum Wages and Conditions of Employment (General) Order, 2002 | 14 | 4,203,899 |

## Substance
Five Minimum-Wages-and-Conditions-of-Employment Orders spanning two decades of statutory wage-setting under the Minimum Wages and Conditions of Employment Act (Cap. 276) and its successor, the Employment Code Act, 3 of 2019. These are the operative prescribed-minimum-pay, working-hour, leave-entitlement and statutory-allowance orders that employment-law practice relies on for:

- **Historical reference / back-pay & arrears calculations.** General Orders 2002 and 2010, and Shop Workers Orders 2002 and 2011, give binding pre-Employment-Code minima for unlawful-deduction, underpayment, and unfair-dismissal remedies where the cause of action arose before the 2019 Code came into force.
- **Successive-order diachronic comparison.** Reading the 2002 General Order alongside the 2011 General Order and the 2023 General Order (already in HEAD as `si-zm-2023-048`) surfaces the drafting trajectory of housing allowance, transport allowance, overtime, and the protected-employee threshold — load-bearing for minimum-wage-increase advice.
- **Sector-specific rates.** The 2002 and 2011 Shop Workers Orders pair with the 2023 Shop Workers Order (`si-zm-2023-050`) and the 2023 Domestic Workers Order (`si-zm-2023-049`) to reconstruct the full historical ladder of sector-specific protected-employee wage floors.
- **Truck & Bus Drivers 2021 Amendment.** Amends the 2012 Truck and Bus Drivers Order (not yet in corpus) and sits between that base order and the 2020 Truck and Bus Drivers Order (`si-zm-2020-106`, already in HEAD) — useful for road-transport industry minimum-wage disputes.

The 2002 Shop Workers PDF is unusually large (10.5 MB) because it is a scanned image-plus-OCR hybrid; text extraction succeeded nevertheless (11 sections). No OCR fallback was required on this tick.

## Gaps logged
One target failed with `pdf_parse_empty` — text extraction returned no characters, almost certainly because the PDF is a pure scanned-image without an OCR layer:

- **si/2022/013** Minimum Wages and Conditions of Employment (Truck and Bus Drivers) (Amendment) Order, 2022 — logged to `gaps.md` at 2026-04-24T14:05:36Z. Raw PDF was fetched (hash in provenance.log) but not parsed to a record. Will require an OCR pre-pass (tesseract or cloud OCR) before re-ingestion; pair it with the other scanned-image tax SIs logged in batches 0179 and 0183 for a single consolidated OCR pass once approved.

## Discovery channel
Fresh discovery pass for this tick — `_work/batch_0184_discover.py` fetched `/legislation/?alphabet=E` and `/legislation/?alphabet=M` and filtered anchor texts on the keywords `employment code`, `minimum wages`, `labour`, `factories`, `workers' compensation`, `national pension scheme`, `napsa`, and `occupational safety/health`, skipping any year/number pair already present in HEAD as `si-zm-{year}-{number:03d}-…`. Six novel candidates surfaced; all six were targeted this tick. Output saved to `_work/batch_0184_candidates.json`.

Most E-alphabet and M-alphabet Employment-Code and Minimum-Wages SIs in the ZambiaLII catalogue are therefore now in HEAD or queued as scanned-image gaps. Further expansion of the sis_employment sub-phase should broaden the discovery net (NAPSA / Pensions and Insurance Authority / Workers' Compensation Fund / Factories / Occupational Health) under the N, P, W, F, and O alphabet pages respectively, and add the 2012 Truck & Bus Drivers base order (amended by `si-zm-2021-093` written this batch).

## Fetch detail
All 14 fetches honoured ZambiaLII robots.txt `Crawl-delay: 5` (6 s pacing with +1 s margin). User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`. Endpoints used: `/legislation/?alphabet=E`, `/legislation/?alphabet=M`, `/akn/zm/act/si/YYYY/NN` (HTML title/PDF-link discovery), and `/akn/zm/act/si/YYYY/NN/eng@DATE/source.pdf` (operative text).

## Operational note
Ingest script (`_work/batch_0184.py`) sliced into three 2-target invocations (`--slice=0:2`, `2:4`, `4:6`) to fit the sandbox's 45 s bash-tool timeout. Each invocation checkpoints to `_work/batch_0184_summary.json` and `.batch_0184_state.json`. All six targets attempted; five succeeded first try, one deterministic PDF-empty failure (scanned source, not a worker bug).

The `WORKSPACE` constant in `_work/batch_0184.py` hard-codes this tick's sandbox mount path (`/sessions/sharp-awesome-edison/mnt/corpus`) — the same per-session mount-path substitution pattern used by every prior batch script. Next tick must re-home the constant if executed in a new sandbox session.

## Next-tick plan
sis_employment sub-phase now has **10 records** in HEAD (5 pre-existing Employment-Code and Minimum-Wages SIs plus 5 written this batch) — note that the NAPSA / pension / superannuation regulations count under the same human sub-domain but were collected in earlier batches:

- `si-zm-2019-072` NAPSA Informal Sector Membership and Benefits Regulations 2019
- `si-zm-2017-019` National Pension Scheme Investment Regulations 2017
- `si-zm-2016-095` National Pension Scheme Medical Board Regulations 2016
- `si-zm-2022-016` Local Authorities Superannuation Fund Pension Management Rules 2022
- `si-zm-2020-048` Employment Code Exemption Regulations 2020
- `si-zm-2020-106` Minimum Wages Truck and Bus Drivers Order 2020
- `si-zm-2023-048` Employment Code Minimum Wages General Order 2023
- `si-zm-2023-049` Employment Code Domestic Workers Order 2023
- `si-zm-2023-050` Employment Code Shop Workers Order 2023
- `si-zm-2019-063` National Health Insurance General Regulations 2019

Suggested batch 0185 options (in priority order):

1. **Rotate to `case_law_scz`** (priority_order item 5). Judgment ingestion has different parsing ergonomics (judgment page → PDF judgment, different slug convention, `records/judgments/{year}/` layout) — worth restarting with a fresh pilot batch if `sis_employment` at 10 records is deemed a reasonable first-pass threshold.
2. **Extend sis_employment** by targeting NAPSA / Pensions-and-Insurance-Authority / Workers'-Compensation SIs from `/legislation/?alphabet=N` (NAPSA), `/alphabet=P` (Pensions), `/alphabet=W` (Workers'/Workmen's). Three discovery fetches → up to 6 ingest targets.
3. **OCR consolidation pass.** Combine the accumulated scanned-image SIs (si/2019/025, si/2017/043, si/2022/013) into a tesseract OCR rerun — requires approval since it introduces a new parser_version bump and potentially a new dependency in the sandbox.

Without further guidance from `approvals.yaml`, batch 0185 should default to option 2 (continue sis_employment) to keep the sub-phase coherent before rotating.

## Infrastructure (non-blocking)
Carried forward from batch 0183:

- Stale `corpus.sqlite-journal` rollback journal still blocks FTS rebuild — sandbox rm is denied. Human-side: delete journal, rebuild SQLite from `records/` JSON corpus to restore Phase 5 retrieval surface.
- Pre-existing duplicate IDs in `records/acts/` (34 acts exist as both `records/acts/{id}.json` AND `records/acts/{year}/{id}.json`) — not introduced by this batch.
- B2 raw sync deferred to host — rclone not available in sandbox:
  ```
  rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4
  ```
