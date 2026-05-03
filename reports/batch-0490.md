# Batch 0490 — parser_v0.3.2 reparse continuation (zmcc 2022 judges_no_comma sweep)

- **Tick start (UTC):** 2026-05-03T09:35Z (scheduled tick)
- **Phase:** 5 (judgments) — approved+incomplete
- **Action:** third v0.3.2 reparse pass; clears the remaining `parser_v0.3.1_judges_no_comma_unhandled` candidates flagged in b0371/b0489 (zmcc/2022/{4, 3, 2, 32, 25, 15}) plus two prior `html_no_summary_pdf_no_match` candidates (zmcc/2022/{13, 14}) tested against v0.3.2's widened SUMMARY/TAIL vocabulary.
- **Records written:** 6 (zmcc/2022/{04, 03, 02, 32, 25, 15})
- **Records deferred:** 2 (zmcc/2022/{13, 14}) — both `html_no_summary_pdf_no_match` (re-confirmed under v0.3.2)
- **Cumulative today:** 0/2000 fetches; ~6k tokens (parser script copy + report)
- **Yield this tick:** 6/8 = 75% (vs b0489's 3/8 = 37.5%; v0.3.2 judges-no-comma fix is producing high marginal yield as the bench-format-blocked candidates with operative phrases in PDF tails get cleared)

## Targets and selection

The b0489 report recommended continuing with zmcc/2022/{11, 10, 9, 7, 6, 4, 3, 2}. Of those, b0489 had already deferred {11, 10, 9, 7, 6} as `html_no_summary_pdf_no_match` under v0.3.2 (re-running them would yield identical deferrals). This tick therefore prioritised the four still-unattempted-under-v0.3.2 `parser_v0.3.1_judges_no_comma_unhandled` candidates ({4, 3, 2, 32}, {25}, {15}) plus two unattempted `html_no_summary_pdf_no_match` candidates from earlier batches ({13, 14}) to fill the slot. All eight HTML+PDF pairs already on disk; this run consumed 0 fresh fetches.

## Resolutions

- **[2022] ZMCC 4 — Chapter One Foundation Ltd v Attorney-General** (2022-02-25)
  - Outcome: `dismissed`
  - Detail: "The Petition is accordingly dismissed"
  - Source: `pdf-tail-2pages[v031-tail]` (subject-passive `... is dismissed` pattern)
  - Judges (parse_judges_v032 no-comma fix): Chibomba (PC), Mulenga (JCC), Munalula (JCC), Musaluke (JCC), Mulongoti (JCC). All resolved against existing canonical entries.
  - Record id: `judgment-zm-2022-zmcc-04-chapter-one-foundation-ltd-v-attorney-general`

- **[2022] ZMCC 3 — Shah and Anor v The Attorney-General** (2022-01-25)
  - Outcome: `dismissed`
  - Detail: "[60] This Petition fails and is hereby dismissed"
  - Source: `pdf-tail-2pages[v031-tail]` (`petition fails` pattern)
  - Judges (parse_judges_v032 no-comma fix): Mulenga (JCC), Mulonda (JCC), Munalula (JCC), Musaluke (JCC), Mulongoti (JCC). All resolved against existing canonical entries.
  - Record id: `judgment-zm-2022-zmcc-03-shah-and-anor-v-the-attorney-general`

- **[2022] ZMCC 2 — Lieutenant Muchindu v Attorney-General** (2022-01-27)
  - Outcome: `dismissed`
  - Detail: "We accordingly dismiss it for want of …"
  - Source: `pdf-tail-2pages[v031-tail]` (active `we accordingly dismiss` pattern)
  - Judges (parse_judges_v032 no-comma fix): Mulenga (JCC), Mulonda (JCC), Musaluke (JCC). All resolved against existing canonical entries.
  - Record id: `judgment-zm-2022-zmcc-02-lieutenant-muchindu-v-attorney-general`

- **[2022] ZMCC 32 — Mwamba v Chewe and Anor** (2022-07-15)
  - Outcome: `dismissed`
  - Detail: "[40] The application fails on that account and it is dismissed"
  - Source: `pdf-tail-2pages[v031-tail]` (`application fails` pattern)
  - Judges (parse_judges_v032 no-comma fix): Munalula (JCC), Sitali (JCC), Mulenga (JCC), Musaluke (JCC), Mulongoti (JCC). All resolved against existing canonical entries.
  - Record id: `judgment-zm-2022-zmcc-32-mwamba-v-chewe-and-anor`

- **[2022] ZMCC 25 — Institute of Law, Policy Research and Human Rights v ...** (2022-10-21)
  - Outcome: `dismissed`
  - Detail: "(59) The Petition fails and is hereby dismissed"
  - Source: `pdf-tail-2pages[v031-tail]` (`petition fails` pattern)
  - Judges (parse_judges_v032 no-comma fix): Munalula (JCC), Mulenga (JCC), Musaluke (JCC), Chisunka (JCC). All resolved against existing canonical entries.
  - Record id: `judgment-zm-2022-zmcc-25-institute-of-law-policy-research-and-human-rights`

- **[2022] ZMCC 15 — Mutelo K v Kang'ombe and Anor (CCZ/A 33 of 2021)** (2022-07-29)
  - Outcome: `upheld`
  - Detail: "Consequently, we uphold the judgment of the trial court"
  - Source: `pdf-tail-2pages[v032-tail]` — NEW in v0.3.2 (the `we uphold the <noun>` simpler form added in PDF_TAIL_PATTERNS_V032 to fix the v0.3.1 backtracking gap on `we <verb> the <noun>` constructions)
  - Judges (parse_judges_v032 no-comma fix): Sitali (JCC), Mulenga (JCC), Mulonda (JCC), Chisunka (JCC), Mulongoti (JCC). All resolved against existing canonical entries.
  - Record id: `judgment-zm-2022-zmcc-15-mutelo-k-v-kang-ombe-and-anor`

## Deferrals (specific reason codes; raw retained on disk)

Both deferred under `html_no_summary_pdf_no_match` (re-confirmed under v0.3.2):

- **zmcc/2022/14 — Malanji v Mulenga and Anor** (2022-08-03). Flynote: "Whether a candidate's Grade 12-based eligibility can be challenged at election stage and who bears the evidential burden." Interpretive electoral-eligibility ruling; no operative-verb match in summary, no PDF tail match under v0.3.2's widened vocabulary. URL: https://zambialii.org/akn/zm/judgment/zmcc/2022/14/eng@2022-08-03.
- **zmcc/2022/13 — Lusambo v Kanengo and Anor** (2022-07-28). Flynote: "Election nullified: court found proven violence, treating and canvassing with appellant's knowledge; annulment confirmed, appeals dismissed." Mixed-disposition (annulment confirmed AND appeals dismissed) — PDF tail not yielding a single safe operative paragraph under v0.3.2. URL: https://zambialii.org/akn/zm/judgment/zmcc/2022/13/eng@2022-07-28.

## Integrity check (post-write)

| Check | Result |
|-------|--------|
| Records total | 89 (was 83; +6) |
| Unique IDs | 89/89 |
| Provenance complete (4-field base) | 89/89 |
| `source_hash` shape `sha256:...` | 89/89 |
| `source_hash` resolves on disk | 89/89 |
| Spot-recompute (n=6, seed=490) | 6/6 |
| Phase-5 cross-refs unresolved | 0 |
| Judges resolve in registry (v0.3.x) | 205 judge-aliases all resolve |
| Outcome enum (v0.3.x records, n=55) | 0 invalid |
| v0.3.x records with no judges / empty issue_tags | 0 / 0 |
| Court breakdown | ZMCC 64 / ZMSC 25 |
| Raw tree (informational) | 3203 files / 2926 unique sha256 |

**ALL_INTEGRITY_PASS.**

## Phase 5 progress

- Records: 83 → 89 (target 100–160; 11 short of low end)
- ZMCC 2022 raw-on-disk no-record backlog after this batch: written {2, 3, 4, 5, 8, 12, 15, 19, 20, 21, 25, 26, 28, 29, 32, 34} (16 records); deferred {1, 6, 7, 9, 10, 11, 13, 14, 17, 18, 22, 23, 24, 27, 30, 31, 33} (17 records); OCR-pending {16}. The judges_no_comma sub-backlog for 2022 is now empty under v0.3.2 — every remaining 2022 deferral is `html_no_summary_pdf_no_match`.
- Five-consecutive-zero-discovery completion criterion remains UN-FIRED (b0488/b0489/b0490 produced new records on three consecutive substantive ticks).

## Recommendation for next tick (b0491)

The judges_no_comma backlog under v0.3.2 is essentially exhausted across ZMCC. Remaining v0.3.2-addressable inventory is dominated by `html_no_summary_pdf_no_match` candidates that may match v0.3.2's widened SUMMARY_PATTERNS_V032 (refused/granted/conviction-confirmed/case-withdrawn/declaratory-academic) on candidates not yet retried under v0.3.2. Suggested slice for b0491:

1. **ZMCC 2022 untested-under-v0.3.2 html_no_summary candidates:** 17, 18, 22, 23, 24, 27, 30, 31 (8 records) — all classified `html_no_summary_pdf_no_match` under v0.3.1; v0.3.2 vocabulary widening (refused/granted/declaratory-academic patterns) is the most likely unblock for procedural-refusal and joinder-refused styles per the v0.3.2 launch note.
2. **Pivot to ZMCC 2024 untested:** the 2024 raw-on-disk no-record backlog is fully classified under v0.3.1 across b0373-b0374; many entries are `parser_v0.3.1_judges_no_comma_unhandled` (will yield cleanly under v0.3.2) and several are `html_no_summary_pdf_no_match` for declaratory rulings.

Option 1 is the cleaner continuation of the 2022 ZMCC sweep. Option 2 opens a new high-yield year. Either path is bounded by the same MAX_BATCH_SIZE=8 / 0-fetch budget.

ZMSC older-year sweep remains pending Peter's confirmation of the canonical source URL pattern (per approvals.yaml `zmsc_older_year_sweep_approval_note`); not actionable by scheduled tick until that confirmation arrives.
