#!/usr/bin/env python3
"""Batch 0254 - Phase 4 bulk ingest. Continuation of pivot to acts_in_force.

Drains 5 of the 7 alphabet=C primary residuals identified at the close of
batch 0253. The two largest residuals (Constitution of Zambia 1996/17 and
Citizens Economic Empowerment 2006/9) are deferred to dedicated batches
because of expected size; every other primary act in the alphabet=C
residual set is attempted here.

Picks (alpha, yr/num, title):
  C 1926/20 Clubs Registration Act, 1926
  C 1963/64 Central African Power Corporation Act, 1963
  C 1964/7  Central African Civil Air Transport Act, 1964
  C 1968/18 Calculation of Taxes Act, 1968
  C 1981/3  Central Committee Act, 1981

Reuses parser logic and structure from batch_0253.py (PARSER_VERSION
0.6.0-act-zambialii-2026-04-26). Conservative 5-record batch leaves
headroom under the 8 MAX_BATCH_SIZE cap.
"""
import os, sys, re, time, json, hashlib, io
from datetime import datetime, timezone
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import urllib.request

BATCH_NUM = "0254"
USER_AGENT = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
CRAWL = 6  # zambialii crawl-delay 5s + 1s margin
PARSER_VERSION = "0.6.0-act-zambialii-2026-04-26"

PICKS = [
    {"yr": "1926", "num": "20", "title": "Clubs Registration Act, 1926",
     "slug": "clubs-registration-act-1926",
     "sub_phase": "acts_in_force", "alpha": "C"},
    {"yr": "1963", "num": "64", "title": "Central African Power Corporation Act, 1963",
     "slug": "central-african-power-corporation-act-1963",
     "sub_phase": "acts_in_force", "alpha": "C"},
    {"yr": "1964", "num": "7", "title": "Central African Civil Air Transport Act, 1964",
     "slug": "central-african-civil-air-transport-act-1964",
     "sub_phase": "acts_in_force", "alpha": "C"},
    {"yr": "1968", "num": "18", "title": "Calculation of Taxes Act, 1968",
     "slug": "calculation-of-taxes-act-1968",
     "sub_phase": "acts_in_force", "alpha": "C"},
    {"yr": "1981", "num": "3", "title": "Central Committee Act, 1981",
     "slug": "central-committee-act-1981",
     "sub_phase": "acts_in_force", "alpha": "C"},
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
                if len(pdf_body) > 4_500_000:
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
    rb, _ = fetch("https://zambialii.org/robots.txt", sleep=True)
    rh = hashlib.sha256(rb).hexdigest()
    append_costs({"date": utc_now()[:10], "url": "https://zambialii.org/robots.txt",
                  "bytes": len(rb), "batch": BATCH_NUM, "kind": "robots"})
    print(f"robots sha256: {rh[:16]} (expect fce67b697ee4ef44)")

    results = []
    for pick in PICKS:
        rec, status = ingest_one(pick)
        results.append({
            "yr": pick["yr"], "num": pick["num"], "title": pick["title"],
            "status": status, "id": (rec["id"] if rec else None),
        })
        print(f"  {pick['yr']}/{pick['num']} -> {status}")

    os.makedirs("_work", exist_ok=True)
    with open(f"_work/batch_{BATCH_NUM}_summary.json", "w") as f:
        json.dump(results, f, indent=2)
    print("DONE")
    print(json.dumps([r["status"] for r in results]))


if __name__ == "__main__":
    main()
