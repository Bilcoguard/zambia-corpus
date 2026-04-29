# Batch 0341 — Phase 5 kickoff (ZMCC judgments)

- **Tick start:** 2026-04-29T13:02:06Z
- **Phase:** phase_5_judgments (lowest approved + incomplete)
- **Source:** ZambiaLII Constitutional Court of Zambia index (`/judgments/ZMCC/`)
- **Bounded unit:** Schema lock + judges-registry init + 8 ConCourt 2026 candidates → 6 records written, 2 deferred to gaps.md.

## Infrastructure locked at kickoff

| Artefact | Path | Status |
|---|---|---|
| Judgment record schema | `schema/judgment.schema.json` | NEW (v0.2.0) |
| Judges registry | `judges_registry.yaml` | NEW (13 canonical names) |

## Records written (6)

| ID | Citation | Court | Outcome | Date |
|---|---|---|---|---|
| judgment-zm-2026-zmcc-09-legal-resources-foundation-limited-v-the | [2026] ZMCC 9 | Constitutional Court of Zambia | allowed | 2026-04-02 |
| judgment-zm-2026-zmcc-10-people-s-action-for-the-country-s-transf | [2026] ZMCC 10 | Constitutional Court of Zambia | dismissed | 2026-03-30 |
| judgment-zm-2026-zmcc-08-munir-zulu-v-the-attorney-general-and-or | [2026] ZMCC 8 | Constitutional Court of Zambia | dismissed | 2026-03-25 |
| judgment-zm-2026-zmcc-04-brigade-construction-limited-and-ors-v-t | [2026] ZMCC 4 | Constitutional Court of Zambia | struck-out | 2026-02-24 |
| judgment-zm-2026-zmcc-05-makebi-zulu-v-the-attorney-general | [2026] ZMCC 5 | Constitutional Court of Zambia | dismissed | 2026-02-11 |
| judgment-zm-2026-zmcc-03-law-association-of-zambia-and-ors-v-the | [2026] ZMCC 3 | Constitutional Court of Zambia | withdrawn | 2026-02-10 |

## Records deferred (2) → gaps.md

| Citation | Reason |
|---|---|
| [2026] ZMCC 7 (Climate Action Professionals) | summary is a question of law; no disposition phrase mappable to outcome enum |
| [2026] ZMCC 6 (Munir Zulu, parliamentary privilege) | summary is a question of law; no disposition phrase mappable to outcome enum |

## Provenance

All 6 records carry: `source_url`, `source_hash` (sha256 of HTML), `raw_sha256` (sha256 of source.pdf), `fetched_at` (ISO 8601 UTC), `parser_version: 0.2.0`. Raw HTML and PDF persisted to `raw/zambialii/judgments/zmcc/2026/`.

## Integrity checks

- 6/6 unique IDs.
- 6/6 records have all 20 required fields.
- 6/6 outcomes ∈ allowed enum.
- 6/6 records have ≥1 judge; every judges[*].name resolves in `judges_registry.yaml`.
- 6/6 records have ≥1 issue_tag (parsed from ZambiaLII Flynote).
- 6/6 source_hash values match raw HTML on disk.
- 6/6 raw_sha256 values match raw PDF on disk.
- `key_statutes` is empty for all 6 records — Phase 5 schema permits an empty array; statute-resolution is a separate later pass.

**Result: PASS.**

## Budget impact

- Fresh fetches this tick: 11 (1 ConCourt index + 8 judgment HTML pages cached on the prior parser-debug pass + 8 source PDFs of which only 6 succeeded for written records before deferred branch — net 11 fresh successful GETs).
- Cumulative fetches today: 44 → 55 (target ≤ 2000/day). ~2.75% of daily fetch budget.

## Next tick

- Lowest approved + incomplete phase remains `phase_5_judgments` (target 100–160 landmark judgments).
- Next batch should: (a) revisit the 2 deferred summaries by parsing the PDF order paragraph for the disposition; (b) continue down the ConCourt 2026 list (still 42 candidates uningested); (c) then pivot to Supreme Court constitutional bucket per BRIEF priority order.

## Sandbox notes

- B2 sync deferred to host (rclone not in sandbox).
- `.git/objects/maintenance.lock` is owned by host and unlinkable from this sandbox; pre-tick lock cleanup ran without error.
