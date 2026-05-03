# Batch 0491 — parser_v0.3.2 reparse pass (zmcc 2022 untested-under-v0.3.2 html_no_summary slice)

- **Tick start (UTC):** 2026-05-03T~10:30Z (scheduled tick)
- **Phase:** 5 (judgments) — approved+incomplete
- **Action:** fourth v0.3.2 reparse pass; tests the eight ZMCC 2022 candidates that were classified `html_no_summary_pdf_no_match` under parser_v0.3.1 in batches b0368/b0369 but never re-tested under v0.3.2's widened SUMMARY_PATTERNS_V032 / PDF_TAIL_PATTERNS_V032 vocabulary plus the ORDER_INTRO + window-scan resolver.
- **Records written:** 0
- **Records deferred:** 8 (all `html_no_summary_pdf_no_match` re-confirmed under v0.3.2)
- **Cumulative today:** 0/2000 fetches; ~5k tokens (parser script copy + report)
- **Yield this tick:** 0/8 = 0% — v0.3.2's vocabulary widening did not unblock any of these eight specifically (the patterns added in v0.3.2 cover refusal/granted/conviction-confirmed/case-withdrawn/declaratory-academic forms, but these eight present interpretive/declaratory framings whose operative verbs are still outside both v0.3.1 and v0.3.2 SUMMARY/TAIL patterns).

## Targets and selection

Per b0490's recommendation — "ZMCC 2022 untested-under-v0.3.2 html_no_summary candidates: 17, 18, 22, 23, 24, 27, 30, 31 (8 records)" — this tick exhausts the remaining 2022 ZMCC `html_no_summary_pdf_no_match` slice that had not yet been retried under v0.3.2. All eight HTML+PDF pairs already on disk; this run consumed 0 fresh fetches.

## Deferrals (specific reason codes; raw retained on disk)

All eight deferred under `html_no_summary_pdf_no_match` (re-confirmed under v0.3.2):

- **zmcc/2022/17 — Zimba v Attorney General (CCZ 7 of 2022)** (2022-08-31). Flynote: "The DPP is amenable to the JCC's disciplinary/removal process under Article 182(3) read with Articles 143 and 144." Declaratory ratio statement; no operative-disposition token in flynote, no SUMMARY/TAIL match in v0.3.2's widened vocabulary. URL: https://zambialii.org/akn/zm/judgment/zmcc/2022/17/eng@2022-08-31.

- **zmcc/2022/18 — Malanji and Anor v Attorney General and Anor (CCZ 18 of 2022)** (2022-09-07). Flynote: "Article 72(4) bars only those who caused vacancies in the specific instances listed in Article 72(2); judicial nullification is excluded." Interpretive declaratory with no operative verb match under v0.3.1 or v0.3.2 patterns. URL: https://zambialii.org/akn/zm/judgment/zmcc/2022/18/eng@2022-09-07.

- **zmcc/2022/22 — Kachize Phiri and Anor v Electoral Commission of Zambia (CCZ/A 4 of 2022)** (2022-09-23). Flynote: "Whether a parliamentary election appeal was competently before the Constitutional Court after High Court leave to appeal out of time was granted." Procedural-competency disposition; no operative verb match. URL: https://zambialii.org/akn/zm/judgment/zmcc/2022/22/eng@2022-09-23.

- **zmcc/2022/23 — Sinkamba and Anor v Electoral Commission of Zambia (CCZ 23 of 2022)** (2022-10-17). Flynote: "Whether the Electoral Commission breached Article 52(6) by not cancelling elections after candidate resignations, and effect of a court stay." Operative verbs not in either v0.3.1 or v0.3.2 SUMMARY_PATTERNS; PDF tail produced no safe match. URL: https://zambialii.org/akn/zm/judgment/zmcc/2022/23/eng@2022-10-17.

- **zmcc/2022/24 — Kanengo v Attorney General and Anor** (2022-10-20). Flynote: "The 21-day constitutional time limit…cannot be stopped or extended by any court or authority." Pure interpretive declaratory with no operative disposition verb in either v0.3.x vocabulary. URL: https://zambialii.org/akn/zm/judgment/zmcc/2022/24/eng@2022-10-20.

- **zmcc/2022/27 — Sangwa v Attorney General** (2022-11-10). Flynote: "Court dismisses functus officio objection and allows constitutional challenge to section 30 (costs) to proceed to hearing." Mixed-disposition interlocutory order (one objection dismissed; another challenge allowed to proceed) — not a final disposition; v0.3.2's widened vocabulary does not safely resolve compound interlocutory orders. URL: https://zambialii.org/akn/zm/judgment/zmcc/2022/27/eng@2022-11-10.

- **zmcc/2022/30 — Sikazwe v Attorney General and Anor** (2022-11-11). Flynote: joinder application by intended second respondent refused. The operative verb "joinder refused" is still not in v0.3.2's SUMMARY_PATTERNS_V032 (which added "refused" patterns for application/petition/relief but not for joinder); PDF tail no match. URL: https://zambialii.org/akn/zm/judgment/zmcc/2022/30/eng@2022-11-11.

- **zmcc/2022/31 — Mutwena v Attorney General** (2022-01-19). Flynote: refusal to interpret Article 52(6) on the basis of a speculative challenge. Refusal-to-interpret ("declined to determine") form is outside the application/petition/conviction refusal set in SUMMARY_PATTERNS_V032; PDF tail no match. URL: https://zambialii.org/akn/zm/judgment/zmcc/2022/31/eng@2022-01-19.

## Integrity check (post-write)

| Check | Result |
|-------|--------|
| Records total | 89 (was 89; +0) |
| Unique IDs | 89/89 |
| Provenance complete (4-field base) | 89/89 |
| `source_hash` shape `sha256:...` | 89/89 |
| `source_hash` resolves on disk | 89/89 |
| Spot-recompute (n=6, seed=491) | 6/6 |
| Phase-5 cross-refs unresolved | 0 |
| Judges resolve in registry (v0.3.x) | 205/205 judge-aliases all resolve |
| Outcome enum (v0.3.x records, n=55) | 0 invalid |
| v0.3.x records with no judges / empty issue_tags | 0 / 0 |
| Court breakdown | ZMCC 64 / ZMSC 24 / SCZ-pilot 1 = 89 |
| Raw tree (informational) | 3203 files / 2926 unique sha256 |

**ALL_INTEGRITY_PASS.**

## gaps.md updates

Eight `RECONFIRMED-DEFERRED in batch-0491` notes appended under the original parser_v0.3.1 deferred-list entries for zmcc/2022/{17, 18, 22, 23, 24, 27, 30, 31} per the BRIEF.md "RESOLVED-line append under the original gaps.md entry; never delete the entry" rule. No deletions.

## Phase 5 progress

- Records: 89 → 89 (target 100–160; 11 short of low end). No movement this tick.
- ZMCC 2022 raw-on-disk no-record backlog after this batch: written {2, 3, 4, 5, 8, 12, 15, 19, 20, 21, 25, 26, 28, 29, 32, 34} (16 records); deferred {1, 6, 7, 9, 10, 11, 13, 14, 17, 18, 22, 23, 24, 27, 30, 31, 33} (17 records); OCR-pending {16}. The full 2022 ZMCC raw-on-disk inventory has now been re-tested under v0.3.2 — the judges_no_comma sub-backlog is empty and the html_no_summary_pdf_no_match sub-backlog is fully re-confirmed under v0.3.2.
- Five-consecutive-zero-discovery completion criterion: NOT fired this tick. b0488/b0489/b0490 were three consecutive substantive ticks (un-firing the criterion); b0491 is now a single zero-write tick. Four more consecutive zero-write substantive ticks would re-fire the criterion under the BRIEF.md threshold; this tick alone does not.

## Recommendation for next tick (b0492)

The 2022 ZMCC reparse-first inventory is now exhausted under v0.3.2 (every raw-on-disk no-record candidate has been re-tested at the current parser version). Per b0490's secondary recommendation, the next high-yield path is:

1. **Pivot to ZMCC 2024 untested-under-v0.3.2 candidates.** Per b0490: the 2024 raw-on-disk no-record backlog is fully classified under v0.3.1 across b0373-b0374; many entries are `parser_v0.3.1_judges_no_comma_unhandled` (will yield cleanly under v0.3.2's parse_judges_v032 no-comma fix) and several are `html_no_summary_pdf_no_match` for declaratory rulings. The judges-no-comma sub-class produced 6/8 = 75% yield in b0490 against ZMCC 2022 — the same fix should produce comparable yield against ZMCC 2024.

2. **ZMCC 2023 untested-under-v0.3.2 candidates** — same logic; gaps.md entries at b0361..b0367 captured several 2023 deferrals.

3. **ZMCC 2025 untested-under-v0.3.2 candidates** — gaps.md b0362..b0364 captured several `html_no_summary_pdf_no_match` 2025 deferrals; v0.3.2 vocabulary may unblock declaratory-academic style rulings.

The cleanest continuation is option 1 (ZMCC 2024) since b0490 already identified it as next-in-line and the 2022 sweep is now formally exhausted.

The ZMSC older-year sweep remains pending Peter's confirmation of the canonical source URL pattern (per `approvals.yaml.zmsc_older_year_sweep_approval_note`); not actionable by scheduled tick until that confirmation arrives.

The zero-write outcome of this tick does not warrant any approvals.yaml change — Phase 5 remains `approved: true / complete: false` per the human-only confirmation rule. No flips.
