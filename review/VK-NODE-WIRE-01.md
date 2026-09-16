# VK-NODE-WIRE-01 — Independent Review

Date: 2026-09-16
Verdict: `PASS / SPECIFICATION_PASS / REVIEWER_PASS`

## Reviewed persisted authority
Reviewer inspected the repository-persisted normative specification, machine-readable profile, golden/rejection vectors, transition matrix and conformance backlog after persistence.

## Findings
1. **Wire Profile v1 unchanged — PASS.** Extension specializes existing DurableRecord and reuses existing canonical UTF-8/JSON, identifiers, origin_sequence, parents, StateClass and SHA-256 integrity. No second causal system and no Wire-v2 semantics are introduced.
2. **Required records — PASS.** NodeEnrollmentRecord, NodeRevocationRecord, NodeMigrationRecord and NodeRecoveryRecord each have closed payload schemas.
3. **Cryptographic representation — PASS.** Ed25519 public keys are exactly 32 raw bytes represented as 64 lowercase hex; signatures exactly 64 raw bytes as 128 lowercase hex. No OS-specific object/key-store representation is normative.
4. **Signing domain — PASS.** Exact domain prefix + LF + unchanged Wire-v1 canonical UTF-8 of the complete unsigned record after removal of only top-level integrity_digest and payload.signature. LogicalIdentity and record_type remain inside signed canonical content. Four action domains are distinct.
5. **Integrity/authenticity separation — PASS.** Signature-domain construction and DurableRecord integrity are separate; integrity includes the transmitted signature, while signature message excludes signature and integrity_digest. Specification does not claim crypto verification.
6. **Migration correction — PASS.** Migration keeps subject NodeIdentity ACTIVE and closes only old host incarnation. Incarnation ID is opaque/non-hardware authority.
7. **Recovery/clone — PASS.** SAME_NODE recovery cannot bypass unresolved CLONE_CONFLICT; replacement recovery requires a separately valid replacement enrollment and fresh origin namespace.
8. **SECRETS/StateClass — PASS.** Lifecycle records are explicitly SHARED_REPLICATED because all authorized peers require common lifecycle authority evidence; private/recovery secret material is forbidden.
9. **Replay/conflict — PASS.** Existing DurableRecord replay/record/sequence/gap semantics remain primary; lifecycle-specific action/binding/authority conflicts are deterministic; wall clock never selects a winner.
10. **Vectors — PASS for specification gate.** Eight golden fixtures cover first/additional enrollment, revocation, migration, same-node recovery, replacement enrollment/recovery link, authorized split and causal parents. Each fixture deterministically materializes exact canonical Wire-v1 bytes and signing-domain bytes; expected lengths and SHA-256 byte identities are persisted. Signatures are explicitly encoding-only zero placeholders, so no cryptographic PASS is falsely claimed. Twenty-eight rejection vectors cover required structural, crypto-encoding, causal, authority, clone and transition failures. Actual Ed25519 signature vectors are correctly deferred to NODE-02/crypto conformance.
11. **Cross-platform — PASS.** Required operations are UTF-8, canonical JSON, SHA-256, raw Ed25519 bytes/lowercase hex and deterministic field rules, portable across Python/C++/Kotlin/Rust.
12. **DIST-04 boundary — PASS.** Lifecycle validation/authorization occurs before ordinary replication; only AUTHORIZED reaches DIST-04. DIST-04 is not modified or made enrollment authority.
13. **Transport independence — PASS.** No HTTP/TCP/IP/path/OS/device identity is part of schema authority.

## Scope verification
No LIVE runtime modification, no DIST-04 modification, no existing Wire-v1/vector modification, no NODE-02 implementation, no transport, no distributed runtime activation, no Codex.

## Conclusion
The persisted extension is sufficient for two independent implementations to reproduce schema validation, canonical byte identity, integrity digest, signing-domain byte identity, lifecycle interpretation and deterministic rejection categories without redefining Wire Profile v1. Cross-language implementation conformance is NOT claimed by this gate.
