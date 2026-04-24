# Batch 0181 — Phase 4 (sis_tax sub-phase)

**Batch:** 0181
**Phase:** phase_4_bulk
**Sub-phase:** sis_tax (priority_order item 3)
**Started:** 2026-04-24T12:32Z
**Completed:** 2026-04-24T~12:35Z (run across two Python invocations: first killed by sandbox bash-timeout at record 3/6 after full fetch+write; resumed with TARGETS reduced to remaining 3)
**Records written:** 6
**Fetches used:** 12 (6 × AKN HTML + 6 × PDF fallback)
**Integrity:** ALL PASS (CHECK1 unique, CHECK2 no HEAD collision, CHECK3 source_hash matches on-disk raw for all 6, CHECK4 no unresolved cross-refs, CHECK5 required fields present)

## Records

| ID | Title | Sections | PDF bytes |
|---|---|---:|---:|
| si-zm-2017-041-income-tax-double-taxation-relief-taxes-on-income-kingdom-of-norway-order-2017 | Income Tax (Double Taxation Relief) (Taxes on Income) (Kingdom of Norway) Order, 2017 | 102 | 231,016 |
| si-zm-2015-095-income-tax-double-taxation-relief-taxes-on-income-netherlands-order-2015 | Income Tax (Double Taxation Relief) (Taxes on Income) (Netherlands) Order, 2015 | 126 | 256,375 |
| si-zm-2015-070-income-tax-double-taxation-relief-taxes-on-income-ireland-order-2015 | Income Tax (Double Taxation Relief) (Taxes on Income) (Ireland) Order, 2015 | 110 | 159,089 |
| si-zm-2015-020-income-tax-double-taxation-relief-taxes-on-income-republic-of-botswana-order-201 | Income Tax (Double Taxation Relief) (Taxes on Income) (Republic of Botswana) Order, 2015 | 118 | 152,578 |
| si-zm-2015-030-property-transfer-tax-exemption-order-2015 | Property Transfer Tax (Exemption) Order, 2015 | 2 | 92,677 |
| si-zm-2015-031-property-transfer-tax-approval-and-exemption-order-2015 | Property Transfer Tax (Approval and Exemption) Order, 2015 | 4 | 93,624 |

## Substance
Four Double Taxation Avoidance Agreements (Norway, Netherlands, Ireland, Botswana) — each carries full treaty articles as numbered sections (102–126). High citation value for cross-border tax planning and withholding-tax advice. Two Property Transfer Tax Orders (2015/30 Exemption, 2015/31 Approval & Exemption) — lightweight compliance orders with 2–4 sections each.

## Fetch detail
All 12 fetches honoured ZambiaLII robots.txt `Crawl-delay: 5` (6 s pacing with +1 s margin). User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`. Today fetches ~124/2000 (6.2% of daily budget). Endpoints used: `/akn/zm/act/si/YYYY/NN` (allowed) — no use of `/search/api/` or `/api/` (disallowed per robots.txt audit from batch 0172).

## Operational note
First Python invocation was killed by the sandbox 45 s bash-tool timeout after writing records for 2017/41, 2015/95, 2015/70 (records + raw + costs.log + provenance.log writes all completed for those 3 before kill). The kill terminated the script before the state-summary JSON could be emitted. Recovery: TARGETS narrowed to the 3 unwritten slots (2015/20, 2015/30, 2015/31) and re-run succeeded. Final integrity re-verified over all 6 JSON records against on-disk raw PDFs.

## Next-tick plan
Continue sis_tax with the next wave from the batch-0180 queued list:
- si/2014/68, si/2014/69 — VAT 2014 historical amendments
- Additional novel tax candidates from cached `/legislation/subsidiary` pages 4–10

After sis_tax reaches ~20 records (currently 14: 8 from batch-0180 + 6 here), rotate to sis_employment (priority_order item 4).

## Infrastructure (non-blocking)
Stale `corpus.sqlite-journal` rollback journal still blocks FTS rebuild — sandbox rm is denied. Human-side: delete journal, rebuild SQLite from `records/` JSON corpus to restore Phase 5 retrieval surface.

B2 raw sync deferred to host — rclone not available in sandbox:
```
rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4
```
