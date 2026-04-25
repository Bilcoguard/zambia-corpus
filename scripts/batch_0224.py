"""Batch 0224 ingest — 8 modern SI candidates from C/M/P alphabets (cache from batch 0223).

Cross-sub_phase fill drawing on 0223's discovery cache (228 novel candidates from
C/M/P alphabet probes; 16 modern >=2017; 8 already ingested in batch 0223).
This batch picks the remaining 8 modern (2017+) text-extractable candidates
without re-spending discovery fetches.

Sub-phases covered:
  - sis_security (Constitution Threatened-Security Proclamation 2017/53;
    Preservation of Public Security Regs 2017/55)
  - sis_trade (Control of Goods Forest Produce Regs 2017/27 + Prohibition Order
    2017/31; Control of Goods Agriculture Prohibition of Export Order 2019/64)
  - sis_local_government (National Markets and Bus Stations Development Fund
    Regs 2017/77; Provincial and District Boundaries Division Order 2021/114)
  - sis_agriculture (Plant Variety and Seeds Amendment Regs 2021/109)
"""
import sys, os, json, hashlib, time, urllib.request, re
from datetime import datetime, timezone
from bs4 import BeautifulSoup

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6.0
PARSER_VERSION = "0.5.0"

PICKS = [
    {'yr_num':'2017/53','year':'2017','num':'53','title':'Constitution of Zambia Act—Proclamation—Declaration of Threatened State of Public Security, 2017','sub_phase':'sis_security','parent_act':'Constitution of Zambia Act'},
    {'yr_num':'2017/55','year':'2017','num':'55','title':'Preservation of Public Security Regulations, 2017','sub_phase':'sis_security','parent_act':'Preservation of Public Security Act'},
    {'yr_num':'2017/27','year':'2017','num':'27','title':'Control of Goods (Import and Export) (Forest Produce) Regulations, 2017','sub_phase':'sis_trade','parent_act':'Control of Goods Act'},
    {'yr_num':'2017/31','year':'2017','num':'31','title':'Control of Goods (Import and Export) (Forest Produce) (Prohibition of Importation) Order, 2017','sub_phase':'sis_trade','parent_act':'Control of Goods Act'},
    {'yr_num':'2019/64','year':'2019','num':'64','title':'Control of Goods (Import and Export) (Agriculture) (Prohibition of Export) Order, 2019','sub_phase':'sis_trade','parent_act':'Control of Goods Act'},
    {'yr_num':'2017/77','year':'2017','num':'77','title':'National Markets and Bus Stations Development Fund Regulations, 2017','sub_phase':'sis_local_government','parent_act':'Markets and Bus Stations Act'},
    {'yr_num':'2021/114','year':'2021','num':'114','title':'Provincial and District Boundaries (Division) (Amendment) (No. 2) Order, 2021','sub_phase':'sis_local_government','parent_act':'Provincial and District Boundaries Act'},
    {'yr_num':'2021/109','year':'2021','num':'109','title':'Plant Variety and Seeds (Amendment) Regulations, 2021','sub_phase':'sis_agriculture','parent_act':'Plant Variety and Seeds Act'},
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

    # Fetch HTML — first request in a slice doesn't need pre-sleep
    html_bytes = fetch(base_url, sleep=(not first_in_slice))
    with open(html_path,'wb') as f: f.write(html_bytes)
    html_sha = hashlib.sha256(html_bytes).hexdigest()
    fetches_done.append({'url': base_url, 'bytes': len(html_bytes), 'path': html_path, 'sha': html_sha})

    # Parse HTML for date and PDF link
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
        first = (i == start)
        try:
            r = fetch_one(i, first_in_slice=first)
        except Exception as e:
            r = {'pick': PICKS[i], 'status':'fail', 'error': f'exception: {e}', 'fetches': []}
        results.append(r)
        print(f'[{i}] {PICKS[i]["yr_num"]} -> {r["status"]} {r.get("error","")}', flush=True)
    out = f'_work/batch_0224_slice_{start}_{end}.json'
    with open(out,'w') as f: json.dump(results, f, indent=2, default=str)
    print(f'WROTE {out}')
