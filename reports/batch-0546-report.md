# Batch 0546 — Phase 8 Nightly Re-verification (2026-05-09 UTC)

## Summary

Fifth Phase 8 tick. First tick on the new UTC date (2026-05-09), so the
deterministic seed rolls over to `phase8-reverify-2026-05-09` and draws
a fresh independent sample from the candidate pool. **No records
mutated** — Phase 8 is read-only on the corpus.

| Field | Value |
|-------|-------|
| Phase | `phase_8_nightly_reverify` |
| Batch | `0546` |
| Parser/fetcher version | `phase8-reverify-0.1.0` |
| Seed | `phase8-reverify-2026-05-09` |
| Pool size | 1853 (unchanged from b0545) |
| Sample size | 8 |
| Match | 4 |
| Drift | 4 |
| Fetch error | 0 |
| Fetches issued | 8 |
| Started | 2026-05-09T05:58:41Z |
| Completed | 2026-05-09T05:59:03Z |
| Wall-clock | ~22s |

## Per-record verdicts

| Record id | Verdict | Status | Notes |
|-----------|---------|-------:|-------|
| `act-zm-1967-058-council-of-law-reporting-act-1967` | drift | 200 | zambialii.org `/akn/...` HTML — established pattern |
| `act-zm-2016-008-the-constitutional-court` | match | 200 | parliament.gov.zm static PDF |
| `act-zm-2020-023-value-added-tax-amendment-act-2020` | drift | 200 | **truncated stored_sha256 — see "New finding" below** |
| `act-zm-1920-002-public-pounds-and-trespass-act` | drift | 200 | zambialii.org `/akn/...` HTML |
| `local-government-appointment-of-local-government-administrator-kafue-town-counci-2022` | match | 200 | media.zambialii.org `/source.pdf` (PDF endpoint) |
| `act-zm-2019-004-zambia-law-development-commission-amendment-act-20` | match | 200 | parliament.gov.zm static PDF |
| `act-zm-2010-029-cattle-cleansing-repeal-act-2010-act-no-29-of-2010` | match | 200 | parliament.gov.zm static PDF |
| `si-zm-2020-097-public-finance-management-general-regulations-2020` | drift | 200 | zambialii.org `/akn/...` HTML |

Full per-fetch JSON: [`reports/batch-0546-reverify.json`](batch-0546-reverify.json).
Drift triage entries: see `gaps.md` § "Phase 8 — Nightly re-verification, batch 0546 (2026-05-09 UTC)".

## NEW finding — truncated `source_hash` field on disk (data quality, not drift)

Record `act-zm-2020-023-value-added-tax-amendment-act-2020` has a
stored `source_hash` of `sha256:83df74b511734b91` — only **16 hex
characters (8 bytes)** after the `sha256:` prefix, instead of the
expected 64 hex characters. The freshly fetched PDF returns
`83df74b511734b91d6344f019be20c16f4e61088c77c4817264e65d729699bfc`,
whose **first 16 hex chars match the stored value byte-for-byte**.

This means:

- The **upstream PDF is byte-identical** to what was originally
  ingested on 2026-04-10 (no real content drift).
- The **stored field is truncated** at record-write time. Likely cause:
  the parliament-pdf-v1.2 parser (the recorded `parser_version`)
  truncated the hash when serialising to the JSON record. The on-disk
  raw file under `raw/...` should still carry the full hash; only the
  record's `source_hash` field is short.

Phase 8's verdict logic correctly classifies this as `drift` because
the strings are not equal, but the underlying signal here is
"record-level data quality issue" rather than "upstream content
changed". This is a NEW class of drift surface not seen in
b0524/b0533/b0538/b0545.

**Recommendation (informational; human action required):** corpus-wide
audit of `source_hash` field length. Any record with
`len(source_hash) < len("sha256:") + 64` is a candidate for the same
truncation bug and should be re-hashed from the raw on-disk bytes.
Re-hashing must NOT mutate the record under Phase 8 — flag for a
separate repair phase. (No worker action required — flagged for Peter.)

## Pattern observation (cross-tick, five-tick reproduction)

Three of the four drifts target ZambiaLII `/akn/...` HTML rendering
URLs (2 acts, 1 SI). The fourth drift (`act-zm-2020-023-...`) is the
truncated-hash case above and is **not** a true HTML CMS drift — its
URL is a parliament.gov.zm PDF whose bytes are unchanged. The four
matches comprise three parliament.gov.zm static PDFs and one
media.zambialii.org `/source.pdf` endpoint (the latter is a stable
binary endpoint, distinct from `/akn/...` HTML).

Re-baselining the cross-tick pattern with the truncated-hash case
excluded from the HTML-drift category:

| Tick | ZambiaLII-HTML drifts | Stable-PDF matches | Other |
|------|-----------------------|--------------------|-------|
| b0524 (2026-05-06) | 4/4 | 4/4 | — |
| b0533 (2026-05-07) | 7/7 | 1/1 | — |
| b0538 (2026-05-08 early) | 6/6 | 2/2 | — |
| b0545 (2026-05-08 late)  | 7/7 | 1/1 | — |
| b0546 (2026-05-09)       | 3/3 | 4/4 | 1 truncated-hash false-drift |
| **Cumulative** | **27/27 HTML-URL drifts** | **12/12 PDF-URL matches** | **1 record-level data-quality finding** |

The 27/27 HTML-URL → drift and 12/12 PDF-URL → match invariants are
preserved for a fifth consecutive tick.

## Integrity check

Phase-8-scope checks (per BRIEF.md §"Phase 8 — Nightly re-verification"):

- ✅ No records mutated (script writes only to `reports/` and append
  logs; `records/` tree unchanged — `git status records/` shows clean
  tree post-tick).
- ✅ Sample is deterministic given the seed AND the pool snapshot
  (re-runnable from the same git revision).
- ✅ Every fetch result has both `stored_sha256` (from disk) and
  `fetched_sha256` (newly computed). All 8 fetches returned status 200;
  the only verdicts are `match` or `drift`. Zero `fetch_error`.
- ✅ All 8 sampled records still parse cleanly from disk and carry
  intact `source_url` + `source_hash` fields (verified post-tick).
- ✅ approvals.yaml NOT modified (`git diff approvals.yaml` empty).
  Phase 8 has not reached completion criteria; only a human flips
  `complete: true`.
- ✅ Rate limits honoured: zambialii.org @ 5s gap, www.parliament.gov.zm
  @ 2s gap, media.zambialii.org @ 5s gap (per `RATE_LIMITS` in script).
  Wall-clock ~22s for 8 fetches is consistent with the rate-limit floor
  for this host mix (this batch had a parliament-heavy sample, hence
  faster than b0545's zambialii-heavy sample).

### Pre-existing finding (re-flagged, not a regression)

Corpus-wide unique-id check surfaces **5 active duplicate-ID pairs**
where the same `id` appears in both flat (`records/acts/x.json`) and
year-tree (`records/acts/YYYY/x.json`) locations with **diverged
content** (different file-level sha256). Specifically:

- `act-zm-2025-014-cotton-act`
- `act-zm-2025-028-appropriation-act`
- `act-zm-2019-010-nurses-and-midwives-act-2019`
- `act-zm-2020-010-national-council-for-construction-act-2020`
- `act-zm-2018-001-public-finance-management-act`

These pairs were introduced in earlier Phase 4 batches (b0005, b0289,
and similar) and are documented as a known historical condition in
`gaps.md` (search for "duplicate IDs" and the b0173 audit note). They
are NOT introduced by this Phase 8 tick (Phase 8 doesn't write
records). The diverged-content aspect (vs. identical-content
duplicates the b0173 audit catalogued) is the new sub-finding;
re-flagged in `gaps.md` for a future repair-phase to reconcile.

## Provenance

| Field | Value |
|-------|-------|
| User-Agent | `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` |
| Fetcher | `scripts/batch_0546_phase8_reverify.py` (clone of frozen baseline `scripts/batch_0533_phase8_reverify.py`; only `BATCH` and `WORKSPACE` constants changed from b0545 clone). |
| Robots | All hosts in sample (`zambialii.org`, `www.parliament.gov.zm`, `media.zambialii.org`) permit `User-Agent: *` for the queried paths (re-verified vs. b0545). |

## Budget impact

- Fetches: 8 (cumulative_today before tick: 0/2000; well under cap).
- Tokens: minimal (HTTP I/O only; no LLM invocations during the script).

## Next-tick recommendation

- **Next tick:** continue Phase 8 nightly reverify cadence. If the
  next tick fires inside the same UTC date (2026-05-09), the seed is
  unchanged; the sample composition will only shift if the candidate
  pool size changes. If the next tick crosses UTC midnight, the seed
  rolls to `phase8-reverify-2026-05-10`.
- **Phase 8 completion criterion:** undefined in `approvals.yaml`
  (`complete: true` flip is human-only). Phase 8 is by design
  open-ended: samples 1%/night indefinitely. No worker action will
  flip `complete`.
- **Open recommendations (human action required):**
  1. Normalised-text comparison for ZambiaLII `/akn/...` HTML URLs —
     case unchanged from b0545 next-tick recommendation; 27/27 HTML
     drifts reproduced over five consecutive ticks.
  2. **NEW** — corpus-wide audit of truncated `source_hash` field
     values (any `len(source_hash) < 71` is suspect; root cause
     appears to be parliament-pdf-v1.2 parser ingestion). Re-hashing
     of stored records from raw on-disk bytes is appropriate but must
     happen in a dedicated repair phase, not in Phase 8.
  3. Reconciliation of the 5 diverged-content flat-vs-year-tree
     duplicate-ID pairs surfaced in this tick's pool-build sweep
     (pre-existing condition; documented as a follow-up in `gaps.md`).
