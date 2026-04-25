"""Batch 0223 ingest — 8 modern SI candidates from C/M/P alphabets."""
import sys, os, json, hashlib, time, urllib.request, re
from datetime import datetime, timezone
from bs4 import BeautifulSoup

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6.0
PARSER_VERSION = "0.5.0"

PICKS = [
    {'yr_num':'2021/55','year':'2021','num':'55','title':'Metrology (Measuring Instruments) Regulations, 2021','sub_phase':'sis_consumer','parent_act':'Metrology Act'},
    {'yr_num':'2021/56','year':'2021','num':'56','title':'Metrology (Pre-Packaged Commodities) Regulations, 2021','sub_phase':'sis_consumer','parent_act':'Metrology Act'},
    {'yr_num':'2021/59','year':'2021','num':'59','title':'Metrology (Certification of Competence) Regulations, 2021','sub_phase':'sis_consumer','parent_act':'Metrology Act'},
    {'yr_num':'2020/52','year':'2020','num':'52','title':'Metrology (Verification Fees) Regulations, 2020','sub_phase':'sis_consumer','parent_act':'Metrology Act'},
    {'yr_num':'2020/69','year':'2020','num':'69','title':'Plant Pests and Diseases (Phytosanitary Certification) Regulations, 2020','sub_phase':'sis_agriculture','parent_act':'Plant Pests and Diseases Act'},
    {'yr_num':'2020/70','year':'2020','num':'70','title':'Plant Pests and Diseases (Plant Quarantine and Phytosanitary Service Fees) Regulations, 2020','sub_phase':'sis_agriculture','parent_act':'Plant Pests and Diseases Act'},
    {'yr_num':'2018/23','year':'2018','num':'23','title':'Plant Variety and Seeds Regulations, 2018','sub_phase':'sis_agriculture','parent_act':'Plant Variety and Seeds Act'},
    {'yr_num':'2017/1','year':'2017','num':'1','title':'Citizens Economic Empowerment (Reservation Scheme) Regulations, 2017','sub_phase':'sis_corporate','parent_act':'Citizens Economic Empowerment Act'},
]

def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+","-",s).strip('-')
    return s[:120]

def fetch(url, sleep=True):
    if sleep: time.sleep(CRAWL)
    req = urllib.request.Request(url, headers=HEADERS)
    return urllib.request.urlopen(req, timeout=45).read()

def fetch_one(idx):
    p = PICKS[idx]
    yr = p['year']; num = p['num']
    base_url = f"https://zambialii.org/akn/zm/act/si/{yr}/{num}"
    title_slug = slugify(p['title'])
    record_id = f"si-zm-{yr}-{int(num):03d}-{title_slug}"
    
    # Already-pre-saved info
    raw_dir = f'raw/zambialii/si/{yr}'
    os.makedirs(raw_dir, exist_ok=True)
    html_path = f'{raw_dir}/{record_id}.html'
    pdf_path = f'{raw_dir}/{record_id}.pdf'
    
    fetches_done = []
    
    # Fetch HTML
    html_bytes = fetch(base_url, sleep=(idx>0))
    with open(html_path,'wb') as f: f.write(html_bytes)
    html_sha = hashlib.sha256(html_bytes).hexdigest()
    fetches_done.append({'url': base_url, 'bytes': len(html_bytes), 'path': html_path, 'sha': html_sha})
    
    # Parse HTML for date and PDF link
    soup = BeautifulSoup(html_bytes, 'html.parser')
    # Find PDF link in source link
    pdf_url = None
    for a in soup.find_all('a', href=True):
        if 'source.pdf' in a['href']:
            pdf_url = a['href']
            if pdf_url.startswith('/'):
                pdf_url = 'https://zambialii.org' + pdf_url
            break
    if not pdf_url:
        # Try direct
        # Pattern: /akn/zm/act/si/YEAR/NUM/eng@DATE/source.pdf — parse date from page meta
        date_match = None
        for meta in soup.find_all('meta'):
            if meta.get('property')=='og:url':
                m = re.search(r'eng@(\d{4}-\d{2}-\d{2})', meta.get('content',''))
                if m: date_match = m.group(1); break
        if not date_match:
            # Try canonical
            for link in soup.find_all('link', rel='canonical'):
                m = re.search(r'eng@(\d{4}-\d{2}-\d{2})', link.get('href',''))
                if m: date_match = m.group(1); break
        if date_match:
            pdf_url = f'https://zambialii.org/akn/zm/act/si/{yr}/{num}/eng@{date_match}/source.pdf'
    
    # Extract effective_date
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
            # Try parse with pdfplumber
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
    
    # Build record JSON
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
            r = fetch_one(i)
        except Exception as e:
            r = {'pick': PICKS[i], 'status':'fail', 'error': f'exception: {e}', 'fetches': []}
        results.append(r)
        print(f'[{i}] {PICKS[i]["yr_num"]} -> {r["status"]} {r.get("error","")}', flush=True)
    out = f'_work/batch_0223_slice_{start}_{end}.json'
    with open(out,'w') as f: json.dump(results, f, indent=2, default=str)
    print(f'WROTE {out}')
