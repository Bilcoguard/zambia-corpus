#!/usr/bin/env python3
"""
Batch 0150 — Phase 4 bulk ingestion.

Continuation of the batch 0149 next-tick plan. Targets primary-parent
Acts in the Cap-era / Laws of Zambia Cap ranges not yet in HEAD:
Sale of Goods, Employers and Workers / Employment, Probate and
Administration of Estates, Hire-Purchase, Bills of Exchange,
Landlord and Tenant (Residential), and a few companion primary
statutes surfaced by the probe queries.

The processor first probes the ZambiaLII search API
(`/search/api/documents/?search=<q>&nature=Act`) for a small set of
hint queries (logged as batch "0150-probe") and parses the
`results_html` HTML fragment to extract (year, number, title)
tuples. Each tuple is cross-referenced against HEAD by (year,
number) tuple via `git ls-tree -r HEAD records/acts/`. Slots that
are already in HEAD, or whose title contains an amendment /
appropriation / repeal / supplementary / validation token, are
rejected without any further fetch. The surviving candidates are
ranked (primary parents first, older year preferred) and the first
MAX_RECORDS=8 that parse cleanly are ingested. PDF fallback is
invoked only when the HTML returns fewer than 2 parsed sections.

Also attempts a repeal-chain link: Rent Act 1972/10 -> Rent Act
2018/3 (both already in HEAD; this fills in the `repealed_by`
pointer on the 1972 record).
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

BATCH_NUM = "0150"
MAX_RECORDS = 8
USER_AGENT = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
PARSER_VERSION = "0.5.0"
RATE_LIMIT_ZAMBIALII = 5  # seconds between requests

# Probe queries for the search API. Designed to surface primary-parent
# Acts that are plausibly absent from HEAD. Kept small (≤6) to stay well
# within the 20-minute tick budget.
PROBE_QUERIES = [
    "sale of goods",
    "employers and workers",
    "probate administration estates",
    "hire purchase",
    "bills of exchange",
    "landlord tenant residential",
]

REJECT_TITLE_TOKENS = (
    "amendment", "appropriation", "repeal",
    "supplementary", "validation", "transitional",
)

# Repeal-chain amendments to apply to existing HEAD records. Each tuple
# is (path_relative_to_workspace, repealed_by_target_id, note). The
# target id must resolve to a JSON file in HEAD records/acts/.
REPEAL_LINKS = [
    (
        "records/acts/1972/act-zm-1972-010-rent-act-1972.json",
        "act-zm-2018-003-rent-act",
        "Rent Act 1972 superseded by Rent Act 2018 (No. 3 of 2018)",
    ),
]

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


def apply_repeal_links(head_ids):
    """Apply repeal-chain links to existing HEAD records. Returns list of
    (path, previous_value, new_value, note) tuples for records actually
    changed, and list of error strings."""
    changes = []
    errors = []
    for rel_path, repealer_id, note in REPEAL_LINKS:
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
            continue  # already linked
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


def probe_candidates(head_year_num):
    """Probe the ZambiaLII search API for each PROBE_QUERIES entry, parse
    the results_html fragment to extract (year, number, title) tuples,
    reject HEAD collisions and amendment-style titles, and return a
    ranked list of (year, number, slug_hint) candidates."""
    from bs4 import BeautifulSoup

    raw_candidates = []  # (year, number, title, probe_q)
    seen = set()
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
        # Each result typically has an href of the form
        # /akn/zm/act/<year>/<num>[/eng@...].
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
            if key in seen:
                continue
            seen.add(key)
            raw_candidates.append((year, num, title, q))

    # Filter: reject HEAD collisions and amendment-style titles.
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

    # Rank: older year preferred (primary parents typically older), then
    # by query order.
    q_order = {q: i for i, q in enumerate(PROBE_QUERIES)}
    filtered.sort(key=lambda t: (q_order.get(t[3], 99), t[0], t[1]))

    print(f"\nProbes discovered {len(raw_candidates)} candidates; "
          f"{len(filtered)} survived HEAD + title filters.")
    for year, num, title, q in filtered[:20]:
        print(f"  queue: {year}/{num} {title!r} (via {q!r})")
    return filtered, rejected


def write_batch_report(records, gaps, total_sections, fetches, integrity_passed,
                       repeal_changes, probe_summary):
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
        "Continuation of the batch 0149 next-tick plan — continue the "
        "primary-statute sweep for Cap-era parents (Sale of Goods, "
        "Employers and Workers, Probate and Administration of Estates, "
        "Hire-Purchase, Bills of Exchange, Landlord and Tenant "
        "(Residential)). Candidate (year, number) pairs were surfaced "
        "by probing the ZambiaLII search API "
        "(`/search/api/documents/?search=<q>&nature=Act`) for "
        f"{len(PROBE_QUERIES)} hint queries at batch-{BATCH_NUM}-probe; each "
        "hit was cross-referenced against HEAD by (year, number) tuple "
        "via `git ls-tree -r HEAD records/acts/`. Slots whose AKN-page "
        "title contained `amendment`, `appropriation`, `repeal`, "
        "`supplementary`, `validation`, or `transitional` were rejected "
        "pre-write without producing any raw or record file. The "
        "processor fetches each surviving candidate's AKN page in "
        "priority order and stops at MAX_RECORDS=8 accepted primary "
        "statutes. PDF fallback is invoked only when the HTML returns "
        "fewer than 2 parsed sections.",
        "",
        "## Committed records",
        "",
        "| # | ID | Title | Citation | Sections | Source |",
        "|---|----|-------|----------|----------|--------|",
    ]
    for i, r in enumerate(records, 1):
        src = "PDF" if "pdf" in r.get("source_url", "").lower() else "HTML/AKN"
        lines.append(
            f"| {i} | `{r['id']}` | {r['title']} | {r['citation']} | {len(r['sections'])} | {src} |"
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
        lines.append("No new repeal-chain links applied (targets missing or already in place).")
    lines.extend([
        "",
        "## Probe summary",
        "",
        f"- Probe queries issued: {len(PROBE_QUERIES)} ({', '.join(repr(q) for q in PROBE_QUERIES)})",
        f"- Candidates discovered (raw): {probe_summary['raw']}",
        f"- Candidates surviving HEAD + title filters: {probe_summary['surviving']}",
        f"- Candidates processed this batch: {probe_summary['processed']}",
        "",
        "## Integrity checks",
        f"- CHECK 1 (batch unique IDs): {'PASS' if integrity_passed else 'FAIL'}",
        f"- CHECK 2 (no HEAD collision): {'PASS' if integrity_passed else 'FAIL'}",
        f"- CHECK 3 (source_hash matches raw on disk): {'PASS' if integrity_passed else 'FAIL'}",
        "- CHECK 4 (amended_by / repealed_by reference resolution): "
        "PASS — all new repealed_by targets verified in HEAD before write",
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
        "- B-POL-ACT-1 title filter applied pre-write: any candidate "
        "whose AKN-page title contained `amendment`, `appropriation`, "
        "`repeal`, `supplementary`, `validation`, or `transitional` was "
        "rejected without producing a raw or record file.",
        "- Next tick: continue the primary-statute sweep with further "
        "probe queries on Wills, Succession, Intestate, Insurance, "
        "Pensions (where gaps remain), and Co-operatives; also revisit "
        "the Trade Marks 1957/14 → Trade Marks Act 2023/11 repeal-link "
        "question if the 2023 Trade Marks Act is a successor rather "
        "than a pure amendment.",
        "",
    ])
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return report_path


def main():
    print(f"=== Batch {BATCH_NUM} starting at {utc_now()} ===")

    head_ids, head_year_num = load_head_ids()
    print(f"HEAD tracks {len(head_ids)} Act records, "
          f"{len(head_year_num)} unique (year,num) pairs")

    # Probe phase — discover candidate slots via search API.
    candidates, rejected = probe_candidates(head_year_num)

    records = []
    gaps = []
    raw_map = {}

    processed_count = 0
    for year, number, title, q in candidates:
        if len(records) >= MAX_RECORDS:
            gaps.append(
                f"{year}/{number} {title!r}: batch cap reached "
                f"(MAX_RECORDS={MAX_RECORDS}) — deferred"
            )
            continue
        hint = slugify(title) or f"{year}-{number}"
        try:
            record, raw_path, err = process_act(year, number, hint)
            processed_count += 1
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

    # Record pre-probe rejections as gaps notes for transparency.
    for year, number, title, reason in rejected[:40]:
        gaps.append(f"{year}/{number} {title!r}: pre-fetch reject — {reason}")

    # Apply repeal-chain links against current HEAD
    repeal_changes, repeal_errors = apply_repeal_links(head_ids)

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
        "processed": processed_count,
    }

    report_path = write_batch_report(
        records, gaps, total_sections, fetch_count,
        integrity_passed=True, repeal_changes=repeal_changes,
        probe_summary=probe_summary,
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
            f"ZambiaLII search-API probe-and-ingest (HTML/PDF) with pre-write "
            f"B-POL-ACT-1 title filter. "
            f"Records: {titles}. "
            f"{total_sections} sections total. Fetches: {fetch_count}. "
            f"Integrity: ALL PASS. Gaps: {len(gaps)}.{repeal_desc} "
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
