# Phase 8 — Nightly re-verification: batch 0653

- **UTC window:** 2026-05-14T18:34:34Z → 2026-05-14T18:35:02Z
- **Worker:** worker-tick (scheduled, 30-min cadence — `phase-runner` lane)
- **Phase:** `phase_8_nightly_reverify` (approvals.yaml; sample_rate 0.01)
- **Parser/fetcher version:** `phase8-reverify-0.1.0`
- **Script:** `scripts/batch_0653_phase8_reverify.py` (clone of frozen
  baseline `scripts/batch_0546_phase8_reverify.py` via the most recent
  tick `scripts/batch_0652_phase8_reverify.py`; only the `BATCH`
  constant and the docstring batch-id changed for this tick — logic
  byte-for-byte identical to the baseline). `WORKSPACE` remains
  derived from the script's location so the tick is portable across
  sandboxes.
- **Seed:** `phase8-reverify-2026-05-14-b0653` (deterministic;
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

Of the 5 drifts, 4 are upstream-rendering-variance cohort members
(zambialii.org AKN-HTML `/eng@…` + judiciaryzambia.com CoA-judgment
HTML — both characterised across b0625 → b0652 as 100 %-drift cohorts)
and 1 is a new data-quality finding (truncated stored `source_hash`
for `act-zm-2020-018`; see Sample detail and gaps.md).

## Sample detail

| # | id | host | path-shape | verdict | stored_sha256 (prefix) | fetched_sha256 (prefix) |
|---|---|---|---|---|---|---|
| 1 | judgment-zm-2024-zmsc-02-mabvuto-mwale-and-anor-v-the-people | zambialii.org | AKN HTML `/eng@2024-04-19` | **drift** | 54befddc… | b424035d… |
| 2 | judgment-zm-2022-coa-091-douglas-aaron-simukonda-v-the-people | judiciaryzambia.com | WordPress page | **drift** | 92582702… | f23f75d9… |
| 3 | act-zm-2013-012-the-patents-and-companies-registration-agency-amendment-2013 | www.parliament.gov.zm | `/sites/default/files/documents/amendment_act/…PDF` | match | 3c7ea3e2… | 3c7ea3e2… |
| 4 | act-zm-1984-012-property-transfer-tax-act-1984 | zambialii.org | AKN HTML `/eng@1996-12-31` | **drift** | 3096e5e1… | 76da3d6e… |
| 5 | act-zm-1989-018-safety-of-civil-aviation-act-1989 | zambialii.org | AKN HTML `/eng@1996-12-31` | **drift** | 1ee90272… | db197b1a… |
| 6 | si-zm-2021-045-education-aided-educational-institutions-regulations-2021 | zambialii.org | `…/source.pdf` | match | 41a223e1… | 41a223e1… |
| 7 | si-zm-2023-001-income-tax-double-taxation-relief-taxes-on-income-united-arab-emirates-order-202 | zambialii.org | `…/source.pdf` | match | 0b717ed0… | 0b717ed0… |
| 8 | act-zm-2020-018-zambia-academy-of-sciences-act-2020 | www.parliament.gov.zm | `/sites/default/files/documents/acts/…pdf` | **drift** (truncated stored hash) | 67a7d56ceb24860f *(16-char TRUNCATED)* | 67a7d56c… |

(Stored prefixes match the per-record JSON in `records/`; see
`reports/batch-0653-reverify.json` for full 64-char hashes and byte
counts. **Row #8 — `act-zm-2020-018` — stored `source_hash` is only
16 hex chars: `sha256:67a7d56ceb24860f`. The fetched 64-char hash
starts with that same prefix, so underlying content matches; the
drift is a data-quality artefact in the stored record, not upstream
drift.**)

## Cohort interpretation

The 4 upstream drifts fall into the established drift cohorts:

- **zambialii.org AKN HTML `/eng@…` cohort** (Act/SI/judgment
  consolidated-snapshot HTML): 3 drifts this tick — `judgment-zm-2024-zmsc-02`
  on `/eng@2024-04-19`, `act-zm-1984-012` on `/eng@1996-12-31`,
  `act-zm-1989-018` on `/eng@1996-12-31`. Identical renderer
  variance to earlier `/eng@2020-10-26` / `/eng@2007-04-13` members;
  100 %-drift cohort.
- **judiciaryzambia.com CoA-judgment HTML cohort**: 1 drift —
  `judgment-zm-2022-coa-091-douglas-aaron-simukonda-v-the-people`.
  WordPress-rendered judgment page; embedded session/timestamp tokens
  shift between fetches; 100 %-drift cohort.

The 3 matches are stable static-PDF cohorts:

- `act-zm-2013-012` on `www.parliament.gov.zm`
  `/sites/.../amendment_act/Patents%20and%20Companies%28Amendment%29%20Act%202013.PDF`
  (parliament static-PDF mirror, deterministic).
- `si-zm-2021-045` on zambialii `…/source.pdf` (zambialii static-PDF
  endpoint, deterministic).
- `si-zm-2023-001` on zambialii `…/source.pdf` (zambialii static-PDF
  endpoint, deterministic).

The 1 truncated-stored-hash finding (`act-zm-2020-018`) is logged
separately in `gaps.md` as a data-quality issue; the parliament.gov.zm
static-PDF cohort is otherwise stable.

No `media.zambialii.org` candidates in this sample — that cohort
unchanged this tick.

### Cohort tallies post-b0653 (delta from b0652 cumulative)

- zambialii.org AKN HTML bare-path SI cohort:
  23 / 23 drift (100 %) — Δ+0 (no sample this tick)
- zambialii.org AKN HTML `/eng@…` Act-or-SI-or-judgment cohort:
  143 / 143 drift (100 %) — Δ+3
- judiciaryzambia.com CoA-judgment HTML cohort:
  4 / 4 drift (100 %) — Δ+1
- zambialii.org `/source.pdf` cohort: 54 / 54 stable (0 %) — Δ+2
- www.parliament.gov.zm `/acts/` and `/amendment_act/` cohort:
  134 / 135 stable (99.3 %) — Δ+2 stable, Δ+1 truncated-prefix-drift
- media.zambialii.org `/media/.../source_file/…pdf` cohort: stable — Δ+0
- **truncated_stored_hash findings**: 1 new this tick (`act-zm-2020-018`)

## Integrity checks (CHECK1 – CHECK8)

Phase 8 is read-only — `corpus.sqlite` and `records/*.json` were
NOT touched by this batch.

- **CHECK1** (no duplicate IDs in records/): n/a — no new records
  written. Pool composition unchanged from b0652 (1925 records).
- **CHECK2** (every `amended_by` reference resolves): n/a — no new
  records.
- **CHECK3** (every `repealed_by` reference resolves): n/a — no new
  records.
- **CHECK4** (every `cited_authorities` reference resolves): n/a —
  no new records.
- **CHECK5** (every `source_hash` matches on-disk raw file):
  out-of-scope (no on-disk raw mutation; remote-fetch reverify only).
- **CHECK6** (per-host rate-limits honoured): PASS — script uses
  `_LAST_FETCH_BY_HOST` with the limits in `RATE_LIMITS`
  (zambialii.org/media/judiciaryzambia 5s, default 2s).
- **CHECK7** (seed reproducibility): PASS — seed
  `phase8-reverify-2026-05-14-b0653` is deterministic from
  `utc_today()` + `BATCH`; re-running this script today yields the
  same 8 candidates.
- **CHECK8** (records vs records_fts parity): not relevant to this
  read-only tick; carried-forward host-side gap of ≥4 since
  repair-040 unchanged this tick (see worker.log).

All applicable integrity checks PASS. Phase 8 read-only nature means
no commit can violate corpus invariants.

## Provenance

- Started: 2026-05-14T18:34:34Z
- Completed: 2026-05-14T18:35:02Z
- Wall-clock: ~28 s (well within 20-min budget)
- Network fetches: 8 (HTTP 200 on every URL)
- Bytes down: ~1.1 MB
  (42,894 + 166,008 + 14,047 + 108,771 + 97,407 + 177,217 + 419,678
  + 51,426 ≈ 1.08 MB)
- LLM tokens: 0
- Storage delta: `reports/batch-0653-reverify.json` (~5 KB),
  `reports/batch-0653.md` (~7 KB), gaps.md append (~3.5 KB),
  scripts/batch_0653_phase8_reverify.py (clone, ~8 KB),
  worker.log + costs.log + provenance.log appends.
- robots.txt: respected (User-Agent
  `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`;
  no `Disallow` matches for any of the 8 URLs against the published
  `robots.txt` of zambialii.org / parliament.gov.zm /
  judiciaryzambia.com).
- Budget consumed today: 8 fetches this tick → cumulative
  ≥32/2000 fetches (well under daily cap); tokens ≈0/1,000,000.

## Phase status

`phase_8_nightly_reverify.complete` remains `false` per the
approval note ("Nightly re-verification of corpus integrity at 1 %
sample rate") — Phase 8 is a continuous-cycle phase. `approvals.yaml`
was **NOT** modified by this tick (non-negotiable #4 honoured).

## Next tick

`b0654-phase8` — next scheduled `phase-runner` invocation at
+30 min cadence. Same 1 %-of-1925 sampling; same MAX_BATCH=8;
deterministic next-day seed
`phase8-reverify-<UTC-date>-b0654`. Expected behaviour: identical
to b0625 → b0653 (~50 % match / ~50 % drift, drift confined to
known upstream-rendering cohorts plus any further truncated-hash
findings).
