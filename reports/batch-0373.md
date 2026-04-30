# Batch 0373 — Phase 5 ZMCC reparse-first continuation (opens 2024 backlog), parser_v0.3.1

**Date (UTC):** 2026-04-30
**Phase:** phase_5_judgments — reparse-first triage (zero fetch budget)
**Outcome:** 3 records written, 5 deferred.

## Slice rationale

b0372 closed the 2021 ZMCC sub-backlog under v0.3.1 and noted the
remaining v0.3.1-amenable inventory was empty *for ZMCC 2021*.
Cross-verifying the broader ZMCC raw-on-disk no-record set against
b0361–b0367 target lists revealed that **2024/{10–22, 25, 27}** were
deferred under parser_v0.3.0 with the legacy generic reason
`outcome_not_inferable_under_tightened_policy` and have NOT yet been
re-attempted under v0.3.1 + judges_no_comma guard. That makes them the
correct next addressable reparse-first inventory per the
`reparse_first_note` in approvals.yaml ("Only when no addressable
deferreds remain should the tick continue the fresh DESC sweep").

This tick took the DESC top-of-2024 8-slice — the maximum batch size:

- zmcc 2024/27, 25, 22, 21, 20, 19, 18, 17

Excluded: 2024/24 and 2024/26 already have records; 2024/23 has no
raw on disk (404 upstream). 2024/{10, 11, 13, 15, 16} are reserved
for the next reparse tick.

Zero fresh fetch budget consumed (all eight raw HTML+PDF pairs already
on disk under raw/zambialii/judgments/zmcc/2024/).

## Resolved (raw retained per audit policy)

- **judgment-zm-2024-zmcc-21-mildred-luwaile-v-attorney-general**
  (Mildred Luwaile v Attorney General [2024] ZMCC 21, decided 2024-10-11).
  RESOLVED in batch-0373 (parser_v0.3.1).
  Outcome: dismissed (outcome_source=pdf-tail-2pages).
  Five-judge bench: Munalula PC presiding; Sitali, Mulenga, Mwandenga,
  Mulife JJC concurring. All five resolved against existing canonical
  entries / aliases in `judges_registry.yaml` (no registry write
  needed).
  URL: https://zambialii.org/akn/zm/judgment/zmcc/2024/21/eng@2024-10-11.

- **judgment-zm-2024-zmcc-19-agnicious-mushabati-and-ors-v-national-prosecution**
  (Agnicious Mushabati and Ors v National Prosecution Authority
  [2024] ZMCC 19, decided 2024-07-26). RESOLVED in batch-0373
  (parser_v0.3.1). Outcome: dismissed (outcome_source=pdf-tail-2pages).
  Three-judge bench: Sitali, Chisunka, Mulife JJC. All three resolved
  against existing canonical entries.
  URL: https://zambialii.org/akn/zm/judgment/zmcc/2024/19/eng@2024-07-26.

- **judgment-zm-2024-zmcc-18-mutazu-john-v-anthony-hubert-kabungo-and-ors**
  (Mutazu John v Anthony Hubert Kabungo and Ors [2024] ZMCC 18,
  decided 2024-07-26). RESOLVED in batch-0373 (parser_v0.3.1).
  Outcome: dismissed (outcome_source=pdf-tail-2pages).
  Three-judge bench: Munalula PC, Shilimi DPC, Mulife JC. All three
  resolved against existing canonical entries.
  URL: https://zambialii.org/akn/zm/judgment/zmcc/2024/18/eng@2024-07-26.

## Deferred candidates this batch

Each deferral carries a SPECIFIC reason code per approvals.yaml
`deferral_reasons_locked` (no generic
`outcome_not_inferable_under_tightened_policy`). Raw HTML+PDF retained
on disk in `raw/zambialii/judgments/zmcc/2024/`.

- **[2024] ZMCC 27** (Michelo Chizombe v Edgar Chagwa Lungu and Ors,
  2024-12-10) — reason: `html_no_summary_pdf_no_match`. Summary head:
  "Whether transitional savings preserved the repealed term‑limit
  regime, rendering the former president ineligible for future
  presidential elections." Interpretive declaratory; no operative-verb
  match. URL:
  https://zambialii.org/akn/zm/judgment/zmcc/2024/27/eng@2024-12-10.

- **[2024] ZMCC 25** (Institute of Law Policy Research and Human Rights,
  2024-11-13) — reason: `html_no_summary_pdf_no_match`. Summary head:
  "Originating summons for abstract interpretation of Article 74(2)
  dismissed as the dispute is personalized, contentious and requires
  trial." `dismissed` is implied but the operative phrase pattern does
  not match `SUMMARY_PATTERNS` and PDF tail produced no safe match.
  URL: https://zambialii.org/akn/zm/judgment/zmcc/2024/25/eng@2024-11-13.

- **[2024] ZMCC 22** (Electoral Commission of Zambia v Belemu Sibanze,
  2024-10-15) — reason: `html_no_summary_pdf_no_match`. Summary head:
  "Constitutional electoral timelines (90‑day by‑election; 7/21‑day
  nomination challenge) are mandatory and cannot be extended by court
  proceedings." Declaratory; no operative-verb match. URL:
  https://zambialii.org/akn/zm/judgment/zmcc/2024/22/eng@2024-10-15.

- **[2024] ZMCC 20** (Michelo Chizombe v Edgar Chagwa Lungu and Ors,
  2024-10-03) — reason: `html_no_summary_pdf_no_match`. Summary head:
  "Recusal application alleging judicial bias dismissed for lack of
  cogent evidence; presumption of impartiality upheld." `dismissed` is
  implied but the operative construction does not match
  `SUMMARY_PATTERNS` (`recusal application … dismissed for lack`) and
  PDF tail produced no safe match. URL:
  https://zambialii.org/akn/zm/judgment/zmcc/2024/20/eng@2024-10-03.

- **[2024] ZMCC 17** (Isaac Mwaanza and Civil Liberties Union v
  Attorney General, 2024-07-29) — reason: `html_no_summary_pdf_no_match`.
  Summary head: "Petition challenging Penal Code's 'order of nature'
  provisions raises substantial constitutional issues; Court orders
  full hearing before a single judge." Procedural; no operative-verb
  match. URL:
  https://zambialii.org/akn/zm/judgment/zmcc/2024/17/eng@2024-07-29.

## Phase 5 progress

48 → 51 / 100–160. Yield this tick: 3 / 8 = 37.5%.

## Recommendation

The pdf-tail-2pages fallback continues to be the dominant rescue
mechanism for ZMCC under v0.3.1 (3 of 3 written records this tick).
The 5 deferrals all share the `html_no_summary_pdf_no_match` profile
characteristic of declaratory / interpretive constitutional rulings
where the operative phrase is not in the locked
`SUMMARY_PATTERNS` / `PDF_TAIL_PATTERNS` vocabulary. Parser_v0.3.2
vocabulary widening (declaratory operative verbs +
`recusal application … dismissed`) remains the dominant unblock for
the remaining ZMCC backlog — subject to Peter's approval per
BRIEF.md non-negotiable on parser vocabulary changes.

Next reparse tick should pick up zmcc/2024/{16, 15, 13, 11, 10} +
optional spillover into 2024/{2, 4–8} which were attempted under
v0.3.1 in b0364 but deferred — those would yield identical deferrals
under v0.3.1 today, so are excluded. The 2024 raw-on-disk no-record
backlog after b0373: 11 candidates remaining (5 newly classified
this tick + 5 reserved for next tick + 1 already deferred under
v0.3.1 in earlier batches; b0364 deferreds for 2024/{2,4–8} are
not reparseable under v0.3.1 again).

B2 sync deferred to host (rclone not in sandbox).
SQLite ingestion deferred to host (corpus.sqlite FTS5
malformed-disk-image carry-forward; canonical source remains
records/*.json).
