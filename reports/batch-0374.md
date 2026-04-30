# Batch 0374 — Phase 5 ZMCC reparse-first (continues 2024 ZMCC + 2025 carryover)

**Date:** 2026-04-30T21:00:00Z
**Phase:** phase_5_judgments (approved: true, complete: false)
**Parser:** parser_v0.3.1 (frozen baseline `scripts/batch_0360_parse.py` ⇒ `scripts/batch_0374_parse.py`)
**Mode:** REPARSE-FIRST (zero fresh fetch budget; all raw bytes already on disk)
**Slice (8 candidates):** zmcc/2024/{23, 16, 15, 13, 11, 10}, zmcc/2025/{25, 24}

## Slice rationale

Per b0373's recommendation ("Next reparse tick should pick up zmcc/2024/{16, 15, 13, 11, 10}") plus two
addressable v0.3.0 generic-reason candidates not yet reclassified under v0.3.1:

- **zmcc/2024/23** — listed in `gaps.md` under the legacy `outcome_not_inferable_under_tightened_policy`
  reason from a pre-v0.3.1 batch; never re-attempted under v0.3.1.
- **zmcc/2025/{25, 24}** — top of the 2025 DESC backlog under the legacy generic v0.3.0 reason; never
  re-attempted under v0.3.1.

Excluded from this slice (would yield identical deferrals under v0.3.1):
zmcc/2024/{17, 20, 22, 25, 27} reclassified `html_no_summary_pdf_no_match` in b0373;
zmcc/2024/{2, 4–8} reclassified `html_no_summary_pdf_no_match` in b0364;
zmcc/2025/19 reclassified `pdf_extraction_empty_likely_scanned` (needs OCR).

## Result

- **Written:** 2 records (both via `pdf-tail-2pages` fallback)
- **Deferred:** 6 records (all `html_no_summary_pdf_no_match`)
- **Fresh fetches:** 0
- **Phase 5 progress:** 51 → 53 / 100–160 target

### Resolved (raw retained per audit policy)

- **judgment-zm-2024-zmcc-16-sean-tembo-suing-in-his-capacity-as-the-president**
  (Sean Tembo (Suing in his capacity as the President of the Patriots for Economic Progress) v
  Attorney General [2024] ZMCC 16, decided 2024-07-10).
  RESOLVED in batch-0374 (parser_v0.3.1).
  Outcome: dismissed (outcome_source=pdf-tail-2pages; "petition and we dismiss them").
  Seven-judge bench: Shilimi DPC, Sitali, Mulonda, Mulenga, Musaluke, Mulongoti, Mwandenga JJC.
  All seven resolved against existing canonical entries / aliases in `judges_registry.yaml`
  (no registry write needed).
  URL: https://zambialii.org/akn/zm/judgment/zmcc/2024/16/eng@2024-07-10.

- **judgment-zm-2024-zmcc-11-sean-tembo-suing-in-his-capacity-as-the-president**
  (Sean Tembo (Suing in his capacity as the President of the Patriots for Economic Progress) v
  The Attorney General [2024] ZMCC 11, decided 2024-06-17).
  RESOLVED in batch-0374 (parser_v0.3.1).
  Outcome: dismissed (outcome_source=pdf-tail-2pages;
  "23] The upshot of the preceding paragraphs is that the Petition fails").
  Three-judge bench: Shilimi DPC, Mulongoti, Mulife JJC.
  All three resolved against existing canonical entries in `judges_registry.yaml`
  (no registry write needed).
  URL: https://zambialii.org/akn/zm/judgment/zmcc/2024/11/eng@2024-06-17.

### Deferred candidates this batch

Each deferral carries a SPECIFIC reason code per approvals.yaml `deferral_reasons_locked`
(no generic `outcome_not_inferable_under_tightened_policy`). Raw HTML+PDF retained on disk
in `raw/zambialii/judgments/zmcc/{2024,2025}/`.

- **[2024] ZMCC 23** (— v —, 2024-10-29) — reason: `html_no_summary_pdf_no_match`.
  Summary head: "An interim stay cannot be granted where the presidential suspension has
  already been implemented; single judge declined to decide standing." Procedural single-judge
  refusal; declarative summary; no operative-verb match in summary, no PDF anchor or tail match.
  URL: https://zambialii.org/akn/zm/judgment/zmcc/2024/23/eng@2024-10-29.

- **[2024] ZMCC 15** (Milingo Lungu v The Attorney General and Anor, 2024-07-08) — reason:
  `html_no_summary_pdf_no_match`. Summary head: "The applicant's discontinuance was allowed;
  the Court exercised discretion and ordered each party to bear their own costs." `allowed`
  is implied but the operative construction (`discontinuance was allowed`) does not match
  `SUMMARY_PATTERNS`; PDF tail produced no safe match.
  URL: https://zambialii.org/akn/zm/judgment/zmcc/2024/15/eng@2024-07-08.

- **[2024] ZMCC 13** (Elijah Simbai v The Zambia Institute of Advanced Legal Education,
  2024-06-28) — reason: `html_no_summary_pdf_no_match`. Summary head: "The applicant's
  constitutional challenge to ZIALE's investigation and withholding of results was dismissed
  for lack of constitutional breach." `dismissed` is implied but operative construction
  (`constitutional challenge … was dismissed for lack`) does not match `SUMMARY_PATTERNS`;
  PDF tail produced no safe match.
  URL: https://zambialii.org/akn/zm/judgment/zmcc/2024/13/eng@2024-06-28.

- **[2024] ZMCC 10** (Moses Sakala v Attorney General and Ors, 2024-06-25) — reason:
  `html_no_summary_pdf_no_match`. Summary head: "Leader of the opposition is elected by the
  largest opposition party via internal processes; Speaker only receives written notification."
  Declaratory; no operative-verb match in summary, no PDF anchor or tail match.
  URL: https://zambialii.org/akn/zm/judgment/zmcc/2024/10/eng@2024-06-25.

- **[2025] ZMCC 25** (—, 2025-12-04) — reason: `html_no_summary_pdf_no_match`.
  Summary head: "Court refused stay of Speaker's vacancy ruling absent special and convincing
  grounds; merits not to be decided interlocutorily." Procedural refusal; no operative-verb
  match in summary, no PDF anchor or tail match.
  URL: https://zambialii.org/akn/zm/judgment/zmcc/2025/25/eng@2025-12-04.

- **[2025] ZMCC 24** (—, 2025-11-28) — reason: `html_no_summary_pdf_no_match`.
  Summary head: "The Constitutional Court held the Attorney General may represent the Speaker
  as the legal representative of 'Government' and ordered joinder of the Attorney General."
  Procedural joinder ruling; declaratory operative phrase does not match `SUMMARY_PATTERNS`;
  no PDF anchor or tail match.
  URL: https://zambialii.org/akn/zm/judgment/zmcc/2025/24/eng@2025-11-28.

## Recommendation

The pdf-tail-2pages fallback rescued 2 of 2 written records again — pattern continues to hold
for ZMCC under v0.3.1 (active-voice operative phrases at the end of the PDF). All 6 deferrals
share the `html_no_summary_pdf_no_match` profile characteristic of declaratory/procedural
constitutional rulings (interim stays, joinder applications, ZIALE complaint, constitutional
challenges with operative phrases not in vocabulary). Parser_v0.3.2 vocabulary widening
(declaratory operative verbs + procedural-refusal patterns + `discontinuance allowed`,
`challenge … dismissed for lack`) remains the dominant unblock — subject to Peter's approval
per BRIEF.md non-negotiable on parser vocabulary changes.

The 2024 ZMCC v0.3.1-addressable reparse inventory is now empty (written {01, 03, 09, 11,
12, 14, 16, 18, 19, 21, 24, 26}; deferred-html_no_summary_pdf_no_match {02, 04, 05, 06, 07,
08, 10, 13, 15, 17, 20, 22, 23, 25, 27}). Next reparse tick can either (a) continue the 2025
DESC sweep on zmcc/2025/{22, 21, 18, 17, 16, 15, 14, 12, 11} (still on legacy generic v0.3.0
reason; never re-attempted under v0.3.1), (b) pivot to non-ZMCC courts (zmsc, zmca, zmhc)
under v0.3.1, or (c) pause for parser_v0.3.2 approval.

## Logs

- `worker.log` updated with start/parse/integrity/commit lines.
- `costs.log` updated with `reparse-no-fetch` event (0 bytes, written=2, deferred=6).
- `provenance.log` updated with the 2 written record provenance entries.
- B2 sync deferred to host (rclone not in sandbox).
- SQLite ingestion deferred to host (corpus.sqlite FTS5 malformed-disk-image carry-forward).
