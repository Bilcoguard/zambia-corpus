# Batch 0579 — Phase 8 Nightly Re-verification (2026-05-10)

**UTC start:** 2026-05-10T20:05:17Z
**UTC end:** 2026-05-10T20:05:56Z
**Worker:** worker-tick (Phase 8)
**Phase:** phase_8_nightly_reverify (approved 2026-05-06; sample_rate 0.01)
**Parser:** phase8-reverify-0.1.0 (functional contract per scripts/batch_0546_phase8_reverify.py)
**Tick scope:** Twenty-sixth Phase 8 tick overall; twelfth worker-tick of UTC
   date 2026-05-10 (after b0563 at 05:50Z, b0564 at 06:02:42Z, b0565 at 09:09:35Z,
   b0567 at 10:06:09Z, b0568 at 10:12:41Z, b0569 at 10:36Z, b0570 at 11:08Z,
   b0572 at 16:34:30Z, b0575 at 18:46:30Z, b0576 at 19:04:49Z, b0578 at 19:35:51Z).
**Execution mode:** inline runner (`/sessions/laughing-cool-thompson/_inline_reverify_b0579.py`,
   NOT committed) per sandbox-session safety constraint maintained since b0548
   (b0548..b0578 precedent). Functional contract matches scripts/batch_0546_phase8_reverify.py
   baseline including scripts/certs/*.pem PKI loader. Differences from baseline:
   tick-suffixed seed `phase8-reverify-2026-05-10-b0579`, plus truncated-stored-hash-prefix
   detection (carried forward from b0570/b0578 — recomputed sha256 starting with the
   stored 16-hex prefix is classified as `truncated_stored_hash_false_drift`).

## Pre-tick git state observation

Pre-tick `git pull --ff-only` returned `Already up to date` (HEAD=16fb1f9 from
b0578). The index was again in the stale staged-deletion state inherited
from prior aborted operations (b0570..b0578 documented the same condition):
the eleven `D ` entries from b0578 (records/judgments/zmcc/2016 ZMCC 2016
records and reports/batch-057{5,6,7,8} files) plus three/four `MM` log
files (`costs.log`, `provenance.log`, `worker.log`, `gaps.md`) whose
staged versions had reverted to a pre-b0575 state. Net effect: HEAD ≡
working-tree contents, but the index had drifted backward.

The default `.git/index.lock` cleanup remains constrained on this
sandbox by `Operation not permitted`/virtiofs semantics for
backup-suffixed lock files in `.git/`. `git pull --ff-only` succeeded
with a single warning about an unremovable `.git/objects/maintenance.lock`
backup file — pull semantics not affected.

Workaround applied this tick (per non-negotiable #5 — halt-on-failure
discipline + non-mutating recovery): a per-PID alt-index path is used
for staging/commit (`GIT_INDEX_FILE=/tmp/alt-index-b0579`), the alt-index
is reset to HEAD for all stale-staged paths, and only this tick's intended
files are added before commit. `reports/repair-batch-019.md` (an unrelated
repair-tick uncommitted modification) is again deliberately excluded from
the b0579 commit.

## Inputs

- Pool size: **1867** (unchanged from b0578 close — no new judgment-ingestion
  ticks since b0577).
- Seed: `phase8-reverify-2026-05-10-b0579` (tick-suffixed deterministic seed).
- Sample size: **8** (= MAX_BATCH cap; ceil(0.01 × 1867) = 19 → capped at 8).
- Out-of-band re-fetches: **none**.

## Results — 5 match / 3 drift / 0 truncated_stored_hash_false_drift / 0 fetch_error

| Verdict      | Count | Records |
|--------------|------:|---------|
| match        |     5 | si-zm-2009-044-banking-and-financial-services-restriction-on-kwacha-lending-to-non-residents-re (zambialii akn /source.pdf 357,672 B); act-zm-2018-008-the-anti-terrorism-and-non-proliferation-act-2018 (parliament.gov.zm /acts/ subdir 204,434 B); judgment-zm-2019-zmcc-24-mwiya-mutapwe-v-shomeno-dominic (zambialii judgment-akn HTML rendering URL 47,457 B — judgment-akn cohort match); si-zm-2020-096-higher-education-loans-and-scholarships-transfer-of-staff-regulations-2020 (zambialii akn /source.pdf 10,269 B); si-zm-1994-039-workmens-compensation-assessment-or-earnings-regulations-1994 (zambialii akn /source.pdf 188,197 B) |
| drift        |     3 | judgment-zm-2026-zmcc-07-climate-action-professionals-zambia-v-attorney-gen (zambialii.org/akn/zm/judgment/zmcc/2026/7/eng@2026-03-25 49,750 B — judgment-akn drift cohort; FIRST 2026-vintage record reverified across 26 Phase 8 ticks); si-zm-2023-041-energy-regulation-general-regulations-2023 (zambialii.org/akn/zm/act/si/2023/41 41,800 B — bare AKN path with **no /eng@/ suffix and no /source.pdf** — FIRST observation of bare-AKN-path drift variant in 26-tick series; fits AKN-HTML drift cohort); act-zm-1965-008-provincial-and-district-boundaries-act-1965 (zambialii.org/akn/zm/act/1965/8/eng@1996-12-31 40,613 B — fits AKN-HTML drift cohort) |
| truncated_stored_hash_false_drift | 0 | — |
| fetch_error  |     0 | — |

## Cohort-level cumulative tally (post-b0579, 26 ticks)

| Cohort                                                              | Pre-b0579 | Δ b0579 | Post-b0579 |
|---------------------------------------------------------------------|----------:|--------:|-----------:|
| zambialii.org/akn/.../act-or-SI-HTML drift                          |     80/80 |   +2/+2 |      82/82 |
| zambialii.org/akn/.../source.pdf match                              |     12/12 |   +3/+3 |      15/15 |
| media.zambialii.org/media/legislation/ legacy-PDF match             |       1/1 |     0/0 |        1/1 |
| parliament.gov.zm static PDF match (real-match)                     |     81/81 |   +1/+1 |      82/82 |
| parliament.gov.zm static PDF real DRIFT                             |      0/83 |   0/+1  |       0/84 |
| parliament.gov.zm static PDF truncated_stored_hash_false_drift      |      2/83 |   0/+1  |       2/84 |
| zambialii judgment-akn HTML drift                                   |      3/10 |   +1/+2 |       4/12 |
| Parliament-node landing                                             |       0/1 |     0/0 |        0/1 |
| Stable-PDF combined supercohort (parliament + zambialii source.pdf + media.zambialii legacy) — real-drift basis | 92/95 | +4/+4 | 96/99 § |

§ Stable-PDF supercohort now 96/99 across 26 ticks. The 3 cumulative
  non-matches are all truncated-stored-hash false drifts (b0569 act-zm-2020-014
  → reclassified at b0570 OOB; b0570 act-zm-2020-011; b0578 act-zm-2020-019).
  **Real drift count on the stable-PDF supercohort remains zero across 26 ticks.**

## Notable observations (b0579)

1. **AKN-HTML drift cohort symmetry holds at 82/82 (100% reproduction).**
   Both Act/SI drifts this tick are zambialii.org/akn/... HTML rendering
   URLs — the same drift mechanism observed across all 80 prior AKN-HTML
   observations across 25 prior ticks. No AKN-HTML rendering URL has ever
   matched its stored hash across 26 Phase 8 ticks.

2. **First bare-AKN-path drift variant.** si-zm-2023-041-energy-regulation-general-regulations-2023
   has source_url `https://zambialii.org/akn/zm/act/si/2023/41` with **no
   `/eng@/<date>/` suffix and no `/source.pdf` suffix** — the canonical bare
   AKN identifier path that 302-redirects to the latest English point-in-time
   rendering. This is the first such bare-path drift sampled in 26 Phase 8
   ticks (all prior Act/SI AKN-HTML drifts carried `/eng@/<expression-date>/`
   in the stored URL). The drift mechanism is the same — AKN renders dynamic
   metadata into the HTML body — but the URL form extends the AKN-HTML drift
   cohort beyond its prior shape. No new failure mode; same cohort.

3. **First 2026-vintage record reverified.** judgment-zm-2026-zmcc-07-climate-action-professionals-zambia-v-attorney-gen
   is the first record from calendar year 2026 sampled across 26 Phase 8
   ticks. The drift verdict is consistent with the broader judgment-akn-HTML
   cohort; cohort proportion now 4/12 = 33.3% drift across all observed
   judgment-akn samples (was 3/10 = 30.0% pre-b0579).

4. **Judgment-akn cohort observed second match.** judgment-zm-2019-zmcc-24-mwiya-mutapwe-v-shomeno-dominic
   matched. This is the eighth match across 12 judgment-akn samples observed
   (cumulative 8 match / 4 drift). The match/drift mix on judgment-akn
   continues to be more variable than the (deterministic) Act/SI AKN-HTML
   drift cohort — judgment HTML embeds less time-varying metadata than
   Act/SI HTML pages.

5. **Highest match rate in 26-tick Phase 8 series at 5/8 = 62.5%** (was 3/8
   = 37.5% at b0578; prior peak 7/8 = 87.5% at b0575). Sample distribution
   (3 zambialii /source.pdf matches + 1 parliament PDF match + 1 judgment
   match + 2 AKN-HTML drifts + 1 judgment drift) is broadly representative
   of the pool's stable-PDF / AKN-HTML / judgment-HTML mix.

6. **No truncated-prefix observations this tick.** Cumulative truncated-prefix
   cohort on parliament.gov.zm static PDFs remains 2/84 — both from
   2020-vintage `parliament-pdf-v1.2` parser baseline (act-zm-2020-011 at
   b0570, act-zm-2020-019 at b0578). Operator action recommended (carried
   forward from b0578): one-time backfill sweep to recompute and re-store
   full 64-hex source_hash for any remaining records whose
   `parser_version=parliament-pdf-v1.2` and `source_hash` length is
   `sha256:` + 16 hex.

## Repository state observations

- Pre-existing repo-layout finding (predates b0578): five divergent-content
  duplicate-ID Act records at `records/acts/<year>/<id>.json` AND
  `records/acts/<id>.json` — act-zm-2025-014, act-zm-2025-028, act-zm-2019-010,
  act-zm-2020-010, act-zm-2018-001. None of the b0579 sample IDs are involved
  in this duplication. Pool count `1867` continues to exceed `corpus.sqlite
  records=1864` by these 5 layout duplicates minus 2 (= +3) plus the 2 b0577
  jiw additions (= +5 net surplus over 1862 sqlite-snapshot baseline; the
  judgments_meta count of 174 confirms both ZMCC 2016 jiw additions are in
  sqlite, leaving the 5-ID layout dupe as the only systemic surplus).
- `corpus.sqlite` PRAGMA integrity_check: **ok**. records=1864,
  records_fts=1864, judgments_meta=174. Unchanged from b0578.
- Cross-ref sweep: 0 unresolved amended_by/repealed_by/cited_authorities
  references against canonical id-set.
- `judges_registry.yaml` unchanged.
- `approvals.yaml` unchanged. **Phase 8 remains open-ended (sample_rate
  audit, no completion target).** No completion flip.
- `records/` not modified by this tick (Phase 8 reverify is read-only by
  contract).

## Daily budget (worker-tick channel)

`cumulative_today` (worker-tick before b0579): **89/2000** (4.45%).
b0579 spent 8 fetches. **Post-b0579 cumulative_today (worker-tick):
97/2000 (4.85%).** Well under cap.

## Files written / appended

- `reports/batch-0579-reverify.json` — structured per-record audit
  output (machine-readable; consumed by future cumulative-cohort
  recomputation if the seed register is ever rebuilt).
- `reports/batch-0579.md` — this human-readable report.
- `provenance.log` — appended one line summarising this tick.
- `costs.log` — appended one tick line + one summary JSON line.
- `worker.log` — appended START / body / STOP / push trace.
- `gaps.md` — appended b0579 cohort entry plus reaffirmation of
  pre-existing divergent-duplicate-id observation.

## Files NOT written / mutated

- `records/**/*.json`
- `corpus.sqlite`
- `approvals.yaml`
- `judges_registry.yaml`
- `scripts/batch_0579_phase8_reverify.py` (NOT committed; b0548..b0578
  sandbox-session safety precedent maintained — inline runner lives at
  `/sessions/laughing-cool-thompson/_inline_reverify_b0579.py` outside the
  workspace tree).

## B2 sync

`rclone` not available in sandbox — B2 sync deferred to host (b0563..b0578 precedent).
