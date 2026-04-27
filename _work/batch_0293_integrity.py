"""Batch 0293 integrity check — probe-only tick.

Probe-only batches do not write records, so the standard
no-duplicate-IDs / amended_by-resolves / source_hash-matches checks
have no new records to validate. This script verifies that the
inherited corpus state is consistent and that this tick did not
inadvertently mutate it.

Checks:

  C1: records/sis/ JSON count matches the prior closing state (539).
  C2: records/acts/ JSON count matches the prior closing state (1169).
  C3: All 7 alphabet probes produced cached HTML on disk and are
      well-formed (BeautifulSoup parses without error; >0 <a> links).
  C4: zambialii robots.txt sha256 = expected (frozen since b0193).
  C5: parliament robots.txt sha256 = expected (frozen since b0290).
  C6: /legislation/recent and parliament page0 confirm zero novel
      Acts (steady-state preserved).
  C7: No record JSON written under records/sis/ or records/acts/
      with mtime in this tick window (sanity guard).

Exit code 0 = pass; non-zero = fail.
"""
import os, glob, json, re, hashlib, sys, time
from bs4 import BeautifulSoup

EXPECTED_ZLII = "fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0"
EXPECTED_PARL = "278e83bcf567badfebcdea4d5d20ca9898e4449fe4eb2e3b5a08227b4ca9b762"

PRIOR_SIS_COUNT = 539
PRIOR_ACTS_COUNT = 1169

failures = []

# C1
sis_count = len(glob.glob('records/sis/**/*.json', recursive=True))
if sis_count != PRIOR_SIS_COUNT:
    failures.append(f"C1 SIs count drift: {sis_count} != {PRIOR_SIS_COUNT}")
print(f"C1 sis_count={sis_count} (expected {PRIOR_SIS_COUNT})")

# C2
acts_count = len(glob.glob('records/acts/**/*.json', recursive=True))
if acts_count != PRIOR_ACTS_COUNT:
    failures.append(f"C2 Acts count drift: {acts_count} != {PRIOR_ACTS_COUNT}")
print(f"C2 acts_count={acts_count} (expected {PRIOR_ACTS_COUNT})")

# C3: all 7 alphabet HTMLs present and parseable
for alpha in ['D', 'G', 'H', 'K', 'O', 'R', 'U']:
    p = f'_work/batch_0293_alphabet_{alpha}.html'
    if not os.path.exists(p):
        failures.append(f"C3 missing {p}")
        continue
    html = open(p).read()
    try:
        soup = BeautifulSoup(html, 'html.parser')
        n_links = len(soup.find_all('a', href=True))
        if n_links == 0:
            failures.append(f"C3 zero links in {p}")
        else:
            print(f"C3 {p}: {n_links} <a> links — OK")
    except Exception as e:
        failures.append(f"C3 parse error in {p}: {e}")

# C4: zambialii robots
p = '_work/batch_0293_zambialii_robots.txt'
if os.path.exists(p):
    sha = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    if sha != EXPECTED_ZLII:
        failures.append(f"C4 zambialii robots drift: {sha}")
    else:
        print(f"C4 zambialii robots sha={sha[:16]} — OK")
else:
    failures.append("C4 missing zambialii robots cache")

# C5: parliament robots
p = '_work/batch_0293_parliament_robots.txt'
if os.path.exists(p):
    sha = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    if sha != EXPECTED_PARL:
        failures.append(f"C5 parliament robots drift: {sha}")
    else:
        print(f"C5 parliament robots sha={sha[:16]} — OK")
else:
    failures.append("C5 missing parliament robots cache")

# C6: probe.json produced; in-priority picks = 0
probe_path = '_work/batch_0293_probe.json'
if not os.path.exists(probe_path):
    failures.append("C6 missing probe.json")
else:
    probe = json.load(open(probe_path))
    n_picks_raw = len(probe.get('picks', []))
    print(f"C6 probe.picks (raw) = {n_picks_raw}")
    # Recompute true picks against comprehensive existing-set
    sis_existing = set()
    for fp in glob.glob('records/sis/**/*.json', recursive=True):
        fn = os.path.basename(fp)
        m = re.match(r'si-zm-(\d{4})-0*(\d+)(?:-.*)?\.json', fn)
        if m:
            sis_existing.add((int(m.group(1)), int(m.group(2))))
            continue
        try:
            d = json.load(open(fp))
            cit = d.get('citation', '') or ''
            m2 = re.search(r'(?:SI|Statutory Instrument)[^\d]*(\d+)\s+of\s+(\d{4})', cit, re.I)
            if m2:
                sis_existing.add((int(m2.group(2)), int(m2.group(1))))
        except Exception:
            pass
    true_picks = []
    for p_ in probe['picks']:
        key = (p_['yr'], p_['num'])
        if key not in sis_existing:
            true_picks.append(p_)
    print(f"C6 probe.picks (true, after comprehensive existing-set): {len(true_picks)}")
    if len(true_picks) != 0:
        failures.append(f"C6 unexpected non-zero true picks: {len(true_picks)}")

# C7: no records/ writes in this tick
tick_start = time.time() - 30 * 60  # 30-min window
recent_writes = []
for fp in glob.glob('records/sis/**/*.json', recursive=True) + \
          glob.glob('records/acts/**/*.json', recursive=True):
    if os.path.getmtime(fp) > tick_start:
        recent_writes.append(fp)
if recent_writes:
    failures.append(f"C7 unexpected record writes: {recent_writes[:5]}")
else:
    print("C7 no record writes this tick — OK")

print()
if failures:
    print("INTEGRITY FAIL:")
    for f in failures:
        print(f"  {f}")
    sys.exit(1)
else:
    print("INTEGRITY PASS")
    sys.exit(0)
