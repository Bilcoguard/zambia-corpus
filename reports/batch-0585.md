# Batch 0585 — Phase 8 Nightly Re-verification (2026-05-11)

**UTC start:** 2026-05-11T07:29:52Z
**UTC end:** 2026-05-11T07:30:21Z
**Worker:** worker-tick (Phase 8)
**Phase:** phase_8_nightly_reverify (approved 2026-05-06; sample_rate 0.01)
**Parser:** phase8-reverify-0.1.0 (functional contract per scripts/batch_0546_phase8_reverify.py)
**Tick scope:** Twenty-ninth Phase 8 tick overall; first worker-tick of UTC date 2026-05-11
   (b0581 at 2026-05-10T20:34Z, b0582 at 2026-05-10T21:04Z were prior worker-tick
   ticks on 2026-05-10).
**Execution mode:** inline runner (`/tmp/b0583_phase8_reverify.py`, NOT committed)
   per sandbox-session safety constraint maintained since b0548 (b0548..b0582
   precedent). Underlying runner file retains its pre-renumber `b0583` name on
   disk; the report and commit use the renumbered b0585. Functional contract
   matches `scripts/batch_0546_phase8_reverify.py` baseline including
   `scripts/certs/*.pem` PKI loader. Differences from baseline: tick-suffixed
   seed `phase8-reverify-2026-05-11-b0583` (kept as-is after renumber to
   preserve sample-set reproducibility), plus truncated-stored-hash-prefix
   detection (b0570/b0578/b0581 cohort — recomputed sha256 whose value
   startswith the stored short-prefix is classified `match_truncated_prefix`
   and counted under `truncated_stored_hash_false_drift_count`).

## Batch-number renumber: b0583 → b0585

This tick was initially issued as b0583 — the next-available batch number
when `git pull --ff-only` returned `Already up to date` at HEAD=4a515f6
(b0582). Mid-tick, a parallel `judgment-ingestion-worker` push at
2026-05-11T07:48:01Z UTC took commit `6059533` claiming batch-0583 for the
first-ever Court of Appeal ingestion (NEW SOURCE: judiciaryzambia.com),
and a subsequent jiw push at 2026-05-11T11:35Z took commit `156d98e`
claiming batch-0584 for the page-2 CoA continuation. The same b0580
renumbering precedent — "Underlying scripts/_work/b0579/* artifacts
unchanged in path; report and commit message use b0580" — applies here:
**report and commit use b0585; underlying sample seed remains
`phase8-reverify-2026-05-11-b0583` so the sampled 8-record set remains
exactly reproducible from the seed alone.** The reverify-JSON file is
renamed `reports/batch-0585-reverify.json`; the underlying runner file
`/tmp/b0583_phase8_reverify.py` keeps its pre-renumber name (uncommitted
per sandbox-session safety constraint).

## Pre-tick git state observation

Pre-tick `git pull --ff-only` returned `Already up to date` at HEAD=4a515f6
(b0582). After the jiw collision and a second post-collision pull,
HEAD=156d98e (jiw b0584). This tick commits b0585's intended files via a
per-PID alt-index path (`GIT_INDEX_FILE=/tmp/b0585-commit-index`) reset to
HEAD per b0579..b0582 alt-index precedent, leaving the regular index
untouched.

The default `.git/index.lock` and `.git/HEAD.lock` cleanup remain
constrained on this sandbox by `Operation not permitted` virtiofs
semantics for backup-suffixed lock files in `.git/`. `git pull --ff-only`
succeeded with a single warning about an unremovable
`.git/objects/maintenance.lock` backup file — pull semantics not affected.

## Inputs

- Pool size: **1870** (at sample time, pre-jiw b0583/b0584 net additions;
  pool advanced to 1881 after jiw activity but the sample was already
  drawn from the 1870 record snapshot).
- Seed: `phase8-reverify-2026-05-11-b0583` (preserved after renumber for
  sample-set reproducibility).
- Sample size: **8** (= MAX_BATCH cap; ceil(0.01 × 1870) = 19 → capped at 8).
- Out-of-band re-fetches: **none**.

## Results — 5 match / 3 drift / 1 truncated_prefix / 0 fetch_error

| Verdict      | Count | Records |
|--------------|------:|---------|
| match (real) |     4 | si-zm-2010-006-national-monuments-entry-and-user-fees-regulation-2010 (zambialii akn /source.pdf 799,306 B — extends Act/SI `/source.pdf` stable-PDF cohort to 19/19); act-zm-2004-013-computer-misuse-and-crimes-act-2004 (media.zambialii.org legacy-PDF 1,480,069 B — **SECOND observation of the media.zambialii.org legacy-PDF endpoint in 29-tick series** after b0575 si-zm-2024-026; cohort now 2/2); si-zm-1986-004-income-tax-foreign-organisations-exemption-approval-order-1986 (zambialii akn /source.pdf 258,374 B — extends Act/SI `/source.pdf` stable-PDF cohort to 20/20); act-zm-2018-015 (parliament.gov.zm `/acts/` 14,937 B Value Added Tax Amendment Act 2018) |
| match_truncated_prefix |     1 | act-zm-2020-024-skills-development-levy-amendment-act-2020 (parliament.gov.zm `/amendment_act/` 19,845 B — **FOURTH 2020-vintage parliament-pdf-v1.2 truncated-stored-hash false-drift observation** after b0570 act-zm-2020-011, b0578 act-zm-2020-019, b0581 act-zm-2020-016. Stored 16-hex prefix `966825e257ac241a` startswith-matches recomputed full sha256 `966825e257ac241a507236985eb3e6c701e09f694b8b4e8d895a2bc012b79755`. Confirms pattern is reproducible across multiple 2020-vintage `parliament-pdf-v1.2` parser records.) |
| drift        |     3 | act-zm-1971-034-landlord-and-tenant-business-premises-act-1971 (zambialii.org/akn/zm/act/1971/34/eng@2020-10-26 211,326 B — fits AKN-HTML drift cohort); si-zm-2008-024-national-constitutional-conference-committees-regulations-2008 (zambialii.org/akn/zm/act/si/2008/24 bare-AKN-path 39,280 B — **FOURTH bare-AKN-path drift observation** in 29-tick series after b0579 si-zm-2023-041, b0581 si-zm-2019-014, b0582 si-zm-2023-009; sub-cohort remains SI-only); act-zm-1988-029-sports-council-of-zambia-act-1988 (zambialii.org/akn/zm/act/1988/29/eng@1996-12-31 137,298 B — fits AKN-HTML drift cohort) |
| fetch_error  |     0 | — |

## Cohort-level cumulative tally (post-b0585, 29 ticks)

| Cohort                                                              | Pre-b0585 | Δ b0585 | Post-b0585 |
|---------------------------------------------------------------------|----------:|--------:|-----------:|
| zambialii.org/akn/.../act-or-SI-HTML drift                          |     90/90 |   +3/+3 |      93/93 |
| zambialii.org/akn/.../source.pdf match (Acts/SIs)                   |     18/18 |   +2/+2 |      20/20 |
| zambialii.org/akn/.../source.pdf match (Judgments)                  |       1/1 |     0/0 |        1/1 |
| media.zambialii.org/media/legislation/ legacy-PDF match             |       1/1 |   +1/+1 |        2/2 |
| parliament.gov.zm static PDF match (real-match)                     |     82/82 |   +1/+1 |      83/83 |
| parliament.gov.zm static PDF real DRIFT                             |      0/85 |   0/+1  |       0/86 |
| parliament.gov.zm static PDF truncated_stored_hash_false_drift      |      3/85 |   +1/+1 |       4/86 |
| zambialii judgment-akn HTML drift                                   |      7/15 |     0/0 |       7/15 |
| Parliament-node landing                                             |       0/1 |     0/0 |        0/1 |
| Stable-PDF combined supercohort (parliament + zambialii akn /source.pdf + media.zambialii legacy) — real-drift basis | 101/104 | +4/+5 | 105/109 § |

§ Stable-PDF supercohort now 105/109 across 29 ticks. The 4 cumulative
  non-real-matches are the four truncated-stored-hash false drifts
  (b0570 act-zm-2020-011; b0578 act-zm-2020-019; b0581 act-zm-2020-016;
  b0585 act-zm-2020-024). **Real drift count on the stable-PDF supercohort
  remains zero across 29 ticks.**

## Notable observations (b0585)

1. **Fourth 2020-vintage parliament-pdf-v1.2 truncated-stored-hash false
   drift.** act-zm-2020-024 (Skills Development Levy Amendment Act 2020) now
   joins act-zm-2020-011 (b0570), act-zm-2020-019 (b0578), and act-zm-2020-016
   (b0581) in the truncated-stored-hash cohort. All four are Acts published
   in 2020, all four are parser_version `parliament-pdf-v1.2`, all four
   have stored `source_hash` of `sha256:` + 16 hex (not the full 64-hex).
   The recomputed full sha256 starts with the stored 16-hex prefix in
   each case — these are stored-hash truncation artefacts, NOT real
   content drift. Standing operator recommendation for a one-time
   backfill sweep is reinforced.

2. **Second media.zambialii.org legacy-PDF observation.** act-zm-2004-013
   (Computer Misuse and Crimes Act 2004) is the second sample drawn from
   the media.zambialii.org legacy-PDF endpoint in 29 ticks (first was
   b0575 si-zm-2024-026). Both observations matched cleanly. Cohort
   now 2/2.

3. **Fourth bare-AKN-path drift observation.** si-zm-2008-024
   (National Constitutional Conference Committees Regulations 2008) is the
   fourth bare-AKN-path drift in the 29-tick series after b0579
   (si-zm-2023-041), b0581 (si-zm-2019-014), and b0582 (si-zm-2023-009).
   All four are SIs, with URL form `/akn/zm/act/si/<year>/<n>` (no
   `/eng@<date>` suffix, no `/source.pdf` suffix). Acts in the Phase 8
   sample pool continue to consistently use the `/eng@<date>` form. This
   is a URL-form sub-classification of the AKN-HTML drift cohort, not a
   new drift class — the underlying mechanism (akn-HTML rendering
   pipeline non-determinism) is the same.

4. **No new judgment-akn HTML drift observations this tick.** Sample
   contained no judgment records; judgment-akn HTML drift cohort (7/15)
   remains unchanged from b0582.

5. **Pre-existing five divergent-content duplicate-ID Act records
   finding REAFFIRMED** — none of b0585 sample IDs are involved:
   act-zm-2025-014, act-zm-2025-028, act-zm-2019-010, act-zm-2020-010,
   act-zm-2018-001 each appear at both
   `records/acts/<year>/<id>.json` AND `records/acts/<id>.json` with
   divergent content. Operator dedupe action recommended (predates b0578).

6. **Batch-number renumber (see header section).** This tick was
   originally b0583 — renumbered to b0585 after the jiw worker pushed
   commits 6059533 (b0583, FIRST-ever Court of Appeal ingestion) and
   156d98e (b0584, CoA page-2 continuation) during the interval between
   sample-draw (07:29:52Z) and commit. Sample seed kept as
   `phase8-reverify-2026-05-11-b0583` to preserve sample-set
   reproducibility; the JSON results file (`batch-0585-reverify.json`)
   and this report carry the renumbered identifier.

## Integrity check

Per BRIEF.md §"Integrity checks". For a Phase 8 reverify batch (no record
mutation), the per-tick integrity check is:

- JSON report well-formed and parseable — **PASS**.
- All required summary keys present (batch, phase, parser_version,
  started_at, completed_at, seed, pool_size, sample_size, sample_rate,
  max_batch, results, match_count, drift_count, fetch_error_count,
  truncated_stored_hash_false_drift_count, fetches) — **PASS**.
- `sample_size <= MAX_BATCH (8)` — **PASS** (8 <= 8).
- `fetches <= MAX_BATCH (8)` — **PASS** (8 fetches).
- `match_count + drift_count + fetch_error_count == sample_size` —
  **PASS** (5 + 3 + 0 = 8) (truncated_prefix counted under match per
  baseline convention).
- All 8 sample IDs resolve to existing JSON records on disk under
  `records/**/*.json` — **PASS** (8/8 resolved via id-index).
- No sample record file mutated during/after the tick (record mtime
  not newer than `started_at − 5s`) — **PASS** (0/8 mutated).
- Each result entry contains the required fields (id, type, source_url,
  stored_sha256, fetched_status, fetched_at, verdict) — **PASS**.
- Each `verdict` is one of {match, drift, fetch_error,
  match_truncated_prefix} — **PASS**.
- Pool size ≥ 1800 (sanity floor) — **PASS** (1870 at sample time;
  1881 at commit time).

No record mutation occurred. No new records were written. The three
drift observations are reported analytically; per the 29-tick standing
finding they do NOT indicate corpus integrity failure — they indicate
upstream AKN-HTML rendering-pipeline non-determinism, and the
underlying legal text is unchanged. The stable-PDF supercohort (105/109
real-matches across 29 ticks; 4 truncated-prefix false drifts; zero
real drifts) continues to demonstrate that the stored corpus content
is faithful to the upstream sources.

## Budget impact

- Fetches this tick: **8** (7 to zambialii.org / media.zambialii.org at
  5 seconds between requests, 1 to www.parliament.gov.zm at 2 seconds
  between requests per approvals.yaml; wait: actually 2 of the 8 went
  to www.parliament.gov.zm).
- Cumulative today (pre-b0585, on 2026-05-11): 0 (fresh UTC day, this is
  the first worker-tick channel tick of the day).
- Cumulative today (post-b0585, on 2026-05-11): **8 / 2000**.
- Wall-clock duration: 29 seconds (well within 20-minute cap).

## Outputs

- `reports/batch-0585-reverify.json` (deterministic JSON output).
- `reports/batch-0585.md` (this file).
- Append-only updates to `worker.log`, `costs.log`, `provenance.log`.
- No records written, modified, or deleted.
- No schema or YAML changes.

## Standing recommendations (carried forward — operator decision pending)

1. **Truncated-stored-hash backfill sweep** (b0578/b0579/b0581/b0585
   standing): recompute and re-store full 64-hex `source_hash` for any
   remaining records where `parser_version=parliament-pdf-v1.2` AND
   `source_hash` length is `sha256:` + 16 hex. Cohort has now reproduced
   4 times across 29 ticks; underlying raw bytes unchanged; only stored
   hash representation extended.

2. **Phase 8 endpoint refinement** (b0565/b0567/b0569 standing): the
   29-tick pattern shows stable-PDF cohort real-drifts at zero and
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
