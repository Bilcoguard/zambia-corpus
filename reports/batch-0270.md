# Batch 0270 — Phase 4 (acts_in_force) cross-alphabet residual sweep

**Tick start:** 2026-04-26T14:32:53Z
**Tick end:** ~2026-04-26T14:55Z
**Phase:** phase_4_bulk (priority_order item 1: `acts_in_force`)
**Result:** 8/8 ok (100% yield) — extends 100%-yield streak to 25 consecutive batches (0246–0270)

## Picks (8/8 ingested)

| # | alpha | yr/num | id | sections | parser path |
|---|-------|--------|----|----------|-------------|
| 0 | S | 1983/10 | act-zm-1983-010-supplementary-appropriation-1981-act-1983 | 26 | PDF |
| 1 | E | 1984/5  | act-zm-1984-005-excess-expenditure-appropriation-1981-act-1984 | 3 | PDF |
| 2 | S | 1984/6  | act-zm-1984-006-supplementary-appropriation-1982-act-1984 | 2 | PDF |
| 3 | E | 1985/8  | act-zm-1985-008-excess-expenditure-appropriation-1982-act-1985 | 2 | PDF |
| 4 | S | 1985/9  | act-zm-1985-009-supplementary-appropriation-1983-act-1985 | 2 | PDF |
| 5 | S | 1986/9  | act-zm-1986-009-supplementary-appropriation-1984-act-1986 | 3 | PDF |
| 6 | E | 1986/10 | act-zm-1986-010-excess-expenditure-appropriation-1983-act-1986 | 1 | PDF |
| 7 | S | 1987/12 | act-zm-1987-012-supplementary-appropriation-1985-act-1987 | 1 | PDF |

All 8 are short-form fiscal Appropriation / Excess Expenditure Acts. As anticipated by batch 0269's next-tick plan, every one fell back to PDF parsing because the HTML representation had fewer than 2 `akn-section` blocks. Section counts of 1–3 are typical for these short fiscal acts (the largest, 1983/10, returned 26 sections from a denser PDF layout).

## Discovery

- Robots.txt re-verified at tick start (sha256 prefix `fce67b697ee4ef44` — unchanged from batches 0193–0269; crawl-delay 5s honoured at 6s margin).
- 0 new alphabet listing fetches this tick (all 24 A–Z listings cached from earlier batches; X confirmed empty in 0269).
- Cross-alphabet residual sweep over cached A–Z listings filtered against `records/acts/**/*.json` (`act-zm-YYYY-NNN-…` and `act-YYYY-NN` formats). After excluding 3 known-deferred items (1956/4 S, 1996/17 C, 2006/9 C) **26 non-deferred residuals** were identified — exactly matching batch 0269's prediction. The 8 chronologically-first picks were taken; **18 residuals carry to next tick**.

## Picks not yet on disk — cross-checked

For each pick, `(yr, num)` was tested against the 885 `(yr,num)` keys derived from the on-disk acts corpus before fetching. All 8 confirmed not on disk — no silent overwrite (BRIEF non-negotiable #4).

## Integrity (`_work/integrity_0270.py`)

- **CHECK1a** batch unique ids: 8/8 unique
- **CHECK1b** corpus presence on disk: 8/8 written under `records/acts/{1983,1984,1985,1986,1987}/`
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
| record HTML fetches | 9 (8 unique + 1 retry on 1984/6 after host 45s timeout — same sha256 verified) |
| PDF fallback fetches | 8 |
| **Total this batch** | **18** |

Today running total: 345 (pre-tick) + 18 = **363 / 2000** fetches (18.15% of daily budget). Tokens within budget.

## Cumulative state after batch 0270

- acts: **1024** (+8 over 1016)
- SIs: 593 (unchanged from batch 0252)
- judgments: 25 (paused per robots Disallow on `/akn/zm/judgment/`)

## Reserved residuals carried to next tick

**18 cross-alphabet acts_in_force candidates** (chronological):
- E 1987/13, E 1988/14, S 1988/15, E 1988/30, E 1989/32, E 1990/38, E 1992/15
- P 1993/20, P 1993/24, E 1994/30, P 1994/45, E 1995/32 (note: title says 1992 but listed under 1995)
- plus the rest of the 26 less the 8 picked

Prior reserved residuals still pending:
- 1 S residual: 1956/4 Service of Process and Execution of Judgments — disambiguator-deferred
- 2 C deferred: Citizens Economic Empowerment 2006/9 + Constitution of Zambia 1996/17 (large; dedicated batches)
- 1 SI residual: 1990/39 ZNPF >4.5 MB — OCR backlog (15 items)

## Next-tick plan

1. Sweep next 8 cross-alphabet residuals (E/S 1987–1992 series will dominate, then P series 1993–1994).
2. Implement disambiguator-aware fetch handler for 1956/4.
3. OCR retry on 15-item SI backlog once tesseract is wired (deferred to host).
4. Re-verify robots.txt at start of next tick.

## Infrastructure follow-up (non-blocking)

- batch-0270 raw files (8 act HTML + 8 PDF + 1 robots; 0 alphabet listing) plus accumulated batches 0192–0269 raw files awaiting host-driven B2 sync (`rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4` — rclone unavailable in sandbox).
- Persistent virtiofs unlink-failure warnings on `.git/objects/tmp_obj_*` and `.git/objects/maintenance.lock` unchanged from batches 0192–0269 (rename succeeds, unlink fails — non-fatal).
- SQLite snapshot drift unchanged (`corpus.sqlite` still at 543 records vs 1590 JSON on disk after this batch) — periodic full rebuild expected from host.
- Pre-existing FTS5 vtable malformed image (`records_fts`) unchanged — non-blocking for record integrity, flagged for full-rebuild scope.

Parser version: `0.6.0-act-zambialii-2026-04-26` (unchanged across 0252–0270).
