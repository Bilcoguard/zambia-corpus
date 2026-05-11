# Batch 0597 — Judgment Ingestion Worker

**Tick:** jiw-b0597
**Worker:** judgment-ingestion-worker
**Started:** 2026-05-11T23:06Z
**Priority:** (b) Court of Appeal sweep — judiciaryzambia.com pages 7-remainders + page 8
**Sweep position before tick:** page-7-remaining (3 candidates) + page-8 fresh
**Sweep position after tick:** page-8 partial (5 of 11 from page 8 processed); page-8 remaining (6 candidates) for next tick

## Inputs

- 8 post URLs targeted:
  - Page 7 remainders (3): App-113 Chisumpa Liandisha v People, App-123 Patson Kabungo Sichoni v People, Appeal-154 Mandahill v Freshview
  - Page 8 fresh (5): App-165 Savenda v Lumwana, App-181 Zanaco v Allan Kandala, App-211 Rotor Moulder v Stanley Jordan, App-24 Peter Mutale v Davies Mukumbwa, App-304 Setrec Steel v Zanaco

## Fetches

- Post HTML fetches: 8
- PDF fetches: 7 (1 post had no PDF link — Appeal-no-154-2019 Mandahill Centre v Freshview)
- Total: 15 fetches (cumulative_today: 95 + 15 = 110 / 500)

## Parse results

| Post | Quality gate | Pages | Body chars | Status |
|------|--------------|-------|------------|--------|
| App-113-2020 Chisumpa Liandisha v People | pass | 8 | 6,704 | parsed-clean |
| App-211-2022 Rotor Moulder v Jordan | pass | 20 | 23,019 | parsed-clean |
| App-123-2023 Sichoni v People | fail-body-len | 16 | 15 | scanned-PDF defer |
| App-165-2024 Savenda v Lumwana | fail-body-len | 20 | 19 | scanned-PDF defer |
| App-181-2023 Zanaco v Kandala | fail-body-len | 20 | 19 | scanned-PDF defer |
| App-24-2024 Mutale v Mukumbwa | fail-body-len | 21 | 20 | scanned-PDF defer |
| App-304-2022 Setrec v Zanaco | fail-body-len | 33 | 32 | scanned-PDF defer |
| Appeal-154-2019 Mandahill v Freshview | N/A | — | — | no-pdf-found in post page |

**Outcome summary:** 2 clean records parsed; 5 scanned-PDF deferred (need ocrmypdf fallback); 1 no-pdf-found.

## Insert outcome

Inserts BLOCKED by pre-existing FTS5 corruption (17th consecutive blocked tick).

- 2 parsed records DEFERRED to `raw/judiciary-zm/coa/_deferred/b0597_parsed_records.json`
- 5 scanned-PDF records added to ocrmypdf backlog
- No `corpus.sqlite` mutation this tick.

## CHECK results

- CHECK1 (judges non-empty): PASS (3 each)
- CHECK2 (issue_tags non-empty): PASS
- CHECK3 (outcome enum): PASS — `set-aside` (Rotor Moulder), `other` (Chisumpa — to be re-extracted next tick with v0.4.1 parser)
- CHECK4 (judges resolve in registry): PASS — Mchenga, Chishimba, Majula, Makungu, Muzenga, Chembe
- CHECK5 (no duplicate IDs): PASS
- CHECK6 (raw_sha256 matches on-disk): PASS
- CHECK7 (no duplicate case_name+court+date): PASS
- CHECK8 (records == records_fts): PASS via no-mutation this tick (1892 = 1892)

## NEW FINDING — FTS5 INSERT mechanics

This tick performed a deeper diagnostic on the FTS5 corruption: while `INSERT INTO records_fts(records_fts) VALUES('integrity-check')` and `INSERT INTO records_fts(records_fts) VALUES('optimize')` continue to FAIL with `database disk image is malformed`, a regular column-based `INSERT INTO records_fts(id, type, title, citation, case_name, outcome_detail, body) VALUES (...)` on a /tmp isolated copy SUCCEEDS without raising the corruption error.

This is a structural change in understanding from b0590..b0594 reports. The malformed pages (14599, 28316–28340) appear to be in FTS5 metadata structures that affect the index-wide consistency check but DO NOT prevent appending new rows that are written to fresh pages. The backlog of 26 deferred records (24 + 2 this tick) could potentially be flushed by direct column-based inserts.

**RECOMMENDATION TO OPERATOR:**

1. The repair-worker SHOULD still add the `fts5-rebuild-records-fts` task to its manifest to fix the underlying corruption (queries against corrupted pages may return stale or incomplete results).
2. In the interim, the JIW could be authorised to flush its 26-record backlog using direct column-based inserts on `corpus.sqlite`, since:
   - The inserts demonstrably succeed on the corrupt FTS5 table
   - CHECK8 (records == records_fts) would continue to hold
   - The corrupt pages would remain corrupt — but the records themselves would be queryable for newly inserted rows
3. Alternatively, defer all backlog flushing until FTS5 rebuild completes.

This finding is escalated for operator decision. JIW continued the conservative defer pattern this tick pending operator guidance.

## Backlog status (carry-forward)

- **Deferred FTS5 backlog:** 24 (b0590..b0594) + 2 (b0597 this tick) = **26 records**
- **Deferred scanned-PDF backlog:** 5 (b0593..b0594) + 5 (b0597 this tick) = **10 records**
- **No-PDF-found:** 1 (Appeal-154-2019 Mandahill Centre v Freshview — possible WP page-builder format variation; manual follow-up flagged)

## Sweep position for next tick (b-coa)

- judiciary-coa-sweep: **page 8 remaining** (6 candidates: App-181 already retried, App-222-2015 Penelope Chishimba Chipasha-Mambwe v Millingtone Mambwe, App-311-2021 Transquic Service v ?, App-57-2023 Lovemore Gumbo v Stanchart, App-75-2025 Astro Holdings v Hamuwele, Appeal-117-2024 Lumbwe Kakoma v Mulenga, Appeal-268-2022 Mpoyi Mbambu v Joserine Trading)

## Execution notes

- Stale git lock workaround needed (ORIG_HEAD.lock and objects/maintenance.lock zero-byte FUSE-locked files) — moved aside to `_stale_locks_b0597/` to permit pull/commit
- pre-tick corpus.sqlite backup: NONE this tick (no mutation)
- Execution mode: inline runner; no derivative script committed (sandbox-session safety constraint)
- User-Agent: KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)
