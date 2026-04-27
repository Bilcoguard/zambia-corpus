"""Batch 0296 — Phase 4 / minimal upstream-refresh tick.

Inherited closing state (after b0290..b0295):

  - acts_in_force: chronological-first sweep complete through 2026/11.
  - All 22 active zambialii alphabet letters exhaustively swept across
    b0291..b0293 (A B C D E F G H I J K L M N O P R S T U V W; Q,X,Y,Z
    omitted by design).
  - Every priority_order sub-phase confirmed at upstream steady state for
    the requests + beautifulsoup4 + pdfplumber toolset.
  - OCR backlog: 21 (unchanged from b0293..b0295).

This tick: minimal upstream refresh (no alphabet sweep), to detect any
new entries on the two chronological feeds:

  - zambialii.org/legislation/recent
  - parliament.gov.zm/acts-of-parliament  (page 0)

PROBE-ONLY: zero record writes by design.

PARSER_VERSION: 0.5.0 (probe-only — same as b0290..b0295)
USER_AGENT:    KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)

robots.txt sha256 (zambialii):  fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0
robots.txt sha256 (parliament): 278e83bcf567badfebcdea4d5d20ca9898e4449fe4eb2e3b5a08227b4ca9b762
Crawl-delay: 6s zambialii (>= robots 5s); 11s parliament (>= robots 10s).

PROBE RESULTS (see _work/batch_0296_probe.json for full data):

  /legislation/recent:    13 act links (2025/5..9 + 2025/22..29)
                          ALL 13 in corpus (steady state).
  parliament page 0:      20 act links (2026/1..11 + 2025/21..29)
                          ALL 20 in corpus (verified via "Act No. N of
                          YYYY" text pattern).

  In-priority candidates (sis_corporate, sis_tax, sis_employment,
                          sis_mining, sis_family, sis_data_protection,
                          case_law_scz, acts_in_force):
    0 — every priority_order sub-phase confirmed at upstream steady
    state.
"""

# This script is documentation-only; no executable ingest unit.
PICKS = []
"""
Empty by design — every priority_order sub-phase is at upstream steady
state for the requests + beautifulsoup4 + pdfplumber toolset.

Phase 4 disposition unchanged from b0293..b0295: cannot meaningfully
advance further without one of:
  (a) an OCR pipeline (Tesseract or equivalent) to unblock the OCR
      backlog (currently 21 items),
  (b) an oversize-PDF chunked-extract pipeline (6 acts deferred),
  (c) a multi-Act gazette splitter (2024/9 deferred),
  (d) a scope definition for pre-2017 alphabet sweeps,
  (e) priority_order expansion to admit the off-priority reserve
      sub-phases (sis_road_traffic, sis_planning, sis_education,
      sis_diplomacy, sis_defence, sis_higher_education,
      sis_disaster_management, sis_climate, sis_emoluments).
"""
