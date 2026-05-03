# Batch 0497 — parser_v0.3.2 reparse, ZMCC 2023 DESC continuation/finisher (num {16, 14, 12, 8, 6, 5, 4, 3})

- **Tick start (UTC):** 2026-05-03T13:55Z (scheduled tick)
- **Phase:** 5 (judgments) — approved+incomplete
- **Action:** tenth v0.3.2 reparse pass; per b0496 next-tick recommendation, continues the ZMCC 2023 DESC sweep with the remaining 8 raw-on-disk no-record candidates. Together b0496+b0497 formally exhaust the ZMCC 2023 v0.3.2 reparse-first inventory.
- **Records written:** 2 (`zmcc/2023/16` Institute of Law Policy Research and Human Rights v ECZ; `zmcc/2023/14` Martin Chilukwa v The Attorney General)
- **Records deferred:** 6 (zmcc/2023/{12, 8, 6, 5, 4, 3}, all `html_no_summary_pdf_no_match`)
- **Cumulative today:** 0/2000 fetches (all reparse from on-disk raw — zero fresh fetches consumed); ~7k tokens (script copy + parser run + report + gaps.md edits)
- **Yield this tick:** 2/8 = 25.0%
- **Five-consecutive-zero-discovery counter:** 0 (b0494 zero, b0495 wrote 1, b0496 wrote 1, b0497 wrote 2 — three consecutive substantive ticks since b0494)

## Tick prelude

`find .git -name "*.lock" -delete` and `find .git -name "*.lock.bak" -delete` ran cleanly — no stale-lock backlog this tick (Peter's host-side cleanup at ~13:05Z holds). One `.git/objects/maintenance.lock` could not be unlinked under sandbox virtiofs `EPERM` but the warning is benign and `git pull --ff-only` returned `Already up to date.` immediately. No fetch budget consumed; no token budget consumed beyond the parser run itself.

## Targets and selection

Per b0496's next-tick recommendation. ZMCC 2023 raw-on-disk no-record DESC continuation: the remaining 8 candidates after b0496 covered {27..18}: `zmcc 2023/{16, 14, 12, 8, 6, 5, 4, 3}`. All eight HTML+PDF pairs already on disk under `raw/zambialii/judgments/zmcc/2023/`; 0 fresh fetches consumed. Targets file: `_work/b0497/targets.json`.

## Resolutions

### [2023] ZMCC 16 — Institute of Law, Policy Research and Human Rights and Ors v Electoral Commission of Zambia and Ors (2023-07-11)

- **Outcome:** `dismissed`
- **Outcome detail:** "On that account we dismiss the petition"
- **Outcome source:** `pdf-tail-2pages[v032-tail:\bwe\s+(?:hereby\s+|therefore\s+|accordi]` — the active-voice "we dismiss" operative-verb pattern (one of the 24 v0.3.2 phrase additions Peter listed in the 2026-05-03 widening). Last-match-wins; the operative paragraph sits at the end of the judgment.
- **Bench:** three-judge — Munalula DPC (presiding), Mulonda JJC, Chisunka JJC. All three already canonical in `judges_registry.yaml`; no new aliases added.
- **Issue tags (from summary):** Constitutional Court jurisdiction; petition challenging nominations; rescinding resignations; parliamentary by-elections.
- **Citation:** `[2023] ZMCC 16`.
- **Record id:** `judgment-zm-2023-zmcc-16-institute-of-law-policy-research-and-human-rights`.
- **Source URL:** `https://zambialii.org/akn/zm/judgment/zmcc/2023/16/eng@2023-07-11`.
- Supersedes batch-0353 deferral note `outcome_not_inferable_under_tightened_policy` (parser_v0.3.0). RESOLVED line appended beneath the original gaps.md b0353 detailed entry per the reparse-first audit-policy non-negotiable; original entry not deleted.

### [2023] ZMCC 14 — Martin Chilukwa v The Attorney General (2023-03-10)

- **Outcome:** `dismissed`
- **Outcome detail:** "Challenge to DC appointments dismissed for lack of evidence and because employment-related claims lie outside Constitutional Court jurisdiction"
- **Outcome source:** `summary[v032:\b(?:application|petition|appeal|challen]` — the v0.3.2 SUMMARY pattern covering "(application/petition/appeal/challenge) is dismissed/refused/granted" family. A Peter-targeted regex addition from the 2026-05-03 widening (`is dismissed` form on noun "challenge").
- **Bench:** three-judge — Mulonda JJC (presiding), Musaluke JJC, Chisunka JJC. All three already canonical in `judges_registry.yaml`; no new aliases added.
- **Issue tags (from summary):** DC appointments challenge; lack of evidence; employment-related claims; Constitutional Court jurisdiction.
- **Citation:** `[2023] ZMCC 14`.
- **Record id:** `judgment-zm-2023-zmcc-14-martin-chilukwa-v-the-attorney-general`.
- **Source URL:** `https://zambialii.org/akn/zm/judgment/zmcc/2023/14/eng@2023-03-10`.
- Supersedes batch-0353 deferral note `outcome_not_inferable_under_tightened_policy` (parser_v0.3.0). RESOLVED line appended beneath the original gaps.md b0353 detailed entry per the reparse-first audit-policy non-negotiable; original entry not deleted.

## Deferrals (specific reason codes only)

All six `html_no_summary_pdf_no_match` re-confirmations under v0.3.2 SUMMARY_PATTERNS_V032, PDF_TAIL_PATTERNS_V032 and ORDER_INTRO window-scan:

- **[2023] ZMCC 12** (Mutambo v The Attorney General, 2023-09-26) — declaratory holding on Article 165 (prospective) plus jurisdictional bar on chieftaincy succession; no operative disposition verb.
- **[2023] ZMCC 8** (Mwiinde v Attorney General and National Pensions Scheme Authority, 2023-04-21) — declaratory mixed holding on Article 189 protections and NAPSA eligibility; no case-level disposition token.
- **[2023] ZMCC 6** (Sangwa v Attorney General and Law Association of Zambia, 2023-03-08) — declaratory holding-style summary on judicial financial autonomy with subordinate-clause "declines to void"; outside operative-disposition pattern pools.
- **[2023] ZMCC 5** (Governance Elections Advocacy Research Services Initiative Zambia v Attorney General, 2023-03-08) — declaratory interpretive holding on Article 52(6); no disposition verb.
- **[2023] ZMCC 4** (Ikelenge Town Council v National Pension Scheme Authority, 2023-02-09) — declaratory holding on Article 266 / Article 160 immunity; no operative case-level disposition token.
- **[2023] ZMCC 3** (Malanji and Anor v Attorney General and Anor, 2023-02-08) — issue-style summary head ("Whether vacancies caused by nullification …"); pure question framing with no disposition token.

All six received `RECONFIRMED-DEFERRED in batch-0497 (parser_v0.3.2, 2026-05-03)` notes appended beneath their original `gaps.md` entries (in the batch-0353 / batch-0354 detailed sections). No `gaps.md` entries were deleted.

## Integrity checks

- `scripts/integrity_check_b0497.py` returns `INTEGRITY CHECK: PASS (2 record(s))`.
- IDs unique across `records/judgments/` (96/96).
- All 20 required fields present on each new record.
- Provenance (source_url, source_hash, fetched_at, parser_version) present and correct on each record.
- `source_hash` matches sha256 of raw HTML on disk for both records.
- `raw_sha256` matches sha256 of raw PDF on disk for both records.
- `outcome` ∈ enum (`dismissed` for both).
- `court` ∈ enum (Constitutional Court of Zambia).
- All `judges[*].role` ∈ enum (presiding, concurring).
- All judges resolve in `judges_registry.yaml` — six judge-resolutions (3 + 3), zero new canonical entries added.
- `issue_tags` non-empty on both records.
- `outcome_detail` passes the v0.3.1 `_detail_is_safe` filter for both records.

## Cumulative v0.3.2 yield

Across b0488..b0497: **18 records written / 75 attempted = 24.0%**.

| Batch | Cohort | Written | Attempted | Yield | Profile |
|-------|--------|---------|-----------|-------|---------|
| 0488  | ZMCC 2022 (DESC entry) | 2 | 8 | 25.0% | parser-launch + in-batch regression patch |
| 0489  | ZMCC 2022 (DESC continuation) | 3 | 8 | 37.5% | five-judge benches with v031-tail operative phrases |
| 0490  | ZMCC 2022 (DESC completion) | 6 | 8 | 75.0% | judges_no_comma backlog cleared |
| 0491  | ZMCC 2022 (html_no_summary untested) | 0 | 8 | 0.0% | declaratory/interpretive — vocabulary-blind |
| 0492  | ZMCC 2024 (num-ASC pivot) | 0 | 8 | 0.0% | declaratory/interlocutory — same blind spot |
| 0493  | ZMCC 2025 (DESC pivot, num {33..19}) | 3 | 8 | 37.5% | two SUMMARY hits on Peter-targeted phrases + one PDF-tail hit |
| 0494  | ZMCC 2025 (DESC continuation, num {18..7}) | 0 | 8 | 0.0% | declaratory / ratio-style cohort |
| 0495  | ZMCC 2025 (DESC finisher, num {6, 5, 2}) | 1 | 3 | 33.3% | "we dismiss" v032-tail hit on ZMCC 02 |
| 0496  | ZMCC 2023 (DESC entry, num {27..18}) | 1 | 8 | 12.5% | "we dismiss" v032-tail hit on ZMCC 19 |
| 0497  | ZMCC 2023 (DESC continuation/finisher, num {16,14,12,8,6,5,4,3}) | 2 | 8 | 25.0% | one v032-tail hit + one v032 SUMMARY "is dismissed" challenge-noun hit |

## Phase 5 progress

94 → 96 records (target 100–160 landmark judgments). 4 short of low end.

## ZMCC 2023 reparse-first inventory now formally exhausted

After b0496 (8 candidates: {27,26,25,23,21,20,19,18}; 1 written, 7 deferred) and b0497 (8 candidates: {16,14,12,8,6,5,4,3}; 2 written, 6 deferred), the ZMCC 2023 raw-on-disk no-record DESC inventory under v0.3.2 is FORMALLY EXHAUSTED. Combined yield: 3 written / 16 attempted = 18.75%. Remaining ZMCC 2023 no-record candidates that are NOT addressable by reparse: `zmcc 2023/17` (PDF 404 at source — hard upstream gap, see batch-0353), `zmcc 2023/11` and `zmcc 2023/9` (HTTP 404 at source — number not assigned upstream, see batch-0354).

## Next-tick recommendation

Pivot options for the next tick (in expected-yield order):

1. **ZMCC 2026 untested-under-v0.3.2** (11 candidates) — most recent cohort. Likely contains v0.3.2-addressable disposition phrases. Recommended.
2. **ZMCC 2021 untested-under-v0.3.2** (18 candidates) — older cohort with mixed disposition styles; expect some v0.3.2 SUMMARY hits.
3. **ZMSC older-year sweep** — option (3) — remains pending Peter's URL pattern confirmation per `approvals.yaml.zmsc_older_year_sweep_approval_note`; not actionable by scheduled tick until that confirmation lands.

Five-consecutive-zero-discovery completion criterion remains UN-FIRED. approvals.yaml NOT modified per Phase 5 human-only confirmation rule.

## SQLite ingestion status

Carry-forward: `corpus.sqlite` FTS5 malformed-disk-image condition first observed in b0474 still holds under sandbox virtiofs (`database disk image is malformed`). No new corruption introduced this tick. Host-side rebuild remains required before next FTS query. Per established pattern, SQLite ingestion deferred to host.

## B2 sync status

`rclone` is not available in the sandbox; B2 sync deferred to host as in every prior tick. Logged in costs.log as `batch-0497 B2 sync deferred to host (rclone not in sandbox)`.
