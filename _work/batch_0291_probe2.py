"""Batch 0291 — second-pass probe: alphabets B, I, P, S to characterise
modern novel SIs likely-relevant to sis_corporate (BFS, Insurance, Pensions,
Securities). Probe-only.
"""
import os, json, hashlib, time, urllib.request, re, glob
from datetime import datetime, timezone
from bs4 import BeautifulSoup

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6.0

# Reload existing keys
existing = set()
for f in glob.glob('records/sis/**/si-zm-*.json', recursive=True) + glob.glob('records/sis/si-zm-*.json'):
    fn = os.path.basename(f)
    parts = fn.split('-')
    if len(parts) >= 4:
        try:
            yr = int(parts[2]); num = int(parts[3])
            existing.add((yr, num))
        except: pass

ALPHABETS = ['B','I','P','S']
all_results = {}
all_novel = []
for alpha in ALPHABETS:
    url = f"https://zambialii.org/legislation/?alphabet={alpha}"
    print(f"GET {url}")
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
    print(f"  alphabet={alpha}: total={len(si_links)} modern={len(modern)} novel={len(novel)}")
    novel_sorted = sorted(novel, key=lambda x: (-x['yr'], x['num']))
    for n in novel_sorted:
        print(f"    {n['yr']}/{n['num']:>3} ({n['eng_date']}) {n['title'][:100]}")
    all_results[alpha] = {'total': len(si_links), 'modern': len(modern), 'novel_count': len(novel)}
    all_novel += novel

# Save union
with open('_work/batch_0291_probe2.json','w') as f:
    json.dump({'summary': all_results, 'novel': sorted(all_novel, key=lambda x: (-x['yr'], x['num']))}, f, indent=2)
print(f"\nTotal novel modern SIs across B,I,P,S: {len(all_novel)}")
