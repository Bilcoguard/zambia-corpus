# Batch 0612 — Judgment Ingestion Worker

**Timestamp:** 2026-05-12T11:13Z
**Parser version:** 0.4.4-inline-b0612
**Phase:** priority_a_reparse_deferred (b0591 + b0593 drain)
**Fetches:** 0 (zero-fetch re-parse from raw PDFs on disk)
**Cumulative today:** 0/500

## Pre-flush state

- FTS5 integrity_check: ok
- records: 1906
- records_fts: 1906
- judgments_meta: 216

## Backup

`corpus.sqlite.bak.b0612-pre-flush-20260512T110943Z` (119,201,792 bytes)

## Inserted (5 new records)

| ID | Case Number | Date Decided | Outcome | Judges |
|----|-------------|--------------|---------|--------|
| `judgment-zm-2024-coa-083-felix-nkululumbwe-v-charles-musonda-17-others-attorney-general` | APP/083/2021 | 2024-12-24 | dismissed | Kondolo SC, Makungu, Sharpe-Phiri JJA |
| `judgment-zm-2026-coa-109-jervis-zimba-v-sankana-general-dealers` | APP/109/2023 | 2026-01-27 | dismissed | Kondolo SC, Majula, Muzenga JJA |
| `judgment-zm-2026-coa-128-robert-mwanza-v-mtn-zambia-limited` | APP/128/2023 | 2026-01-27 | allowed | Kondolo SC, Majula, Muzenga JJA |
| `judgment-zm-2026-coa-206-mutale-chanda-v-ian-musweu` | APP/206/2024 | 2026-01-13 | dismissed | Chashi, Makungu, Banda-Bobo JJA |
| `judgment-zm-2025-coa-176-bright-jangazya-v-first-national-bank-zambia-limited` | APP/176/2022 (CAZ/08/075/2022) | 2025-12-31 | dismissed | Kondolo SC, Makungu, Banda-Bobo JJA |

### Notes

- **coa-083**: Land law / specific performance dispute — claim for specific performance unsustainable absent contractual relationship with Respondents. Trial judge's misconception ruling upheld. Costs to Respondents.
- **coa-109**: Costs ground only — costs discretion appropriately exercised in favour of successful respondent (vicarious-liability employment dispute below).
- **coa-128**: First reversal in the b0591 cohort. Grounds 1 & 4 allowed (Order 11 Rule 1 S.I. 58/2020 conditional-appearance abolition not engaged — defendant rightly entered defence then challenged irregular pleadings; trial Judge erred). Matter remitted for trial before a different Judge. Ground 2 dismissed. Costs in the cause.
- **coa-206**: Res-judicata + abuse-of-process / obiter-dicta classification dispute. All grounds lack merit; lower court's res-judicata finding affirmed.
- **coa-176-bj** (Bright Jangazya): Re-parsed from raw PDF with cleaned `case_name` (was `BRIGHT JANGAZYA a j DEC 2025 v FIRST NATIONAL BANK ZAMBIA LIMITED` under v0.3.9 — `a j DEC 2025` was a Coram-line OCR artifact). All three appeal grounds dismissed for want of merit; Industrial & Labour Division origin → parties bear own costs.

## Post-flush state

- records: 1911
- records_fts: 1911
- judgments_meta: 221
- Court of Appeal coverage: **44 / 800** (5.5% of target; +5 this tick)

## Integrity checks

- CHECK1 (≥1 judge per record): **PASS** — 3 judges each on all 5
- CHECK2 (issue_tags non-empty): **PASS**
- CHECK3 (outcome ∈ enum): **PASS** — `dismissed`(×4), `allowed`(×1)
- CHECK4 (judges resolve in registry): **PASS** — all 7 distinct judges (Kondolo SC, Makungu, Sharpe-Phiri, Majula, Muzenga, Chashi, Banda-Bobo) pre-existing canonical entries
- CHECK5 (no duplicate IDs): **PASS**
- CHECK6 (raw_sha256 == on-disk sha): **PASS** — all 5 SHAs verified
- CHECK7 (no duplicate case_name+court+date): **PASS**
- CHECK8 (records.count == records_fts.count): **PASS** (1911 == 1911)

## FTS5 smoke

- `Nkululumbwe` → 1 hit (coa-083)
- `Jangazya` → 2 hits (new coa-176 + pre-existing coa-262 cosmas-mulenga-vs-bright-jangazya)
- `mwanza AND mtn` → 1 hit (coa-128)

## Parser v0.4.4-inline-b0612 — minimal upgrade from v0.4.3-inline-b0611

- **Hand-curated issue tags** (3–5 each) drawn from b0591-jiw + b0593-deferred descriptors, narrowed for decision-specificity (v0.4.3 trend continued).
- **`case_name` re-cleaning for b0593 Bright Jangazya**: stripped Coram-line bleed-through (`a j DEC 2025`) to recover canonical 3-token name. ID slug also re-cut from `bright-jangazya-a-j-dec-2025-v-first-national-bank-zambia-limited` (61 chars) to `bright-jangazya-v-first-national-bank-zambia-limited` (54 chars).
- **Direct corpus.sqlite write** (no `/tmp` staging): host `/tmp` was at 100% capacity (88M free vs 119M corpus); virtiofs mount allowed direct write without disk-IO errors this session. b0548…b0611 staging precedent suspended this tick due to capacity constraint.
- **`fetched_at`** preserved at original b0591 batch timestamp `2026-05-11T17:18:00Z` for the 4 b0591 records and `2026-05-11T17:18:00Z` for the b0593 record (consistent with raw-on-disk provenance).

## Drained-backlog accounting

**Deferred-fts5 backlog: 12 → 7.**
Drained this tick (5):
- 4× b0591 (coa-083, coa-109, coa-128, coa-206) — parsed JSON not archived; re-parsed from raw PDFs as planned at b0611
- 1× b0593 parser-clean (coa-176 bright-jangazya) — case_name v0.4 cleanup applied; body re-extracted from raw PDF

Remaining (7):
- **5 records from b0593 v0.4-pending dirty** (Lamasat, Jennifer Tembo Njovu, Mukamunya Homeowners, Emergency Response Zambia, Caz-09-127 Philemon Dyamini) — need parser upgrade for Coram-line bleed-through fix (judge names polluted with "In Chambers" / "For the Appellant" / law-firm strings; manual cleanup feasible next tick).
- **2 records from b0597** (`date_decided=null` on both — gating decision still needed re whether to insert with NULL date or block until date can be recovered).

**Scanned-PDF backlog: 10 records (unchanged).**

## Execution

Inline runner `_b0612_jiw_inline.py`. Direct write to `corpus.sqlite` (host `/tmp` at 100% capacity precluded staging). Single-transaction insert per record, with `BEGIN IMMEDIATE` and 3-table commit (records → judgments_meta → records_fts). FTS5 remained healthy across all 5 inserts. `PRAGMA journal_mode=TRUNCATE` set pre-flush per b0610 standing recommendation.

## Sweep position next tick (b0613)

`judiciary-coa-sweep: page 8 remaining` (6 unprocessed CoA candidates on judiciaryzambia.com page 8). Sweep deferred only if b0593 v0.4-pending dirty records can be parser-cleaned within the same tick — otherwise advance the sweep ahead of the dirty-cohort decision.

## Recommended next-tick sequence (b0613)

1. Re-probe FTS5 health (5 signals).
2. Take `corpus.sqlite.bak.b0613-pre-flush-...` backup.
3. **Option A** (drain-first): Manually clean 5 b0593 v0.4-pending dirty records' `case_name` and `judges` strings (Coram-line bleed-through fix), then insert.
4. **Option B** (sweep-first): Advance to `judiciary-coa-sweep: page 8` (6 candidates remaining) and defer the b0593 dirty cohort.
5. **Decision rule:** prefer Option A if all 5 dirty records share the same Coram-line bleed-through pattern (single regex fix); prefer Option B if cleanup requires per-record manual intervention.
