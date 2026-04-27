#!/usr/bin/env python3
"""Batch 0290 - Phase 4 bulk: pool-refresh probe.

Inherited zambialii chronological-first acts_in_force pool was exhausted
at end of batch 0289 (full sweep through 2025/28). Per b0289 closing note,
this tick performs a pool-refresh probe across both upstream act sources
to determine whether any newly published 2025/2026 Acts exist that are
not yet in the corpus.

Scope: probe-only (no record writes, no record fetches). Ingest pool is
empty after probe.

PROBE 1 - zambialii.org
  - GET /robots.txt          (re-verify; sha256 unchanged)
  - GET /legislation/recent  (most recently published listing)
  Result: 13 acts on listing -> 2025/5..9 + 2025/22..29.
          All 13 already in corpus (verified vs records/acts/**/*.json).

PROBE 2 - www.parliament.gov.zm
  - GET /robots.txt
  - GET /acts-of-parliament         (page 0: 2026/1..11 + 2025/21..29)
  - GET /acts-of-parliament?page=1  (page 1: 2025/1..20)
  - GET /acts-of-parliament?page=2  (page 2: 2024/12..30)
  Result: 59 distinct (yr, num) tuples enumerated across the three pages
          (2026/1..11 + 2025/1..29 + 2024/12..30 = 11 + 29 + 19 = 59).
          All 59 already in corpus (verified vs records/acts/**/*.json).

CONCLUSION
  acts_in_force chronological-first sweep is COMPLETE through 2026/11
  (the most recent Act published by Parliament of Zambia per the upstream
  listing page first row, dated mid-Q1 2026). The pool refresh produced
  ZERO new picks. Batch 0290 ingest is therefore empty by design.

  This is the diagnostic the b0289 closing note flagged as needed before
  the next round.

NEXT MOVE (for human review; worker does NOT flip approvals.yaml)
  The acts_in_force sub-phase has reached steady-state for current
  publication. Three retry queues remain:

    - multi-act-gazette retry queue: 1 item (2024/9)
    - oversize-pdf queue: 6 items (2002/6, 2005/21, 2008/5, 2009/10,
      2009/30, 2012/16)
    - OCR section-tolerant retry queue: 6 items (1988/32, 1994/40,
      1995/33, 2004/6, 2008/9, 2009/7)
    - OCR backlog: 18 items

  These each need a targeted approach (PDF chunking for oversize, true
  OCR pipeline for the OCR backlog, multi-Act gazette splitter for the
  multi-act-gazette retry queue).

  Per approvals.yaml priority_order, sub-phase that follows acts_in_force
  is sis_corporate, which has 6 records on disk vs an unknown universe.
  Both directions are out of scope for batch 0290 since no specific work
  unit was approved beyond "phase_4_bulk: complete: false". Human review
  is needed to either:
    (a) target a specific retry queue,
    (b) define the sis_corporate scope,
    (c) flip phase_4_bulk -> complete: true if the residual queues are
        deemed acceptable gaps (and add them to gaps.md).

PARSER_VERSION reused from b0289: 0.6.0-act-zambialii-2026-04-26
USER_AGENT: KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)
robots.txt sha256 (zambialii):     fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0
robots.txt sha256 (parliament):    278e83bcf567badfebcdea4d5d20ca9898e4449fe4eb2e3b5a08227b4ca9b762

Crawl-delay: 6s on zambialii (>= robots 5s); 11s on parliament (>= robots 10s).
"""

# This script is a record of the batch logic, not an executable ingest
# routine: there is nothing to ingest (pool empty). Leaving as
# documentation per project convention (every batch leaves a script).

PICKS = []  # zero
PROBE_RESULTS = {
    "zambialii_legislation_recent": {
        "found_acts": [
            ("2025", 5), ("2025", 6), ("2025", 7), ("2025", 8), ("2025", 9),
            ("2025", 22), ("2025", 23), ("2025", 24), ("2025", 25),
            ("2025", 26), ("2025", 27), ("2025", 28), ("2025", 29),
        ],
        "missing_from_corpus": [],
    },
    "parliament_acts_of_parliament_pages_0_1_2": {
        "found_acts": (
            [("2026", n) for n in range(1, 12)]
            + [("2025", n) for n in range(1, 30)]
            + [("2024", n) for n in range(12, 31)]
        ),
        "missing_from_corpus": [],
    },
}

if __name__ == "__main__":
    print("batch_0290: pool-refresh probe; 0 picks; see reports/batch-0290.md")
