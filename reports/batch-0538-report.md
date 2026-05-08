# Batch 0538 — Phase 8 Nightly Re-verification (2026-05-08)

## Summary

Third Phase 8 tick. Deterministic sample of 8 records (1% of pool=1849,
capped by MAX_BATCH_SIZE=8) re-fetched from their canonical
`source_url`s; recomputed sha256 compared against stored `source_hash`.
**No records mutated** — Phase 8 is read-only on the corpus and only
appends drift findings to `gaps.md` for human triage.

| Field | Value |
|-------|-------|
| Phase | `phase_8_nightly_reverify` |
| Batch | `0538` |
| Parser/fetcher version | `phase8-reverify-0.1.0` |
| Seed | `phase8-reverify-2026-05-08` |
| Pool size | 1849 |
| Sample size | 8 |
| Match | 2 |
| Drift | 6 |
| Fetch error | 0 |
| Fetches issued | 8 |
| Started | 2026-05-08T07:18:16Z |
| Completed | 2026-05-08T07:18:52Z |
| Wall-clock | ~36s |

## Per-record verdicts

| Record id | Verdict | Status |
|-----------|---------|-------:|
| `si-zm-2017-028-dambwa-local-forest-no-f22-alteration-of-boundaries-order-2017` | drift | 200 |
| `act-zm-1989-001-zambia-centre-for-accountancy-studies-act-1989` | drift | 200 |
| `act-zm-2025-003-cyber-security-act` | drift | 200 |
| `si-zm-2020-027-income-tax-remission-ndola-lime-company-limited-order-2020` | match | 200 |
| `act-zm-2017-022-appropriation` | match | 200 |
| `act-zm-1963-027-law-reform-frustrated-contracts-act-1963` | drift | 200 |
| `judgment-zm-2021-zmcc-17-anderson-mwale-buchisa-mwalongo-and-kola-odubote-v` | drift | 200 |
| `act-zm-1997-013-appropriation-act-1997` | drift | 200 |

Full per-fetch JSON: [`reports/batch-0538-reverify.json`](batch-0538-reverify.json).
Drift triage entries: see `gaps.md` § "Phase 8 — Nightly re-verification, batch 0538 (2026-05-08)".

## Pattern observation (cross-tick, three-tick reproduction)

All 6 drifts target ZambiaLII `/akn/...` HTML rendering URLs (acts, an
SI, and — first observed this tick — a judgment URL `/akn/zm/judgment/zmcc/2021/17/eng@2021-09-20`).
Both matches are stable PDF endpoints (one parliament.gov.zm PDF, one
media.zambialii.org `/source_file/` PDF). The pattern from b0524 +
b0533 is now reproduced for a third consecutive tick:

| Tick | ZambiaLII-HTML drifts | Stable-PDF matches |
|------|-----------------------|--------------------|
| b0524 (2026-05-06) | 4/4 | 4/4 |
| b0533 (2026-05-07) | 7/7 | 1/1 |
| b0538 (2026-05-08) | 6/6 | 2/2 |
| **Cumulative**     | **17/17 HTML-URL drifts** | **7/7 PDF-URL matches** |

The first observed HTML-URL drift on a `/akn/zm/judgment/...` URL this
tick (`judgment-zm-2021-zmcc-17`) extends the pattern from acts/SIs to
judgments, suggesting the dynamic-markup root cause is uniform across
the ZambiaLII CMS — not specific to legislation pages. The b0524 /
b0533 recommendation therefore continues to apply (and now applies more
broadly): a normalised-text comparison stage would let the Phase-8
verdict for ZambiaLII HTML URLs switch from `drift` to
`html_byte_drift_normalised_text_pending`. Until then, drifts of
sub-kind `content_changed_full_drift` on `/akn/...` HTML URLs are
informational only.

## Integrity check

Phase-8-scope checks (per BRIEF.md §"Phase 8 — Nightly re-verification"):

- ✅ No records mutated (script writes nothing under `records/`;
  verified: `find records -newer scripts/batch_0538_phase8_reverify.py`
  returned 0).
- ✅ Sample is deterministic (re-runnable; same UTC date → same
  sample via `random.Random("phase8-reverify-2026-05-08")`).
- ✅ Every fetch result has both `stored_sha256` (from disk) and
  `fetched_sha256` (newly computed). All 8 fetches returned status 200;
  the only verdicts are `match` or `drift`. Zero `fetch_error`.
- ✅ Drift entries appended to `gaps.md` (one row per drift in the
  triage table; sub-kind `content_changed_full_drift`).
- ✅ approvals.yaml NOT modified (`git diff approvals.yaml` empty).
  Phase 8 has not reached completion criteria; only a human flips
  `complete: true`.
- ✅ Rate limits honoured: zambialii.org @ 5s gap, www.parliament.gov.zm
  @ 2s gap, media.zambialii.org @ 5s gap (per
  `RATE_LIMITS` in script). Wall-clock ~36s for 8 fetches is consistent
  with the rate-limit floor for this host mix.

## Provenance

| Field | Value |
|-------|-------|
| User-Agent | `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` |
| Fetcher | `scripts/batch_0538_phase8_reverify.py` (clone of frozen baseline `scripts/batch_0533_phase8_reverify.py`; only `BATCH` and `WORKSPACE` constants changed). |
| Robots | All hosts in sample sets (`zambialii.org`, `www.parliament.gov.zm`, `media.zambialii.org`) permit `User-Agent: *` for the queried paths (re-verified vs. b0533). |

## Budget impact

- Fetches: 8 (cumulative_today before tick: 0/2000; well under cap).
- Tokens: minimal (HTTP I/O only; no LLM invocations during the script).

## Next-tick recommendation

- **2026-05-09 UTC:** the next deterministic seed
  `phase8-reverify-2026-05-09` will draw a fresh independent sample of
  8 records from the same (slightly grown) pool. No code changes
  anticipated.
- **Phase 8 completion criterion:** undefined in `approvals.yaml`
  (`complete: true` flip is human-only). The phase is by design
  open-ended: it samples 1%/night indefinitely. No worker action will
  flip `complete`.
- **Open recommendation (informational, human action required):** with
  17/17 HTML-URL drifts now reproduced across three consecutive ticks,
  and the first judgment-URL drift now observed, the case for a
  normalised-text comparison stage on ZambiaLII HTML URLs is materially
  stronger. Raw-bytes comparison continues to produce one drift signal
  per CMS-rendered URL per tick; that signal is uninformative without
  text normalisation. (No worker action required — flagged for Peter.)
