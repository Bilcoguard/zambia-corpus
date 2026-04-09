#!/usr/bin/env python3
"""
Single audited HTTP fetch for the Zambian Authorities Corpus worker.

Usage:
    python3 scripts/fetch_one.py <url> [--out PATH] [--no-save] [--print-body]
    python3 scripts/fetch_one.py <url> --head-only [--log-tag TAG]

Behaviour:
- Uses the configured User-Agent from approvals.yaml.
- Captures full response: status, final URL after redirects, headers, body bytes.
- Computes sha256 of the body bytes (GET mode only).
- Appends a structured entry to provenance.log (GET mode only; HEAD-mode
  probes are screening actions and are logged to worker.log instead, since
  they carry no body to hash or cite).
- If --out is given, writes the body bytes to that path (GET mode only).
- Prints a human summary to stdout.
- Does NOT respect rate limits internally — the caller must pace requests.
- Does NOT obey robots.txt — the caller is responsible for that check first.

This script is deliberately simple. It is NOT a crawler. It performs exactly
one HTTP request per invocation so every fetch is auditable.

v0.2.0 (B-POL-INFRA-1): adds --head-only mode for Content-Length band
screening, a FETCHER_VERSION constant, and a band classifier used by the
HEAD-mode worker.log writer. The default GET path is unchanged.
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
WORKER_LOG = "worker.log"
FETCHER_VERSION = "0.2.0"
EXTRA_CERTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "certs")

# Content-Length bands (bytes) for substantive-judgment screening, per
# B-POL-2b. HEAD-mode probes classify responses into target / stretch /
# outside. These bands are policy constants and are NOT used in GET mode.
BAND_TARGET_MIN = 200_000
BAND_TARGET_MAX = 1_500_000
BAND_STRETCH_MIN = 150_000
BAND_STRETCH_MAX = 2_500_000


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


def fetch(url, timeout=30, method="GET"):
    started_at = utc_now_iso()
    t0 = time.monotonic()
    if method == "HEAD":
        req = urllib.request.Request(
            url, method="HEAD", headers={"User-Agent": USER_AGENT}
        )
    else:
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
            if method != "HEAD":
                body = r.read()
    except urllib.error.HTTPError as e:
        status = e.code
        final_url = e.url if hasattr(e, "url") else url
        headers = {k: v for k, v in (e.headers.items() if e.headers else [])}
        if method != "HEAD":
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
        "method": method,
        "_body_bytes": body,
    }


def _header_ci(headers, name):
    """Case-insensitive header lookup. Returns the first match or None."""
    target = name.lower()
    for k, v in headers.items():
        if k.lower() == target:
            return v
    return None


def classify_band(content_length):
    """Classify a Content-Length (int or None) into target / stretch /
    outside bands per B-POL-2b.

    - target:  BAND_TARGET_MIN  <= cl <= BAND_TARGET_MAX
    - stretch: BAND_STRETCH_MIN <= cl <  BAND_TARGET_MIN
               OR BAND_TARGET_MAX < cl <= BAND_STRETCH_MAX
    - outside: everything else
    - "outside:null" when content_length is None (header absent)
    """
    if content_length is None:
        return "outside:null"
    if BAND_TARGET_MIN <= content_length <= BAND_TARGET_MAX:
        return "target"
    if BAND_STRETCH_MIN <= content_length < BAND_TARGET_MIN:
        return "stretch"
    if BAND_TARGET_MAX < content_length <= BAND_STRETCH_MAX:
        return "stretch"
    return "outside"


def log_head_to_worker(result, log_tag=None):
    """Append a single HEAD-probe line to worker.log. Never writes to
    provenance.log. Returns the structured entry dict for caller use."""
    headers = result.get("headers") or {}
    cl_raw = _header_ci(headers, "Content-Length")
    try:
        content_length = int(cl_raw) if cl_raw is not None else None
    except (TypeError, ValueError):
        content_length = None
    entry = {
        "url": result.get("request_url"),
        "final_url": result.get("final_url"),
        "http_status": result.get("status"),
        "content_length": content_length,
        "content_type": _header_ci(headers, "Content-Type"),
        "last_modified": _header_ci(headers, "Last-Modified"),
        "etag": _header_ci(headers, "ETag"),
        "elapsed_ms": result.get("elapsed_ms"),
        "fetcher_version": FETCHER_VERSION,
        "timestamp_utc": result.get("started_at"),
        "band": classify_band(content_length),
    }
    tag_str = f"[{log_tag}] " if log_tag else ""
    line = (
        f"[{entry['timestamp_utc']}] {tag_str}head_probe "
        f"{json.dumps(entry, ensure_ascii=False)}"
    )
    with open(WORKER_LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    return entry


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
    ap.add_argument("--head-only", action="store_true",
                    help="Issue an HTTP HEAD request instead of GET. "
                         "No body is read. Response is logged to worker.log, "
                         "not provenance.log. --out / --no-save / --print-body "
                         "are incompatible or ignored in this mode.")
    ap.add_argument("--log-tag", default=None,
                    help="Directive tag to prefix HEAD-mode worker.log lines "
                         "(e.g. \"B-POL-2b · Step 2\"). Ignored in GET mode.")
    args = ap.parse_args()

    if args.head_only and args.print_body:
        sys.stderr.write(
            "error: --head-only and --print-body are mutually exclusive\n"
        )
        sys.exit(2)

    if args.head_only:
        result = fetch(args.url, method="HEAD")
        entry = log_head_to_worker(result, log_tag=args.log_tag)
        print(f"fetcher_version: {FETCHER_VERSION}")
        print(f"mode: HEAD")
        print(f"started_at: {result['started_at']}")
        print(f"request_url: {result['request_url']}")
        print(f"final_url: {result['final_url']}")
        print(f"status: {result['status']}")
        print(f"elapsed_ms: {result['elapsed_ms']}")
        if result['error']:
            print(f"error: {result['error']}")
        print(f"content_length: {entry['content_length']}")
        print(f"content_type: {entry['content_type']}")
        print(f"last_modified: {entry['last_modified']}")
        print(f"etag: {entry['etag']}")
        print(f"band: {entry['band']}")
        print(f"body_len: {result['body_len']}  (expected 0 in HEAD mode)")
        if args.out or args.no_save:
            print("note: --out / --no-save ignored in HEAD mode")
        return

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
