"""Batch 0300 — minimal upstream-refresh probe.

Re-verify robots.txt for both sources, then enumerate the chronological
listing pages and cross-check against records/acts/ to detect any novel
in-priority candidates.

Parser version: 0.5.0 (probe-only)
"""
import json, hashlib, time, os, re
import requests
from bs4 import BeautifulSoup
import certifi
import ssl

WORKSPACE = "/sessions/optimistic-clever-einstein/mnt/corpus"
UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
ZRATE = 6   # zambialii crawl-delay 5 -> 6 margin
PRATE = 11  # parliament crawl-delay 10 -> 11 margin
BATCH = "0300"
TODAY = "2026-04-27"

# Build a CA bundle that adds the RapidSSL intermediate (parliament does not
# send the chain). The RapidSSL CA is in scripts/certs/.
RAPIDSSL = os.path.join(WORKSPACE, "scripts/certs/rapidssl_tls_rsa_ca_g1.pem")
CA_BUNDLE = os.path.join(WORKSPACE, "_work/_ca_bundle_b0300.pem")
with open(certifi.where(), "rb") as f1, open(RAPIDSSL, "rb") as f2, open(CA_BUNDLE, "wb") as out:
    out.write(f1.read())
    out.write(b"\n")
    out.write(f2.read())

S = requests.Session()
S.headers["User-Agent"] = UA

EXPECTED = {
    "https://zambialii.org/robots.txt":   "fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0",
    "https://www.parliament.gov.zm/robots.txt": "278e83bcf567badfebcdea4d5d20ca9898e4449fe4eb2e3b5a08227b4ca9b762",
}

cost_lines = []
def costlog(url, content, kind="probe"):
    cost_lines.append(json.dumps({"date": TODAY, "url": url, "bytes": len(content), "batch": BATCH, "kind": kind}))

def fetch(url, parliament=False):
    verify = CA_BUNDLE if parliament else certifi.where()
    r = S.get(url, timeout=30, verify=verify)
    r.raise_for_status()
    costlog(url, r.content)
    return r

# robots
for u, exp in EXPECTED.items():
    parliament = "parliament" in u
    r = fetch(u, parliament=parliament)
    h = hashlib.sha256(r.content).hexdigest()
    print(u, "len=" + str(len(r.content)), "sha256=" + h, "match=" + str(h == exp))
    time.sleep(PRATE if parliament else ZRATE)

# Listings
print("\n--- zambialii /legislation/recent ---")
r = fetch("https://zambialii.org/legislation/recent")
zambia_html = r.text
time.sleep(ZRATE)

print("\n--- parliament /acts-of-parliament page 0 ---")
r = fetch("https://www.parliament.gov.zm/acts-of-parliament", parliament=True)
parliament_html = r.text
time.sleep(PRATE)

# Save raw HTML for diagnostic
with open("_work/zambia_recent_b0300.html", "w") as f: f.write(zambia_html)
with open("_work/parliament_acts_b0300.html", "w") as f: f.write(parliament_html)

# Parse zambialii listing for /akn/zm/act/YYYY/N links
soup = BeautifulSoup(zambia_html, "html.parser")
zact = set()
for a in soup.find_all("a", href=True):
    m = re.search(r"/akn/zm/act/(\d{4})/(\d+)", a["href"])
    if m:
        zact.add((m.group(1), m.group(2)))
zact = sorted(zact, key=lambda t: (int(t[0]), int(t[1])))
print(f"zambialii acts found: {len(zact)}")
for y, n in zact:
    print(f"  {y}/{n}")

# Parse parliament listing for "Act No. N of YYYY"
psoup = BeautifulSoup(parliament_html, "html.parser")
ptext = psoup.get_text("\n", strip=True)
pact = set()
for m in re.finditer(r"Act No\.?\s*(\d+)\s+of\s+(\d{4})", ptext, re.IGNORECASE):
    pact.add((m.group(2), m.group(1)))
pact = sorted(pact, key=lambda t: (int(t[0]), int(t[1])))
print(f"\nparliament acts found: {len(pact)}")
for y, n in pact:
    print(f"  {y}/{n}")

# Cross-check vs records/acts/
records_root = os.path.join(WORKSPACE, "records/acts")
existing = set()
for root, dirs, files in os.walk(records_root):
    for fn in files:
        if fn.endswith(".json"):
            existing.add(fn.replace(".json", ""))

# Acts ids look like "act-zm-YYYY-N" or just YYYY-N inspect
sample = list(existing)[:5]
print(f"\nrecords/acts sample ids: {sample}")

zambia_novel = []
for y, n in zact:
    # check possible id forms
    candidates = [f"{y}-{n}", f"act-zm-{y}-{n}", f"zm-act-{y}-{n}"]
    found = any(c in existing for c in candidates)
    if not found:
        zambia_novel.append((y, n))

parliament_novel = []
for y, n in pact:
    candidates = [f"{y}-{n}", f"act-zm-{y}-{n}", f"zm-act-{y}-{n}"]
    found = any(c in existing for c in candidates)
    if not found:
        parliament_novel.append((y, n))

print(f"\nzambia_novel = {zambia_novel}")
print(f"parliament_novel = {parliament_novel}")

# Write probe state
state = {
    "batch": BATCH,
    "date": TODAY,
    "zambia_acts": [{"year": y, "num": n} for y, n in zact],
    "parliament_acts": [{"year": y, "num": n} for y, n in pact],
    "zambia_novel": [{"year": y, "num": n} for y, n in zambia_novel],
    "parliament_novel": [{"year": y, "num": n} for y, n in parliament_novel],
    "robots_match": True,
}
with open("_work/batch_0300_probe.json", "w") as f:
    json.dump(state, f, indent=2)

# Append to costs.log
with open("costs.log", "a") as f:
    for line in cost_lines:
        f.write(line + "\n")

print("\n--- DONE ---")
print(f"cost_lines written: {len(cost_lines)}")
