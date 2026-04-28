"""Batch 0328 — Phase 4 / minimal upstream-refresh tick (39th consecutive steady-state tick).

Inherited closing state (after b0290..b0327):

  - acts_in_force: chronological-first sweep complete through 2026/11.
  - All 22 active zambialii alphabet letters exhaustively swept across
    b0291..b0293 (A B C D E F G H I J K L M N O P R S T U V W; Q,X,Y,Z
    omitted by design).
  - Every priority_order sub-phase confirmed at upstream steady state
    for the requests + beautifulsoup4 + pdfplumber toolset.
  - OCR backlog: 21 (unchanged from b0293..b0327).
  - Cumulative records: acts 1169, SIs 539, judgments 25 (all unchanged
    from b0311..b0327).

This tick: minimal upstream refresh (no alphabet sweep), to detect any
new entries on the two chronological feeds:

  - zambialii.org/legislation/recent
  - parliament.gov.zm/acts-of-parliament  (page 0)

PROBE-ONLY: zero record writes by design.

PARSER_VERSION: 0.5.0 (probe-only — same as b0290..b0327)
USER_AGENT:    KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)

robots.txt sha256 (zambialii):  fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0
robots.txt sha256 (parliament): 278e83bcf567badfebcdea4d5d20ca9898e4449fe4eb2e3b5a08227b4ca9b762
Crawl-delay: 6s zambialii (>= robots 5s); 11s parliament (>= robots 10s).

PROBE RESULTS (see _work/batch_0328_probe.json for full data):

  /legislation/recent:    16 act links (2026/1..8 + 2026/10 + 2025/5..9
                          + 2025/28 + 2025/29).
                          ALL 16 in corpus (steady state).
                          page bytes: 95,192 (unchanged vs b0327).
                          page sha256: 1c1bb006edda00f240e42e0fc8c0ca1804301fe4f90918c949c153ebda191665
                          (unchanged vs b0327 — feed surface has not
                          re-ranked again since b0327).
  parliament page 0:      20 act links (2026/1..11 + 2025/21..29).
                          ALL 20 in corpus.
                          page bytes: 38,208 (unchanged).
                          page sha256: 256eefeafd8a58a7d6f19b11928bbe524fd41ede91e09fa3bade1f1c3af430fd
                          (differs across ticks — session/CSRF token
                          churn; byte-count and extracted act-list
                          stable).

  In-priority candidates (sis_corporate, sis_tax, sis_employment,
                          sis_mining, sis_family, sis_data_protection,
                          case_law_scz, acts_in_force):
    0 — every priority_order sub-phase confirmed at upstream steady
    state.

SANDBOX NOTE (carried from b0299..b0327):

  - parliament.gov.zm does not send the RapidSSL TLS RSA CA G1
    intermediate in its TLS chain. Worked around by appending
    scripts/certs/rapidssl_tls_rsa_ca_g1.pem to certifi.where() and
    pointing requests.verify at the merged bundle. No insecure fallback
    used.
  - .git/index.lock and .git/objects/maintenance.lock cleared via
    _stale_locks/ rotation pre-commit (sandbox cannot delete with rm;
    mv works). The pre-tick `find .git -name "*.lock" -delete` returns
    benign "Operation not permitted" on .git/objects/maintenance.lock
    (sandbox unlink limit), which does not block git operations.
"""

# This script is documentation-only; no executable ingest unit.
# The probe lives at _work/batch_0328_probe.py (gitignored scratch).
PICKS = []
"""
Empty by design — every priority_order sub-phase is at upstream steady
state for the requests + beautifulsoup4 + pdfplumber toolset.

Phase 4 disposition unchanged from b0293..b0327: cannot meaningfully
advance further without one of:

  (a) human confirmation that Phase 4 is complete (set complete: true
      in approvals.yaml — worker may not flip this flag), or
  (b) approval of Phase 5 / a successor phase, or
  (c) authorisation to expand the source map (out of Phase 4 scope), or
  (d) host-side OCR flow to drain the 21-record OCR backlog.
"""
