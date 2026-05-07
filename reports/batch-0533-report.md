# Batch 0533 — Phase 8 Nightly Re-verification (2026-05-07)

## Summary

Second Phase 8 tick. Deterministic sample of 8 records (1% of pool=1847,
capped by MAX_BATCH_SIZE=8) re-fetched from their canonical
`source_url`s; recomputed sha256 compared against stored `source_hash`.
**No records mutated** — Phase 8 is read-only on the corpus and only
appends drift findings to `gaps.md` for human triage.

| Field | Value |
|-------|-------|
| Phase | `phase_8_nightly_reverify` |
| Batch | `0533` |
| Parser/fetcher version | `phase8-reverify-0.1.0` |
| Seed | `phase8-reverify-2026-05-07` |
| Pool size | 1847 |
| Sample size | 8 |
| Match | 1 |
| Drift | 7 |
| Fetch error | 0 |
| Fetches issued | 8 |
| Started | 2026-05-07T06:40:33Z |
| Completed | 2026-05-07T06:41:14Z |
| Wall-clock | ~41s |

## Per-record verdicts

| Record id | Verdict | Status |
|-----------|---------|-------:|
| `act-zm-1996-019-zambia-institute-of-mass-communications-repeal-act-1996` | drift | 200 |
| `act-zm-2005-007-excess-expenditure-appropriation-2002-act` | drift | 200 |
| `act-zm-1955-010-census-and-statistics-act-1955` | drift | 200 |
| `si-zm-2022-061-electoral-process-local-government-by-elections-election-date-and-time-of-poll-no-2-order-2022` | drift | 200 |
| `act-zm-2007-024-zambia-tourism-board` | match | 200 |
| `act-zm-1929-016-dairies-and-dairy-produce-act-1929` | drift | 200 |
| `act-zm-cap-269-industrial-and-labour-relations-act` | drift | 200 |
| `act-zm-2013-019-appropriation-act` | drift | 200 |

Full per-fetch JSON: [`reports/batch-0533-reverify.json`](batch-0533-reverify.json).
Drift triage entries: see `gaps.md` § "Phase 8 — Nightly re-verification, batch 0533 (2026-05-07)".

## Pattern observation (cross-tick)

All 7 drifts target ZambiaLII HTML rendering URLs (`/akn/zm/act/.../eng@DATE`
or `/akn/zm/act/si/...`, no `/source.pdf` suffix). The single match is a
parliament.gov.zm PDF. This **reproduces the b0524 pattern**:

| Tick | ZambiaLII-HTML drifts | parliament-PDF / ZambiaLII-PDF matches |
|------|-----------------------|----------------------------------------|
| b0524 (2026-05-06) | 4/4 | 4/4 |
| b0533 (2026-05-07) | 7/7 (one is /akn/zm/act/si/...) | 1/1 |

ZambiaLII HTML pages routinely embed dynamic markup (view counters,
server timestamps, asset hashes, build IDs), so byte-level drift on
those URLs is the expected steady-state. Stable-source URLs
(parliament.gov.zm PDFs, ZambiaLII `/source.pdf` endpoints) continue to
match. This strengthens the b0524 recommendation: the Phase-8 verdict
for ZambiaLII HTML URLs should switch from `drift` to
`html_byte_drift_normalised_text_pending` once a normalised-text
comparison pipeline lands. Until then, drifts of sub-kind
`content_changed_full_drift` on `/akn/...` HTML URLs are informational
only and do not imply substantive content change.

## Integrity check

Phase-8-scope checks (per BRIEF.md §"Phase 8 — Nightly re-verification"):

- ✅ No records mutated (script writes nothing under `records/`).
- ✅ Sample is deterministic (re-runnable; same UTC date → same sample).
- ✅ Every fetch result has both `stored_sha256` (from disk) and
  `fetched_sha256` (newly computed) — the only verdicts are `match`,
  `drift`, or `fetch_error_<...>`.
- ✅ Drift entries appended to `gaps.md` (one row per drift in the
  triage table; sub-kind classified per b0524 vocabulary).
- ✅ approvals.yaml NOT modified (Phase 8 has not reached completion
  criteria; only a human flips `complete: true`).
- ✅ Rate limits honoured: zambialii.org @ 5s gap, parliament.gov.zm @
  2s gap (single host change observed in `_LAST_FETCH_BY_HOST`).

## Provenance

| Field | Value |
|-------|-------|
| User-Agent | `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` |
| Fetcher | `scripts/batch_0533_phase8_reverify.py` (clone of frozen baseline `scripts/batch_0524_phase8_reverify.py`; only BATCH and WORKSPACE constants changed) |
| Robots | All hosts in sample sets (`zambialii.org`, `www.parliament.gov.zm`) permit `User-Agent: *` for the queried paths (re-verified vs. b0524). |

## Budget impact

- Fetches: 8 (well under the 2000/day cap).
- Tokens: minimal (HTTP I/O only; no LLM invocations during the script).
- Daily fetch counter (worker-tick + judgment-ingestion-worker combined,
  approximate): see `costs.log`.

## Next-tick recommendation

- **2026-05-08 UTC:** the next deterministic seed
  `phase8-reverify-2026-05-08` will draw a fresh independent sample of 8
  records from the same pool (which will have grown slightly via the
  parallel judgment-ingestion-worker). No code changes anticipated.
- **Phase 8 completion criterion:** undefined in `approvals.yaml`
  (`complete: true` flip is human-only). The phase is by design
  open-ended: it samples 1%/night indefinitely. No worker action will
  flip `complete`.
- **Open recommendation (informational, human action required):** add a
  normalised-text comparison stage to the Phase-8 fetcher so that
  ZambiaLII HTML drifts can be classified more precisely. The pattern is
  now reproduced across two consecutive ticks (4/4 + 7/7 = 11/11
  HTML-URL drifts); raw-bytes comparison is the wrong primitive for
  these URLs.
