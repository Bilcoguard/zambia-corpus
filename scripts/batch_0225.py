"""Batch 0225 ingest — 8 modern (>=2017) novel SI candidates from V/S/B/F/T/N alphabet probes.

Selected from 25 novel modern candidates discovered in this tick (V/S/B/F/T/N
alphabet probes). Picks span priority sub-phases (sis_tax, sis_corporate) plus
new cross-sub-phase fill (sis_environment, sis_tourism, sis_consumer, sis_governance).

Sub-phases covered:
  - sis_tax (VAT Zero-Rating Amendment Order 2022/4) — FIRST hit on priority_order
    item sis_tax in many ticks.
  - sis_corporate (Societies Amendment Rules 2022/12) — FIRST hit on priority_order
    item sis_corporate via Societies Act SI.
  - sis_consumer (Standards Compulsory Standards Declaration Order 2017/68 —
    second cluster after batch 0223's Metrology run).
  - sis_governance / sis_statistics (Statistics National Census Declaration
    Order 2021/92) — first sis_statistics record.
  - sis_environment (Forest Carbon Stock Management Regs 2021/66 + Forests
    Community Forest Management Regs 2018/11) — first sis_environment cluster.
  - sis_tourism (Tourism and Hospitality Casino Regs 2017/22 + Licensing
    Temporary Disapplication 2022/26) — first sis_tourism records.
"""
import sys, os, json, hashlib, time, urllib.request, re
from datetime import datetime, timezone
from bs4 import BeautifulSoup

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6.0
PARSER_VERSION = "0.5.0"

PICKS = [
    {'yr_num':'2022/4','year':'2022','num':'4','title':'Value Added Tax (Zero-Rating) (Amendment) Order, 2022','sub_phase':'sis_tax','parent_act':'Value Added Tax Act'},
    {'yr_num':'2022/12','year':'2022','num':'12','title':'Societies (Amendment) Rules, 2021','sub_phase':'sis_corporate','parent_act':'Societies Act'},
    {'yr_num':'2017/68','year':'2017','num':'68','title':'Standards (Compulsory Standards) (Declaration) Order, 2017','sub_phase':'sis_consumer','parent_act':'Standards Act'},
    {'yr_num':'2021/92','year':'2021','num':'92','title':'Statistics (National Census) (Declaration) Order, 2021','sub_phase':'sis_statistics','parent_act':'Statistics Act'},
    {'yr_num':'2021/66','year':'2021','num':'66','title':'Forest (Carbon Stock Management) Regulations, 2021','sub_phase':'sis_environment','parent_act':'Forests Act'},
    {'yr_num':'2018/11','year':'2018','num':'11','title':'Forests (Community Forest Management) Regulations, 2018','sub_phase':'sis_environment','parent_act':'Forests Act'},
    {'yr_num':'2022/26','year':'2022','num':'26','title':'Tourism and Hospitality (Licensing) (Temporary Disapplication of Renewal and Retention Fees) Regulations, 2022','sub_phase':'sis_tourism','parent_act':'Tourism and Hospitality Act'},
    {'yr_num':'2017/22','year':'2017','num':'22','title':'Tourism and Hospitality (Casino) Regulations, 2017','sub_phase':'sis_tourism','parent_act':'Tourism and Hospitality Act'},
    # Reserve picks (idx 8+): used if earlier picks fail/skip
    {'yr_num':'2018/14','year':'2018','num':'14','title':'Tourism and Hospitality (Accommodation Establishment Standards) Regulations, 2018','sub_phase':'sis_tourism','parent_act':'Tourism and Hospitality Act'},
    {'yr_num':'2017/20','year':'2017','num':'20','title':'Tourism and Hospitality (Prepaid Package Tours) Regulations, 2017','sub_phase':'sis_tourism','parent_act':'Tourism and Hospitality Act'},
    {'yr_num':'2022/7','year':'2022','num':'7','title':'National Archives (Fees) Regulations, 2021','sub_phase':'sis_governance','parent_act':'National Archives Act'},
    {'yr_num':'2020/64','year':'2020','num':'64','title':'National Market and Bus Station Development Fund Regulations, 2020','sub_phase':'sis_local_government','parent_act':'Markets and Bus Stations Act'},
    {'yr_num':'2020/123','year':'2020','num':'123','title':'Tourism and Hospitality (Registration of Hotel Managers) (Temporary Disapplication of Registration Fee) Regulations, 2020','sub_phase':'sis_tourism','parent_act':'Tourism and Hospitality Act'},
    {'yr_num':'2026/8','year':'2026','num':'8','title':'Fisheries (Management Area) (Declaration) Order, 2025','sub_phase':'sis_fisheries','parent_act':'Fisheries Act'},
]

def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+","-",s).strip('-')
    return s[:120]

def fetch(url, sleep=True):
    if sleep: time.sleep(CRAWL)
    req = urllib.request.Request(url, headers=HEADERS)
    return urllib.request.urlopen(req, timeout=45).read()

def fetch_one(idx, first_in_slice=False):
    p = PICKS[idx]
    yr = p['year']; num = p['num']
    base_url = f"https://zambialii.org/akn/zm/act/si/{yr}/{num}"
    title_slug = slugify(p['title'])
    record_id = f"si-zm-{yr}-{int(num):03d}-{title_slug}"

    raw_dir = f'raw/zambialii/si/{yr}'
    os.makedirs(raw_dir, exist_ok=True)
    html_path = f'{raw_dir}/{record_id}.html'
    pdf_path = f'{raw_dir}/{record_id}.pdf'

    fetches_done = []

    html_bytes = fetch(base_url, sleep=(not first_in_slice))
    with open(html_path,'wb') as f: f.write(html_bytes)
    html_sha = hashlib.sha256(html_bytes).hexdigest()
    fetches_done.append({'url': base_url, 'bytes': len(html_bytes), 'path': html_path, 'sha': html_sha})

    soup = BeautifulSoup(html_bytes, 'html.parser')
    pdf_url = None
    for a in soup.find_all('a', href=True):
        if 'source.pdf' in a['href']:
            pdf_url = a['href']
            if pdf_url.startswith('/'):
                pdf_url = 'https://zambialii.org' + pdf_url
            break
    if not pdf_url:
        date_match = None
        for meta in soup.find_all('meta'):
            if meta.get('property')=='og:url':
                m = re.search(r'eng@(\d{4}-\d{2}-\d{2})', meta.get('content',''))
                if m: date_match = m.group(1); break
        if not date_match:
            for link in soup.find_all('link', rel='canonical'):
                m = re.search(r'eng@(\d{4}-\d{2}-\d{2})', link.get('href',''))
                if m: date_match = m.group(1); break
        if date_match:
            pdf_url = f'https://zambialii.org/akn/zm/act/si/{yr}/{num}/eng@{date_match}/source.pdf'

    eff_date = None
    if pdf_url:
        m = re.search(r'eng@(\d{4}-\d{2}-\d{2})', pdf_url)
        if m: eff_date = m.group(1)

    pdf_sha = None
    pdf_text_pages = 0
    pdf_text_chars = 0
    if pdf_url:
        try:
            pdf_bytes = fetch(pdf_url, sleep=True)
            with open(pdf_path,'wb') as f: f.write(pdf_bytes)
            pdf_sha = hashlib.sha256(pdf_bytes).hexdigest()
            fetches_done.append({'url': pdf_url, 'bytes': len(pdf_bytes), 'path': pdf_path, 'sha': pdf_sha})
            import pdfplumber
            with pdfplumber.open(pdf_path) as pdf:
                pdf_text_pages = len(pdf.pages)
                txt = ""
                for page in pdf.pages:
                    pt = page.extract_text() or ""
                    txt += pt + "\n"
                pdf_text_chars = len(txt.strip())
        except Exception as e:
            return {'pick': p, 'status':'fail','error': f'pdf_fetch_or_parse: {e}', 'fetches': fetches_done}

    if pdf_text_chars == 0:
        return {'pick': p, 'status':'fail', 'error':'pdf_parse_empty', 'fetches': fetches_done, 'html_sha': html_sha, 'pdf_sha': pdf_sha}

    fetched_at = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    record = {
        'id': record_id,
        'type': 'statutory_instrument',
        'jurisdiction': 'ZM',
        'year': int(yr),
        'number': int(num),
        'title': p['title'],
        'parent_act': p['parent_act'],
        'sub_phase': p['sub_phase'],
        'effective_date': eff_date,
        'source_url': base_url,
        'source_pdf_url': pdf_url,
        'source_hash': pdf_sha or html_sha,
        'html_hash': html_sha,
        'fetched_at': fetched_at,
        'parser_version': PARSER_VERSION,
        'pdf_pages': pdf_text_pages,
        'pdf_text_chars': pdf_text_chars,
        'amended_by': [],
        'repealed_by': [],
        'cited_authorities': [],
    }
    out_dir = f'records/sis/{yr}'
    os.makedirs(out_dir, exist_ok=True)
    out_path = f'{out_dir}/{record_id}.json'
    with open(out_path, 'w') as f:
        json.dump(record, f, indent=2)
    return {'pick': p, 'status':'ok', 'record': record, 'record_path': out_path, 'fetches': fetches_done}

if __name__ == '__main__':
    start = int(sys.argv[1]); end = int(sys.argv[2])
    results = []
    for i in range(start, end):
        try:
            first = (i == start)
            r = fetch_one(i, first_in_slice=first)
        except Exception as e:
            r = {'pick': PICKS[i], 'status':'fail', 'error': f'exception: {e}', 'fetches': []}
        results.append(r)
        print(f'[{i}] {PICKS[i]["yr_num"]} -> {r["status"]} {r.get("error","")}', flush=True)
    out = f'_work/batch_0225_slice_{start}_{end}.json'
    with open(out,'w') as f: json.dump(results, f, indent=2, default=str)
    print(f'WROTE {out}')
