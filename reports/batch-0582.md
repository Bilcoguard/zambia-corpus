# Batch 0582 — Phase 8 Nightly Re-verification (2026-05-10)

**UTC start:** 2026-05-10T21:04:53Z
**UTC end:** 2026-05-10T21:05:39Z
**Worker:** worker-tick (Phase 8)
**Phase:** phase_8_nightly_reverify (approved 2026-05-06; sample_rate 0.01)
**Parser:** phase8-reverify-0.1.0 (functional contract per scripts/batch_0546_phase8_reverify.py)
**Tick scope:** Twenty-eighth Phase 8 tick overall; fourteenth worker-tick of
   UTC date 2026-05-10 (after b0563 at 05:50Z, b0564 at 06:02:42Z,
   b0565 at 09:09:35Z, b0567 at 10:06:09Z, b0568 at 10:12:41Z, b0569 at
   10:36Z, b0570 at 11:08Z, b0572 at 16:34:30Z, b0575 at 18:46:30Z,
   b0576 at 19:04:49Z, b0578 at 19:35:51Z, b0579 at 20:05:17Z,
   b0581 at 20:34:34Z).
**Execution mode:** inline runner (`/tmp/b0582_phase8_reverify.py`, NOT
   committed) per sandbox-session safety constraint maintained since b0548
   (b0548..b0581 precedent). Functional contract matches
   scripts/batch_0546_phase8_reverify.py baseline including
   scripts/certs/*.pem PKI loader. Differences from baseline: tick-suffixed
   seed `phase8-reverify-2026-05-10-b0582`, plus truncated-stored-hash-prefix
   detection (b0570/b0578/b0581 cohort — recomputed sha256 whose value
   startswith the stored short-prefix is classified
   `match_truncated_prefix` and counted under
   `truncated_stored_hash_false_drift_count`).

## Pre-tick git state observation

Pre-tick `git pull --ff-only` returned `Already up to date` (HEAD=592e75f
from b0581). The regular `.git/index` still carries the staged b0580
judgment-ingestion-worker commit-prep (3 ZMSC 2020 record additions,
3 helper scripts under `scripts/batch_0580_*.py`, plus
`reports/batch-0580-jiw.md` and four log-file modifications) — uncommitted
because the b0580 jiw push line is absent from `worker.log`. This is the
same parallel-channel state observed at b0581 pre-tick; the Phase 8
worker-tick channel does not own it. Per b0579..b0581 alt-index precedent,
this tick commits b0582's intended files via a per-PID alt-index path
(`GIT_INDEX_FILE=/tmp/alt-index-b0582`) reset to HEAD, leaving the regular
index untouched for the jiw next tick to reconcile.

The default `.git/index.lock` cleanup remains constrained on this sandbox
by `Operation not permitted` virtiofs semantics for backup-suffixed lock
files in `.git/`. `git pull --ff-only` succeeded with a single warning
about an unremovable `.git/objects/maintenance.lock` backup file — pull
semantics not affected.

## Inputs

- Pool size: **1870** (unchanged from b0581 close at 1870 — no jiw record
  additions visible to the Phase 8 loader between b0581 and b0582).
- Seed: `phase8-reverify-2026-05-10-b0582` (tick-suffixed deterministic seed).
- Sample size: **8** (= MAX_BATCH cap; ceil(0.01 × 1870) = 19 → capped at 8).
- Out-of-band re-fetches: **none**.

## Results — 1 match / 7 drift / 0 truncated_prefix / 0 fetch_error

| Verdict      | Count | Records |
|--------------|------:|---------|
| match        |     1 | si-zm-2015-070-income-tax-double-taxation-relief-taxes-on-income-ireland-order-2015 (zambialii akn /source.pdf 159,089 B — extends Act/SI `/source.pdf` stable-PDF cohort to 18/18 across 28 Phase 8 ticks) |
| drift        |     7 | act-zm-1970-018-investment-disputes-convention-act-1970 (zambialii.org/akn/zm/act/1970/18/eng@1996-12-31 213,526 B — fits AKN-HTML drift cohort; **earliest-year Act drift since b0567 act-zm-1930-028 set the 1930 floor — 1970-vintage drift confirms drift mechanism is independent of original enactment year**); act-zm-2004-005-excess-expenditure-appropriation-2000-act (zambialii.org/akn/zm/act/2004/5/eng@2004-04-20 38,805 B — fits AKN-HTML drift cohort); si-zm-2023-009-urban-and-regional-planning-designated-local-planning-authority-regulations-2023 (zambialii.org/akn/zm/act/si/2023/9 39,339 B — **third bare-AKN-path drift observation** in 28-tick series after b0579 si-zm-2023-041 and b0581 si-zm-2019-014); judgment-zm-2022-zmcc-28-kolala-v-zambia-postal-services-corporation (zambialii.org/akn/zm/judgment/zmcc/2022/28/eng@2022-01-26 48,529 B — fits judgment-akn HTML drift cohort); judgment-zm-2023-zmcc-19-tresford-mubanga-v-zesco-limited (zambialii.org/akn/zm/judgment/zmcc/2023/19/eng@2023-10-26 45,770 B — fits judgment-akn HTML drift cohort); judgment-zm-2025-zmsc-07-star-drilling-and-exploration-limited-v-national-t (zambialii.org/akn/zm/judgment/zmsc/2025/7/eng@2025-02-21 44,153 B — **first ZMSC judgment-akn /eng@ HTML drift observation** — extends judgment-akn drift coverage from ZMCC-only to ZMCC+ZMSC); act-zm-2006-002-excess-expenditure-appropriation-2003-act (zambialii.org/akn/zm/act/2006/2/eng@2006-03-31 39,913 B — fits AKN-HTML drift cohort) |
| match_truncated_prefix | 0 | — (no parliament.gov.zm `/acts/` 2020-vintage records in sample this tick) |
| fetch_error  |     0 | — |

## Cohort-level cumulative tally (post-b0582, 28 ticks)

| Cohort                                                              | Pre-b0582 | Δ b0582 | Post-b0582 |
|---------------------------------------------------------------------|----------:|--------:|-----------:|
| zambialii.org/akn/.../act-or-SI-HTML drift                          |     86/86 |   +4/+4 |      90/90 |
| zambialii.org/akn/.../source.pdf match (Acts/SIs)                   |     17/17 |   +1/+1 |      18/18 |
| zambialii.org/akn/.../source.pdf match (Judgments)                  |       1/1 |     0/0 |        1/1 |
| media.zambialii.org/media/legislation/ legacy-PDF match             |       1/1 |     0/0 |        1/1 |
| parliament.gov.zm static PDF match (real-match)                     |     82/82 |     0/0 |      82/82 |
| parliament.gov.zm static PDF real DRIFT                             |      0/85 |     0/0 |       0/85 |
| parliament.gov.zm static PDF truncated_stored_hash_false_drift      |      3/85 |     0/0 |       3/85 |
| zambialii judgment-akn HTML drift                                   |      4/12 |   +3/+3 |       7/15 |
| Parliament-node landing                                             |       0/1 |     0/0 |        0/1 |
| Stable-PDF combined supercohort (parliament + zambialii akn /source.pdf + media.zambialii legacy) — real-drift basis | 100/103 | +1/+1 | 101/104 § |

§ Stable-PDF supercohort now 101/104 across 28 ticks. The 3 cumulative
  non-real-matches remain the same three truncated-stored-hash false
  drifts (b0570 act-zm-2020-011; b0578 act-zm-2020-019; b0581 act-zm-2020-016).
  **Real drift count on the stable-PDF supercohort remains zero across 28
  ticks.**

## Notable observations (b0582)

1. **Sample composition was almost entirely AKN-HTML.** Of 8 sampled
   records, only 1 carried the stable `/source.pdf` AKN endpoint
   (si-zm-2015-070); the remaining 7 were AKN-HTML rendering URLs
   (4 act/SI + 3 judgment). All 7 drifted, consistent with the
   28-tick standing finding: AKN HTML rendering bytes are NOT stable
   across requests (dynamic header/footer chrome and metadata
   injection), while the underlying `/source.pdf` cached PDFs ARE
   stable.

2. **Judgment-akn HTML drift cohort widened to ZMSC.** Prior 4
   judgment-akn-HTML drift observations across b0524..b0581 were all
   ZMCC (Constitutional Court) URLs. b0582 adds the first ZMSC
   (Supreme Court) judgment-akn-HTML drift observation
   (judgment-zm-2025-zmsc-07). The drift mechanism is identical
   (akn-HTML rendering pipeline) — the court-specific URL path
   `/judgment/zmsc/...` vs `/judgment/zmcc/...` is incidental to
   the drift cause. Cohort now 7/15.

3. **Bare-AKN-path drift sub-pattern continues to reproduce.** Three
   consecutive Phase 8 ticks (b0579 si-zm-2023-041, b0581 si-zm-2019-014,
   b0582 si-zm-2023-009) have observed drift on the bare-AKN-path
   URL form (no `/eng@<date>` suffix, no `/source.pdf` suffix). All
   three observations are SIs — Acts in the Phase 8 sample pool
   appear to consistently use the `/eng@<date>` form. No operator
   action recommended; this is a URL-form sub-classification rather
   than a new drift class.

4. **Earliest-year Act drift not extended.** The earliest-year Act
   drift observed in the 28-tick series remains b0567's
   act-zm-1930-028-petroleum-act-1930. b0582's earliest Act drift is
   act-zm-1970-018 (1970-vintage enactment, eng@1996-12-31 republication
   date). Confirms drift mechanism is rendering-pipeline-bound rather
   than vintage-bound.

5. **Truncated-stored-hash cohort unchanged this tick.** Sample did
   not include any parliament.gov.zm `/acts/` 2020-vintage Acts
   (where all 3 cumulative truncated-stored-hash false drifts have
   been observed). The b0578/b0579/b0581 standing operator
   recommendation — one-time backfill sweep to extend truncated
   16-hex stored hashes to full 64-hex for
   `parser_version=parliament-pdf-v1.2` records — is carried forward.

6. **Pre-existing five divergent-content duplicate-ID Act records
   finding REAFFIRMED** — none of b0582 sample IDs are involved:
   act-zm-2025-014, act-zm-2025-028, act-zm-2019-010, act-zm-2020-010,
   act-zm-2018-001 each appear at both
   `records/acts/<year>/<id>.json` AND `records/acts/<id>.json` with
   divergent content. Operator dedupe action recommended (predates b0578).

## Integrity check

Per BRIEF.md §"Integrity checks". For a Phase 8 reverify batch (no record
mutation), the per-tick integrity check is:

- JSON report well-formed and parseable — **PASS**.
- All required summary keys present (batch, phase, parser_version,
  started_at, completed_at, seed, pool_size, sample_size, sample_rate,
  max_batch, results, match_count, drift_count, fetch_error_count,
  fetches) — **PASS**.
- `sample_size <= MAX_BATCH (8)` — **PASS** (8 <= 8).
- `fetches <= MAX_BATCH (8)` — **PASS** (8 fetches).
- `match_count + drift_count + fetch_error_count == sample_size` —
  **PASS** (1 + 7 + 0 = 8).
- All 8 sample IDs resolve to existing JSON records on disk under
  `records/**/*.json` — **PASS** (8/8 resolved via id-index).
- No sample record file mutated during/after the tick (record mtime
  not newer than `started_at − 5s`) — **PASS** (0/8 mutated).
- Each result entry contains the required fields (id, type, source_url,
  stored_sha256, fetched_status, fetched_at, verdict) — **PASS**.
- Each `verdict` is one of {match, drift, fetch_error,
  match_truncated_prefix} — **PASS**.
- Pool size ≥ 1800 (sanity floor) — **PASS** (1870).

No record mutation occurred. No new records were written. The seven
drift observations are reported analytically; per the 28-tick standing
finding they do NOT indicate corpus integrity failure — they indicate
upstream AKN-HTML rendering-pipeline non-determinism, and the
underlying legal text is unchanged. The stable-PDF supercohort (101/104
real-matches across 28 ticks; 3 truncated-prefix false drifts; zero
real drifts) continues to demonstrate that the stored corpus content
is faithful to the upstream sources.

## Budget impact

- Fetches this tick: **8** (all to zambialii.org, rate-limited at
  5 seconds between requests per approvals.yaml).
- Cumulative today (pre-b0582): 105 (per costs.log b0581 entry).
- Cumulative today (post-b0582): **113 / 2000**.
- Wall-clock duration: 46 seconds (well within 20-minute cap).

## Outputs

- `reports/batch-0582-reverify.json` (5.5 KB; deterministic JSON
  output of the reverify run).
- `reports/batch-0582.md` (this file).
- Append-only updates to `gaps.md`, `worker.log`, `costs.log`,
  `provenance.log`.
- No records written, modified, or deleted.
- No schema or YAML changes.

## Standing recommendations (carried forward — operator decision pending)

1. **Truncated-stored-hash backfill sweep** (b0578/b0579/b0581 standing):
   recompute and re-store full 64-hex `source_hash` for any remaining
   records where `parser_version=parliament-pdf-v1.2` AND `source_hash`
   length is `sha256:` + 16 hex. Underlying raw bytes unchanged; only
   stored hash representation extended.

2. **Phase 8 endpoint refinement** (b0565/b0567/b0569 standing): the
   28-tick pattern shows stable-PDF cohort drifts at zero and
   AKN-HTML cohort drifts at near-100%. Operator action options:
   (a) move Phase 8 to text-extraction-stable hashing for HTML
   endpoints, or (b) restrict Phase 8 to stable-PDF endpoints only,
   or (c) leave as-is (drift observations are now well-characterised).

3. **Divergent-content duplicate-ID Act records** (b0578 standing):
   dedupe the five Act records that appear at both
   `records/acts/<year>/<id>.json` AND `records/acts/<id>.json` with
   divergent content.

None of the above were actioned this tick — Phase 8 reverify worker
is read-only on records by design.
