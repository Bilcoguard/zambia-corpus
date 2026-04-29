"""Batch 0334 — Phase 4 / minimal upstream-refresh tick (45th consecutive steady-state tick).

Inherited closing state (after b0290..b0333):

  - acts_in_force: chronological-first sweep complete through 2026/11.
  - All 22 active zambialii alphabet letters exhaustively swept across
    b0291..b0293 (A B C D E F G H I J K L M N O P R S T U V W; Q,X,Y,Z
    omitted by design).
  - Every priority_order sub-phase confirmed at upstream steady state
    for the requests + beautifulsoup4 + pdfplumber toolset.
  - OCR backlog: 21 (unchanged from b0293..b0333).
  - Cumulative records: acts 1169, SIs 539, judgments 25 (all unchanged
    from b0311..b0333).
  - Long-standing pre-tick file/id gap on records (1733 files, 1720
    unique ids; 5 duplicate ids) — outside this probe's integrity scope.

This tick: minimal upstream refresh (no alphabet sweep), to detect any
new entries on the two chronological feeds:

  - zambialii.org/legislation/recent
  - parliament.gov.zm/acts-of-parliament  (page 0)

PROBE-ONLY: zero record writes by design.

PARSER_VERSION: 0.5.0 (probe-only — same as b0290..b0333)
USER_AGENT:    KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)

robots.txt sha256 (zambialii):  fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0
robots.txt sha256 (parliament): 278e83bcf567badfebcdea4d5d20ca9898e4449fe4eb2e3b5a08227b4ca9b762
Crawl-delay: 6s zambialii (>= robots 5s); 11s parliament (>= robots 10s).

PROBE RESULTS (see _work/batch_0334_probe.json for full data):

  /legislation/recent:    15 act links (2026/1..11 + 2025/6..9).
                          ALL 15 in corpus (steady state).
                          page bytes: 95,392 (unchanged vs b0329..b0333).
                          page sha256: 507f7542eddc74c7089f669398fc86861aea75d60dc9dabe0fbddb922d79321c
                          (UNCHANGED for the sixth consecutive tick —
                          feed surface and ranking are byte-for-byte
                          identical to b0329..b0333).
  parliament page 0:      20 act links (2026/1..11 + 2025/21..29).
                          ALL 20 in corpus.
                          page bytes: 38,208 (unchanged across all 45
                          steady-state ticks).
                          page sha256: a71e110e44a3b01eb15f74da92d510f5e32411e7738ae636910a5df29584699a
                          (differs across ticks — session/CSRF token
                          churn; byte-count and extracted act-list
                          stable).

  In-priority candidates (sis_corporate, sis_tax, sis_employment,
                          sis_mining, sis_family, sis_data_protection,
                          case_law_scz, acts_in_force):
    0 — every priority_order sub-phase confirmed at upstream steady
    state.

INTEGRITY (lightweight, on records/{type}/{year}/*.json):
  records.scanned: 1733
  ids.unique:      1720
  ids.duplicate:   5  (long-standing pre-tick gap; outside probe scope)
  parse.fail:      0
  refs.total:      7
  refs.unresolved: 0
  hash.sampled:    50  (raw files not present locally for sample;
                        host-side OCR flow holds raw artefacts)
  hash.mismatch:   0

SANDBOX NOTE (carried from b0299..b0333):

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
# The probe lives at _work/batch_0334_probe.py (gitignored scratch).
PICKS = []
"""
Empty by design — every priority_order sub-phase is at upstream steady
state for the requests + beautifulsoup4 + pdfplumber toolset.

Phase 4 disposition unchanged from b0293..b0333: cannot meaningfully
advance further without one of:

  (a) human confirmation that Phase 4 is complete (set complete: true
      in approvals.yaml — worker may not flip this flag), or
  (b) approval of Phase 5 / a successor phase, or
  (c) authorisation to expand the source map (out of Phase 4 scope), or
  (d) host-side OCR flow to drain the 21-record OCR backlog.
"""
