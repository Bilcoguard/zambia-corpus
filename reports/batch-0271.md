# Batch 0271 — Phase 4 (acts_in_force) cross-alphabet residual sweep

**Tick start:** 2026-04-26T15:02:00Z
**Tick end:** ~2026-04-26T15:18Z
**Phase:** phase_4_bulk (priority_order item 1: `acts_in_force`)
**Result:** 8/8 ok (100% yield) — extends 100%-yield streak to 26 consecutive batches (0246–0271)

## Picks (8/8 ingested)

| # | alpha | yr/num | id | sections | parser path |
|---|-------|--------|----|----------|-------------|
| 0 | E | 1987/13 | act-zm-1987-013-excess-expenditure-appropriation-1984-act-1987 | 1 | PDF |
| 1 | E | 1988/14 | act-zm-1988-014-excess-expenditure-appropriation-1985-act-1988 | 12 | PDF |
| 2 | S | 1988/15 | act-zm-1988-015-supplementary-appropriation-1986-act-1988 | 34 | PDF |
| 3 | E | 1988/30 | act-zm-1988-030-excess-expenditure-appropriation-1986-act-1988 | 2 | PDF |
| 4 | E | 1989/32 | act-zm-1989-032-excess-expenditure-appropriation-1987-act-1989 | 2 | PDF |
| 5 | E | 1990/38 | act-zm-1990-038-excess-expenditure-appropriation-1988-act-1990 | 1 | PDF |
| 6 | E | 1992/15 | act-zm-1992-015-excess-expenditure-appropriation-1989-act-1992 | 1 | PDF |
| 7 | P | 1993/20 | act-zm-1993-020-prices-and-incomes-commission-dissolution-act-1993 | 12 | PDF |

7 short-form fiscal Appropriation / Excess Expenditure Acts (E and S series) plus 1 P (Prices and Incomes Commission Dissolution 1993). All 8 fell back to PDF parsing because the HTML representation had fewer than 2 `akn-section` blocks (consistent with batches 0269/0270 patterns for fiscal acts).

## Discovery

- Robots.txt re-verified at tick start (sha256 `fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0` — unchanged from batches 0193–0270; crawl-delay 5s honoured at 6s margin). Cached at `raw/zambialii/_robots/robots-20260426T150502Z.txt`.
- 0 new alphabet listing fetches this tick (all 24 A–Z listings cached; X confirmed empty in 0269).
- Cross-alphabet residual sweep over cached A–Z listings filtered against `records/acts/**/*.json` (`act-zm-YYYY-NNN-…` and legacy `act-…-YYYY` formats — 893 (yr,num) keys derived). After excluding 3 known-deferred items (1956/4 S, 1996/17 C, 2006/9 C) **18 non-deferred residuals** were identified — exactly matching batch 0270's prediction. The 8 chronologically-first picks were taken; **10 residuals carry to next tick**.

## Picks not yet on disk — cross-checked

For each pick, `(yr, num)` was tested against the 893 `(yr,num)` keys derived from the on-disk acts corpus before fetching. All 8 confirmed not on disk — no silent overwrite (BRIEF non-negotiable #4).

## Integrity (`_work/integrity_0271.py`)

- **CHECK1a** batch unique ids: 8/8 unique
- **CHECK1b** corpus presence on disk: 8/8 written under `records/acts/{1987,1988,1989,1990,1992,1993}/`
- **CHECK2** amended_by refs: 0 (none on these acts)
- **CHECK3** repealed_by refs: 0
- **CHECK4** source_hash sha256 matches raw on-disk HTML: 8/8
- **CHECK5** required-field count: 16 × 8 = 128/128 present
- **CHECK6** cited_authorities refs: 0
- **Result:** PASS

## Costs (this batch)

| Kind | Count |
|---|---|
| robots.txt re-verify | 1 |
| alphabet listings | 0 |
| record HTML fetches | 8 (slice 0:3 truncated by host 45s timeout after writing 2 records — re-driven as 2:4 + 4:6 + 6:8 with 1988/15 HTML re-fetched once, same sha256, no parser drift) |
| PDF fallback fetches | 8 |
| **Total this batch** | **17** |

Today running total: 363 (pre-tick) + 17 = **380 / 2000** fetches (19.0% of daily budget). Tokens within budget.

## Cumulative state after batch 0271

- acts: **1032** (+8 over 1024)
- SIs: 593 (unchanged from batch 0252)
- judgments: 25 (paused per robots Disallow on `/akn/zm/judgment/`)

## Reserved residuals carried to next tick

**10 cross-alphabet acts_in_force candidates** (chronological):
- P 1993/24 Prescribed Minerals and Materials Commission (Dissolution) Act, 1993
- E 1994/30 Excess Expenditure Appropriation (1991) Act, 1994
- P 1994/45 Presidential Emoluments (Amendment) Act, 1994
- E 1995/32 Excess Expenditure Appropriation (1992) Act, 1993 (filed under 1995)
- E 1997/22 Excess Expenditure Appropriation (1993) Act, 1997
- E 2000/8 Excess Expenditure Appropriation (1995) Act, 2000
- E 2000/16 Excess Expenditure Appropriation (1997) Act, 2000
- E 2003/17 Excess Expenditure Appropriation (1998) Act, 2003
- E 2004/4 Excess Expenditure Appropriation (1999) Act, 2004
- N 2005/17 National Health Services (Repeal) Act, 2005

Prior reserved residuals still pending:
- 1 S residual: 1956/4 Service of Process and Execution of Judgments — disambiguator-deferred
- 2 C deferred: Citizens Economic Empowerment 2006/9 + Constitution of Zambia 1996/17 (large; dedicated batches)
- 1 SI residual: 1990/39 ZNPF >4.5 MB — OCR backlog (15 items)

## Next-tick plan

1. Sweep next 8 of 10 cross-alphabet residuals (E series 1994–2004 will dominate, plus P/N entries).
2. Implement disambiguator-aware fetch handler for 1956/4.
3. OCR retry on 15-item SI backlog once tesseract is wired (deferred to host).
4. Re-verify robots.txt at start of next tick.
5. Once cross-alphabet residual queue empties (≤2 ticks), revisit alphabet sweeps for residuals introduced by upstream changes since 2026-04-25.

## Infrastructure follow-up (non-blocking)

- batch-0271 raw files (8 act HTML + 8 PDF + 1 robots; 0 alphabet listing) plus accumulated batches 0192–0270 raw files awaiting host-driven B2 sync (`rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4` — rclone unavailable in sandbox).
- Persistent virtiofs unlink-failure warnings on `.git/objects/tmp_obj_*` and `.git/objects/maintenance.lock` unchanged from batches 0192–0270 (rename succeeds, unlink fails — non-fatal).
- SQLite snapshot drift unchanged (`corpus.sqlite` still at 543 records vs 1598 JSON on disk after this batch) — periodic full rebuild expected from host.
- Pre-existing FTS5 vtable malformed image (`records_fts`) unchanged — non-blocking for record integrity, flagged for full-rebuild scope.

Parser version: `0.6.0-act-zambialii-2026-04-26` (unchanged across 0252–0271).
