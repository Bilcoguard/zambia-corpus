"""Ingest a single PICK index from batch_0241 — per-record subprocess pattern.
Mirror of batch_0240. Invoke via:
    python3 _work/batch_0241_ingest_one.py <idx> [sleep_first=1]
Writes _work/batch_0241_one_<idx>.json with status=ok|skip|fail.
"""
import sys, os, json, hashlib, time, urllib.request, re
from datetime import datetime, timezone
from bs4 import BeautifulSoup

sys.path.insert(0, 'scripts')
from batch_0241 import PICKS, slugify, fetch, CRAWL, PARSER_VERSION, UA, HEADERS

MAX_PDF_BYTES = 4_500_000

def fetch_one(idx, sleep_first=False):
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

    if os.path.exists(html_path):
        html_bytes = open(html_path,'rb').read()
        html_sha = hashlib.sha256(html_bytes).hexdigest()
        fetches_done.append({'url': base_url, 'bytes': len(html_bytes), 'path': html_path, 'sha': html_sha, 'reused': True})
    else:
        html_bytes = fetch(base_url, sleep=sleep_first)
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
        if not date_match and p.get('eng_date'):
            date_match = p['eng_date']
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
            if os.path.exists(pdf_path):
                pdf_bytes = open(pdf_path,'rb').read()
                pdf_sha = hashlib.sha256(pdf_bytes).hexdigest()
                fetches_done.append({'url': pdf_url, 'bytes': len(pdf_bytes), 'path': pdf_path, 'sha': pdf_sha, 'reused': True})
            else:
                pdf_bytes = fetch(pdf_url, sleep=True)
                with open(pdf_path,'wb') as f: f.write(pdf_bytes)
                pdf_sha = hashlib.sha256(pdf_bytes).hexdigest()
                fetches_done.append({'url': pdf_url, 'bytes': len(pdf_bytes), 'path': pdf_path, 'sha': pdf_sha})
            if len(pdf_bytes) > MAX_PDF_BYTES:
                return {'pick': p, 'status':'skip', 'error': f'pdf_too_large_{len(pdf_bytes)}b', 'fetches': fetches_done, 'html_sha': html_sha, 'pdf_sha': pdf_sha}
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
        'id': record_id, 'type': 'statutory_instrument', 'jurisdiction': 'ZM',
        'year': int(yr), 'number': int(num), 'title': p['title'],
        'parent_act': p['parent_act'], 'sub_phase': p['sub_phase'],
        'effective_date': eff_date, 'source_url': base_url, 'source_pdf_url': pdf_url,
        'source_hash': pdf_sha or html_sha, 'html_hash': html_sha,
        'fetched_at': fetched_at, 'parser_version': PARSER_VERSION,
        'pdf_pages': pdf_text_pages, 'pdf_text_chars': pdf_text_chars,
        'amended_by': [], 'repealed_by': [], 'cited_authorities': [],
    }
    out_dir = f'records/sis/{yr}'
    os.makedirs(out_dir, exist_ok=True)
    out_path = f'{out_dir}/{record_id}.json'
    with open(out_path, 'w') as f:
        json.dump(record, f, indent=2)
    return {'pick': p, 'status':'ok', 'record': record, 'record_path': out_path, 'fetches': fetches_done}

if __name__ == '__main__':
    idx = int(sys.argv[1])
    sleep_first = (sys.argv[2] == '1') if len(sys.argv) > 2 else True
    try:
        r = fetch_one(idx, sleep_first=sleep_first)
    except Exception as e:
        r = {'pick': PICKS[idx], 'status':'fail', 'error': f'exception: {e}', 'fetches': []}
    out = f'_work/batch_0241_one_{idx}.json'
    with open(out,'w') as f: json.dump(r, f, indent=2, default=str)
    print(f'[{idx}] {PICKS[idx]["yr_num"]} -> {r["status"]} {r.get("error","")}')
