# Phase 8 — Nightly Re-verification — batch 0718

- **Phase:** `phase_8_nightly_reverify`
- **Worker run id:** `b0718-phase8`
- **Script:** `scripts/batch_0718_phase8_reverify.py` (clone of frozen baseline `scripts/batch_0546_phase8_reverify.py`; only `BATCH` constant and docstring header differ from `scripts/batch_0717_phase8_reverify.py`)
- **Parser version:** `phase8-reverify-0.1.0`
- **Seed:** `phase8-reverify-2026-05-18-b0718`
- **Started:** `2026-05-18T21:03:57Z`
- **Completed:** `2026-05-18T21:04:52Z`
- **Wall clock:** 55s (budget 20min; headroom ~19m05s)
- **Pool size:** 1973 records (records/**/*.json with both `source_url` + `source_hash`) — unchanged from b0717 (no JIW ingestion since b0716-jiw at 19:42:24Z).
- **Sample size:** 8 (`sample_rate 0.01`, capped at `MAX_BATCH=8`)
- **Fetches:** 8 (8× HTTP 200, 0× fetch error)
- **Outcome counts:** match=3, drift=5, fetch_error=0
- **B2 sync:** deferred to host (rclone not in sandbox; Phase 8 is read-only on corpus — no `raw/` mutation)

## Results

| Verdict | Type | ID | Source host | URL kind | Notes |
|---|---|---|---|---|---|
| drift | judgment | judgment-zm-2024-zmsc-03-masautso-banda-v-the-people | zambialii.org | AKN-HTML `eng@`-suffixed (`/akn/zm/judgment/zmsc/2024/3/eng@2024-04-19`) | `zambialii_akn_html_dynamic_render_drift` cohort (`eng@`-suffixed sub-variant; SCZ judgment HTML) |
| drift | act | act-zm-2018-013-statistics-act-2018 | zambialii.org | AKN-HTML `eng@`-suffixed (`/akn/zm/act/2018/13/eng@2018-12-26`) | `zambialii_akn_html_dynamic_render_drift` cohort (`eng@`-suffixed sub-variant) |
| drift | judgment | judgment-zm-2025-zmcc-11-ford-chombo-v-the-attorney-general | zambialii.org | AKN-HTML `eng@`-suffixed (`/akn/zm/judgment/zmcc/2025/11/eng@2025-06-19`) | `zambialii_akn_html_dynamic_render_drift` cohort (`eng@`-suffixed sub-variant; ZMCC judgment HTML) |
| drift | act | act-zm-1969-036-state-security-act-1969 | zambialii.org | AKN-HTML `eng@`-suffixed (`/akn/zm/act/1969/36/eng@1996-12-31`) | `zambialii_akn_html_dynamic_render_drift` cohort (`eng@`-suffixed sub-variant) |
| match | statutory_instrument | local-courts-rules-1966 | commons.laws.africa | laws.africa `publication-document.pdf` (`/akn/zm/act/si/1966/293/media/publication/zm-act-si-1966-293-publication-document.pdf`) | laws.africa publication-document supercohort match (stable PDF) |
| match | act | act-zm-2023-024-access-to-information-act-2023 | zambialii.org | zambialii.org `source.pdf` (`/akn/zm/act/2023/24/eng@2023-12-26/source.pdf`) | zambialii.org source.pdf supercohort match |
| match | act | act-zm-2010-013-disaster-management-2010 | www.parliament.gov.zm | parliament.gov.zm Act PDF | stable-PDF supercohort match |
| drift | statutory_instrument | si-zm-2019-040-corporate-insolvency-insolvency-practitioner-accreditation-regulations-2019 | zambialii.org | AKN bare-path SI (`/akn/zm/act/si/2019/40`) | `zambialii_akn_html_dynamic_render_drift` cohort (bare-AKN-path sub-variant; SI HTML) |

The b0718 sample composition: 1/8 parliament.gov.zm Act PDF, 1/8 zambialii.org `source.pdf`, 1/8 commons.laws.africa publication-document PDF, 4/8 zambialii.org AKN-HTML `eng@`-suffixed (2 Acts + 1 SCZ judgment + 1 ZMCC judgment), and 1/8 zambialii.org AKN bare-path SI HTML. The 1 parliament.gov.zm PDF matched (stable-PDF supercohort behaviour). The 1 zambialii.org `source.pdf` matched (zambialii source.pdf supercohort behaviour). The 1 commons.laws.africa `publication-document.pdf` matched (laws.africa publication-document supercohort behaviour). All 5 zambialii.org AKN-HTML records (4 `eng@`-suffixed + 1 bare-path) drifted (`zambialii_akn_html_dynamic_render_drift` cohort — known server-rendered timestamp / asset cache-busting behaviour; not substantive legal-text change). No fetch errors this tick.

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
| 7 | robots.txt respected; per-host rate limits honoured (zambialii.org min_gap ≥ 5s; commons.laws.africa min_gap ≥ 5s; deterministic `sleep_for_host` mechanism unchanged from baseline) | PASS |
| 8 | User-Agent honest: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` | PASS |
| 9 | corpus.sqlite live `quick_check=ok records=1970 records_fts=1970 dup_ids=0` (FTS parity with records table preserved across tick) | PASS |

All 9 checks PASS — tick commits via normal path.

### Pre-existing disk-state observation (NOT a new failure; not introduced by this tick)

A read-only audit confirms the on-disk `records/**/*.json` filesystem retains the documented pre-existing state: 11 record files missing the `id` JSON field and 5 duplicate-ID pairs (same `id` exists at both `records/acts/{id}.json` and `records/acts/{year}/{id}.json` paths). None of those records are in this tick's sample. `corpus.sqlite` is the source of truth and reports `records=1970, dup_ids=0`. This pre-existing state predates Phase 8 b0718 and is unchanged by this tick (Phase 8 is read-only on records). Carried-forward operator-triage item.

## Cost / budget

- Network fetches this tick: 8 (8× HTTP 200, 0× fetch error)
- Cumulative daily fetches across all workers today (per costs.log fetches= sum): ~429 pre-tick; + 8 (this tick) = ~437 of 2000 daily budget. Plenty of headroom.
- Tokens consumed: 0 (deterministic pipeline, no LLM calls). LLM budget 0/1,000,000 today.
- Bandwidth: 11,862,325 B total (dominated by 10,520,091 B `local-courts-rules-1966` publication PDF from commons.laws.africa).
- Wall clock: 55s (budget 20min; headroom ~19m05s).

## B2 sync

Deferred to host — rclone not available in sandbox. Phase 8 is read-only on corpus (no `raw/` mutation) so deferral is acceptable per BRIEF.md §8.

## Repo-state note

Working tree at tick start carried pre-existing-staged residue from prior sessions (8 ZMCC judgment JSONs already on disk from b0716-jiw; deleted-in-index reverify reports for batches 0715–0717; etc.) — this is the same FUSE/index situation worked around by b0716-phase8 and b0717-phase8. Phase 8's own commit is scoped strictly to this tick's deliverables (new script + new reports + own log/costs/provenance appends) via the documented `GIT_INDEX_FILE` + `git read-tree HEAD` + scoped `git add` + `git commit-tree` + `git update-ref` bypass.

## Next tick

Routine Phase 8 sampling continues. No new audit-trail items this tick. 5 drifts fall under the pre-existing `zambialii_akn_html_dynamic_render_drift` cohort (4 `eng@`-suffixed + 1 bare-AKN-path sub-variant). Pre-existing carry-forwards remain:

- `judgment-zm-2024-coa-024-kingfred-phiri-v-life-master-ltd` 404 (b0717 — still single observation; audit-only).
- `judgment-zm-2025-zmcc-14` canonical-URL-date variant 404 (b0700 — audit-only; remediation requires explicit Peter approval).
- Existing 15 `parliament-pdf-v1.2` truncated-16hex defect records remain an open operator-triage item (latent — not drawn this tick).
- Pre-existing on-disk JSON state (11 no-`id` files + 5 duplicate-ID pairs) — operator-triage item.
