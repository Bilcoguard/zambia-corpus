# Batch 0558 — judgment-ingestion-worker tick

- **Worker**: judgment-ingestion-worker (scheduled task `judgment-ingestion`)
- **Wall-clock window**: 2026-05-09T10:06Z..10:20Z (UTC, ~14 min, well under 20 min target)
- **Phase**: Phase 5 dedicated post-completion ingestion (continued).
- **Parser**: v0.3.2 baseline (`scripts/batch_0498_parse.py:build_record_v032`,
  re-pointed via `scripts/batch_0558_parse.py` thin wrapper at `_work/b0558/`).
  No parser, fetcher, or core-logic modifications. Configuration-tier reuse via
  `scripts/batch_0558_fetch.py` and `scripts/batch_0558_sqlite_insert.py`.
- **Outcome**: **2 records written, 6 deferred, 28 fetches consumed**.
  First-ever ZMCC 2020 records added to the corpus.

## Tick decision (priority order)

a. **REPARSE DEFERRED** — skipped. The two most recent reparse ticks
   (b0544, b0552) both redeferred all 8 candidates under
   `html_no_summary_pdf_no_match`; the 52-record v0.3.3-pending cohort
   cannot move under the current parser_v0.3.2 anchor inventory and
   authoring v0.3.3 anchor additions is out-of-tick work (per b0552 and
   b0557 standing recommendation).
b. **SCZ SWEEP** — partially attempted (HEAD probes only). ZMSC 2026
   internal-gap and upper-boundary discovery: probed
   `{5, 11, 12, 13, 14, 15}` → 6/6 = 404. Combined with prior years:
   - ZMSC 2026 → upper boundary num=10 confirmed (5 consecutive 404s
     above; permanent internal gap at num=5)
   - ZMSC 2025 → upper boundary num=32 confirmed (b0547)
   - ZMSC 2024 → upper boundary num=34 confirmed (b0550)
   All three current/recent years now exhausted within ZambiaLII's
   visible numbering window. Pivoted to (c).
c. **ZMCC NEW YEARS** — chosen for this tick. ZMCC 2017–2020 had no
   records *and no raw files* on disk before this tick (records start
   at 2021). 2020 was the most recent uncovered year so swept first.

## Phase 0 — HEAD probe (ZMCC 2020) — 6 fetches

`_work/b0558/head_probe_zmcc.py` (ad-hoc inline probe, b0547/b0550
pattern). Sparse sample to confirm year is published before committing
GET-fetch budget.

| court / year / num | code | status / final URL                                                  |
|--------------------|-----:|---------------------------------------------------------------------|
| zmcc / 2020 / 1    | 200  | OK → `…/eng@2020-01-30`                                              |
| zmcc / 2020 / 5    | 200  | OK → `…/eng@2020-05-20`                                              |
| zmcc / 2020 / 10   | 200  | OK → `…/eng@2020-11-19`                                              |
| zmcc / 2020 / 15   | 200  | OK → `…/eng@2020-12-10`                                              |
| zmcc / 2020 / 20   | 404  | absent                                                               |
| zmcc / 2020 / 25   | 404  | absent                                                               |

**Verdict**: ZambiaLII publishes ZMCC 2020. Upper boundary lies between
15 (OK) and 20 (404). Delivery dates span the calendar year. Proceed
to GET fetch nums `{1..8}`.

## Phase 1 — fetch via `batch_0506_zmsc_fetch.fetch_one` — 16 fetches

`scripts/batch_0558_fetch.py` (thin wrapper around the b0506 fetcher
which uses a generic `/akn/zm/judgment/{court}/{year}/{num}/eng`
URL pattern that works for both ZMSC and ZMCC). Rate-limited to 5s
between requests per `approvals.yaml.zambialii_seconds_between_requests`.

| court / year / num | status | date_decided | html bytes | pdf bytes  |
|--------------------|--------|--------------|-----------:|-----------:|
| zmcc / 2020 / 1    | ok     | 2020-01-30   | 41,992     | 3,768,388  |
| zmcc / 2020 / 2    | ok     | 2020-02-18   | 43,104     | 5,267,850  |
| zmcc / 2020 / 3    | ok     | 2020-02-05   | 47,964     | 4,053,144  |
| zmcc / 2020 / 4    | ok     | 2020-07-03   | 50,439     | 6,169,355  |
| zmcc / 2020 / 5    | ok     | 2020-05-20   | 47,816     | 4,223,573  |
| zmcc / 2020 / 6    | ok     | 2020-10-16   | 51,898     | 7,579,165  |
| zmcc / 2020 / 7    | ok     | 2020-10-28   | 38,301     | 6,680,798  |
| zmcc / 2020 / 8    | ok     | 2020-11-03   | 38,159     | 2,950,638  |

All eight resolved via the canonical
`/akn/zm/judgment/zmcc/{year}/{num}/eng` redirect to a dated
`eng@YYYY-MM-DD` URL. 16 successful HTTP fetches; zero errors.

## Phase 2 — parse via parser_v0.3.2

`scripts/batch_0558_parse.py` (thin wrapper) re-pointed
`scripts/batch_0498_parse.build_record_v032` at `_work/b0558/`. The
v0.3.2 baseline already handles ZMCC court_full ("Constitutional
Court of Zambia") and citation pattern (`[YYYY] ZMCC NN`) correctly
— no parser changes needed.

| court / year / num | result   | outcome   | outcome_source                                                              |
|--------------------|----------|-----------|-----------------------------------------------------------------------------|
| zmcc / 2020 / 1    | deferred | —         | `html_no_summary_pdf_no_match` (declaratory holding; joins v0.3.3-pending)  |
| zmcc / 2020 / 2    | written  | dismissed | `summary[…dismissed]` v0.3.2 anchor                                          |
| zmcc / 2020 / 3    | written  | dismissed | `pdf-tail-2pages[v031-tail:…appeal\|petition\|application…fail]`             |
| zmcc / 2020 / 4    | deferred | —         | `html_no_summary_pdf_no_match` (declaratory holding)                         |
| zmcc / 2020 / 5    | deferred | —         | `html_no_summary_pdf_no_match` (declaratory holding)                         |
| zmcc / 2020 / 6    | deferred | —         | `html_no_summary_pdf_no_match` (interlocutory expungement holding)           |
| zmcc / 2020 / 7    | deferred | —         | `pdf_extraction_empty_likely_scanned` (likely scanned PDF — needs OCR)       |
| zmcc / 2020 / 8    | deferred | —         | `pdf_extraction_empty_likely_scanned` (likely scanned PDF — needs OCR)       |

### Records written

1. `judgment-zm-2020-zmcc-02-kambwili-v-attorney-general`
   - Citation: [2020] ZMCC 2
   - Title: *Kambwili v Attorney-General* (9 of 2019) — 18 February 2020
   - Court: Constitutional Court of Zambia
   - Judges: Chibomba PC (presiding); Sitali, Mulenga, Mulonda,
     Musaluke (concurring) — all JCC
   - Outcome: `dismissed` — *"Court held Speaker exceeded powers by
     interpreting Article 72 and ruling on a sub judice matter;
     petition dismissed, each party to bear own costs"*
   - Issue tags: Constitutional law; separation of powers;
     parliamentary exclusive cognisance; Article 72 / 77(1) / 119;
     declaratory relief and justiciability.
   - raw_sha256: `b95d63e881552ac718dc7042a60c35782f3da0b6957571eae1c0045a89819afd`

2. `judgment-zm-2020-zmcc-03-dean-masule-v-kangombe`
   - Citation: [2020] ZMCC 3
   - Title: *Dean Masule v Kangombe* — 5 February 2020
   - Court: Constitutional Court of Zambia
   - Judges: Chibomba PC (presiding); Mulenga, **Mulembe**, Munalula,
     Musaluke (concurring) — all JCC
   - Outcome: `dismissed` (election petition appeal failed)
   - Issue tags: Electoral law; Electoral Process Act s.97(2)(b);
     burden of proof in election petitions; *Josephat Mlewa* relevance.
   - raw_sha256: `4e4ab822c21373a4b6af8b6867f1cf8444d64d117f44c41316157e1c05d3ca9b`

### Records deferred

All 6 deferrals were appended to `gaps.md` with the b0558 stamp. The
4 v0.3.3-pending entries (nums 1, 4, 5, 6) are declaratory or
interlocutory holdings whose summary contains no operative verb that
parser_v0.3.2 recognises; their summaries are well-formed but
non-anchorable. The 2 OCR candidates (nums 7, 8) returned <200 chars
from pdfplumber and need OCR before any reparse.

## Phase 3 — judges registry update

| judge       | title | aliases now                              | first_seen_in (this tick)                                     |
|-------------|-------|------------------------------------------|----------------------------------------------------------------|
| Chibomba    | PC    | Chibomba PC, Chibomba JJS                | (existing canonical)                                           |
| Sitali      | JCC   | Sitali JC, Sitali JJC, Sitali JCC        | (existing canonical, JCC already known)                        |
| Mulenga     | JCC   | Mulenga JC, Mulenga JJC, Mulenga JCC     | (existing canonical, JCC already known)                        |
| Mulonda     | JCC   | Mulonda JJC, Mulonda JC, Mulonda JCC     | (existing canonical, JCC already known)                        |
| Musaluke    | JCC   | Musaluke JCC, JJC, JC + honorific alias  | (existing canonical, JCC already known)                        |
| Munalula    | JCC   | Munalula PC, JCC, JJC, DPC               | (existing canonical, JCC already known)                        |
| **Mulembe** | JCC   | Mulembe JCC                              | **NEW canonical** — `judgment-zm-2020-zmcc-03-dean-masule-v-kangombe` |

Net: 1 new canonical name; 0 new aliases for existing canonicals
(all six prior canonicals already had a JCC alias from later years).
Diff: 8 lines added to `judges_registry.yaml`.

## Phase 4 — corpus.sqlite update

TMPDIR-routed atomic copy (b0531 pattern) plus PRAGMA
`journal_mode=TRUNCATE` (b0557 workaround for the FUSE/virtiofs
restriction on `unlink(2)` of the rollback journal). Per-record commits.

| table          | before | after | delta |
|----------------|-------:|------:|------:|
| records        |  1851  | 1853  |  +2   |
| records_fts    |  1851  | 1853  |  +2   |
| judgments_meta |   161  |  163  |  +2   |

`PRAGMA integrity_check` → `ok`. `records ∖ records_fts` gap = 0
(strict assertion satisfied; repair-worker can continue body repairs).

## Phase 5 — integrity checks (PASS)

- ✓ Every judgment has at least one judge (5 each)
- ✓ `issue_tags` non-empty (4 entries each, from HTML flynote)
- ✓ `outcome` from allowed enum (`dismissed`)
- ✓ All `judges[].name` resolve in `judges_registry.yaml` (36 canonical names total after this tick)
- ✓ No duplicate IDs in corpus (1853 unique)
- ✓ `raw_sha256` matches on-disk PDF (re-hashed both files)
- ✓ FTS sanity searches: `Kambwili`, `Masule`, `Dean Masule` each return exactly the expected row.

## Budget and rate limits

- Fetches today before tick: 92 / 500
- Fetches consumed this tick: 28 (6 HEAD probes ZMSC 2026 + 6 HEAD
  probes ZMCC 2020 + 8 HTML + 8 PDF GET fetches ZMCC 2020)
- Fetches today after tick: 120 / 500
- Rate limit: 5 s between zambialii.org requests (honoured throughout)
- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`

## approvals.yaml

NOT modified. Phase 5 ceiling 161/160 → 163/160 (now 3 above the upper
sentinel). The judgment-ingestion-worker does not touch
`approvals.yaml`; recommend operator action to extend the ceiling band
or formally close Phase 5 (per b0553 / b0557 standing recommendation).

## Cohort tally (ZMSC + ZMCC head probes, cumulative since b0504)

| court / year | head OK | head 404 | written this tick | written cumulative |
|--------------|--------:|---------:|------------------:|-------------------:|
| zmsc / 2026  | unchanged | +6 | 0 | 7 (records on disk) |
| zmcc / 2020  | +4       | +2  | 2 | 2 (NEW year)        |

Cumulative since b0504: **66 OK / 52 OK / 37 OK / 40 confirmed-404 /
4 OK ZMCC-2020-new** (slight extension over b0553's
64-52-37-40 with this tick adding ZMCC 2020 as a new dimension).

## Out-of-tick follow-ups (recommendations for next ticks / operator)

1. **HEAD-probe ZMCC 2020/{16, 17, 18, 19}** to nail down upper
   boundary (currently known to lie in 16–19 inclusive).
2. **Continue priority (c)** with ZMCC 2020/{9..15} GET fetches next
   tick (high probability all OK based on this tick's 8/8 yield).
3. **Author parser_v0.3.3 anchor patterns** for the 4 declaratory /
   interlocutory holding families this tick added — total v0.3.3-
   pending cohort now ~58 records (52 prior + 4 new + 2 not counted as
   they need OCR).
4. **OCR pipeline for scanned PDFs** — zmcc/2020/7 and zmcc/2020/8
   are the first scanned-PDF deferrals encountered; if more appear in
   ZMCC 2020-and-earlier sweeps, an OCR fallback (Tesseract or
   pdf-to-image + cloud OCR) becomes worth implementing.
5. **Operator action on Phase 5 ceiling** 163/160 — now 3 above the
   sentinel. Recommend extend-band or close-Phase-5 at next opportunity.
6. **rclone B2 sync deferred** to host (rclone not in sandbox) — the
   8 new raw files (`raw/zambialii/judgments/zmcc/2020/*.{html,pdf}`)
   total ~40 MB and are awaiting B2 sync.
