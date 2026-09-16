# VK-NODE-01 — Independent Architecture Review

Date: 2026-09-16
Verdict: `PASS / ARCHITECTURE_PASS / REVIEWER_PASS`

## Inputs reviewed

- `decisions/VK_NODE_IDENTITY_ENROLLMENT_TRUST_CLONE_RECOVERY_CONTRACT_2026-09-16.md`
- `evidence/VK-NODE-01/THREAT_FAILURE_MATRIX_2026-09-16.md`
- `planning/VK_NODE_01_IMPLEMENTATION_CONFORMANCE_BACKLOG_2026-09-16.md`

Prerequisites were read from current WORKSHOP main and are present: VK-DIST-03 COMPLETE/BEHAVIORAL_PASS/REVIEWER_PASS; VK-DIST-04 COMPLETE/BEHAVIORAL_PASS/REVIEWER_PASS; VK-WIRE-02 COMPLETE/BEHAVIORAL_PASS/REVIEWER_PASS; VK-WIRE-05 COMPLETE/CPP_PASS/CROSS_LANGUAGE_CONFORMANCE_PASS/REVIEWER_PASS. None was reopened or re-executed.

## Deterministic decision review

PASS. Two independent implementations can derive the same top-level decision from the normative evidence model:

1. If competing credible incarnations claim the same NodeIdentity and exclusive continuation is unresolved -> `CLONE_CONFLICT`.
2. Else if a recognized lineage cannot establish required identity/recovery material or safe continuation requires recovery authority -> `RECOVERY_REQUIRED`.
3. Else if enrollment is absent/unaccepted, identity proof invalid, lifecycle is REVOKED/RETIRED/SUSPENDED for ordinary replication, old host incarnation is migration-closed, or explicit denial applies -> `NOT_AUTHORIZED`.
4. Else if enrollment binding and identity proof are valid, lifecycle is ACTIVE and no applicable unresolved clone/revocation/migration conflict exists -> `AUTHORIZED`.

The ordering above prevents a duplicate valid key from being misclassified merely as AUTHORIZED and prevents damaged known identity from being treated as an unknown enrollment case.

## Required properties

- LogicalIdentity / NodeIdentity separation: PASS. One LogicalIdentity may enroll multiple distinct NodeIdentities; environment/media identifiers are non-authoritative.
- Enrollment authority: PASS. Owner-controlled LEA/delegated signed authority; arbitrary LogicalIdentity claim cannot join; ordinary ACTIVE operation needs no repeated human approval.
- Cryptographic binding: PASS. Per-node keypair, portable public verification identity, signed enrollment binding, identity proof, recovery/revocation relationships; Ed25519 baseline; no OS keystore is normative.
- Clone semantics: PASS. SSD/Seed/VM/directory/key duplication cannot silently create two active replicas; credible duplicate continuation is CLONE_CONFLICT with no automatic winner.
- Authorized split: PASS. New NodeIdentity/new future origin_sequence namespace; copied valid history/provenance unchanged.
- Migration: PASS after authoring correction. NodeIdentity lineage remains ACTIVE at target; only old host incarnation continuation is closed. This removes the potential contradiction of marking the same NodeIdentity RETIRED while continuing it at the target.
- Recovery: PASS. Same-identity recovery requires authenticated authority/non-conflict; otherwise replacement NodeIdentity enrollment. Missing authority is RECOVERY_REQUIRED.
- Revocation/retirement: PASS. Future authority is denied without erasing historical valid provenance.
- Portable Seed: PASS. Media is bootstrap/recovery material, never identity authority; duplicate active node secrets trigger clone handling.
- SECRETS isolation: PASS. Identity/recovery secrets are never SHARED_REPLICATED and DIST-04 is not secret provisioning.
- DIST-04 boundary: PASS. Only AUTHORIZED enters ordinary replication; DIST-04 consumes but cannot create/override identity authority.
- Cross-platform portability: PASS at architecture level. Ed25519 and versioned portable encodings are available to Python/C++/Kotlin/Rust and Windows/Linux x86/ARM without binding authority to an OS store. Executable cross-language conformance remains correctly deferred.
- Wall-clock/device winner semantics: ABSENT. Timestamp, newest hardware, hostname, MAC, IP, path, uptime and last-seen are explicitly non-authoritative.

## Wire extension assessment

PASS. All four assessed lifecycle-control objects are correctly classified `BOUNDED_WIRE_EXTENSION_REQUIRED`: NodeEnrollmentRecord, NodeRevocationRecord, NodeMigrationRecord, NodeRecoveryRecord. Current Wire Profile v1 and vectors are not modified. The backlog defines a separate bounded extension gate with closed schemas, canonical/signature rules, causal/conflict semantics and vectors.

## Threat/failure coverage

PASS. Matrix covers all required scenarios: returning/new/interrupted enrollment, SSD/Seed/VM/directory clones, simultaneous duplicate identity, migration/old host, lost/revoked/retired nodes, Seed recovery, missing recovery authority, LogicalIdentity impersonation, hardware change, corrupted metadata, divergent clone history, legitimate concurrent nodes, Android, and offline enrollment/recovery. History/provenance and replication eligibility are explicit.

## Protected scope

PASS. No LIVE runtime modification, DIST-04 modification, Wire Profile/vector modification, NODE-02 implementation, transport implementation, Windows-Pi connection, distributed communication activation, or Codex use occurred in NODE-01.

## Conclusion

The persisted NODE-01 architecture is sufficient and deterministic for independent implementation. The next dependency is the bounded lifecycle-control Wire extension gate; implementation must not skip directly to runtime enrollment or transport.

Grant: `VK-NODE-01 = ARCHITECTURE_PASS / REVIEWER_PASS`.
