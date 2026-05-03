# Batch 0488 — parser_v0.3.2 launch + first reparse pass

- **Tick start (UTC):** 2026-05-03T08:30Z (interactive Cowork session — Peter present)
- **Phase:** 5 (judgments) — approved+incomplete
- **Action taken:** parser bump 0.3.1→0.3.2, approvals.yaml amendment on Peter's explicit instruction, first v0.3.2 reparse pass against the judges_no_comma backlog
- **Records written:** 2 (zmcc/2022/{34, 21})
- **Records deferred:** 6 (zmcc/2022/{33, 30, 27, 23, 22, 17})
- **Cumulative today:** 0/2000 fetches; ~12k tokens (parser code + report; well within 1,000,000 limit)
- **Tick note:** First substantive (record-writing) tick of Phase 5 since b0374. Breaks the 112-tick audit-only streak (b0375..b0487). Approvals.yaml was amended this batch on Peter's explicit Cowork instruction (parser_version 0.3.1→0.3.2; parser_baseline `scripts/batch_0360_parse.py`→`scripts/batch_0488_parse.py`; parser_policy_note rewritten; `deferral_reasons_locked` extended with `parser_v0.3.2_token_unhandled` and `canonical_url_date_unrecoverable`; `zmsc_older_year_sweep_approved: true` added). NO `approved`/`complete` flags were flipped — the human-only-gate non-negotiable is intact.

## parser_v0.3.2 design

- **Frozen baseline:** `scripts/batch_0488_parse.py`. Imports the v0.3.1 baseline (`scripts/batch_0360_parse.py`) unchanged via `import batch_0360_parse as v031`. The v0.3.1 file is NOT edited. The v0.3.1 `_detail_is_safe` filter is reused unchanged so v0.3.2 cannot regress safety on detail extraction.
- **SUMMARY_PATTERNS_V032** (13 regex additions, post-regression): widened outcome vocabulary covering Peter's 24 explicit phrases — passive forms ("application is refused", "conviction is upheld", "sentence is confirmed", "case is withdrawn", "matter is struck off"), active forms ("we set aside the judgment", "we refuse the relief"), procedural-refusal patterns ("dismissed for lack/failing/want/failure"), declaratory operative phrases ("declaratory relief was academic", "single-judge declined", "court refused stay"), discontinuance ("discontinuance allowed").
- **PDF_TAIL_PATTERNS_V032** (10 regex additions): same 24 phrases tail-tolerant, PLUS simpler "we &lt;verb&gt; the &lt;noun&gt;" forms that fix a v0.3.1 backtracking pathology — v0.3.1's `\bwe\s+...dismiss\s+(?:the\s+\w+\s+)?(?:appeal|...)` fails to match "we accordingly dismiss the appeal and uphold the declaration" because the optional group greedily consumes "the appeal " and then can't match the conjunction. v0.3.2's `\bwe\s+...dismiss\s+the\s+(?:appeal|...)` matches cleanly.
- **ORDER_INTRO + window-scan:** "we order that …" / "it is ordered that …" / "we make the following order(s)" — when found in the PDF tail, scan the next ~600 chars for a v0.3.2-or-v0.3.1 SUMMARY operative verb. The intro itself is not an outcome.
- **`parse_judges_v032`:** when `judges_text` contains no commas but ≥2 trailing judicial-title tokens (PC|DPC|CJ|DCJ|JCC|JJC|JJS|JS|JC|JA|JJA|JJ|J), match `<Surname Title>` pairs via a single regex and emit one judge per pair. Comma-separated input continues to use v0.3.1 `parse_judges` verbatim.
- **`find_outcome_in_pdf_tail_v032`:** combined v0.3.2 + v0.3.1 tail patterns into a single LAST-match-wins pool. This is critical — without the combined pool, a stray earlier match in v0.3.2 (or v0.3.1) would beat the final operative line in multi-issue judgments. The b0488 zmcc/2022/21 regression made this concrete: v0.3.2 SUMMARY initially matched "costs order set aside" (sub-finding) and produced wrong outcome `overturned`; the patch moved the passive set_aside pattern to TAIL-only AND restructured the tail resolver into the combined-pool design, after which the operative line "we accordingly dismiss the appeal" correctly produced `dismissed`.

## Reparse-first inventory (batch-0488 entry)

| Bucket | Count | Addressable by v0.3.2? |
|--------|------:|------------------------|
| `parser_v0.3.1_judges_no_comma_unhandled` | 19 | YES — `parse_judges_v032` resolves judges directly; outcome resolution then runs |
| `html_no_summary_pdf_no_match` | 60 | PARTIAL — depends on whether the operative line uses v0.3.2 vocabulary |
| `pdf_extraction_empty_likely_scanned` | 7 | NO — needs OCR pipeline |
| other (multi-judge, etc.) | 5 | NO — needs further parser stages |
| **Total missing (raw on disk, no record)** | **89** | |

## Targets this batch

Top 8 in priority order (judges_no_comma DESC then html_no_summary DESC):
zmcc/2022/{34, 33, 30, 27, 23, 22, 21, 17}.

## Resolutions

- **zmcc/2022/34 — Chanda v Lukonde** ([2022] ZMCC 34, 2022-02-15)
  - Outcome: `overturned`
  - Detail: "We set aside the decision of the Tribunal and …"
  - Source: `pdf-tail-2pages[v031-tail:\bwe\s+set\s+aside\s+(?:the\s+)?(?:judgment|order|decision|finding)\b]`
  - Judges (parse_judges_v032 no-comma fix): Chibomba (PC), Mulenga (JCC), Musaluke (JCC), Chisunka (JCC), Mulongoti (JCC)
  - Record id: `judgment-zm-2022-zmcc-34-chanda-v-lukonde`

- **zmcc/2022/21 — Chilufya v Ng'andwe and Anor** ([2022] ZMCC 21, 2022-09-29)
  - Outcome: `dismissed`
  - Detail: "four grounds of appeal have failed, we accordingly dismiss the appeal and uphold the declaration by the lower court that the 1° Respondent, Jean Chisenga Ng'andwe was duly elected …"
  - Source: `pdf-tail-2pages[v032-tail:\bwe\s+...dismiss\s+the\s+(?:petition|appeal|...)\b]` (the new v0.3.2 simpler-form pattern that fixes the v0.3.1 backtracking gap)
  - Judges (parse_judges_v032 no-comma fix): Sitali (JCC), Mulenga (JCC), Munalula (JCC), Mulongoti (JCC)
  - Record id: `judgment-zm-2022-zmcc-21-chilufya-v-ng-andwe-and-anor`

## Deferrals (specific reason codes; raw retained on disk)

All 6 deferred under `html_no_summary_pdf_no_match`. Per-record analysis is in `gaps.md` under "## Batch 0488 — REPARSE PASS under parser_v0.3.2 (2026-05-03)". One-liner each:

- zmcc/2022/33 — "We set aside the nullification" — noun "nullification" not in object list
- zmcc/2022/30 — "application for joinder is unsuccessful and accordingly dismissed" — too many words between "application" and "dismissed" for v031/v032 adverb tolerance
- zmcc/2022/27 — multi-disposition (dismisses functus officio AND allows constitutional challenge to proceed)
- zmcc/2022/23 — single-judge separate opinion; no clear majority disposition in extracted tail
- zmcc/2022/22 — "notice of motion … fails and is accordingly dismissed" — noun "notice of motion" not in object list
- zmcc/2022/17 — pure declaratory judgment (interpretive holding, no operative verb)

## Integrity check (post-parser, pre-commit)

- Records total: **80** (was 78 at end of b0487; +2 written this batch)
- Unique IDs: **80/80** (0 duplicates)
- Provenance complete (`source_url` + `source_hash` + `fetched_at` + `parser_version`): **80/80**
- `source_hash` shape valid: **80/80**
- `source_hash` resolves into `raw/` tree: **80/80** (sha256 index over raw/, 3203 files / 2926 unique sha256)
- Spot-recompute (seed=488): **6/6**
- Unresolved cross-refs within Phase 5 scope: **0**
- Court breakdown: Constitutional Court of Zambia=55 (was 53; +2 ZMCC 2022 records); Supreme Court of Zambia=25 (24 ZMSC + 1 SCZ pilot, unchanged).

## In-batch parser regression and fix (logged for audit trail)

The first v0.3.2 SUMMARY draft included a passive set_aside pattern:
`(?:judgment|order|decision|conviction|sentence|finding|ruling|verdict)\s+(?:is\s+)?(?:hereby\s+)?(?:quashed|set\s+aside)`. This matched "costs order set aside" in the zmcc/2022/21 flynote — but the case-level disposition is `dismissed` (substantive grounds failed; only the costs sub-issue was reversed). Result: a wrong record was briefly written to disk.

The patch (within the same batch, before commit):

1. Removed the passive `<noun>\s+set_aside/quashed` pattern from `SUMMARY_PATTERNS_V032`. The PDF_TAIL form remains (because in the tail, the LAST-match-wins logic correctly picks the operative line, not a sub-finding).
2. Restructured `find_outcome_in_pdf_tail_v032` to combine v0.3.2 + v0.3.1 tail patterns into a single LAST-match-wins pool. Without this, the v0.3.2 patterns would short-circuit before v0.3.1 patterns got a chance to find later matches.
3. Re-ran v0.3.2 against zmcc/2022/21 and overwrote the bad record file with the corrected `dismissed` resolution.
4. Verified zmcc/2022/34 was not affected by the patch (still resolves to `overturned` via v0.3.1's "we set aside the decision" pattern in the tail).

The bad record file was overwritten in place because the sandbox cannot unlink files; the corrected v0.3.2 resolution replaced the wrong content. No git history retains the bad record (it was never committed).

The b0488 gaps.md entry for zmcc/2022/21 documents the regression and the patch in the RESOLVED line so the audit trail is preserved.

## Operational status

- approvals.yaml AMENDED this batch on Peter's explicit Cowork instruction (parser_version 0.3.1→0.3.2; baseline path; policy note; deferral codes; ZMSC sweep approval). Diff is narrow and additive — no `approved`/`complete` flag was flipped. BRIEF.md non-negotiable on parser changes is satisfied (Peter's chat instruction IS the human approval).
- BRIEF.md unchanged this batch.
- gaps.md amended: 2 RESOLVED lines added under existing entries (zmcc/2022/34, zmcc/2022/21); 1 new "## Batch 0488" section appended documenting the 6 new deferrals and the in-batch regression.
- Phase 5 progress: 78 → 80 records (target 100–160).
- Five-consecutive-zero-discovery completion criterion is now UN-FIRED (this batch wrote 2 records). The criterion will need 5 more consecutive zero-write ticks to re-fire.
- B2 sync: deferred to host (rclone not in sandbox).
- SQLite ingestion: deferred to host (FTS5 carry-forward).

## Carry-forward note for next tick

Next scheduled tick should:

1. Run reparse-first against the remaining v0.3.2-addressable backlog: zmcc/2022/{20, 16, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1} + zmcc/2021/21 (top 8 in DESC order). The 2 written / 6 deferred ratio from b0488 is the empirical baseline; if the next batch confirms a similar pattern, that's a signal that further v0.3.2 vocabulary widening would be needed for the 2022 election-petition style.
2. If the entire judges_no_comma backlog completes with 0 fresh writes for 3 consecutive ticks, pivot to either (a) html_no_summary_pdf_no_match candidates with operative-verb candidates in the tail, or (b) BLOCK on Peter for ZMSC older-year sweep URL confirmation (approved this session but URL pattern pending).
3. ZMSC older-year sweep is approved (`zmsc_older_year_sweep_approved: true` in approvals.yaml) but the canonical source URL pattern is NOT confirmed. Worker MUST NOT issue any ZambiaLII fetches against /akn/zm/judgment/zmsc/ older years until Peter confirms the URL pattern via Cowork or by editing approvals.yaml directly.
