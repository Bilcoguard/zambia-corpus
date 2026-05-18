# Phase 8 — Nightly re-verification: batch 0625

- **UTC window:** 2026-05-13T04:34:45Z → 2026-05-13T04:35:14Z
- **Worker:** worker-tick (scheduled, 30-min cadence)
- **Phase:** `phase_8_nightly_reverify` (approvals.yaml; sample_rate 0.01)
- **Parser/fetcher version:** `phase8-reverify-0.1.0`
- **Script:** `scripts/batch_0625_phase8_reverify.py` (clone of frozen baseline
  `scripts/batch_0546_phase8_reverify.py` with `WORKSPACE`, `BATCH`, and
  seed-format constants changed; logic identical to the baseline)
- **Seed:** `phase8-reverify-2026-05-13-b0625` (deterministic; re-runnable)
- **Pool size:** 1925 records with both `source_url` and `source_hash`
- **Sample size:** 8 (cap = MAX_BATCH_SIZE)
- **User-Agent:** `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
- **Rate limits honoured:** zambialii.org 5s, parliament.gov.zm 2s

## Outcome

| verdict      | count |
|--------------|------:|
| match        |     5 |
| drift        |     3 |
| fetch_error  |     0 |
| **total**    | **8** |

## Sample detail

| # | id | host | verdict | stored_sha256 (prefix) | fetched_sha256 (prefix) |
|---|---|---|---|---|---|
| 1 | act-zm-2019-018-the-appropriation-act-2019 | www.parliament.gov.zm | match | acf5c17c… | acf5c17c… |
| 2 | si-zm-2017-042-income-tax-overseas-private-investment-corporation-approval-and-exemption-order- | zambialii.org | match | b3f84893… | b3f84893… |
| 3 | judgment-zm-2023-zmsc-04-attorney-general-v-siakakole-and-ors | zambialii.org | **drift** | 258e5467… | 2e834e6f… |
| 4 | act-zm-2016-024-the-supreme-court-amendment | www.parliament.gov.zm | match | 8ebfc08f… | 8ebfc08f… |
| 5 | si-zm-2000-037-pension-scheme-regulation-investment-exemption-order-2000 | zambialii.org | match | a1b94078… | a1b94078… |
| 6 | act-zm-2025-003-cyber-security-act | zambialii.org | **drift** | 538b241e… | 14117329… |
| 7 | si-zm-2020-002-national-assembly-by-election-chilubi-constituency-no-095-election-date-and-time-of-poll-order-2020 | zambialii.org | **drift** | 53ca8519… | ba8cd268… |
| 8 | act-zm-2021-020-rural-electrification-amendment-act-2021 | www.parliament.gov.zm | match | 98d867f2… | 98d867f2… |

## Drift analysis

All three drifts fall into the known **`zambialii.org` AKN HTML rendering
cohorts** — re-fetches of:

- `https://zambialii.org/akn/zm/judgment/zmsc/2023/4/eng@2023-02-23` —
  AKN HTML `/eng@…` Act-or-judgment cohort (drift #3).
- `https://zambialii.org/akn/zm/act/2025/3/eng@2025-04-15` — same
  cohort (drift #6).
- `https://zambialii.org/akn/zm/act/si/2020/2` — bare-AKN-path SI
  cohort, no `/eng@…` suffix, no `/source.pdf` (drift #7).

These cohorts have shown 100% drift across all prior Phase 8 ticks where
they have appeared (AKN toolchain renders HTML with non-deterministic
byte content across fetches: timestamp comments, embedded session ids,
pagination tokens). The corresponding `/source.pdf` URLs on the same
host remain 100% stable (drifts #2 and #5 were `/source.pdf` and both
matched).

Per Phase 8's read-only mandate: **no record was mutated**, **no
`source_hash` rewritten**, **no `provenance.log` entry added**. The three
drifts are noted here for the human reviewer; they reinforce the existing
recommendation (see prior batch reports) to prefer canonical PDF URLs over
bare AKN HTML paths and `/eng@…` HTML paths when (re-)ingesting from
zambialii.org.

Cohort tally post-b0625 (approximate, based on prior reports):
- zambialii.org AKN HTML bare-path SI cohort: 18/18 drift (100%) — +1
- zambialii.org AKN HTML `/eng@…` Act-or-SI-or-judgment cohort: 132/132 drift (100%) — +2
- zambialii.org `/source.pdf` cohort: 48/48 stable (0%) — +2
- www.parliament.gov.zm `/acts/` and `/amendment_act/` static-PDF cohort: 128/128 stable (0%) — +3

## Integrity checks (this batch)

| check | description | verdict |
|---|---|---|
| CHECK1 | every sampled `id` resolves to an on-disk record file | **PASS** |
| CHECK2 | each record's on-disk `source_hash` unchanged vs report's `stored_sha256` | **PASS** |
| CHECK3 | append-only logs (worker, costs, provenance) exist | **PASS** |
| CHECK4 | `provenance.log` unchanged by this batch (Phase 8 is read-only) | **PASS** |
| CHECK5 | every drift attributable to a known cohort | **PASS** (3/3 zambialii.org AKN HTML) |
| CHECK6 | no truncated-prefix false drift | **PASS** |
| CHECK7 | seed deterministic (re-pick reproduces same 8 ids) | **PASS** |
| CHECK8 | no record file modified after batch start (read-only invariant) | **PASS** |
| sqlite | `PRAGMA quick_check` / `PRAGMA integrity_check` | **ok** / **ok** |
| counts | records=1928, records_fts=1928 (parity preserved) | **PASS** |

## Budget

- Fetches this tick: **8** (8 productive)
- Retries: 0
- Cumulative today (pre-tick): 24
- Cumulative today (post-tick): **32 / 2000**
- Margin remaining: **1968**
- Tokens today: well within `max_tokens_per_day` (1,000,000)

## Provenance & sync

- `provenance.log`: **not appended** (Phase 8 is read-only; no records
  inserted or updated)
- `costs.log`: appended (tsv summary)
- `worker.log`: appended
- `gaps.md`: appended (3 drift entries under §"Phase 8 reverify drift log")
- B2 sync (`rclone sync raw/ b2raw:kwlp-corpus-raw/`): **deferred to host
  worker** — `rclone` is not present in the sandbox.

## Next tick

The next scheduled tick (t+30 min) will re-evaluate `approvals.yaml`. Phase 8
remains `approved: true, complete: false`. With ~1968 fetches of budget
margin and stable rate-limit headroom on both hosts, the next tick can run
another 1%-sample reverify batch (different daily-rotating seed if executed
on the next UTC day; today's seeds b0623 / b0624 / b0625 are now consumed).
