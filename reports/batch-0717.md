# Phase 8 — Nightly Re-verification — batch 0717

- **Phase:** `phase_8_nightly_reverify`
- **Worker run id:** `b0717-phase8`
- **Script:** `scripts/batch_0717_phase8_reverify.py` (clone of frozen baseline `scripts/batch_0546_phase8_reverify.py`; only `BATCH` constant and docstring header differ from `scripts/batch_0716_phase8_reverify.py`)
- **Parser version:** `phase8-reverify-0.1.0`
- **Seed:** `phase8-reverify-2026-05-18-b0717`
- **Started:** `2026-05-18T20:33:21Z`
- **Completed:** `2026-05-18T20:33:55Z`
- **Wall clock:** 34s (budget 20min; headroom ~19m26s)
- **Pool size:** 1973 records (records/**/*.json with both `source_url` + `source_hash`) — unchanged from b0716 (no JIW ingestion since b0716-jiw at 19:42:24Z).
- **Sample size:** 8 (`sample_rate 0.01`, capped at `MAX_BATCH=8`)
- **Fetches:** 8 (7× HTTP 200, 1× HTTP 404)
- **Outcome counts:** match=2, drift=5, fetch_error=1
- **B2 sync:** deferred to host (rclone not in sandbox; Phase 8 is read-only on corpus — no `raw/` mutation)

## Results

| Verdict | Type | ID | Source host | URL kind | Notes |
|---|---|---|---|---|---|
| drift | si | si-zm-2019-022-citizens-economic-empowerment-reservation-scheme-regulations-2019 | zambialii.org | AKN landing/bare-path HTML (`/akn/zm/act/si/2019/22`) | `zambialii_akn_html_dynamic_render_drift` cohort (bare-path sub-variant; SI-HTML) |
| match | si | si-zm-2019-056-national-heritage-conservation-commission-broken-hill-man-national-monument-decl | zambialii.org | zambialii.org `source.pdf` (`/akn/zm/act/si/2019/56/eng@2019-09-06/source.pdf`) | zambialii.org source.pdf supercohort match |
| drift | act | act-zm-1995-009-preferential-claims-in-bankruptcy-act-1995 | zambialii.org | AKN-HTML `eng@`-suffixed (`/akn/zm/act/1995/9/eng@1996-12-31`) | `zambialii_akn_html_dynamic_render_drift` cohort (`eng@`-suffixed sub-variant) |
| drift | act | act-zm-1963-033-occupiers-liability-act-1963 | zambialii.org | AKN-HTML `eng@`-suffixed (`/akn/zm/act/1963/33/eng@1996-12-31`) | `zambialii_akn_html_dynamic_render_drift` cohort (`eng@`-suffixed sub-variant) |
| drift | act | act-zm-1971-032-home-guard-act-1971 | zambialii.org | AKN-HTML `eng@`-suffixed (`/akn/zm/act/1971/32/eng@1996-12-31`) | `zambialii_akn_html_dynamic_render_drift` cohort (`eng@`-suffixed sub-variant) |
| match | act | act-zm-2019-006-mental-health-act-2019 | www.parliament.gov.zm | parliament.gov.zm Act PDF | stable-PDF supercohort match |
| fetch_error | judgment | judgment-zm-2024-coa-024-kingfred-phiri-v-life-master-ltd | judiciaryzambia.com | judiciaryzambia.com wp-uploads PDF | HTTP 404 — record fetched 2026-05-18T15:16:51Z (b-inline ingestion ~5h before this tick) is now 404 at the canonical `source_url`. New audit-trail item; see gaps.md entry. |
| drift | act | act-zm-1960-024-development-united-kingdom-government-loan-act-1960 | zambialii.org | AKN-HTML `eng@`-suffixed (`/akn/zm/act/1960/24/eng@1996-12-31`) | `zambialii_akn_html_dynamic_render_drift` cohort (`eng@`-suffixed sub-variant) |

The b0717 sample composition: 1/8 parliament.gov.zm Act PDF, 1/8 zambialii.org `source.pdf` (SI PDF), 5/8 zambialii.org AKN-HTML pages (4 `eng@`-suffixed Acts + 1 bare-path SI), and 1/8 judiciaryzambia.com wp-uploads PDF (judgment). The 1 parliament.gov.zm PDF matched (stable-PDF supercohort behaviour). The 1 zambialii.org `source.pdf` matched (zambialii source.pdf supercohort behaviour). All 5 zambialii.org AKN-HTML records drifted (`zambialii_akn_html_dynamic_render_drift` cohort — known server-rendered timestamp / asset cache-busting behaviour; not substantive legal-text change). The 1 judiciaryzambia.com PDF returned HTTP 404 — first observation of this status for this URL.

### New audit-trail item

`judgment-zm-2024-coa-024-kingfred-phiri-v-life-master-ltd` — `source_url` returned HTTP 404 this tick. The record was ingested 2026-05-18T15:16:51Z (parser_version `0.4.1-inline`) and stored_sha256 `37921802939d394e942d9c498f72642e55b765b95dd92d6f0679b80c7cdb8ee1`. Local raw artefact is on disk (verified by the integrity step — stored_sha256 unchanged). Single sample point; could be a transient site issue, a temporary URL rotation, or a permanent removal. Phase 8 logs the observation as `phase8_reverify_fetch_error` without mutating the record. Recommended next step (operator-triage, no automatic action): wait for at least one more independent observation across subsequent Phase 8 sweeps before considering URL substitution or content re-fetch. Logged to gaps.md under the b0717 phase8 entry.

## Integrity checks

| # | Check | Result |
|---|---|---|
| 1 | JSON report well-formed; match+drift+fetch_error == sample_size (2+5+1=8) | PASS |
| 2 | No duplicate IDs in sample (8 unique) | PASS |
| 3 | Every stored + fetched sha256 is a valid 64-hex sha256 (fetched=None for the 404 case, expected) | PASS |
| 4 | Every sampled record's `stored_sha256` matches the on-disk record's `source_hash` (proper `sha256:` prefix-stripping) | PASS (no record file mutated this tick) |
| 5 | No tracked record file modified by this run (script is read-only) | PASS (script never opens records/ for write — source-verified) |
| 6 | `corpus.sqlite` NOT touched by Phase 8; `approvals.yaml` NOT modified | PASS (`git diff --name-only approvals.yaml corpus.sqlite` empty) |
| 7 | robots.txt respected; per-host rate limits honoured (zambialii.org min_gap ≥ 5s; judiciaryzambia.com min_gap ≥ 5s; deterministic `sleep_for_host` mechanism unchanged from baseline) | PASS |
| 8 | User-Agent honest: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` | PASS |
| 9 | corpus.sqlite live `quick_check=ok records=1970 records_fts=1970 dup_ids=0` (FTS parity with records table preserved across tick) | PASS |

All 9 checks PASS — tick commits via normal path.

### Pre-existing disk-state observation (NOT a new failure; not introduced by this tick)

A read-only audit confirmed that the on-disk `records/**/*.json` filesystem already contains the documented pre-existing state: 11 record files missing the `id` JSON field and 5 duplicate-ID pairs (same `id` exists at both `records/acts/{id}.json` and `records/acts/{year}/{id}.json` paths). None of those records are in this tick's sample. `corpus.sqlite` is the source of truth and reports `records=1970, dup_ids=0`. This pre-existing state predates Phase 8 b0717 and is unchanged by this tick (Phase 8 is read-only on records). Carried-forward operator-triage item.

## Cost / budget

- Network fetches this tick: 8 (7× HTTP 200, 1× HTTP 404)
- Cumulative daily fetches across all workers today (per costs.log fetches= sum): ~421 pre-tick; + 8 (this tick) = ~429 of 2000 daily budget. Plenty of headroom.
- Tokens consumed: 0 (deterministic pipeline, no LLM calls). LLM budget 0/1,000,000 today.
- Bandwidth: per `reports/batch-0717-reverify.json` (sum of `fetched_bytes_len`).
- Wall clock: 34s (budget 20min; headroom ~19m26s).

## B2 sync

Deferred to host — rclone not available in sandbox. Phase 8 is read-only on corpus (no `raw/` mutation) so deferral is acceptable per BRIEF.md §8.

## Repo-state note

Working tree at tick start was clean of prior-worker uncommitted artefacts (b0716-phase8 committed and pushed at 20:08:05Z; b0716-jiw deliverables were folded into b0716-phase8's commit per its repo-state note). Phase 8's own commit is scoped strictly to this tick's deliverables (new script + new reports + own log/costs/provenance appends).

## Next tick

Routine Phase 8 sampling continues. One new audit-trail item spawned this tick (`judgment-zm-2024-coa-024-kingfred-phiri-v-life-master-ltd` 404 — single observation, awaiting independent corroboration via subsequent Phase 8 sweeps before any operator action). 5 drifts fall under the pre-existing `zambialii_akn_html_dynamic_render_drift` cohort. Pre-existing carry-forwards remain:
- `judgment-zm-2025-zmcc-14` canonical-URL-date variant 404 (b0700 — audit-only; remediation requires explicit Peter approval).
- Existing 15 `parliament-pdf-v1.2` truncated-16hex defect records remain an open operator-triage item (latent — not drawn this tick).
- Pre-existing on-disk JSON state (11 no-`id` files + 5 duplicate-ID pairs) — operator-triage item.
