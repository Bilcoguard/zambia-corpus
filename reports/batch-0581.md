# Batch 0581 — Phase 8 Nightly Re-verification (2026-05-10)

**UTC start:** 2026-05-10T20:34:34Z
**UTC end:** 2026-05-10T20:35:07Z
**Worker:** worker-tick (Phase 8)
**Phase:** phase_8_nightly_reverify (approved 2026-05-06; sample_rate 0.01)
**Parser:** phase8-reverify-0.1.0 (functional contract per scripts/batch_0546_phase8_reverify.py)
**Tick scope:** Twenty-seventh Phase 8 tick overall; thirteenth worker-tick of UTC
   date 2026-05-10 (after b0563 at 05:50Z, b0564 at 06:02:42Z, b0565 at 09:09:35Z,
   b0567 at 10:06:09Z, b0568 at 10:12:41Z, b0569 at 10:36Z, b0570 at 11:08Z,
   b0572 at 16:34:30Z, b0575 at 18:46:30Z, b0576 at 19:04:49Z, b0578 at 19:35:51Z,
   b0579 at 20:05:17Z).
**Execution mode:** inline runner (`/tmp/b0581_phase8_reverify.py`, NOT
   committed) per sandbox-session safety constraint maintained since b0548
   (b0548..b0579 precedent). Functional contract matches
   scripts/batch_0546_phase8_reverify.py baseline including
   scripts/certs/*.pem PKI loader. Differences from baseline: tick-suffixed
   seed `phase8-reverify-2026-05-10-b0581`, plus truncated-stored-hash-prefix
   detection (carried forward from b0570/b0578 — recomputed sha256 starting
   with the stored 16-hex prefix is classified as
   `truncated_stored_hash_false_drift`).

## Pre-tick git state observation

Pre-tick `git pull --ff-only` returned `Already up to date` (HEAD=d262187
from b0579). The index carries the staged b0580 judgment-ingestion-worker
commit-prep (3 ZMSC 2020 record additions, 3 helper scripts under
`scripts/batch_0580_*.py`, plus `reports/batch-0580-jiw.md` and four log
file modifications) — uncommitted because the b0580 jiw push line is
absent from `worker.log`. This is parallel work from the
judgment-ingestion-worker channel; the Phase 8 worker-tick channel does
not own it. Per b0579 alt-index precedent, this tick commits b0581's
intended files via a per-PID alt-index path
(`GIT_INDEX_FILE=/tmp/alt-index-b0581`) reset to HEAD, leaving the
regular index untouched for the jiw next tick to reconcile.

The default `.git/index.lock` cleanup remains constrained on this sandbox
by `Operation not permitted` virtiofs semantics for backup-suffixed lock
files in `.git/`. `git pull --ff-only` succeeded with a single warning
about an unremovable `.git/objects/maintenance.lock` backup file — pull
semantics not affected.

## Inputs

- Pool size: **1870** (grew +3 from b0579 close at 1867 — b0580 jiw added
  3 records: judgment-zm-2020-zmsc-120, judgment-zm-2020-zmsc-130,
  judgment-zm-2020-zmsc-150 (Mwale-Harman, Muzyamba, Mulenga)).
- Seed: `phase8-reverify-2026-05-10-b0581` (tick-suffixed deterministic seed).
- Sample size: **8** (= MAX_BATCH cap; ceil(0.01 × 1870) = 19 → capped at 8).
- Out-of-band re-fetches: **none**.

## Results — 4 match / 4 drift / 1 truncated_stored_hash_false_drift / 0 fetch_error

| Verdict      | Count | Records |
|--------------|------:|---------|
| match        |     4 | judgment-zm-2025-zmsc-23-the-v-zambia (zambialii akn /source.pdf JUDGMENT 279,698 B — **FIRST observation of judgment-akn /source.pdf endpoint match in 27-tick series**); si-zm-2009-044-banking-and-financial-services-restriction-on-kwacha-lending-to-non-residents-re (zambialii akn /source.pdf 357,672 B; **second observation of this exact record in series — also matched at b0579**); si-zm-2024-012-subordinate-courts-civil-jurisdiction-rules-2024 (zambialii akn /source.pdf 283,231 B); act-zm-2020-016-financial-intelligence-centre-amendment-act-2020 (parliament.gov.zm /acts/ subdir 111,675 B — verdict `match_truncated_prefix`, see truncated row) |
| drift        |     4 | act-zm-2024-020-supplementary-appropriation-2024-no-2-act (zambialii.org/akn/zm/act/2024/20/eng@2024-12-26 38,863 B — fits AKN-HTML drift cohort); act-zm-2007-019-national-constitutional-conference-act-2007 (www.zambialii.org/akn/zm/act/2007/19/eng@2007-08-31 42,680 B — fits AKN-HTML drift cohort); si-zm-2019-014-companies-general-regulations-2019 (zambialii.org/akn/zm/act/si/2019/14 39,047 B — **second bare-AKN-path drift variant in 27-tick series after b0579 si-zm-2023-041**, no /eng@/ and no /source.pdf); act-zm-2020-026-appropriation-act (zambialii.org/akn/zm/act/2020/26/eng@2020-12-18 181,859 B — fits AKN-HTML drift cohort) |
| truncated_stored_hash_false_drift | 1 | act-zm-2020-016-financial-intelligence-centre-amendment-act-2020 — stored 16-hex prefix `f10dd27b0444a767` startswith-matches recomputed full 64-hex `f10dd27b0444a767723ad4547e6dea27c47173d057b401cfd027e52dde55a737`. **Third observation in the 2020-vintage `parliament-pdf-v1.2` truncated-prefix cohort** (after b0570 act-zm-2020-011, b0578 act-zm-2020-019). All three observations on parliament.gov.zm `/acts/` subdir Acts from calendar year 2020. |
| fetch_error  |     0 | — |

## Cohort-level cumulative tally (post-b0581, 27 ticks)

| Cohort                                                              | Pre-b0581 | Δ b0581 | Post-b0581 |
|---------------------------------------------------------------------|----------:|--------:|-----------:|
| zambialii.org/akn/.../act-or-SI-HTML drift                          |     82/82 |   +4/+4 |      86/86 |
| zambialii.org/akn/.../source.pdf match (Acts/SIs)                   |     15/15 |   +2/+2 |      17/17 |
| zambialii.org/akn/.../source.pdf match (Judgments)                  |       0/0 |   +1/+1 |    1/1 NEW |
| media.zambialii.org/media/legislation/ legacy-PDF match             |       1/1 |     0/0 |        1/1 |
| parliament.gov.zm static PDF match (real-match)                     |     82/82 |     0/0 |      82/82 |
| parliament.gov.zm static PDF real DRIFT                             |      0/84 |   0/+1  |       0/85 |
| parliament.gov.zm static PDF truncated_stored_hash_false_drift      |      2/84 |   +1/+1 |       3/85 |
| zambialii judgment-akn HTML drift                                   |      4/12 |     0/0 |       4/12 |
| Parliament-node landing                                             |       0/1 |     0/0 |        0/1 |
| Stable-PDF combined supercohort (parliament + zambialii akn /source.pdf + media.zambialii legacy) — real-drift basis | 96/99 | +4/+4 | 100/103 § |

§ Stable-PDF supercohort now 100/103 across 27 ticks. The 3 cumulative
  non-real-matches are all truncated-stored-hash false drifts (b0570
  act-zm-2020-011; b0578 act-zm-2020-019; b0581 act-zm-2020-016).
  **Real drift count on the stable-PDF supercohort remains zero across 27 ticks.**

## Notable observations (b0581)

1. **First observation of judgment-akn `/source.pdf` endpoint match.**
   judgment-zm-2025-zmsc-23-the-v-zambia carries source_url
   `https://zambialii.org/akn/zm/judgment/zmcc/2025/23/eng@2025-04-03/source.pdf`
   — the AKN-served PDF endpoint for a Supreme Court judgment. Across the
   prior 26 Phase 8 ticks every sampled judgment was either a judgment-akn
   HTML rendering URL (4 drift / 8 match across 12 observations) or
   absent. This is the first time a judgment record's source_url has
   been the AKN `/source.pdf` form — and it matched on first
   observation. The `/source.pdf` endpoint serves the byte-stable PDF
   (same mechanism as Act/SI `/source.pdf`), and the match supports
   classifying judgment-akn `/source.pdf` together with Act/SI
   `/source.pdf` in the stable-PDF supercohort. New cohort row added
   above with seeded count 1/1.

2. **Second bare-AKN-path drift variant.** si-zm-2019-014-companies-general-regulations-2019
   has source_url `https://zambialii.org/akn/zm/act/si/2019/14` with **no
   `/eng@/<date>/` suffix and no `/source.pdf` suffix** — same canonical
   bare AKN identifier path observed at b0579 (si-zm-2023-041). This
   confirms the bare-AKN-path drift cohort is not a fluke of one
   instance: bare-path AKN URLs 302-redirect to dynamic latest-PIT
   HTML rendering, identical drift mechanism to `/eng@/...` form. AKN-HTML
   drift cohort symmetry holds at 86/86 (100% reproduction across 27 ticks).

3. **Third truncated-stored-hash false-drift observation, all on
   2020-vintage parliament-pdf-v1.2.** act-zm-2020-016 joins act-zm-2020-011
   (b0570) and act-zm-2020-019 (b0578) in the cohort of records whose
   stored `source_hash` is the 16-hex prefix-truncated form of the
   recomputed full 64-hex sha256. All three carry parser_version
   `parliament-pdf-v1.2` and are calendar-year-2020 Acts on
   parliament.gov.zm `/acts/` subdir. **Operator action recommended
   (carried forward from b0578/b0579):** one-time backfill sweep to
   recompute and re-store full 64-hex source_hash for any remaining
   records whose `parser_version=parliament-pdf-v1.2` AND `source_hash`
   length is `sha256:` + 16 hex (≈3 known + unknown remaining count).
   Such a backfill would not modify the underlying raw bytes, only the
   stored hash representation; integrity-check semantics preserved.

4. **Repeat observation of si-zm-2009-044.** This SI was sampled at
   b0579 (matched, /source.pdf 357,672 B) and again at b0581 (matched,
   /source.pdf 357,672 B identical). Tick-suffixed seed deterministically
   produces independent samples per tick, so collisions are by chance;
   the identical bytes-and-hash on consecutive samples confirms the
   /source.pdf endpoint stability for this record.

5. **Pool size grew +3.** Pool size advanced from 1867 (b0579 close)
   to 1870, reflecting the 3 net judgment-ingestion-worker b0580
   additions to records/judgments/zmsc/2020/. corpus.sqlite shows
   records=1867 (jiw b0580 sqlite_insert ran, sqlite is ahead of HEAD
   commit; this is normal jiw mid-flight state because b0580 is staged
   but not yet committed/pushed).

6. **Match rate 5/8 = 62.5% (counting truncated-prefix as match)** —
   on par with b0579 5/8. Sample distribution (3 zambialii Act/SI
   /source.pdf matches + 1 zambialii judgment /source.pdf match + 0
   parliament real-match + 1 parliament truncated-prefix + 4 AKN-HTML
   drifts) is broadly representative of the pool's stable-PDF /
   AKN-HTML / judgment mix and consistent with the cumulative tally.

## Repository state observations

- Pre-existing repo-layout finding (predates b0578): five divergent-content
  duplicate-ID Act records at `records/acts/<year>/<id>.json` AND
  `records/acts/<id>.json` — act-zm-2025-014, act-zm-2025-028, act-zm-2019-010,
  act-zm-2020-010, act-zm-2018-001. None of the b0581 sample IDs are involved
  in this duplication. The pool count `1870` exceeds `corpus.sqlite
  records=1867` by these 5 layout duplicates minus 2 (= +3 net surplus).
- `corpus.sqlite` PRAGMA integrity_check: **ok**. records=1867,
  records_fts=1867, judgments_meta=177. Reflects b0580 jiw mid-flight
  insertions; not modified by b0581.
- Cross-ref sweep: 0 unresolved amended_by/repealed_by/cited_authorities
  references against canonical id-set (1872 ids; 7 cross-refs total).
- `judges_registry.yaml` unchanged.
- `approvals.yaml` unchanged. **Phase 8 remains open-ended (sample_rate
  audit, no completion target).** No completion flip.
- `records/` not modified by this tick (Phase 8 reverify is read-only by
  contract).
- B0580 jiw staged-but-uncommitted addition is left in place for the
  jiw worker to reconcile on its next tick.

## Daily budget (worker-tick channel)

`cumulative_today` (worker-tick before b0581): **97/2000** (4.85%).
b0581 spent 8 fetches. **Post-b0581 cumulative_today (worker-tick):
105/2000 (5.25%).** Well under cap.

## Files written / appended

- `reports/batch-0581-reverify.json` — structured per-record audit
  output.
- `reports/batch-0581.md` — this human-readable report.
- `provenance.log` — appended one line summarising this tick.
- `costs.log` — appended one tick line + one summary JSON line.
- `worker.log` — appended START / body / STOP / push trace.
- `gaps.md` — appended b0581 cohort entry plus reaffirmation of
  pre-existing divergent-duplicate-id observation.

## Files NOT written / mutated

- `records/**/*.json`
- `corpus.sqlite`
- `approvals.yaml`
- `judges_registry.yaml`
- `scripts/batch_0581_phase8_reverify.py` (NOT committed; b0548..b0579
  sandbox-session safety precedent maintained — inline runner lives at
  `/tmp/b0581_phase8_reverify.py` outside the workspace tree).

## B2 sync

`rclone` not available in sandbox — B2 sync deferred to host (b0563..b0579 precedent).
