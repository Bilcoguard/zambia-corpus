"""Batch 0315 integrity / steady-state invariant assertions.

Yields=0, so CHECK1..CHECK6 (record-level) are N/A. We assert the
cumulative invariants instead.
"""
import json, re, subprocess
from pathlib import Path

ASSERTIONS = []
def assertion(name, ok, detail=""):
    ASSERTIONS.append({"name": name, "ok": ok, "detail": detail})
    print(("PASS" if ok else "FAIL"), name, detail)

# 1) cumulative file counts
acts = list(Path("records/acts").rglob("*.json"))
sis  = list(Path("records/sis").rglob("*.json"))
judg = list(Path("records/judgments").rglob("*.json"))
assertion("acts==1169",     len(acts) == 1169, f"got {len(acts)}")
assertion("sis==539",       len(sis)  == 539,  f"got {len(sis)}")
assertion("judgments==25",  len(judg) == 25,   f"got {len(judg)}")

# 2) records/ tree is git-clean
out = subprocess.run(["git", "status", "--short", "records/"],
                     capture_output=True, text=True).stdout
assertion("records/_git_clean", out.strip() == "", repr(out[:200]))

# 3) probe novel counts == 0 (steady state)
probe = json.loads(Path("_work/batch_0315_probe.json").read_text())
assertion("zambialii_novel==0", probe["zambialii_recent"]["novel_count"] == 0,
          f"novel pairs: {probe['zambialii_recent']['novel_pairs']}")
assertion("parliament_novel==0", probe["parliament_page0"]["novel_count"] == 0,
          f"novel pairs: {probe['parliament_page0']['novel_pairs']}")

# 4) robots.txt SHA matches expected
zam_check = next(c for c in probe["checks"] if "zambialii" in c["url"])
parl_check = next(c for c in probe["checks"] if "parliament" in c["url"])
assertion("zambialii_robots_match",  zam_check["match"], zam_check["sha256"])
assertion("parliament_robots_match", parl_check["match"], parl_check["sha256"])

ok = all(a["ok"] for a in ASSERTIONS)
Path("_work/integrity_b0315.json").write_text(json.dumps({
    "passed": ok, "assertions": ASSERTIONS,
}, indent=2))
print()
print("OVERALL:", "PASS" if ok else "FAIL")
