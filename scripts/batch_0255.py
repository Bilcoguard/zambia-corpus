#!/usr/bin/env python3
"""Batch 0255 - Phase 4 bulk ingest. acts_in_force alphabet=D pivot batch.

Discovery: probed /legislation?alphabet=D&nature=act this tick (raw cached
to raw/zambialii/_alphabets/legislation-alphabet-D-<ts>.html). 16 unique
/akn/zm/act/{yr}/{num} hrefs returned. After filtering against the 910
existing act IDs and dropping amendment/appropriation/supplementary/
validation/transitional/repeal tokens, 5 primary candidates remain — all
ingested here.

Picks (alpha, yr/num, title):
  D 1938/12 Debtors Act, 1938
  D 1953/46 Defamation Act, 1953
  D 1960/24 Development (United Kingdom Government) Loan Act, 1960
  D 1960/48 District Messengers Act, 1960
  D 1965/30 Diplomatic Immunities and Privileges Act, 1965

Reuses parser logic from batch_0254.py (PARSER_VERSION
0.6.0-act-zambialii-2026-04-26). Conservative 5-record batch under 8
MAX_BATCH_SIZE cap. Continues acts_in_force pivot from batches 0253/0254.
"""
import os, sys, re, time, json, hashlib, io
from datetime import datetime, timezone
import urllib.request

BATCH_NUM = "0255"
USER_AGENT = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
CRAWL = 6  # zambialii crawl-delay 5s + 1s margin
PARSER_VERSION = "0.6.0-act-zambialii-2026-04-26"
MAX_PDF_BYTES = 4_500_000

PICKS = [
    {"yr": "1938", "num": "12", "title": "Debtors Act, 1938",
     "slug": "debtors-act-1938",
     "sub_phase": "acts_in_force", "alpha": "D"},
    {"yr": "1953", "num": "46", "title": "Defamation Act, 1953",
     "slug": "defamation-act-1953",
     "sub_phase": "acts_in_force", "alpha": "D"},
    {"yr": "1960", "num": "24", "title": "Development (United Kingdom Government) Loan Act, 1960",
     "slug": "development-united-kingdom-government-loan-act-1960",
     "sub_phase": "acts_in_force", "alpha": "D"},
    {"yr": "1960", "num": "48", "title": "District Messengers Act, 1960",
     "slug": "district-messengers-act-1960",
     "sub_phase": "acts_in_force", "alpha": "D"},
    {"yr": "1965", "num": "30", "title": "Diplomatic Immunities and Privileges Act, 1965",
     "slug": "diplomatic-immunities-and-privileges-act-1965",
     "sub_phase": "acts_in_force", "alpha": "D"},
]


def fetch(url, sleep=True):
    if sleep:
        time.sleep(CRAWL)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read(), r.geturl()


def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_html_sections(html_text):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_text, "html.parser")
    h1 = soup.find("h1")
    title = h1.get_text(strip=True) if h1 else ""
    sections = []
    akn = soup.find_all(["section", "div"], class_=re.compile(r"akn-section"))
    if not akn:
        akn = soup.find_all(id=re.compile(r"sec_|chp_"))
    for sec in akn:
        num_el = sec.find(class_=re.compile(r"akn-num"))
        heading_el = sec.find(class_=re.compile(r"akn-heading"))
        num = num_el.get_text(strip=True).rstrip(".") if num_el else ""
        heading = heading_el.get_text(strip=True) if heading_el else ""
        parts = []
        for child in sec.find_all(class_=re.compile(r"akn-content|akn-intro|akn-paragraph|akn-subsection")):
            t = child.get_text(" ", strip=True)
            if t and t not in parts:
                parts.append(t)
        if not parts:
            text = sec.get_text(" ", strip=True)
            if heading and text.startswith(heading):
                text = text[len(heading):].strip()
            if num and text.startswith(num):
                text = text[len(num):].strip()
        else:
            text = "\n".join(parts)
        if num or heading or text:
            sections.append({"number": num, "heading": heading, "text": text[:5000]})
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
    except Exception:
        return "", [], 0
    if not full_text.strip():
        return "", [], 0
    lines = full_text.strip().split("\n")
    title = lines[0].strip() if lines else ""
    secs = []
    pat = re.compile(r"^(\d+)\.\s+(.+?)(?:\n|$)(.*?)(?=^\d+\.\s|\Z)", re.MULTILINE | re.DOTALL)
    for m in pat.finditer(full_text):
        secs.append({
            "number": m.group(1),
            "heading": m.group(2).strip()[:300],
            "text": m.group(3).strip()[:5000],
        })
    return title, secs, len(full_text)


def append_costs(rec):
    with open("costs.log", "a") as f:
        f.write(json.dumps(rec) + "\n")


def append_provenance(rec):
    with open("provenance.log", "a") as f:
        f.write(json.dumps(rec) + "\n")


def ingest_one(pick):
    yr = pick["yr"]; num = pick["num"]
    base = f"https://zambialii.org/akn/zm/act/{yr}/{num}"
    try:
        html_body, final_html_url = fetch(base, sleep=True)
    except Exception as e:
        return None, f"html_err_{type(e).__name__}_{getattr(e,'code','')}"
    h_sha = hashlib.sha256(html_body).hexdigest()
    append_costs({"date": utc_now()[:10], "url": base, "bytes": len(html_body),
                  "batch": BATCH_NUM, "kind": "record"})
    raw_html_path = f"raw/zambialii/act/{yr}/{yr}-{int(num):03d}.html"
    os.makedirs(os.path.dirname(raw_html_path), exist_ok=True)
    with open(raw_html_path, "wb") as f:
        f.write(html_body)

    title, sections = parse_html_sections(html_body.decode("utf-8", errors="replace"))
    final_title = title or pick["title"]
    final_url = final_html_url

    pdf_path = None
    pdf_sha = None
    if len(sections) < 2:
        pdf_match = re.search(r'href="(/akn/zm/act/[0-9]+/[0-9]+/eng@[0-9-]+/source\.pdf)"',
                              html_body.decode("utf-8", errors="replace"))
        if pdf_match:
            pdf_url = "https://zambialii.org" + pdf_match.group(1)
            try:
                pdf_body, _ = fetch(pdf_url, sleep=True)
                if len(pdf_body) > MAX_PDF_BYTES:
                    return None, f"pdf_too_large_{len(pdf_body)}"
                pdf_sha = hashlib.sha256(pdf_body).hexdigest()
                append_costs({"date": utc_now()[:10], "url": pdf_url, "bytes": len(pdf_body),
                              "batch": BATCH_NUM, "kind": "record"})
                pdf_raw_path = f"raw/zambialii/act/{yr}/{yr}-{int(num):03d}.pdf"
                with open(pdf_raw_path, "wb") as f:
                    f.write(pdf_body)
                pdf_path = pdf_raw_path
                ptitle, psecs, _ = parse_pdf_sections(pdf_body)
                if psecs:
                    sections = psecs
                if ptitle and not title:
                    final_title = ptitle
            except Exception as e:
                return None, f"pdf_err_{type(e).__name__}"

    if not sections:
        return None, "no_sections"

    rid = f"act-zm-{yr}-{int(num):03d}-{pick['slug']}"
    rec = {
        "id": rid,
        "type": "act",
        "jurisdiction": "ZM",
        "title": final_title,
        "citation": f"Act No. {int(num)} of {yr}",
        "enacted_date": None,
        "commencement_date": None,
        "in_force": True,
        "amended_by": [],
        "repealed_by": None,
        "cited_authorities": [],
        "sections": sections,
        "source_url": final_url,
        "source_hash": f"sha256:{h_sha}",
        "fetched_at": utc_now(),
        "parser_version": PARSER_VERSION,
    }
    out_path = f"records/acts/{yr}/{rid}.json"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(rec, f, indent=2, ensure_ascii=False)

    append_provenance({
        "id": rid, "source_url": final_url,
        "source_hash": f"sha256:{h_sha}", "fetched_at": rec["fetched_at"],
        "parser_version": PARSER_VERSION, "batch": BATCH_NUM,
        "raw_html": raw_html_path, "raw_pdf": pdf_path,
        "sections": len(sections),
    })
    return rec, "ok"


def main():
    # robots already re-verified during discovery this tick; do not refetch.
    results = []
    for pick in PICKS:
        rec, status = ingest_one(pick)
        results.append({
            "yr": pick["yr"], "num": pick["num"], "title": pick["title"],
            "status": status, "id": (rec["id"] if rec else None),
            "sections": (len(rec["sections"]) if rec else 0),
            "source_hash": (rec["source_hash"] if rec else None),
            "source_url": (rec["source_url"] if rec else None),
        })
        print(f"  {pick['yr']}/{pick['num']} -> {status}")

    os.makedirs("_work", exist_ok=True)
    with open(f"_work/batch_{BATCH_NUM}_summary.json", "w") as f:
        json.dump(results, f, indent=2)
    print("DONE")
    print(json.dumps([r["status"] for r in results]))


if __name__ == "__main__":
    main()
