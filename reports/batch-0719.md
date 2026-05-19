# Phase 8 — Nightly Re-verification — batch 0719

- **Phase:** `phase_8_nightly_reverify`
- **Worker run id:** `b0719-phase8`
- **Script:** `scripts/batch_0719_phase8_reverify.py` (clone of frozen baseline `scripts/batch_0546_phase8_reverify.py`; only `BATCH` constant and docstring header differ from `scripts/batch_0718_phase8_reverify.py`)
- **Parser version:** `phase8-reverify-0.1.0`
- **Seed:** `phase8-reverify-2026-05-18-b0719`
- **Started:** `2026-05-18T21:33:43Z`
- **Completed:** `2026-05-18T21:34:24Z`
- **Wall clock:** 41s (budget 20min; headroom ~19m19s)
- **Pool size:** 1973 records (records/**/*.json with both `source_url` + `source_hash`) — unchanged from b0718 (no JIW ingestion since b0716-jiw at 19:42:24Z).
- **Sample size:** 8 (`sample_rate 0.01`, capped at `MAX_BATCH=8`)
- **Fetches:** 8 (8× HTTP 200, 0× fetch error)
- **Outcome counts:** match=3, drift=5, fetch_error=0
- **B2 sync:** deferred to host (rclone not in sandbox; Phase 8 is read-only on corpus — no `raw/` mutation)

## Results

| Verdict | Type | ID | Source host | URL kind | Notes |
|---|---|---|---|---|---|
| match | statutory_instrument | si-zm-2026-011-tolls-tom-mtine-toll-plaza-regulations-2026 | zambialii.org | zambialii.org `source.pdf` (`/akn/zm/act/si/2026/11/eng@2026-02-13/source.pdf`) | zambialii.org source.pdf supercohort match (stable PDF) |
| match | statutory_instrument | si-zm-1980-029-income-tax-international-organisations-exemption-approval-order-1980 | zambialii.org | zambialii.org `source.pdf` (`/akn/zm/act/si/1980/29/eng@1980-02-15/source.pdf`) | zambialii.org source.pdf supercohort match (stable PDF) |
| drift | statutory_instrument | si-zm-1985-014-equity-levy-exemption-order-1985 | zambialii.org | AKN bare-path SI (`/akn/zm/act/si/1985/14`) | `zambialii_akn_html_dynamic_render_drift` cohort (bare-AKN-path sub-variant; SI HTML) |
| match | act | act-zm-2007-018-plant-breeders-rights-act-2007 | media.zambialii.org | laws.africa-style `publication-document.pdf` (`/media/legislation/35257/source_file/.../zm-act-2007-18-publication-document.pdf`) | media.zambialii.org publication-document supercohort match (stable PDF) |
| drift | act | act-zm-2018-013-statistics-act-2018 | zambialii.org | AKN-HTML `eng@`-suffixed (`/akn/zm/act/2018/13/eng@2018-12-26`) | `zambialii_akn_html_dynamic_render_drift` cohort (`eng@`-suffixed sub-variant) |
| drift | judgment | judgment-zm-2024-zmsc-03-masautso-banda-v-the-people | zambialii.org | AKN-HTML `eng@`-suffixed (`/akn/zm/judgment/zmsc/2024/3/eng@2024-04-19`) | `zambialii_akn_html_dynamic_render_drift` cohort (`eng@`-suffixed sub-variant; SCZ judgment HTML) |
| drift | statutory_instrument | si-zm-2018-033-electoral-process-local-government-by-elections-election-date-and-time-of-poll-order-2018 | zambialii.org | AKN bare-path SI (`/akn/zm/act/si/2018/33`) | `zambialii_akn_html_dynamic_render_drift` cohort (bare-AKN-path sub-variant; SI HTML) |
| drift | statutory_instrument | si-zm-2023-021-urban-and-regional-planning-development-plans-guidelines-and-exempted-development-classes-regulations-2023 | zambialii.org | AKN bare-path SI (`/akn/zm/act/si/2023/21`) | `zambialii_akn_html_dynamic_render_drift` cohort (bare-AKN-path sub-variant; SI HTML) |

The b0719 sample composition: 2/8 zambialii.org `source.pdf` SIs, 1/8 media.zambialii.org `publication-document.pdf` Act, 1/8 zambialii.org AKN-HTML `eng@`-suffixed Act, 1/8 zambialii.org AKN-HTML `eng@`-suffixed SCZ judgment, and 3/8 zambialii.org AKN bare-path SIs. The 2 zambialii.org `source.pdf` SIs matched (zambialii source.pdf supercohort behaviour). The 1 media.zambialii.org `publication-document.pdf` Act matched (publication-document supercohort behaviour). All 5 zambialii.org AKN-HTML records (2 `eng@`-suffixed + 3 bare-path) drifted (`zambialii_akn_html_dynamic_render_drift` cohort — known server-rendered timestamp / asset cache-busting behaviour; not substantive legal-text change). No fetch errors this tick.

Notably, `act-zm-2018-013-statistics-act-2018` and `judgment-zm-2024-zmsc-03-masautso-banda-v-the-people` are repeat-draws from b0718 (the seed is per-batch, not global; collisions are expected at ~0.4% per record per tick). Both drifted with new sha256 values in this tick as in b0718, which is consistent with the dynamic-render cohort — re-renders are not stable across observations.

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
| 7 | robots.txt respected; per-host rate limits honoured (zambialii.org min_gap ≥ 5s; media.zambialii.org min_gap ≥ 5s; deterministic `sleep_for_host` mechanism unchanged from baseline) | PASS |
| 8 | User-Agent honest: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` | PASS |
| 9 | corpus.sqlite live `quick_check=ok integrity_check=ok records=1970 records_fts=1970 dup_ids=0` (FTS parity with records table preserved across tick) | PASS |

All 9 checks PASS — tick commits via normal path.

### Pre-existing disk-state observation (NOT a new failure; not introduced by this tick)

A read-only audit confirms the on-disk `records/**/*.json` filesystem retains the documented pre-existing state: 11 record files missing the `id` JSON field and 5 duplicate-ID pairs (same `id` exists at both `records/acts/{id}.json` and `records/acts/{year}/{id}.json` paths). None of those records are in this tick's sample. `corpus.sqlite` is the source of truth and reports `records=1970, dup_ids=0`. This pre-existing state predates Phase 8 b0719 and is unchanged by this tick (Phase 8 is read-only on records). Carried-forward operator-triage item.

## Cost / budget

- Network fetches this tick: 8 (8× HTTP 200, 0× fetch error)
- Cumulative daily fetches across all workers today (per costs.log fetches= sum): ~437 pre-tick; + 8 (this tick) = ~445 of 2000 daily budget. Plenty of headroom.
- Tokens consumed: 0 (deterministic pipeline, no LLM calls). LLM budget 0/1,000,000 today.
- Bandwidth: 5,538,412 B total (dominated by 4,876,293 B `act-zm-2007-018-plant-breeders-rights-act-2007` publication PDF from media.zambialii.org).
- Wall clock: 41s (budget 20min; headroom ~19m19s).

## B2 sync

Deferred to host — rclone not available in sandbox. Phase 8 is read-only on corpus (no `raw/` mutation) so deferral is acceptable per BRIEF.md §8.

## Repo-state note

Working tree at tick start carried pre-existing-staged residue from prior sessions (same FUSE/index situation worked around by b0716–b0718). Phase 8's own commit is scoped strictly to this tick's deliverables (new script + new reports + own log/costs/provenance appends) via the documented `GIT_INDEX_FILE` + `git read-tree HEAD` + scoped `git add` + `git commit-tree` + `git update-ref` bypass.

## Next tick

Routine Phase 8 sampling continues. No new audit-trail items this tick. 5 drifts fall under the pre-existing `zambialii_akn_html_dynamic_render_drift` cohort (2 `eng@`-suffixed + 3 bare-AKN-path sub-variant). Pre-existing carry-forwards remain:

- `judgment-zm-2024-coa-024-kingfred-phiri-v-life-master-ltd` 404 (b0717 — still single observation; audit-only).
- `judgment-zm-2025-zmcc-14` canonical-URL-date variant 404 (b0700 — audit-only; remediation requires explicit Peter approval).
- Existing 15 `parliament-pdf-v1.2` truncated-16hex defect records remain an open operator-triage item (latent — not drawn this tick).
- Pre-existing on-disk JSON state (11 no-`id` files + 5 duplicate-ID pairs) — operator-triage item.
