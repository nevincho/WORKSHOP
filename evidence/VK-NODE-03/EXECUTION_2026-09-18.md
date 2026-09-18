# VK-NODE-03 C++20 Ed25519 Cross-Language Conformance Evidence — 2026-09-18

STATUS: CPP_PASS / CROSS_LANGUAGE_CRYPTO_CONFORMANCE_PASS

Repository: nevincho/WORKSHOP
Branch: vk-node-03-cpp-ed25519
Base/rollback: e4e51febf646cb7adeb9756a8d500d369faac31c
Tested head: bf7f52f49974a0dce58959e986239ed3aca634c4

Implementation independence: C++20 only. No Python embedding, invocation, runtime dependency, or Python crypto calls. Frozen NODE-02 public vectors are the oracle. The accepted WIRE-05 C++ canonicalizer was materialized byte-identically (blob 5a16649e2dd6996b6306cffe143b5082b315a328) and reused; no second canonicalization semantics were introduced.

Vector provenance: evidence/VK-NODE-02/crypto_vectors_v1.json blob 52714a69495936107690e54b70ecefc2b3832eae, originating at commit f00b113232710e5822175885360482f65a18ffb7. GitHub Actions provenance check PASS.
Accepted protocol prerequisites remain checkpointed: VK-NODE-02 e4e51febf646cb7adeb9756a8d500d369faac31c; Wire-v1/NODE-WIRE-01/NODE-WIRE-02-PY were not modified.

Crypto implementation: OpenSSL EVP Ed25519 via EVP_PKEY_new_raw_public_key(EVP_PKEY_ED25519), EVP_DigestVerifyInit, EVP_DigestVerify. OpenSSL 3.0.13. No handwritten Ed25519.

Representation: public key raw 32 bytes / 64 lowercase hex; signature raw 64 bytes / 128 lowercase hex. Strict lowercase hex decoder rejects malformed/uppercase encodings.

Signing domain independently reconstructed as ASCII("VK-NODE-CONTROL-V1/<ACTION>") || LF || accepted Wire-v1 canonical unsigned-record bytes. The C++ parser/canonicalizer parses the frozen unsigned JSON bytes, reserializes independently, and requires exact canonical byte equality.

Valid frozen vectors:
- ENROLLMENT domain length 856, SHA-256 525277b9c778cf794d26a975d30d16f40503a551ee03a7931f5024fe712559e1 — exact bytes/hash/Ed25519 PASS.
- REVOCATION length 676, SHA-256 31c915a1e3ee04feb047854a98ed58897f1f06e8adf1769b58a9e75138dd4be5 — PASS.
- MIGRATION length 722, SHA-256 70840b303dd15dd3ab10769d17e9a00900426ec0b7b583ae26c637d1e9081430 — PASS.
- RECOVERY length 924, SHA-256 a2e604d003d6966ad5e8510e1acd0a6807719acf78655cdb0cbfb4823c402923 — PASS.

Signature generation: NOT_APPLICABLE_PUBLIC_VECTOR_ONLY. Frozen persisted NODE-02 vectors intentionally contain no private test seed; secret handling was not weakened.

Negative checks: 32 PASS. Coverage includes all cross-action domain-prefix substitutions, signature bit mutation, wrong public key, LogicalIdentity, origin NodeIdentity, subject NodeIdentity, record_type, origin_sequence, parents, payload mutation, signature copy to another record, malformed/truncated/uppercase signature, R28 placeholder signature, integrity/authenticity separation, authority and clone boundaries.

R28_BAD_SIGNATURE: SIGNATURE_INVALID.

Integrity vs authenticity: a synthesized valid signed-record integrity digest changes under payload mutation. Stale digest differs/fails Wire integrity; recomputed digest can restore SHA integrity but the original Ed25519 signature still fails against the mutated signing domain.

Authority separation: verifier returns cryptographic validity only. Test explicitly preserves SIGNATURE_VALID with authorized=false.
Clone limit: verifier explicitly preserves SIGNATURE_VALID with no_clone_conflict=false.

Secrets: no production private key committed, logged, embedded in records, matrix, or evidence. No private vector was introduced.

Real execution:
Run 35321994486
Job 105526342225
Ubuntu 24.04.5
g++ 13.3.0
CMake 3.31.6
OpenSSL 3.0.13
ICU 74.2
Build: cmake -S cpp/vk_node03 -B build && cmake --build build --parallel
Test: ./build/vk_node03 evidence/VK-NODE-02/crypto_vectors_v1.json
Result: 4/4 valid vectors PASS; 32 negative checks PASS; CPP_CRYPTO_CONFORMANCE_PASS.

Machine-readable matrix: evidence/VK-NODE-03/cross_language_crypto_matrix.json.
Python NODE-02 changed: NO.
NODE-02 vectors changed: NO.
Wire-v1 semantics changed: NO.
DIST-04 changed: NO.
Transport activated: NO.
