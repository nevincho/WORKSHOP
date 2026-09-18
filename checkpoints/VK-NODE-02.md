# VK-NODE-02 Checkpoint

STATUS: COMPLETE / CRYPTOGRAPHIC_CONFORMANCE_PASS / REVIEWER_PASS
Date: 2026-09-18

LIVE branch: vk-node-02-ed25519
Base/rollback: e2ad2dd8a52e6bce581efd7b74b68797604393a6
Tested implementation head: d4a4fb0af51e3771d1adb611b3ce7c5f2c4ff40c
Actions: run 35319954154 / job 105520021056
Environment: Ubuntu 24.04.5 / CPython 3.12.14 / cryptography 46.0.2
Tests: 23/23 unittest methods PASS; existing 12 unit regression PASS; authoritative 8 golden and 27 prior executable rejection vectors PASS; R28_BAD_SIGNATURE closed by real Ed25519 verification as SIGNATURE_INVALID.

Crypto: Ed25519 raw public key 32 bytes -> 64 lowercase hex; signature 64 bytes -> 128 lowercase hex.
Domain: ASCII("VK-NODE-CONTROL-V1/<ACTION>") || 0x0A || WireV1Canonical(unsigned_record).
Authority invariant: SIGNATURE_VALID != AUTHORIZED. Issuer binding and lifecycle authority remain separate.
Clone invariant: SIGNATURE_VALID != NO_CLONE_CONFLICT.
Secrets: excluded from lifecycle records and public evidence.
Wire-v1 changed: NO.
DIST-04 changed: NO.
Transport/runtime activation: NONE.
Cross-language crypto conformance: NOT CLAIMED.

Evidence: evidence/VK-NODE-02/EXECUTION_2026-09-18.md
Vectors: evidence/VK-NODE-02/crypto_vectors_v1.json
Review: review/VK-NODE-02.md

Exact next gate: VK-NODE-03 — independent non-Python Ed25519 cryptographic conformance against frozen NODE-02 vectors.
