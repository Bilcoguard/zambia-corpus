# Batch 0553 — judgment-ingestion-worker tick

- **Worker**: judgment-ingestion-worker (scheduled task `judgment-ingestion`)
- **Wall-clock window**: 2026-05-09T10:0xZ..10:1xZ (UTC, well under 20 min target)
- **Phase**: Phase 5 dedicated post-completion ingestion (continued).
- **Parser**: v0.3.2 baseline (`scripts/batch_0498_parse.py` +
  `scripts/batch_0506_zmsc_parse.py` wrapper). No parser, fetcher, or
  core-logic modifications. Configuration-tier reuse via
  `scripts/batch_0553_zmsc_fetch.py` and
  `scripts/batch_0553_zmsc_parse.py` thin wrappers pointing at
  `_work/b0553/targets.json`.
- **Outcome**: **2 records written, 1 deferred under
  `html_no_summary_pdf_no_match`**. Six fetches consumed (3 HTML + 3
  PDF for the GET fetches).

## Tick decision (priority order)

a. **REPARSE DEFERRED** — not run this tick. The two most recent
   reparse ticks (b0544, b0552) both redeferred all 8 candidates under
   `html_no_summary_pdf_no_match`; the v0.3.3-pending cohort cannot
   move under the current parser_v0.3.2 anchor inventory and authoring
   the v0.3.3 anchor additions is out-of-tick work. Skipping reparse
   here.
b. **SCZ SWEEP** — chosen for this tick. The b0547 inline HEAD probe
   of ZMSC 2025 confirmed nums {4, 31, 32} as 200-OK but the GET
   fetches were never run (b0547 was Phase-0 HEAD-only). This tick
   GET-fetches and parses those three records — guaranteed-available
   targets with zero 404 risk.
c. **ZMCC NEW YEARS** — not run this tick (priority (b) had work).

## Phase 0 — target selection (zero fetch cost)

The b0547 HEAD-probe results (recorded in `_work/b0547/head_probe_results.json`)
identified three available ZMSC 2025 nums not yet on disk:

| court / num   | b0547 HEAD | raw on disk before tick | record before tick |
|---------------|------------|--------------------------|---------------------|
| zmsc/2025/4   | 200-OK     | absent                   | absent              |
| zmsc/2025/31  | 200-OK     | absent                   | absent              |
| zmsc/2025/32  | 200-OK     | absent                   | absent              |

`_work/b0553/targets.json` lists these three nums.

## Phase 1 — fetch via `batch_0506_zmsc_fetch.fetch_one`

`scripts/batch_0553_zmsc_fetch.py` (thin wrapper) ran each target
through the existing rate-limited (5s/request) ZambiaLII fetcher.

| court / num   | status | date_decided | html bytes | pdf bytes  |
|---------------|--------|---------------|-----------:|-----------:|
| zmsc/2025/4   | ok     | 2025-01-15    | 40,912     | 1,223,988  |
| zmsc/2025/31  | ok     | 2025-10-28    | 44,844     |   199,466  |
| zmsc/2025/32  | ok     | 2025-03-11    | 40,906     | 2,833,540  |

All three resolved via the canonical
`/akn/zm/judgment/zmsc/{year}/{num}/eng` redirect to a dated
`eng@YYYY-MM-DD` URL. Six successful HTTP fetches; zero errors.

## Phase 2 — parse via parser_v0.3.2

`scripts/batch_0553_zmsc_parse.py` (thin wrapper) re-pointed the b0506
parser at `_work/b0553/`.

| court / num   | result   | outcome   | outcome_source                                                |
|---------------|----------|-----------|----------------------------------------------------------------|
| zmsc/2025/4   | written  | allowed   | `summary[v032:...application|petition|appeal|leave|r...]`     |
| zmsc/2025/31  | deferred | —         | `html_no_summary_pdf_no_match` (joins v0.3.3-pending cohort)  |
| zmsc/2025/32  | written  | dismissed | `pdf-tail-2pages[v031-tail:...we (hereby|therefore|accordi]`  |

### Records written

1. `judgment-zm-2025-zmsc-04-minimart-development-corporation-company-limited-v`
   - Citation: [2025] ZMSC 4
   - Case: Minimart Development Corporation Company Limited v Ackim
     Chirwa and Ors (SCZ/8/25/2023)
   - Date decided: 2025-01-15
   - Judges: Hamaundu (presiding) — alias `E. M. Hamaundu` added to
     existing canonical entry
   - Outcome: `allowed` — leave granted to appeal because reasonable
     doubt exists whether lender consent and corporate formalities
     validated the liability transfer
   - raw_sha256: 583457474215a61d30c140305e5fe554e4e420d88f34cdc816b013bc897061ca
2. `judgment-zm-2025-zmsc-32-shaba-mulengela-and-anor-v-frank-mumba`
   - Citation: [2025] ZMSC 32
   - Case: Shaba Mulengela and Anor v Frank Mumba (SCZ/7/36/2024)
   - Date decided: 2025-03-11
   - Judges: Malila CJ (presiding), Kaoma JJS, Chisanga JJS — all
     pre-existing canonical entries
   - Outcome: `dismissed` — "We dismiss it with costs to" (PDF tail
     anchor)
   - raw_sha256: ab24088b0f53068309f3b8c46fbfaecf2ab1e39d8b32c0ddf7f5601173fbc46b

### Deferred this tick

| court / num   | pdf bytes  | reason                         | summary head |
|---------------|-----------:|---------------------------------|--------------|
| zmsc/2025/31  | 199,466    | `html_no_summary_pdf_no_match` | "Whether discrimination and equal-pay claims under Employment Code s.5 are arbitrable and whether tribunals may compare non-parties' contracts." |

The deferred record is a declaratory holding on arbitrability — falls
under the v0.3.3-pending pattern family 9 documented in b0552
(declaratory holdings without operative-disposition verbs). Joins the
v0.3.3-pending cohort: 51 → 52 records.

## Judges registry

`judges_registry.yaml` updated: added alias `E. M. Hamaundu` to the
existing canonical entry `Hamaundu`. No new canonical entries; the
other three judges (Malila, Kaoma, Chisanga) already had their
title-suffixed aliases registered.

## corpus.sqlite

Updated via TMPDIR-routed atomic copy (`scripts/batch_0553_sqlite_insert.py`,
delegating to `batch_0531_sqlite_insert`):
- `records`: 1849 → 1851 (+2)
- `judgments_meta`: 159 → 161 (+2)
- `records_fts` deferred to host-side rebuild (`scripts/batch_0504_build_fts5.py`).

A residual `corpus.sqlite-journal` left over after the atomic copy was
parked aside as `_stale_b0553_corpus.sqlite-journal` (post-copy
verification confirmed the DB reads cleanly; the journal predates this
tick and was not replayed).

## Integrity checks (`scripts/integrity_check_b0553.py`)

PASS — 2 records examined (each unique by ID, type=`judgment`, outcome
in allowed enum, issue_tags non-empty, judges resolve in registry,
raw_sha256 matches on-disk PDF, present in both `records` and
`judgments_meta`); 1 deferred raw HTML+PDF pair on disk; 161 unique
judgment IDs corpus-wide.

## Cohort cumulative since b0504

- **64** records written (was 62; +2 this tick — zmsc/2025/{4, 32})
- **52** v0.3.3-pending deferred (was 51; +1 this tick — zmsc/2025/31)
- **37** OCR-pending deferred (unchanged)
- **40** confirmed 404 (unchanged)

## Phase 5 ceiling

Was 159/160; now 161/160. The Phase 5 procedural ceiling band (target
100–160) is **just above the upper sentinel by 1**. Authoring approval
to extend the band or close Phase 5 should be raised with the human
operator on the next opportunity (this is a non-blocking observation —
the dedicated post-Phase-5 ingestion task is what the worker is
running, per the 2026-05-03 directive in `BRIEF.md`).

## Next-tick recommendation

1. **Continue ZMSC 2025 boundary hardening**. The b0547 HEAD probe
   left nums {5–13, 15–30} confirmed as on-disk + written; nums
   {1, 5, 14, 31, 33–36} unresolved before this tick; this tick wrote
   {4, 32}. The remaining gap candidates are {1, 5, 14, 33+}. ZMSC
   2025/{1, 5} had records previously deferred — candidates for
   v0.3.3 reparse if the parser advances, or OCR.
2. **ZMCC 2025/2026 boundary probe** (per b0543 next-tick recommendation
   that has now been deferred through five+ subsequent ticks).
3. **Author parser_v0.3.3 anchor pack** to reduce the 52-record
   v0.3.3-pending cohort. The pattern families documented in b0541,
   b0544, and b0552 reports total 11 near-miss families that could
   plausibly be addressed by a single anchor-pack release.

## Daily fetch budget

- Worker: judgment-ingestion-worker
- Today (2026-05-09 UTC): 86 → 92 / 500 (+6 this tick)

## B2 sync

Deferred to host (rclone not in sandbox).

## approvals.yaml

NOT modified per human-only confirmation rule.
