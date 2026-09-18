# VK-NODE-WIRE-02-PY Execution Closure Evidence — 2026-09-18

## Status
BEHAVIORAL_PASS

## Initial execution
Run 35316145275 / job 105508095331 executed the original 12-unit suite on d1ba64a8db09a3d6d09ef604f47cd94265ea4396: 12/12 PASS, but authoritative vectors were not loaded. This evidence is retained as incomplete coverage evidence.

## Root cause and bounded corrections
GitHub Actions discovery/trigger was repaired via a default-branch execution workflow. Full-vector run 35318638343 then exposed an execution-infrastructure relative-path defect. Run 35318911655 authenticated provenance and exposed a vector-test harness defect: malformed mutations were rehashed through the Wire validator before expected rejection. Subsequent runs isolated R02/R03 ordering. Only the vector harness and explicit lifecycle conflict context were boundedly corrected; authoritative vectors and Wire-v1 were not changed.

## Final execution
Repository: nevincho/LIVE
Corrected branch lineage: vk-node-wire-02-py-exec-trigger
Exact tested commit: e2ad2dd8a52e6bce581efd7b74b68797604393a6
Source-equivalence relative to corrected source commit 62168fdc62b5a3806ca4d48aa8317cf1ca0a45ca: implementation blob unchanged at 26e4a8bc87aae9d94f99b968c5f30d3a38726da8; original unit-test blob unchanged at 07a9f52e7d901ab12fb95348300397ace8848d3b. Only vector harness changed after real failures.
Final workflow trigger commit: 539b88829b93e0f5cbc81de13834d7ad87bf7fc1
Run: 35319084982
Job: 105517251093
OS: Ubuntu 24.04.5
Python: CPython 3.12.14
Command: python -m unittest -v tests.test_distributed_node_control_v1 tests.test_distributed_node_control_vectors_v1
Result: 15 unittest methods PASS. This comprises 12/12 unit regression plus three vector-driver tests. The vector drivers load and execute all authoritative cases: 8/8 golden PASS; 27/27 executable rejection PASS; R28_BAD_SIGNATURE excluded exactly as DEFERRED_TO_NODE02_CRYPTO.

## Provenance
Implementation blob: 26e4a8bc87aae9d94f99b968c5f30d3a38726da8
Unit-test blob: 07a9f52e7d901ab12fb95348300397ace8848d3b
Vector-test blob: be77b5272a67a27eb6b704d8444466b229a723ad
Accepted Python Wire-v1 blob: 8e753ac5bd3072750e8f87450acac65bba9e0071
NODE-WIRE-01 checkpoint source: a86e46811bfe9e76a429b19843793865b31f3dc0
Schema blob: 614aae46e4c2960e6ffa332a05406d6a9eb40b90
Golden blob: 1fbc4f82024e22d2870b2a610489cf964571bd6c
Rejection blob: 2a7ecf3f0bcb16105614c59821282782b088b281
Workflow printed PROVENANCE_PASS before tests.

## Behavioral results
- 12/12 original unit regression PASS.
- 8/8 golden vectors PASS: exact canonical length/SHA-256, Wire integrity digest, signing-domain length/SHA-256 and structural lifecycle acceptance checked.
- 27/27 executable rejection vectors PASS: each authoritative vector ID R01-R27 is iterated and expected error code compared with actual.
- R28_BAD_SIGNATURE = DEFERRED_TO_NODE02_CRYPTO and is not counted as PASS.
- canonical/signing-domain determinism PASS.
- placeholder signature authority negative test PASS: CRYPTOGRAPHIC_AUTHENTICITY_NOT_VERIFIED; no AUTHORIZED/AUTHENTICATED/SIGNATURE_VALID.
- SHARED_REPLICATED and null claim/admission enforcement PASS.
- secrets/extra private key rejection PASS.
- migration ACTIVE invariant PASS.
- SAME_NODE recovery structural rule PASS; replacement recovery/enrollment namespace separation PASS.
- unresolved CLONE_CONFLICT cannot be cleared by recovery PASS.
- lifecycle action, identity binding and revoked-reactivation conflict contexts exercised by R24/R23/R18 respectively.
- no cryptographic authenticity claim; no Ed25519 runtime implemented.

## Scope preservation
Wire-v1 changed: NO.
DIST-04 changed: NO.
NODE-02 crypto implemented: NO.
Transport/runtime activation: NONE.
Authoritative vectors changed: NO.
