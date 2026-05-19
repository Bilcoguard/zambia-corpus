#!/usr/bin/env python3
"""
Phase 8 — Nightly re-verification: batch 0719.

Clone of frozen baseline scripts/batch_0546_phase8_reverify.py (frozen baseline; only BATCH constant changed);
only BATCH constant changed for this tick. Same logic as
scripts/batch_0718_phase8_reverify.py (immediately prior Phase 8 tick).

Goal: sample `sample_rate` (1%) of existing corpus records, re-fetch each,
recompute sha256, compare with the stored `source_hash`, and log any drift.
Records are NEVER mutated by this script.

Reference: BRIEF.md §"Phase 8 — Nightly re-verification."; approvals.yaml
phase_8_nightly_reverify (sample_rate: 0.01).

Note: WORKSPACE is derived from this script's location so the tick is
portable across sandboxes (prior baselines hard-coded a session-specific
path).

Parser/fetcher version: phase8-reverify-0.1.0
"""

from __future__ import annotations

import glob
import hashlib
import json
import os
import random
import ssl
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from math import ceil
from typing import Optional
from urllib.parse import urlparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.dirname(SCRIPT_DIR)
RECORDS_DIR = os.path.join(WORKSPACE, "records")
REPORTS_DIR = os.path.join(WORKSPACE, "reports")
GAPS_PATH = os.path.join(WORKSPACE, "gaps.md")
WORKER_LOG = os.path.join(WORKSPACE, "worker.log")
COSTS_LOG = os.path.join(WORKSPACE, "costs.log")
PROVENANCE_LOG = os.path.join(WORKSPACE, "provenance.log")

USER_AGENT = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
PARSER_VERSION = "phase8-reverify-0.1.0"
BATCH = "0725"
SAMPLE_RATE = 0.01  # from approvals.yaml phase_8_nightly_reverify
MAX_BATCH = 8       # scheduled-task hard cap

EXTRA_CERTS_DIR = os.path.join(SCRIPT_DIR, "certs")

# Per-host minimum gap (seconds). Defaults from approvals.yaml.
RATE_LIMITS = {
    "zambialii.org": 5,
    "www.zambialii.org": 5,
    "media.zambialii.org": 5,
    "commons.laws.africa": 5,
    "judiciary.gov.zm": 5,
    "judiciaryzambia.com": 5,
}
RATE_DEFAULT = 2

_LAST_FETCH_BY_HOST: dict[str, float] = {}


def build_ssl_context() -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    if os.path.isdir(EXTRA_CERTS_DIR):
        for pem in sorted(glob.glob(os.path.join(EXTRA_CERTS_DIR, "*.pem"))):
            try:
                ctx.load_verify_locations(cafile=pem)
            except Exception as e:
                print(f"WARN: failed to load extra cert {pem}: {e}", file=sys.stderr)
    return ctx


SSL_CONTEXT = build_ssl_context()
OPENER = urllib.request.build_opener(urllib.request.HTTPSHandler(context=SSL_CONTEXT))


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def utc_today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def normalise_hash(h: Optional[str]) -> Optional[str]:
    if not h:
        return None
    h = h.strip().lower()
    if h.startswith("sha256:"):
        h = h[len("sha256:"):]
    return h or None


def sleep_for_host(host: str) -> float:
    gap = RATE_LIMITS.get(host, RATE_DEFAULT)
    last = _LAST_FETCH_BY_HOST.get(host)
    if last is None:
        return 0.0
    elapsed = time.time() - last
    wait = gap - elapsed
    if wait > 0:
        time.sleep(wait)
        return wait
    return 0.0


def fetch_url(url: str, timeout: int = 60) -> dict:
    host = urlparse(url).netloc
    sleep_for_host(host)
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "*/*",
    })
    started = time.time()
    out = {
        "url": url,
        "host": host,
        "status": None,
        "final_url": None,
        "bytes_len": 0,
        "sha256": None,
        "error": None,
        "duration_s": 0.0,
    }
    try:
        with OPENER.open(req, timeout=timeout) as resp:
            body = resp.read()
            out["status"] = resp.status
            out["final_url"] = resp.geturl()
            out["bytes_len"] = len(body)
            out["sha256"] = hashlib.sha256(body).hexdigest()
    except urllib.error.HTTPError as e:
        out["status"] = e.code
        out["final_url"] = url
        out["error"] = f"HTTPError {e.code} {e.reason}"
    except urllib.error.URLError as e:
        out["error"] = f"URLError {e.reason}"
    except Exception as e:
        out["error"] = f"{type(e).__name__}: {e}"
    finally:
        out["duration_s"] = round(time.time() - started, 3)
        _LAST_FETCH_BY_HOST[host] = time.time()
    return out


def load_pool() -> list[dict]:
    pool: list[dict] = []
    for f in sorted(glob.glob(os.path.join(RECORDS_DIR, "**/*.json"),
                              recursive=True)):
        try:
            with open(f, "r", encoding="utf-8") as fh:
                rec = json.load(fh)
        except Exception:
            continue
        url = rec.get("source_url")
        h = normalise_hash(rec.get("source_hash"))
        if not url or not h:
            continue
        pool.append({
            "file": f,
            "id": rec.get("id") or os.path.splitext(os.path.basename(f))[0],
            "type": rec.get("type", "unknown"),
            "source_url": url,
            "stored_sha256": h,
            "parser_version": rec.get("parser_version"),
        })
    return pool


def pick_sample(pool: list[dict], sample_rate: float, cap: int,
                seed: str) -> list[dict]:
    target = min(cap, max(1, ceil(len(pool) * sample_rate)))
    rng = random.Random(seed)
    return rng.sample(pool, target)


def main() -> int:
    started_at = utc_now_iso()
    pool = load_pool()
    seed = f"phase8-reverify-{utc_today()}-b{BATCH}"
    sample = pick_sample(pool, SAMPLE_RATE, MAX_BATCH, seed)

    summary = {
        "batch": BATCH,
        "phase": "phase_8_nightly_reverify",
        "parser_version": PARSER_VERSION,
        "started_at": started_at,
        "seed": seed,
        "pool_size": len(pool),
        "sample_size": len(sample),
        "sample_rate": SAMPLE_RATE,
        "max_batch": MAX_BATCH,
        "results": [],
        "match_count": 0,
        "drift_count": 0,
        "fetch_error_count": 0,
        "fetches": 0,
        "completed_at": None,
    }

    for cand in sample:
        result = fetch_url(cand["source_url"])
        summary["fetches"] += 1
        entry = {
            "id": cand["id"],
            "type": cand["type"],
            "source_url": cand["source_url"],
            "stored_sha256": cand["stored_sha256"],
            "fetched_status": result["status"],
            "fetched_sha256": result["sha256"],
            "fetched_bytes_len": result["bytes_len"],
            "fetched_at": utc_now_iso(),
            "duration_s": result["duration_s"],
            "fetch_error": result["error"],
            "verdict": None,
        }
        if result["error"] or result["status"] != 200:
            entry["verdict"] = "fetch_error"
            summary["fetch_error_count"] += 1
        elif result["sha256"] == cand["stored_sha256"]:
            entry["verdict"] = "match"
            summary["match_count"] += 1
        else:
            entry["verdict"] = "drift"
            summary["drift_count"] += 1
        summary["results"].append(entry)
        print(f"  [{entry['verdict']:<11}] {cand['id']}  "
              f"({cand['source_url']}) status={result['status']} "
              f"new_sha={result['sha256']}", file=sys.stderr, flush=True)

    summary["completed_at"] = utc_now_iso()

    os.makedirs(REPORTS_DIR, exist_ok=True)
    json_path = os.path.join(REPORTS_DIR, f"batch-{BATCH}-reverify.json")
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, sort_keys=True)
    print(f"WROTE {json_path}", file=sys.stderr)

    print(json.dumps({
        "batch": BATCH,
        "phase": "phase_8_nightly_reverify",
        "pool_size": summary["pool_size"],
        "sample_size": summary["sample_size"],
        "match": summary["match_count"],
        "drift": summary["drift_count"],
        "fetch_error": summary["fetch_error_count"],
        "fetches": summary["fetches"],
        "seed": summary["seed"],
        "started_at": summary["started_at"],
        "completed_at": summary["completed_at"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
