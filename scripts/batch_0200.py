#!/usr/bin/env python3
"""
Batch 0200 — Phase 4 sis_employment rotation.

Per batch-0199 next-tick plan:
  "rotate to sis_employment (priority_order item 4) via alphabet=E
   (Employment Code Act 2019/003 derivative SIs) and alphabet=M
   (Minimum Wages orders), with parent-Act back-reference probe on
   /akn/zm/act/2019/3. If sis_employment yield <3, rotate to
   sis_data_protection (priority_order item 6)."

Discovery (this tick):
  Cached alphabet E/M from batch-0198 cross-checked; most obvious
  Employment Code and Minimum Wages SIs already in corpus. Fresh
  alphabet F/W/L/N fetched this tick (4 discovery); parent-Act probes
  on Minimum Wages and Conditions of Employment Act 1982/25, Industrial
  and Labour Relations Act 1993/27, Worker's Compensation Act 1999/10,
  Employment Code Act 2019/3 (4 more discovery).

Novel targets identified (4 total, all sis_employment):

  2022/013 Minimum Wages and Conditions of Employment (Truck and Bus
           Drivers) (Amendment) Order, 2022                 [alphabet=M]
  2018/035 Industrial and Labour Relations (Fees) Regulations, 2018
                                                            [alphabet=I]
  2019/029 Employment Code Act (Commencement) Order, 2019
                                                 [parent-act 2019/3]
  2000/105 Worker's Compensation Act 1999 (Commencement) Order, 2000
                                                 [parent-act 1999/10]

MAX_BATCH_SIZE=8 respected (4 records; yield <3 threshold cleared).
Expected ingest fetches: 8 (HTML+PDF pairs). Discovery fetches already
issued pre-script (9: robots + alphabet F/W/L/N + parent-acts 1982/25,
1993/27, 1999/10, 2019/3). Today's cumulative pre-tick ~346/2000
(17.3%); post-tick ~346+9+8=363/2000 (18.2%). Well inside daily budget.

Robots.txt re-verified at tick start (sha256 prefix fce67b697ee4ef44,
unchanged from batches 0193-0199). All target paths under permitted
/akn/zm/act/si/. case_law_scz remains paused per robots.txt Disallow on
/akn/zm/judgment/.
"""
import argparse
import hashlib
import io
import json
import os
import re
import sys
import time
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

BATCH_NUM = "0200"
USER_AGENT = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
PARSER_VERSION = "0.5.0"
CRAWL_DELAY_SECONDS = 6

TARGETS = [
    (2022, 13,  "sis_employment"),   # Minimum Wages T&B Drivers AMD 2022
    (2018, 35,  "sis_employment"),   # Industrial and Labour Relations (Fees) 2018
    (2019, 29,  "sis_employment"),   # Employment Code Act (Commencement) 2019
    (2000, 105, "sis_employment"),   # Worker's Compensation Act 1999 (Commencement) 2000
]

WORKSPACE = os.environ.get("KWLP_CORPUS_WORKSPACE") or os.getcwd()
os.chdir(WORKSPACE)
UTC = timezone.utc


def utc_now():
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def slugify(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text).strip("-")
    text = re.sub(r"-+", "-", text)
    return text[:80]


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
    header_title = lines[0].strip() if lines else ""
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
        sections.append({"number": "1", "heading": "Full text", "text": full_text[:5000]})
    return header_title, sections


def fetch(url, session, last_fetch_t):
    if last_fetch_t[0] is not None:
        elapsed = time.time() - last_fetch_t[0]
        if elapsed < CRAWL_DELAY_SECONDS:
            sleep = CRAWL_DELAY_SECONDS - elapsed
            print(f"  sleep {sleep:.1f}s (zambialii crawl delay)")
            time.sleep(sleep)
    print(f"  GET {url}")
    r = session.get(url, timeout=40, allow_redirects=True)
    last_fetch_t[0] = time.time()
    return r


def extract_title_and_pdf(html_bytes):
    soup = BeautifulSoup(html_bytes, "html.parser")
    title = ""
    for sel in [{"property": "og:title"}, {"name": "twitter:title"}]:
        m = soup.find("meta", attrs=sel)
        if m and m.get("content"):
            title = m["content"].strip()
            break
    if not title and soup.title:
        title = soup.title.get_text(strip=True).split("|")[0].strip()
    title = re.sub(r"\s+", " ", title)
    pdf_url = None
    for a in soup.find_all("a", href=True):
        h = a["href"]
        if "/source.pdf" in h or (h.endswith(".pdf") and "/akn/" in h):
            pdf_url = h if h.startswith("http") else f"https://zambialii.org{h}"
            break
    if not pdf_url:
        for a in soup.find_all("a", href=True):
            h = a["href"]
            if "media.zambialii.org" in h and h.endswith(".pdf"):
                pdf_url = h
                break
    if not pdf_url:
        for a in soup.find_all("a", href=True):
            h = a["href"]
            if "commons.laws.africa" in h and h.endswith(".pdf"):
                pdf_url = h
                break
    return title, pdf_url


def build_record(year, number, title, sections, source_url, source_hash,
                 fetched_at, alternates):
    slug = slugify(title) if title else f"si-{year}-{number}"
    record_id = f"si-zm-{year}-{number:03d}-{slug}"
    if len(record_id) > 120:
        record_id = record_id[:120]
    return {
        "id": record_id,
        "type": "si",
        "jurisdiction": "ZM",
        "title": title,
        "citation": f"Statutory Instrument No. {number} of {year}",
        "enacted_date": None,
        "commencement_date": None,
        "in_force": True,
        "amended_by": [],
        "repealed_by": None,
        "sections": sections,
        "source_url": source_url,
        "source_hash": f"sha256:{source_hash}",
        "fetched_at": fetched_at,
        "parser_version": PARSER_VERSION,
        "alternate_sources": alternates,
    }


def process_target(session, year, number, sub_phase, head_ids, head_slots,
                   last_fetch_t, fetch_counter):
    akn_url = f"https://zambialii.org/akn/zm/act/si/{year}/{number}"
    start_html = utc_now()
    try:
        rh = fetch(akn_url, session, last_fetch_t)
    except Exception as e:
        return f"fetch_html_error:{type(e).__name__}:{e}", None, None
    fetch_counter[0] += 1
    if rh.status_code != 200:
        return f"http_{rh.status_code}", None, None
    html_bytes = rh.content
    html_hash = hashlib.sha256(html_bytes).hexdigest()
    final_url = rh.url

    title, pdf_url = extract_title_and_pdf(html_bytes)
    if not pdf_url:
        return f"no_pdf_link:title={title!r}:final={final_url}", None, None

    start_pdf = utc_now()
    try:
        rp = fetch(pdf_url, session, last_fetch_t)
    except Exception as e:
        return f"fetch_pdf_error:{type(e).__name__}:{e}", None, None
    fetch_counter[0] += 1
    if rp.status_code != 200:
        return f"pdf_http_{rp.status_code}", None, None
    pdf_bytes = rp.content
    pdf_hash = hashlib.sha256(pdf_bytes).hexdigest()

    pdf_title, sections = parse_pdf_sections(pdf_bytes)
    if not sections:
        return "pdf_parse_empty", None, None
    if not title and pdf_title:
        title = pdf_title
    if not title:
        return "no_title", None, None

    raw_dir = os.path.join(WORKSPACE, "raw", "zambialii", "si", str(year))
    os.makedirs(raw_dir, exist_ok=True)
    safe_title_slug = slugify(title) or f"si-{year}-{number}"
    stem = f"si-zm-{year}-{number:03d}-{safe_title_slug}"[:120]
    raw_html = os.path.join(raw_dir, stem + ".html")
    raw_pdf = os.path.join(raw_dir, stem + ".pdf")
    with open(raw_html, "wb") as f:
        f.write(html_bytes)
    with open(raw_pdf, "wb") as f:
        f.write(pdf_bytes)

    record = build_record(
        year=year, number=number, title=title, sections=sections,
        source_url=pdf_url, source_hash=pdf_hash, fetched_at=start_pdf,
        alternates=[{
            "source_url": final_url,
            "source_hash": f"sha256:{html_hash}",
            "fetched_at": start_html,
            "role": "discovery_and_title",
        }],
    )

    # CHECK1: id collision with HEAD
    if record["id"] in head_ids:
        return f"check1_fail_id_collision:{record['id']}", None, None
    # CHECK2: prefix/slot collision within SI namespace
    prefix = f"si-zm-{year}-{number:03d}-"
    if any(i.startswith(prefix) for i in head_ids):
        return f"check2_fail_prefix_clash:{prefix}", None, None
    # CHECK3: on-disk hash matches source_hash
    with open(raw_pdf, "rb") as f:
        if hashlib.sha256(f.read()).hexdigest() != pdf_hash:
            return "check3_fail_hash_mismatch", None, None
    # CHECK4: cross-refs empty
    if record["amended_by"] or record["repealed_by"]:
        return "check4_fail_crossref_present", None, None
    # CHECK5: required fields
    for k in ("id", "type", "jurisdiction", "title", "citation", "sections",
              "source_url", "source_hash", "fetched_at", "parser_version"):
        if record.get(k) in (None, "", []):
            return f"check5_fail_missing:{k}", None, None

    out_dir = os.path.join(WORKSPACE, "records", "sis", str(year))
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{record['id']}.json")
    with open(out_path, "w") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)

    today = datetime.now(UTC).strftime("%Y-%m-%d")
    with open("costs.log", "a") as f:
        f.write(json.dumps({"date": today, "url": akn_url,
                            "bytes": len(html_bytes),
                            "batch": BATCH_NUM, "fetch_n": fetch_counter[0] - 1}) + "\n")
        f.write(json.dumps({"date": today, "url": pdf_url,
                            "bytes": len(pdf_bytes),
                            "batch": BATCH_NUM, "fetch_n": fetch_counter[0]}) + "\n")
    with open("provenance.log", "a") as f:
        f.write(json.dumps({"request_url": akn_url, "status": 200,
                            "sha256": html_hash, "bytes": len(html_bytes),
                            "started_at": start_html, "batch": BATCH_NUM,
                            "parser_version": PARSER_VERSION,
                            "sub_phase": sub_phase}) + "\n")
        f.write(json.dumps({"request_url": pdf_url, "status": 200,
                            "sha256": pdf_hash, "bytes": len(pdf_bytes),
                            "started_at": start_pdf, "batch": BATCH_NUM,
                            "parser_version": PARSER_VERSION,
                            "sub_phase": sub_phase}) + "\n")

    head_slots.add((year, number))
    return "ok", record, {
        "akn_url": akn_url, "pdf_url": pdf_url,
        "html_hash": html_hash, "pdf_hash": pdf_hash,
        "html_bytes": len(html_bytes), "pdf_bytes": len(pdf_bytes),
        "raw_html": raw_html, "raw_pdf": raw_pdf,
        "record_path": out_path, "sections": len(sections),
        "title": title, "sub_phase": sub_phase,
    }


def load_head():
    head_ids = set()
    head_slots = set()
    for root, dirs, files in os.walk(os.path.join(WORKSPACE, "records", "sis")):
        for fn in files:
            if fn.endswith(".json"):
                rid = fn[:-5]
                head_ids.add(rid)
                m = re.match(r"si-zm-(\d{4})-(\d+)-", rid)
                if m:
                    head_slots.add((int(m.group(1)), int(m.group(2))))
    return head_ids, head_slots


def run_slice(start_idx, end_idx, fetch_start):
    head_ids, head_slots = load_head()
    print(f"HEAD SI records: {len(head_ids)}; slots: {len(head_slots)}")
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    last_fetch_t = [None]
    fetch_counter = [fetch_start]
    started_at = utc_now()

    results = []
    for (year, number, sub_phase) in TARGETS[start_idx:end_idx]:
        print(f"\n=== SI {year}/{number:03d}  [{sub_phase}] ===")
        status, rec, meta = process_target(
            session, year, number, sub_phase, head_ids, head_slots,
            last_fetch_t, fetch_counter)
        print(f"  status: {status}")
        entry = {"year": year, "number": number, "sub_phase": sub_phase,
                 "status": status}
        if rec is not None:
            entry.update({
                "record_id": rec["id"],
                "sections": meta["sections"],
                "title": meta["title"],
                "pdf_url": meta["pdf_url"],
                "pdf_hash": meta["pdf_hash"],
                "pdf_bytes": meta["pdf_bytes"],
                "raw_pdf": meta["raw_pdf"],
                "record_path": meta["record_path"],
            })
            head_ids.add(rec["id"])
        else:
            with open("gaps.md", "a") as f:
                f.write(f"- [{utc_now()}] si/{year}/{number:03d} status={status} "
                        f"url=https://zambialii.org/akn/zm/act/si/{year}/{number} "
                        f"batch={BATCH_NUM} sub_phase={sub_phase}\n")
        results.append(entry)

    slice_key = f"{start_idx}_{end_idx}"
    partial = {
        "batch": BATCH_NUM,
        "slice": [start_idx, end_idx],
        "started_at": started_at,
        "completed_at": utc_now(),
        "fetch_start": fetch_start,
        "fetch_end": fetch_counter[0],
        "results": results,
    }
    os.makedirs("_work", exist_ok=True)
    with open(f"_work/batch_{BATCH_NUM}_slice_{slice_key}.json", "w") as f:
        json.dump(partial, f, indent=2)
    print(f"\n==> slice {slice_key}: {sum(1 for r in results if r['status']=='ok')}/"
          f"{len(results)} ok, fetch_end={fetch_counter[0]}")
    return fetch_counter[0]


def write_final_state():
    slices = []
    for fn in sorted(os.listdir("_work")):
        if fn.startswith(f"batch_{BATCH_NUM}_slice_") and fn.endswith(".json"):
            with open(os.path.join("_work", fn)) as f:
                slices.append(json.load(f))
    all_results = []
    for s in slices:
        all_results.extend(s["results"])
    ok = sum(1 for r in all_results if r["status"] == "ok")
    emp_ok = sum(1 for r in all_results
                 if r["status"] == "ok" and r["sub_phase"] == "sis_employment")
    summary = {
        "batch": BATCH_NUM,
        "phase": "phase_4_bulk",
        "sub_phase": "sis_employment_rotation_opener",
        "started_at": slices[0]["started_at"] if slices else utc_now(),
        "completed_at": utc_now(),
        "fetches_used": slices[-1]["fetch_end"] if slices else 0,
        "records_written": ok,
        "targets_attempted": len(all_results),
        "employment_records_ok": emp_ok,
        "results": all_results,
        "slices": [s["slice"] for s in slices],
        "robots_sha256_prefix": "fce67b697ee4ef44",
    }
    with open(f"_work/batch_{BATCH_NUM}_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    with open(f".batch_{BATCH_NUM}_state.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nFINAL batch {BATCH_NUM}: {ok}/{len(all_results)} ok, "
          f"fetches={summary['fetches_used']}, emp_ok={emp_ok}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slice", required=True,
                    help="start:end indices into TARGETS")
    ap.add_argument("--fetch-start", type=int, required=True)
    ap.add_argument("--final", action="store_true",
                    help="After slice, aggregate slices into state+summary.")
    args = ap.parse_args()
    s, e = [int(x) for x in args.slice.split(":")]
    fetch_end = run_slice(s, e, args.fetch_start)
    print(f"FETCH_END={fetch_end}")
    if args.final:
        write_final_state()
    return 0


if __name__ == "__main__":
    sys.exit(main())
