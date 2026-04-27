#!/usr/bin/env python3
"""Batch 0288 - Phase 4 bulk ingest. acts_in_force chronological-first.

Per next-tick plan in batch 0287:
- Refreshed pool inherited from _work/batch_0287_remaining.json (14 items).
- Sweep next 8 chronologically-earliest from refreshed pool.
- Robots.txt re-verified at start of tick (sha256 unchanged).

First 8 chronological from inherited pool:
  2021/53 Appropriation Act, 2021                                       (alpha A, fiscal)
  2022/7  Supplementary Appropriation (2022) Act, 2022                  (alpha S, fiscal)
  2022/30 Appropriation Act, 2022                                       (alpha A, fiscal)
  2023/10 Supplementary Appropriation (2023) Act, 2023                  (alpha S, fiscal)
  2023/18 Public-Private Partnership Act, 2023                          (alpha P, non-fiscal)
  2023/29 Appropriation Act, 2023                                       (alpha A, fiscal)
  2024/9  Supplementary Appropriation Act, 2024                         (alpha S, fiscal)
  2024/20 Supplementary Appropriation (2024) (No. 2) Act, 2024          (alpha S, fiscal)

NOTE: 7/8 fiscal-series, plus 1 substantive non-fiscal Act (Public-Private
Partnership 2023). Yield expected to be ~87-100%. Some "Appropriation" PDFs
in this era can exceed MAX_PDF_BYTES (4.5 MB); those will be deferred to
the oversize-PDF host-side queue per established pattern.

Pre-flight on-disk dedup: each pick verified absent via slug_glob_exists on
records/acts/<yr>/act-zm-<yr>-<num:03d>-*.json. None of the 8 are present.

Reuses parser from batches 0269..0287 (PARSER_VERSION 0.6.0-act-zambialii-2026-04-26).
"""
import os, sys, re, time, json, hashlib, io, glob
from datetime import datetime, timezone
import urllib.request

BATCH_NUM = "0288"
USER_AGENT = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
CRAWL = 6
PARSER_VERSION = "0.6.0-act-zambialii-2026-04-26"
MAX_PDF_BYTES = 4_500_000

PICKS = [
    {"yr":"2021","num":"53","title":"Appropriation Act, 2021",
     "slug":"appropriation-act","sub_phase":"acts_in_force","alpha":"A"},
    {"yr":"2022","num":"7","title":"Supplementary Appropriation (2022) Act, 2022",
     "slug":"supplementary-appropriation-2022-act","sub_phase":"acts_in_force","alpha":"S"},
    {"yr":"2022","num":"30","title":"Appropriation Act, 2022",
     "slug":"appropriation-act","sub_phase":"acts_in_force","alpha":"A"},
    {"yr":"2023","num":"10","title":"Supplementary Appropriation (2023) Act, 2023",
     "slug":"supplementary-appropriation-2023-act","sub_phase":"acts_in_force","alpha":"S"},
    {"yr":"2023","num":"18","title":"Public-Private Partnership Act, 2023",
     "slug":"public-private-partnership-act","sub_phase":"acts_in_force","alpha":"P"},
    {"yr":"2023","num":"29","title":"Appropriation Act, 2023",
     "slug":"appropriation-act","sub_phase":"acts_in_force","alpha":"A"},
    {"yr":"2024","num":"9","title":"Supplementary Appropriation Act, 2024",
     "slug":"supplementary-appropriation-act","sub_phase":"acts_in_force","alpha":"S"},
    {"yr":"2024","num":"20","title":"Supplementary Appropriation (2024) (No. 2) Act, 2024",
     "slug":"supplementary-appropriation-2024-no-2-act","sub_phase":"acts_in_force","alpha":"S"},
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


def slug_glob_exists(yr, num):
    """Slug-suffix-agnostic on-disk dedup."""
    pat = f"records/acts/{yr}/act-zm-{yr}-{int(num):03d}-*.json"
    return bool(glob.glob(pat))


def ingest_one(pick):
    yr = pick["yr"]; num = pick["num"]
    if slug_glob_exists(yr, num):
        return None, "duplicate_existing_pre_flight"
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
    indices = None
    if len(sys.argv) > 1:
        a = sys.argv[1]
        if ":" in a:
            i,j = a.split(":")
            i = int(i) if i else 0
            j = int(j) if j else len(PICKS)
            indices = list(range(i,j))
        else:
            indices = [int(a)]
    else:
        indices = list(range(len(PICKS)))

    results = []
    for idx in indices:
        pick = PICKS[idx]
        rec, status = ingest_one(pick)
        results.append({
            "idx": idx,
            "yr": pick["yr"], "num": pick["num"], "title": pick["title"],
            "alpha": pick["alpha"],
            "status": status, "id": (rec["id"] if rec else None),
            "sections": (len(rec["sections"]) if rec else 0),
            "source_hash": (rec["source_hash"] if rec else None),
            "source_url": (rec["source_url"] if rec else None),
        })
        print(f"  [{idx}] {pick['yr']}/{pick['num']} -> {status}", flush=True)

    os.makedirs("_work", exist_ok=True)
    suffix = sys.argv[1].replace(":","_") if len(sys.argv) > 1 else "all"
    with open(f"_work/batch_{BATCH_NUM}_run_{suffix}.json", "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
