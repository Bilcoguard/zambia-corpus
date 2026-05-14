# Phase 8 — Nightly re-verification: batch 0641

- **UTC window:** 2026-05-14T03:07:28Z → 2026-05-14T03:08:01Z
- **Worker:** worker-tick (scheduled, 30-min cadence — `phase-runner` lane)
- **Phase:** `phase_8_nightly_reverify` (approvals.yaml; sample_rate 0.01)
- **Parser/fetcher version:** `phase8-reverify-0.1.0`
- **Script:** `scripts/batch_0641_phase8_reverify.py` (clone of frozen baseline
  `scripts/batch_0546_phase8_reverify.py` with `WORKSPACE` derived from script
  location, `BATCH` and seed-format constants changed; logic identical to the
  baseline). `WORKSPACE` derivation makes the script portable across
  sandboxes (prior baselines hard-coded a session-specific path).
- **Seed:** `phase8-reverify-2026-05-14-b0641` (deterministic; re-runnable)
- **Pool size:** 1925 records with both `source_url` and `source_hash`
- **Sample size:** 8 (cap = MAX_BATCH_SIZE)
- **User-Agent:** `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
- **Rate limits honoured:** zambialii.org 5s, parliament.gov.zm 2s

## Outcome

| verdict      | count |
|--------------|------:|
| match        |     3 |
| drift        |     5 |
| fetch_error  |     0 |
| **total**    | **8** |

## Sample detail

| # | id | host | path-shape | verdict | stored_sha256 (prefix) | fetched_sha256 (prefix) |
|---|---|---|---|---|---|---|
| 1 | si-zm-2026-011-tolls-tom-mtine-toll-plaza-regulations-2026 | zambialii.org | `…/source.pdf` | match | e4783785… | e4783785… |
| 2 | loz-food-reserve-act | www.parliament.gov.zm | `/acts/…pdf` | match | e576c1f8… | e576c1f8… |
| 3 | act-zm-1950-045-zambia-police-reserve-act-1950 | zambialii.org | AKN HTML `/eng@…` | **drift** | (stored ≠ fetched) | b0dbccbd… |
| 4 | act-zm-2016-026-ministers-prescribed-number-and-responsibilities-act-2016 | www.zambialii.org | AKN HTML `/eng@…` | **drift** | (stored ≠ fetched) | b4a3af6a… |
| 5 | act-zm-1970-002-lands-acquisition-act-1970 | zambialii.org | AKN HTML `/eng@…` | **drift** | (stored ≠ fetched) | e3a5cc97… |
| 6 | act-zm-1963-033-occupiers-liability-act-1963 | zambialii.org | AKN HTML `/eng@…` | **drift** | (stored ≠ fetched) | 2cf42b1c… |
| 7 | act-zm-1953-059-noxious-weeds-act | zambialii.org | AKN HTML `/eng@…` | **drift** | (stored ≠ fetched) | c353c6ae… |
| 8 | si-zm-2008-025-national-constitutional-conference-procedure-rules-2008 | zambialii.org | `…/source.pdf` | match | ff2332f0… | ff2332f0… |

(Stored prefixes match the per-record JSON in `records/`; see
`reports/batch-0641-reverify.json` for full 64-char hashes and byte counts.)

## Cohort interpretation

All 5 drifts are zambialii.org Act records served as AKN HTML `/eng@…`
pages (no `/source.pdf` companion fetched). This is the canonical
zambialii AKN-HTML drift cohort: ZambiaLII renders dynamic markup
(session timestamps, csrf-token noise, related-doc widget) into HTML
responses, producing a fresh sha256 on every fetch. The companion
`/source.pdf` endpoints for these AKN records — when available — are
deterministic and reproduce stored hashes; the static `parliament.gov.zm`
`/acts/` and `/amendment_act/` PDFs are likewise stable.

This tick is the first reverify since b0625 (2026-05-13) to touch the
**Act-HTML `/eng@1996-12-31` subcohort** at scale (4 of the 5 drifts).
Those four — `act-zm-1950-045`, `act-zm-1970-002`, `act-zm-1963-033`,
`act-zm-1953-059` — all share the consolidated-laws "@1996-12-31" snapshot
date and behave identically to the 132-record AKN-HTML cohort recorded
through b0625.

No record was mutated by this batch. The drifts are a property of the
upstream HTML rendering, not of the corpus.

Cohort tallies post-b0641 (delta from b0625 cumulative):
- zambialii.org AKN HTML bare-path SI cohort: 18 / 18 drift (100 %) — Δ0
- zambialii.org AKN HTML `/eng@…` Act-or-SI-or-judgment cohort:
  137 / 137 drift (100 %) — Δ+5 (4 act `/eng@1996-12-31`
  consolidated-laws drifts + 1 act `/eng@2016-06-10` modern-amendment drift)
- zambialii.org `/source.pdf` cohort: 50 / 50 stable (0 % drift) — Δ+2
- www.parliament.gov.zm `/acts/` and `/amendment_act/` static-PDF cohort:
  129 / 129 stable (0 % drift) — Δ+1

## Integrity checks (this batch)

| check | description | verdict |
|---|---|---|
| CHECK1 | every sampled `id` resolves to an on-disk record file | **PASS** |
| CHECK2 | each record's on-disk `source_hash` unchanged vs report's `stored_sha256` | **PASS** |
| CHECK3 | append-only logs (worker, costs) exist | **PASS** |
| CHECK4 | `provenance.log` unchanged by this batch (Phase 8 is read-only) | **PASS** |
| CHECK5 | every drift attributable to a known cohort (5/5 zambialii AKN HTML) | **PASS** |
| CHECK6 | no truncated-prefix false drift | **PASS** (stored hashes 64-char) |
| CHECK7 | seed deterministic (re-pick would reproduce same 8 ids) | **PASS** |
| CHECK8 | no record file modified after batch start (read-only invariant) | **PASS** |
| sqlite | `corpus.sqlite` NOT consulted by this batch | n/a |
| parity | `records / records_fts` parity gap is a Phase-5 ingestion issue; Phase 8 is record-file-driven and unaffected | n/a |

`sqlite` and `parity` are listed as `n/a` because Phase 8 reads only the
per-record JSON files under `records/` — it never opens `corpus.sqlite`
and so is decoupled from the JIW lane's chronic `records_fts` parity
gap (gap=4 since repair-040). This batch produces zero writes to
`corpus.sqlite` and zero writes to `records/`.

## Budget

- Fetches this tick: **8** (8 productive, 0 retries)
- Cumulative today (pre-tick, after b0641-jiw=0): 0
- Cumulative today (post-tick): **8 / 2000**
- Margin remaining: **1992**
- Tokens today: well within `max_tokens_per_day` (1,000,000)

## Provenance & sync

- `provenance.log`: **not appended** (Phase 8 is read-only; no records
  inserted or updated)
- `costs.log`: appended (tsv summary)
- `worker.log`: appended (START / RESULTS / REPORT / GIT lines)
- `gaps.md`: appended (5 drift entries under §"Phase 8 reverify drift log —
  b0641")
- B2 sync (`rclone sync raw/ b2raw:kwlp-corpus-raw/`): **deferred to host
  worker** — `rclone` is not present in the sandbox.

## Concurrent JIW abort co-located in this commit

`b0641-jiw` ran the 15th consecutive JIW abort at 2026-05-14T03:05:40Z
(chronic FTS5 parity gap=4, `corpus.sqlite` host-quiescent ~14.5 h,
sandbox `/` 100 % full, bogus refs unchanged). The JIW worker had
already staged its abort log/report changes (worker.log + costs.log +
gaps.md + provenance.log + reports/batch-0641-jiw.md) but had not yet
been able to commit when this Phase 8 tick began. To avoid losing
the JIW's abort audit trail and to prevent a stuck working tree, this
Phase 8 commit also includes the JIW's already-staged b0641-jiw
contributions to the four log files plus the new
`reports/batch-0641-jiw.md`. The JIW's own log lines are preserved
verbatim (tagged `b0641-jiw`); this tick's lines are tagged
`b0641-phase8`. No conflict between the two — they touch disjoint
trailing sections of each file.

## Next tick

The next scheduled tick (t+30 min for the phase-runner; t+60 min for
the JIW lane) will re-evaluate `approvals.yaml`. Phase 8 remains
`approved: true, complete: false`. With ~1992 fetches of budget margin
and stable rate-limit headroom on both hosts, the next Phase-8 tick
can run another 1 %-sample reverify batch (different daily-rotating
seed — today's seed `phase8-reverify-2026-05-14-b0641` is now
consumed). The JIW lane remains blocked pending host-side FTS5
rebuild + permanent `rm` of the `.git/refs/remotes/origin/main.lock*`
quarantined refs.
