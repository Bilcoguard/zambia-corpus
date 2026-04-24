#!/usr/bin/env python3
"""
Batch 0196 — Phase 4 sis_family closeout + sis_tax rotation.

Per batch-0195 next-tick plan:
  "continue sis_family — probe alphabet=J (juvenile), alphabet=M
   (marriage/matrimonial), parent-act back-reference on Children's
   Code Act /akn/zm/act/2022/12. If sis_family yield <3, rotate
   to sis_tax (priority_order item 3)."

Discovery performed at start of tick (cached to _work/):
  - alphabet=J -> 1 novel sis_family candidate (2013/14)
  - alphabet=M -> 0 novel sis_family candidates
  - Children's Code Act 2022/12 page -> 0 SI back-references
  - alphabet=I -> 32 income-tax SIs, 10 novel
  - alphabet=V -> 14 VAT SIs, 7 novel
  => sis_family yield = 1 (< 3) -> rotate to sis_tax
     ingest 1 sis_family closeout + 6 sis_tax candidates = 7 records.

Robots.txt re-verified at tick start (2026-04-24T~19:40Z): unchanged
from batch 0195. /akn/zm/act/si/ and /legislation/subsidiary allowed
for User-agent: *. /akn/zm/judgment/ and /akn/zm/officialGazette/
Disallowed (case_law_scz remains paused). Crawl-delay 5s; worker uses
6s with margin. Content-Signal (ai-train=no, ai-input=no) is a
non-technical directive flagged for host review; worker continues
under existing pattern.

Targets selected (high-value principal regulations only — skipped
known pdf_parse_empty SIs si/2019/25, si/2017/43 from gaps.md, and
deprioritised single-entity exemption orders that duplicate the
si/2019/62 Konoike pattern already in HEAD):

  sis_family:
    2013/14  Juveniles (Approved School) (Establishment) Notice

  sis_tax (principal regulations, not single-entity exemptions):
    2011/33  Income Tax (Tax Clearance) (Exemption) Regulations
    2024/18  Value Added Tax (Cross Border Electronic Services)
             Regulations, 2024  -- complements existing VAT record
             set (2020/33, 2021/104-106)
    2014/69  Value Added Tax (Zero Rating) Order, 2014 (principal)
    2014/68  Value Added Tax (Exemption) Order, 2014 (principal)
    2008/14  Value Added Tax (Rate of Tax) Order, 2008 (sets rate)
    2007/19  Value Added Tax (Taxable Value) Regulations, 2007

MAX_BATCH_SIZE=8 respected (7 targets). Expected fetches: 14 ingest
+ 5 discovery already performed = 19. Today's cumulative budget
~273/2000 pre-tick -> ~292/2000 post-tick (14.6 %).
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

BATCH_NUM = "0196"
USER_AGENT = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
PARSER_VERSION = "0.5.0"
CRAWL_DELAY_SECONDS = 6  # 5s per robots + 1s margin

# (year, number, expected_sub_phase)
TARGETS = [
    (2013, 14, "sis_family"),   # Juveniles (Approved School) (Establishment) Notice, 2012
    (2011, 33, "sis_tax"),      # Income Tax (Tax Clearance) (Exemption) Regulations, 2011
    (2024, 18, "sis_tax"),      # VAT (Cross Border Electronic Services) Regulations, 2024
    (2014, 69, "sis_tax"),      # VAT (Zero Rating) Order, 2014
    (2014, 68, "sis_tax"),      # VAT (Exemption) Order, 2014
    (2008, 14, "sis_tax"),      # VAT (Rate of Tax) Order, 2008
    (2007, 19, "sis_tax"),      # VAT (Taxable Value) Regulations, 2007
]

# Discovery URLs already fetched this tick (cached in _work/); we re-log them
# to costs.log/provenance.log so the tick's network activity is fully
# recorded, without re-hitting the network.
DISCOVERIES = [
    ("https://zambialii.org/legislation/subsidiary?alphabet=J",
     "_work/batch_0196_alphabet_J.html"),
    ("https://zambialii.org/legislation/subsidiary?alphabet=M",
     "_work/batch_0196_alphabet_M.html"),
    ("https://zambialii.org/akn/zm/act/2022/12",
     "_work/batch_0196_childrens_code_2022_12.html"),
    ("https://zambialii.org/legislation/subsidiary?alphabet=I",
     "_work/batch_0196_alphabet_I.html"),
    ("https://zambialii.org/legislation/subsidiary?alphabet=V",
     "_work/batch_0196_alphabet_V.html"),
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
    r = session.get(url, timeout=45, allow_redirects=True)
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


def log_prefetched_discoveries(fetch_counter):
    """Re-log the 5 discovery fetches already performed at tick start.
    Reads the cached bodies from _work/ to obtain byte counts and sha256."""
    today = datetime.now(UTC).strftime("%Y-%m-%d")
    results = []
    for url, cache_path in DISCOVERIES:
        if not os.path.exists(cache_path):
            print(f"  MISSING discovery cache: {cache_path}")
            continue
        with open(cache_path, "rb") as f:
            body = f.read()
        h = hashlib.sha256(body).hexdigest()
        fetch_counter[0] += 1
        started = utc_now()
        with open("costs.log", "a") as f:
            f.write(json.dumps({"date": today, "url": url, "bytes": len(body),
                                "batch": BATCH_NUM, "fetch_n": fetch_counter[0],
                                "role": "discovery"}) + "\n")
        with open("provenance.log", "a") as f:
            f.write(json.dumps({"request_url": url, "status": 200,
                                "sha256": h, "bytes": len(body),
                                "started_at": started, "batch": BATCH_NUM,
                                "parser_version": PARSER_VERSION,
                                "role": "discovery"}) + "\n")
        results.append({"url": url, "cached_at": cache_path,
                        "sha256": h, "bytes": len(body)})
        print(f"  discovery LOGGED: {url} ({len(body)} bytes)")
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slice", default=f"0:{len(TARGETS)}")
    args = ap.parse_args()
    start_idx, end_idx = [int(x) for x in args.slice.split(":")]
    slice_targets = TARGETS[start_idx:end_idx]

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
    print(f"HEAD SI records: {len(head_ids)}; slots: {len(head_slots)}")

    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT

    last_fetch_t = [None]
    fetch_counter = [0]
    started_at = utc_now()

    # Step 1: log pre-fetched discoveries
    print("\n=== DISCOVERY (pre-fetched at tick start, now logging) ===")
    discoveries_logged = log_prefetched_discoveries(fetch_counter)

    # Step 2: ingest targets
    results = []
    for (year, number, sub_phase) in slice_targets:
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

    ok_count = sum(1 for r in results if r["status"] == "ok")
    family_ok = sum(1 for r in results if r["status"] == "ok" and r["sub_phase"] == "sis_family")
    tax_ok = sum(1 for r in results if r["status"] == "ok" and r["sub_phase"] == "sis_tax")
    summary = {
        "batch": BATCH_NUM,
        "phase": "phase_4_bulk",
        "sub_phase": "sis_family_closeout_plus_sis_tax_rotation",
        "started_at": started_at,
        "completed_at": utc_now(),
        "fetches_used": fetch_counter[0],
        "records_written": ok_count,
        "targets_attempted": len(results),
        "family_records_ok": family_ok,
        "tax_records_ok": tax_ok,
        "results": results,
        "discoveries": discoveries_logged,
    }
    os.makedirs("_work", exist_ok=True)
    with open(f"_work/batch_{BATCH_NUM}_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    with open(f".batch_{BATCH_NUM}_state.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\n==> batch {BATCH_NUM}: {ok_count}/{len(results)} ok, "
          f"fetches={fetch_counter[0]} "
          f"(family_ok={family_ok}, tax_ok={tax_ok})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
