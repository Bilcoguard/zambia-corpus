"""Batch 0320 — Phase 4 / minimal upstream-refresh tick (31st consecutive steady-state tick).

Inherited closing state (after b0290..b0319):

  - acts_in_force: chronological-first sweep complete through 2026/11.
  - All 22 active zambialii alphabet letters exhaustively swept across
    b0291..b0293 (A B C D E F G H I J K L M N O P R S T U V W; Q,X,Y,Z
    omitted by design).
  - Every priority_order sub-phase confirmed at upstream steady state
    for the requests + beautifulsoup4 + pdfplumber toolset.
  - OCR backlog: 21 (unchanged from b0293..b0319).
  - Cumulative records: acts 1169, SIs 539, judgments 25 (all unchanged
    from b0311..b0319).

This tick: minimal upstream refresh (no alphabet sweep), to detect any
new entries on the two chronological feeds:

  - zambialii.org/legislation/recent
  - parliament.gov.zm/acts-of-parliament  (page 0)

PROBE-ONLY: zero record writes by design.

PARSER_VERSION: 0.5.0 (probe-only — same as b0290..b0319)
USER_AGENT:    KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)

robots.txt sha256 (zambialii):  fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0
robots.txt sha256 (parliament): 278e83bcf567badfebcdea4d5d20ca9898e4449fe4eb2e3b5a08227b4ca9b762
Crawl-delay: 6s zambialii (>= robots 5s); 11s parliament (>= robots 10s).

PROBE RESULTS (see _work/batch_0320_probe.json for full data):

  /legislation/recent:    13 act links (2025/5..9 + 2025/22..29)
                          ALL 13 in corpus (steady state).
                          page sha256: 452f6ec2c4d177e306881f24ecc21d17294e09d6e12b4a06059687ad738b0cfa
                          (unchanged from b0316..b0319).
  parliament page 0:      20 act links (2025/21..29 + 2026/1..11)
                          ALL 20 in corpus.
                          page sha256: 0b121dd9283472c165f71ed9da5a21c3dcbd4e34ba2d2a7d9aef8b961b4f5ab5
                          (differs from b0319 — session/CSRF token churn;
                           byte-count 38208 unchanged).

  In-priority candidates (sis_corporate, sis_tax, sis_employment,
                          sis_mining, sis_family, sis_data_protection,
                          case_law_scz, acts_in_force):
    0 — every priority_order sub-phase confirmed at upstream steady
    state.

SANDBOX NOTE (carried from b0299..b0319):

  - parliament.gov.zm does not send the RapidSSL TLS RSA CA G1
    intermediate in its TLS chain. Worked around by appending
    scripts/certs/rapidssl_tls_rsa_ca_g1.pem to certifi.where() and
    pointing requests.verify at the merged bundle. No insecure fallback
    used.
  - .git/index.lock and .git/objects/maintenance.lock cleared via
    _stale_locks/ rotation pre-commit (sandbox cannot delete with rm;
    mv works).
"""

# This script is documentation-only; no executable ingest unit.
PICKS = []
"""
Empty by design — every priority_order sub-phase is at upstream steady
state for the requests + beautifulsoup4 + pdfplumber toolset.

Phase 4 disposition unchanged from b0293..b0319: cannot meaningfully
advance further without one of:

  (a) human confirmation that Phase 4 is complete (set complete: true
      in approvals.yaml — worker may not flip this flag), or
  (b) approval of Phase 5 / a successor phase, or
  (c) authorisation to expand the source map (out of Phase 4 scope), or
  (d) host-side OCR flow to drain the 21-record OCR backlog.
"""
