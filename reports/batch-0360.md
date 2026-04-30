# Batch 0360 — Phase 5 ZMCC ingestion (parser_v0.3.1 introduces PDF-tail-2-pages outcome fallback)

- Tick start: 2026-04-30T03:01Z
- Tick end:   2026-04-30T03:12Z
- Sandbox session: lucid-stoic-gauss
- Parser version: 0.3.1 (NEW this batch)
- Phase: 5 (judgments) — approved=true, complete=false
- Phase 5 progress at end of tick: 35 / 100-160 target (was 30 at b0359)

## What changed (parser_v0.3.0 -> 0.3.1)

Per Peter's instruction (2026-04-30): "When a judgment's outcome cannot be inferred
from the HTML summary, read the PDF's final 2 pages to find the order/disposition
paragraph. Extract the outcome from there. This should clear most of the deferred
judgments."

Two changes:

1. **PDF-tail-2-pages fallback** (new). After the existing `summary` and
   `pdf-anchor:<keyword>` paths fail, the parser now extracts the final 2 pages of
   the PDF (or the last ~10000 chars of the full extracted text if the final-2
   pages come up empty under pdfplumber) and scans a new pattern set,
   `PDF_TAIL_PATTERNS`, tuned for the active-voice operative paragraph that
   characterises Zambian judgments ("we therefore dismiss the Petition", "petition
   is forthwith dismissed", "we decline to grant the reliefs sought", numbered
   closing orders, etc.). The latest match in the tail (= operative paragraph,
   which sits at the end) wins, and the same `_detail_is_safe` sanity check that
   protects the summary path is applied.

2. **JJS title token** added to the judges-title regex (fixes the `Chibomba JJS`
   case noted in worker.log b0359 post-parse fix). `JJS` had been missing from
   the alternation `(PC|DPC|CJ|DCJ|JCC|JJC|JC|JS|JA|J|JJ|JJA)` so the last-token
   fallback produced a bogus canonical "Jjs". Fix: insert `JJS` ahead of `JS`
   in all three regex sites.

Pre-existing logic (HTML summary path, PDF order-anchor path) is unchanged - the
fallback is strictly additive, so no record that would have been written under
parser_v0.3.0 fails to be written under v0.3.1.

Reprocessing of older deferred judgments listed in `gaps.md` (under
`outcome_not_inferable_under_tightened_policy`) is reserved for future ticks per
Peter's instruction; this batch only applies the new logic to the 8 fresh
candidates.

## Targets (8 candidates this batch)

ZMCC 2021/{24, 23} (top of year, fresh) plus ZMCC 2021/{17, 16, 15, 14, 13, 12}
(continuation of the DESC sweep, picking up after the b0359 deferred-tail).
Note: 2021/{18, 19, 21, 22} were deferred in earlier ticks and are NOT reprocessed
here - see "future work" below.

## Outcome

**5 records written / 3 deferred.**

| ZMCC #  | Date       | Case                                                        | Outcome   | Source path        |
|---------|------------|-------------------------------------------------------------|-----------|--------------------|
| 2021/24 | 2021-10-27 | Gilford Malenji v Zambia Airports Corporation Limited       | dismissed | summary            |
| 2021/23 | 2021-11-29 | Charles Chihinga v New Future Financial Company Limited     | dismissed | **pdf-tail-2pages**|
| 2021/17 | 2021-09-20 | Anderson Mwale, Buchisa Mwalongo and Kola Odubote v ...     | dismissed | summary            |
| 2021/16 | 2021-11-22 | Sampa v Mundubile and Anor                                  | dismissed | **pdf-tail-2pages**|
| 2021/13 | 2021-07-20 | Bric Back Limited T/A Gamamwe Ranches v Kirkpatrick         | dismissed | **pdf-tail-2pages**|

3 of 5 records were rescued by the new pdf-tail-2pages path - confirming that the
fallback does meaningful work on candidates that would otherwise have been
deferred under parser_v0.3.0.

## Deferred (3)

- **2021/15 - Shunxue v The Attorney General & Anor (44 pages):** pdfplumber
  returned empty extraction across all pages. Likely scanned/image-based PDF.
  HTML summary did not yield a disposition either. **Root cause: PDF extraction
  failure, not parser policy.** Tail fallback cannot help here. -> defer to
  OCR pass (future scope).

- **2021/14 - Legal Resources Foundation Limited & 2 Others v Edgar Lungu
  (104 pages):** same - pdfplumber extraction empty, likely scanned PDF.

- **2021/12 - Dipak Patel v Minister of Finance and Attorney General
  (75 pages):** PDF extraction worked (~95k chars) but the operative paragraph
  is a single judge's separate opinion ("I would therefore go further and
  suspend the declaration of unconstitutionality...") with no clear majority
  disposition phrase. Multi-judge separate-opinion cases are a known gap.

All 3 deferreds are appended to `gaps.md` under reasons distinct from the
generic `outcome_not_inferable_under_tightened_policy`, so a future re-parse pass
can target them specifically.

## Integrity checks — PASS (5/5)

`scripts/integrity_check_b0360.py`:

- 5/5 unique IDs (no duplicates within batch, no collisions with prior batches)
- 5/5 records have all 20 required fields
- 5/5 outcome in enum
- 5/5 court in enum (`Constitutional Court of Zambia`)
- 5/5 >=1 judge resolves in `judges_registry.yaml`
- 5/5 `judges[*].role` in enum
- 5/5 >=1 issue_tag from Flynote
- 5/5 `source_hash` matches raw HTML sha256 on disk
- 5/5 `raw_sha256` matches raw PDF sha256 on disk
- 5/5 ID matches locked pattern
- 5/5 date_decided matches `YYYY-MM-DD`
- 5/5 outcome_detail safety: >=12 alpha chars, no blacklisted substrings, no
  leading lowercase mid-word fragment

## Budgets

- Fresh fetches today: 2 (1 HTML + 1 PDF for ZMCC 2021/12; 7 of 8 candidates were
  already on disk from the b0359 fetcher's discovery probes).
- Cumulative today: 0 -> 2 / 2000 (~0.1%).
- Token usage: well under 1M/day budget.
- B2 sync: deferred to host (rclone not in sandbox).

## corpus.sqlite

Not modified this tick. Pre-existing B-tree corruption on pages 84..99 remains;
canonical source-of-truth continues to be `records/**/*.json`.

## Future work flagged

1. **OCR pass for image-based ZMCC PDFs.** 2021/14 and 2021/15 cannot be parsed
   without OCR. Scope this in a sibling phase (or a sub-task of phase_5).
2. **Multi-judge separate-opinion handling.** 2021/12 needs a "majority view"
   inference. Defer.
3. **Re-parse pass for older deferreds.** Apply parser_v0.3.1 to the candidates
   already deferred under v0.3.0 in batches b0344..b0359 (raw bytes on disk,
   listed in gaps.md). Per Peter's 2026-04-30 instruction.
