"""Batch 0293 — Phase 4 / final-letter alphabet exhaust + upstream-acts refresh.

Inherited closing state (from b0290 + b0291 + b0292):

  - acts_in_force: chronological-first sweep complete through 2026/11.
  - sis_corporate-modern:    A,B,C,I,M,P,S,T,V probed (b0291) — empty.
  - sis_tax-modern:          3 candidates OCR-deferred (b0291).
  - sis_employment-modern:   E,F,J,L,N,W probed (b0292) — 1 OCR-deferred.
  - sis_mining-modern:       M alphabet empty (b0291).
  - sis_family-modern:       empty across F,J,L,M,W.
  - case_law_scz, sis_data_protection: at upstream steady state.

This tick closes the alphabet exhaust by probing the 7 remaining
uncovered high-yield letters (D, G, H, K, O, R, U) plus refreshing two
upstream Act listings (zambialii /legislation/recent and parliament
/acts-of-parliament page 0). 4 letters are intentionally omitted (Q, X,
Y, Z — empty/near-empty on this jurisdiction). After this tick, every
Latin alphabet letter that produces SIs has been swept.

PROBE-ONLY: zero record writes by design.

Coverage of zambialii alphabets after b0293:
  b0291 swept: A B C I M P S T V                            (9)
  b0292 swept: E F J L N W                                  (6)
  b0293 swept: D G H K O R U                                (7) <-- this tick
  Total      : 22 letters / 26 (Q, X, Y, Z omitted by design)

PARSER_VERSION: 0.5.0 (probe-only — same as b0291/0292)
USER_AGENT:    KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)

robots.txt sha256 (zambialii):  fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0
robots.txt sha256 (parliament): 278e83bcf567badfebcdea4d5d20ca9898e4449fe4eb2e3b5a08227b4ca9b762
Crawl-delay: 6s on zambialii (>= robots 5s); 11s on parliament (>= robots 10s).

PROBE RESULTS (see _work/batch_0293_probe.json for full data):

  Alphabet  Total  Modern  Novel(raw)  Novel(true*)
  D            -       -         -            0
  G            -       -         -            0
  H            -       -         -            0
  K            -       -         -            0
  O            -       -         -            0
  R            -       -         -            0
  U            -       -         -            0
  *true novel = excluding records already on disk under non-standard
   filenames (e.g. slug-only filenames for pre-2017 SIs).

  /legislation/recent: 13 act links — ALL 13 in corpus.
  parliament page0:    20 act links (2026/1..11, 2025/21..29) — ALL 20
                       in corpus. (parser verified via
                       'Act No. N of YYYY' text-pattern, since href
                       structure does not embed the year/num key.)

  In-priority candidates (sis_corporate, sis_tax, sis_employment,
                          sis_mining, sis_family, sis_data_protection):
    0 — every priority_order sub-phase confirmed at upstream steady
    state for letters D/G/H/K/O/R/U.

  Off-priority reserved discoveries:
    1 unique novel modern SI (sis_road_traffic):
      2020/7 Road Traffic (Speed Limits) Regulations, 2019
      ALREADY in OCR backlog from b0276 (pdf_parse_empty / scanned image).

  (37 novel-looking entries from the raw probe were re-classified as
  already-in-corpus under non-standard filenames, e.g. Urban and
  Regional Planning regulations, Diplomatic Immunities orders, etc.
  Verified by reading citation/id fields from each on-disk JSON.)
"""

# This script is documentation-only; no executable ingest unit.
PICKS = []
"""
Empty by design — every priority_order sub-phase is at upstream steady
state for the requests + beautifulsoup4 + pdfplumber toolset.

Phase 4 disposition unchanged from b0292: cannot meaningfully advance
further without one of:
  (a) an OCR pipeline (Tesseract or equivalent) to unblock the OCR
      backlog (currently 21+ items),
  (b) an oversize-PDF chunked-extract pipeline (6 acts deferred),
  (c) a multi-Act gazette splitter (2024/9 deferred),
  (d) a scope definition for pre-2017 alphabet sweeps,
  (e) priority_order expansion to admit the off-priority reserve
      sub-phases (sis_road_traffic, sis_planning, sis_education,
      sis_diplomacy, sis_defence, sis_higher_education,
      sis_disaster_management, sis_climate, sis_emoluments).
"""
