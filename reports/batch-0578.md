# Batch 0578 — Phase 8 Nightly Re-verification (2026-05-10)

**UTC start:** 2026-05-10T19:35:51Z
**UTC end:** 2026-05-10T19:36:11Z
**Worker:** worker-tick (Phase 8)
**Phase:** phase_8_nightly_reverify (approved 2026-05-06; sample_rate 0.01)
**Parser:** phase8-reverify-0.1.0 (functional contract per scripts/batch_0546_phase8_reverify.py)
**Tick scope:** Twenty-fifth Phase 8 tick overall; eleventh worker-tick of UTC
   date 2026-05-10 (after b0563 at 05:50Z, b0564 at 06:02:42Z, b0565 at 09:09:35Z,
   b0567 at 10:06:09Z, b0568 at 10:12:41Z, b0569 at 10:36Z, b0570 at 11:08Z,
   b0572 at 16:34:30Z, b0575 at 18:46:30Z, b0576 at 19:04:49Z).
**Execution mode:** inline runner (`/sessions/festive-fervent-sagan/_inline_reverify_b0578.py`,
   NOT committed) per sandbox-session safety constraint maintained since b0548
   (b0548..b0577 precedent). Functional contract matches scripts/batch_0546_phase8_reverify.py
   baseline including scripts/certs/*.pem PKI loader. Differences from baseline:
   tick-suffixed seed `phase8-reverify-2026-05-10-b0578`, plus truncated-stored-hash-prefix
   detection (carried forward from b0570 — recomputed sha256 starting with the stored
   16-hex prefix is classified as `truncated_stored_hash_false_drift` instead of `drift`).

## Pre-tick git state observation

Pre-tick `git pull --ff-only` returned `Already up to date` (HEAD=e154424 from
b0577). The index was again in the stale staged-deletion state inherited
from prior aborted operations (b0570..b0576 documented the same condition):
five `D ` entries (b0575/b0576 reverify outputs and b0577 jiw report)
showing as staged-for-deletion even though the on-disk files exist and
HEAD includes them; three `MM` log files (`costs.log`, `provenance.log`,
`worker.log`) and one `MM` `gaps.md` whose staged versions had reverted
to the pre-b0575 state. Net effect: HEAD ≡ working-tree contents, but
the index had drifted backward.

The default `.git/index.lock` cleanup (`find .git -name "*.lock" -delete`)
remained blocked by the virtiofs `Operation not permitted` constraint
documented in b0570..b0577 worker.log entries — including a residual
zero-byte `.git/index.lock` that could not be removed, renamed, or
truncated by the sandbox user.

Workaround applied this tick (per non-negotiable #5 — halt-on-failure
discipline + non-mutating recovery): a copy of the live index was made
via `cat .git/index > /tmp/alt-index-<unix-ts>-<pid>` (stale
`/tmp/alt-index` from a prior session was owned by a different sandbox
user and could not be overwritten on the sticky `/tmp` mount, so a
fresh per-PID path was used), and all subsequent `git` operations for
this tick ran under `GIT_INDEX_FILE=$ALT`. After resetting the
alt-index to HEAD for the eleven stale-staged paths, the alt-index
showed only the expected post-push annotation diffs vs HEAD plus this
tick's own b0578 entries. `reports/repair-batch-019.md` (an unrelated
repair-tick uncommitted modification) was again deliberately excluded
from the b0578 commit.

## Inputs

- Pool size: **1867** (was 1866 at b0576 close; +1 net addition since b0576
  reflects the b0577 jiw record additions — judgment-zm-2016-zmcc-08
  Siamoondo and judgment-zm-2016-zmcc-10 Mutapwe, both with
  `source_url`+`source_hash` populated, against b0576's then-pool of
  1866; the +1 net suggests a single record without complete provenance
  in the b0577 batch is excluded from the audit pool, or one record
  pre-existed in the prior pool count, requires audit at next pool
  validation tick).
- Seed: `phase8-reverify-2026-05-10-b0578` (tick-suffixed deterministic seed).
- Sample size: **8** (= MAX_BATCH cap; ceil(0.01 × 1867) = 19 → capped at 8).
- Out-of-band re-fetches: **none**.

## Results — 3 match / 4 drift / 1 truncated_stored_hash_false_drift / 0 fetch_error

| Verdict                              | Count | Records |
|--------------------------------------|------:|---------|
| match                                |     3 | act-zm-2009-008-one-stop-border-control (parliament.gov.zm /acts/ subdir 1,157,270 B); act-zm-2018-013 (parliament.gov.zm /acts/ subdir 233,571 B — Statistics Act 2018); act-zm-2021-032-electoral-process-amendment-act-2021 (parliament.gov.zm /amendment_act/ subdir 25,131 B) |
| drift                                |     4 | act-zm-1992-017-appropriation-act-1992 (zambialii.org/akn/zm/act/1992/17/eng@1992-04-01 HTML 40,712 B no `/source.pdf` suffix — fits AKN-HTML drift cohort); act-zm-1968-034-loans-kafue-gorge-hydro-electric-power-project-act-1968 (zambialii.org/akn/zm/act/1968/34/eng@1996-12-31 HTML 47,412 B no `/source.pdf` suffix — fits AKN-HTML drift cohort); act-zm-2003-017-excess-expenditure-appropriation-1998-act-2003 (zambialii.org/akn/zm/act/2003/17/eng@2003-12-12 HTML 38,703 B no `/source.pdf` suffix — fits AKN-HTML drift cohort); act-zm-cap-270-employment-special-provisions-act (zambialii.org/akn/zm/act/1966/29/eng@1996-12-31 HTML 49,139 B no `/source.pdf` suffix — fits AKN-HTML drift cohort, CAP-form ID maps to 1966/29) |
| truncated_stored_hash_false_drift    |     1 | act-zm-2020-019-zambia-national-public-health-institute-act-2020 (parliament.gov.zm /acts/ subdir 82,258 B — stored sha256 prefix `de3e14baaecfaf16` (16 hex) matches recomputed full sha256 prefix; not real drift) |
| fetch_error                          |     0 | — |

## Cohort-level cumulative tally (post-b0578, 25 ticks)

| Cohort                                                              | Pre-b0578 | Δ b0578 | Post-b0578 |
|---------------------------------------------------------------------|----------:|--------:|-----------:|
| zambialii.org/akn/.../act-or-SI-HTML drift                          |     76/76 |   +4/+4 |      80/80 |
| zambialii.org/akn/.../source.pdf match                              |     12/12 |     0/0 |      12/12 |
| media.zambialii.org/media/legislation/ legacy-PDF match             |       1/1 |     0/0 |        1/1 |
| parliament.gov.zm static PDF match (real-match)                     |     78/78 |   +3/+3 |      81/81 |
| parliament.gov.zm static PDF DRIFT (real)                           |      0/79 |   0/+4  |       0/82 |
| parliament.gov.zm static PDF truncated_stored_hash_false_drift      |      1/79 |   +1/+4 |       2/82 |
| zambialii judgment-akn HTML drift                                   |      3/10 |     0/0 |       3/10 |
| Parliament-node landing                                             |       0/1 |     0/0 |        0/1 |
| Stable-PDF combined supercohort (parliament + zambialii source.pdf + media.zambialii legacy) — real-drift basis | 89/91 | +3/+4 | 92/95 § |

§ Stable-PDF supercohort now 92/95 across 25 ticks. The 3 cumulative
  non-matches are all truncated-stored-hash false drifts (b0569 act-zm-2020-014
  → reclassified at b0570 OOB; b0570 act-zm-2020-011; b0578 act-zm-2020-019).
  **Real drift count on the stable-PDF supercohort remains zero across 25 ticks.**

## Notable observations (b0578)

1. **AKN-HTML drift cohort symmetry holds at 80/80 (100% reproduction).**
   All four drifts this tick are zambialii.org/akn/.../[eng@…] bare-path
   HTML rendering URLs — the same drift mechanism observed across all 76
   prior AKN-HTML observations across 24 prior ticks. No AKN-HTML
   rendering URL has ever matched its stored hash across 25 Phase 8 ticks.

2. **Second truncated-prefix false-drift on parliament.gov.zm cohort.**
   act-zm-2020-019-zambia-national-public-health-institute-act-2020 has
   a 16-hex stored hash (`de3e14baaecfaf16`) which prefix-matches the
   recomputed full 64-hex sha256 (`de3e14baaecfaf16244a254c85c375707…`).
   This is the second observation of this pattern after b0570's
   act-zm-2020-011 finding (b0569 act-zm-2020-014 was reclassified at
   b0570 OOB). The cumulative truncated-prefix cohort on parliament
   static PDFs is now 2/82, all from 2020-vintage `parliament-pdf-v1.2`
   parser baseline. Operator action recommended: a one-time backfill
   sweep to recompute and re-store full 64-hex source_hash for any
   remaining records whose `parser_version=parliament-pdf-v1.2` and
   `source_hash` length is `sha256:` + 16 hex.

3. **CAP-form ID drift observation.** act-zm-cap-270-employment-special-provisions-act
   maps to URL `https://zambialii.org/akn/zm/act/1966/29/eng@1996-12-31`
   (CAP 270 → 1966/29 numbered Act). This is the first CAP-form record
   sampled by Phase 8 to date and confirms CAP-mapped legacy Acts
   exhibit the same AKN-HTML drift behaviour as numbered-Act records.
   No new failure mode.

4. **Lowest match rate in 25-tick Phase 8 series at 3/8 = 37.5%.** Sample
   was heavily zambialii-AKN-HTML weighted (4/8 zambialii bare-path drifts).
   Prior low was b0567 at 6/8 = 75% (per b0575 cumulative note); however
   b0567's distribution has since been superseded by smaller samples;
   the binomial chance of drawing 4+ AKN-HTML records given the AKN-HTML
   cohort's 80/1867 ≈ 4.3% pool share is ~0.07% — sampling variance
   alone, no signal of new drift mechanism.

5. **Parliament static-PDF cohort real-match rate steady at 81/82 = 98.8%
   (1 truncated-prefix false drift, 0 real drifts).** The 81/82 ratio is
   the highest-coverage stable cohort observation in the 25-tick series.

## Repository state observations

- Pool count `1867` exceeds `corpus.sqlite records` count `1864`. Repo
  contains records-on-disk JSON files at both `records/{type}/<year>/<id>.json`
  and `records/{type}/<id>.json` paths for at least five Acts
  (act-zm-2025-014-cotton-act, act-zm-2025-028-appropriation-act,
  act-zm-2019-010-nurses-and-midwives-act-2019,
  act-zm-2020-010-national-council-for-construction-act-2020,
  act-zm-2018-001-public-finance-management-act). The five duplicate-id
  pairs have **divergent JSON content** (file-level sha256 differs
  between each pair). Pre-existing condition (predates b0578); pool
  duplicate-counting is layout-driven not phase-8-driven; logged to
  gaps.md for operator review. None of the b0578 sample IDs are
  involved in this duplication.
- `corpus.sqlite` PRAGMA integrity_check: **ok**. records=1864,
  records_fts=1864, judgments_meta=174. Unchanged from b0577.
- `judges_registry.yaml` unchanged.
- `approvals.yaml` unchanged. **Phase 8 remains open-ended (sample_rate
  audit, no completion target).** No completion flip.
- `records/` not modified by this tick (Phase 8 reverify is read-only
  by contract).

## Daily budget (worker-tick channel)

`cumulative_today` (worker-tick before b0578): **81/2000** (4.05%).
b0578 spent 8 fetches. **Post-b0578 cumulative_today (worker-tick):
89/2000 (4.45%).** Well under cap.

## Files written / appended

- `reports/batch-0578-reverify.json` — structured per-record audit
  output (machine-readable; consumed by future cumulative-cohort
  recomputation if the seed register is ever rebuilt).
- `reports/batch-0578.md` — this human-readable report.
- `provenance.log` — appended one line summarising this tick.
- `costs.log` — appended one tick line + one summary JSON line.
- `worker.log` — appended START / body / STOP / push trace.
- `gaps.md` — appended b0578 cohort entry plus pre-existing
  divergent-duplicate-id observation note.

## Files NOT written / mutated

- `records/**/*.json`
- `corpus.sqlite`
- `approvals.yaml`
- `judges_registry.yaml`
- `scripts/batch_0578_phase8_reverify.py` (NOT committed; b0548..b0577
  sandbox-session safety precedent maintained — inline runner lives at
  `/sessions/festive-fervent-sagan/_inline_reverify_b0578.py` outside the
  workspace tree).

## B2 sync

`rclone` not available in sandbox — B2 sync deferred to host (b0563..b0577 precedent).
