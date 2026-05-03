#!/usr/bin/env python3
"""Integrity check for batch-0503 (Phase 5 audit-only zero-yield tick #5 - completion criterion fires).

Phase 5 scope, no-regression sweep — matches the b0499 lighter check:
  - Unique IDs across records/judgments/
  - Core provenance complete: source_url + source_hash + fetched_at + parser_version
  - source_hash shape: "sha256:" + 64-hex
  - source_hash resolves into raw/ tree (sha256-by-content index)
  - Spot recompute 6 random records (deterministic seed=503) — sha256 must match
  - Cross-refs (cited_authorities / amended_by / repealed_by): 0 unresolved
"""

import hashlib
import json
import pathlib
import re
import random
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

CORE = ("source_url", "source_hash", "fetched_at", "parser_version")
SH_RE = re.compile(r"^sha256:([0-9a-f]{64})$")


def build_raw_sha_index():
    idx = {}
    for p in (ROOT / "raw").rglob("*"):
        if not p.is_file():
            continue
        try:
            h = hashlib.sha256(p.read_bytes()).hexdigest()
        except Exception:
            continue
        idx.setdefault(h, []).append(str(p.relative_to(ROOT)))
    return idx


def main():
    errors = []
    notes = []
    records = sorted((ROOT / "records/judgments").rglob("*.json"))
    print(f"records/judgments JSON files: {len(records)}")

    parsed = []
    for p in records:
        try:
            r = json.loads(p.read_text())
        except Exception as e:
            errors.append(f"{p}: invalid JSON ({e})")
            continue
        parsed.append((p, r))

    # uniqueness
    seen = {}
    for p, r in parsed:
        rid = r.get("id")
        if not rid:
            errors.append(f"{p}: missing id")
            continue
        seen.setdefault(rid, []).append(str(p))
    dups = {k: v for k, v in seen.items() if len(v) > 1}
    if dups:
        errors.append(f"duplicate ids: {list(dups)[:5]}")
    print(f"unique IDs: {len(seen)} / {len(parsed)} (dups={len(dups)})")

    # core provenance
    prov_ok = 0
    for p, r in parsed:
        miss = [k for k in CORE if not r.get(k)]
        if miss:
            errors.append(f"{p}: missing core provenance {miss}")
            continue
        prov_ok += 1
    print(f"core provenance complete: {prov_ok} / {len(parsed)}")

    # source_hash shape
    shape_ok = 0
    sh_to_records = {}
    for p, r in parsed:
        sh = r.get("source_hash") or ""
        m = SH_RE.match(sh)
        if not m:
            errors.append(f"{p}: bad source_hash shape {sh!r}")
            continue
        shape_ok += 1
        sh_to_records.setdefault(m.group(1), []).append(p)
    print(f"source_hash shape valid: {shape_ok} / {len(parsed)}")

    # raw sha256 index
    print("Building raw sha256 index ...")
    raw_idx = build_raw_sha_index()
    total_raw = sum(len(v) for v in raw_idx.values())
    print(f"raw/: {total_raw} files / {len(raw_idx)} unique sha256")

    # source_hash resolves
    resolved = 0
    unresolved = []
    for hex_sh, recs in sh_to_records.items():
        if hex_sh in raw_idx:
            resolved += len(recs)
        else:
            for p in recs:
                unresolved.append((str(p), hex_sh))
    print(f"source_hash resolves into raw/: {resolved} / {shape_ok}")
    if unresolved:
        errors.append(f"unresolved source_hash for {len(unresolved)} record(s); first: {unresolved[:3]}")

    # internal xrefs
    all_ids = {r.get("id") for _, r in parsed}
    xref_unresolved = []
    xref_total = 0
    for p, r in parsed:
        for k in ("cited_authorities", "amended_by", "repealed_by"):
            v = r.get(k)
            if not v:
                continue
            for ref in v:
                xref_total += 1
                tgt = ref if isinstance(ref, str) else (ref.get("id") if isinstance(ref, dict) else None)
                if tgt and tgt.startswith("judgment-zm-") and tgt not in all_ids:
                    xref_unresolved.append((str(p), k, tgt))
    print(f"internal xrefs: {xref_total} ({len(xref_unresolved)} unresolved)")
    if xref_unresolved:
        errors.append(f"unresolved internal xrefs (first 3): {xref_unresolved[:3]}")

    # spot recompute (seed=503, 6 records)
    if parsed:
        rng = random.Random(503)
        sample = rng.sample(parsed, min(6, len(parsed)))
        spot_ok = 0
        for p, r in sample:
            sh = r.get("source_hash") or ""
            m = SH_RE.match(sh)
            if not m:
                errors.append(f"spot: {p} bad source_hash {sh!r}")
                continue
            hex_sh = m.group(1)
            paths = raw_idx.get(hex_sh)
            if not paths:
                errors.append(f"spot: {p} hash {hex_sh} not in raw/")
                continue
            disk = ROOT / paths[0]
            try:
                actual = hashlib.sha256(disk.read_bytes()).hexdigest()
                if actual == hex_sh:
                    spot_ok += 1
                else:
                    errors.append(f"spot mismatch {p}: declared {hex_sh} vs disk {actual}")
            except Exception as e:
                errors.append(f"spot read fail {p}: {e}")
        print(f"spot recompute (seed=503): {spot_ok} / {len(sample)}")

    # parser_version histogram
    pv = {}
    for _, r in parsed:
        pv[r.get("parser_version", "?")] = pv.get(r.get("parser_version", "?"), 0) + 1
    print("parser_version histogram:", pv)

    # court histogram
    ch = {}
    for _, r in parsed:
        ch[r.get("court", "?")] = ch.get(r.get("court", "?"), 0) + 1
    print("court histogram:", ch)

    print("---")
    if errors:
        print("INTEGRITY CHECK: FAIL")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print(f"INTEGRITY CHECK: PASS ({len(parsed)} record(s) — Phase 5 scope, audit-only)")


if __name__ == "__main__":
    main()
