# Batch 0543 — judgment-ingestion-worker tick

- **Worker**: judgment-ingestion-worker (scheduled task `judgment-ingestion`)
- **Wall-clock window**: 2026-05-08T21:0xZ..21:2xZ (UTC, well under 20 min target)
- **Phase**: Phase 5 dedicated post-completion ingestion (continued).
- **Parser**: v0.3.2 baseline (`scripts/batch_0498_parse.py` + `scripts/batch_0506_zmsc_parse.py` wrapper). No parser, fetcher, or core-logic modifications. Only configuration-tier wrappers added (`scripts/batch_0543_zmsc_fetch.py`, `scripts/batch_0543_zmsc_parse.py`, `scripts/batch_0543_sqlite_insert.py`, `scripts/integrity_check_b0543.py`) following the established b0539/b0540/b0541 pattern.
- **Outcome**: 3 records written, 4 deferred. Resumes substantive ingestion after 3-tick fail-safe series (b0532, b0537, b0542).

## Tick decision (priority order)

a. **REPARSE DEFERRED** — gaps.md cohort of **51** raw-on-disk
   `html_no_summary_pdf_no_match` deferrals still requires v0.3.3 parser
   patterns (succeeds/fails / remitted / set-aside-from-jurisdiction-finding —
   enumerated in b0541). Reparse under v0.3.2 is a confirmed no-op.
   33 OCR-pending records (~243 MB scanned PDFs) likewise require OCR
   tooling outside the v0.3.2 baseline. **Not eligible** under existing
   parser baseline.

b. **SCZ SWEEP — ZMSC 2020 upper-boundary HEAD-only probe + GET-fetch
   confirmed-OK nums** (this tick). Per b0541 next-tick recommendation,
   the upper boundary of ZMSC 2020 (max-num ≥ 50 confirmed by previous
   sweeps) was probed HEAD-only at nums {51, 55, 60, 65, 70, 75, 80, 90}.
   **7 of 8 returned 200**; only num=80 was 404. The boundary therefore
   extends well above 50, with at least one internal 404 between 75 and 90.
   Following the HEAD probe, the 7 confirmed-OK nums were GET-fetched and
   parsed; **3 records written, 4 deferred (all OCR-pending)**.

c. **ZMCC NEW YEARS** — not reached; SCZ year sweeps still active and
   yielding new records.

## Phase 0 — HEAD-only upper-boundary probe

Inline HEAD probes (8 fetches, polite 1.0 s rate limit, User-Agent
KateWestonLegal-CorpusBuilder/1.0; saved to `_work/b0543/head_probe.json`):

| court / num   | HEAD status | redirect target              |
|---------------|------------:|------------------------------|
| zmsc/2020/51  | 200 OK      | `/zmsc/2020/51/eng@2020-06-30` |
| zmsc/2020/55  | 200 OK      | `/zmsc/2020/55/eng@2020-08-04` |
| zmsc/2020/60  | 200 OK      | `/zmsc/2020/60/eng@2020-08-19` |
| zmsc/2020/65  | 200 OK      | `/zmsc/2020/65/eng@2020-08-19` |
| zmsc/2020/70  | 200 OK      | `/zmsc/2020/70/eng@2020-08-12` |
| zmsc/2020/75  | 200 OK      | `/zmsc/2020/75/eng@2020-08-20` |
| zmsc/2020/80  | 404         | (internal gap)               |
| zmsc/2020/90  | 200 OK      | `/zmsc/2020/90/eng@2020-09-29` |

**Finding**: ZMSC 2020 has at least 89 valid nums (max num=90 confirmed
OK, num=80 confirmed 404 internal gap). Previous sweeps (b0540, b0541)
covered only nums 1..50 — the year is much larger than the prior
working assumption. Upper-boundary-true ceiling still unresolved
(>90).

## Phase 1 — fetch the 7 confirmed-OK nums

| court / num   | result | html bytes | pdf bytes  | judgment date |
|---------------|--------|-----------:|-----------:|---------------|
| zmsc/2020/51  | ok     |     41,557 |  5,012,098 | 2020-06-30    |
| zmsc/2020/55  | ok     |     38,617 |  6,680,964 | 2020-08-04    |
| zmsc/2020/60  | ok     |     41,058 |    234,969 | 2020-08-19    |
| zmsc/2020/65  | ok     |     38,734 |    295,623 | 2020-08-19    |
| zmsc/2020/70  | ok     |     38,602 |  8,925,516 | 2020-08-12    |
| zmsc/2020/75  | ok     |     38,739 |  3,796,753 | 2020-08-20    |
| zmsc/2020/90  | ok     |     38,633 |  6,257,230 | 2020-09-29    |

Total fetches in Phase 1: 14 GETs (7 HTML + 7 PDF). Combined with the
8 HEAD probes in Phase 0, this tick consumed **22 fetches** against the
500/day judgment-ingestion budget. Cumulative today: **70/500**.

## Phase 2 — parse via parser_v0.3.2

| court / num   | result   | outcome   | source                                            |
|---------------|----------|-----------|---------------------------------------------------|
| zmsc/2020/51  | written  | allowed   | `pdf-tail-2pages[v031-tail:appeal succeeds]`      |
| zmsc/2020/55  | deferred | —         | `pdf_extraction_empty_likely_scanned`             |
| zmsc/2020/60  | written  | upheld    | `summary[Court upheld]`                           |
| zmsc/2020/65  | written  | dismissed | `pdf-tail-2pages[v031-tail:appeal is dismissed]`  |
| zmsc/2020/70  | deferred | —         | `pdf_extraction_empty_likely_scanned`             |
| zmsc/2020/75  | deferred | —         | `pdf_extraction_empty_likely_scanned`             |
| zmsc/2020/90  | deferred | —         | `pdf_extraction_empty_likely_scanned`             |

Three written records:

1. **judgment-zm-2020-zmsc-51-richard-h-chama-213-other-v-national-pension-schem** —
   *Richard H. Chama & 213 Others v National Pension Scheme Authority & Others*,
   `[2020] ZMSC 51`, Appeal 101 of 2018, decided 2020-06-30. Outcome: **allowed**
   ("appeal succeeds in" — pdf-tail anchor). Coram: Malila, Kaoma, Mambilima.
2. **judgment-zm-2020-zmsc-60-matias-chitigwa-mugogo-v-the-people** —
   *Matias Chitigwa Mugogo v The People*, `[2020] ZMSC 60`, SCZ Appeal 42 of 2019,
   decided 2020-08-19. Outcome: **upheld** ("Court upheld" — HTML summary anchor).
   Coram: Hamaundu, Muyovwe, Chinyama.
3. **judgment-zm-2020-zmsc-65-jackson-kamanga-others-v-the-people** —
   *Jackson Kamanga & Others v The People*, `[2020] ZMSC 65`, Appeal 30 of 2020,
   decided 2020-08-19. Outcome: **dismissed** ("appeal is dismissed" — pdf-tail
   anchor). Coram: Hamaundu, Muyovwe, Chinyama.

Four deferred records (all under `pdf_extraction_empty_likely_scanned`,
adding to the OCR-pending cohort):

| court / num   | bytes (PDF) | reason                                  |
|---------------|------------:|-----------------------------------------|
| zmsc/2020/55  |   6,680,964 | pdf_extraction_empty_likely_scanned     |
| zmsc/2020/70  |   8,925,516 | pdf_extraction_empty_likely_scanned     |
| zmsc/2020/75  |   3,796,753 | pdf_extraction_empty_likely_scanned     |
| zmsc/2020/90  |   6,257,230 | pdf_extraction_empty_likely_scanned     |

Total OCR-pending PDF bytes added this tick: ~25.7 MB.

## Phase 3 — judges_registry update

One new judge added:

- **Muyovwe** (title `JS`, alias `Muyovwe JS`, first seen in
  `judgment-zm-2020-zmsc-60-matias-chitigwa-mugogo-v-the-people`,
  first_seen_at 2026-05-08T21:18:23Z).

The other five judges (Malila, Kaoma, Mambilima, Hamaundu, Chinyama)
were already canonical in the registry from prior batches.

## Phase 4 — corpus.sqlite update

Inserted 3 records via `scripts/batch_0543_sqlite_insert.py`
(re-uses b0531's TMPDIR-routed atomic copy pattern):

```
records: 1846 -> 1849 (+3)
judgments_meta: 156 -> 159 (+3)
```

Phase 5 ceiling 159/160 — **one record under ceiling**. records_fts left
to host-side rebuild via `scripts/batch_0504_build_fts5.py` per the b0517
precedent.

## Phase 5 — integrity checks

`scripts/integrity_check_b0543.py` — **PASS** for all 3 records:

- Each record has unique ID, type=judgment, outcome in allowed enum,
  issue_tags non-empty, judges non-empty.
- All 9 judge entries (3 records × 3 judges) resolve to canonical names
  in `judges_registry.yaml`.
- Each `raw_sha256` matches on-disk PDF (sha256 verified).
- Corpus-wide ID uniqueness check: 159 unique IDs, no duplicates.
- corpus.sqlite contains all 3 records in both `records` and
  `judgments_meta`.

## B2 sync

B2 sync deferred to host (`rclone` not in sandbox; same as every prior
batch since b0517).

## Cohort cumulative tracking (since b0504)

| metric                                 | b0541 | b0543 (this tick) |
|----------------------------------------|------:|-------------------:|
| written                                |    59 |                 62 |
| v0.3.3-pending deferred                |    51 |                 51 |
| OCR-pending deferred                   |    33 |                 37 |
| confirmed 404                          |    26 |                 27 |

ZMSC 2020 status after b0543: 23 of ≥89 valid nums attempted
(4 written + 1 v0.3.3-pending + 18 OCR-pending; max-num ≥ 90 confirmed,
upper boundary still unresolved).

## Daily fetch budget

| component                           | fetches |
|-------------------------------------|--------:|
| pre-tick                            |      48 |
| this tick: HEAD probes (Phase 0)    |       8 |
| this tick: GET fetches (Phase 1)    |      14 |
| **post-tick total**                 |  **70** |
| budget                              |     500 |

430 fetches remain in today's judgment-ingestion budget.

## Next-tick recommendation

1. **Continue ZMSC 2020 upper-boundary discovery** with another
   8 HEAD-only probes at fine granularity around the un-bounded ceiling
   ({95, 100, 105, 110, 115, 120, 130, 150}) to localise the true
   ZMSC 2020 max-num.
2. **GET-fetch any nums 81-89** where the internal-gap signal
   (zmsc/2020/80 = 404) suggests further internal gaps may exist.
   At 4-record yield-per-7-fetches, an 8-num GET sweep would expect
   to add roughly 3-4 more written records.
3. **OCR backfill workflow** for the now-37-record cohort
   (~269 MB scanned PDFs) — highest-leverage track because no new
   fetches required and Phase 5 ceiling is now imminently reachable
   (159/160).
4. The **51 v0.3.3-pending records** continue to await a parser
   v0.3.3 patch authored outside this scheduled tick (succeeds/fails,
   remitted, jurisdictional set-aside).
