"""Substitute pick for batch_0251 idx=3 (1990/39 ZNPF was pdf_too_large_4624989b).
Uses the SUBS pool entry 1996/44 ZNPF instead. Writes _work/batch_0251_one_3.json
overwriting the prior skip result so the batch reaches 8/8 yield.
"""
import sys, os, json, hashlib, urllib.request, re
from datetime import datetime, timezone
from bs4 import BeautifulSoup

sys.path.insert(0, 'scripts')
from batch_0251 import slugify, fetch, CRAWL, PARSER_VERSION, UA, HEADERS

# Override PICKS[3] with substitute (1996/44 ZNPF Statutory Contributions)
SUB_PICK = {"yr_num":"1996/44","year":"1996","num":"44","title":"","parent_act":"Zambia National Provident Fund Act","sub_phase":"sis_governance"}

# Re-import the per-record helper from main ingest module by inlining the
# fetch_one logic with SUB_PICK in place of PICKS[3].
MAX_PDF_BYTES = 4_500_000


def extract_title(soup, default=""):
    for meta in soup.find_all('meta'):
        if meta.get('property') == 'og:title':
            t = meta.get('content', '').strip()
            if t:
                return t
    if soup.title and soup.title.string:
        t = soup.title.string.strip()
        t = re.sub(r'\s*[|\-]\s*Zambia.*$', '', t).strip()
        if t:
            return t
    h1 = soup.find('h1')
    if h1:
        t = h1.get_text(strip=True)
        if t:
            return t
    return default


def extract_parent_act(soup, fallback=""):
    for a in soup.find_all('a', href=True):
        href = a['href']
        if '/akn/zm/act/' in href and '/si/' not in href:
            txt = a.get_text(strip=True)
            if txt and 'Act' in txt:
                return txt
    return fallback


def fetch_one(p, sleep_first=True):
    yr = p['year']
    num = p['num']
    base_url = f"https://zambialii.org/akn/zm/act/si/{yr}/{num}"
    raw_dir = f'raw/zambialii/si/{yr}'
    os.makedirs(raw_dir, exist_ok=True)
    fetches_done = []

    tmp_html = f'{raw_dir}/_tmp-batch-0251-sub-{yr}-{num}.html'
    if os.path.exists(tmp_html):
        html_bytes = open(tmp_html, 'rb').read()
        html_sha = hashlib.sha256(html_bytes).hexdigest()
        fetches_done.append({'url': base_url, 'bytes': len(html_bytes), 'path': tmp_html, 'sha': html_sha, 'reused': True})
    else:
        html_bytes = fetch(base_url, sleep=sleep_first)
        with open(tmp_html, 'wb') as f:
            f.write(html_bytes)
        html_sha = hashlib.sha256(html_bytes).hexdigest()
        fetches_done.append({'url': base_url, 'bytes': len(html_bytes), 'path': tmp_html, 'sha': html_sha})

    soup = BeautifulSoup(html_bytes, 'html.parser')

    title = extract_title(soup, default=p.get('title', '') or f"SI {yr}/{num}")
    if not title:
        return {'pick': p, 'status': 'fail', 'error': 'title_extract_failed', 'fetches': fetches_done, 'html_sha': html_sha}

    parent_act = p.get('parent_act') or extract_parent_act(soup, fallback="")
    title_slug = slugify(title)
    record_id = f"si-zm-{yr}-{int(num):03d}-{title_slug}"

    html_path = f'{raw_dir}/{record_id}.html'
    if not os.path.exists(html_path):
        os.rename(tmp_html, html_path)
    else:
        try:
            os.remove(tmp_html)
        except OSError:
            pass
    fetches_done[0]['path'] = html_path

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
            if meta.get('property') == 'og:url':
                m = re.search(r'eng@(\d{4}-\d{2}-\d{2})', meta.get('content', ''))
                if m:
                    date_match = m.group(1); break
        if not date_match:
            for link in soup.find_all('link', rel='canonical'):
                m = re.search(r'eng@(\d{4}-\d{2}-\d{2})', link.get('href', ''))
                if m:
                    date_match = m.group(1); break
        if date_match:
            pdf_url = f'https://zambialii.org/akn/zm/act/si/{yr}/{num}/eng@{date_match}/source.pdf'

    eff_date = None
    if pdf_url:
        m = re.search(r'eng@(\d{4}-\d{2}-\d{2})', pdf_url)
        if m:
            eff_date = m.group(1)

    pdf_path = f'{raw_dir}/{record_id}.pdf'
    pdf_sha = None
    pdf_text_pages = 0
    pdf_text_chars = 0

    if pdf_url:
        try:
            if os.path.exists(pdf_path):
                pdf_bytes = open(pdf_path, 'rb').read()
                pdf_sha = hashlib.sha256(pdf_bytes).hexdigest()
                fetches_done.append({'url': pdf_url, 'bytes': len(pdf_bytes), 'path': pdf_path, 'sha': pdf_sha, 'reused': True})
            else:
                pdf_bytes = fetch(pdf_url, sleep=True)
                with open(pdf_path, 'wb') as f:
                    f.write(pdf_bytes)
                pdf_sha = hashlib.sha256(pdf_bytes).hexdigest()
                fetches_done.append({'url': pdf_url, 'bytes': len(pdf_bytes), 'path': pdf_path, 'sha': pdf_sha})
            if len(pdf_bytes) > MAX_PDF_BYTES:
                return {'pick': p, 'status': 'skip', 'error': f'pdf_too_large_{len(pdf_bytes)}b', 'fetches': fetches_done, 'html_sha': html_sha, 'pdf_sha': pdf_sha, 'title': title}
            import pdfplumber
            with pdfplumber.open(pdf_path) as pdf:
                pdf_text_pages = len(pdf.pages)
                txt_parts = []
                for page in pdf.pages:
                    pt = page.extract_text() or ""
                    txt_parts.append(pt)
                txt = "\n".join(txt_parts).strip()
                pdf_text_chars = len(txt)
        except Exception as e:
            return {'pick': p, 'status': 'fail', 'error': f'pdf_fetch_or_parse: {e}', 'fetches': fetches_done, 'title': title}
    else:
        return {'pick': p, 'status': 'fail', 'error': 'no_pdf_url_found', 'fetches': fetches_done, 'html_sha': html_sha, 'title': title}

    if pdf_text_chars == 0:
        return {'pick': p, 'status': 'fail', 'error': 'pdf_parse_empty', 'fetches': fetches_done, 'html_sha': html_sha, 'pdf_sha': pdf_sha, 'title': title}

    fetched_at = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    record = {
        'id': record_id,
        'type': 'statutory_instrument',
        'jurisdiction': 'ZM',
        'year': int(yr),
        'number': int(num),
        'title': title,
        'parent_act': parent_act,
        'sub_phase': p.get('sub_phase', ''),
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
    return {'pick': p, 'status': 'ok', 'record': record, 'record_path': out_path, 'fetches': fetches_done, 'title': title}


if __name__ == '__main__':
    try:
        r = fetch_one(SUB_PICK, sleep_first=True)
    except Exception as e:
        r = {'pick': SUB_PICK, 'status': 'fail', 'error': f'exception: {e}', 'fetches': []}
    out = '_work/batch_0251_one_3.json'
    with open(out, 'w') as f:
        json.dump(r, f, indent=2, default=str)
    print(f"[3-sub] {SUB_PICK['yr_num']} -> {r['status']} {r.get('error','')} title={r.get('title','')[:60]}")
