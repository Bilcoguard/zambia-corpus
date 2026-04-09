#!/usr/bin/env python3
"""
Single audited HTTP fetch for the Zambian Authorities Corpus worker.

Usage:
    python3 scripts/fetch_one.py <url> [--out PATH] [--no-save]

Behaviour:
- Uses the configured User-Agent from approvals.yaml.
- Captures full response: status, final URL after redirects, headers, body bytes.
- Computes sha256 of the body bytes.
- Appends a structured entry to provenance.log (one JSON line per fetch).
- If --out is given, writes the body bytes to that path.
- Prints a human summary to stdout.
- Does NOT respect rate limits internally — the caller must pace requests.
- Does NOT obey robots.txt — the caller is responsible for that check first.

This script is deliberately simple. It is NOT a crawler. It performs exactly
one HTTP request per invocation so every fetch is auditable.
"""

import argparse
import glob
import hashlib
import json
import os
import ssl
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone

USER_AGENT = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
PROVENANCE_LOG = "provenance.log"
EXTRA_CERTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "certs")


def build_ssl_context():
    """Build an SSL context that uses the system trust store plus any
    additional intermediate/root certs found in scripts/certs/*.pem.

    Per Phase 2 Checkpoint A policy decision (2026-04-09): chain repair is
    permitted when (a) the server presents an incomplete chain with a valid
    leaf, (b) the missing intermediate is fetched from the AIA URL embedded
    in the leaf cert itself, (c) the intermediate is issued by a CA already
    in the system trust store, and (d) every repair is logged. Adding extra
    real CAs to a trust context only ADDS trust; it never disables
    verification. Verification bypass is never permitted by this script.
    """
    ctx = ssl.create_default_context()
    if os.path.isdir(EXTRA_CERTS_DIR):
        for pem in sorted(glob.glob(os.path.join(EXTRA_CERTS_DIR, "*.pem"))):
            try:
                ctx.load_verify_locations(cafile=pem)
            except Exception as e:
                print(f"WARN: failed to load extra cert {pem}: {e}", file=sys.stderr)
    return ctx


SSL_CONTEXT = build_ssl_context()
HTTPS_HANDLER = urllib.request.HTTPSHandler(context=SSL_CONTEXT)
OPENER = urllib.request.build_opener(HTTPS_HANDLER)


def utc_now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch(url, timeout=30):
    started_at = utc_now_iso()
    t0 = time.monotonic()
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    error = None
    status = None
    final_url = None
    headers = {}
    body = b""
    try:
        with OPENER.open(req, timeout=timeout) as r:
            status = r.status
            final_url = r.geturl()
            headers = {k: v for k, v in r.getheaders()}
            body = r.read()
    except urllib.error.HTTPError as e:
        status = e.code
        final_url = e.url if hasattr(e, "url") else url
        headers = {k: v for k, v in (e.headers.items() if e.headers else [])}
        body = e.read() if hasattr(e, "read") else b""
        error = f"HTTPError {e.code} {e.reason}"
    except Exception as e:
        error = f"{type(e).__name__}: {e}"
    elapsed_ms = int((time.monotonic() - t0) * 1000)
    sha256 = hashlib.sha256(body).hexdigest() if body else None
    return {
        "started_at": started_at,
        "request_url": url,
        "final_url": final_url,
        "status": status,
        "headers": headers,
        "elapsed_ms": elapsed_ms,
        "body_len": len(body),
        "sha256": sha256,
        "error": error,
        "_body_bytes": body,
    }


def log_provenance(result):
    record = {k: v for k, v in result.items() if k != "_body_bytes"}
    line = json.dumps(record, ensure_ascii=False)
    with open(PROVENANCE_LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--out", default=None,
                    help="Path to save the response body bytes.")
    ap.add_argument("--no-save", action="store_true",
                    help="Do not save body to disk regardless of --out.")
    ap.add_argument("--print-body", action="store_true",
                    help="Print the response body to stdout (text only, decoded utf-8).")
    args = ap.parse_args()

    result = fetch(args.url)
    log_provenance(result)

    print(f"started_at: {result['started_at']}")
    print(f"request_url: {result['request_url']}")
    print(f"final_url: {result['final_url']}")
    print(f"status: {result['status']}")
    print(f"elapsed_ms: {result['elapsed_ms']}")
    print(f"body_len: {result['body_len']}")
    print(f"sha256: {result['sha256']}")
    if result['error']:
        print(f"error: {result['error']}")
    print("headers:")
    for k, v in result['headers'].items():
        print(f"  {k}: {v}")

    if args.out and not args.no_save and result['body_len']:
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        with open(args.out, "wb") as f:
            f.write(result["_body_bytes"])
        print(f"saved: {args.out} ({result['body_len']} bytes)")

    if args.print_body and result['body_len']:
        try:
            print("--- body ---")
            sys.stdout.write(result["_body_bytes"].decode("utf-8", errors="replace"))
            if not result["_body_bytes"].endswith(b"\n"):
                print()
            print("--- end body ---")
        except Exception as e:
            print(f"(body decode error: {e})")


if __name__ == "__main__":
    main()
