# Batch 0346 — Phase 5 ZMCC 2025 sweep (most-recent-first, slice 11–18)

- **Tick start:** 2026-04-29T14:32Z
- **Phase:** phase_5_judgments (lowest approved + incomplete)
- **Source:** ZambiaLII Constitutional Court of Zambia — fresh fetch of 8
  judgments from the 2025 docket (ZMCC 2025/18 down to 2025/11).
- **Bounded unit:** Fetch + parse 8 candidates under the tightened
  `parser_version: 0.3.0` policy locked in at b0344. No policy change
  this tick.
- **Fetcher upgrade:** dates were discovered at fetch time by hitting the
  dateless canonical URL (`/akn/zm/judgment/{court}/{year}/{num}/eng`),
  which ZambiaLII 302-redirects to the dated form. This removes the need
  for a hand-curated index probe before each ZMCC slice.
- **Result:** 1 record written, 7 deferred (per non-negotiable #1).

## Records written (1)

| ID | Citation | Date | Outcome | Source | Judges |
| --- | --- | --- | --- | --- | --- |
| `judgment-zm-2025-zmcc-13-issac-mwanza-and-anor-v-the-attorney-general-and-o` | [2025] ZMCC 13 | 2025-07-25 | dismissed | summary: "Constitutional Court lacked proper forum for Bill of Rights challenge to Penal Code; petition dismissed and costs borne by parties" | Shilimi DPC (presiding), Musaluke, Chisunka, Mulongoti, Mwandenga, Kawimbe, Mulife |

The outcome was resolved from the PRIMARY summary source (no PDF anchor
fallback required). All 7 panel-member judges resolve to existing
canonicals in `judges_registry.yaml`. One title — `DPC` (Deputy
President) — was newly observed on Shilimi (already canonical with
`JCC`); the alias `Shilimi DPC` was appended.

## Deferred (7) — recorded in `gaps.md`

All seven summaries describe holdings, issues, or ratio decidendi without
an enum-mappable disposition phrase, AND no eligible PDF order anchor
match was found within the strict 800-character window. Per BRIEF.md
non-negotiable #1 (no fabrication), no record was written.

| ID candidate | Summary head |
| --- | --- |
| [2025] ZMCC 18 — TC Promotions Ltd v Lusaka City Council (2025-09-30) | "Whether a local authority resolution increasing advertising fees is a statutory instrument requiring gazetting and reporting under Articles 67 and 199." (Issue framing; no disposition verb.) |
| [2025] ZMCC 17 — Isaac Mwaanza (2025-08-27) | "Petitioner had standing but challenge to parliamentary vacancy improperly filed in Constitutional Court; vacancy questions fall to High Court/tribunal under section 96 EPA." (Jurisdictional ratio; no disposition verb.) |
| [2025] ZMCC 16 — Miles Bwalya Sampa v AG and 4 Ors (2025-08-25) | "A single judge may grant an extension to file amicus materials; delay condoned in the interests of justice, but costs awarded." (Procedural ruling; "condoned" not on enum.) |
| [2025] ZMCC 15 — Tresford Chali v Judicial Complaints Commission (2025-07-23) | "A citizen acting in the public interest has standing to challenge alleged constitutional contraventions before the Constitutional Court." (Locus-standi ratio; no disposition verb.) |
| [2025] ZMCC 14 — The People v John Sinkamba and Ors (2025-07-28) | "Article 266 defines a child as any person below eighteen; attaining eighteen confers adult status under the Constitution." (Substantive ratio; no disposition verb.) |
| [2025] ZMCC 12 — Munir Zulu and Anor v Attorney General (2025-06-27) | "Court holds it can review pre-Bill executive initiation of constitutional amendments and requires people-driven wide consultations." (Jurisdictional/procedural ratio; "holds … can review" not on enum.) |
| [2025] ZMCC 11 — Ford Chombo v Attorney General (2025-06-19) | "A pre-2016 pension dispute is a labour matter and outside the Constitutional Court's jurisdiction." (Jurisdictional ratio; no disposition verb.) |

Raw HTML+PDF for all seven remain on disk under
`raw/zambialii/judgments/zmcc/2025/` and can be revisited by a later
batch with hand-anchored PDF order paragraphs once the parser supports
them. No re-fetch will be required.

## Integrity checks (PASS)

`scripts/integrity_check_b0346.py`:

- 1/1 unique ID (no collisions across 40 records under `records/judgments/`)
- 1/1 records have all 20 required fields
- 1/1 outcome ∈ enum (dismissed)
- 1/1 court ∈ enum (Constitutional Court of Zambia)
- 1/1 ≥1 judge resolves in registry (7/7 — Shilimi, Musaluke, Chisunka,
  Mulongoti, Mwandenga, Kawimbe, Mulife — all canonicals already present)
- 1/1 judges[*].role ∈ enum
- 1/1 ≥1 issue_tag from Flynote (4 tags)
- 1/1 source_hash matches raw HTML on disk
- 1/1 raw_sha256 matches raw PDF on disk
- 1/1 ID matches locked pattern `^judgment-zm-[a-z0-9-]+$`
- 1/1 date matches `YYYY-MM-DD`
- outcome_detail safety: 130 chars, no blacklist substrings, no leading
  lowercase mid-word fragment, ≥12 alphabetic chars

## Budget impact

- Fetches this tick: 16 (8 HTML + 8 PDF)
- Cumulative today: 94 → 110 / 2000 (~5.5%)
- B2 sync: deferred to host (rclone not in sandbox)

## Phase 5 progress

- 15 / 100–160 target (was 14 at b0345 end-state; +1 this tick).
- ZMCC 2025 ingested: {13, 20, 26, 27, 29, 31}.
- ZMCC 2025 deferred: {11, 12, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24,
  25, 28, 30, 32, 33} + 2026/01 (raw on disk).
- ZMCC 2025/{1..10} not yet attempted.

## Next tick

Continue ZMCC 2025 sweep most-recent-first from 2025/10 backwards to
2025/03 (8-candidate slice) under the same parser_version 0.3.0 policy.
Same dateless-canonical fetcher pattern.
