# Batch 0496 — parser_v0.3.2 reparse pivot to ZMCC 2023 (DESC entry, num {27, 26, 25, 23, 21, 20, 19, 18})

- **Tick start (UTC):** 2026-05-03T13:33Z (scheduled tick)
- **Phase:** 5 (judgments) — approved+incomplete
- **Action:** ninth v0.3.2 reparse pass; per b0495 next-tick recommendation option (2), pivots from the formally-exhausted ZMCC 2025 v0.3.2 reparse-first inventory to ZMCC 2023 (year-DESC entry across the 16 raw-on-disk no-record candidates remaining in that cohort).
- **Records written:** 1 (`zmcc/2023/19` — Tresford Mubanga v Zesco Limited)
- **Records deferred:** 7 (zmcc/2023/{27, 26, 25, 23, 21, 20, 18} all `html_no_summary_pdf_no_match`)
- **Cumulative today:** 0/2000 fetches; ~7k tokens (script copy + parser run + report + gaps.md edits)
- **Yield this tick:** 1/8 = 12.5%
- **Five-consecutive-zero-discovery counter:** 0 (b0494 zero, b0495 wrote 1, b0496 wrote 1)

## Tick prelude

Lock cleanup ran cleanly (one stale `maintenance.lock` could not be `unlink()`-ed due to sandbox virtiofs `EPERM` — same constraint Peter cleaned up host-side at 13:05Z; this single benign maintenance.lock entry will be swept by the next host-side cleanup. `git pull --ff-only` returned `Already up to date.` immediately.

## Targets and selection

Per b0495's next-tick recommendation option (2). ZMCC 2023 raw-on-disk no-record DESC slice. Raw HTML+PDF inventory under `raw/zambialii/judgments/zmcc/2023/`: 24 candidates with both HTML+PDF; 8 already in records (`{01, 02, 07, 10, 13, 15, 22, 24}`). Remaining 16 raw-on-disk no-record candidates: `{27, 26, 25, 23, 21, 20, 19, 18, 16, 14, 12, 8, 6, 5, 4, 3}`. This batch took the first DESC slice of 8: `{27, 26, 25, 23, 21, 20, 19, 18}`. All HTML+PDF pairs already on disk; 0 fresh fetches consumed.

## Resolutions

- **[2023] ZMCC 19 — Tresford Mubanga v Zesco Limited** (2023-10-26)
  - Outcome: `dismissed`
  - Detail: "merit in question one of the Respondent's application and we dismiss the Petition accordingly"
  - Source: `pdf-tail-2pages[v032-tail:\bwe\s+(?:hereby\s+|therefore\s+|accordi]` — the active-voice "we dismiss" operative-verb pattern (one of the 24 v0.3.2 phrase additions Peter listed in the 2026-05-03 widening)
  - Judges (3-judge bench): Sitali (presiding), Musaluke (concurring), Chisunka (concurring). All three already canonical in `judges_registry.yaml`; no new aliases added.
  - Issue tags: Constitutional jurisdiction; Article 128; interpretation of the Constitution versus employment disputes; redundancy and pension retention on payroll; Industrial Relations Division competent to grant employment remedies.
  - Record id: `judgment-zm-2023-zmcc-19-tresford-mubanga-v-zesco-limited`
  - Supersedes b0366 deferral note `html_no_summary_pdf_no_match`. RESOLVED line appended beneath the original gaps.md b0366 detailed entry per the reparse-first audit-policy non-negotiable; original entry not deleted.

## Deferrals (specific reason codes only)

All seven `html_no_summary_pdf_no_match` re-confirmations under v0.3.2:

- **[2023] ZMCC 27** (Zambia Community Development Initiative Programme & Anor v Attorney General, 2023-08-03) — originating-summons subject framing for the "dismissed" token; falls outside both v0.3.2 and v0.3.1 SUMMARY/TAIL pools.
- **[2023] ZMCC 26** (Milingo Lungu v The Attorney General and Anor, 2023-12-16) — procedural-amendment ruling (leave-to-amend limitation); no operative case-level disposition verb.
- **[2023] ZMCC 25** (Sean Tembo v The Attorney General, 2023-12-08) — issue-style summary head ("Whether the President's non-occupation … was justiciable") with no disposition token.
- **[2023] ZMCC 23** (Milingo Lungu v The Attorney General and Anor, 2023-11-07) — recusal-rebuttal holding; no recognised disposition verb.
- **[2023] ZMCC 21** (John Sangwa v The Attorney General, 2023-10-27) — constitutional-validity holding ("Section 30 CCA is constitutional"); no disposition verb.
- **[2023] ZMCC 20** (Leslie Mbula v Attorney General and Anor, 2023-10-26) — "dismissed" token in subordinate-clause context ("originating summons was unsuitable and dismissed"); outside operative-disposition pattern pools.
- **[2023] ZMCC 18** (Patrick Banda v The Electoral Commission and Ors, 2023-10-02) — pure holding-style summary ("election can only be annulled by a petition under Section 97 EPA"); no disposition token.

All seven received `RECONFIRMED-DEFERRED in batch-0496 (parser_v0.3.2)` notes appended beneath their original `gaps.md` entries (in the batch-0365 / batch-0366 detailed sections). No `gaps.md` entries were deleted.

## Integrity checks

- IDs unique across `records/judgments/` (94/94 — one new record this tick).
- All 20 required fields present on the new record.
- Both four-field provenance set (source_url, source_hash, fetched_at, parser_version) present and correct.
- `source_hash` matches sha256 of raw HTML on disk (verified by integrity_check_b0496.py).
- `raw_sha256` matches sha256 of raw PDF on disk.
- `outcome` ∈ enum (`dismissed`).
- `court` ∈ enum (Constitutional Court of Zambia).
- All `judges[*].role` ∈ enum (presiding, concurring, concurring).
- All three judges resolve in `judges_registry.yaml` (canonical or bare-surname).
- `issue_tags` non-empty (5 tags).
- `outcome_detail` passes the v0.3.1 `_detail_is_safe` filter (≥12 alphabetic chars, no blacklisted substrings, no leading lowercase mid-word fragment).
- `scripts/integrity_check_b0496.py` returns `INTEGRITY CHECK: PASS (1 record(s))`.

## Cumulative v0.3.2 yield

Across b0488..b0496: **16 records written / 67 attempted = 23.9%**.

## Phase 5 progress

93 → 94 (target 100–160 landmark judgments). 6 short of low end.

## Next-tick recommendation

Continue the ZMCC 2023 DESC sweep with the next slice: `zmcc/2023/{16, 14, 12, 8, 6, 5, 4, 3}` (the remaining 8 raw-on-disk no-record candidates — exactly one MAX_BATCH_SIZE bucket). After that the ZMCC 2023 v0.3.2 reparse-first inventory will be formally exhausted, leaving the cohorts ZMCC 2026 (11 candidates), ZMCC 2021 (18 candidates), and ZMSC 2025/2026 (24 candidates) as the remaining v0.3.2-untested reparse-first inventory.

ZMSC older-year sweep — option (3) — remains pending Peter's URL pattern confirmation per `approvals.yaml.zmsc_older_year_sweep_approval_note`; not actionable by scheduled tick until that confirmation lands.
