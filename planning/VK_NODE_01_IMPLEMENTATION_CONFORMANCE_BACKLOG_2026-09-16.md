# VK-NODE-01 — Implementation / Conformance Backlog

Date: 2026-09-16
Status: PLANNING ONLY — NO IMPLEMENTATION AUTHORIZED

Authority: `decisions/VK_NODE_IDENTITY_ENROLLMENT_TRUST_CLONE_RECOVERY_CONTRACT_2026-09-16.md`.

## Gate sequence

### VK-NODE-WIRE-01 — lifecycle control-record Wire extension
Define only the bounded extension required for NodeEnrollmentRecord, NodeRevocationRecord, NodeMigrationRecord and NodeRecoveryRecord. Produce closed schemas, signature preimages, canonical rules, causal/idempotency/conflict semantics, compatibility rules, golden/rejection vectors and independent review. Do not mutate Wire Profile v1 vectors in place.

### VK-NODE-02 — cryptographic identity reference implementation
Implement portable Ed25519 node key generation/sign/verify and NodeIdentity binding against the accepted extension. Cover Python first only if authorized; no runtime activation. Verify fixed portable encodings and deterministic verification behavior.

### VK-NODE-03 — enrollment authority and lifecycle decision engine
Implement the smallest owner-controlled LEA/delegation verifier and pure authorization function returning exactly AUTHORIZED / NOT_AUTHORIZED / RECOVERY_REQUIRED / CLONE_CONFLICT. No networking and no DIST-04 mutation.

### VK-NODE-04 — lifecycle behavioral conformance
Bounded tests must cover at least:
- valid enrollment;
- invalid enrollment and malformed/unauthorized signer;
- LogicalIdentity impersonation;
- duplicate NodeIdentity;
- simultaneous identity proof;
- clone conflict for SSD/Seed/VM/directory copies;
- authorized identity split;
- migration and exclusive handoff;
- old-host return;
- same-NodeIdentity recovery;
- replacement-NodeIdentity recovery;
- missing recovery material;
- revocation and revoked reconnect;
- retirement;
- unknown node;
- legitimate hardware change;
- corrupted identity metadata;
- divergent clone history;
- two legitimate concurrent nodes;
- Android enrollment semantics;
- offline enrollment/recovery;
- Portable Seed recovery;
- history preservation;
- origin_sequence preservation/continuation rules.

### VK-NODE-05 — DIST-04 authorization adapter
Implement a narrow precondition adapter so DIST-04 replication executes only for AUTHORIZED peers. Demonstrate NOT_AUTHORIZED, RECOVERY_REQUIRED and CLONE_CONFLICT cannot enter ordinary replication. DIST-04 remains replication engine, never enrollment authority or secret provisioner.

### VK-NODE-06 — cross-platform identity conformance
At minimum two independent language implementations, with Python plus one non-Python implementation selected from C++/Rust/Kotlin. Verify identical enrollment signature verification, NodeIdentity binding, lifecycle/control-record interpretation and four-way authorization decisions using common vectors. Android/Kotlin compatibility must be demonstrated before Android runtime integration.

### VK-NODE-07 — Portable Seed / recovery integration contract tests
Verify Seed known-host, new-host, original-host-lost, replacement bootstrap, duplicated Seed, two active copies, damaged metadata and offline recovery behavior. Prove media identity never becomes NodeIdentity and SECRETS never enter DIST-04 synchronization.

## Required negative assertions across implementation gates

Every implementation gate must prove:

1. no newest timestamp winner;
2. no hardware/hostname/MAC/IP/path winner;
3. no arbitrary LogicalIdentity claim enrollment;
4. no silent clone continuation;
5. no retroactive history erasure on revocation/retirement;
6. no origin_sequence reassignment during authorized split;
7. no secret provisioning through SHARED_REPLICATED/DIST-04;
8. no enrollment/recovery/revocation authority inside DIST-04;
9. no OS-specific keystore is normative authority;
10. existing DIST-03/DIST-04 and Wire v1 behavior remains protected unless a separately authorized compatibility gate explicitly changes it.

## Evidence expectations

Each future implementation gate requires objective executable evidence, exact source/blob provenance, negative-path coverage, independent review and checkpoint. A report from another agent is not proof. Cross-platform conformance must compare common normative vectors, not merely independent unit-test success.
