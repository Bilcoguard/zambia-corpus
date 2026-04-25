#!/usr/bin/env python3
"""
Batch 0205 — Phase 4 sis_employment rotation.

Per batch-0204 next-tick plan:
  "Continue sis_corporate with deeper L probe... and a fresh probe of
   alphabets E... and T.... If yield still <3 across two consecutive
   ticks, rotate to sis_employment (priority_order item 4) — Employment
   Code Act 2019/3 derivatives, NHIMA Act 2018/2 SIs, NAPSA Act SIs."

Batch 0204 yielded only 1 keyword-matching novel sis_corporate candidate
(R 2015/033 only); seven others were sourced from curated overrides.
That counts as the first low-yield tick for sis_corporate. Per the
fallback, this tick rotates to sis_employment and uses the same proven
discovery+ingest pipeline.

Workflow:
  1. Re-verify robots.txt (sha256, must match prefix fce67b697ee4ef44).
  2. Live discovery probes — alphabets E, M, N, O, W — extract
     /akn/zm/act/si/ hrefs along with their visible link text.
  3. Filter to novel (year, number) slots not already in HEAD
     records/sis, then keep only candidates whose visible title contains
     employment / labour / NAPSA / NHIMA / occupational / wages /
     workers' compensation / industrial relations keywords.
  4. Ingest up to MAX_BATCH_SIZE = 8 records using the same path that
     batches 0201-0204 followed (HTML → PDF → pdfplumber sectioning →
     CHECK1-5).

MAX_BATCH_SIZE = 8 records hard cap. Crawl delay = 6 s (margin over the
robots.txt-declared 5 s). Daily fetch budget tracked through costs.log.
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

BATCH_NUM = "0212"
USER_AGENT = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
PARSER_VERSION = "0.5.0"
CRAWL_DELAY_SECONDS = 6
MAX_BATCH_SIZE = 8
ROBOTS_SHA256_EXPECTED_PREFIX = "fce67b697ee4ef44"
SUB_PHASE_TAG = "sis_tax"

# Keyword tags used to qualify candidate SI link text from alphabet indexes.
# sis_employment scope: Employment Code Act 2019/3 derivatives, Industrial
# and Labour Relations Act, NAPSA Act 1996/40, NHIMA Act 2018/2, Workers'
# Compensation Act, Minimum Wages and Conditions of Employment Act,
# Occupational Health and Safety Act 2010/36.
CORPORATE_KEYWORDS = [
    "income tax",
    "value added tax",
    "value-added tax",
    "vat",
    "customs and excise",
    "customs",
    "excise",
    "tax appeals",
    "tax administration",
    "property transfer tax",
    "property-transfer tax",
    "tourism levy",
    "tobacco levy",
    "skills development levy",
    "insurance premium levy",
    "mineral royalty",
    "withholding tax",
    "double taxation",
    "presumptive tax",
    "turnover tax",
    "rental income",
    "carbon emission",
    "petroleum levy",
    "fuel levy",
    "advance tax",
    "tax clearance",
    "tax remission",
    "exemption",
    "remission",
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

    if record["id"] in head_ids:
        return f"check1_fail_id_collision:{record['id']}", None, None
    prefix = f"si-zm-{year}-{number:03d}-"
    if any(i.startswith(prefix) for i in head_ids):
        return f"check2_fail_prefix_clash:{prefix}", None, None
    with open(raw_pdf, "rb") as f:
        if hashlib.sha256(f.read()).hexdigest() != pdf_hash:
            return "check3_fail_hash_mismatch", None, None
    if record["amended_by"] or record["repealed_by"]:
        return "check4_fail_crossref_present", None, None
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


def verify_robots(session, last_fetch_t, fetch_counter):
    """Re-fetch robots.txt and confirm sha256 prefix."""
    url = "https://zambialii.org/robots.txt"
    r = fetch(url, session, last_fetch_t)
    fetch_counter[0] += 1
    if r.status_code != 200:
        raise RuntimeError(f"robots.txt fetch failed: HTTP {r.status_code}")
    h = hashlib.sha256(r.content).hexdigest()
    if not h.startswith(ROBOTS_SHA256_EXPECTED_PREFIX):
        raise RuntimeError(
            f"robots.txt drift: got {h[:16]}, expected {ROBOTS_SHA256_EXPECTED_PREFIX}"
        )
    raw_dir = os.path.join(WORKSPACE, "raw", "discovery", "zambialii")
    os.makedirs(raw_dir, exist_ok=True)
    with open(os.path.join(raw_dir, "robots.txt"), "wb") as f:
        f.write(r.content)
    today = datetime.now(UTC).strftime("%Y-%m-%d")
    with open("costs.log", "a") as f:
        f.write(json.dumps({"date": today, "url": url,
                            "bytes": len(r.content),
                            "batch": BATCH_NUM, "fetch_n": fetch_counter[0],
                            "purpose": "robots_reverify"}) + "\n")
    with open("provenance.log", "a") as f:
        f.write(json.dumps({"request_url": url, "status": 200,
                            "sha256": h, "bytes": len(r.content),
                            "started_at": utc_now(), "batch": BATCH_NUM,
                            "parser_version": PARSER_VERSION,
                            "sub_phase": "robots_reverify"}) + "\n")
    print(f"  robots.txt sha256={h} (prefix OK)")
    return h


def probe_alphabet(session, letter, last_fetch_t, fetch_counter):
    """Fetch the legislation alphabet index page for a given letter and
    extract /akn/zm/act/si/<year>/<num> hrefs along with link text."""
    url = f"https://zambialii.org/legislation/?alphabet={letter}"
    r = fetch(url, session, last_fetch_t)
    fetch_counter[0] += 1
    if r.status_code != 200:
        print(f"  alphabet={letter} HTTP {r.status_code} — skipping")
        return []
    today = datetime.now(UTC).strftime("%Y-%m-%d")
    h = hashlib.sha256(r.content).hexdigest()
    raw_dir = os.path.join(WORKSPACE, "raw", "zambialii", "legislation")
    os.makedirs(raw_dir, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%d")
    with open(os.path.join(raw_dir, f"alphabet-{letter}-{stamp}.html"), "wb") as f:
        f.write(r.content)
    with open("costs.log", "a") as f:
        f.write(json.dumps({"date": today, "url": url,
                            "bytes": len(r.content),
                            "batch": BATCH_NUM, "fetch_n": fetch_counter[0],
                            "purpose": f"alphabet_{letter}"}) + "\n")
    with open("provenance.log", "a") as f:
        f.write(json.dumps({"request_url": url, "status": 200,
                            "sha256": h, "bytes": len(r.content),
                            "started_at": utc_now(), "batch": BATCH_NUM,
                            "parser_version": PARSER_VERSION,
                            "sub_phase": f"alphabet_probe_{letter}"}) + "\n")

    soup = BeautifulSoup(r.content, "html.parser")
    candidates = []
    seen = set()
    for a in soup.find_all("a", href=True):
        h = a["href"]
        m = re.match(r"^/akn/zm/act/si/(\d{4})/(\d+)(?:/|$|@)", h)
        if not m:
            continue
        year = int(m.group(1)); number = int(m.group(2))
        text = a.get_text(" ", strip=True).lower()
        key = (year, number)
        if key in seen:
            continue
        seen.add(key)
        candidates.append({"year": year, "number": number, "text": text,
                           "letter": letter})
    print(f"  alphabet={letter}: {len(candidates)} unique SI candidates")
    return candidates


def filter_candidates(cands, head_slots):
    """Drop slots already in HEAD; keep only those whose link text matches a
    corporate/finance keyword."""
    out = []
    for c in cands:
        if (c["year"], c["number"]) in head_slots:
            continue
        text = c["text"]
        if not any(kw in text for kw in CORPORATE_KEYWORDS):
            continue
        out.append(c)
    return out


def cmd_discovery(args):
    """Phase A: robots verify + alphabet probes + write discovery state."""
    head_ids, head_slots = load_head()
    print(f"HEAD SI records: {len(head_ids)}; slots: {len(head_slots)}")

    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    last_fetch_t = [None]
    fetch_counter = [args.fetch_start]
    started_at = utc_now()

    print("=== robots.txt re-verify ===")
    robots_hash = verify_robots(session, last_fetch_t, fetch_counter)

    all_cands = []
    letters = list(args.alphabets)
    for letter in letters:
        print(f"\n=== alphabet probe: {letter} ===")
        all_cands.extend(probe_alphabet(session, letter, last_fetch_t, fetch_counter))

    novel_all = [c for c in all_cands if (c["year"], c["number"]) not in head_slots]
    novel = filter_candidates(all_cands, head_slots)
    dedup = {}
    for c in novel:
        key = (c["year"], c["number"])
        if key not in dedup:
            dedup[key] = c
    novel = list(dedup.values())
    novel.sort(key=lambda c: (-c["year"], c["number"]))

    state = {
        "batch": BATCH_NUM,
        "phase": "discovery",
        "started_at": started_at,
        "completed_at": utc_now(),
        "fetches_used": fetch_counter[0] - args.fetch_start,
        "fetch_end": fetch_counter[0],
        "robots_sha256": robots_hash,
        "alphabets": letters,
        "novel_total_pre_keyword": len(novel_all),
        "novel_kept_post_keyword": len(novel),
        "candidates": novel,
        "novel_pre_keyword_sample": novel_all[:200],
    }
    os.makedirs("_work", exist_ok=True)
    with open(f"_work/batch_{BATCH_NUM}_discovery.json", "w") as f:
        json.dump(state, f, indent=2)
    print(f"\nDISCOVERY done: {len(novel)} candidates, fetch_end={fetch_counter[0]}")
    for t in novel[:30]:
        print(f"  - SI {t['number']:03d} of {t['year']} (alphabet={t['letter']}) "
              f"text={t['text'][:80]}")
    return 0


def cmd_ingest(args):
    """Phase B: load discovery state, ingest a slice of candidates."""
    head_ids, head_slots = load_head()
    print(f"HEAD SI records: {len(head_ids)}; slots: {len(head_slots)}")

    discovery_path = f"_work/batch_{BATCH_NUM}_discovery.json"
    with open(discovery_path) as f:
        disc = json.load(f)
    candidates = disc["candidates"]

    # Append override targets if given (year:number:letter:text)
    for ov in args.override_target or []:
        parts = ov.split(":", 3)
        if len(parts) < 2:
            continue
        y = int(parts[0]); n = int(parts[1])
        letter = parts[2] if len(parts) >= 3 else "X"
        text = parts[3] if len(parts) >= 4 else ""
        candidates.append({"year": y, "number": n, "letter": letter, "text": text})

    # Slice
    s, e = args.slice_start, args.slice_end
    chunk = candidates[s:e]

    # Already-done check: skip slots already in head from prior ingest sub-calls
    chunk = [c for c in chunk if (c["year"], c["number"]) not in head_slots]

    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    last_fetch_t = [None]
    fetch_counter = [args.fetch_start]
    started_at = utc_now()

    results = []
    for t in chunk:
        year, number = t["year"], t["number"]
        print(f"\n=== SI {year}/{number:03d}  [{SUB_PHASE_TAG}] ===")
        status, rec, meta = process_target(
            session, year, number, SUB_PHASE_TAG, head_ids, head_slots,
            last_fetch_t, fetch_counter)
        print(f"  status: {status}")
        entry = {"year": year, "number": number, "sub_phase": SUB_PHASE_TAG,
                 "status": status, "discovery_text": t.get("text", ""),
                 "alphabet": t.get("letter", "")}
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
                        f"batch={BATCH_NUM} sub_phase={SUB_PHASE_TAG}\n")
        results.append(entry)

    slice_key = f"{s}_{e}"
    partial = {
        "batch": BATCH_NUM,
        "phase": "ingest",
        "slice": [s, e],
        "started_at": started_at,
        "completed_at": utc_now(),
        "fetch_start": args.fetch_start,
        "fetch_end": fetch_counter[0],
        "results": results,
    }
    os.makedirs("_work", exist_ok=True)
    with open(f"_work/batch_{BATCH_NUM}_slice_{slice_key}.json", "w") as f:
        json.dump(partial, f, indent=2)
    ok = sum(1 for r in results if r["status"] == "ok")
    print(f"\n==> slice {slice_key}: {ok}/{len(results)} ok, fetch_end={fetch_counter[0]}")
    return 0


def cmd_finalize(args):
    """Phase C: aggregate all slices into a final state file."""
    slices = []
    for fn in sorted(os.listdir("_work")):
        if fn.startswith(f"batch_{BATCH_NUM}_slice_") and fn.endswith(".json"):
            with open(os.path.join("_work", fn)) as f:
                slices.append(json.load(f))
    discovery_path = f"_work/batch_{BATCH_NUM}_discovery.json"
    disc = {}
    if os.path.exists(discovery_path):
        with open(discovery_path) as f:
            disc = json.load(f)
    all_results = []
    for s in slices:
        all_results.extend(s["results"])
    ok = sum(1 for r in all_results if r["status"] == "ok")
    summary = {
        "batch": BATCH_NUM,
        "phase": "phase_4_bulk",
        "sub_phase": SUB_PHASE_TAG,
        "started_at": disc.get("started_at"),
        "completed_at": utc_now(),
        "discovery_fetches": disc.get("fetches_used", 0),
        "ingest_fetches": (slices[-1]["fetch_end"] - slices[0]["fetch_start"]) if slices else 0,
        "fetches_used": (slices[-1]["fetch_end"] - disc.get("fetch_end", slices[0]["fetch_start"]) + disc.get("fetches_used", 0)) if slices else disc.get("fetches_used", 0),
        "records_written": ok,
        "targets_attempted": len(all_results),
        "results": all_results,
        "discovery_alphabets": disc.get("alphabets", []),
        "robots_sha256": disc.get("robots_sha256"),
        "novel_total_pre_keyword": disc.get("novel_total_pre_keyword"),
        "novel_kept_post_keyword": disc.get("novel_kept_post_keyword"),
        "slices": [s["slice"] for s in slices],
    }
    with open(f"_work/batch_{BATCH_NUM}_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    with open(f".batch_{BATCH_NUM}_state.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nFINAL batch {BATCH_NUM}: {ok}/{len(all_results)} ok across {len(slices)} slice(s)")
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("discovery")
    a.add_argument("--fetch-start", type=int, required=True)
    a.add_argument("--alphabets", default="PMI")

    b = sub.add_parser("ingest")
    b.add_argument("--fetch-start", type=int, required=True)
    b.add_argument("--slice-start", type=int, required=True)
    b.add_argument("--slice-end", type=int, required=True)
    b.add_argument("--override-target", action="append", default=[])

    c = sub.add_parser("finalize")

    args = ap.parse_args()
    if args.cmd == "discovery":
        return cmd_discovery(args)
    if args.cmd == "ingest":
        return cmd_ingest(args)
    if args.cmd == "finalize":
        return cmd_finalize(args)


if __name__ == "__main__":
    sys.exit(main())
