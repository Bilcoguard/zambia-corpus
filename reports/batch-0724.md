# Phase 8 — Nightly Re-verification — batch 0724

- **Phase:** `phase_8_nightly_reverify`
- **Worker run id:** `b0724-phase8`
- **Script:** `scripts/batch_0724_phase8_reverify.py` (clone of frozen baseline `scripts/batch_0546_phase8_reverify.py`; only `BATCH` constant changed from `scripts/batch_0719_phase8_reverify.py`, the immediately prior Phase 8 tick — b0720/b0721 were repair-idle and b0722 was a JIW tick, so b0724 picks up the next Phase 8 slot after b0723 was consumed by a concurrent JIW worker)
- **Parser version:** `phase8-reverify-0.1.0`
- **Seed:** `phase8-reverify-2026-05-19-b0724`
- **Started:** `2026-05-19T07:39:14Z`
- **Completed:** `2026-05-19T07:39:50Z`
- **Wall clock:** 36s (budget 20min; headroom ~19m24s)
- **Pool size:** 1982 records (records/**/*.json with both `source_url` + `source_hash`) — pool grew by +9 since b0719 (1973 → 1982) consistent with intervening b0716-jiw / b0722-jiw insertions and a small set of files surfacing through re-parse since the prior Phase 8 tick.
- **Sample size:** 8 (`sample_rate 0.01`, capped at `MAX_BATCH=8`)
- **Fetches:** 8 (8× HTTP 200, 0× fetch error)
- **Outcome counts:** match=3, drift=5, fetch_error=0
- **B2 sync:** deferred to host (rclone not in sandbox; Phase 8 is read-only on corpus — no `raw/` mutation)

## Results

| Verdict | Type | ID | Source host | URL kind | Notes |
|---|---|---|---|---|---|
| match | act | act-zm-2011-011-day-nurseries-repeal-act-2011 | www.parliament.gov.zm | parliament.gov.zm `documents/acts/*.pdf` | parliament.gov.zm acts-PDF supercohort match (stable PDF) |
| drift | statutory_instrument | si-zm-2020-004-electoral-process-local-government-by-elections-election-date-and-time-of-poll-no-2-order-2020 | zambialii.org | AKN bare-path SI (`/akn/zm/act/si/2020/4`) | `zambialii_akn_html_dynamic_render_drift` cohort (bare-AKN-path sub-variant; SI HTML) |
| match | si | si-zm-1981-049-income-tax-foreign-organisations-exemption-approval-order-1981 | zambialii.org | zambialii.org `source.pdf` (`/akn/zm/act/si/1981/49/eng@1981-03-27/source.pdf`) | zambialii.org source.pdf supercohort match (stable PDF) |
| drift | judgment | judgment-zm-2022-zmsc-58-luboni-simunga-v-the-people | zambialii.org | AKN-HTML `eng@`-suffixed (`/akn/zm/judgment/zmsc/2022/58/eng@2022-08-31`) | `zambialii_akn_html_dynamic_render_drift` cohort (`eng@`-suffixed sub-variant; SCZ judgment HTML) |
| drift | act | act-zm-1985-008-excess-expenditure-appropriation-1982-act-1985 | zambialii.org | AKN-HTML `eng@`-suffixed (`/akn/zm/act/1985/8/eng@1985-04-12`) | `zambialii_akn_html_dynamic_render_drift` cohort (`eng@`-suffixed sub-variant; Act HTML) |
| match | act | act-zm-2013-003-the-medicines-and-allied-substances-2013 | www.parliament.gov.zm | parliament.gov.zm `documents/acts/*.pdf` | parliament.gov.zm acts-PDF supercohort match (stable PDF) |
| drift | statutory_instrument | si-zm-2016-043-zambia-wildlife-export-prohibition-order-2016 | zambialii.org | AKN bare-path SI (`/akn/zm/act/si/2016/43`) | `zambialii_akn_html_dynamic_render_drift` cohort (bare-AKN-path sub-variant; SI HTML) |
| drift | act | act-zm-1968-034-loans-kafue-gorge-hydro-electric-power-project-act-1968 | zambialii.org | AKN-HTML `eng@`-suffixed (`/akn/zm/act/1968/34/eng@1996-12-31`) | `zambialii_akn_html_dynamic_render_drift` cohort (`eng@`-suffixed sub-variant; Act HTML) |

The b0724 sample composition: 2/8 `parliament.gov.zm/documents/acts/*.pdf` Acts, 1/8 zambialii.org `source.pdf` SI, 3/8 zambialii.org AKN-HTML `eng@`-suffixed records (1 SCZ judgment + 2 Acts), and 2/8 zambialii.org AKN bare-path SIs. All 3 stable-PDF cohort records matched (`parliament.gov.zm` acts-PDF supercohort ×2 + zambialii.org `source.pdf` supercohort ×1). All 5 zambialii.org AKN-HTML records drifted (`zambialii_akn_html_dynamic_render_drift` cohort — known server-rendered timestamp / asset cache-busting behaviour; not substantive legal-text change). No fetch errors this tick.

No repeat-draws this tick (seed is per-batch, not global; collisions are statistically expected at ~0.4% per record per tick but the eight IDs in b0724 do not appear in the b0723-cohort phase8 slot — b0723 was a JIW tick — nor in b0719's sample).

### Carry-forward audit-trail items

- `judgment-zm-2024-coa-024-kingfred-phiri-v-life-master-ltd` 404 (first observed b0717 at 20:33:55Z, single observation to date). NOT in this tick's sample — no new observation; record remains under audit-only watch pending independent corroboration in subsequent Phase 8 sweeps.
- `judgment-zm-2025-zmcc-14` canonical-URL-date variant 404 (b0700 — audit-only; remediation requires explicit Peter approval) — NOT in this tick's sample.

## Integrity checks

| # | Check | Result |
|---|---|---|
| 1 | JSON report well-formed; match+drift+fetch_error == sample_size (3+5+0=8) | PASS |
| 2 | No duplicate IDs in sample (8 unique) | PASS |
| 3 | Every stored + fetched sha256 is a valid 64-hex sha256 | PASS |
| 4 | Every sampled record's `stored_sha256` matches the on-disk record's `source_hash` (proper `sha256:` prefix-stripping) | PASS (no record file mutated this tick) |
| 5 | No tracked record file modified by this run (`git diff --name-only records/` empty) | PASS (script never opens records/ for write — source-verified) |
| 6 | `corpus.sqlite` NOT touched; `approvals.yaml` NOT modified (`git status --porcelain corpus.sqlite approvals.yaml` empty) | PASS |
| 7 | robots.txt respected; per-host rate limits honoured (zambialii.org min_gap ≥ 5s; www.parliament.gov.zm min_gap ≥ 2s default; deterministic `sleep_for_host` mechanism unchanged from baseline) | PASS |
| 8 | User-Agent honest: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` | PASS |
| 9 | corpus.sqlite live `quick_check=ok records=1978 records_fts=1978 dup_ids=0` (FTS parity with records table preserved across tick) | PASS |

All 9 checks PASS — tick commits via normal path.

### Pre-existing disk-state observation (NOT a new failure; not introduced by this tick)

A read-only audit confirms the on-disk `records/**/*.json` filesystem retains the documented pre-existing state (`records=1978` in `corpus.sqlite` vs `1982` JSON files on disk reflecting 11 record files missing the `id` JSON field and 5 duplicate-ID pairs at `records/acts/{id}.json` and `records/acts/{year}/{id}.json` paths plus minor recent JIW spool). None of those records are in this tick's sample. `corpus.sqlite` is the source of truth and reports `records=1978, dup_ids=0`. This pre-existing state predates Phase 8 b0724 and is unchanged by this tick (Phase 8 is read-only on records). Carried-forward operator-triage item.

## Cost / budget

- Network fetches this tick: 8 (8× HTTP 200, 0× fetch error)
- Cumulative daily fetches across all workers today (per costs.log fetches= sum): ~0 phase8 + 0 JIW so far on 2026-05-19 (b0722-jiw was a zero-fetch reparse tick); + 8 (this tick) = ~8 of 2000 daily budget. Massive headroom.
- Tokens consumed: 0 (deterministic pipeline, no LLM calls). LLM budget 0/1,000,000 today.
- Bandwidth: 820,714 B total across 8 fetches (acts-PDF 2× from parliament.gov.zm at 359,934 B + 107,456 B; source.pdf 1× from zambialii.org at 146,185 B; AKN-HTML 5× from zambialii.org at 38,991 + 43,273 + 38,646 + 38,976 + 47,253 B).
- Wall clock: 36s (budget 20min; headroom ~19m24s).

## B2 sync

Deferred to host — rclone not available in sandbox. Phase 8 is read-only on corpus (no `raw/` mutation) so deferral is acceptable per BRIEF.md §8.

## Repo-state note

Working tree at tick start carried pre-existing untracked / cross-session FUSE residue (consistent with prior Phase 8 ticks). Three stale git locks (`.git/index.lock`, `.git/objects/maintenance.lock`, `.git/ORIG_HEAD.lock`) were renamed (not deleted — FUSE EPERM) to `*.lock.b0724-stale-<ns>.bak` per the documented bypass pattern before `git pull --ff-only` succeeded ("Already up to date."). Phase 8's own commit is scoped strictly to this tick's deliverables (new script + new reports + own log/costs/provenance + gaps.md appends).

## Next tick

Routine Phase 8 sampling continues. No new audit-trail items this tick. 5 drifts fall under the pre-existing `zambialii_akn_html_dynamic_render_drift` cohort (3 `eng@`-suffixed + 2 bare-AKN-path sub-variant). Pre-existing carry-forwards remain:

- `judgment-zm-2024-coa-024-kingfred-phiri-v-life-master-ltd` 404 (b0717 — still single observation; audit-only).
- `judgment-zm-2025-zmcc-14` canonical-URL-date variant 404 (b0700 — audit-only; remediation requires explicit Peter approval).
