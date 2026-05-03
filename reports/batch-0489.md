# Batch 0489 — parser_v0.3.2 reparse continuation (zmcc 2022 DESC)

- **Tick start (UTC):** 2026-05-03T09:05Z (scheduled tick)
- **Phase:** 5 (judgments) — approved+incomplete
- **Action:** second v0.3.2 reparse pass; continues b0488's recommended sweep down the zmcc/2022 judges_no_comma + html_no_summary backlog (b0488 advised next slice would be zmcc/2022/{20, 16, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1} + zmcc/2021/21 — minus {16}, which is OCR-pending)
- **Records written:** 3 (zmcc/2022/{20, 8, 5})
- **Records deferred:** 5 (zmcc/2022/{11, 10, 9, 7, 6}) — all `html_no_summary_pdf_no_match`
- **Cumulative today:** 0/2000 fetches; ~5k tokens (parser script copy + report)
- **Yield this tick:** 3/8 = 37.5% (vs b0488's 2/8 = 25%; v0.3.2 SUMMARY/TAIL/judges-no-comma unblock is producing rising marginal yield as the simpler operative-verb cases get cleared)

## Targets and selection

DESC scan of the b0488 recommended slice: zmcc/2022/{20, 11, 10, 9, 8, 7, 6, 5}. Skipped {16} per the OCR-pending classification (`pdf_extraction_empty_likely_scanned` — held for OCR pipeline approval, not addressable by v0.3.2). All eight HTML+PDF pairs already on disk; this run consumed 0 fresh fetches.

## Resolutions

- **[2022] ZMCC 20 — Ndhlovu and Ors v Road Development Agency** (CCZ 5 of 2022, 2022-09-21)
  - Outcome: `dismissed`
  - Detail: "The Petition is accordingly dismissed"
  - Source: `pdf-tail-2pages[v031-tail:\b(?:petition|appeal|application|action|...)\s+(?:is\s+)?(?:hereby\s+)?...dismissed\b]`
  - Judges (parse_judges_v032 no-comma fix): Munalula (JCC), Mulenga (JCC), Chisunka (JCC). All resolved against existing `judges_registry.yaml` canonical entries — no registry write needed.
  - Record id: `judgment-zm-2022-zmcc-20-ndhlovu-and-ors-v-road-development-agency`

- **[2022] ZMCC 8 — Kafwaya v Katonga and Ors** (2022-04-13)
  - Outcome: `allowed`
  - Detail: "mandatory requirement of section 97(2)(a) of the Act, the appeal succeeds"
  - Source: `pdf-tail-2pages[v031-tail:\b(?:appeal|petition|application)\s+succeeds\b]`
  - Judges (parse_judges_v032 no-comma fix): Sitali (JCC), Mulenga (JCC), Mulonda (JCC), Munalula (JCC), Mulongoti (JCC). All resolved against existing canonical entries.
  - Record id: `judgment-zm-2022-zmcc-08-kafwaya-v-katonga-and-ors`

- **[2022] ZMCC 5 — Moyo v Attorney-General** (2022-02-28)
  - Outcome: `dismissed`
  - Detail: "We therefore decline to grant the Petitioner the …"
  - Source: `pdf-tail-2pages[v031-tail:\bwe\s+(?:therefore\s+|accordingly\s+){0,3}decline\s+to\s+grant\b]`
  - Judges (parse_judges_v032 no-comma fix): Sitali (JCC), Mulenga (JCC), Mulonda (JCC), Munalula (JCC), Chisunka (JC). All resolved; Chisunka's prior alias set already includes both `JCC` and `JC` titles, so registry write needed only to confirm continuity.
  - Record id: `judgment-zm-2022-zmcc-05-moyo-v-attorney-general`

## Deferrals (specific reason codes; raw retained on disk)

All five deferred under `html_no_summary_pdf_no_match`. Per-record one-liner:

- **zmcc/2022/11 — Chisanga and Anor v Electoral Commission of Zambia** (2022-05-16). Flynote: "Filing the record of appeal outside the 30-day period without leave renders the appeal incompetent and dismissible." Declaratory holding ("dismissible" not "dismissed"); operative paragraph absent from extracted PDF tail under v0.3.2 vocabulary.
- **zmcc/2022/10 — Lungu v Attorney General and Ors** (2022-05-19). Flynote: "Constitutional Court may stay criminal proceedings pending determination of constitutional questions, including where immunity or nolle prosequi is alleged." Declaratory; no operative-disposition verb match in summary or PDF tail.
- **zmcc/2022/9 — Tembo v Attorney General** (2022-03-14). Flynote: "Whether non-publication of presidential asset declarations breached Article 52(3) absent statutory prescription." Interpretive declaratory; no operative-verb match.
- **zmcc/2022/7 — Law Association of Zambia v Attorney-General** (2022-03-22). Flynote: "A Member of Parliament whose election is nullified and who appeals to the Constitutional Court retains the seat pending determination of the appeal." Declaratory; no operative-verb match. Already classified the same way under v0.3.1 in b0371; v0.3.2 confirms the diagnosis.
- **zmcc/2022/6 — Malanji v Mulenga and Anor** (2022-02-24). Flynote: "Whether an appellate court should admit fresh evidence under s25(1)(b) where documents were available before trial." Interpretive; no operative-verb match.

## Integrity check (post-write)

| Check | Result |
|-------|--------|
| Records total | 83 (was 80; +3) |
| Unique IDs | 83/83 |
| Provenance complete (4-field base) | 83/83 |
| `source_hash` shape `sha256:...` | 83/83 |
| `source_hash` resolves on disk | 83/83 |
| Spot-recompute (n=6, seed=489) | 6/6 |
| Phase-5 cross-refs unresolved | 0 |
| Judges resolve in registry | all (3 ZMCC records, 13 judge-aliases all on existing canonical entries) |
| Outcome enum (v0.3.x records) | 0 invalid |
| Court breakdown | ZMCC 58 / ZMSC 24 / SCZ-pilot 1 |
| Raw tree (informational) | 3203 files / 2926 unique sha256 |

**ALL_INTEGRITY_PASS.**

## Phase 5 progress

- Records: 80 → 83 (target 100–160; 17 short of low end)
- ZMCC backlog after this batch: 86 raw-on-disk no-record candidates remain (was 89 → −3 written)
- Five-consecutive-zero-discovery completion criterion remains UN-FIRED (b0488 un-fired it; b0489 produced new records)

## Recommendation for next tick (b0490)

Continue the v0.3.2 sweep down the same DESC slice. Next eight ZMCC candidates (b0488 recommendation minus b0489's hits): zmcc/2022/{11, 10, 9, 7, 6, 4, 3, 2} OR pivot to zmcc/2022/{4, 3, 2, 1} + zmcc/2021/{21, 18, 12} to clear remaining `parser_v0.3.1_judges_no_comma_unhandled` (4, 3, 2 are all judges_no_comma; 1, 21, 18, 12 are html_no_summary). The judges_no_comma DESC remainder is small (only zmcc/2022/{4, 3, 2} after this batch); after those are addressed the remaining work is dominated by html_no_summary_pdf_no_match — likely lower yield, but still worth running before pivoting.

ZMSC older-year sweep is approved by Peter (2026-05-03) but the canonical source URL pattern remains pending Peter confirmation. Until that confirmation arrives via Cowork, scheduled ticks continue reparse-first only.
