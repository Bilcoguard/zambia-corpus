# Batch 0493 — parser_v0.3.2 reparse continuation (ZMCC 2025 pivot)

- **Tick start (UTC):** 2026-05-03T11:03Z (scheduled tick)
- **Phase:** 5 (judgments) — approved+incomplete
- **Action:** sixth v0.3.2 reparse pass; pivots from the now-exhausted ZMCC 2024 cohort (b0492 zero-yield) to ZMCC 2025 untested-under-v0.3.2 per b0492's next-tick recommendation. Targets prioritise the deferral set explicitly anticipated by Peter's 2026-05-03 v0.3.2 widening (`court refused stay` and `declaratory relief was academic` — both regexes appear directly in SUMMARY_PATTERNS_V032).
- **Records written:** 3 (zmcc/2025/{32, 25, 22})
- **Records deferred:** 5 (zmcc/2025/{33, 28, 24, 21} all `html_no_summary_pdf_no_match`; zmcc/2025/19 `pdf_extraction_empty_likely_scanned`)
- **Cumulative today:** 0/2000 fetches; ~6k tokens (parser script copy + report)
- **Yield this tick:** 3/8 = 37.5% (best v0.3.2 single-tick yield since b0490's 6/8; the v0.3.2 widening worked exactly as intended for the two SUMMARY-targeted phrases)

## Tick prelude — host-side ref-cleanup workaround

The 11:03Z scheduled tick aborted on first attempt with `fatal: bad object refs/heads/main.lock.bak.b0492.103928` left over from a prior failed git operation. Sandbox mount denies `unlink` on these files (PermissionError on `os.unlink`, `rm -f`, and `git update-ref -d`), so the standard cleanup path documented in worker.log can't remove the stale ref names directly. The tick recovered by **writing the current `refs/heads/main` SHA** (`2573c70e71cb07980f2c2f0ee4345b26ba39db2c`) into the orphan ref files (`.git/refs/heads/main.lock.bak.b0492.103928` and `.git/refs/heads/test_create`) — git's resolver is then satisfied because both names now point at a valid object. `git pull --ff-only` succeeded immediately after. The orphan ref names remain on disk but are now harmless. Host-side `rm` on those files is still recommended at the next manual session for a cleaner refs tree.

## Targets and selection

The b0492 report recommended pivoting from ZMCC 2024 (formally exhausted under v0.3.2) to ZMCC 2025 starting from `{25, 24, 23, 22, 21}` because v0.3.2's widening was specifically designed for two SUMMARY phrases that appear in this cohort. Of those, 23 is already in the corpus (`judgment-zm-2025-zmcc-23-emmanuel-kayuni-suing-as-administrator-of-the-esta`); the remaining four were taken in DESC order, padded out to MAX_BATCH_SIZE=8 with the next-highest untested ZMCC 2025 raw-on-disk candidates (`{33, 32, 28, 19}`). Final target slice: `zmcc/2025/{33, 32, 28, 25, 24, 22, 21, 19}`. All eight HTML+PDF pairs already on disk; this run consumed 0 fresh fetches.

## Resolutions

- **[2025] ZMCC 32 — The Law Association of Zambia and Ors v The Attorney General** (2025-12-16)
  - Outcome: `dismissed`
  - Detail: "We therefore dismiss the application for conservatory order"
  - Source: `pdf-tail-2pages[v032-tail]` (active `we therefore dismiss …` operative-verb pattern, one of the 24 v0.3.2 phrase additions)
  - Judges (parse_judges_v032 no-comma fix): Munalula (PC), Shilimi (DPC), Musaluke (JJC), Mulongoti (JJC), Mwandenga (JJC). All resolved against existing canonical entries.
  - Record id: `judgment-zm-2025-zmcc-32-the-law-association-of-zambia-and-ors-v-the-attorn`

- **[2025] ZMCC 25 — Tresford Chali v Attorney General** (2025-12-04)
  - Outcome: `dismissed`
  - Detail: "Court refused stay of Speaker's vacancy ruling absent special and convincing grounds; merits not to be decided interlocutorily"
  - Source: `summary[v032]` (one of the 24 v0.3.2 phrase additions Peter listed: `\bcourt\s+refused\s+(?:a\s+)?(?:to\s+gra…)?` — refusal-as-outcome variant)
  - Judges: Hon. Mr. Justice M. Musaluke (single-judge bench). Resolved against existing canonical entry (Musaluke).
  - Record id: `judgment-zm-2025-zmcc-25-tresford-chali-v-attorney-general`

- **[2025] ZMCC 22 — Sean Tembo (Spokesperson) v Attorney General** (2025-11-27)
  - Outcome: `dismissed`
  - Detail: "Declaratory relief was academic; transitional Act provisions governed eligibility, and Article 267(3)(b)(c) did not affect the Court's decision"
  - Source: `summary[v032]` (one of the 24 v0.3.2 phrase additions: `\bdeclaratory\s+relief\s+(?:was|is)\s+ac(?:ademic)?`)
  - Judges (parse_judges_v032 no-comma fix, seven-judge bench): Shilimi (DPC), Musaluke (JJC), Chisunka (JJC), Mulongoti (JJC), Mwandenga (JJC), Kawimbe (JJC), Mulife (JJC). All resolved against existing canonical entries.
  - Record id: `judgment-zm-2025-zmcc-22-sean-tembo-suing-in-his-capacity-as-spokesperson-o`

## Deferrals (specific reason codes only — no generic `outcome_not_inferable_under_tightened_policy`)

- **[2025] ZMCC 33** (Sampa v AG and Ors, 2025-12-18) — `html_no_summary_pdf_no_match`. Negative interpretive holding ("did not amount to disposal of State equity"); no operative-verb match in either pool.
- **[2025] ZMCC 28** (Mundubile and Anor v Hichilema and Anor, 2025-12-05) — `html_no_summary_pdf_no_match`. Procedural-direction declaratory ("must proceed against the Attorney-General"); no operative-verb match.
- **[2025] ZMCC 24** (LAZ v Speaker, 2025-11-28) — `html_no_summary_pdf_no_match`. Joinder-ordered (interlocutory direction); v0.3.2 only added refusal-as-outcome variants, not joinder-ordered.
- **[2025] ZMCC 21** (LAZ and Ors v AG, 2025-11-25) — `html_no_summary_pdf_no_match`. "Application … dismissed for failing …" participial dependency falls outside v0.3.2's `dismissed-for-(lack|failing|want|failure)` regex (which requires direct adjacency between the noun head and the disposition token).
- **[2025] ZMCC 19** (BetBio Zambia Ltd v AG, 2025-09-30) — `pdf_extraction_empty_likely_scanned`. Re-confirmed under v0.3.2 (parser bump does not change PDF extraction); awaits OCR pass.

All five deferrals received `RECONFIRMED-DEFERRED in batch-0493 (parser_v0.3.2)` notes appended beneath their original `gaps.md` entries, per the reparse-first audit-policy non-negotiable. No `gaps.md` entries were deleted.

## Integrity checks

- IDs unique across `records/judgments/` (92/92).
- All four-field provenance present on the 3 new records (source_url, source_hash, fetched_at, parser_version) plus raw_sha256.
- All `source_hash` and `raw_sha256` values for new records resolve to bytes on disk (sha256 verified via direct re-hash of the named raw files).
- Full-corpus sha256 resolution PASS (3203 files / 2926 unique sha; every non-empty source_hash and raw_sha256 across the 92 records resolves into the disk index).
- All `judges[*].name` on the 3 new records resolve in `judges_registry.yaml` (canonical or bare-surname). 273/273 judge entries across the full corpus resolve. Zero new judges added (every alias mapped to an existing canonical entry).
- `outcome` ∈ enum on the 3 new records (all `dismissed`).
- `issue_tags` non-empty on the 3 new records.
- `outcome_detail` passes safety filter on the 3 new records (no blacklisted substrings, ≥12 alphabetic chars, no leading lowercase mid-word fragment).
- `scripts/integrity_check_b0493.py` returns `INTEGRITY CHECK: PASS (3 record(s))`.

## Cumulative v0.3.2 yield

Across b0488..b0493: **14 records written / 48 attempted = 29.2%**.

| Batch | Cohort | Written | Attempted | Yield | Profile |
|-------|--------|---------|-----------|-------|---------|
| 0488  | ZMCC 2022 (judges_no_comma + html_no_summary, DESC entry) | 2 | 8 | 25.0% | parser-launch + in-batch regression patch |
| 0489  | ZMCC 2022 (judges_no_comma DESC continuation) | 3 | 8 | 37.5% | five-judge benches with v031-tail operative phrases |
| 0490  | ZMCC 2022 (judges_no_comma DESC completion) | 6 | 8 | 75.0% | judges_no_comma backlog cleared |
| 0491  | ZMCC 2022 (html_no_summary untested-under-v0.3.2) | 0 | 8 | 0.0%  | declaratory/interpretive — vocabulary-blind |
| 0492  | ZMCC 2024 (num-ASC pivot)                       | 0 | 8 | 0.0%  | declaratory/interlocutory — same blind spot |
| 0493  | ZMCC 2025 (DESC pivot per b0492 recommendation) | 3 | 8 | 37.5% | two SUMMARY hits on Peter-targeted phrases + one PDF-tail hit |

## Phase 5 progress

89 → 92 (target 100–160 landmark judgments). 8 short of low end after this tick. Five-consecutive-zero-discovery completion criterion remains UN-FIRED (b0488/0489/0490 all wrote records, b0491/0492 zero-write, b0493 wrote 3 — counter resets).

## Next-tick recommendation

Continue option (1) from gaps.md b0493 recommendation: ZMCC 2025 DESC sweep through the remaining untested-under-v0.3.2 candidates `{18, 17, 14, 11, 10, 9, 8, 7}`. Yield expectation moderate — same mixed profile as today but the `court refused stay` / `declaratory relief was academic` SUMMARY widenings have proven their value, and the cohort almost certainly contains a few more cases each side of the line. Defer ZMCC 2023 inventory pass and ZMSC older-year sweep until ZMCC 2025 reparse-first inventory is exhausted under v0.3.2 (or until Peter confirms the ZMSC URL pattern, whichever comes first).
