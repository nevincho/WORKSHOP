# VK-NODE-02 Ed25519 Cryptographic Conformance Evidence — 2026-09-18

STATUS: CRYPTOGRAPHIC_CONFORMANCE_PASS

Repository: nevincho/LIVE
Branch: vk-node-02-ed25519
Base/rollback: e2ad2dd8a52e6bce581efd7b74b68797604393a6
Tested implementation head: d4a4fb0af51e3771d1adb611b3ce7c5f2c4ff40c
Final workflow trigger: 8306d28bd4afccb6624102c88d861c42891c72a6

Changed from base: exactly three added files: app/distributed_node_crypto_v1.py, tests/test_distributed_node_crypto_v1.py, tests/emit_node02_crypto_vectors.py. No pre-existing source file changed.

Crypto library: Python cryptography 46.0.2, established Ed25519 implementation, CPython 3.12.14 compatible. Dependency is execution-installed for this bounded reference gate; protocol is library-independent.

Wire-v1 blob: 8e753ac5bd3072750e8f87450acac65bba9e0071 — authenticated unchanged.
NODE-WIRE-01 schema/golden/rejection blobs: 614aae46e4c2960e6ffa332a05406d6a9eb40b90 / 1fbc4f82024e22d2870b2a610489cf964571bd6c / 2a7ecf3f0bcb16105614c59821282782b088b281.

Signing domain: ASCII("VK-NODE-CONTROL-V1/<ACTION>") || 0x0A || WireV1Canonical(unsigned_record), where unsigned_record removes exactly top-level integrity_digest and payload.signature.

Key encoding: Ed25519 raw 32-byte public key -> exactly 64 lowercase hex.
Signature encoding: raw 64-byte Ed25519 signature -> exactly 128 lowercase hex.

Signing validates structural record, requires signing private key public half to equal payload.issuer_public_key, signs exact checkpointed domain, inserts only payload.signature, then recomputes Wire integrity_digest.
Verification validates Wire/schema/integrity first, verifies expected issuer-key binding, then Ed25519 signature. Results distinguish SIGNATURE_VALID, SIGNATURE_INVALID, ISSUER_KEY_MISMATCH, CRYPTOGRAPHIC_AUTHENTICITY_NOT_VERIFIED. SIGNATURE_VALID yields authorized=true only when independent authority_ok is explicitly true.

Deterministic public conformance vectors persisted at evidence/VK-NODE-02/crypto_vectors_v1.json. They cover ENROLLMENT, REVOCATION, MIGRATION, RECOVERY with public key, exact signing-domain bytes, SHA-256, expected signature, verification result. Test-only private seed exists only in test code and is explicitly non-production; it is not in lifecycle records/evidence/vector output.

R28_BAD_SIGNATURE: CLOSED. Placeholder 64-byte-zero NODE-WIRE-01 signature against the expected real test public key returns SIGNATURE_INVALID.

Negative tests cover wrong expected key, bit-mutated/truncated/malformed/uppercase signatures, logical/record/envelope/payload mutations, cross-action domain separation, unauthorized signer authority separation, integrity-vs-authenticity, secret embedding and clone boundary. Structural NODE-WIRE regression continues to cover identity/action/revocation authority conflicts and private-key extra fields.

Integrity/authenticity proof: mutation without digest recomputation fails Wire integrity before crypto. With digest recomputed, the unchanged Ed25519 signature fails. Integrity therefore cannot repair authenticity.

Clone boundary: two copies with the same private key can produce the same valid deterministic Ed25519 signature. SIGNATURE_VALID is explicitly not evidence of NO_CLONE_CONFLICT.

Final real execution:
GitHub Actions run 35319954154 / job 105520021056
Ubuntu 24.04.5 / CPython 3.12.14 / cryptography 46.0.2
Command: python -m unittest -v tests.test_distributed_node_control_v1 tests.test_distributed_node_control_vectors_v1 tests.test_distributed_node_crypto_v1
Result: 23/23 unittest methods PASS.
Composition: 12 existing unit regression + 3 authoritative vector-driver tests (8 golden + 27 pre-existing executable rejection vectors; R28 separately closed by crypto test) + 8 crypto conformance test methods.
PROVENANCE_PASS printed before execution.

Earlier failing run 35319736049 classified TEST_DEFECT in integrity-vs-authenticity test mutation selection and corrected minimally. Later emitter workflow failures were EXECUTION_INFRASTRUCTURE_DEFECT only; final conformance run is clean.

DIST-04 changed: NO.
Transport/runtime activation: NONE.
Cross-language cryptographic conformance: NOT CLAIMED.
