# Batch 0559 — judgment-ingestion-worker tick

- **Worker**: judgment-ingestion-worker (scheduled task `judgment-ingestion`)
- **Wall-clock window**: 2026-05-09T11:00Z..11:12Z (UTC, ~12 min, well under 20 min target)
- **Phase**: Phase 5 dedicated post-completion ingestion (continued).
- **Parser**: v0.3.2 baseline (`scripts/batch_0498_parse.py:build_record_v032`,
  re-pointed via `scripts/batch_0559_parse.py` thin wrapper at `_work/b0559/`).
  No parser, fetcher, or core-logic modifications. Configuration-tier reuse via
  `scripts/batch_0559_fetch.py` (thin wrapper around `batch_0506_zmsc_fetch.fetch_one`).
- **Outcome**: **0 records written, 8 deferred, 20 fetches consumed.
  Zero-yield tick.** ZMCC 2020 upper boundary now confirmed at num 18.

## Tick decision (priority order)

a. **REPARSE DEFERRED** — skipped. Parser_v0.3.2 cannot move the
   v0.3.3-pending cohort (now 61 records after this tick). Standing
   recommendation per b0552 / b0557 / b0558 unchanged.
b. **SCZ SWEEP** — skipped. ZMSC 2024 (b0550), 2025 (b0547), 2026
   (b0558) all confirmed-exhausted within ZambiaLII's visible
   numbering window.
c. **ZMCC NEW YEARS** — chosen. b0558 began ingesting ZMCC 2020
   (nums 1-8 fetched, 2 written) and identified two follow-ups:
   nail down the upper boundary in [16..19] and continue fetching
   nums 9-15. b0559 does both.

## Phase 0 — HEAD probe (ZMCC 2020 boundary) — 4 fetches

`_work/b0559/head_probe_zmcc.py` (ad-hoc inline probe, b0547/b0550/b0558
pattern). Targeted probe to nail down the upper boundary.

| court / year / num | code | status / final URL                                |
|--------------------|-----:|---------------------------------------------------|
| zmcc / 2020 / 16   | 200  | OK → `…/eng@2020-02-19`                           |
| zmcc / 2020 / 17   | 200  | OK → `…/eng@2020-04-24`                           |
| zmcc / 2020 / 18   | 200  | OK → `…/eng@2020-09-20`                           |
| zmcc / 2020 / 19   | 404  | absent                                             |

**Verdict**: ZMCC 2020 upper boundary **confirmed at num 18**. Combined
with b0558's HEAD probe (nums 1, 5, 10, 15 OK; 20, 25 = 404), the year
is fully bounded: nums 1-18 published on ZambiaLII, no internal gaps
detected in the sparse sample. Total ZMCC 2020 = **18 records**.

## Phase 1 — fetch via `batch_0506_zmsc_fetch.fetch_one` — 16 fetches

`scripts/batch_0559_fetch.py` (thin wrapper around the b0506 fetcher
with the generic `/akn/zm/judgment/{court}/{year}/{num}/eng` URL
pattern). Rate-limited to 5s between requests per
`approvals.yaml.zambialii_seconds_between_requests`.

| court / year / num | status | date_decided | html bytes | pdf bytes  |
|--------------------|--------|--------------|-----------:|-----------:|
| zmcc / 2020 / 9    | ok     | 2020-10-20   | 38,502     | 4,519,966  |
| zmcc / 2020 / 10   | ok     | 2020-11-19   | 38,418     | 6,130,241  |
| zmcc / 2020 / 11   | ok     | 2020-11-24   | 44,513     | 1,800,021  |
| zmcc / 2020 / 12   | ok     | 2020-12-10   | 45,340     | 3,642,792  |
| zmcc / 2020 / 13   | ok     | 2020-05-29   | 38,266     | 351,748    |
| zmcc / 2020 / 14   | ok     | 2020-07-17   | 43,658     | 1,881,220  |
| zmcc / 2020 / 15   | ok     | 2020-12-10   | 45,548     | 4,663,583  |
| zmcc / 2020 / 16   | ok     | 2020-02-19   | 41,193     | 2,545,740  |

All eight resolved via the canonical
`/akn/zm/judgment/zmcc/{year}/{num}/eng` redirect to a dated
`eng@YYYY-MM-DD` URL. 16 successful HTTP fetches; zero errors.

## Phase 2 — parse via parser_v0.3.2

`scripts/batch_0559_parse.py` (thin wrapper) re-pointed
`scripts/batch_0498_parse.build_record_v032` at `_work/b0559/`.

| court / year / num | result   | reason                                                                           |
|--------------------|----------|----------------------------------------------------------------------------------|
| zmcc / 2020 / 9    | deferred | `pdf_extraction_empty_likely_scanned` (PDF 4.5 MB, pdfplumber <200 chars)         |
| zmcc / 2020 / 10   | deferred | `pdf_extraction_empty_likely_scanned` (PDF 6.1 MB, pdfplumber <200 chars)         |
| zmcc / 2020 / 11   | deferred | `html_no_summary_pdf_no_match` (interlocutory motion / Article 154)               |
| zmcc / 2020 / 12   | deferred | `html_no_summary_pdf_no_match` (Article 189(2) early retirement; declaratory)     |
| zmcc / 2020 / 13   | deferred | `pdf_extraction_empty_likely_scanned` (PDF 0.34 MB, pdfplumber <200 chars)        |
| zmcc / 2020 / 14   | deferred | `html_no_summary_pdf_no_match` (discretionary procedural relief; out-of-time)     |
| zmcc / 2020 / 15   | deferred | `html_no_summary_pdf_no_match` (Article 189(2) early retirement; companion to 12) |
| zmcc / 2020 / 16   | deferred | `html_no_summary_pdf_no_match` (committal-notice particulars; declaratory)        |

**Zero-yield tick — 0/8 records written.** This is the third highest-
deferral-density slice observed in any ZMCC sweep (after the
ZMCC 2017-2019 cohort, which has not yet been fetched). The 5
declaratory/interlocutory holdings have well-formed HTML summaries
but no operative-verb anchor that v0.3.2 recognises (verbs sit in
sub-clauses or describe legal effect rather than the order made).
The 3 scanned PDFs cannot be parsed without OCR. None of these are
parser bugs — they are the expected v0.3.3-pending and OCR-pending
cohorts.

### Records deferred (all 8 appended to gaps.md)

All 8 deferrals were appended to `gaps.md` with the b0559 stamp,
including raw_sha256 for each PDF. The 5 v0.3.3-pending entries
join the existing cohort (now 61 records); the 3 OCR-pending entries
extend the ZMCC 2020 scanned-PDF cluster (now 5 records, ~28% of
the year — materially higher than later years).

## Phase 3 — judges registry update

**No changes.** Zero records written = zero new judges encountered.
`judges_registry.yaml` unchanged. (Judges from the 8 deferred records
will be added to the registry when those records are eventually
parsed under v0.3.3 / post-OCR.)

## Phase 4 — corpus.sqlite update

**Skipped.** Zero records written = nothing to insert. Pre-tick
sanity check confirmed `records=1853 records_fts=1853 judgments_meta=163`
unchanged from b0558 final state, and `PRAGMA integrity_check=ok`.

| table          | before | after | delta |
|----------------|-------:|------:|------:|
| records        |  1853  | 1853  |   0   |
| records_fts    |  1853  | 1853  |   0   |
| judgments_meta |   163  |  163  |   0   |

## Phase 5 — integrity checks (PASS)

- ✓ Raw bytes on disk for all 8 b0559 fetches (HTML 38k-46k, PDF 0.34MB-6.13MB)
- ✓ All 8 raw_sha256 values recomputed and recorded in gaps.md
- ✓ corpus.sqlite `records ∖ records_fts` gap = 0 (still satisfies
  the strict assertion the repair-worker is held back by)
- ✓ corpus.sqlite no duplicate IDs (1853 unique)
- ✓ b0558 records (`zmcc-2020-02-kambwili`, `zmcc-2020-03-dean-masule`)
  still resolve in both `records` and `records_fts`
- ✓ `PRAGMA integrity_check` → `ok`

(No "judges resolve in registry" or "issue_tags non-empty" or
"outcome from enum" checks needed this tick — those are write-time
checks and zero records were written.)

## Budget and rate limits

- Fetches today before tick: 120 / 500
- Fetches consumed this tick: 20 (4 HEAD probes ZMCC 2020 boundary
  + 8 HTML + 8 PDF GET fetches ZMCC 2020 nums 9-16)
- Fetches today after tick: 140 / 500
- Rate limit: 5s between zambialii.org requests (honoured throughout)
- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`

## approvals.yaml

NOT modified. Phase 5 ceiling 163/160 unchanged (still 3 above the
upper sentinel). Recommend operator action to extend the ceiling band
or formally close Phase 5 (per b0553 / b0557 / b0558 standing
recommendation).

## Cohort tally

| cohort                              | pre-b0559 | b0559 Δ | post-b0559 |
|-------------------------------------|----------:|--------:|-----------:|
| corpus records (all)                |  1853     |    0    |  1853      |
| ZMCC 2020 records written           |     2     |    0    |     2      |
| ZMCC 2020 raw on disk               |     8     |   +8    |    16      |
| v0.3.3-pending cohort               |    56     |   +5    |    61      |
| OCR-pending cohort (all years)      |     2     |   +3    |     5      |
| OCR-pending — ZMCC 2020 only        |     2     |   +3    |     5      |

## Out-of-tick follow-ups (recommendations for next ticks / operator)

1. **Finish ZMCC 2020** — GET-fetch nums {17, 18} (2 records,
   ~4 fetches). After this ZMCC 2020 is completely covered on
   disk. Likely yield 0-1 written records given the b0559 pattern
   (5/8 declaratory). Carry to next tick.
2. **Pivot to ZMCC 2019** — start sparse-sample HEAD probe of the
   next uncovered year. If similar pre-2020 publication patterns
   hold, expect 6-12 records per year and substantial OCR exposure.
3. **Author parser_v0.3.3 anchor patterns** for the declaratory /
   interlocutory holding families now identified (61 records pending);
   patterns observed include sub-clause "dismissed" / "must be
   retained" / "is fatal" / "exercised discretion to allow" / "ruled
   it lacks jurisdiction".
4. **OCR pipeline implementation** — 5 ZMCC 2020 records pending
   (nums 7, 8 from b0558; 9, 10, 13 from b0559). At ~28% scanned-PDF
   prevalence in this year, ZMCC 2017-2019 likely have similar or
   higher rates and the OCR pipeline is becoming a higher-priority
   blocker than parser_v0.3.3.
5. **Operator action on Phase 5 ceiling** 163/160 — now 3 above the
   sentinel since b0558. Recommend extend-band or close-Phase-5 at
   next opportunity.
6. **rclone B2 sync deferred to host** — the 8 new raw files
   (`raw/zambialii/judgments/zmcc/2020/judgment-zm-2020-zmcc-{09..16}-*.{html,pdf}`)
   total ~25 MB and are awaiting B2 sync.
