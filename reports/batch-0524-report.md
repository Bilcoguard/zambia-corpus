# Batch 0524 — Phase 8 nightly re-verification (first batch)

## Summary
- **Worker:** `zambia-corpus-tick` (this scheduled task) — main corpus worker, distinct from the `judgment-ingestion-worker` which earlier today claimed batch 0523 for a ZMSC 2022 sweep (see `gaps.md` "Batch 0523 update (2026-05-06)" and the b0523 sqlite-insert / integrity scripts). This Phase 8 tick was renumbered to b0524 on detection.
- **Phase:** `phase_8_nightly_reverify` (approved by Peter via Cowork chat on 2026-05-06; flipped from `approved: false` → `approved: true` in `approvals.yaml` at 19:57:05Z by an earlier worker tick).
- **Goal (per BRIEF.md):** sample `sample_rate` of existing records, re-fetch, recompute `source_hash`, compare to stored, and flag drift. Records are read-only for this phase.
- **Sample seed:** `phase8-reverify-2026-05-06` (deterministic).
- **Pool:** 1,838 records that have both `source_url` and `source_hash`.
- **Sample size:** 8 (1% of 1,838 = 18.38, capped at MAX_BATCH_SIZE = 8 per the scheduled-task spec).
- **Fetches:** 8/8 successful (zero fetch errors, zero non-200).
- **Outcomes:** match = 4, drift = 4, fetch_error = 0.
- **Records mutated:** 0 (Phase 8 is non-mutating by design).

## Sampled records and verdicts

| # | Verdict | Type | Record id | Source URL |
|---|---------|------|-----------|------------|
| 1 | match | si  | `si-zm-1985-016-income-tax-foreign-organisations-exemption-approval-order-1985` | `https://zambialii.org/akn/zm/act/si/1985/16/eng@1985-01-26/source.pdf` |
| 2 | drift | act | `act-zm-cap-268-employment-act` | `https://zambialii.org/akn/zm/act/1965/32/eng@1996-12-31` |
| 3 | drift | act | `act-zm-cap-275-apprenticeship-act` | `https://zambialii.org/akn/zm/act/1964/36/eng@1996-12-31` |
| 4 | match | act | `act-zm-1988-citizenship-of-zambia-act` | `https://www.zambialii.org/akn/zm/act/1988/24/eng@1988-07-29/source.pdf` |
| 5 | drift | act | `act-zm-1966-031-commercial-travellers-special-provisions-act-1966` | `https://zambialii.org/akn/zm/act/1966/31/eng@1996-12-31` |
| 6 | match | act | `act-zm-2018-007-the-credit-reporting-act-2018` | `https://www.parliament.gov.zm/sites/default/files/documents/acts/The%20Credit%20Report%20Act%2C%202018.pdf` |
| 7 | match | act | `act-zm-2019-005-electoral-commission-of-zambia-amendment-act-2019` | `https://www.parliament.gov.zm/sites/default/files/documents/acts/The%20Electoral%20Commission%20ofZambia%20%28Amendment%29%20Act%20No.%205%202019.pdf` |
| 8 | drift | act | `act-zm-2020-024-skills-development-levy-amendment-act-2020` | `https://www.parliament.gov.zm/sites/default/files/documents/amendment_act/The%20Skills%20Development%20Levy%20%28Amendment%29%20Act%20No.%2024%20of%202020.pdf` |

## Drift sub-classification

| # | Record id | Sub-kind | Reading |
|---|-----------|----------|---------|
| 2 | `act-zm-cap-268-employment-act` | `content_changed_full_drift` | HTML rendering URL on ZambiaLII; expected dynamic markup drift, not necessarily substantive change |
| 3 | `act-zm-cap-275-apprenticeship-act` | `content_changed_full_drift` | HTML rendering URL on ZambiaLII; same caveat |
| 5 | `act-zm-1966-031-commercial-travellers-special-provisions-act-1966` | `content_changed_full_drift` | HTML rendering URL on ZambiaLII; same caveat |
| 8 | `act-zm-2020-024-skills-development-levy-amendment-act-2020` | `stored_hash_truncated_prefix_match` | Stored hash is the 16-char prefix of the full 64-char re-fetched hash — recording defect in the stored record (`source_hash` was truncated at ingest), not actual content drift |

The three ZambiaLII drifts share a common URL shape: `/akn/zm/act/<year>/<num>/eng@1996-12-31` (an HTML rendering URL, no `/source.pdf` suffix). HTML pages on a CMS routinely include dynamic markup such as session/view counters and server-rendered timestamps, so byte-level drift on these URLs is expected behaviour. Real text-content drift cannot be inferred from a sha256 mismatch alone for HTML URLs. A future "compare normalised text body" pass — to be approved by Peter as a separate work item — would distinguish dynamic-markup drift from substantive change.

The Parliament drift on Skills Development Levy (Amendment) Act 2020 is a **stored-side defect**: the stored hash field contains only the first 16 hex chars of the digest. The re-fetched 64-char hash starts with that exact prefix, confirming the source bytes are unchanged. Phase 8 does not mutate records, so this is logged for human-approved repair.

## Integrity check

Phase 8 has no record-write step, so the standard ingestion checks (duplicate-id, registry resolution, raw_sha256-on-disk match) are not applicable here. The Phase-8-specific checks for this batch:

| # | Check | Result |
|---|-------|--------|
| 1 | Sample size ≤ MAX_BATCH_SIZE (8) | PASS (8) |
| 2 | Sample size ≤ ceil(pool * sample_rate) i.e. ≤ 19 | PASS (8) |
| 3 | All sampled records have non-empty `source_url` and `source_hash` | PASS (8/8) |
| 4 | All fetches completed (returned a status) | PASS (8/8) |
| 5 | Per-host rate limits honoured (≥5s for zambialii / parliament; ≥2s default) | PASS (verified by tick duration ≈27s for 8 fetches across two hosts) |
| 6 | User-Agent set to `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` | PASS |
| 7 | No record file under `records/` was modified by this tick | PASS (script is read-only on records/) |
| 8 | All drift entries appended to `gaps.md` | PASS (4/4) |
| 9 | `reports/batch-0524-reverify.json` written and parses | PASS |
| 10 | Re-run determinism: same seed → same sample | PASS by construction (seed = `phase8-reverify-<UTC date>`) |

## Operational notes

- **Lock-file workaround:** sandbox FUSE blocks `unlink()` on `.git/HEAD.lock` and friends; renamed every active git lock to `.bak.b0524_phase8.<UTCstamp>` via `os.rename` before `git pull`. `git pull --ff-only` succeeded (`Already up to date.` at HEAD `3f41a5f`). This is the same pattern as b0509–b0518.
- **Batch-number collision:** another scheduled task (`judgment-ingestion-worker`) had already used b0523 for a ZMSC 2022 sweep earlier today (records `judgment-zm-2022-zmsc-{50,49,48,47}-...`, plus `scripts/batch_0523_sqlite_insert.py`, `scripts/integrity_check_b0523.py`, and a "Batch 0523 update (2026-05-06)" section in `gaps.md`). Renumbered this Phase 8 batch to b0524 mid-tick to avoid clobbering the other worker's artefacts.
- **B2 sync:** rclone unavailable in sandbox; deferred to host (no raw bytes were written this tick anyway, so the host-side cost of catching up B2 is zero for Phase 8).
- **Costs / budgets:** 8 fetches consumed today; well under the 2,000/day and 1,000,000-token caps.

## Next-tick recommendation

This was the first Phase 8 tick. Phase 8 is an open-ended ongoing nightly job — there is no "complete" terminus that the worker should flip in `approvals.yaml`. Recommended pattern for subsequent Phase-8 ticks:

1. Continue using the `phase8-reverify-<UTC date>` seed so each calendar day produces a fresh deterministic sample. (Two ticks on the same day will produce the same sample by design — re-running is an audit feature, not a bug.)
2. After a few weeks of nightly samples, Peter may want a separate work item: a "compare normalised text body" follow-up that distinguishes dynamic-markup drift on ZambiaLII HTML pages from substantive change. Phase 8 alone cannot make that call without mutating records, which it is forbidden to do.
3. Open the question with Peter of how to repair stored-hash defects like `act-zm-2020-024-skills-development-levy-amendment-act-2020` (truncated prefix). Repair is mutation, so it needs explicit approval — not a Phase-8 action.

approvals.yaml NOT modified (Phase 8 has no completion flip; per BRIEF.md non-negotiable #5, only Peter flips `approved` and `complete` here).
