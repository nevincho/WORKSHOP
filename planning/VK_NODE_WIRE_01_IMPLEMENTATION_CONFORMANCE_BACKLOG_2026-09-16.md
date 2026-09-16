# VK-NODE-WIRE-01 — Implementation / Conformance Backlog

Date: 2026-09-16
Status: PLANNING ONLY

1. `VK-NODE-WIRE-02-PY` — Python closed-schema validator/codec for the four specialized DurableRecord types; unchanged Wire-v1 canonicalizer; execute all golden/rejection vectors; verify canonical bytes, integrity digests and signing-domain bytes. No signature PASS yet unless NODE-02 crypto profile is checkpointed.
2. `VK-NODE-02` — portable Ed25519 identity/sign/verify reference with fixed raw-key/lowercase-hex encoding and deterministic published test keys/signatures; no runtime activation.
3. `VK-NODE-WIRE-03-PY-CRYPTO` — add actual signature verification vectors and lifecycle authority rejection paths.
4. `VK-NODE-WIRE-04-INDEPENDENT` — independently implement schema/canonical/signing-domain interpretation in one non-Python language (C++/Rust/Kotlin) without delegating semantics to Python.
5. `VK-NODE-WIRE-05-CROSS-LANGUAGE` — exact canonical-byte, SHA-256 integrity, signing-domain byte, signature verification, lifecycle semantic/error comparison on common vectors.
6. `VK-NODE-03` — enrollment authority/lifecycle decision engine consuming accepted control records and returning AUTHORIZED / NOT_AUTHORIZED / RECOVERY_REQUIRED / CLONE_CONFLICT.
7. `VK-NODE-05` — narrow DIST-04 authorization adapter only after lifecycle engine conformance.

Every implementation gate must prove: existing Wire-v1 vectors unchanged/pass; no SECRETS in lifecycle records; no timestamp/device winner; migration closes only old incarnation; recovery cannot bypass CLONE_CONFLICT; replacement uses new origin namespace; revocation preserves history; DIST-04 unchanged until its separately authorized adapter gate; no transport/runtime activation.
