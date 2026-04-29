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
- **Phase 6 — Retrieval API.** Build a local SQLite index + FTS5 virtual table over the corpus. Expose a minimal query interface.
- **Phase 7 — Integration brief.** Write `INTEGRATION.md` explaining how the Kate Weston Legal plugin should call the retrieval API and format citations.
- **Phase 8 — Nightly re-verification.** Sample `sample_rate` of existing records per night, re-fetch, compare hashes, flag drift.

> **Renumbering note (2026-04-29):** Phase 5 was previously "Retrieval API"; it is now "Judgments ingestion". The former Phase 5/6/7 shifted to 6/7/8. `approvals.yaml` still references the old keys (`phase_5_retrieval_api`, `phase_6_integration_brief`, `phase_7_nightly_reverify`) and must be reconciled by a human — the worker never edits approval flags or phase keys. Until reconciled, the worker treats `phase_5_judgments` as **not approved** (no matching `approved: true` entry exists) and remains idle.

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
4. Run that phase's worker script for one bounded unit of work (one batch, one pilot, etc.).
5. Run integrity checks. If any fail, halt, log, do not commit.
6. If checks pass, write records, update `worker.log`, `git add`, `git commit -m "worker: <phase> <unit>"`, `git push`.
7. If the phase's work is complete, set `complete: true` in approvals.yaml (worker CAN flip complete; only human flips approved).
8. Exit cleanly so the next tick starts fresh.

## Paths
- Workspace: `/Users/peterndhlovu/KateWestonCorpus/corpus`
- Raw local cache: `./raw/` (gitignored, synced to B2 `b2raw:kwlp-corpus-raw`)
- Structured records: `./corpus/`
- Reports: `./batches/`
- Logs: `./worker.log`
- Gaps: `./gaps.md`

## Contact
peter@bilcoguard.com
