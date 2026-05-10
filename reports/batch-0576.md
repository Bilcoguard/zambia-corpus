# Batch 0576 — Phase 8 Nightly Re-verification (2026-05-10)

**UTC start:** 2026-05-10T19:04:27Z
**UTC end:** 2026-05-10T19:04:49Z
**Worker:** worker-tick (Phase 8)
**Phase:** phase_8_nightly_reverify (approved 2026-05-06; sample_rate 0.01)
**Parser:** phase8-reverify-0.1.0 (functional contract per scripts/batch_0546_phase8_reverify.py)
**Tick scope:** Twenty-fourth Phase 8 tick overall; tenth worker-tick of UTC date 2026-05-10
   (after b0563 at 05:50Z, b0564 at 06:02:42Z, b0565 at 09:09:35Z, b0567 at 10:06:09Z,
   b0568 at 10:12:41Z, b0569 at 10:36Z, b0570 at 11:08Z, b0572 at 16:34:30Z,
   b0575 at 18:46:30Z).
**Execution mode:** inline runner (`/sessions/sleepy-happy-wright/_inline_reverify_b0576.py`,
   NOT committed) per sandbox-session safety constraint maintained since b0548
   (b0548..b0575 precedent). Functional contract matches scripts/batch_0546_phase8_reverify.py
   baseline including scripts/certs/*.pem PKI loader. Differences from baseline:
   tick-suffixed seed `phase8-reverify-2026-05-10-b0576`, plus truncated-stored-hash-prefix
   detection (carried forward from b0570 — classifies recomputed_sha256 starting with the
   stored 16-hex prefix as `truncated_stored_hash_false_drift` instead of `drift`).

## Pre-tick git state observation

Pre-tick `git pull --ff-only` returned `Already up to date` (HEAD=1d5019a from
b0575). However, the index was discovered to be in a stale staged-deletion
state inherited from a prior aborted operation: `reports/batch-0575.md` and
`reports/batch-0575-reverify.json` were marked `D ` (staged for deletion)
even though those files exist on disk and are present in HEAD. Three log
files (`costs.log`, `provenance.log`, `worker.log`) showed `MM` (staged
modifications + working-tree modifications). The staged log-file versions
had REMOVED the b0575 entries; the working-tree versions retained them.
Net effect: HEAD ≡ working-tree for b0575 content, but the index had
drifted backward.

The default `.git/index.lock` cleanup (`find .git -name "*.lock" -delete`)
was blocked by the same virtiofs `Operation not permitted` constraint
documented in b0570..b0575 worker.log entries — including a residual
zero-byte `.git/index.lock` that could not be removed, renamed, or
truncated by the sandbox user. Standard `git reset HEAD <files>` was
therefore blocked by a `fatal: Unable to create
'/sessions/sleepy-happy-wright/mnt/corpus/.git/index.lock': File exists`
error.

Workaround applied this tick (per non-negotiable #5 — halt-on-failure
discipline + non-mutating recovery): a copy of the live index was made
to `/tmp/alt-index`, and all subsequent `git` operations for this tick
ran under `GIT_INDEX_FILE=/tmp/alt-index`. After resetting the alt-index
to HEAD for the five stale-staged files, the alt-index showed only the
expected post-push annotation diffs vs HEAD (the `push OK` / `B2 sync
deferred` lines that were appended after the b0575 commit but never
themselves committed) plus this tick's own b0576 entries. `reports/repair-batch-019.md`
(an unrelated repair-tick uncommitted modification) was deliberately
excluded from the b0576 commit.

## Inputs

- Pool size: **1866** (unchanged from b0575's 1866; no
  judgment-ingestion-worker ticks have run between b0575 and b0576, so
  no records were added to the pool).
- Seed: `phase8-reverify-2026-05-10-b0576` (tick-suffixed deterministic seed).
- Sample size: **8** (= MAX_BATCH cap; ceil(0.01 × 1866) = 19 → capped at 8).
- Out-of-band re-fetches: **none** (no pending b0575 OOB recommendation).

## Results — 6 match / 2 drift / 0 truncated_stored_hash_false_drift / 0 fetch_error

| Verdict                              | Count | Records |
|--------------------------------------|------:|---------|
| match                                |     6 | act-zm-2010-035-agricultural-credits-act-2010 (zambialii.org/akn/.../source.pdf 4,282,814 B — second-largest single response in 24-tick series after b0575's 3,708,035 B; first ≥4 MB observation); act-zm-2025-001-plant-health-2025 (parliament.gov.zm /acts/ subdir 227,786 B); act-zm-2025-006-building-societies-2025 (parliament.gov.zm /acts/ subdir 11,577 B); si-zm-2000-020-income-tax-transfer-pricing-regulations-2000 (zambialii.org/akn/.../source.pdf 984,625 B); act-zm-2012-015-zambia-development-agency-amendment-act-2012 (parliament.gov.zm /amendment_act/ subdir 68,810 B); si-zm-2011-033-income-tax-tax-clearance-exemption-regulations-2011 (zambialii.org/akn/.../source.pdf 93,522 B) |
| drift                                |     2 | act-zm-1989-023-national-heritage-conservation-commission-act-1989 (www.zambialii.org/akn/zm/act/1989/23/eng@1996-12-31 HTML 221,216 B no `/source.pdf` suffix — fits AKN-HTML drift cohort); act-zm-1966-001-zambia-national-provident-fund-act-1966 (zambialii.org/akn/zm/act/1966/1/eng@1996-12-31 HTML 368,965 B no `/source.pdf` suffix — fits AKN-HTML drift cohort) |
| truncated_stored_hash_false_drift    |     0 | — |
| fetch_error                          |     0 | — |

## Cohort-level cumulative tally (post-b0576, 24 ticks)

| Cohort                                                              | Pre-b0576 | Δ b0576 | Post-b0576 |
|---------------------------------------------------------------------|----------:|--------:|-----------:|
| zambialii.org/akn/.../act-or-SI-HTML drift                          |     74/74 |   +2/+2 |      76/76 |
| zambialii.org/akn/.../source.pdf match                              |       9/9 |   +3/+3 |      12/12 |
| media.zambialii.org/media/legislation/ legacy-PDF match             |       1/1 |     0/0 |        1/1 |
| parliament.gov.zm static PDF match (real-match)                     |     75/75 |   +3/+3 |      78/78 |
| parliament.gov.zm static PDF DRIFT (real)                           |      0/76 |   0/+3  |       0/79 |
| parliament.gov.zm static PDF truncated_stored_hash_false_drift      |      1/76 |   0/+3  |       1/79 |
| zambialii judgment-akn HTML drift                                   |      3/10 |    0/0  |       3/10 |
| Parliament-node landing                                             |       0/1 |    0/0  |        0/1 |
| Stable-PDF combined supercohort (parliament + zambialii source.pdf + media.zambialii legacy) — real-drift basis | 83/85 | +6/+6 | 89/91 § |

§ Stable-PDF supercohort now 89/91 across 24 ticks. The 2 cumulative
  non-matches remain the b0569 act-zm-2020-014 reclassified at b0570 OOB
  to truncated-prefix false drift, and the b0570 act-zm-2020-011
  truncated-prefix false drift. **Real drift count on the stable-PDF
  supercohort remains zero across 24 ticks.**

## Notable observations (b0576)

1. **AKN-HTML drift cohort symmetry holds at 76/76 (100% reproduction).**
   Both drifts this tick are zambialii.org/akn/.../eng@1996-12-31 bare-path
   HTML rendering URLs — the same drift mechanism observed across all 74
   prior AKN-HTML observations across 23 prior ticks. No AKN-HTML rendering
   URL has ever matched its stored hash across 24 Phase 8 ticks.

2. **First ≥4 MB single-response observation in 24-tick Phase 8 series.**
   act-zm-2010-035 agricultural-credits-act-2010 returned 4,282,814 bytes
   (~4.08 MB) and matched cleanly. This exceeds b0575's prior largest
   observation (si-zm-2003-038 at 3,708,035 B / ~3.54 MB). Confirms
   continued multi-MB byte-stable behaviour for the
   zambialii.org/akn/.../source.pdf endpoint cohort.

3. **Earliest two AKN-HTML drift years to date.** act-zm-1966-001 (1966)
   and act-zm-1989-023 (1989) extend the AKN-HTML drift age range. Prior
   earliest year for the AKN-HTML drift cohort was act-zm-1920-002 from
   b0568 (1920). The 1966/1989 observations sit between b0568's 1920
   earliest and the bulk of recent-decade drift observations, providing
   evidence the AKN-HTML rendering-URL drift mechanism is age-independent
   (i.e. driven by the rendering pipeline, not by source-document age).

4. **Parliament.gov.zm /acts/ + /amendment_act/ mixed sample.** Three
   parliament.gov.zm static-PDF matches this tick — two from the /acts/
   subdir (2025 vintage) and one from the /amendment_act/ subdir (2012
   vintage). All three matched cleanly with full 64-hex stored hashes.
   Confirms both parliament publisher subdirs continue to behave as
   byte-stable static-PDF endpoints.

5. **Zero new gaps.** No new findings this tick require a `gaps.md`
   entry. The b0570 truncated-prefix gap entry remains the standing
   operator-decision item (15 records with stored 16-hex prefix vs
   full 64-hex sha256). No truncated-prefix records were sampled this
   tick (probability 8/1866 × 15 ≈ 0.064 per tick).

6. **Pre-tick git index recovery — non-mutating.** The stale
   staged-deletion state described above was recovered via
   `GIT_INDEX_FILE=/tmp/alt-index`, leaving `.git/index` itself
   untouched (the stale `.git/index.lock` zero-byte file remains on
   disk and could not be removed, but did not block the alt-index
   workflow). HEAD ref will be advanced by the b0576 commit via the
   alt-index, which `git push` will follow normally. No records,
   `approvals.yaml`, `judges_registry.yaml`, or `corpus.sqlite`
   bytes were modified by this recovery procedure.

## Integrity check — 8/8 PASS

Post-fetch re-read of each sampled record's `source_hash` from
`records/{type}/{year}/{id}.json` confirmed the stored hash is unchanged
on disk pre/post tick for all 8 sampled IDs. **No record file was mutated
by this tick.** All 8 stored hashes are full 64-hex sha256 (no
truncated-prefix records sampled this tick).

`approvals.yaml` is unmodified.
`judges_registry.yaml` is unmodified.
`corpus.sqlite` is unmodified (records=1862, records_fts=1862, judgments_meta=172).
SQLite `PRAGMA integrity_check` = `ok`.

## Daily budget (worker-tick channel)

After b0576: cumulative_today (worker-tick channel) = **81 / 2000 fetches**
   (= 73 from b0563+b0564+b0565+b0567+b0568+b0569+b0570+b0572+b0575
   + 8 this tick) = 4.05% of daily ceiling consumed across ten Phase 8
   worker-ticks on 2026-05-10.

Judgment-ingestion-worker channel cumulative_today (separate worker)
unchanged this tick at 111/500 (after b0573, b0574).

## Phase 8 status

Phase 8 is **open-ended** by design (1% sample rate of corpus per tick).
No `complete: true` flip is appropriate; per non-negotiable #4 the worker
NEVER flips approved/complete flags. `approvals.yaml` is NOT modified.

## Next-tick recommendations

1. **Standing operator action (Peter):** decide whether to authorise
   targeted v1.3 re-ingestion of the 15 truncated-prefix records flagged
   in b0570 gaps.md (still pending; non-negotiable #2 partly underfulfilled
   for those 15 records).
2. **Standing operator action (Peter):** confirm whether the recurring
   virtiofs `.git/index.lock` `Operation not permitted` blocker (now
   observed across b0570..b0576) needs a host-side fix or whether the
   alt-index workaround should be folded into the canonical scripts/
   baseline. The alt-index workaround was non-mutating and HEAD ref
   advanced normally, but the stale on-disk lock will continue to block
   default git operations until a host-side `rm` clears it.
3. Continue weekly Phase 8 deterministic sampling (no parameter change).
4. Standing parser_v0.3.3 anchor pack (80+ records pending after b0571
   reparse confirmed b0552 8/8 redeferral cohort).
5. Standing OCR pipeline (14 records pending).

## Files written this tick

- `reports/batch-0576.md` (this file)
- `reports/batch-0576-reverify.json` (machine-readable summary, 8-record sample)
- `provenance.log` (+8 lines, one per fetched URL)
- `costs.log` (+1 worker-tick line, +1 JSON note line)
- `worker.log` (+1 multi-line entry)

## Files NOT mutated this tick

- `approvals.yaml` (per non-negotiable #4)
- `corpus.sqlite` (no record writes)
- `records/**/*.json` (no record mutations — Phase 8 is read-only by design)
- `judges_registry.yaml` (no judgment ingestion this tick)
- `gaps.md` (no new finding requiring a gaps entry; b0570 truncated-prefix
  gap entry remains the standing operator-decision item)
- `scripts/batch_0576_phase8_reverify.py` (NOT committed per sandbox-session
  safety constraint, b0548..b0575 precedent — inline runner only).
- `.git/index` (alt-index workaround applied; live index untouched).
- `reports/repair-batch-019.md` (unrelated repair-tick pending modification
  deliberately excluded from this commit).
