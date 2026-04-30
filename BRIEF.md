# Zambian Authorities Corpus — Worker Brief

## Mission
Build and maintain a verified, citation-grade corpus of Zambian primary legal authorities (Constitution, Acts, Statutory Instruments, reported judgments) so that Kate Weston Legal Practitioners' AI tools can ground every legal statement in a real, current, verifiable source.

## Non-negotiables
1. **No fabrication.** Never invent a citation, section number, case name, or date. If a source cannot be fetched or parsed cleanly, record it in `gaps.md` and move on.
2. **Provenance is sacred.** Every record must include `source_url`, `source_hash` (sha256 of raw bytes), `fetched_at` (ISO 8601 UTC), and `parser_version`.
3. **Respect the sources.** Obey robots.txt. Use the configured User-Agent. Honour the rate limits in `approvals.yaml`. Identify yourself honestly.
4. **Versioning.** When an Act is amended, keep the prior version and link it via `amended_by`. Never silently overwrite.
5. **Approval gates.** Read `approvals.yaml` at the start of every tick. Only run phases where `approved: true` and `complete: false`. Never flip an approval yourself.
6. **Budgets.** Stop for the day if `max_fetches_per_day` or `max_tokens_per_day` is exceeded.
7. **Integrity checks before commit.** No duplicate IDs. All `amended_by` / `repealed_by` references must resolve. All `source_hash` values must match the raw file on disk. If any check fails, halt, do not commit, write the failure to `worker.log`.

## Sources (priority order)
1. **Parliament of Zambia** — parliament.gov.zm (Acts, Bills, Hansard)
2. **ZambiaLII** — zambialii.org (consolidated Acts, SIs, case law)
3. **Judiciary of Zambia** — judiciary.gov.zm (SCZ, CAZ, HC judgments)
4. **Government Gazette** — for SIs not yet on ZambiaLII
5. **Regulator sites** — PACRA, ZRA, BoZ, PIA, SEC, ZPPA, ZEMA, ODPC (subsidiary legislation, guidelines, directives)

## Phases
- **Phase 0 — Source map.** Produce `sources.yaml` listing every source, its URL pattern, robots.txt status, rate limit, and parser strategy. Human approval required.
- **Phase 1 — Schema.** Lock the JSON record schema in `schema/record.schema.json`. Create empty folder skeleton under `corpus/`.
- **Phase 2 — Pilot statute.** Ingest the Companies Act No. 10 of 2017 end-to-end: fetch raw, hash, parse to sections, emit JSON records, commit. Human reviews before Phase 3 unlocks.
- **Phase 3 — Pilot judgment.** Ingest one reported SCZ judgment end-to-end. Human reviews before Phase 4 unlocks.
- **Phase 4 — Bulk ingestion.** Work through `priority_order` from `approvals.yaml` in batches of `batch_size`. Emit a `batches/NNNN-report.md` for each batch. Human reviews reports; flags issues via `gaps.md`.
- **Phase 5 — Judgments ingestion** (`phase_5_judgments`).
  - **Source:** ZambiaLII judgment pages — Constitutional Court, Supreme Court, High Court.
  - **Target:** 100–160 landmark judgments.
  - **Batch size:** 8 records per tick (same as Phase 4).
  - **Priority order:** Constitutional Court → Supreme Court (constitutional) → Supreme Court (commercial) → mining → property → family.
  - **Required fields per judgment record** (in addition to the base provenance fields `source_url`, `source_hash`, `fetched_at`, `parser_version`): `court`, `citation`, `case_name`, `case_number`, `date_decided`, `judges` (list of `{name, role, dissented: bool}`), `issue_tags`, `outcome`, `outcome_detail`, `reasoning_tags`, `key_statutes`, `raw_sha256`. See "Judgment record schema" below.
  - **Judges registry:** maintain `judges_registry.yaml` at the workspace root, mapping each judge to a canonical name plus title history (e.g., `J.` → `JA` → `JS` → `CJ`, with dates). Reuse existing entries on every batch; never create duplicates. Each judgment's `judges[*].name` MUST resolve to an entry in `judges_registry.yaml` (auto-add new judges on first encounter, with a `first_seen` timestamp and the source citation).
  - **Integrity checks (in addition to the standard ones):** every judgment has at least one judge; `issue_tags` non-empty; `outcome ∈ {allowed, dismissed, upheld, overturned, remitted, struck-out, withdrawn}` — locked in `schema/judgment.schema.json`; every `judges[*].name` resolves in `judges_registry.yaml`; every `key_statutes` reference resolves to an existing statute record `id` in the corpus where possible (else recorded as an unresolved citation in `gaps.md`).
  - **Completion criterion:** five consecutive zero-discovery ticks OR 160 judgments reached. On either trigger the worker logs "Phase 5 appears complete, awaiting human confirmation" to `worker.log` and stops; only a human flips `complete: true` in `approvals.yaml`.
  - **Parser policy (locked-in 2026-04-30, parser_version 0.3.1+):**
    - **Frozen baseline:** `scripts/batch_0360_parse.py` (parser_v0.3.1). New batches copy from this file, not from earlier b0359/b0358 baselines.
    - **Outcome inference order (3 stages):**
      1. **Summary path** — match `SUMMARY_PATTERNS` against the HTML summary paragraph extracted from the ZambiaLII `<dl>` block. If a safe match is found, use it.
      2. **PDF order-anchor path** — find the last occurrence of any `PDF_ORDER_ANCHORS` keyword (`it is ordered`, `we accordingly order`, `the order of the court`, …) in the full PDF text and search the 800-char window after it for a `SUMMARY_PATTERNS` match.
      3. **PDF tail-2-pages path (NEW)** — extract the final 2 pages of the PDF (or the last 10000 chars of `full_text` if those pages came up empty under pdfplumber, which catches scanned final pages on otherwise-extractable PDFs) and scan with `PDF_TAIL_PATTERNS` (active-voice operative phrases such as `we therefore dismiss the petition`, `petition is forthwith dismissed`, `we decline to grant the reliefs sought`, numbered closing orders, `appeal succeeds/fails`). The **latest** safe match wins — the operative paragraph sits at the end of the judgment.
    - All three stages share the same `_detail_is_safe` guard (≥12 alphabetic chars, no blacklisted substrings, no leading lowercase mid-word fragment).
    - Pre-existing logic is unchanged — the tail fallback is strictly additive.
  - **Reparse-first policy (locked-in 2026-04-30):** before consuming fresh fetch budget, scan `gaps.md` and the `records/judgments/` tree for candidates whose raw HTML+PDF are already on disk but whose record was never written under the older parser. If any deferral reason is now addressable by the current parser version (e.g., `outcome_not_inferable_under_tightened_policy` once parser_v0.3.1 is live), spend the tick re-parsing those candidates — up to `MAX_BATCH_SIZE` records — instead of fetching new ones. Re-parsing has zero fetch-budget cost and typically high yield. Only when no addressable deferreds remain should the tick continue the fresh DESC sweep. When a deferred candidate is successfully re-parsed, append a `RESOLVED in batch-NNNN (parser_vX.Y.Z)` line beneath its `gaps.md` entry rather than removing the entry — the historical record stays intact for audit.
  - **Specific deferral reason codes (required, no generic fallback):** never defer a candidate with a vague reason like `outcome_not_inferable_under_tightened_policy`. Pick a precise code so a future re-parse can target it:
    - `pdf_extraction_empty_likely_scanned` — pdfplumber returned no text; needs OCR pass.
    - `multi_judge_separate_opinions_no_clear_majority_disposition` — concurring/dissenting opinions only, no majority operative paragraph; needs majority-view inference logic.
    - `parser_v<X.Y.Z>_<token>_unhandled` — known parser bug for the current version (e.g., `parser_v0.3.0_jjs_title_unhandled`).
    - `outcome_inferred_but_detail_unsafe` — outcome enum identified but `outcome_detail` failed `_detail_is_safe`.
    - `html_no_summary_pdf_no_match` — neither summary, anchor, nor tail patterns matched anything; raw retained for manual triage.
- **Phase 6 — Retrieval API.** Build a local SQLite index + FTS5 virtual table over the corpus. Expose a minimal query interface.
- **Phase 7 — Integration brief.** Write `INTEGRATION.md` explaining how the Kate Weston Legal plugin should call the retrieval API and format citations.
- **Phase 8 — Nightly re-verification.** Sample `sample_rate` of existing records per night, re-fetch, compare hashes, flag drift.

> **Renumbering note (2026-04-29):** Phase 5 was previously "Retrieval API"; it is now "Judgments ingestion". The former Phase 5/6/7 shifted to 6/7/8. `approvals.yaml` was reconciled by Peter on 2026-04-29: `phase_5_judgments` (approved: true, complete: false), `phase_6_retrieval_api`, `phase_7_integration_brief`, `phase_8_nightly_reverify` (the last three retain their prior approved/complete values).

## Record schema (summary)
```json
{
  "id": "act-companies-2017",
  "type": "act | si | judgment | constitution | regulation",
  "jurisdiction": "ZM",
  "title": "Companies Act, 2017",
  "citation": "Act No. 10 of 2017",
  "enacted_date": "2017-11-20",
  "commencement_date": "2018-06-29",
  "in_force": true,
  "amended_by": ["act-...-2022"],
  "repealed_by": null,
  "sections": [
    { "number": "1", "heading": "Short title", "text": "..." }
  ],
  "source_url": "https://...",
  "source_hash": "sha256:...",
  "fetched_at": "2026-04-09T12:00:00Z",
  "parser_version": "0.1.0"
}
```

## Judgment record schema (Phase 5)
Judgment records use `type: "judgment"` and extend the base record with the fields below. Lock the full schema in `schema/judgment.schema.json` at Phase 5 kick-off. **All values below are placeholders for shape only — do not treat as real citations.**
```json
{
  "id": "judgment-<court>-<year>-<slug>",
  "type": "judgment",
  "jurisdiction": "ZM",
  "court": "Supreme Court of Zambia | Constitutional Court | High Court",
  "citation": "<neutral or report citation, e.g. [YYYY] ZMSC NN>",
  "case_name": "<Plaintiff/Appellant> v <Defendant/Respondent>",
  "case_number": "<court file number>",
  "date_decided": "YYYY-MM-DD",
  "judges": [
    { "name": "<canonical name>", "role": "presiding",  "dissented": false },
    { "name": "<canonical name>", "role": "concurring", "dissented": false },
    { "name": "<canonical name>", "role": "dissenting", "dissented": true  }
  ],
  "issue_tags": ["<issue-tag-1>", "<issue-tag-2>"],
  "outcome": "<one of: allowed | dismissed | upheld | overturned | remitted | struck-out | withdrawn>",
  "outcome_detail": "<one-sentence summary of the disposition>",
  "reasoning_tags": ["<reasoning-tag-1>", "<reasoning-tag-2>"],
  "key_statutes": ["<resolvable corpus id, e.g. act-companies-2017>"],
  "raw_sha256": "sha256:...",
  "source_url": "https://zambialii.org/zm/judgment/...",
  "source_hash": "sha256:...",
  "fetched_at": "YYYY-MM-DDTHH:MM:SSZ",
  "parser_version": "0.2.0"
}
```
Allowed `outcome` enum: `allowed`, `dismissed`, `upheld`, `overturned`, `remitted`, `struck-out`, `withdrawn`.
Allowed `judges[*].role` enum: `presiding`, `concurring`, `dissenting`, `partial-concurring`, `partial-dissenting`.

## Tick prompt (what to do every 30 minutes)
1. `git pull --ff-only` to get latest approvals.
2. Read `approvals.yaml`. Identify the lowest-numbered phase that is `approved: true` and `complete: false`.
3. Check today's fetch/token budget in `worker.log`. Halt if exceeded.
4. **Reparse-first triage** (Phase 5+ only): before any new fetches, scan `gaps.md` and `records/judgments/` for candidates whose raw HTML+PDF are already on disk and whose deferral reason is addressable by the current parser version. If any are found, spend this tick re-parsing them (up to MAX_BATCH_SIZE = 8 records) — zero fetch budget, high yield. Skip step 5's fetch step in that case. When a re-parse succeeds, append a `RESOLVED in batch-NNNN (parser_v<X.Y.Z>)` line beneath the original gaps.md entry; do NOT delete the entry.
5. If no addressable deferreds remain, run that phase's worker script for one bounded unit of work (one batch, one pilot, etc.). For Phase 5 judgments, copy the frozen parser baseline `scripts/batch_0360_parse.py` (parser_v0.3.1) to `scripts/batch_NNNN_parse.py` and edit only the TARGETS slice, WORK directory, and any version-bump comments. Defer any candidate the parser cannot handle with a SPECIFIC reason code (see "Phase 5 — Parser policy" non-negotiables) — never the generic `outcome_not_inferable_under_tightened_policy`.
6. Run integrity checks. If any fail, halt, log, do not commit.
7. If checks pass, write records, update `worker.log`, `git add`, `git commit -m "worker: <phase> <unit>"`, `git push`.
8. If the phase's work is complete, set `complete: true` in approvals.yaml (worker CAN flip complete; only human flips approved).
9. Exit cleanly so the next tick starts fresh.

## Paths
- Workspace: `/Users/peterndhlovu/KateWestonCorpus/corpus`
- Raw local cache: `./raw/` (gitignored, synced to B2 `b2raw:kwlp-corpus-raw`)
- Structured records: `./corpus/`
- Reports: `./batches/`
- Logs: `./worker.log`
- Gaps: `./gaps.md`

## Contact
peter@bilcoguard.com
