# Batch 0345 — Phase 5 ZMCC 2025 sweep (most-recent-first, slice 19–26)

- **Tick start:** 2026-04-29T14:19Z
- **Phase:** phase_5_judgments (lowest approved + incomplete)
- **Source:** ZambiaLII Constitutional Court of Zambia — fresh fetch of 8
  judgments from the 2025 docket (ZMCC 2025/26 down to 2025/19).
- **Bounded unit:** Fetch + parse 8 candidates under the tightened
  `parser_version: 0.3.0` policy locked in at b0344. No policy change
  this tick.
- **Result:** 2 records written, 6 deferred (per non-negotiable #1).

## Records written (2)

| ID | Citation | Date | Outcome | Source | Judges |
| --- | --- | --- | --- | --- | --- |
| `judgment-zm-2025-zmcc-26-jayesh-shah-v-attorney-general` | [2025] ZMCC 26 | 2025-11-18 | dismissed | summary: "The applicant's challenge to the Court of Appeal was a veiled appeal, not a constitutional question; petition dismissed with costs" | Munalula (presiding), Shilimi, Chisunka, Mwandenga, Kawimbe |
| `judgment-zm-2025-zmcc-20-edward-bwalya-phiri-v-attorney-general` | [2025] ZMCC 20 | 2025-10-03 | dismissed | summary: "Court held section 5(1) did not unlawfully expand the Emoluments Commission's mandate; petition dismissed" | Shilimi (presiding), Munalula, Musaluke, Chisunka, Mulife, Mwandenga, Mulongoti |

Both outcomes resolved from the PRIMARY summary source (no PDF anchor
fallback required). All 12 panel-member judges resolve to existing
canonicals in `judges_registry.yaml`. No new canonicals were created;
no new aliases or titles were added (the tightened name parser already
maps the surname tokens encountered to bare-surname canonicals).

## Deferred (6) — recorded in `gaps.md`

All six summaries describe holdings, issues, or ratio decidendi without
an enum-mappable disposition phrase, AND no eligible PDF order anchor
match was found within the strict 800-character window. Per BRIEF.md
non-negotiable #1 (no fabrication), no record was written.

| ID candidate | Summary head |
| --- | --- |
| [2025] ZMCC 25 — Tresford Chali v Attorney General (2025-12-04) | "Court refused stay of Speaker's vacancy ruling absent special and convincing grounds; merits not to be decided interlocutorily." (Phrase "refused stay" is not an enum verb; "Application for X dismissed" pattern requires a literal "dismissed" verb.) |
| [2025] ZMCC 24 — Law Association of Zambia v Speaker of National Assembly (2025-11-28) | "The Constitutional Court held the Attorney General may represent the Speaker as the legal representative of 'Government' and ordered joinder of the Attorney General." (Phrase "ordered joinder" is not on the locked `joinder granted` / `granted joinder` pattern.) |
| [2025] ZMCC 23 — Emmanuel Kayuni v Bwalya (2025-11-27) | "A pension-quantum and payroll dispute is a labour matter for the Industrial Relations Division, not the Constitutional Court." (Jurisdictional ratio; no disposition phrase.) |
| [2025] ZMCC 22 — Sean Tembo (Tonse Alliance) v Attorney General (2025-11-27) | "Declaratory relief was academic; transitional Act provisions governed eligibility, and Article 267(3)(b)(c) did not affect the Court's decision." (Ratio only.) |
| [2025] ZMCC 21 — Law Association of Zambia v Attorney General (2025-11-25) | "Application to suspend a presidentially appointed constitutional Technical Committee dismissed for failing to show irreparable harm." (Word "dismissed" is far from "Application", separated by a long noun phrase; locked `Application for <X> dismissed` pattern requires the noun phrase to follow `for` with ≤4 word tokens before `dismissed`.) |
| [2025] ZMCC 19 — BetBio Zambia Ltd v Attorney General (2025-09-30) | Empty `<dd>` summary on the ZambiaLII page; PDF order anchor sweep yielded no enum-mappable phrase. |

The raw HTML+PDF for all six remain on disk at
`raw/zambialii/judgments/zmcc/2025/` so a future tick (or a parser
extension) can revisit without re-fetching.

## Integrity checks (this batch)

- 2/2 unique IDs (no collisions across `records/judgments/`).
- 2/2 records have all 20 required fields per the judgment schema.
- 2/2 outcomes ∈ {`allowed`, `dismissed`, `upheld`, `overturned`,
  `remitted`, `struck-out`, `withdrawn`}.
- 2/2 court ∈ {`Constitutional Court of Zambia`, ...}.
- 2/2 ≥1 judge; all 12 `judges[*].name` resolve in
  `judges_registry.yaml` (via direct or first-token match).
- 2/2 `judges[*].role` ∈ {`presiding`, `concurring`, ...}.
- 2/2 ≥1 `issue_tag` parsed from the Flynote.
- 2/2 `source_hash` matches sha256 of on-disk raw HTML.
- 2/2 `raw_sha256` matches sha256 of on-disk raw PDF.
- 2/2 IDs match the locked id-pattern `^judgment-zm-[a-z0-9-]+$`.
- 2/2 `date_decided` matches `YYYY-MM-DD`.

PASS. (5 pre-existing dup-id files in `records/acts/` from
b0128/b0264/b0289 lineage are unchanged this batch — not regressions.)

## Budget impact

- Fresh fetches this tick: **16** (8 HTML + 8 PDF, all from
  `zambialii.org` at the configured 5 s rate limit).
- Cumulative today: **78 → 94 / 2000 fetches (~4.7 %)**.
- Token budget: ~unchanged (no LLM calls).

## Phase 5 progress

- **Records to date:** 14 / 100–160 target (was 12 at b0344 end; +2 this tick).
- **ZMCC 2026:** unchanged (8 of 10 records ingested; 2026/01 deferred).
- **ZMCC 2025:** 5 records ingested in total (2025/{20, 26, 27, 29, 31}).
- **ZMCC 2025 deferred:** 11 (2025/{19, 21, 22, 23, 24, 25, 28, 30, 32, 33}
  + 2026/01) — all with raw on disk.
- **ZMCC 2025/{1..18}** not yet attempted.

## B2 sync

Deferred to host. `rclone` not available in the sandbox (consistent
with prior 4 ticks; logged in `worker.log`).

## Next tick

- Continue ZMCC 2025 sweep — most-recent-first from 2025/18 backwards,
  using the same `parser_version: 0.3.0` policy.
- A future enhancement (not attempted here, to keep parser policy stable)
  could safely add patterns for a few high-confidence summary phrasings
  (e.g. "Application to <verb-phrase> dismissed", "ordered joinder" /
  "joinder ordered"), but ONLY after a controlled review of the false-
  positive risk on the existing on-disk corpus.
