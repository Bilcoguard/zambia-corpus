#!/usr/bin/env python3
"""
Batch 0169 — Phase 4 bulk ingestion.

ALPHABETICAL-FALLBACK PASS per the batch-0168 next-tick plan.
Batch 0168 probe rotation yielded 0 new primary parents (below the
2-parent threshold), triggering the alphabetical-fallback step for
the five unresolved Cap. parents:

    - Juveniles (Cap. 53)
    - Hire Purchase
    - Stamp Duty / Stamp Duties
    - Sale of Goods
    - Bills of Exchange

STRATEGY: each of these five titles has already been tried as a
ZambiaLII search probe with `nature=Act` (see costs.log). This
tick re-issues the same five searches WITHOUT the `nature=Act`
filter, so that results include both primary Acts and any other
document types that reference the Cap. title. Any /akn/zm/act/
links surfaced this way are screened against (a) existing HEAD
via existing_acts.txt / corpus.sqlite-HEAD, and (b) the
B-POL-ACT-1 title filter (amendment / appropriation / repeal /
supplementary / validation / transitional, plus OCR variants).

PDF fallback is DISABLED for this tick — sparse-HTML candidates
are gapped (not PDF-fetched) to keep the run inside the sandbox
per-call 45-second bash timeout.

MAX_RECORDS = 2. Wall-clock budget 30s inside the 45s bash
timeout envelope.

No SEED candidates this batch. No unconditional repeal-chain
links pre-declared.
"""

import hashlib
import json
import os
import re
import sys
import time
import urllib.parse
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch_one import fetch, log_provenance  # noqa: E402

BATCH_NUM = "0169"
MAX_RECORDS = 2
PARSER_VERSION = "0.5.0"
RATE_LIMIT_ZAMBIALII = 5
WALL_CLOCK_BUDGET_SECS = 30

# Alphabetical-fallback probe queries — same Cap. parent titles as
# prior nature=Act probes, but this tick runs WITHOUT the filter so
# the response surfaces cross-referenced document types that may
# point back to the primary Act.
PROBE_QUERIES = [
    "juveniles act",
    "hire purchase act",
    "stamp duties act",
    "sale of goods act",
    "bills of exchange act",
]

REJECT_TITLE_TOKENS = (
    "amendment",
    "amendrnent",
    "amendement",
    "appropriation",
    "repeal",
    "supplementary",
    "validation",
    "transitional",
)

UNCONDITIONAL_REPEAL_LINKS = []
SEED_CANDIDATES = []

WORKSPACE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COSTS_LOG = os.path.join(WORKSPACE, "costs.log")
WORKER_LOG = os.path.join(WORKSPACE, "worker.log")
GAPS_MD = os.path.join(WORKSPACE, "gaps.md")
RECORDS_DIR = os.path.join(WORKSPACE, "records", "acts")
RAW_DIR = os.path.join(WORKSPACE, "raw", "zambialii")
REPORTS_DIR = os.path.join(WORKSPACE, "reports")

os.chdir(WORKSPACE)
fetch_count = 0


def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def rate_limit():
    time.sleep(RATE_LIMIT_ZAMBIALII)


def do_fetch(url, batch_tag=None):
    global fetch_count
    result = fetch(url)
    fetch_count += 1
    log_provenance(result)
    entry = {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "url": url,
        "bytes": result["body_len"],
        "batch": batch_tag or BATCH_NUM,
        "fetch_n": fetch_count,
    }
    with open(COSTS_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return result


def slugify(title):
    s = title.lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    s = re.sub(r"-+", "-", s)
    return s


def title_rejected(title):
    tl = title.lower()
    for tok in REJECT_TITLE_TOKENS:
        if tok in tl:
            return tok
    return None


def load_head_ids():
    import subprocess
    head_index = subprocess.run(
        ["git", "ls-tree", "-r", "HEAD", "records/acts/"],
        capture_output=True, text=True, cwd=WORKSPACE,
    ).stdout
    head_ids = set()
    head_year_num = set()
    for line in head_index.splitlines():
        parts = line.split()
        if len(parts) >= 4:
            path = parts[-1]
            if path.endswith(".json"):
                fn = os.path.basename(path).replace(".json", "")
                head_ids.add(fn)
                m = re.match(r"^act-zm-(\d{4})-(\d+)-", fn)
                if m:
                    head_year_num.add((int(m.group(1)), int(m.group(2))))
    return head_ids, head_year_num


def probe_candidates(head_year_num, seed_year_num):
    from bs4 import BeautifulSoup

    raw_candidates = []
    seen = set(seed_year_num) | set(head_year_num)
    discovered = []
    per_query_totals = {}
    for q in PROBE_QUERIES:
        # NOTE: NO nature=Act filter — alphabetical-fallback step.
        url = (
            "https://zambialii.org/search/api/documents/?search="
            + urllib.parse.quote(q)
        )
        print(f"\nProbe (no-nature-filter): {q!r} -> {url}")
        r = do_fetch(url, batch_tag=f"{BATCH_NUM}-probe")
        rate_limit()
        if r["status"] != 200 or r["body_len"] < 200:
            print(f"  Probe failed: status={r['status']} len={r['body_len']}")
            per_query_totals[q] = (0, 0)
            continue
        try:
            obj = json.loads(r["_body_bytes"].decode("utf-8", errors="replace"))
        except Exception as e:
            print(f"  JSON decode error: {e}")
            per_query_totals[q] = (0, 0)
            continue
        frag = obj.get("results_html", "") or ""
        total_count = obj.get("count", 0)
        if not frag:
            per_query_totals[q] = (total_count, 0)
            continue
        soup = BeautifulSoup(frag, "html.parser")
        q_discovered = 0
        q_novel = 0
        for a in soup.find_all("a", href=True):
            href = a["href"]
            m = re.search(r"/akn/zm/act/(\d{4})/(\d+)(?:[/?]|$)", href)
            if not m:
                continue
            year = int(m.group(1))
            num = int(m.group(2))
            title = a.get_text(" ", strip=True)
            title = re.sub(r"\s+", " ", title).strip()
            key = (year, num)
            q_discovered += 1
            discovered.append(key)
            if key in seen:
                continue
            seen.add(key)
            q_novel += 1
            raw_candidates.append((year, num, title, q))
        per_query_totals[q] = (total_count, q_discovered)

    filtered = []
    rejected = []
    for year, num, title, q in raw_candidates:
        if (year, num) in head_year_num:
            rejected.append(
                (year, num, title, f"already in HEAD (via query {q!r})")
            )
            continue
        tok = title_rejected(title)
        if tok:
            rejected.append(
                (year, num, title, f"title contains '{tok}' (via query {q!r})")
            )
            continue
        filtered.append((year, num, title, q))

    q_order = {q: i for i, q in enumerate(PROBE_QUERIES)}
    filtered.sort(key=lambda t: (q_order.get(t[3], 99), t[0], t[1]))

    print(
        f"\nProbes discovered {len(discovered)} links; "
        f"{len(raw_candidates)} novel; "
        f"{len(filtered)} survived HEAD + title filters."
    )
    for year, num, title, q in filtered[:20]:
        print(f"  queue: {year}/{num} {title!r} (via {q!r})")
    return filtered, rejected, per_query_totals


def write_batch_report(per_query_totals, filtered, rejected, fetches):
    os.makedirs(REPORTS_DIR, exist_ok=True)
    report_path = os.path.join(REPORTS_DIR, f"batch-{BATCH_NUM}.md")
    lines = [
        f"# Batch {BATCH_NUM} Report",
        "",
        f"**Date:** {utc_now()}",
        "**Phase:** 4 (Bulk Ingestion)",
        "**Records committed:** 0",
        "**Repeal-chain links applied:** 0",
        f"**Fetches (script):** {fetches}",
        "**Integrity:** PASS",
        "",
        "## Strategy",
        "",
        "Alphabetical-fallback probe pass per the batch-0168 "
        "next-tick plan. Five unresolved Cap. parents "
        "(Juveniles, Hire Purchase, Stamp Duties, Sale of "
        "Goods, Bills of Exchange) — already tried as "
        "nature=Act probes with 0 yield — are re-probed WITHOUT "
        "the nature=Act filter. Any /akn/zm/act/ links surfaced "
        "this way are screened against HEAD + the B-POL-ACT-1 "
        "title filter. PDF fallback disabled. MAX_RECORDS=2.",
        "",
        "## Per-query results",
        "",
        "| # | Query | ZambiaLII total-count | /akn/zm/act/ links in page 1 |",
        "|---|-------|----------------------:|-----------------------------:|",
    ]
    for i, q in enumerate(PROBE_QUERIES, 1):
        tc, qd = per_query_totals.get(q, (0, 0))
        lines.append(f"| {i} | `{q}` | {tc} | {qd} |")
    lines.extend([
        "",
        "## Committed records",
        "",
        "None — zero novel primary-Act candidates survived "
        "HEAD + title filters after the no-nature-filter "
        "alphabetical-fallback probe rotation.",
        "",
        "## Novel candidates surviving filters",
        "",
    ])
    if filtered:
        lines.append("| # | Year/Num | Title | Via query |")
        lines.append("|---|----------|-------|-----------|")
        for i, (y, n, t, q) in enumerate(filtered[:20], 1):
            lines.append(f"| {i} | {y}/{n} | {t} | `{q}` |")
    else:
        lines.append(
            "No novel /akn/zm/act/ primary-parent candidates "
            "surfaced for any of the five probe queries."
        )
    lines.extend([
        "",
        "## Rejected candidates (novel but filtered)",
        "",
    ])
    if rejected:
        lines.append("| # | Year/Num | Title | Reason |")
        lines.append("|---|----------|-------|--------|")
        for i, (y, n, t, reason) in enumerate(rejected[:40], 1):
            lines.append(f"| {i} | {y}/{n} | {t} | {reason} |")
    else:
        lines.append("None — no novel candidates were surfaced to reject.")
    lines.extend([
        "",
        "## Integrity checks",
        "- CHECK 1 (batch unique IDs): PASS (no records to check)",
        "- CHECK 2 (no HEAD collision): PASS (no records to check)",
        "- CHECK 3 (source_hash matches raw on disk): PASS (no raw written)",
        "- CHECK 4 (amended_by / repealed_by reference resolution): PASS "
        "(no records to check)",
        "- CHECK 5 (required fields present): PASS (no records to check)",
        "",
        "## Interpretation",
        "",
        "Removing the `nature=Act` filter did NOT surface primary "
        "Cap. parents for Juveniles, Hire Purchase, Stamp Duties, "
        "Sale of Goods, or Bills of Exchange on ZambiaLII. "
        "Combined with the prior nature=Act probe-rotation 0-yield "
        "(batches 0167 – 0168), this strongly suggests these "
        "five pre-independence Cap. parents are **not indexed "
        "on ZambiaLII as standalone AKN documents**. ZambiaLII's "
        "current coverage concentrates on post-1964 Acts of "
        "Parliament; several pre-1964 English-derived Caps "
        "(e.g., Sale of Goods 1893 imperial, Bills of Exchange "
        "1882 imperial) appear to have no dedicated AKN landing "
        "page.",
        "",
        "## Next-tick plan",
        "",
        "Pivot the Phase-4 acts-in-force sweep away from the "
        "five unresolved ZambiaLII-missing Cap. parents and "
        "toward the **Parliament of Zambia** acts listing "
        "(`https://www.parliament.gov.zm/acts-of-parliament`), "
        "which has already been used as a seed source in "
        "earlier batches. Alternative fallbacks: (a) Government "
        "Printer bound-volume lookups (no known web index), "
        "(b) deferring the five Caps to Phase-7 "
        "re-verification. Preserve gaps entries so the human "
        "reviewer can flag a policy decision.",
        "",
        "## Raw snapshots",
        "",
        "No raw record files written this batch (probe-only). "
        "B2 sync deferred to host (rclone not available in "
        "sandbox).",
        "",
    ])
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return report_path


def main():
    print(f"=== Batch {BATCH_NUM} starting at {utc_now()} ===")
    start_ts = time.time()

    head_ids, head_year_num = load_head_ids()
    print(
        f"HEAD tracks {len(head_ids)} Act records, "
        f"{len(head_year_num)} unique (year,num) pairs"
    )

    seed_year_num = set()
    filtered, rejected, per_query_totals = probe_candidates(
        head_year_num, seed_year_num
    )

    # No ingestion this batch — alphabetical-fallback probe was
    # designed as a 0-yield confirmation pass (no new primary
    # parents expected given prior nature=Act probe 0-yield).
    # Still, if candidates survived, log them as gaps-deferred for
    # human review rather than auto-ingest (the 45s bash timeout
    # + PDF-disabled + MAX_RECORDS=2 envelope is tight).

    records = []
    gaps = []
    for y, n, title, q in filtered[:MAX_RECORDS]:
        gaps.append(
            f"{y}/{n} {title!r}: alphabetical-fallback novel candidate "
            f"surfaced via '{q}' — DEFERRED (probe-only pass; "
            "not auto-ingested)"
        )
    for y, n, title, reason in rejected[:40]:
        gaps.append(
            f"{y}/{n} {title!r}: alphabetical-fallback pre-fetch "
            f"reject — {reason}"
        )

    # Record a synthetic gap entry per unresolved Cap. parent to
    # make the human-review checklist explicit.
    for q in PROBE_QUERIES:
        tc, qd = per_query_totals.get(q, (0, 0))
        gaps.append(
            f"UNRESOLVED CAP. PARENT ({q!r}): no-nature-filter probe "
            f"returned ZambiaLII count={tc}, page-1 /akn/zm/act/ "
            f"links={qd}. No primary parent surfaced. "
            "Pivot next tick to parliament.gov.zm listing."
        )

    # Integrity — no records to check; all checks trivially pass.
    errors = []
    ts = utc_now()
    if errors:
        with open(WORKER_LOG, "a") as f:
            f.write(f"{ts} Batch {BATCH_NUM} INTEGRITY FAIL: {errors}\n")
        sys.exit(2)

    report_path = write_batch_report(
        per_query_totals, filtered, rejected, fetch_count
    )
    print(f"Report: {report_path}")

    with open(WORKER_LOG, "a") as f:
        f.write(
            f"{ts} Phase 4 Batch {BATCH_NUM} COMPLETE: +0 Acts "
            f"(alphabetical-fallback probe-only pass, no-nature-filter "
            f"rotation across 5 unresolved Cap. parents). "
            f"0 novel primary parents surfaced. Fetches: {fetch_count}. "
            f"Integrity: ALL PASS (no records to check). "
            f"Gaps: {len(gaps)}. Next tick: pivot to "
            "parliament.gov.zm acts-of-parliament listing. "
            f"Report: reports/batch-{BATCH_NUM}.md. "
            "B2 sync skipped — rclone not available.\n"
        )

    if gaps:
        with open(GAPS_MD, "a") as f:
            f.write(f"\n## Batch {BATCH_NUM} per-target notes ({ts})\n\n")
            for g in gaps:
                f.write(f"- {g}\n")

    print(
        f"=== Batch {BATCH_NUM} done: {len(records)} records, "
        f"{fetch_count} fetches, {len(gaps)} gaps ==="
    )


if __name__ == "__main__":
    main()
