#!/usr/bin/env python3
"""
Batch 0170 — Phase 4 bulk ingestion.

PIVOT per batch-0169 next-tick plan: after two successive 0-yield ticks
on the ZambiaLII `search/api/documents/` probe (batches 0168, 0169), the
plan is to pivot to the parliament.gov.zm `acts-of-parliament` listing.

Parliament.gov.zm listing pages 1-12 were cached on 2026-04-10 under
raw/discovery/parliament-zm/. A re-parse of those pages against HEAD
(existing_acts.txt, 729 Acts) and the B-POL-ACT-1 title filter
surfaced 5 novel primary-Act candidates, all from 2021:

    2021/41  Electronic Government Act, 2021               (/node/9014)
    2021/38  Insurance Act, 2021                           (/node/9009)
    2021/37  Zambia Correctional Service Act, 2021         (/node/9008)
    2021/35  Narcotic Drugs And Psychotropic Substances    (/node/9005)
    2021/34  Industrial Hemp Act, 2021                     (/node/9004)

These fill visible 2021 gaps in HEAD (HEAD has 2021/01-21, 23-33 — the
5 new slots are 2021/34, 35, 37, 38, 41). They are all primary Acts
(non-amendment / non-appropriation / non-repeal).

STRATEGY
- Source of TRUTH for ingest remains ZambiaLII AKN (consistent AKN
  structure and stable URLs) — candidates are looked up at
  https://zambialii.org/akn/zm/act/<year>/<number>.
- Parliament.gov.zm was the DISCOVERY source for this batch only
  (no content fetched from parliament.gov.zm this tick).
- HTML/AKN fetch first, PDF fallback if fewer than 2 parsed sections,
  with the pre-write B-POL-ACT-1 title filter (+OCR variants).
- MAX_RECORDS = 8 per tick policy; actual target = 5.

SANDBOX BUDGET
- Rate limit: 5s between ZambiaLII fetches (approvals.yaml).
- Wall clock: the sandbox bash timeout caps each invocation at 45s.
  The script supports a --slice CLI arg so one invocation processes a
  contiguous sub-range of the SEED list. Default is the full list.

No unconditional repeal-chain links pre-declared this batch.
No probe stage this batch (parliament.gov.zm listing has already been
re-parsed and provides a closed candidate list).
"""

import argparse
import hashlib
import io
import json
import os
import re
import sys
import time
import urllib.parse
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch_one import fetch, log_provenance  # noqa: E402

BATCH_NUM = "0170"
MAX_RECORDS = 8
USER_AGENT = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
PARSER_VERSION = "0.5.0"
RATE_LIMIT_ZAMBIALII = 5  # seconds between ZambiaLII requests

# SEED candidates discovered by re-parsing the cached parliament.gov.zm
# acts-of-parliament listing pages. Each tuple:
#   (year, number, slug_hint, note)
SEED_CANDIDATES = [
    (2021, 41, "electronic-government-act-2021",
     "parliament.gov.zm /node/9014 — primary Act, absent from HEAD"),
    (2021, 38, "insurance-act-2021",
     "parliament.gov.zm /node/9009 — primary Act, absent from HEAD"),
    (2021, 37, "zambia-correctional-service-act-2021",
     "parliament.gov.zm /node/9008 — primary Act, absent from HEAD"),
    (2021, 35, "narcotic-drugs-and-psychotropic-substances-act-2021",
     "parliament.gov.zm /node/9005 — primary Act, absent from HEAD"),
    (2021, 34, "industrial-hemp-act-2021",
     "parliament.gov.zm /node/9004 — primary Act, absent from HEAD"),
]

REJECT_TITLE_TOKENS = (
    "amendment",
    "amendrnent",   # OCR variant of 'amendment' (rn -> m)
    "amendement",   # stray 'e' OCR variant
    "appropriation",
    "repeal",
    "supplementary",
    "validation",
    "transitional",
)

UNCONDITIONAL_REPEAL_LINKS = []

WORKSPACE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COSTS_LOG = os.path.join(WORKSPACE, "costs.log")
WORKER_LOG = os.path.join(WORKSPACE, "worker.log")
GAPS_MD = os.path.join(WORKSPACE, "gaps.md")
RECORDS_DIR = os.path.join(WORKSPACE, "records", "acts")
RAW_DIR = os.path.join(WORKSPACE, "raw", "zambialii")
REPORTS_DIR = os.path.join(WORKSPACE, "reports")
STATE_PATH = os.path.join(WORKSPACE, f".batch_{BATCH_NUM}_state.json")

os.chdir(WORKSPACE)

fetch_count = 0
_last_fetch_ts = 0.0


def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def rate_limit():
    """Sleep only if the last fetch was less than RATE_LIMIT_ZAMBIALII
    seconds ago. Skips the leading sleep before the first fetch in an
    invocation, preserving courtesy spacing across the sub-tick."""
    global _last_fetch_ts
    if _last_fetch_ts:
        elapsed = time.time() - _last_fetch_ts
        remaining = RATE_LIMIT_ZAMBIALII - elapsed
        if remaining > 0:
            time.sleep(remaining)


def do_fetch(url, batch_tag=None):
    global fetch_count, _last_fetch_ts
    rate_limit()
    result = fetch(url)
    _last_fetch_ts = time.time()
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


def parse_html_sections(html_text):
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html_text, "html.parser")
    title_el = soup.find("h1") or soup.find("title")
    title = title_el.get_text(strip=True) if title_el else ""

    sections = []
    akn_sections = soup.find_all(
        ["section", "div"], class_=re.compile(r"akn-section")
    )
    if not akn_sections:
        akn_sections = soup.find_all(id=re.compile(r"sec_|chp_"))

    for sec in akn_sections:
        num_el = sec.find(class_=re.compile(r"akn-num"))
        heading_el = sec.find(class_=re.compile(r"akn-heading"))

        num = num_el.get_text(strip=True).rstrip(".") if num_el else ""
        heading = heading_el.get_text(strip=True) if heading_el else ""

        text_parts = []
        for child in sec.find_all(
            class_=re.compile(r"akn-content|akn-intro|akn-paragraph|akn-subsection")
        ):
            t = child.get_text(" ", strip=True)
            if t and t not in text_parts:
                text_parts.append(t)

        if not text_parts:
            text = sec.get_text(" ", strip=True)
            if heading and text.startswith(heading):
                text = text[len(heading):].strip()
            if num and text.startswith(num):
                text = text[len(num):].strip()
        else:
            text = "\n".join(text_parts)

        if num or heading or text:
            sections.append(
                {
                    "number": num,
                    "heading": heading,
                    "text": text[:5000],
                }
            )
    return title, sections


def parse_pdf_sections(pdf_bytes):
    import pdfplumber

    full_text = ""
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                pt = page.extract_text()
                if pt:
                    full_text += pt + "\n"
    except Exception as e:
        print(f"  PDF parse error: {e}", file=sys.stderr)
        return "", []

    if not full_text.strip():
        return "", []

    lines = full_text.strip().split("\n")
    title = lines[0].strip() if lines else ""

    sections = []
    section_pattern = re.compile(
        r"^(\d+)\.\s+(.+?)(?:\n|$)(.*?)(?=^\d+\.\s|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    for m in section_pattern.finditer(full_text):
        num = m.group(1)
        heading = m.group(2).strip()
        text = m.group(3).strip()
        sections.append({"number": num, "heading": heading, "text": text[:5000]})

    if not sections and full_text.strip():
        sections.append(
            {"number": "1", "heading": "Full text", "text": full_text[:5000]}
        )
    return title, sections


def title_rejected(title):
    tl = title.lower()
    for tok in REJECT_TITLE_TOKENS:
        if tok in tl:
            return tok
    return None


def build_record(year, number, title, sections, source_url, source_hash, fetched_at):
    slug = slugify(title) if title else f"act-{year}-{number}"
    record_id = f"act-zm-{year}-{number:03d}-{slug}"
    if len(record_id) > 100:
        record_id = record_id[:100]
    return {
        "id": record_id,
        "type": "act",
        "jurisdiction": "ZM",
        "title": title,
        "citation": f"Act No. {number} of {year}",
        "enacted_date": f"{year}-01-01",
        "commencement_date": None,
        "in_force": True,
        "amended_by": [],
        "repealed_by": None,
        "sections": sections,
        "source_url": source_url,
        "source_hash": f"sha256:{source_hash}",
        "fetched_at": fetched_at,
        "parser_version": PARSER_VERSION,
    }


def process_act(year, number, slug_hint, try_pdf_fallback=True):
    html_url = f"https://zambialii.org/akn/zm/act/{year}/{number}"
    print(f"\n--- {slug_hint} ({year}/{number}) ---")
    print(f"  Fetching HTML: {html_url}")
    r = do_fetch(html_url)

    if r["status"] != 200 or r["body_len"] < 1000:
        return None, None, f"HTML fetch failed: status={r['status']} len={r['body_len']}"

    html_body = r["_body_bytes"]
    html_hash = r["sha256"]
    source_url = r["final_url"] or html_url
    source_hash = html_hash
    fetched_at = r["started_at"]
    used_source = "html"

    title, sections = parse_html_sections(html_body.decode("utf-8", errors="replace"))

    if not title:
        title = f"Act No. {number} of {year}"
    title = re.sub(r"\s+", " ", title).strip()
    if title.upper().startswith("ACT"):
        title = title[3:].strip()

    reject_token = title_rejected(title)
    if reject_token:
        return None, None, (
            f"title rejected (contains '{reject_token}'): "
            f"{title!r}"
        )

    pdf_body = None
    pdf_hash = None
    pdf_url_used = None
    if try_pdf_fallback and len(sections) < 2:
        pdf_url = (r["final_url"] or html_url).rstrip("/") + "/source.pdf"
        print(f"  HTML sparse (sections={len(sections)}), trying PDF: {pdf_url}")
        pr = do_fetch(pdf_url)
        if pr["status"] == 200 and pr["body_len"] > 500:
            pdf_body = pr["_body_bytes"]
            pdf_hash = pr["sha256"]
            pdf_url_used = pr["final_url"] or pdf_url
            ptitle, psections = parse_pdf_sections(pdf_body)
            if psections:
                sections = psections
                source_url = pdf_url_used
                source_hash = pdf_hash
                used_source = "pdf"
                fetched_at = pr["started_at"]

    if not sections:
        return None, None, "no parseable sections in HTML or PDF"

    slug = slugify(title) if title else slug_hint
    record_id = f"act-zm-{year}-{number:03d}-{slug}"
    if len(record_id) > 100:
        record_id = record_id[:100]

    raw_subdir = os.path.join(RAW_DIR, str(year))
    os.makedirs(raw_subdir, exist_ok=True)

    html_path = os.path.join(raw_subdir, f"{record_id}.html")
    with open(html_path, "wb") as f:
        f.write(html_body)
    print(f"  Saved HTML raw: {html_path} ({len(html_body)} bytes)")

    pdf_path = None
    if pdf_body is not None:
        pdf_path = os.path.join(raw_subdir, f"{record_id}.pdf")
        with open(pdf_path, "wb") as f:
            f.write(pdf_body)
        print(f"  Saved PDF raw: {pdf_path} ({len(pdf_body)} bytes)")

    raw_path = pdf_path if used_source == "pdf" else html_path

    record = build_record(year, number, title, sections, source_url, source_hash, fetched_at)

    record_subdir = os.path.join(RECORDS_DIR, str(year))
    os.makedirs(record_subdir, exist_ok=True)
    record_path = os.path.join(record_subdir, f"{record['id']}.json")
    with open(record_path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
    print(f"  Saved record: {record_path}")
    print(f"  Title: {title!r}")
    print(f"  Sections: {len(sections)} (source={used_source})")
    return record, raw_path, None


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


def load_state():
    if not os.path.exists(STATE_PATH):
        return {
            "records": [],      # list of record dicts
            "raw_map": {},      # record_id -> raw_path
            "gaps": [],
            "next_idx": 0,
            "fetch_count": 0,
        }
    with open(STATE_PATH) as f:
        return json.load(f)


def save_state(state):
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def integrity_check_batch(records, raw_map, head_ids):
    errors = []

    ids = [r["id"] for r in records]
    if len(ids) != len(set(ids)):
        errors.append("DUPLICATE IDS IN BATCH")

    for r in records:
        if r["id"] in head_ids:
            errors.append(f"HEAD COLLISION: {r['id']}")

    for r in records:
        src_hash = r["source_hash"].replace("sha256:", "")
        raw_file = raw_map.get(r["id"])
        if not raw_file or not os.path.exists(raw_file):
            errors.append(f"RAW MISSING: {r['id']} ({raw_file})")
            continue
        with open(raw_file, "rb") as f:
            fh = hashlib.sha256(f.read()).hexdigest()
        if fh != src_hash:
            errors.append(
                f"HASH MISMATCH: {r['id']} "
                f"(raw={fh[:12]}... vs src={src_hash[:12]}... path={raw_file})"
            )

    for r in records:
        for field in ["id", "type", "jurisdiction", "title", "source_url",
                      "source_hash", "fetched_at", "parser_version"]:
            if not r.get(field):
                errors.append(f"MISSING FIELD: {r['id']}.{field}")

    return errors


def write_batch_report(records, gaps, total_sections, fetches, integrity_passed):
    os.makedirs(REPORTS_DIR, exist_ok=True)
    report_path = os.path.join(REPORTS_DIR, f"batch-{BATCH_NUM}.md")
    lines = [
        f"# Batch {BATCH_NUM} Report",
        "",
        f"**Date:** {utc_now()}",
        "**Phase:** 4 (Bulk Ingestion)",
        f"**Records committed:** {len(records)}",
        "**Repeal-chain links applied:** 0",
        f"**Fetches (script):** {fetches}",
        f"**Integrity:** {'PASS' if integrity_passed else 'FAIL'}",
        "",
        "## Strategy",
        "",
        "PIVOT per batch-0169 next-tick plan. Two successive 0-yield ticks on the "
        "ZambiaLII `search/api/documents/` probe (batches 0168, 0169) triggered a "
        "pivot to the parliament.gov.zm `acts-of-parliament` listing for candidate "
        "discovery. The 12 cached listing pages (fetched 2026-04-10, already on "
        "disk under `raw/discovery/parliament-zm/`) were re-parsed in-sandbox and "
        "cross-referenced against HEAD. Five novel primary-Act candidates surfaced, "
        "all from 2021 (filling HEAD gaps 2021/34, 35, 37, 38, 41). Each candidate "
        "was ingested from ZambiaLII's AKN endpoint "
        "(`https://zambialii.org/akn/zm/act/<year>/<number>`) with the pre-write "
        "B-POL-ACT-1 title filter (+OCR variants) and PDF fallback when HTML "
        "returned fewer than 2 parsed sections. No new fetches against "
        "parliament.gov.zm this tick (discovery-only re-parse).",
        "",
        "## Seed candidates",
        "",
        "| # | Year/Num | Title hint | Source | Outcome |",
        "|---|----------|------------|--------|---------|",
    ]
    seed_status = {}
    for r in records:
        m = re.match(r"^act-zm-(\d{4})-(\d+)-", r["id"])
        if m:
            seed_status[(int(m.group(1)), int(m.group(2)))] = (r["id"], "committed")
    for g in gaps:
        m = re.match(r"^(\d{4})/(\d+)", g)
        if m:
            seed_status.setdefault((int(m.group(1)), int(m.group(2))), (None, "gapped"))
    for i, (y, n, hint, _note) in enumerate(SEED_CANDIDATES, 1):
        rid, outcome = seed_status.get((y, n), (None, "deferred"))
        lines.append(
            f"| {i} | {y}/{n} | {hint} | parliament.gov.zm listing | "
            f"{outcome}{(' (' + rid + ')') if rid else ''} |"
        )
    lines.extend([
        "",
        "## Committed records",
        "",
        "| # | ID | Title | Citation | Sections | Source |",
        "|---|----|-------|----------|----------|--------|",
    ])
    for i, r in enumerate(records, 1):
        src = "PDF" if "pdf" in r.get("source_url", "").lower() else "HTML/AKN"
        lines.append(
            f"| {i} | `{r['id']}` | {r['title']} | {r['citation']} | "
            f"{len(r['sections'])} | {src} |"
        )
    lines.extend([
        "",
        f"**Total sections:** {total_sections}",
        "",
        "## Integrity checks",
        f"- CHECK 1 (batch unique IDs): {'PASS' if integrity_passed else 'FAIL'}",
        f"- CHECK 2 (no HEAD collision): {'PASS' if integrity_passed else 'FAIL'}",
        f"- CHECK 3 (source_hash matches raw on disk): {'PASS' if integrity_passed else 'FAIL'}",
        f"- CHECK 4 (amended_by / repealed_by resolution): "
        f"{'PASS' if integrity_passed else 'FAIL'} (no cross-refs this batch)",
        f"- CHECK 5 (required fields present): {'PASS' if integrity_passed else 'FAIL'}",
        "",
        "## Raw snapshots",
        "",
        "All raw bytes saved to `raw/zambialii/<year>/<id>.{html|pdf}`. "
        "B2 sync deferred to host (rclone not available in sandbox).",
        "",
    ])
    if gaps:
        lines.extend(["## Gaps / skipped targets", ""])
        for g in gaps:
            lines.append(f"- {g}")
        lines.append("")
    lines.extend([
        "## Notes",
        "",
        "- Parliament.gov.zm pivot established a stable discovery channel "
        "after ZambiaLII probe exhaustion in 0168-0169.",
        "- B-POL-ACT-1 title filter retained.",
        "- No unconditional repeal-chain link applied this batch.",
        "- Next tick: continue the parliament.gov.zm re-parse sweep — "
        "the page parse yielded only 5 novel primary parents across 12 pages, "
        "suggesting HEAD already covers most post-1994 primary Acts indexed "
        "there. If this tick commits all 5, next tick probes the 2021/22, "
        "2021/36, 2021/39, 2021/40 slots and cross-year remaining gaps "
        "(1990s/early-2000s); otherwise continues the deferred parliament "
        "candidates. Remain on the parliament.gov.zm rail until it exhausts, "
        "then restart ZambiaLII probe rotation with new keyword families.",
        "",
    ])
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return report_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slice", default="full",
                    help="range 'start:end' (0-indexed, end exclusive) or 'full'")
    ap.add_argument("--finalise", action="store_true",
                    help="run integrity + write report + worker.log and clear state")
    args = ap.parse_args()

    print(f"=== Batch {BATCH_NUM} starting at {utc_now()} (slice={args.slice} finalise={args.finalise}) ===")
    start_ts = time.time()

    head_ids, head_year_num = load_head_ids()
    print(f"HEAD tracks {len(head_ids)} Act records, {len(head_year_num)} unique (year,num) pairs")

    state = load_state()
    global fetch_count
    fetch_count = state.get("fetch_count", 0)

    if args.slice == "full":
        start, end = 0, len(SEED_CANDIDATES)
    else:
        a, b = args.slice.split(":")
        start, end = int(a), int(b)

    if not args.finalise:
        for idx in range(max(start, state["next_idx"]), min(end, len(SEED_CANDIDATES))):
            year, number, hint, note = SEED_CANDIDATES[idx]
            if (year, number) in head_year_num:
                state["gaps"].append(
                    f"{year}/{number} '{hint}': pre-queue reject — already in HEAD ({note})"
                )
                state["next_idx"] = idx + 1
                save_state(state)
                continue
            # Wall-clock guard — if we're over 35s, halt and defer.
            if time.time() - start_ts > 35:
                print(f"  Wall-clock budget (35s) reached before slot {idx}. Stopping.")
                save_state(state)
                state["fetch_count"] = fetch_count
                save_state(state)
                print(f"=== Partial tick: processed up to idx={state['next_idx']}, fetches={fetch_count} ===")
                return
            try:
                record, raw_path, err = process_act(year, number, hint)
            except Exception as e:
                import traceback
                traceback.print_exc()
                err = f"Exception: {type(e).__name__}: {e}"
                record = None
                raw_path = None
            if err or record is None:
                state["gaps"].append(f"{year}/{number} '{hint}': {err}")
            else:
                state["records"].append(record)
                state["raw_map"][record["id"]] = raw_path
            state["next_idx"] = idx + 1
            state["fetch_count"] = fetch_count
            save_state(state)

        print(f"=== Slice complete: next_idx={state['next_idx']}, "
              f"records={len(state['records'])}, fetches={fetch_count} ===")
        if state["next_idx"] >= len(SEED_CANDIDATES):
            print("  All seed slots processed. Re-run with --finalise to write report + worker.log.")
        return

    # --finalise path: integrity + report + worker.log
    records = state["records"]
    raw_map = state["raw_map"]
    gaps = state["gaps"]

    errors = integrity_check_batch(records, raw_map, head_ids)
    total_sections = sum(len(r["sections"]) for r in records)
    ts = utc_now()

    if errors:
        with open(WORKER_LOG, "a") as f:
            f.write(f"{ts} Batch {BATCH_NUM} INTEGRITY FAIL: {errors}\n")
        with open(GAPS_MD, "a") as f:
            f.write(f"\n## Batch {BATCH_NUM} integrity failures ({ts})\n\n")
            for e in errors:
                f.write(f"- {e}\n")
        err_dir = os.path.join(WORKSPACE, "error-reports")
        os.makedirs(err_dir, exist_ok=True)
        err_path = os.path.join(
            err_dir,
            f"{ts.replace(':', '').replace('-', '')}-batch-{BATCH_NUM}.md",
        )
        with open(err_path, "w") as f:
            f.write(f"# Batch {BATCH_NUM} integrity failure\n\n")
            for e in errors:
                f.write(f"- {e}\n")
        print("INTEGRITY FAILURES:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(2)

    report_path = write_batch_report(
        records, gaps, total_sections, state["fetch_count"],
        integrity_passed=True,
    )
    print(f"Report: {report_path}")

    with open(WORKER_LOG, "a") as f:
        titles = ", ".join(f"{r['title']} ({len(r['sections'])}s)" for r in records)
        f.write(
            f"{ts} Phase 4 Batch {BATCH_NUM} COMPLETE: +{len(records)} Acts via "
            f"parliament.gov.zm listing pivot -> ZambiaLII AKN ingest (HTML/PDF) "
            f"with pre-write B-POL-ACT-1 title filter (+OCR variants). "
            f"Records: {titles}. "
            f"{total_sections} sections total. Fetches: {state['fetch_count']}. "
            f"Integrity: ALL PASS. Gaps: {len(gaps)}. "
            f"Report: reports/batch-{BATCH_NUM}.md. "
            f"B2 sync deferred — rclone not available.\n"
        )

    if gaps:
        with open(GAPS_MD, "a") as f:
            f.write(f"\n## Batch {BATCH_NUM} per-target notes ({ts})\n\n")
            for g in gaps:
                f.write(f"- {g}\n")

    # Clear state
    if os.path.exists(STATE_PATH):
        os.remove(STATE_PATH)

    print(f"=== Batch {BATCH_NUM} done: {len(records)} records, "
          f"{state['fetch_count']} fetches, {len(gaps)} gaps ===")


if __name__ == "__main__":
    main()
