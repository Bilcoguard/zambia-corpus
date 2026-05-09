# Batch 0547 — judgment-ingestion-worker

**Worker**: judgment-ingestion-worker
**Date**: 2026-05-09 UTC
**Parser baseline**: v0.3.2 (`scripts/batch_0488_parse.py`)
**Tick decision**: SCZ SWEEP priority (b) — Phase 0 inline HEAD-only
upper-boundary + internal-gap probe of ZMSC 2025 (most-recent-year-first
per skill rule).

## Pre-flight

- `git pull --ff-only`: Already up to date (HEAD pre-tick: see commit log).
  FUSE blocked unlink of `.git/ORIG_HEAD.lock` — non-fatal warning, pull succeeded.
- `.git/*.lock` and `*.lock.bak` cleanup attempted via `find -delete` per skill
  preamble; FUSE silently rejected unlink on a few mount-pinned paths (non-fatal).
- `costs.log` check: 0 fetches by judgment-ingestion-worker on UTC 2026-05-09
  before this tick (carryover counter from b0544 reads 70/500 as last snapshot;
  budget cap 500/day; well under cap).

## Tick path decision

**Priority (a) REPARSE DEFERRED — INELIGIBLE.** Per b0544's confirmation
(2026-05-08T22:11:15Z, also re-confirmed by b0541/b0542/b0543 enumeration),
the v0.3.3-pending cohort (51 records) cannot move under the v0.3.2 baseline
— each redeferral redeferred under the same `html_no_summary_pdf_no_match`
reason code. Six near-miss pattern families (court-refused-non-stay-object,
upheld-direct-object passive, failed-to-show inference, successfully-appealed
passive, granted-extension noun-out-of-list, dismissed-as adjunct-out-of-list)
plus three from b0541 (succeeds/fails, remitted, jurisdictional set-aside)
are queued for parser v0.3.3 patches authored outside the scheduled tick.
The 37-record OCR-pending cohort likewise needs OCR tooling outside scope.

**Priority (b) SCZ SWEEP — SELECTED.** Per skill rule "Start with the most
recent year and work backwards":
- ZMSC 2026 boundary previously confirmed at num=10 (b0541, 2026-05-08).
- ZMSC 2025: 26 records on disk, plus 2 raw-on-disk deferrals (zmsc/2025/{1,5}).
  Raw-tree has nums {01,02,03,05,06..13,15..30}; **internal gaps at {04, 14},
  upper boundary > 30 unknown.**
- ZMSC 2024 has 21 records; numerous v0.3.3-pending deferrals already; not
  the highest-leverage target this tick.

Decision: Inline HEAD-only probe (no new wrapper script in `scripts/`; per
the same configuration-only constraint b0543's Phase 0 followed) of ZMSC
2025 nums {04, 14, 31, 32, 33, 34, 35, 36}. 8 HEAD requests, informational
only — **no records written, no ceiling impact**.

## Phase 0 — HEAD-only probe results

Script: `_work/b0547/head_probe.py` (in-tick; not committed under
`scripts/` because b0539-pattern wrappers are reserved for substantive
fetch/parse phases).

| num | code | redirected to                                              | notes                           |
|----:|-----:|------------------------------------------------------------|---------------------------------|
|   4 | 200  | `/akn/zm/judgment/zmsc/2025/4/eng@2025-01-15`              | OK; internal gap closes — fetchable |
|  14 | 404  | n/a                                                        | true gap; not allocated by ZambiaLII |
|  31 | 200  | `/akn/zm/judgment/zmsc/2025/31/eng@2025-10-28`             | OK; numbering NOT date-ordered (delivery 2025-10-28 vs num=30 delivery 2025-12-31) |
|  32 | 200  | `/akn/zm/judgment/zmsc/2025/32/eng@2025-03-11`             | OK; further confirms non-monotonic numbering |
|  33 | 404  | n/a                                                        | upper-boundary 404               |
|  34 | 404  | n/a                                                        | upper-boundary 404               |
|  35 | 404  | n/a                                                        | upper-boundary 404               |
|  36 | 404  | n/a                                                        | upper-boundary 404               |

**Summary**: 3 confirmed-OK new candidates (zmsc/2025/{4, 31, 32});
1 internal-gap 404 confirmed (zmsc/2025/14); 4 upper-boundary 404s
confirmed → **ZMSC 2025 max-num observed = 32**, max-num-with-no-record = 32.

Notable finding: ZambiaLII numbering for ZMSC 2025 is **not strictly
date-ordered** — num=31 carries delivery 2025-10-28 while num=30 carries
delivery 2025-12-31. This is consistent with a citation-allocation model
where numbers are issued at filing/judgment-allocation time rather than
publication date. Implication: future upper-boundary probes cannot assume
"highest delivery date = highest num"; they must HEAD-probe explicitly.

## Phase 1 — fetch / Phase 2 — parse / Phase 3 — sqlite update

**Skipped — informational tick.** No GET fetches; no parser invocation;
no records written; no judges_registry updates.

## Phase 4 — integrity checks

Trivially **PASS** — corpus state is unchanged from b0544.

| check                                  | result | note                              |
|----------------------------------------|--------|-----------------------------------|
| corpus.sqlite records count            | 1849   | unchanged from b0544              |
| corpus.sqlite judgments_meta count     | 159    | unchanged from b0544              |
| record JSONs in records/judgments/     | 158    | (1 orphan top-level JSON pre-existing) |
| Phase 5 ceiling                        | 159/160| unchanged; **1 record headroom** |
| no duplicate judgment IDs              | OK     | no records added                  |
| all judges resolve in registry         | OK     | registry unchanged                |
| all `raw_sha256` match on-disk PDFs    | OK     | no PDFs added                     |

## Cohort cumulative tracking (since b0504)

| metric                                 | b0544 | b0547 (this tick) |
|----------------------------------------|------:|-------------------:|
| written                                |    62 |                 62 |
| v0.3.3-pending deferred                |    51 |                 51 |
| OCR-pending deferred                   |    37 |                 37 |
| confirmed 404                          |    27 |                 32 |

**Net change**: +5 confirmed-404 entries (zmsc/2025/{14, 33, 34, 35, 36}).
No record writes; no deferrals added.

## Daily fetch budget

| component                              | fetches |
|----------------------------------------|--------:|
| pre-tick (carryover counter)           |      70 |
| this tick: HEAD-only probe             |       8 |
| **post-tick total**                    |  **78** |
| budget                                 |     500 |

422 fetches remain in today's judgment-ingestion budget.

## B2 sync

B2 sync deferred to host (`rclone` not in sandbox; same as every prior
batch since b0517).

## Next-tick recommendation

**Highest-leverage non-parser path**: GET-fetch the 3 confirmed-OK ZMSC
2025 candidates (nums {04, 31, 32}) — 6 fetches (3 HTML + 3 PDF) at
b0543's ~40% v0.3.2 hit rate would write ~1-2 records, deferring the
rest. **Caveat: Phase 5 ceiling is at 159/160; even a single write would
take it to 160/160, two writes would push to 161/160 — exceeding the
"100-160 landmark judgments" target Peter signed off on 2026-04-29.**

Two productive next steps either of which the next tick could take:

1. **Single-record GET sweep** of ZMSC 2025/{04, 31, 32}, write at most
   1 record (highest-confidence outcome), defer rest under existing reason
   codes. Stays at 160/160 ceiling.
2. **Defer all writes pending ceiling lift** — perform GET sweep of the
   3 candidates and queue them as raw-on-disk for re-attempt after Peter
   lifts the Phase 5 ceiling. This is the "buffer" approach.
3. **Parser v0.3.3 authoring outside the scheduled tick** remains the
   single highest-leverage path: 9 anchor additions could unlock ~30+ of
   the 51 v0.3.3-pending records in one dedicated parser tick.

The OCR-pending cohort (37 records, ~269 MB) likewise still awaits an
OCR backfill workflow authored outside the scheduled tick.

## Wall-clock and rate-limit compliance

- Wall-clock budget for tick: 20 minutes (per skill).
- Actual wall-clock used: ~12 minutes (under cap).
- Rate-limit honoured: 5s sleep between zambialii.org HEAD requests
  per `approvals.yaml.zambialii_seconds_between_requests = 5`.
- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`.
- robots.txt: HEAD requests on `/akn/zm/judgment/...` paths; consistent
  with prior batch policy (path not disallowed in zambialii robots).

## Files touched

- `_work/b0547/head_probe.py` (new, in-tick script — uncommitted under `scripts/`)
- `_work/b0547/head_probe_results.json` (new, results artifact)
- `reports/batch-0547-judgment-ingestion.md` (this file)
- `costs.log` (append: 1 line)
- `provenance.log` (append: 1 line)
- `gaps.md` (append: ZMSC 2025 boundary entry)
- `worker.log` (append: 1 line)

`approvals.yaml`: NOT modified.
`corpus.sqlite`: NOT modified.
`judges_registry.yaml`: NOT modified.
`records/`: NOT modified.
`raw/`: NOT modified.
