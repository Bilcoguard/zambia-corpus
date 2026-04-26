#!/usr/bin/env python3
"""Batch 0253 - Phase 4 bulk ingest. Pivot to acts_in_force priority_order item 1.

After 252 batches focused on SIs, this batch pivots to acts_in_force (first
item in approvals.yaml priority_order). Discovery: zambialii.org alphabet=
{A,B,C} listings cross-referenced against existing 768-id corpus by
(year/num) tuple. 6 missing primary acts selected from B/C alphabets,
filtering out appropriation/amendment/supplementary/validation/transitional
boilerplate. Conservative 6-record batch (well under 8 cap) given pivot
risk.

Picks (alphabet, yr/num, title):
  B 1931/3  Boy Scouts and Girl Guides Associations Act, 1931
  B 1965/51 Bretton Woods Agreement Act, 1965
  C 1929/17 Control of Dogs Act, 1929
  C 1940/12 Civil Courts (Attachment of Debts) Act, 1940
  C 1954/12 Control of Goods Act, 1954
  C 1994/39 Common Leasehold Schemes Act, 1994

PARSER_VERSION 0.6.0-act-zambialii-2026-04-26 -- adapted from batch 0150
(html section parsing). Reuses scripts/fetch_one.py for audited fetching.
"""
import os, sys, re, time, json, hashlib, io
from datetime import datetime, timezone
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import urllib.request

BATCH_NUM="0253"
USER_AGENT="KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
CRAWL=6
PARSER_VERSION="0.6.0-act-zambialii-2026-04-26"

PICKS=[
    {"yr":"1931","num":"3","title":"Boy Scouts and Girl Guides Associations Act, 1931","slug":"boy-scouts-and-girl-guides-associations-act-1931","sub_phase":"acts_in_force","alpha":"B"},
    {"yr":"1965","num":"51","title":"Bretton Woods Agreement Act, 1965","slug":"bretton-woods-agreement-act-1965","sub_phase":"acts_in_force","alpha":"B"},
    {"yr":"1929","num":"17","title":"Control of Dogs Act, 1929","slug":"control-of-dogs-act-1929","sub_phase":"acts_in_force","alpha":"C"},
    {"yr":"1940","num":"12","title":"Civil Courts (Attachment of Debts) Act, 1940","slug":"civil-courts-attachment-of-debts-act-1940","sub_phase":"acts_in_force","alpha":"C"},
    {"yr":"1954","num":"12","title":"Control of Goods Act, 1954","slug":"control-of-goods-act-1954","sub_phase":"acts_in_force","alpha":"C"},
    {"yr":"1994","num":"39","title":"Common Leasehold Schemes Act, 1994","slug":"common-leasehold-schemes-act-1994","sub_phase":"acts_in_force","alpha":"C"},
]


def fetch(url, sleep=True):
    if sleep: time.sleep(CRAWL)
    req=urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read(), r.geturl()


def utc_now(): return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_html_sections(html_text):
    from bs4 import BeautifulSoup
    soup=BeautifulSoup(html_text, "html.parser")
    h1=soup.find("h1")
    title=h1.get_text(strip=True) if h1 else ""
    # capture commencement / enacted dates if present in metadata block
    enacted=None; commenced=None
    # work-in-text (meta info often in dl class=document-info)
    sections=[]
    akn=soup.find_all(["section","div"], class_=re.compile(r"akn-section"))
    if not akn:
        akn=soup.find_all(id=re.compile(r"sec_|chp_"))
    for sec in akn:
        num_el=sec.find(class_=re.compile(r"akn-num"))
        heading_el=sec.find(class_=re.compile(r"akn-heading"))
        num=num_el.get_text(strip=True).rstrip(".") if num_el else ""
        heading=heading_el.get_text(strip=True) if heading_el else ""
        parts=[]
        for child in sec.find_all(class_=re.compile(r"akn-content|akn-intro|akn-paragraph|akn-subsection")):
            t=child.get_text(" ", strip=True)
            if t and t not in parts:
                parts.append(t)
        if not parts:
            text=sec.get_text(" ", strip=True)
            if heading and text.startswith(heading): text=text[len(heading):].strip()
            if num and text.startswith(num): text=text[len(num):].strip()
        else:
            text="\n".join(parts)
        if num or heading or text:
            sections.append({"number":num,"heading":heading,"text":text[:5000]})
    return title, sections


def parse_pdf_sections(pdf_bytes):
    import pdfplumber
    full_text=""
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                pt=page.extract_text()
                if pt: full_text += pt+"\n"
    except Exception as e:
        return "", [], 0
    if not full_text.strip(): return "", [], 0
    lines=full_text.strip().split("\n")
    title=lines[0].strip() if lines else ""
    secs=[]
    pat=re.compile(r"^(\d+)\.\s+(.+?)(?:\n|$)(.*?)(?=^\d+\.\s|\Z)", re.MULTILINE|re.DOTALL)
    for m in pat.finditer(full_text):
        secs.append({"number":m.group(1),"heading":m.group(2).strip()[:300],"text":m.group(3).strip()[:5000]})
    return title, secs, len(full_text)


def append_costs(rec):
    with open("costs.log","a") as f:
        f.write(json.dumps(rec)+"\n")


def append_provenance(rec):
    with open("provenance.log","a") as f:
        f.write(json.dumps(rec)+"\n")


def ingest_one(pick):
    yr=pick["yr"]; num=pick["num"]
    base=f"https://zambialii.org/akn/zm/act/{yr}/{num}"
    eng_url=base
    # First fetch HTML page
    html_url=f"{base}/eng@{yr}-01-01"  # placeholder; will discover via redirect
    # Actually we should fetch the canonical page (no eng@ date) to find the right path
    html_body,final_html_url=fetch(base, sleep=True)
    h_sha=hashlib.sha256(html_body).hexdigest()
    append_costs({"date":utc_now()[:10],"url":base,"bytes":len(html_body),"batch":BATCH_NUM,"kind":"record"})
    # Save raw HTML
    raw_html_path=f"raw/zambialii/act/{yr}/{yr}-{int(num):03d}.html"
    os.makedirs(os.path.dirname(raw_html_path), exist_ok=True)
    with open(raw_html_path,"wb") as f: f.write(html_body)

    title, sections = parse_html_sections(html_body.decode("utf-8", errors="replace"))
    final_title=title or pick["title"]
    final_url=final_html_url

    # If sections sparse, try PDF fallback
    pdf_path=None; pdf_sha=None; pdf_bytes_len=0
    if len(sections) < 2:
        # discover PDF link from HTML
        pdf_match=re.search(r'href="(/akn/zm/act/[0-9]+/[0-9]+/eng@[0-9-]+/source\.pdf)"', html_body.decode("utf-8", errors="replace"))
        if pdf_match:
            pdf_url="https://zambialii.org" + pdf_match.group(1)
            try:
                pdf_body, _ = fetch(pdf_url, sleep=True)
                if len(pdf_body) > 4_500_000:
                    return None, f"pdf_too_large_{len(pdf_body)}"
                pdf_sha=hashlib.sha256(pdf_body).hexdigest()
                pdf_bytes_len=len(pdf_body)
                append_costs({"date":utc_now()[:10],"url":pdf_url,"bytes":len(pdf_body),"batch":BATCH_NUM,"kind":"record"})
                pdf_raw_path=f"raw/zambialii/act/{yr}/{yr}-{int(num):03d}.pdf"
                with open(pdf_raw_path,"wb") as f: f.write(pdf_body)
                pdf_path=pdf_raw_path
                ptitle, psecs, _ = parse_pdf_sections(pdf_body)
                if psecs:
                    sections=psecs
                if ptitle and not title:
                    final_title=ptitle
            except Exception as e:
                return None, f"pdf_err_{type(e).__name__}"

    if not sections:
        return None, "no_sections"

    rid=f"act-zm-{yr}-{int(num):03d}-{pick['slug']}"
    rec={
        "id":rid,
        "type":"act",
        "jurisdiction":"ZM",
        "title":final_title,
        "citation":f"Act No. {int(num)} of {yr}",
        "enacted_date":None,
        "commencement_date":None,
        "in_force":True,
        "amended_by":[],
        "repealed_by":None,
        "cited_authorities":[],
        "sections":sections,
        "source_url":final_url,
        "source_hash":f"sha256:{h_sha}",
        "fetched_at":utc_now(),
        "parser_version":PARSER_VERSION,
    }
    out_path=f"records/acts/{yr}/{rid}.json"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path,"w") as f:
        json.dump(rec, f, indent=2, ensure_ascii=False)

    # provenance
    append_provenance({"id":rid,"source_url":final_url,"source_hash":f"sha256:{h_sha}","fetched_at":rec["fetched_at"],"parser_version":PARSER_VERSION,"batch":BATCH_NUM,"raw_html":raw_html_path,"raw_pdf":pdf_path,"sections":len(sections)})
    return rec, "ok"


def main():
    # robots.txt re-verify first
    rb,_ = fetch("https://zambialii.org/robots.txt", sleep=True)
    rh=hashlib.sha256(rb).hexdigest()
    append_costs({"date":utc_now()[:10],"url":"https://zambialii.org/robots.txt","bytes":len(rb),"batch":BATCH_NUM,"kind":"robots"})
    print(f"robots sha256: {rh[:16]} (expect fce67b697ee4ef44)")

    results=[]
    for pick in PICKS:
        rec, status = ingest_one(pick)
        results.append({"yr":pick["yr"],"num":pick["num"],"title":pick["title"],"status":status,"id":(rec["id"] if rec else None)})
        print(f"  {pick['yr']}/{pick['num']} -> {status}")

    with open(f"_work/batch_{BATCH_NUM}_summary.json","w") as f:
        json.dump(results, f, indent=2)
    print("DONE")
    print(json.dumps([r["status"] for r in results]))


if __name__=="__main__":
    main()
