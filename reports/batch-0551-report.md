# Phase 8 — Nightly re-verification, batch 0551

**Tick:** 2026-05-09T07:55:16Z → 2026-05-09T07:55:44Z (UTC)
**Worker:** worker-tick (scheduled-task `zambia-corpus-tick`)
**Phase:** `phase_8_nightly_reverify` (approvals.yaml; sample_rate 0.01,
MAX_BATCH_SIZE 8, read-only on corpus)
**Sequence:** Eighth Phase 8 tick overall; **fourth tick of UTC date
2026-05-09** after b0546 (05:59Z), b0548 (06:13Z), b0549 (06:35Z).
**Seed:** `phase8-reverify-2026-05-09-b0551` (tick-suffixed because
the date-only seed and the b0548/b0549 tick-suffixed seeds were already
consumed earlier today).
**Pool size:** 1853 (unchanged from b0546/b0548/b0549).
**Sample size:** 8 (cap; 1% of 1853 = 19, capped at MAX_BATCH 8).
**Parser version:** `phase8-reverify-0.1.0`.
**User-Agent:** `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`.

## Verdict counts

| Verdict | Count |
|---------|------:|
| match | 4 |
| drift | 4 |
| fetch_error | 0 |
| truncated_stored_hash_false_drift | 0 |
| **total** | **8** |

## 4 match entries — and **NEW** finding: first `/akn/judgment/` HTML match

| # | Record id | URL | Endpoint kind |
|--:|-----------|-----|---------------|
| 1 | `loz-dairies-and-dairy-produce-act` | `https://www.parliament.gov.zm/sites/default/files/documents/acts/Dairies%20and%20Dairy%20Produce%20Act.pdf` | parliament.gov.zm static PDF |
| 2 | `judgment-zm-2020-zmsc-51-richard-h-chama-213-other-v-national-pension-schem` | `https://zambialii.org/akn/zm/judgment/zmsc/2020/51/eng@2020-06-30` | **zambialii.org `/akn/judgment/.../eng@<delivery-date>` HTML** |
| 3 | `si-zm-2017-048-information-and-communication-technologies-fees-regulations-2017` | `https://zambialii.org/akn/zm/act/si/2017/48/eng@2017-06-16/source.pdf` | zambialii.org `/source.pdf` PDF endpoint |
| 4 | `act-zm-2010-048-value-added-tax-amendment` | `https://www.parliament.gov.zm/sites/default/files/documents/amendment_act/Value%20Added%20Tax%20%28Amendment%29%202010A.PDF` | parliament.gov.zm static PDF |

### NEW finding — judgment `/akn/` HTML URLs may be byte-stable across re-fetches

Match #2 (`judgment-zm-2020-zmsc-51-richard-h-chama-213-other-v-national-pension-schem`)
is the **first `/akn/` HTML URL match in 8 Phase 8 ticks** (b0524 through
b0551, total 38 `/akn/` HTML acts/SI samples, all of which had drifted).
The URL is `zambialii.org/akn/zm/judgment/zmsc/2020/51/eng@2020-06-30`,
which is a *judgment* `/akn/` HTML rendering pinned to the delivery date.
Re-fetched bytes_len = 41,557 and re-computed sha256 are byte-identical
to the stored values.

This generates a working hypothesis worth stating but **not yet
confirmable** from a single tick:

- Judgment `/akn/` HTML URLs (`/akn/zm/judgment/...`) may be more
  byte-stable than act/SI `/akn/` HTML URLs (`/akn/zm/act/...` and
  `/akn/zm/act/si/...`), possibly because:
  - judgments are not amended after delivery, so the rendered
    consolidated view doesn't change once produced;
  - judgment delivery-date pinning (`eng@<delivery-date>`) is a
    one-shot snapshot, while act `eng@<commencement-date>` HTML is a
    re-rendered consolidated-as-at view that can incorporate
    transparent metadata changes (ZambiaLII publication-date stamps,
    upstream cross-reference updates, etc.).

**Action:** record the finding; do not extrapolate from N=1. Future
Phase 8 ticks should track judgment-`/akn/` matches separately from
act/SI-`/akn/` drifts so that a hypothesis test can accumulate
evidence over a meaningful sample window.

### Cumulative match accounting (post-b0551)

- **Stable PDF endpoints** (parliament.gov.zm static PDFs +
  zambialii.org `/source.pdf` redirected to media.zambialii.org):
  21 (b0524..b0549) + 3 (b0551) = **24/24 across 8 Phase 8 ticks**.
- **Judgment `/akn/` HTML URLs**: **1/1 across 8 Phase 8 ticks** —
  first such match observed.
- **Act/SI `/akn/` HTML URLs**: **0/38 matches**, see drift table below.

## 4 drift entries — all act/SI `/akn/...` HTML rendering URLs (`content_changed_full_drift_akn_html`)

Established `content_changed_full_drift` pattern; **not** a record
data-quality issue. The act/SI `/akn/` HTML rendering surface at
zambialii.org re-renders in a non-deterministic byte-equivalent way
each fetch (pattern reproduces for the **eighth** consecutive tick
across b0524 / b0533 / b0538 / b0545 / b0546 / b0548 / b0549 / b0551;
cumulative act/SI HTML-URL drift count is **38/38**). No record action —
re-fetch and re-hash would just record a new transient drift hash.

| # | Record id | Source URL | Stored sha256 | Re-fetched sha256 | Bytes (new) | Sub-kind |
|--:|-----------|------------|---------------|-------------------|------------:|----------|
| 1 | `act-zm-2014-006-excess-expenditure-appropriation-2011-act` | `https://zambialii.org/akn/zm/act/2014/6/eng@2014-08-05` | `1f4aaa0d0e0e316154ee1cd7ff58fd22a9e5aa3da2e6994a28697b72086a1ce3` | `dad6a1b3890cbfbfeea006858b1c6e10185d9f52eb8a7d1b2266b32de32591ef` | 38,805 | `content_changed_full_drift_akn_html` |
| 2 | `act-zm-2024-002-animal-identification-and-traceability-act-2024` | `https://zambialii.org/akn/zm/act/2024/2/eng@2024-04-18` | `575ad1707f636c7c7740e28085c8c6b59172fd59cd54e36353e1840b6e1b10ed` | `328132f755ee81d7cac7e3f78ff04878ac1136fefd203fc06576bb10b1b3db3b` | 285,428 | `content_changed_full_drift_akn_html` |
| 3 | `si-zm-2020-108-urban-and-regional-planning-designated-local-planning-authorities-no-3-regulations-2020` | `https://zambialii.org/akn/zm/act/si/2020/108` | `7ab47d1b5f58af3f29f8f4af83767c187841d32f546c0c6b8c941ebbf8389951` | `9f41fe98e87f74d8f1713aa83ad998c25933ae38946c063d81ec9975ba384385` | 40,560 | `content_changed_full_drift_akn_html` |
| 4 | `act-zm-1995-022-national-health-services-act-1995` | `https://www.zambialii.org/akn/zm/act/1995/22/eng@1996-12-31` | `b749511f842cced550b768535fd94886e52d1e5c74d648baf05ea9e7329ba753` | `a32c79ab53d5921bc661a1f782ee1ebb074dab5b0c1400cbcc3bcf8c3e452bd2` | 145,137 | `content_changed_full_drift_akn_html` |

### Notable URL patterns in the drift sample

- Drift #3 (`si-zm-2020-108-...`) hits `https://zambialii.org/akn/zm/act/si/2020/108`
  with **no `eng@<date>` pin** — yet it still drifts in the same way as
  the date-pinned act URLs. So the absence of a date pin is not the
  driver of drift; the rendering layer itself is the cause.
- Drift #4 (`act-zm-1995-022-...`) is on the `www.zambialii.org` host
  variant (most other drift URLs use bare `zambialii.org`). The drift
  reproduces on both subdomains, consistent with them serving from the
  same backend.

## Truncated-stored-hash sweep

Zero truncated-stored-hash false drifts in this sample. The b0546
finding (`act-zm-2020-023-vat-amendment` had a 16-hex-char `source_hash`)
was not re-encountered. Corpus-wide hash-length audit remains a separate
repair-phase task; not Phase 8 scope.

## Records mutated

**None.** Phase 8 is read-only on the corpus. `corpus.sqlite`,
`judges_registry.yaml`, `records/`, and `raw/` are all unchanged this
tick. `approvals.yaml` was NOT modified.

## Reproducibility

- Sample seed: `phase8-reverify-2026-05-09-b0551` (deterministic;
  tick-suffixed because three earlier ticks of the same UTC date had
  already consumed the date-only seed and the b0548/b0549 tick-suffixed
  seeds).
- Execution mode: inline runner (no derivative
  `scripts/batch_0551_phase8_reverify.py` committed this tick due to
  sandbox-session safety constraint, per b0548/b0549 precedent).
  Functionality matches the `scripts/batch_0546_phase8_reverify.py`
  baseline including the `scripts/certs/*.pem` PKI loader.
- Full per-fetch JSON: `reports/batch-0551-reverify.json`.
- This markdown summary: `reports/batch-0551-report.md`.

## Daily fetch budget

worker-tick cumulative_today = 40/2000 fetches (was 32/2000 after b0549;
this tick consumed 8 reverify GET fetches on the corpus's source URLs).

## Recommendation reaffirmed

Per b0549 (sixth tick) and b0545 (fourth tick): **switch Phase 8 to
content-equivalence** (DOM-normalised hash) **for `/akn/` HTML URLs**
or **restrict the Phase 8 sample pool to stable PDF endpoints**. The
b0551 NEW finding adds nuance — judgment `/akn/` HTML may be exempt
from the drift, so a content-equivalence rule could be the better
choice (it would preserve the ability to detect *real* drifts on
judgment URLs, where they would matter most). Final decision belongs
to a human approval round — Phase 8 is open-ended; the worker does
not modify approvals.yaml.
