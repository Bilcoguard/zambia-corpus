# Phase 8 — Nightly re-verification: batch 0642

- **UTC window:** 2026-05-14T03:16:05Z → 2026-05-14T03:16:37Z
- **Worker:** worker-tick (scheduled, 30-min cadence — `phase-runner` lane)
- **Phase:** `phase_8_nightly_reverify` (approvals.yaml; sample_rate 0.01)
- **Parser/fetcher version:** `phase8-reverify-0.1.0`
- **Script:** `scripts/batch_0642_phase8_reverify.py` (clone of frozen
  baseline `scripts/batch_0546_phase8_reverify.py` via the most recent
  tick `scripts/batch_0641_phase8_reverify.py`; only the `BATCH`
  constant and a one-line docstring metadata edit changed for this
  tick — logic byte-for-byte identical to the baseline). `WORKSPACE`
  remains derived from the script's location so the tick is portable
  across sandboxes.
- **Seed:** `phase8-reverify-2026-05-14-b0642` (deterministic;
  re-runnable; verified by CHECK7 below)
- **Pool size:** 1925 records with both `source_url` and `source_hash`
- **Sample size:** 8 (cap = MAX_BATCH_SIZE)
- **User-Agent:** `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
- **Rate limits honoured:** zambialii.org 5s, media.zambialii.org 5s,
  judiciaryzambia.com 5s, parliament.gov.zm 2s

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
| 1 | si-zm-2023-026-national-heritage-conservation-commission-zambezi-source-national-monument-decla | zambialii.org | `…/source.pdf` | match | 017af2d0… | 017af2d0… |
| 2 | si-zm-2017-063-local-forest-no-42-kawena-cessation-order-2017 | zambialii.org | AKN bare-path SI `/akn/zm/act/si/2017/63` | **drift** | 70626f8f… | 5d731d62… |
| 3 | judgment-zm-2026-coa-128-robert-mwanza-v-mtn-zambia-limited | judiciaryzambia.com | CoA-judgment HTML `/appeal-…-jja/` | **drift** | 2533c2ba… | 65a33989… |
| 4 | act-zm-2007-008-supplementary-appropriation-2005-act | zambialii.org | AKN HTML `/eng@2007-04-13` | **drift** | 7207777c… | 1821aedf… |
| 5 | act-zm-2024-023-value-added-tax-2024 | www.parliament.gov.zm | `/sites/default/files/documents/acts/…pdf` | match | 582c1a17… | 582c1a17… |
| 6 | act-zm-1965-051-bretton-woods-agreement-act-1965 | zambialii.org | AKN HTML `/eng@1996-12-31` | **drift** | ded42caa… | 8409f6d8… |
| 7 | si-zm-2020-027-income-tax-remission-ndola-lime-company-limited-order-2020 | media.zambialii.org | `/media/legislation/…/source_file/…pdf` | match | 8ee9a2f9… | 8ee9a2f9… |
| 8 | si-zm-2021-003-national-forest-no-f31-kabwe-alteration-of-boundaries-order-2021 | zambialii.org | AKN bare-path SI `/akn/zm/act/si/2021/3` | **drift** | 9d091f5d… | aaeae8ad… |

(Stored prefixes match the per-record JSON in `records/`; see
`reports/batch-0642-reverify.json` for full 64-char hashes and byte
counts.)

## Cohort interpretation

All 5 drifts fall into the three previously-characterised drift cohorts.
No record was mutated by this batch — Phase 8 is read-only.

- **zambialii.org AKN HTML bare-path SI cohort** (no
  `/eng@…` / no `/source.pdf` suffix): 2 drifts — `si-zm-2017-063`
  and `si-zm-2021-003`. Bare-path SI requests render a dynamic
  consolidated-laws HTML page with session tokens; 100 %-drift since
  first observation.
- **zambialii.org AKN HTML `/eng@…` cohort** (Act/SI/judgment
  consolidated-snapshot HTML): 2 drifts — `act-zm-2007-008` on
  `/eng@2007-04-13` (year-original snapshot) and `act-zm-1965-051` on
  `/eng@1996-12-31` (consolidated-laws snapshot). Identical renderer
  to the `eng@1996-12-31` variant; 100 %-drift.
- **judiciaryzambia.com CoA-judgment HTML cohort** (post-slug pages
  under `/appeal-…/`): 1 drift — `judgment-zm-2026-coa-128`. This is
  the third member of the cohort (1/1 at first observation, 2/2 at
  the b0641-bounding-tick gaps.md note, now **3/3**). WordPress-style
  page widgets (related posts, share counts, post-meta) drive the
  hash variance; the underlying judgment text and PDF references on
  the page are stable across fetches but the surrounding chrome is
  not. Same upstream-rendering attribution as the zambialii AKN HTML
  drift — not corpus mutation.

The three matches are all stable static-PDF cohorts:
- `si-zm-2023-026` on zambialii `…/source.pdf` (zambialii static-PDF
  endpoint, deterministic).
- `act-zm-2024-023` on `www.parliament.gov.zm` `/acts/…pdf`
  (parliament static-PDF mirror, deterministic).
- `si-zm-2020-027` on `media.zambialii.org`
  `/media/legislation/…/source_file/…pdf` (zambialii media CDN
  static-PDF asset, deterministic — first observed stable in b0565,
  rolled into the combined stable-PDF cohort).

Cohort tallies post-b0642 (delta from b0641 cumulative):
- zambialii.org AKN HTML bare-path SI cohort:
  20 / 20 drift (100 %) — Δ+2 (`si-zm-2017-063`, `si-zm-2021-003`)
- zambialii.org AKN HTML `/eng@…` Act-or-SI-or-judgment cohort:
  139 / 139 drift (100 %) — Δ+2 (`act-zm-2007-008` on `/eng@2007-04-13`,
  `act-zm-1965-051` on `/eng@1996-12-31`)
- judiciaryzambia.com CoA-judgment HTML cohort:
  3 / 3 drift (100 %) — Δ+1 (`judgment-zm-2026-coa-128`)
- zambialii.org `/source.pdf` cohort: 51 / 51 stable (0 % drift) — Δ+1
- www.parliament.gov.zm `/acts/` and `/amendment_act/` static-PDF cohort:
  130 / 130 stable (0 % drift) — Δ+1
- media.zambialii.org `/media/.../source_file/…pdf` cohort (rolled into
  the combined stable-PDF cohort): stable — Δ+1

## Integrity checks (this batch)

| check | description | verdict |
|---|---|---|
| CHECK1 | every sampled `id` resolves to an on-disk record file | **PASS (8/8)** |
| CHECK2 | each record's on-disk `source_hash` unchanged vs report's `stored_sha256` | **PASS (8/8)** |
| CHECK3 | append-only logs (worker, costs) exist | **PASS** |
| CHECK4 | `provenance.log` mtime ≤ batch start (Phase 8 is read-only — no provenance append) | **PASS** |
| CHECK5 | every drift attributable to a known cohort (5/5 attributed: 2 bare-path SI + 2 `/eng@…` + 1 judiciaryzambia CoA HTML) | **PASS** |
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
- Cumulative today (pre-tick, after b0641-phase8=8): 8
- Cumulative today (post-tick): **16 / 2000**
- Margin remaining: **1984**
- Tokens today: well within `max_tokens_per_day` (1,000,000)

## Provenance & sync

- `provenance.log`: **not appended** (Phase 8 is read-only; no records
  inserted or updated)
- `costs.log`: appended (tsv summary, tagged `b0642-phase8`)
- `worker.log`: appended (START / RESULTS / REPORT / GIT lines)
- `gaps.md`: appended (5 drift entries under §"Phase 8 reverify drift log —
  b0642")
- B2 sync (`rclone sync raw/ b2raw:kwlp-corpus-raw/`): **deferred to host
  worker** — `rclone` is not present in the sandbox.

## Next tick

The next scheduled tick will re-evaluate `approvals.yaml`. Phase 8
remains `approved: true, complete: false`. With ~1984 fetches of budget
margin and stable rate-limit headroom on all hosts, the next Phase-8
tick can run another 1 %-sample reverify batch (different
daily-rotating seed — today's seeds
`phase8-reverify-2026-05-14-b0641` and
`phase8-reverify-2026-05-14-b0642` are now consumed). The JIW lane
remains blocked pending host-side FTS5 rebuild + permanent `rm` of
the `.git/refs/remotes/origin/main.lock*` quarantined refs (unchanged
since b0626).
