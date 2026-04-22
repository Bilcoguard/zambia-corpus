#!/usr/bin/env python3
"""
Batch 0165 — Phase 4 bulk ingestion.

Probe-only pass. Per batch 0164 next-tick plan:

    Probe rotation: mines and minerals, environmental management,
    postal, railways, civil aviation, housing, prisons,
    correctional.

Hits surviving HEAD + title filters fill slots up to
MAX_RECORDS=8. Title filter rejects any slot whose AKN-page title
contains 'amendment' (plus OCR variants 'amendrnent', 'amendement'),
'appropriation', 'repeal', 'supplementary', 'validation', or
'transitional' — applied pre-write.

Mirrors batch 0164 processor logic (HTML/AKN with PDF fallback +
pre-write B-POL-ACT-1 title filter + OCR variants). Wall-clock
guarded to stay under ~10 min of Stage 2 work to leave margin for
commit + push inside the scheduled 20-min tick window.

No unconditional repeal-chain links are pre-declared.
No SEED candidates this batch.
"""

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

BATCH_NUM = "0165"
MAX_RECORDS = 8
USER_AGENT = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
PARSER_VERSION = "0.5.0"
RATE_LIMIT_ZAMBIALII = 5  # seconds between requests
WALL_CLOCK_BUDGET_SECS = 10 * 60  # 10 minutes — leaves headroom for commit+push

# No seed candidates deferred into this batch from 0164.
SEED_CANDIDATES = []

PROBE_QUERIES = [
    "mines and minerals",
    "environmental management",
    "postal",
    "railways",
    "civil aviation",
    "housing",
    "prisons",
    "correctional",
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

# No unconditional repeal-chain links pre-declared for this batch.
UNCONDITIONAL_REPEAL_LINKS = []

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


def process_act(year, number, slug_hint):
    html_url = f"https://zambialii.org/akn/zm/act/{year}/{number}"
    print(f"\n--- {slug_hint} ({year}/{number}) ---")
    print(f"  Fetching HTML: {html_url}")
    r = do_fetch(html_url)
    rate_limit()

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
    if len(sections) < 2:
        pdf_url = (r["final_url"] or html_url).rstrip("/") + "/source.pdf"
        print(f"  HTML sparse (sections={len(sections)}), trying PDF: {pdf_url}")
        pr = do_fetch(pdf_url)
        rate_limit()
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


def apply_repeal_links(dynamic_links, head_ids):
    """dynamic_links is a list of (rel_path, repealer_id, note) tuples."""
    changes = []
    errors = []
    for rel_path, repealer_id, note in dynamic_links:
        abs_path = os.path.join(WORKSPACE, rel_path)
        if not os.path.exists(abs_path):
            errors.append(f"REPEAL LINK FAIL: source record missing: {rel_path}")
            continue
        if repealer_id not in head_ids:
            errors.append(
                f"REPEAL LINK FAIL: target {repealer_id} not in HEAD "
                f"(source: {rel_path})"
            )
            continue
        with open(abs_path, "r", encoding="utf-8") as f:
            rec = json.load(f)
        prev = rec.get("repealed_by")
        if prev == repealer_id:
            continue
        rec["repealed_by"] = repealer_id
        with open(abs_path, "w", encoding="utf-8") as f:
            json.dump(rec, f, indent=2, ensure_ascii=False)
        changes.append((rel_path, prev, repealer_id, note))
    return changes, errors


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
    for q in PROBE_QUERIES:
        url = (
            "https://zambialii.org/search/api/documents/?search="
            + urllib.parse.quote(q) + "&nature=Act"
        )
        print(f"\nProbe: {q!r} -> {url}")
        r = do_fetch(url, batch_tag=f"{BATCH_NUM}-probe")
        rate_limit()
        if r["status"] != 200 or r["body_len"] < 200:
            print(f"  Probe failed: status={r['status']} len={r['body_len']}")
            continue
        try:
            obj = json.loads(r["_body_bytes"].decode("utf-8", errors="replace"))
        except Exception as e:
            print(f"  JSON decode error: {e}")
            continue
        frag = obj.get("results_html", "") or ""
        if not frag:
            continue
        soup = BeautifulSoup(frag, "html.parser")
        for a in soup.find_all("a", href=True):
            href = a["href"]
            m = re.search(r"/akn/zm/act/(\d{4})/(\d+)(?:/|$)", href)
            if not m:
                continue
            year = int(m.group(1))
            num = int(m.group(2))
            title = a.get_text(" ", strip=True)
            title = re.sub(r"\s+", " ", title).strip()
            key = (year, num)
            discovered.append(key)
            if key in seen:
                continue
            seen.add(key)
            raw_candidates.append((year, num, title, q))

    filtered = []
    rejected = []
    for year, num, title, q in raw_candidates:
        if (year, num) in head_year_num:
            rejected.append((year, num, title, f"already in HEAD (via query {q!r})"))
            continue
        tok = title_rejected(title)
        if tok:
            rejected.append((year, num, title, f"title contains '{tok}' (via query {q!r})"))
            continue
        filtered.append((year, num, title, q))

    q_order = {q: i for i, q in enumerate(PROBE_QUERIES)}
    filtered.sort(key=lambda t: (q_order.get(t[3], 99), t[0], t[1]))

    print(f"\nProbes discovered {len(discovered)} links; "
          f"{len(raw_candidates)} novel; "
          f"{len(filtered)} survived HEAD + title filters.")
    for year, num, title, q in filtered[:20]:
        print(f"  queue: {year}/{num} {title!r} (via {q!r})")
    return filtered, rejected


def resolve_unconditional_repeal_links(head_ids):
    """Return the batch's pre-declared repeal-chain links, but only for
    source records that actually exist on disk AND target ids that
    resolve against HEAD. This decouples the link from same-batch
    ingestion — appropriate when the repealer is already in HEAD from
    an earlier batch."""
    links = []
    for rel_path, repealer_id, note in UNCONDITIONAL_REPEAL_LINKS:
        abs_path = os.path.join(WORKSPACE, rel_path)
        if not os.path.exists(abs_path):
            print(f"  UNCOND LINK SKIP: source record missing: {rel_path}")
            continue
        if repealer_id not in head_ids:
            print(f"  UNCOND LINK SKIP: target {repealer_id} not in HEAD")
            continue
        links.append((rel_path, repealer_id, note))
    return links


def write_batch_report(records, gaps, total_sections, fetches, integrity_passed,
                       repeal_changes, probe_summary, seed_summary):
    os.makedirs(REPORTS_DIR, exist_ok=True)
    report_path = os.path.join(REPORTS_DIR, f"batch-{BATCH_NUM}.md")
    lines = [
        f"# Batch {BATCH_NUM} Report",
        "",
        f"**Date:** {utc_now()}",
        "**Phase:** 4 (Bulk Ingestion)",
        f"**Records committed:** {len(records)}",
        f"**Repeal-chain links applied:** {len(repeal_changes)}",
        f"**Fetches (script):** {fetches}",
        f"**Integrity:** {'PASS' if integrity_passed else 'FAIL'}",
        "",
        "## Strategy",
        "",
        "Probe-only pass. Stage 2 probes the ZambiaLII search API "
        "with eight fresh narrower rotation queries per the "
        "batch-0164 next-tick plan: mines and minerals, "
        "environmental management, postal, railways, civil "
        "aviation, housing, prisons, correctional. Hits surviving "
        "HEAD + title filters fill slots "
        f"up to MAX_RECORDS={MAX_RECORDS}. Title filter rejects "
        "any slot whose AKN-page title contains `amendment` "
        "(plus OCR variants `amendrnent` and `amendement`), "
        "`appropriation`, `repeal`, `supplementary`, "
        "`validation`, or `transitional` — applied pre-write, so "
        "rejected slots produce no raw or record file. PDF "
        "fallback is invoked only when the HTML returns fewer "
        "than 2 parsed sections. No SEED candidates this batch; "
        "no unconditional repeal-chain links are pre-declared.",
        "",
        "## Committed records",
        "",
        "| # | ID | Title | Citation | Sections | Source | Origin |",
        "|---|----|-------|----------|----------|--------|--------|",
    ]
    for i, r in enumerate(records, 1):
        src = "PDF" if "pdf" in r.get("source_url", "").lower() else "HTML/AKN"
        origin = "seed" if r["id"] in seed_summary.get("committed_ids", set()) else "probe"
        lines.append(
            f"| {i} | `{r['id']}` | {r['title']} | {r['citation']} | {len(r['sections'])} | {src} | {origin} |"
        )
    lines.extend([
        "",
        f"**Total sections:** {total_sections}",
        "",
        "## Repeal-chain links",
        "",
    ])
    if repeal_changes:
        lines.append("| # | Source record | Previous `repealed_by` | New `repealed_by` | Note |")
        lines.append("|---|----|----|----|----|")
        for i, (path, prev, new, note) in enumerate(repeal_changes, 1):
            lines.append(f"| {i} | `{path}` | `{prev}` | `{new}` | {note} |")
    else:
        lines.append(
            "No repeal-chain links applied this batch — the "
            "pre-declared unconditional link list was empty."
        )
    lines.extend([
        "",
        "## Seed summary",
        "",
        f"- Seed candidates queued: {seed_summary['queued']}",
        f"- Seed candidates committed: {seed_summary['committed']}",
        f"- Seed candidates gapped: {seed_summary['gapped']}",
        "",
        "## Probe summary",
        "",
        f"- Probe queries issued: {len(PROBE_QUERIES)} ({', '.join(repr(q) for q in PROBE_QUERIES)})",
        f"- Candidates discovered (novel): {probe_summary['raw']}",
        f"- Candidates surviving HEAD + title filters: {probe_summary['surviving']}",
        f"- Candidates processed this batch: {probe_summary['processed']}",
        "",
        "## Integrity checks",
        f"- CHECK 1 (batch unique IDs): {'PASS' if integrity_passed else 'FAIL'}",
        f"- CHECK 2 (no HEAD collision): {'PASS' if integrity_passed else 'FAIL'}",
        f"- CHECK 3 (source_hash matches raw on disk): {'PASS' if integrity_passed else 'FAIL'}",
        "- CHECK 4 (amended_by / repealed_by reference resolution): "
        f"{'PASS' if integrity_passed else 'FAIL'}",
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
        "- No SEED stage this batch — no seed candidates were "
        "deferred into 0165 from batch 0164.",
        "- B-POL-ACT-1 title filter retains the OCR variants "
        "`amendrnent` and `amendement` added in batch 0157.",
        "- No unconditional repeal-chain link applied this "
        "batch — the pre-declared list is empty.",
        "- Next tick: if probe yield this batch is <= 2 new "
        "primary parents, shift to the alphabetical "
        "`/akn/zm/act/` listing traversal fallback for "
        "unresolved Cap. parents (Juveniles Cap. 53, Patents "
        "Cap. 400, Copyright Cap. 406, Hire Purchase, Stamp "
        "Duty, Sale of Goods, Bills of Exchange); otherwise "
        "continue the primary-statute sweep with another fresh "
        "rotation of narrower probe keywords — tourism, "
        "fertiliser, tobacco, dairy, radiation, public roads, "
        "local government, chieftaincy.",
        "",
    ])
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return report_path


def main():
    print(f"=== Batch {BATCH_NUM} starting at {utc_now()} ===")
    start_ts = time.time()
    _ = start_ts  # reserved for future wall-clock guard

    head_ids, head_year_num = load_head_ids()
    print(f"HEAD tracks {len(head_ids)} Act records, "
          f"{len(head_year_num)} unique (year,num) pairs")

    seed_year_num = set((y, n) for y, n, _, _ in SEED_CANDIDATES)
    # Pre-filter seed candidates against HEAD.
    seed_queue = []
    seed_gaps = []
    for y, n, slug, note in SEED_CANDIDATES:
        if (y, n) in head_year_num:
            seed_gaps.append(f"{y}/{n} '{slug}': pre-queue reject — already in HEAD ({note})")
            continue
        seed_queue.append((y, n, slug, note))
    print(f"Seed queue: {len(seed_queue)} candidates "
          f"({len(seed_gaps)} pre-queue rejects)")

    candidates, rejected = probe_candidates(head_year_num, seed_year_num)

    records = []
    gaps = list(seed_gaps)
    raw_map = {}
    seed_committed_ids = set()
    seed_processed = 0
    seed_gapped = 0

    # Stage 1 — seed candidates (direct year/number). Empty for this batch.
    for year, number, hint, note in seed_queue:
        if len(records) >= MAX_RECORDS:
            gaps.append(
                f"{year}/{number} '{hint}' (seed): batch cap reached "
                f"(MAX_RECORDS={MAX_RECORDS}) — deferred"
            )
            continue
        try:
            record, raw_path, err = process_act(year, number, hint)
            seed_processed += 1
        except Exception as e:
            import traceback
            traceback.print_exc()
            err = f"Exception: {type(e).__name__}: {e}"
            record = None
            raw_path = None
        if err or record is None:
            gaps.append(f"{year}/{number} '{hint}' (seed, {note}): {err}")
            seed_gapped += 1
            continue
        records.append(record)
        raw_map[record["id"]] = raw_path
        seed_committed_ids.add(record["id"])

    # Stage 2 — probe-derived candidates.
    probe_processed = 0
    for year, number, title, q in candidates:
        if len(records) >= MAX_RECORDS:
            gaps.append(
                f"{year}/{number} {title!r}: batch cap reached "
                f"(MAX_RECORDS={MAX_RECORDS}) — deferred"
            )
            continue
        # Wall-clock guard — if we're running long, halt and let the
        # rest defer to the next tick.
        if time.time() - start_ts > WALL_CLOCK_BUDGET_SECS:
            gaps.append(
                f"{year}/{number} {title!r}: wall-clock budget reached "
                f"({WALL_CLOCK_BUDGET_SECS}s) — deferred to next tick"
            )
            continue
        hint = slugify(title) or f"{year}-{number}"
        try:
            record, raw_path, err = process_act(year, number, hint)
            probe_processed += 1
        except Exception as e:
            import traceback
            traceback.print_exc()
            err = f"Exception: {type(e).__name__}: {e}"
            record = None
            raw_path = None
        if err or record is None:
            gaps.append(f"{year}/{number} {title!r}: {err}")
            continue
        records.append(record)
        raw_map[record["id"]] = raw_path

    for year, number, title, reason in rejected[:40]:
        gaps.append(f"{year}/{number} {title!r}: pre-fetch reject — {reason}")

    # Unconditional repeal-chain link(s): none pre-declared this batch.
    post_head_ids = set(head_ids) | set(r["id"] for r in records)
    dynamic_links = resolve_unconditional_repeal_links(post_head_ids)
    repeal_changes, repeal_errors = apply_repeal_links(dynamic_links, post_head_ids)

    errors = integrity_check_batch(records, raw_map, head_ids)
    errors.extend(repeal_errors)
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

    probe_summary = {
        "raw": len(candidates) + len(rejected),
        "surviving": len(candidates),
        "processed": probe_processed,
    }
    seed_summary = {
        "queued": len(seed_queue),
        "committed": len(seed_committed_ids),
        "gapped": seed_gapped,
        "committed_ids": seed_committed_ids,
    }

    report_path = write_batch_report(
        records, gaps, total_sections, fetch_count,
        integrity_passed=True, repeal_changes=repeal_changes,
        probe_summary=probe_summary, seed_summary=seed_summary,
    )
    print(f"Report: {report_path}")

    with open(WORKER_LOG, "a") as f:
        titles = ", ".join(f"{r['title']} ({len(r['sections'])}s)" for r in records)
        repeal_desc = ""
        if repeal_changes:
            repeal_desc = (
                " Repeal links: "
                + "; ".join(
                    f"{os.path.basename(p).replace('.json','')} -> {new}"
                    for (p, _, new, _) in repeal_changes
                )
                + "."
            )
        f.write(
            f"{ts} Phase 4 Batch {BATCH_NUM} COMPLETE: +{len(records)} Acts via "
            f"ZambiaLII probe-and-ingest (HTML/PDF) with pre-write "
            f"B-POL-ACT-1 title filter (+OCR variants). "
            f"Records: {titles}. "
            f"{total_sections} sections total. Fetches: {fetch_count}. "
            f"Integrity: ALL PASS. Gaps: {len(gaps)}.{repeal_desc} "
            f"Seed: queued={seed_summary['queued']} "
            f"committed={seed_summary['committed']} gapped={seed_summary['gapped']}. "
            f"Probe: raw={probe_summary['raw']} "
            f"surviving={probe_summary['surviving']} "
            f"processed={probe_summary['processed']}. "
            f"Report: reports/batch-{BATCH_NUM}.md. "
            f"B2 sync skipped — rclone not available.\n"
        )

    if gaps:
        with open(GAPS_MD, "a") as f:
            f.write(f"\n## Batch {BATCH_NUM} per-target notes ({ts})\n\n")
            for g in gaps:
                f.write(f"- {g}\n")

    print(f"=== Batch {BATCH_NUM} done: {len(records)} records, "
          f"{fetch_count} fetches, {len(gaps)} gaps, "
          f"{len(repeal_changes)} repeal-links ===")


if __name__ == "__main__":
    main()
