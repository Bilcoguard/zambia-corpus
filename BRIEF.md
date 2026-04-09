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
- **Phase 5 — Retrieval API.** Build a local SQLite index + FTS5 virtual table over the corpus. Expose a minimal query interface.
- **Phase 6 — Integration brief.** Write `INTEGRATION.md` explaining how the Kate Weston Legal plugin should call the retrieval API and format citations.
- **Phase 7 — Nightly re-verification.** Sample `sample_rate` of existing records per night, re-fetch, compare hashes, flag drift.

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
