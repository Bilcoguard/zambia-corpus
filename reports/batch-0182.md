# Batch 0182 — Phase 4 (sis_tax sub-phase)

**Batch:** 0182
**Phase:** phase_4_bulk
**Sub-phase:** sis_tax (priority_order item 3)
**Started:** 2026-04-24T13:05Z
**Completed:** 2026-04-24T13:10Z (executed as three 2-target slices to fit 45 s bash-tool timeout; all slices succeeded first try)
**Records written:** 6
**Fetches used:** 12 ingest fetches (6 × AKN HTML + 6 × PDF) + 2 earlier discovery fetches in this tick = 14
**Integrity:** ALL PASS (CHECK1 unique IDs, CHECK2 no HEAD ID/prefix collision, CHECK3 source_hash matches on-disk raw for all 6, CHECK4 no unresolved cross-refs, CHECK5 all required fields present)

## Records

| ID | Title | Sections | PDF bytes |
|---|---|---:|---:|
| si-zm-2000-020-income-tax-transfer-pricing-regulations-2000 | Income Tax (Transfer Pricing) Regulations, 2000 | 5 | 984,625 |
| si-zm-2009-047-income-tax-turnover-tax-regulations-2009 | Income Tax (Turnover Tax) Regulations, 2009 | 4 | 390,658 |
| si-zm-2014-050-income-tax-pay-as-you-earn-regulations-2014 | Income Tax (Pay As You Earn) Regulations, 2014 | 43 | 138,516 |
| si-zm-2018-005-independent-broadcasting-authority-television-levy-regulations-2018 | Independent Broadcasting Authority (Television Levy) Regulations, 2018 | 11 | 18,523 |
| si-zm-2023-001-income-tax-double-taxation-relief-taxes-on-income-united-arab-emirates-order-2023 | Income Tax (Double Taxation Relief) (Taxes on Income) (United Arab Emirates) Order, 2023 | 119 | 419,678 |
| si-zm-2025-090-income-tax-advance-income-tax-regulations-2025 | Income Tax (Advance Income Tax) Regulations, 2025 | 4 | 380,045 |

## Substance
Base-layer tax regulations with strong day-to-day practice value:
- **Transfer Pricing Regs 2000** — core cross-border pricing rules still cited in ZRA assessments (PE attribution, arm's length).
- **Turnover Tax Regs 2009** — primary small-trader turnover tax framework (was 3% of gross income at the time).
- **PAYE Regs 2014** — 43-section operative Pay-As-You-Earn collection regime (deduction, remittance, returns, penalties).
- **IBA TV Levy Regs 2018** — television licence levy on importers/distributors (small but cited in media-sector client work).
- **UAE DTA 2023** — 119-article double taxation treaty article-by-article (key Gulf counterparty; high withholding-tax planning value).
- **Advance Income Tax Regs 2025** — new 4-section regime for advance-tax collection (fresh from 2025 gazette, not yet widely cited).

## Discovery channel
Re-opened /legislation/?alphabet=I (returns 200) — this alphabet-filtered listing surfaces 98 SIs (70 tax-related, 54 novel vs HEAD) and replaces the exhausted /legislation/subsidiary pages 1-12 channel from batch 0178. Saved to `_work/batch_0182_candidates.json` for future sis_tax ticks.

Two 404 probes up front:
- `/akn/zm/act/si/2014` (year index) — 404
- `/legislation/subsidiary/?year=YYYY` — 404

So year-only index URLs do not exist on ZambiaLII; alphabet-filtered legislation pages do.

## Fetch detail
All 14 fetches honoured ZambiaLII robots.txt `Crawl-delay: 5` (6 s pacing with +1 s margin). User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`. Today fetches ~128/2000 (6.4% of daily budget). Endpoints used: `/akn/zm/act/si/YYYY/NN` + `/legislation/?alphabet=I` (both allowed per robots audit).

## Operational note
Script sliced into three 2-target invocations (`--slice=0:2`, `2:4`, `4:6`) to fit the sandbox's 45 s bash-tool timeout. Each invocation checkpoints into `_work/batch_0182_summary.json` and resumes the fetch counter on next slice. All six targets succeeded first attempt — no retries, no gaps.

## Next-tick plan
Continue sis_tax from the `_work/batch_0182_candidates.json` novel queue (48 remaining tax SIs on the 'I' page). Priority candidates for batch 0183:
- si/2022/032 Income Tax (John Snow Health Zambia) Approval & Exemption Order
- si/2024/065 Income Tax (GOPA Infra GmbH) Approval & Exemption Order
- si/2025/089 Income Tax (GOPA Infra GmbH) Approval & Exemption Order
- si/2017/074 Income Tax (Maamba Collieries interest exemption)
- si/2020/011 Income Tax (Royal Haskoning DHV) Approval & Exemption

After sis_tax reaches ~25 records (currently 20: 8 from 0180 + 6 from 0181 + 6 from 0182), rotate to sis_employment (priority_order item 4).

## Infrastructure (non-blocking)
Stale `corpus.sqlite-journal` rollback journal still blocks FTS rebuild — sandbox rm is denied. Human-side: delete journal, rebuild SQLite from `records/` JSON corpus to restore Phase 5 retrieval surface.

B2 raw sync deferred to host — rclone not available in sandbox:
```
rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4
```
