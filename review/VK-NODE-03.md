# Independent Review — VK-NODE-03 — 2026-09-18

DECISION: PASS / REVIEWER_PASS

Scope reviewed: frozen NODE-02 vector provenance, C++20 source/build boundary, accepted WIRE-05 canonicalizer provenance, final GitHub Actions run 35321994486 / job 105526342225, machine-readable matrix, and base-to-tested-head change set.

Findings:
- Implementation is genuinely non-Python: C++20 executable only; no Python invocation, embedding, runtime dependency, or Python crypto API.
- OpenSSL 3.0.13 EVP Ed25519 is used; no handwritten Ed25519 arithmetic.
- Frozen NODE-02 vector blob 52714a69495936107690e54b70ecefc2b3832eae authenticated before execution.
- Accepted WIRE-05 C++ canonicalizer blob 5a16649e2dd6996b6306cffe143b5082b315a328 was reused byte-identically. Wire-v1 semantics unchanged.
- All four frozen actions reconstruct exact signing-domain bytes and exact SHA-256 values.
- All 4/4 frozen Ed25519 signatures verify as SIGNATURE_VALID.
- R28 placeholder signature independently rejects as SIGNATURE_INVALID.
- 32 negative checks PASS, including cross-action domain separation and explicit LogicalIdentity/origin-node/subject-NodeIdentity/record-type/sequence/parents/payload/signature-copy mutations.
- Integrity and authenticity remain distinct: recomputing SHA integrity after mutation does not repair Ed25519 authenticity.
- Cryptographic validity is not lifecycle authority. SIGNATURE_VALID != AUTHORIZED.
- Cryptographic validity is not clone resolution. SIGNATURE_VALID != NO_CLONE_CONFLICT.
- No production private key material is committed or logged. Signature generation is correctly classified NOT_APPLICABLE_PUBLIC_VECTOR_ONLY because frozen public vectors do not expose private test material.
- Machine-readable matrix is complete for C01-C04 and records lengths, exact-byte equality, SHA equality, public/signature byte equality, expected/actual verification and PASS.
- Real execution PASS on Ubuntu 24.04.5, g++ 13.3.0, CMake 3.31.6, OpenSSL 3.0.13, ICU 74.2.
- Python NODE-02 implementation and vectors unchanged. DIST-04 unchanged. Transport inactive.

Reviewer conclusion: VK-NODE-03 satisfies the bounded independent C++20 cross-language Ed25519 cryptographic conformance gate.
