# VK-WIRE-02-CORRECTION-02 Final Evidence
Date: 2026-09-15

## Result
VK-WIRE-02 = COMPLETE / BEHAVIORAL_PASS, pending independent review recorded separately before checkpoint.

## Normative clarification
Wire Profile v1 canonical RFC3339 UTC timestamps require seconds `00..59`. `:60` is not represented by v1 and is rejected as `INVALID_SCHEMA`. Wall-clock time remains metadata with zero causal authority. This deliberately avoids platform/runtime-dependent leap-second handling; it does not assert leap seconds do not exist.

Normative specification update commit: `7516d5c67647c441ffbf1717aaba2879d9a76be0`.

## Authoritative vectors
Golden vector artifact unchanged:
- path: `evidence/VK-WIRE-01/golden_vectors_v1.json`
- blob: `be675835c4f32ea1ae6b24cc37575a2238572ce8`
- count: 12

Rejection vector artifact changed only by reviewed clarification R26:
- path: `evidence/VK-WIRE-01/rejection_vectors_v1.json`
- previous blob: `ccf5f89100b307ceb67d422fe5096ae575a193f6`
- current blob: `ac79eb094fea32529d3c8f4652f19ad217b1afe3`
- count: 26
- R26: `2016-12-31T23:59:60Z` -> `INVALID_SCHEMA`
- update commit: `624fdd51bc6b73eef20aaa77b44fc1efd395e5ea`

LIVE exact-byte rejection fixture has the same current Git blob `ac79eb094fea32529d3c8f4652f19ad217b1afe3`. Test provenance constants were updated accordingly. Golden fixture remains exact blob `be675835c4f32ea1ae6b24cc37575a2238572ce8`.

## Implementation
No codec change was required in CORRECTION-02: the calendar validator from CORRECTION-01 already rejects second 60 and >=61. Only the normative ambiguity and conformance binding were changed.

LIVE branch: `vk-wire-02-codec`
Tested commit: `354162717abed5cb8b5ff33b2b31579fa0d71571`

## Behavioral execution
GitHub Actions run: `35022606626`
Job: `104561791590`
Runner: Ubuntu 24.04.5
Python: CPython 3.12.14
Command:
`python -m unittest -v tests.test_distributed_wire_v1 tests.test_distributed_wire_v1_correction`

Result: 11 tests PASS / 0 failures / 0 errors.
Coverage includes 12/12 golden vectors, 26/26 current authoritative rejection vectors including R26, exact Git-blob provenance binding, calendar validity, leap-year validity, fractional precision, second 60 and 61 rejection, deterministic canonicalization/digest, integrity, frontier relations, and StateClass safety.

## Boundaries
DIST-03 unchanged: IMPLEMENTED / STATIC REVIEW PASS / BEHAVIORAL VALIDATION BLOCKED.
DIST-04 unchanged: NOT STARTED / PROHIBITED.
No Codex used.
CROSS_LANGUAGE_CONFORMANCE_PASS is NOT claimed.