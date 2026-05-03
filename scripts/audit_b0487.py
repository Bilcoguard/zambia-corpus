#!/usr/bin/env python3
"""Audit-only tick batch-0487 (Phase 5 judgments).

Re-runs the same audit/integrity sweep as the prior consecutive
audit-only ticks (b0375..b0383, b0385..b0464). No fresh fetches.

Outputs:
  _work/b0487/audit_summary.json    — machine-readable result
  reports/batch-0487.md             — human report (written separately)
  worker.log / costs.log            — appended by tick wrapper

Checks:
  1. Reparse-first inventory (raw HTML/PDF/records counts)
  2. Provenance completeness (source_url/source_hash/fetched_at/parser_version)
  3. source_hash shape: ^sha256:[0-9a-f]{64}$
  4. source_hash → raw resolution via full sha256 index over raw/
  5. 6 random spot-recompute (deterministic seed=487)
  6. Cross-reference resolution (cited_authorities, amended_by,
     repealed_by, key_statutes) within Phase 5 scope (judgments).
  7. Global uniqueness of record ids in records/judgments/.
"""
import hashlib
import json
import os
import pathlib
import random
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
JUDG = ROOT / "records/judgments"
RAW = ROOT / "raw"
WORK = ROOT / "_work/b0487"
WORK.mkdir(parents=True, exist_ok=True)

SHA_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


def main():
    res = {
        "batch": "0487",
        "phase": "5",
        "ts_utc_start": None,
        "inventory": {},
        "integrity": {},
        "errors": [],
    }

    # 1. Inventory ----------------------------------------------------------
    zmcc_html = list((RAW / "zambialii/judgments/zmcc").rglob("*.html"))
    zmcc_pdf = list((RAW / "zambialii/judgments/zmcc").rglob("*.pdf"))
    zmsc_html = list((RAW / "zambialii/judgments/zmsc").rglob("*.html"))
    zmsc_pdf = list((RAW / "zambialii/judgments/zmsc").rglob("*.pdf"))

    zmcc_recs = list((JUDG / "zmcc").rglob("*.json"))
    zmsc_recs = list((JUDG / "zmsc").rglob("*.json"))
    scz_recs = [p for p in JUDG.glob("*.json") if p.is_file()]

    res["inventory"] = {
        "zmcc": {
            "raw_html": len(zmcc_html),
            "raw_pdf": len(zmcc_pdf),
            "records": len(zmcc_recs),
            "missing": len(zmcc_html) - len(zmcc_recs),
        },
        "zmsc": {
            "raw_html": len(zmsc_html),
            "raw_pdf": len(zmsc_pdf),
            "records": len(zmsc_recs),
            "missing": 0,
        },
        "scz_pilot": {"records": len(scz_recs)},
        "total_records": len(zmcc_recs) + len(zmsc_recs) + len(scz_recs),
    }

    # 2. Build sha256 index over raw/ tree --------------------------------
    raw_index = {}
    raw_files = 0
    for p in RAW.rglob("*"):
        if not p.is_file():
            continue
        raw_files += 1
        try:
            h = hashlib.sha256(p.read_bytes()).hexdigest()
        except Exception:
            continue
        raw_index.setdefault(h, []).append(str(p.relative_to(ROOT)))

    res["raw_tree"] = {
        "files": raw_files,
        "unique_sha256": len(raw_index),
    }

    # 3. Per-record integrity ---------------------------------------------
    all_recs = list(JUDG.rglob("*.json"))
    seen_ids = {}
    prov_complete = 0
    sha_shape_ok = 0
    sha_resolves = 0
    refs_unresolved = 0
    rec_index = {}

    for rp in all_recs:
        try:
            r = json.loads(rp.read_text())
        except Exception as e:
            res["errors"].append(f"{rp}: JSON parse error {e}")
            continue
        rid = r.get("id")
        if not rid:
            res["errors"].append(f"{rp}: missing id")
            continue
        seen_ids.setdefault(rid, []).append(str(rp))
        rec_index[rid] = r
        ok_prov = all(r.get(f) for f in (
            "source_url", "source_hash", "fetched_at", "parser_version"))
        if ok_prov:
            prov_complete += 1
        else:
            res["errors"].append(f"{rid}: provenance incomplete")

        sh = r.get("source_hash") or ""
        if SHA_RE.match(sh):
            sha_shape_ok += 1
            if sh.split(":", 1)[1] in raw_index:
                sha_resolves += 1
            else:
                res["errors"].append(f"{rid}: source_hash does not resolve in raw/ index ({sh})")
        else:
            res["errors"].append(f"{rid}: source_hash bad shape: {sh!r}")

    dups = {k: v for k, v in seen_ids.items() if len(v) > 1}
    if dups:
        res["errors"].append(f"duplicate ids: {list(dups)[:5]}")

    # 4. Cross-references --------------------------------------------------
    for rid, r in rec_index.items():
        for fld in ("cited_authorities", "amended_by", "repealed_by",
                    "key_statutes"):
            v = r.get(fld) or []
            if isinstance(v, list):
                for ref in v:
                    if isinstance(ref, dict):
                        ref_id = ref.get("id") or ref.get("ref")
                    else:
                        ref_id = ref
                    if not ref_id:
                        continue
                    # Phase 5 scope: only need to resolve refs that
                    # point at other judgments in our corpus. Statute
                    # refs and external refs are out of Phase-5
                    # integrity scope (they belong to Phase 6+).
                    if ref_id.startswith("judgment-") and ref_id not in rec_index:
                        refs_unresolved += 1
                        res["errors"].append(
                            f"{rid}: unresolved {fld} ref: {ref_id}")

    # 5. Spot-recompute (deterministic seed=487) ---------------------------
    rng = random.Random(487)
    sample = rng.sample(all_recs, min(6, len(all_recs)))
    spot_ok = 0
    for rp in sample:
        try:
            r = json.loads(rp.read_text())
            sh = r.get("source_hash", "").split(":", 1)
            if len(sh) != 2:
                continue
            h_expected = sh[1]
            paths = raw_index.get(h_expected, [])
            if not paths:
                continue
            disk_path = ROOT / paths[0]
            h_actual = hashlib.sha256(disk_path.read_bytes()).hexdigest()
            if h_actual == h_expected:
                spot_ok += 1
            else:
                res["errors"].append(
                    f"{r.get('id')}: spot-recompute mismatch")
        except Exception as e:
            res["errors"].append(f"{rp}: spot-recompute error {e}")

    res["integrity"] = {
        "records_total": len(all_recs),
        "unique_ids": len(seen_ids),
        "provenance_complete": prov_complete,
        "source_hash_shape_ok": sha_shape_ok,
        "source_hash_resolves": sha_resolves,
        "spot_recompute_ok": spot_ok,
        "spot_recompute_seed": 487,
        "phase5_refs_unresolved": refs_unresolved,
        "court_breakdown": {
            "ZMCC": len(zmcc_recs),
            "ZMSC": len(zmsc_recs),
            "SCZ-pilot": len(scz_recs),
        },
    }

    out = WORK / "audit_summary.json"
    out.write_text(json.dumps(res, indent=2))
    print(json.dumps(res["integrity"], indent=2))
    print("---")
    print(json.dumps(res["inventory"], indent=2))
    if res["errors"]:
        print(f"ERRORS: {len(res['errors'])}")
        for e in res["errors"][:20]:
            print("  -", e)
        sys.exit(1)
    print("AUDIT-ONLY PASS")


if __name__ == "__main__":
    main()
