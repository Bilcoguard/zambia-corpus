# Batch 0262 — Phase 4 bulk ingest

**Tick start:** 2026-04-26T10:30:00Z
**Sub-phase:** acts_in_force (priority_order item 1)
**Source:** zambialii.org (HTML akn-section parser; no PDF fallback required)
**Parser version:** 0.6.0-act-zambialii-2026-04-26
**Cap:** MAX_BATCH_SIZE = 8 — filled exactly (yield 8/8 = 100%)

## Discovery

- Re-verified `https://zambialii.org/robots.txt` — sha256 prefix
  `fce67b697ee4ef44` unchanged (consistent across batches 0193–0261).
  Crawl-delay 5 s honoured at 6 s margin. `/akn/zm/judgment/` and
  `/akn/zm/officialGazette/` Disallow continue to be respected
  (judgments paused since batch ~0140).
- Probed `/legislation?alphabet=S&nature=act` — single-page listing,
  44 unique act hrefs, 22 primary candidates after filter.
  Raw cached to `raw/zambialii/_alphabets/legislation-alphabet-S-20260426T103405Z.html`
  (sha256 prefix `575d3819054900e5`).
- Reserved residuals from prior ticks:
  - **P primary (3):** Prohibition of Chemical Weapons 2007/2,
    Protection of Names Uniforms and Badges 1957/38, Public Audit 1980/8.
  - **R primary (2):** Revenue Appeals Tribunal 1998/11,
    Rural Councils (Beer Surtax) Fund 1968/45.
- Filtered S against existing 824 distinct (yr,num) act IDs (id-match
  `act-zm-YYYY-NNN-`); dropped amendment / appropriation / supplementary /
  validation / transitional / repeal / continuation / excess-expenditure /
  dissolution / rectification tokens.
- Capped at 8: 5 residuals + first 3 S candidates fill the cap.
  19 S residuals deferred to next tick.

## Picks (8)

| # | Alpha | Year/No | Title                                                        | Sections | Source hash (sha256, first 16) |
|---|-------|---------|--------------------------------------------------------------|----------|--------------------------------|
| 1 | P     | 2007/2  | Prohibition (Chemical Weapons) Act, 2007                     | 72       | `22844fda760d71e0`             |
| 2 | P     | 1957/38 | Protection of Names, Uniforms and Badges Act, 1957           | 17       | `d14b378a603f4994`             |
| 3 | P     | 1980/8  | Public Audit Act, 1980                                       | 13       | `19b3cbd43c5ec074`             |
| 4 | R     | 1998/11 | Revenue Appeals Tribunal Act, 1998                           | 5        | `2eca0cda53d581a0`             |
| 5 | R     | 1968/45 | Rural Councils (Beer Surtax) Fund Act, 1968                  | 8        | `26f947e8e79c2f64`             |
| 6 | S     | 1960/58 | Scrap Metal Dealers Act, 1960                                | 15       | `941cb3ce0b4cf3e6`             |
| 7 | S     | 1988/33 | Self-Management Enterprises Act, 1988                        | 34       | `be4636e5697f01e9`             |
| 8 | S     | 1991/24 | Service Commissions Act, 1991                                | 22       | `06abe486fd2bd606`             |

Total sections parsed: 186 (min 5, max 72). All 8 records parsed cleanly
via akn-section HTML; no PDF fallback required.

## Integrity check (all PASS)

- **CHECK1a** batch unique IDs: 8/8 unique.
- **CHECK1b** corpus presence on disk: 8/8 records written under
  `records/acts/{year}/`.
- **CHECK2** amended_by refs: 0 (no unresolved).
- **CHECK3** repealed_by refs: 0 (no unresolved).
- **CHECK4** source_hash sha256: 8/8 verified against
  `raw/zambialii/act/(1957,1960,1968,1980,1988,1991,1998,2007)/`.
- **CHECK5** required 16 fields × 8 records: all present.
- **CHECK6** cited_authorities refs: 0 (no unresolved).

## Costs (this tick)

| Kind        | Count | Cumulative today |
|-------------|-------|------------------|
| robots      | 1     | (verification)   |
| discovery   | 1     | alphabet=S       |
| record HTML | 8     | one per pick     |
| record PDF  | 0     | no fallback      |

Pre-tick fetches today: 241/2000 (12.05 %). Post-tick: 241 + 1 + 1 + 8
= 251/2000 (12.55 %). Tokens within budget. All requests on
`zambialii.org` under robots-declared 5 s crawl-delay using a 6 s margin.

## Cumulative footprint

- Acts: 952 → 960 (+8). _Note: cumulative count tracked by JSON file
  count under `records/acts/`; was 1526 files post-batch-0261 across 824
  distinct (yr,num) keys + 106 legacy-ID files; now 1534 files / 832
  distinct keys after this batch._
- SIs: 593 (unchanged from batch 0252).
- Judgments: 25 (paused per robots Disallow on `/akn/zm/judgment/`).
- 100 %-yield streak extended: batches 0246–0262 = **17 consecutive
  batches at 100 % yield**.

## Reserved residuals carrying to next tick

- **S primary residuals (19):** Service of Process and Execution of
  Judgments 1956/4, Sheriffs 1960/28, Skills Development Levy 2016/46,
  Small Industries Development 1981/18, Social Workers' Association
  2022/4, Solid Waste Regulation and Management 2018/20, Specific Loan
  (Rhodesia Railways) 1950/47, Specified Offices (Terminal Gratuities)
  1988/38, Specified Offices (Terminal Gratuities) 1989/9, Sports
  Council of Zambia 1988/29, Standardisation of Soap 1957/24, Standards
  2017/4, State Audit Commission 2016/27, Statistics 2018/13, Statutory
  Functions 1970/43, Stock Exchange 1990/43, Superior Courts (Number of
  Judges) 2025/12, plus 2 carry-throughs from non-filtered second pass.
- **Prior reserved residuals still pending:** 2 alphabet=C deferred
  (Citizens Economic Empowerment 2006/9 + Constitution of Zambia
  1996/17 — large, dedicated batches); 1 SI residual (1990/39 ZNPF
  >4.5 MB OCR backlog at 15 items).

## Infrastructure follow-up (non-blocking)

- B2 raw sync deferred to host: `rclone sync raw/ b2raw:kwlp-corpus-raw/
  --fast-list --transfers 4` (rclone unavailable in sandbox).
- Persistent virtiofs unlink-failure warnings non-fatal (workaround
  stable across batches 0192–0262).
- SQLite snapshot drift: `corpus.sqlite` at 543 records vs 1534 JSON
  on disk after this batch — periodic full rebuild expected from host.
- Pre-existing FTS5 vtable malformed image (`records_fts`) unchanged;
  non-blocking for record integrity.

## Next-tick plan

1. Sweep first 8 S residuals (Service of Process / Sheriffs / Skills
   Development Levy / Small Industries Development / Social Workers'
   Association / Solid Waste Regulation / Specific Loan / Specified
   Offices Terminal Gratuities 1988).
2. Continue alphabetic walk through T-U-V if S residuals exhaust before
   cap.
3. Re-verify robots.txt at start of next tick.
