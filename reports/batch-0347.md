# Batch 0347 — Phase 5 ZMCC ingestion (continuation)

**Date (UTC):** 2026-04-29
**Phase:** phase_5_judgments (approved+incomplete)
**Slice:** ZMCC 2025/{10, 9, 8, 7, 6, 5, 4, 3} — 8-candidate slice next-after b0346, going most-recent-first.
**Parser version:** 0.3.0 (frozen from b0344, unchanged through b0345/b0346/b0347)
**Fetcher:** dateless canonical URL pattern (frozen from b0346)

## Fetch

All 8 fetches OK. Raw HTML+PDF pairs persisted to
`raw/zambialii/judgments/zmcc/2025/`.

| # | Date (from redirect) | HTML bytes | PDF bytes |
|---|----------------------|------------|-----------|
| 10 | 2025-06-04 | 50,267 | (varies) |
| 9  | 2025-02-10 | 50,224 | (varies) |
| 8  | 2025-04-01 | 50,234 | (varies) |
| 7  | 2025-04-07 | 43,548 | 5,206,441 |
| 6  | 2025-03-24 | 45,662 | 15,738,773 |
| 5  | 2025-03-24 | 44,670 | 10,259,252 |
| 4  | 2025-02-20 | 51,835 | 16,749,916 |
| 3  | 2025-03-06 | 46,681 | 10,790,530 |

Fetcher: `scripts/batch_0347_fetch.py` (driven from b0346 with new TARGETS slice; all other logic byte-identical).

## Parse

`scripts/batch_0347_parse.py` (parser_version 0.3.0, frozen from b0346)
wrote **1 record** and **deferred 7**.

### Written

| ID | Citation | Date | Outcome | Outcome source |
|----|----------|------|---------|----------------|
| `judgment-zm-2025-zmcc-04-brenda-mpashi-v-attorney-general-and-anor` | [2025] ZMCC 4 | 2025-02-20 | dismissed | pdf-anchor:`the following orders` |

Brenda Mpashi v Attorney General and Anor — outcome inferred from the
PDF order section ("The Petition is hereby dismissed"). Panel:
Musaluke (presiding), Chisunka (concurring), Kawimbe (concurring) — all
JJC. The summary itself did not contain a verb on the locked enum, so
fall-through to the PDF order anchor was used; the matched anchor was
"the following orders" within an 800-char window of the order
paragraph.

### Deferred (no fabrication — per BRIEF.md non-negotiable #1)

All seven deferrals are `outcome_not_inferable_under_tightened_policy`.
Raw HTML+PDF remain on disk and can be revisited later if the parser
acquires hand-anchored PDF order paragraphs or the locked summary regex
list is widened (a parser_version bump, not a tick-time change).

| Candidate | Summary head |
|-----------|--------------|
| [2025] ZMCC 10 — Munir Zulu v AG and Ors (2025-06-04) | "Imprisonment automatically vacates a parliamentary seat; appeals do not suspend the constitutional vacancy or by-election." (Substantive ratio; no disposition verb in summary.) |
| [2025] ZMCC 9 — The People v Attorney General (2025-02-10) | "Imprisonment of an MP automatically vacates the seat and triggers a by-election; appeals do not suspend that process." (Same ratio family as ZMCC 10; no enum verb.) |
| [2025] ZMCC 8 — Richard Sakala v Attorney General (2025-04-01) | "Constitutional petitions are not governed by the Limitation Act 1939, but inordinate unexplained delay may justify dismissal." (Conditional/contingent verb; no clean enum match.) |
| [2025] ZMCC 7 — Munir Zulu v AG and Ors (2025-04-07) | "The Constitutional Court has no jurisdiction under Article 128(2) to stay subordinate court proceedings; the trial court must stay and refer constitutional questions." (Jurisdictional ratio; no disposition verb.) |
| [2025] ZMCC 6 — Miles Bwalya Sampa v Attorney General (2025-03-24) | "Interlocutory subpoenas denied for lack of prior steps, specificity, and demonstrated relevance to Article 210 challenge." ("denied" not on locked enum — would require parser bump.) |
| [2025] ZMCC 5 — Miza Phiri Jr v Isaac Mwanza and Ors (2025-03-24) | "A petitioner cannot file a new petition to challenge another pending petition; proper remedy is joinder, and such filings may be abuse of process." (Procedural ratio; no enum verb.) |
| [2025] ZMCC 3 — Petrushika Trading Limited v AG (2025-03-06) | "Challenge to section 21(4) dismissed: statutory certificate procedure and alternative remedies render it not unconstitutional on these facts." (Verb is "dismissed" but subject is "Challenge", which is not in the locked SUMMARY_PATTERNS subject vocabulary — the locked patterns intentionally enumerate appeal/petition/application/action/matter only. Not loosened mid-tick.) |

Raw HTML+PDF for all seven remain on disk under
`raw/zambialii/judgments/zmcc/2025/` and can be revisited by a later
batch with hand-anchored PDF order paragraphs once the parser supports
them. No re-fetch will be required.

## Integrity checks (PASS)

`scripts/integrity_check_b0347.py`:

- 1/1 unique ID (no collisions across 41 records under `records/judgments/`)
- 1/1 records have all 20 required fields
- 1/1 outcome ∈ enum (dismissed)
- 1/1 court ∈ enum (Constitutional Court of Zambia)
- 1/1 ≥1 judge resolves in registry (3/3 — Musaluke, Chisunka, Kawimbe — all canonicals already present)
- 1/1 judges[*].role ∈ enum (presiding/concurring)
- 1/1 ≥1 issue_tag from Flynote (7 tags)
- 1/1 source_hash matches raw HTML on disk
- 1/1 raw_sha256 matches raw PDF on disk
- 1/1 ID matches locked pattern `^judgment-zm-[a-z0-9-]+$`
- 1/1 date matches `YYYY-MM-DD`
- outcome_detail safety: 32 chars, no blacklist substrings, no leading lowercase mid-word fragment, ≥12 alphabetic chars
- Cross-corpus: 1736 record IDs total; 5 pre-existing duplicates from b0128/b0264/b0289 acts/SI lineage (unchanged); new judgment ID is globally unique. No unresolved amended_by/repealed_by/cited_authorities references in the new record.

## judges_registry.yaml

No new canonicals. All three panel surnames (Musaluke, Chisunka,
Kawimbe) and their JJC titles were already in the registry from b0345.
No aliases added.

## Budget impact

- Fetches this tick: 16 (8 HTML + 8 PDF, dateless canonical pattern)
- Cumulative today: 110 → 126 / 2000 (~6.3%)
- B2 sync: deferred to host (rclone not in sandbox)

## Phase 5 progress

- 16 / 100–160 target (was 15 at b0346 end-state; +1 this tick).
- ZMCC 2025 ingested: {4, 13, 20, 26, 27, 29, 31}.
- ZMCC 2025 deferred (raw on disk): {3, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25, 28, 30, 32, 33} + 2026/01.
- ZMCC 2025/{1, 2} not yet attempted.

## Next tick

Continue ZMCC sweep: small remaining slice 2025/{2, 1} (only 2 candidates left in 2025 numeric sequence under the dateless-canonical fetch). Consider also stepping back into ZMCC 2024 for the remainder of the 8-record budget under the same parser_version 0.3.0 policy.
