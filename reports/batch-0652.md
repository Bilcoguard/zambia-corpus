# Phase 8 — Nightly re-verification: batch 0652

- **UTC window:** 2026-05-14T18:23:07Z → 2026-05-14T18:23:30Z
- **Worker:** worker-tick (scheduled, 30-min cadence — `phase-runner` lane)
- **Phase:** `phase_8_nightly_reverify` (approvals.yaml; sample_rate 0.01)
- **Parser/fetcher version:** `phase8-reverify-0.1.0`
- **Script:** `scripts/batch_0652_phase8_reverify.py` (clone of frozen
  baseline `scripts/batch_0546_phase8_reverify.py` via the most recent
  tick `scripts/batch_0642_phase8_reverify.py`; only the `BATCH`
  constant changed for this tick — logic byte-for-byte identical to
  the baseline). `WORKSPACE` remains derived from the script's
  location so the tick is portable across sandboxes.
- **Seed:** `phase8-reverify-2026-05-14-b0652` (deterministic;
  re-runnable; verified by CHECK7 below)
- **Pool size:** 1925 records with both `source_url` and `source_hash`
- **Sample size:** 8 (cap = MAX_BATCH_SIZE)
- **User-Agent:** `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
- **Rate limits honoured:** zambialii.org 5s, media.zambialii.org 5s,
  judiciaryzambia.com 5s, parliament.gov.zm 2s

## Outcome

| verdict      | count |
|--------------|------:|
| match        |     4 |
| drift        |     4 |
| fetch_error  |     0 |
| **total**    | **8** |

## Sample detail

| # | id | host | path-shape | verdict | stored_sha256 (prefix) | fetched_sha256 (prefix) |
|---|---|---|---|---|---|---|
| 1 | si-zm-2021-073-public-holidays-declaration-no-4-notice-2021 | zambialii.org | AKN bare-path SI `/akn/zm/act/si/2021/73` | **drift** | 0a1b2f12… | 57b9b1f6… |
| 2 | act-zm-cap-257-national-assembly-staff-act | www.parliament.gov.zm | `/sites/default/files/documents/acts/…pdf` | match | f7a8759b… | f7a8759b… |
| 3 | si-zm-1991-030-medical-aid-societies-and-nursing-homes-exemption-establishment-and-operation-au | zambialii.org | `…/source.pdf` | match | fa17918c… | fa17918c… |
| 4 | act-zm-2020-002-national-forensic-act-2020 | www.zambialii.org | AKN HTML `/eng@2020-10-26` | **drift** | b0d8fd37… | 635777ee… |
| 5 | si-zm-1994-049-zambia-revenue-authority-commencement-and-disengagement-order-1994 | zambialii.org | AKN bare-path SI `/akn/zm/act/si/1994/49` | **drift** | 3ac6b26e… | 05e53515… |
| 6 | act-zm-2021-030-the-chartered-institute-of-logistics-and-transport-amendment-act-2021 | www.parliament.gov.zm | `/sites/default/files/documents/acts/…pdf` | match | e9c8f416… | e9c8f416… |
| 7 | si-zm-2022-057-urban-and-regional-planning-designated-local-planning-authorities-regulations-2022 | zambialii.org | AKN bare-path SI `/akn/zm/act/si/2022/57` | **drift** | 2f173dab… | 9dde5cc2… |
| 8 | act-zm-2022-023-the-penal-code-amendment-act-2022 | www.parliament.gov.zm | `/sites/default/files/documents/acts/…pdf` | match | f8553d34… | f8553d34… |

(Stored prefixes match the per-record JSON in `records/`; see
`reports/batch-0652-reverify.json` for full 64-char hashes and byte
counts.)

## Cohort interpretation

All 4 drifts fall into the two zambialii.org AKN HTML drift cohorts
that have been characterised across b0625 → b0642. No record was
mutated by this batch — Phase 8 is read-only.

- **zambialii.org AKN HTML bare-path SI cohort** (no
  `/eng@…` / no `/source.pdf` suffix): 3 drifts — `si-zm-2021-073`,
  `si-zm-1994-049`, `si-zm-2022-057`. Bare-path SI requests render a
  dynamic consolidated-laws HTML page with session tokens; 100 %-drift
  since first observation.
- **zambialii.org AKN HTML `/eng@…` cohort** (Act/SI/judgment
  consolidated-snapshot HTML): 1 drift — `act-zm-2020-002` on
  `/eng@2020-10-26` (year-original snapshot). Identical renderer
  variance to the earlier `/eng@2007-04-13` and `/eng@1996-12-31`
  members; 100 %-drift.

The 4 matches are all stable static-PDF cohorts:
- `si-zm-1991-030` on zambialii `…/source.pdf` (zambialii static-PDF
  endpoint, deterministic).
- `act-zm-cap-257` on `www.parliament.gov.zm`
  `/sites/.../acts/National%20Assembly%20Staff%20Act.pdf` (parliament
  static-PDF mirror, deterministic).
- `act-zm-2021-030` on `www.parliament.gov.zm`
  `/sites/.../acts/Act%20No.%2030%20OF%202021…pdf` (parliament
  static-PDF mirror, deterministic).
- `act-zm-2022-023` on `www.parliament.gov.zm`
  `/sites/.../acts/Act%20No.%2023%20Penal%20Code%20%28Amendment%29%2C%202022.pdf`
  (parliament static-PDF mirror, deterministic).

No `judiciaryzambia.com` and no `media.zambialii.org` candidates in
this sample — those cohorts unchanged this tick.

Cohort tallies post-b0652 (delta from b0642 cumulative):
- zambialii.org AKN HTML bare-path SI cohort:
  23 / 23 drift (100 %) — Δ+3 (`si-zm-2021-073`, `si-zm-1994-049`,
  `si-zm-2022-057`)
- zambialii.org AKN HTML `/eng@…` Act-or-SI-or-judgment cohort:
  140 / 140 drift (100 %) — Δ+1 (`act-zm-2020-002` on
  `/eng@2020-10-26`)
- judiciaryzambia.com CoA-judgment HTML cohort:
  3 / 3 drift (100 %) — Δ+0 (no sample this tick)
- zambialii.org `/source.pdf` cohort: 52 / 52 stable (0 % drift) — Δ+1
- www.parliament.gov.zm `/acts/` and `/amendment_act/` static-PDF cohort:
  133 / 133 stable (0 % drift) — Δ+3
- media.zambialii.org `/media/.../source_file/…pdf` cohort: stable — Δ+0

## Integrity checks (this batch)

| check | description | verdict |
|---|---|---|
| CHECK1 | every sampled `id` resolves to an on-disk record file | **PASS (8/8)** |
| CHECK2 | each record's on-disk `source_hash` unchanged vs report's `stored_sha256` | **PASS (8/8)** |
| CHECK3 | append-only logs (worker, costs) exist | **PASS** |
| CHECK4 | `provenance.log` not modified by this tick (Phase 8 is read-only) | **PASS** |
| CHECK5 | every drift attributable to a known cohort (4/4 attributed: 3 bare-path SI + 1 `/eng@…`) | **PASS** |
| CHECK6 | no truncated-prefix false drift | **PASS** (all 8 stored hashes 64-char) |
| CHECK7 | seed deterministic (re-pick reproduces same 8 ids in same order) | **PASS** |
| CHECK8 | no record file modified after batch start (read-only invariant) | **PASS (8/8)** |
| sqlite | `corpus.sqlite` NOT consulted by this batch | n/a |
| parity | `records / records_fts` parity gap is a Phase-5 ingestion issue; Phase 8 is record-file-driven and unaffected | n/a |

`sqlite` and `parity` are listed as `n/a` because Phase 8 reads only the
per-record JSON files under `records/` — it never opens `corpus.sqlite`
and so is decoupled from the JIW lane's chronic `records_fts` parity
gap (gap=4 since repair-040). This batch produces zero writes to
`corpus.sqlite` and zero writes to `records/`.

## Budget

- Fetches this tick: **8** (8 productive, 0 retries)
- Cumulative today (pre-tick, after b0641-phase8=8 + b0642-phase8=8): 16
- Cumulative today (post-tick): **24 / 2000**
- Margin remaining: **1976**
- Tokens today: well within `max_tokens_per_day` (1,000,000)

## Provenance & sync

- `provenance.log`: **not appended** (Phase 8 is read-only; no records
  inserted or updated)
- `costs.log`: appended (tsv summary, tagged `b0652-phase8`)
- `worker.log`: appended (START / RESULTS / REPORT / GIT lines)
- `gaps.md`: appended (4 drift entries under §"Phase 8 reverify drift log —
  b0652")
- B2 sync (`rclone sync raw/ b2raw:kwlp-corpus-raw/`): **deferred to host
  worker** — `rclone` is not present in the sandbox.

## Next tick

The next scheduled tick will re-evaluate `approvals.yaml`. Phase 8
remains `approved: true, complete: false`. With ~1976 fetches of budget
margin and stable rate-limit headroom on all hosts, the next Phase-8
tick can run another 1 %-sample reverify batch (different
daily-rotating seed — today's seeds
`phase8-reverify-2026-05-14-b0641`,
`phase8-reverify-2026-05-14-b0642`, and
`phase8-reverify-2026-05-14-b0652` are now consumed). The JIW lane
remains blocked pending host-side FTS5 rebuild + permanent `rm` of
the residual quarantined refs / journals (unchanged since b0626).
