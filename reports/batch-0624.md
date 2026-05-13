# Phase 8 — Nightly re-verification: batch 0624

- **UTC window:** 2026-05-13T04:23:34Z → 2026-05-13T04:23:58Z
- **Worker:** worker-tick (scheduled, 30-min cadence)
- **Phase:** `phase_8_nightly_reverify` (approvals.yaml; sample_rate 0.01)
- **Parser/fetcher version:** `phase8-reverify-0.1.0`
- **Script:** `scripts/batch_0624_phase8_reverify.py` (clone of frozen baseline
  `scripts/batch_0546_phase8_reverify.py` with `WORKSPACE`, `BATCH`, and
  seed-format constants changed; logic identical to the baseline)
- **Seed:** `phase8-reverify-2026-05-13-b0624` (deterministic; re-runnable)
- **Pool size:** 1925 records with both `source_url` and `source_hash`
- **Sample size:** 8 (cap = MAX_BATCH_SIZE)
- **User-Agent:** `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
- **Rate limits honoured:** zambialii.org 5s, parliament.gov.zm 2s

## Outcome

| verdict      | count |
|--------------|------:|
| match        |     6 |
| drift        |     2 |
| fetch_error  |     0 |
| **total**    | **8** |

## Sample detail

| # | id | host | verdict | stored_sha256 (prefix) | fetched_sha256 (prefix) |
|---|---|---|---|---|---|
| 1 | act-zm-2009-006-excess-expenditure-appropriation-2006 | www.parliament.gov.zm | match | c9aff037… | c9aff037… |
| 2 | act-zm-2019-014-value-added-tax-amendment-act-2019 | www.parliament.gov.zm | match | bc0cb8b6… | bc0cb8b6… |
| 3 | si-zm-2023-005-energy-regulation-appeals-tribunal-rules-2023 | zambialii.org | **drift** | (stored) | e7f23bb7… |
| 4 | act-zm-2026-006-food-reserve-act | www.parliament.gov.zm | match | 4f00fef6… | 4f00fef6… |
| 5 | si-zm-2019-047-local-government-fire-services-order-2019 | zambialii.org | **drift** | (stored) | 6289c200… |
| 6 | si-zm-2019-029-employment-code-act-commencement-order-2019 | zambialii.org | match | 51ee180d… | 51ee180d… |
| 7 | act-zm-cap-213-valuation-surveyors-act | www.parliament.gov.zm | match | b148fd2c… | b148fd2c… |
| 8 | si-zm-2015-070-income-tax-double-taxation-relief-taxes-on-income-ireland-order-2015 | zambialii.org | match | 3022007b… | 3022007b… |

## Drift analysis

Both drifts fall into the known **`zambialii.org` AKN HTML bare-AKN-path SI
cohort** — re-fetches of `https://zambialii.org/akn/zm/act/si/{year}/{n}`
(no `/eng@…` suffix, no `/source.pdf`) return HTML rendered by the AKN
toolchain with non-deterministic byte content across ticks. This cohort has
shown 100% drift across all prior Phase 8 ticks where it has appeared, while
the corresponding `/source.pdf` URLs on the same host are 100% stable.

Per Phase 8's read-only mandate: **no record was mutated**, **no
`source_hash` rewritten**, **no `provenance.log` entry added**. The two
drifts are noted here for the human reviewer; they reinforce the existing
recommendation (see prior batch reports) to prefer canonical PDF URLs over
bare AKN HTML paths when (re-)ingesting from zambialii.org.

Cohort tally post-b0624 (approximate, based on prior reports):
- zambialii.org AKN HTML bare-path SI cohort: 17/17 drift (100%)
- zambialii.org AKN HTML `/eng@…` Act-or-SI cohort: 130/130 drift (100%)
- zambialii.org `/source.pdf` cohort: 46/46 stable (0%)
- www.parliament.gov.zm `/acts/` static-PDF cohort: 125/125 stable (0%)

## Integrity checks (this batch)

| check | description | verdict |
|---|---|---|
| CHECK1 | every sampled `id` resolves to an on-disk record file | **PASS** |
| CHECK2 | each record's on-disk `source_hash` unchanged vs report's `stored_sha256` | **PASS** |
| CHECK3 | append-only logs (worker, costs, provenance) exist | **PASS** |
| CHECK4 | `provenance.log` unchanged by this batch (Phase 8 is read-only) | **PASS** |
| CHECK5 | every drift attributable to a known cohort | **PASS** (2/2) |
| CHECK6 | no truncated-prefix false drift | **PASS** |
| CHECK7 | seed deterministic (re-pick reproduces same 8 ids) | **PASS** |
| CHECK8 | no record file modified after batch start (read-only invariant) | **PASS** |
| sqlite | `PRAGMA quick_check` / `PRAGMA integrity_check` | **ok** / **ok** |
| counts | records=1928, records_fts=1928 (parity preserved) | **PASS** |

## Budget

- Fetches this tick: **8** (8 productive)
- Retries: 0
- Cumulative today (pre-tick): 16
- Cumulative today (post-tick): **24 / 2000**
- Margin remaining: **1976**
- Tokens today: well within `max_tokens_per_day` (1,000,000)

## Provenance & sync

- `provenance.log`: **not appended** (Phase 8 is read-only; no records
  inserted or updated)
- `costs.log`: appended (tsv + json summary)
- `worker.log`: appended
- B2 sync (`rclone sync raw/ b2raw:kwlp-corpus-raw/`): **deferred to host
  worker** — `rclone` is not present in the sandbox.

## Next tick

The next scheduled tick (t+30 min) will re-evaluate `approvals.yaml`. Phase 8
remains `approved: true, complete: false`. With ~1976 fetches of budget
margin and stable rate-limit headroom on both hosts, the next tick can run
another 1%-sample reverify batch (different daily-rotating seed if executed
on the next UTC day; same seed on this UTC day is now consumed by b0624).
