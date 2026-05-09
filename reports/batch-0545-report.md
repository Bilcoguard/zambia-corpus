# Batch 0545 — Phase 8 Nightly Re-verification (2026-05-08, late-UTC tick)

## Summary

Fourth Phase 8 tick. Deterministic sample of 8 records (1% of pool=1853,
capped by MAX_BATCH_SIZE=8) re-fetched from their canonical
`source_url`s; recomputed sha256 compared against stored `source_hash`.
**No records mutated** — Phase 8 is read-only on the corpus and only
appends drift findings to `gaps.md` for human triage.

Tick scheduling note: this tick fired at `2026-05-08T23:03:51Z` (sandbox
local time `2026-05-09 ~01:04 CAT`). UTC date is still 2026-05-08, so
the deterministic seed `phase8-reverify-2026-05-08` matches the seed
used by b0538 at 07:21Z. However the candidate pool has grown from 1849
(at b0538 time) to 1853 (4 new records inserted by judgment-ingestion-worker
batches b0540 and b0543 between the two ticks), so `random.Random.sample`
draws a different — though overlapping — 8-record subset. This is
expected and documented behaviour: a deterministic seed produces an
identical sample only when the population is also identical.

The next tick that crosses the UTC midnight boundary will use the fresh
seed `phase8-reverify-2026-05-09`.

| Field | Value |
|-------|-------|
| Phase | `phase_8_nightly_reverify` |
| Batch | `0545` |
| Parser/fetcher version | `phase8-reverify-0.1.0` |
| Seed | `phase8-reverify-2026-05-08` |
| Pool size | 1853 |
| Sample size | 8 |
| Match | 1 |
| Drift | 7 |
| Fetch error | 0 |
| Fetches issued | 8 |
| Started | 2026-05-08T23:03:51Z |
| Completed | 2026-05-08T23:04:32Z |
| Wall-clock | ~41s |

## Per-record verdicts

| Record id | Verdict | Status |
|-----------|---------|-------:|
| `si-zm-2017-020-tourism-and-hospitality-prepaid-package-tours-regulations-2017` | drift | 200 |
| `act-zm-1989-001-zambia-centre-for-accountancy-studies-act-1989` | drift | 200 |
| `act-zm-2025-003-cyber-security-act` | drift | 200 |
| `si-zm-2020-018-compulsory-standards-potable-spirits-declaration-order-2020` | drift | 200 |
| `act-zm-2017-022-appropriation` | match | 200 |
| `act-zm-1963-027-law-reform-frustrated-contracts-act-1963` | drift | 200 |
| `judgment-zm-2021-zmcc-17-anderson-mwale-buchisa-mwalongo-and-kola-odubote-v` | drift | 200 |
| `act-zm-1997-013-appropriation-act-1997` | drift | 200 |

Full per-fetch JSON: [`reports/batch-0545-reverify.json`](batch-0545-reverify.json).
Drift triage entries: see `gaps.md` § "Phase 8 — Nightly re-verification, batch 0545 (2026-05-08, late-UTC)".

## Pattern observation (cross-tick, four-tick reproduction)

All 7 drifts target ZambiaLII `/akn/...` HTML rendering URLs (5 acts,
2 SIs, and the same `/akn/zm/judgment/zmcc/2021/17/eng@2021-09-20`
judgment URL first seen at b0538 — drifted again this tick, confirming
per-fetch CMS-driven byte-level instability). The single match is a
stable parliament.gov.zm PDF endpoint. The pattern from b0524 + b0533 +
b0538 is now reproduced for a fourth consecutive tick:

| Tick | ZambiaLII-HTML drifts | Stable-PDF matches |
|------|-----------------------|--------------------|
| b0524 (2026-05-06) | 4/4 | 4/4 |
| b0533 (2026-05-07) | 7/7 | 1/1 |
| b0538 (2026-05-08 early) | 6/6 | 2/2 |
| b0545 (2026-05-08 late)  | 7/7 | 1/1 |
| **Cumulative**     | **24/24 HTML-URL drifts** | **8/8 PDF-URL matches** |

Three records sampled in b0545 were also sampled in b0538 (overlap is
expected because b0538's 8-record sample drew from a 1849-row pool that
forms a strict subset of b0545's 1853-row pool):
`act-zm-1989-001-zambia-centre-for-accountancy-studies-act-1989`
(drift→drift),
`act-zm-2025-003-cyber-security-act`
(drift→drift),
`act-zm-2017-022-appropriation`
(match→match),
`act-zm-1963-027-law-reform-frustrated-contracts-act-1963`
(drift→drift),
`judgment-zm-2021-zmcc-17-...`
(drift→drift),
`act-zm-1997-013-appropriation-act-1997`
(drift→drift).

The two re-sampled HTML-URL drift records yielded **identical
fetched_sha256 values across both ticks** (b0538 and b0545) — i.e. the
ZambiaLII CMS produced byte-identical HTML on the two visits ~16 hours
apart, but those bytes still differ from the stored `source_hash`
captured on the original ingest day. This narrows the drift signal:
the ZambiaLII drift is not random per-fetch jitter; it is a one-shot
permanent shift between original-ingest-day rendering and current
rendering. Normalised-text comparison would still be the correct fix.

The matching PDF (`act-zm-2017-022-appropriation` —
parliament.gov.zm static PDF) returned the same sha256 in both ticks
(`823d530e94...225b`), confirming that static binary endpoints are
byte-stable.

## Integrity check

Phase-8-scope checks (per BRIEF.md §"Phase 8 — Nightly re-verification"):

- ✅ No records mutated (script writes nothing under `records/`;
  verified: `find records -newer scripts/batch_0545_phase8_reverify.py`
  returned 0).
- ✅ Sample is deterministic given the seed AND the pool snapshot
  (re-runnable from the same git revision).
- ✅ Every fetch result has both `stored_sha256` (from disk) and
  `fetched_sha256` (newly computed). All 8 fetches returned status 200;
  the only verdicts are `match` or `drift`. Zero `fetch_error`.
- ✅ Drift entries appended to `gaps.md` (one row per drift in the
  triage table; sub-kind `content_changed_full_drift`).
- ✅ approvals.yaml NOT modified (`git diff approvals.yaml` empty).
  Phase 8 has not reached completion criteria; only a human flips
  `complete: true`.
- ✅ Rate limits honoured: zambialii.org @ 5s gap, www.parliament.gov.zm
  @ 2s gap (per `RATE_LIMITS` in script). Wall-clock ~41s for 8 fetches
  is consistent with the rate-limit floor for this host mix.

## Provenance

| Field | Value |
|-------|-------|
| User-Agent | `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` |
| Fetcher | `scripts/batch_0545_phase8_reverify.py` (clone of frozen baseline `scripts/batch_0533_phase8_reverify.py`; only `BATCH` and `WORKSPACE` constants changed from b0538 clone). |
| Robots | All hosts in sample sets (`zambialii.org`, `www.parliament.gov.zm`) permit `User-Agent: *` for the queried paths (re-verified vs. b0538). |

## Budget impact

- Fetches: 8 (cumulative_today before tick: 0/2000; well under cap).
- Tokens: minimal (HTTP I/O only; no LLM invocations during the script).

## Next-tick recommendation

- **Next tick (post-UTC-midnight, 2026-05-09 UTC):** the deterministic
  seed will roll over to `phase8-reverify-2026-05-09` and draw a fresh
  independent 8-record sample from the (slightly grown) pool. No code
  changes anticipated.
- **Phase 8 completion criterion:** undefined in `approvals.yaml`
  (`complete: true` flip is human-only). The phase is by design
  open-ended: it samples 1%/night indefinitely. No worker action will
  flip `complete`.
- **Open recommendation (informational, human action required):** with
  24/24 HTML-URL drifts now reproduced across four consecutive ticks
  and the cross-tick re-sample showing the ZambiaLII drift is a
  one-shot permanent shift (not per-fetch jitter), the case for a
  normalised-text comparison stage on ZambiaLII HTML URLs is now
  materially complete. Raw-bytes comparison continues to produce one
  drift signal per CMS-rendered URL per tick; that signal remains
  uninformative without text normalisation. (No worker action
  required — flagged for Peter.)
