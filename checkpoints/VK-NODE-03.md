# VK-NODE-03 Checkpoint

STATUS: COMPLETE / CPP_PASS / CROSS_LANGUAGE_CRYPTO_CONFORMANCE_PASS / REVIEWER_PASS
Date: 2026-09-18

Repository: nevincho/WORKSHOP
Branch: vk-node-03-cpp-ed25519
Base/rollback: e4e51febf646cb7adeb9756a8d500d369faac31c
Tested head: bf7f52f49974a0dce58959e986239ed3aca634c4

Frozen NODE-02 vector blob: 52714a69495936107690e54b70ecefc2b3832eae
Accepted WIRE-05 C++ canonicalizer blob: 5a16649e2dd6996b6306cffe143b5082b315a328

Execution: GitHub Actions run 35321994486 / job 105526342225.
Environment: Ubuntu 24.04.5 / g++ 13.3.0 / CMake 3.31.6 / OpenSSL 3.0.13 / ICU 74.2.
Result: 4/4 valid vectors exact cross-language PASS; 32 negative checks PASS; R28 SIGNATURE_INVALID.

All four actions have exact signing-domain byte equality and SHA-256 equality against frozen Python-generated public vectors, followed by successful independent OpenSSL EVP Ed25519 verification.
Signature generation: NOT_APPLICABLE_PUBLIC_VECTOR_ONLY.
Authority invariant: SIGNATURE_VALID != AUTHORIZED.
Clone invariant: SIGNATURE_VALID != NO_CLONE_CONFLICT.
Secrets: production private material absent.
Python NODE-02 changed: NO.
Vectors changed: NO.
Wire-v1 semantics changed: NO.
DIST-04 changed: NO.
Transport/runtime activation: NONE.

Evidence:
- evidence/VK-NODE-03/EXECUTION_2026-09-18.md
- evidence/VK-NODE-03/cross_language_crypto_matrix.json
Review:
- review/VK-NODE-03.md

Exact next gate: VK-NODE-04 — lifecycle authority/transition decision engine over cryptographically verified lifecycle controls, transport-independent.
