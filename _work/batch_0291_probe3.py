"""Batch 0291 probe-3 — alphabets T, V, M, A for additional sis_tax candidates."""
import os, json, hashlib, time, urllib.request, re, glob
from datetime import datetime, timezone
from bs4 import BeautifulSoup

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6.0

existing = set()
for f in glob.glob('records/sis/**/si-zm-*.json', recursive=True) + glob.glob('records/sis/si-zm-*.json'):
    fn = os.path.basename(f); parts = fn.split('-')
    if len(parts) >= 4:
        try: existing.add((int(parts[2]), int(parts[3])))
        except: pass

ALPHABETS = ['T','V','M','A']
all_novel = []
for alpha in ALPHABETS:
    url = f"https://zambialii.org/legislation/?alphabet={alpha}"
    time.sleep(CRAWL)
    req = urllib.request.Request(url, headers=HEADERS)
    html = urllib.request.urlopen(req, timeout=45).read()
    sha = hashlib.sha256(html).hexdigest()
    out = f'_work/batch_0291_alphabet_{alpha}.html'
    with open(out,'wb') as f: f.write(html)
    with open('costs.log','a') as fd:
        fd.write(json.dumps({'date': datetime.now(timezone.utc).strftime('%Y-%m-%d'), 'url': url, 'bytes': len(html), 'batch':'0291','kind':'probe'}) + '\n')
    soup = BeautifulSoup(html, 'html.parser')
    seen = set(); si_links = []
    for a in soup.find_all('a', href=True):
        h = a['href']
        m = re.match(r'/akn/zm/act/si/(\d{4})/(\d+)(?:/eng@(\d{4}-\d{2}-\d{2}))?', h)
        if m:
            yr = int(m.group(1)); num = int(m.group(2)); eng = m.group(3)
            key=(yr,num)
            if key in seen: continue
            seen.add(key)
            si_links.append({'yr':yr,'num':num,'href':h,'eng_date':eng,'title':a.get_text(strip=True),'alpha':alpha})
    modern = [s for s in si_links if s['yr'] >= 2017]
    novel = [s for s in modern if (s['yr'], s['num']) not in existing]
    print(f"alphabet={alpha}: total={len(si_links)} modern={len(modern)} novel={len(novel)}")
    novel_sorted = sorted(novel, key=lambda x: (-x['yr'], x['num']))
    for n in novel_sorted:
        print(f"  {n['yr']}/{n['num']:>3} ({n['eng_date']}) {n['title'][:100]}")
    all_novel += novel

# Classify by sub_phase keywords
TAX_PAT = re.compile(r'\b(Income Tax|Customs|Excise|Value Added Tax|VAT|Property Transfer|Mineral Royalty|Tax|Tourism Levy|Stamp)\b', re.I)
CORP_PAT = re.compile(r'\b(Companies|Corporate|Co-operative|Cooperative|Citizens Economic Empowerment|Banking|Insurance|Pensions|Securities)\b', re.I)
EMPL_PAT = re.compile(r'\b(Employment|Labour|Minimum Wages|National Pension|Workers|Industrial Relations)\b', re.I)
DATA_PAT = re.compile(r'\b(Data Protection|Cyber|Electronic Communications)\b', re.I)
MINING_PAT = re.compile(r'\b(Mines|Mining|Minerals|Petroleum|Geological)\b', re.I)
FAMILY_PAT = re.compile(r'\b(Marriage|Divorce|Children|Adoption|Family)\b', re.I)

bucketed = {'sis_tax':[], 'sis_corporate':[], 'sis_employment':[], 'sis_data_protection':[], 'sis_mining':[], 'sis_family':[], 'other':[]}
for n in all_novel:
    t = n['title']
    if TAX_PAT.search(t): bucketed['sis_tax'].append(n)
    elif CORP_PAT.search(t): bucketed['sis_corporate'].append(n)
    elif EMPL_PAT.search(t): bucketed['sis_employment'].append(n)
    elif DATA_PAT.search(t): bucketed['sis_data_protection'].append(n)
    elif MINING_PAT.search(t): bucketed['sis_mining'].append(n)
    elif FAMILY_PAT.search(t): bucketed['sis_family'].append(n)
    else: bucketed['other'].append(n)

print("\nBucketed (T/V/M/A only):")
for b, items in bucketed.items():
    print(f"  {b}: {len(items)}")
    for n in items[:10]:
        print(f"    {n['alpha']} {n['yr']}/{n['num']:>3} {n['title'][:90]}")

with open('_work/batch_0291_probe3.json','w') as f:
    json.dump({'novel':all_novel,'bucketed':bucketed}, f, indent=2)
