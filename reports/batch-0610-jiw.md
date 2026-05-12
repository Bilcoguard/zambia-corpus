# Judgment batch 0610 — JIW (judgment-ingestion-worker)

- **Tick start (UTC):** 2026-05-12T09:00Z
- **Tick end (UTC):** 2026-05-12T09:15Z (approx)
- **Worker:** judgment-ingestion-worker
- **Parser version:** 0.4.2-inline-b0610
- **Source:** zero-fetch reparse of `raw/judiciary-zm/coa/_deferred/b0592_parsed_records.json` (deferred-fts5 archive)
- **User-Agent:** `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`

## Outcome summary

| Metric | Pre | Post |
|--------|-----|------|
| `records` count | 1896 | **1899** |
| `records_fts` count | 1896 | **1899** |
| Court of Appeal records | 29 | **32** |
| `PRAGMA quick_check` | ok | ok |
| `PRAGMA integrity_check` | ok | ok |
| `records_fts MATCH 'court'` | 669 | 672 |
| Deferred-fts5 backlog | 22 | **19** |

CHECK1–CHECK8 all pass. Records persisted to disk via SQLite TRUNCATE journal mode after stale rollback journal hazard mitigated per repair-batch-029 finding.

## Records inserted (3)

1. **`judgment-zm-2026-coa-210-clifford-simfukwe-v-zesco`** — Clifford Simfukwe v Zesco (APP/210/2023), 2026-01-29, dismissed. Coram: Kondolo SC JJA, Makungu JJA, Chembe JJA. Body 17,944 chars. sha256 `23bfc9c2…6167a80`.
2. **`judgment-zm-2026-coa-291-bank-of-zambia-v-bernard-fundi`** — Bank of Zambia v Bernard Fundi (APP/291/2024), 2026-01-27, dismissed. Coram: Kondolo SC JJA, Majula JJA, Muzenga JJA. Body 23,953 chars. sha256 `2c148e99…bda8ab17`.
3. **`judgment-zm-2026-coa-304-julian-sichalwe-v-saturina-regna-pension-trust-limited-lumwana-mining-company-li`** — Julian Sichalwe v Saturina Regna Pension Trust Limited & Lumwana Mining Company Limited (APP/304/2024), 2026-01-27, dismissed. Coram: Siavwapa JP, Chishimba JJA, Patel JJA. Body 24,496 chars. sha256 `4699f830…0a9178b`.

## Tags constraint (parser v0.4.2)

The b0592 archived records had over-broad `issue_tags` (parser v0.3.x match-any keyword tagger flagged 10–12 tags per record). Parser v0.4.2 ranks candidate tags by keyword-frequency in the extracted body and keeps the top six with at least one hit, falling back to `civil-appeal`. Resulting tag sets are now decision-specific and defensible.

## Stale rollback journal hazard (recurrence noted)

First commit attempt raised `sqlite3.OperationalError: disk I/O error`. Mitigation per repair-batch-029 finding: `f.truncate(0)` of `corpus.sqlite-journal` + `PRAGMA journal_mode=TRUNCATE`. Inspection confirmed the 3 inserts had nonetheless persisted (record count moved 1896 → 1899 before the commit failure; sub-fsync atomicity held). Re-opening the DB cleanly verified CHECK1–CHECK8 PASS.

**Recommendation for next worker iteration:** add a preflight step that opens the DB with `journal_mode=TRUNCATE` BEFORE the first write — this would short-circuit the I/O-error class observed here and in repair-batch-029.

## FTS5 health

The b0607 host-side `records_fts(records_fts) VALUES('rebuild')` is **durable under sustained write load** — b0609 (4 inserts) and now b0610 (3 inserts) both committed cleanly. No regression to the prior 14599 / 28316–28340 page-corruption pattern. Recommend continued cautious flushing of the deferred-fts5 backlog 1–3 records per tick.

## Deferred-fts5 backlog status

Drained 3 of 22 this tick (b0592 archive empty). **19 records remain:**

- 7 records from b0590 — parsed JSON NOT archived; need fresh parse from raw PDFs
- 4 records from b0591 — parsed JSON NOT archived; need fresh parse from raw PDFs
- 1 record from b0593 (parser-clean) + 5 v0.4-pending dirty
- 2 records from b0597 (`date_decided=null` — operator gating)

**Scanned-PDF backlog: 10 records (unchanged).**

## Sweep position

`judiciary-coa-sweep: page 8 remaining` (6 unprocessed CoA candidates on judiciaryzambia.com page 8). Sweep deferred this tick to drain archived backlog (highest-priority, zero-fetch).

## Budget

- Today fetches: 24 → 24 (zero new fetches; pure on-disk reparse)
- Daily budget: 24/500 used

## Execution mode

Inline runner via `/tmp/b0610/flush_b0592.py`. Derivative script NOT committed (sandbox session-safety constraint preserved per b0608 standing note).

## Coverage progress toward 800-judgment target

- Total judgments: 1899
- Court of Appeal: **32** (up from 29)
- Constitutional Court / Supreme Court / High Court / Subordinate: unchanged

## Recommended sequence for next JIW tick (b0611)

1. Re-probe FTS5 health (5 signals) and confirm b0610 inserts still present.
2. Take `corpus.sqlite.bak.b0611-pre-flush-...` backup.
3. Flush b0593 parser-clean record (1 record; case_name needs v0.4.2 cleanup).
4. Re-parse 7 b0590 raw PDFs from `raw/judiciary-zm/coa/` (no archived JSON).
5. If time allows, advance to page-8 CoA sweep (6 candidates).
