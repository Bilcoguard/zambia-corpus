#!/usr/bin/env python3
"""
Batch 0189 — Phase 4 case_law_scz continuation (mid-2025 corridor).

Continues case_law_scz (priority_order item 5) per the batch 0188 next-tick
plan — "continue case_law_scz mid-2025 corridor (zmsc/2025/24, 23, 22, 21
per cached zmsc-index-page-1-20260424.html)" — extending to 8 targets.

Target slots (8 × 2 fetches = 16 AKN HTML + PDF) — mid-2025 ZMSC judgments
discovered via cached raw/.../zmsc-index-page-1-20260424.html and confirmed
as absent from HEAD records/judgments/zmsc/ (9 existing: 2026/1, 4, 7, 10,
scz-09-konkola pilot, 2025/25, 27, 29, 30):

  - zmsc/2025/24  OHSI v James Mataliro (APPEAL NO. 12/2025)     2025-09-19
  - zmsc/2025/23  Securities and Exchange Commission v Zambia Breweries
                                                                  2025-04-03
  - zmsc/2025/22  Chama Cheelemu v Odile Loukombo                 2025-08-19
  - zmsc/2025/21  Joseph Chanda v The People                      2025-08-20
  - zmsc/2025/20  Zambia Revenue Authority v Nestlé Zambia Ltd    2025-08-20
  - zmsc/2025/19  Roanbeat Investment v MTN (Zambia) Limited      2025-08-13
  - zmsc/2025/18  Emmanuel Tumba v Zambia Bata Shoe Company Plc   2025-08-14
  - zmsc/2025/17  Ronald Kaoma Chitotela v Anti-Corruption Commission
                                                                  2025-08-13

Per batch 0182/0186 operational note: sandbox bash-tool has a 45s hard
ceiling. With zambialii.org 5s crawl-delay + per-fetch HTTP + PDF parse,
each record takes ~12-15s. 8 records therefore sliced into 2+2+2+2 via
--slice=START:END with a _work/batch_0189_summary.json resume checkpoint.
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

BATCH_NUM = "0189"
USER_AGENT = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
PARSER_VERSION = "0.5.0"
CRAWL_DELAY_SECONDS = 6  # 5s per robots + 1s margin

# (year, number, expected_date_slug) tuples matching the ZambiaLII
# /akn/zm/judgment/zmsc/{year}/{num}/eng@{date} URL pattern.
TARGETS = [
    (2025, 24, "2025-09-19"),
    (2025, 23, "2025-04-03"),
    (2025, 22, "2025-08-19"),
    (2025, 21, "2025-08-20"),
    (2025, 20, "2025-08-20"),
    (2025, 19, "2025-08-13"),
    (2025, 18, "2025-08-14"),
    (2025, 17, "2025-08-13"),
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


def parse_pdf_text(pdf_bytes):
    """Extract full text + simple paragraph segmentation from a judgment PDF."""
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
    # Paragraph segmentation — numbered paragraphs "1. ...", "2. ..."
    # are standard in SCZ judgments; fall back to page-breaks otherwise.
    paras = []
    para_re = re.compile(r"^\s*(\d{1,3})\.\s+(.+?)(?=^\s*\d{1,3}\.\s|\Z)",
                         re.MULTILINE | re.DOTALL)
    for m in para_re.finditer(full_text):
        num = m.group(1)
        body = m.group(2).strip()
        # cap very long paragraphs to keep JSON sane
        paras.append({"number": num, "text": body[:6000]})
    if not paras:
        # fallback — chunk by double newlines
        chunks = [c.strip() for c in re.split(r"\n\s*\n", full_text) if c.strip()]
        for i, c in enumerate(chunks[:200], 1):
            paras.append({"number": str(i), "text": c[:6000]})
    return full_text, paras


def parse_metadata(html_bytes):
    """Extract title, parties, judges, citation, court, date, pdf_url."""
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

    # Strip the trailing "– ZambiaLII" / publisher suffix if present
    title = re.sub(r"\s*[–-]\s*ZambiaLII\s*$", "", title)

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

    # Neutral citation from title, e.g. "[2026] ZMSC 10"
    citation = ""
    m = re.search(r"\[(\d{4})\]\s+ZMSC\s+(\d+)", title)
    if m:
        citation = f"[{m.group(1)}] ZMSC {m.group(2)}"

    # Case number / appeal docket from title, e.g. "(Appeal No. 22/2025)"
    case_number = ""
    m = re.search(r"\(([^)]*(?:Appeal|SCZ)[^)]*)\)", title)
    if m:
        case_number = m.group(1).strip()

    # Delivery date — strip from the trailing "(DD Month YYYY)" bracket
    delivery_date = ""
    m = re.search(r"\((\d{1,2}\s+[A-Za-z]+\s+\d{4})\)\s*$", title)
    if m:
        try:
            dt = datetime.strptime(m.group(1), "%d %B %Y")
            delivery_date = dt.strftime("%Y-%m-%d")
        except Exception:
            pass

    # Parties: split on " v " or " v. "
    parties = {"appellant": [], "respondent": []}
    head = title
    # Drop bracketed metadata from the case heading
    head = re.sub(r"\s*\([^)]+\)", "", head).strip()
    # Drop the "[YYYY] ZMSC NN" suffix
    head = re.sub(r"\s*\[\d{4}\]\s+ZMSC\s+\d+.*$", "", head).strip()
    parts = re.split(r"\s+v\.?\s+", head, maxsplit=1)
    if len(parts) == 2:
        parties["appellant"] = [parts[0].strip()]
        parties["respondent"] = [parts[1].strip()]

    # Judges — search the full text of the page for "CORAM" / "Before"
    body_text = soup.get_text(" ", strip=False)
    judges = []
    m = re.search(r"(?:CORAM|BEFORE)\s*:?\s*([A-Z][A-Za-z,.\-\s&]{5,200}?)(?:\n|\.\s|JJS\.?\s|$)",
                  body_text)
    if m:
        raw_panel = m.group(1).strip()
        # not reliable — leave judges empty if parse looks dicey
        if len(raw_panel) < 180 and "," in raw_panel:
            judges = [j.strip() for j in raw_panel.split(",") if j.strip()]

    return {
        "title": title,
        "pdf_url": pdf_url,
        "citation": citation,
        "case_number": case_number,
        "delivery_date": delivery_date,
        "parties": parties,
        "judges": judges,
    }


def build_record(year, number, date_slug, meta, body_text, paragraphs,
                 source_url, source_hash, fetched_at, alternates):
    # Build a slug of parties (first-word-of-appellant-v-first-word-of-respondent)
    parties = meta.get("parties", {})
    ap = (parties.get("appellant") or [""])[0]
    rp = (parties.get("respondent") or [""])[0]
    ap_word = slugify(ap).split("-")[0] if ap else "x"
    rp_word = slugify(rp).split("-")[0] if rp else "x"
    party_slug = f"{ap_word}-v-{rp_word}"
    record_id = f"judgment-zm-{year}-zmsc-{number:02d}-{party_slug}"
    if len(record_id) > 120:
        record_id = record_id[:120]

    return {
        "id": record_id,
        "type": "judgment",
        "jurisdiction": "ZM",
        "title": meta["title"],
        "citation": meta.get("citation") or f"[{year}] ZMSC {number}",
        "case_number": meta.get("case_number") or "",
        "court": "Supreme Court of Zambia",
        "delivery_date": meta.get("delivery_date") or date_slug,
        "parties": meta.get("parties") or {"appellant": [], "respondent": []},
        "judges": meta.get("judges") or [],
        "cited_authorities": [],
        "paragraphs": paragraphs,
        "source_url": source_url,
        "source_hash": f"sha256:{source_hash}",
        "fetched_at": fetched_at,
        "parser_version": PARSER_VERSION,
        "alternate_sources": alternates,
        "rights_notice": (
            "Publisher: ZambiaLII (African Legal Information Institute). "
            "Reproduction and retention by Kate Weston Legal Practitioners is "
            "under the fair-dealing exceptions of the Copyright and Performance "
            "Rights Act, Cap. 406 of the Laws of Zambia, for legal research and "
            "professional commentary. Judgments of the Supreme Court of Zambia "
            "are public acts of the state and are cited for their legal "
            "authority only."
        ),
        "sensitive_data_categories": ["none"],
    }


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


def process_target(session, year, number, date_slug, head_ids, head_slots,
                   last_fetch_t, fetch_counter):
    akn_url = f"https://zambialii.org/akn/zm/judgment/zmsc/{year}/{number}/eng@{date_slug}"
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

    meta = parse_metadata(html_bytes)
    if not meta["pdf_url"]:
        return f"no_pdf_link:final={final_url}", None, None
    if not meta["title"]:
        return "no_title", None, None

    start_pdf = utc_now()
    try:
        rp = fetch(meta["pdf_url"], session, last_fetch_t)
    except Exception as e:
        return f"fetch_pdf_error:{type(e).__name__}:{e}", None, None
    fetch_counter[0] += 1
    if rp.status_code != 200:
        return f"pdf_http_{rp.status_code}", None, None
    pdf_bytes = rp.content
    pdf_hash = hashlib.sha256(pdf_bytes).hexdigest()

    body_text, paragraphs = parse_pdf_text(pdf_bytes)
    if not paragraphs:
        return "pdf_parse_empty", None, None

    # Write raw files
    raw_dir = os.path.join(WORKSPACE, "raw", "zambialii", "judgments", "zmsc", str(year))
    os.makedirs(raw_dir, exist_ok=True)
    party_slug = slugify(meta["title"])[:60]
    stem = f"judgment-zm-{year}-zmsc-{number:02d}-{party_slug}"[:120]
    raw_html = os.path.join(raw_dir, stem + ".html")
    raw_pdf = os.path.join(raw_dir, stem + ".pdf")
    with open(raw_html, "wb") as f:
        f.write(html_bytes)
    with open(raw_pdf, "wb") as f:
        f.write(pdf_bytes)

    record = build_record(
        year=year, number=number, date_slug=date_slug, meta=meta,
        body_text=body_text, paragraphs=paragraphs,
        source_url=meta["pdf_url"], source_hash=pdf_hash, fetched_at=start_pdf,
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
    # CHECK2: year/number slot collision within ZMSC namespace
    if (year, number) in head_slots:
        return f"check2_fail_slot_clash:{year}/{number}", None, None
    # CHECK3: on-disk hash matches source_hash
    with open(raw_pdf, "rb") as f:
        if hashlib.sha256(f.read()).hexdigest() != pdf_hash:
            return "check3_fail_hash_mismatch", None, None
    # CHECK4: cross-refs empty (judgments cite but we're not extracting this batch)
    if record.get("cited_authorities"):
        ok_refs = True
        for cref in record["cited_authorities"]:
            if cref not in head_ids:
                ok_refs = False
                break
        if not ok_refs:
            return "check4_fail_crossref_unresolved", None, None
    # CHECK5: required fields
    for k in ("id", "type", "jurisdiction", "title", "citation", "paragraphs",
              "source_url", "source_hash", "fetched_at", "parser_version",
              "court"):
        if record.get(k) in (None, "", []):
            return f"check5_fail_missing:{k}", None, None

    out_dir = os.path.join(WORKSPACE, "records", "judgments", "zmsc", str(year))
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{record['id']}.json")
    with open(out_path, "w") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)

    today = datetime.now(UTC).strftime("%Y-%m-%d")
    with open("costs.log", "a") as f:
        f.write(json.dumps({"date": today, "url": akn_url,
                            "bytes": len(html_bytes),
                            "batch": BATCH_NUM, "fetch_n": fetch_counter[0] - 1}) + "\n")
        f.write(json.dumps({"date": today, "url": meta["pdf_url"],
                            "bytes": len(pdf_bytes),
                            "batch": BATCH_NUM, "fetch_n": fetch_counter[0]}) + "\n")
    with open("provenance.log", "a") as f:
        f.write(json.dumps({"request_url": akn_url, "status": 200,
                            "sha256": html_hash, "bytes": len(html_bytes),
                            "started_at": start_html, "batch": BATCH_NUM,
                            "parser_version": PARSER_VERSION}) + "\n")
        f.write(json.dumps({"request_url": meta["pdf_url"], "status": 200,
                            "sha256": pdf_hash, "bytes": len(pdf_bytes),
                            "started_at": start_pdf, "batch": BATCH_NUM,
                            "parser_version": PARSER_VERSION}) + "\n")

    head_slots.add((year, number))
    head_ids.add(record["id"])
    return "ok", record, {
        "akn_url": akn_url, "pdf_url": meta["pdf_url"],
        "html_hash": html_hash, "pdf_hash": pdf_hash,
        "html_bytes": len(html_bytes), "pdf_bytes": len(pdf_bytes),
        "raw_html": raw_html, "raw_pdf": raw_pdf,
        "record_path": out_path, "paragraphs": len(paragraphs),
        "title": meta["title"], "citation": record["citation"],
    }


def load_prior_state():
    path = f"_work/batch_{BATCH_NUM}_summary.json"
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slice", default=f"0:{len(TARGETS)}",
                    help="Target slice START:END (e.g. 0:2 then 2:4)")
    args = ap.parse_args()
    start_idx, end_idx = [int(x) for x in args.slice.split(":")]
    slice_targets = TARGETS[start_idx:end_idx]

    head_ids = set()
    head_slots = set()
    # Walk existing judgments records to build collision sets
    for root, dirs, files in os.walk(os.path.join(WORKSPACE, "records", "judgments")):
        for fn in files:
            if fn.endswith(".json"):
                rid = fn[:-5]
                head_ids.add(rid)
                m = re.match(r"judgment-zm-(\d{4})-zmsc-(\d+)", rid)
                if m:
                    head_slots.add((int(m.group(1)), int(m.group(2))))
    print(f"HEAD judgment records: {len(head_ids)}; ZMSC slots: {len(head_slots)}")

    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT

    last_fetch_t = [None]
    fetch_counter = [0]
    results = []
    deadline = time.time() + 38  # internal 38s soft deadline (bash hard=45s)
    started_at = utc_now()

    for (year, number, date_slug) in slice_targets:
        if time.time() > deadline:
            results.append({"year": year, "number": number,
                            "date_slug": date_slug, "status": "deadline_skip"})
            continue
        print(f"\n=== ZMSC {year}/{number:02d} @ {date_slug} ===")
        status, rec, meta = process_target(
            session, year, number, date_slug, head_ids, head_slots,
            last_fetch_t, fetch_counter)
        print(f"  status: {status}")
        entry = {"year": year, "number": number, "date_slug": date_slug,
                 "status": status}
        if rec is not None:
            entry.update({
                "record_id": rec["id"],
                "paragraphs": meta["paragraphs"],
                "title": meta["title"],
                "citation": meta["citation"],
                "pdf_url": meta["pdf_url"],
                "pdf_hash": meta["pdf_hash"],
                "pdf_bytes": meta["pdf_bytes"],
                "raw_pdf": meta["raw_pdf"],
                "record_path": meta["record_path"],
            })
        else:
            with open("gaps.md", "a") as f:
                f.write(f"- [{utc_now()}] zmsc/{year}/{number:02d}@{date_slug} "
                        f"status={status} batch={BATCH_NUM}\n")
        results.append(entry)

    prior = load_prior_state()
    if prior:
        merged_results = list(prior.get("results", []))
        merged_fetches = prior.get("fetches_used", 0) + fetch_counter[0]
        started_at = prior.get("started_at", started_at)
        seen = {(r["year"], r["number"]) for r in merged_results}
        for r in results:
            if (r["year"], r["number"]) not in seen:
                merged_results.append(r)
    else:
        merged_results = results
        merged_fetches = fetch_counter[0]

    ok_count = sum(1 for r in merged_results if r["status"] == "ok")
    summary = {
        "batch": BATCH_NUM,
        "phase": "phase_4_bulk",
        "sub_phase": "case_law_scz",
        "started_at": started_at,
        "completed_at": utc_now(),
        "fetches_used": merged_fetches,
        "records_written": ok_count,
        "targets_attempted": len(merged_results),
        "results": merged_results,
    }
    os.makedirs("_work", exist_ok=True)
    with open(f"_work/batch_{BATCH_NUM}_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    with open(f".batch_{BATCH_NUM}_state.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\n==> batch {BATCH_NUM} slice {args.slice}: "
          f"slice_attempted={len(results)}, "
          f"total_ok={ok_count}/{len(merged_results)}, "
          f"slice_fetches={fetch_counter[0]}, cum_fetches={merged_fetches}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
