# Batch 0266 — Phase 4 bulk ingest

**Date (UTC):** 2026-04-26
**Sub-phase:** acts_in_force (T residuals + U/V/W/Z probe sweep)
**Records added:** 8 / 8 (yield 100%)
**Cumulative:** acts 992 (+8 over 984), SIs 593 (unchanged), judgments 25 (unchanged)

## Picks

| # | Year/No. | Title | Alpha | Sections | source_hash (prefix) |
|---|----------|-------|-------|----------|----------------------|
| 0 | 1952/5   | Victoria Memorial Institute (Repeal) Act, 1952 | V | 3  | 8b95a1dd1d0cb54c |
| 1 | 1950/45  | Zambia Police Reserve Act, 1950                | Z | 14 | 606a4d0268effd68 |
| 2 | 1967/28  | War Graves and Memorials Act, 1967             | W | 8  | c0fc9c7cd8ac3067 |
| 3 | 1972/26  | Termination of Pregnancy Act, 1972             | T | 6  | e98fec1f0250afee |
| 4 | 1972/37  | Technical Education and Vocational Training Act, 1972 | T | 31 | 67dc2e1db485f4d3 |
| 5 | 1973/49  | Trades Charges Act, 1973                       | T | 8  | 3d96b981bdad2d2d |
| 6 | 1987/20  | University of Zambia Act, 1987                 | U | 43 | 27d4fbbcb5e17837 |
| 7 | 1992/26  | University Act, 1992                           | U | 53 | f2731ed85d4c35fa |

7 of 8 parsed via akn-section HTML; 1 PDF fallback (1987/20 University of Zambia Act, 1987 — HTML returned <2 akn-sections, source.pdf fetched and parsed; PDF size 3.886 MB, under 4.5 MB cap).

## Discovery

Re-verified robots.txt (sha256 prefix `fce67b697ee4ef44`, unchanged from batches 0193-0265). Probed 5 alphabet listings:

- T residuals carried from batch 0265: 3 (all confirmed not on disk).
- U: 4 candidates / 2 already on disk / 2 new — both picked.
- V: 3 candidates / 2 already on disk / 1 new — picked.
- W: 6 candidates / 5 already on disk / 1 new — picked.
- Y: 0 candidates (empty listing).
- Z: 45 candidates / 28 already on disk / 17 new — 1 picked (1950/45 chronologically first new); 16 carry as residuals.

## Integrity

- CHECK1a unique IDs in batch: 8/8
- CHECK1b corpus presence on disk: 8/8
- CHECK2 amended_by refs: 0
- CHECK3 repealed_by refs: 0
- CHECK4 source_hash sha256 verified against raw/zambialii/act/(1950,1952,1967,1972,1973,1987,1992)/: 8/8
- CHECK5 required 16 fields × 8 records: 0 misses
- CHECK6 cited_authorities refs: 0

## Costs (2026-04-26)

Pre-tick: 291 fetches. This tick: 1 robots + 5 alphabet listings + 8 record HTML + 1 PDF fallback (1987/20) = 15 fetches. Post-tick: 306 / 2000 (15.3%). Tokens within budget. All on zambialii.org under robots-declared 5s crawl-delay (using 6s margin).

## Reserved residuals carried to next tick

- T (none — all swept this tick).
- U (none — both candidates ingested).
- V (none — only candidate ingested).
- W (none — only candidate ingested).
- Z: 16 residuals (chronologically: 1964/39 Zambia Youth Service, 1966/1 Zambia National Provident Fund, 1966/9 Zambia Red Cross Society, 1966/32 Zambia National Commission for UNESCO, 1966/50 Zambian Mines Local Pension Fund (Dissolution), 1967/18 Zambia Tanzania Pipeline, 1973/43 Zambia Security Intelligence Service, 1982/30 Zambia National Tender Board, 1989/1 (Zambia title), 1993/25 Zambia Iron and Steel Authority (Dissolution), 1995/24 Zambia Institute of Diplomacy and International Studies, 1995/36 Zambia Institute of Architects, 1996/10 Zambia Institute of Advanced Legal Education, 1996/11 Zambia Law Development Commission, 1996/19 Zambia Institute of Mass Communications (Repeal), 1997/11 Zambia Institute of Human Resources Management).

Prior reserved residuals still pending: 1 S residual (1956/4 Service of Process and Execution of Judgments — disambiguator-deferred); 2 alphabet=C deferred (Citizens Economic Empowerment 2006/9 + Constitution of Zambia 1996/17 — large, dedicated batches); 1 SI residual (1990/39 ZNPF >4.5MB OCR backlog at 15 items).

## Next-tick plan

(a) Sweep the 16 Z residuals across 2 batches at MAX_BATCH_SIZE=8 (or fewer per tick if section counts grow large — 1992/26 University Act already produced 53 sections this tick).
(b) Implement disambiguator-aware fetch handler for 1956/4.
(c) Schedule dedicated batches for 1996/17 Constitution and 2006/9 Citizens Economic Empowerment.
(d) Probe alphabet=X (skipped this tick — typically empty for ZM acts) at next tick to close the alphabetic walk after Z.
(e) Re-verify robots.txt at start of next tick.

## Infrastructure follow-ups (non-blocking)

- B2 sync deferred to host (rclone unavailable in sandbox): batch 0266 raw files (8 act HTML + 5 alphabet listings + 1 robots) plus accumulated batches 0192-0265 raw files awaiting host-driven `rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4`.
- Persistent virtiofs unlink-failure warnings on .git/objects/* during git operations (rename succeeds, unlink fails) — non-fatal, unchanged from batches 0192-0265.
- corpus.sqlite NOT touched this batch (snapshot drift preserved per established workflow at 543 records vs 1566 JSON on disk after this batch).
- Pre-existing FTS5 vtable malformed image (records_fts) unchanged — flagged for full-rebuild scope.

100%-yield streak now batches 0246-0266 (21 consecutive). MAX_BATCH_SIZE=8 cap filled exactly.
