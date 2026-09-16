# VK-NODE-WIRE-01 Checkpoint

Date: 2026-09-16
Status: `COMPLETE / SPECIFICATION_PASS / REVIEWER_PASS`

## Authority
Prerequisite: VK-NODE-01 `COMPLETE / ARCHITECTURE_PASS / REVIEWER_PASS`.
Existing VK Wire Profile v1 remains unchanged and retains prior WIRE-02/WIRE-05 conformance status.

## Accepted extension
Model: specialized Wire-v1 `DurableRecord` control records with `schema_version=1`, explicit `SHARED_REPLICATED`, closed payloads, unchanged causal primitives and unchanged Wire canonical/integrity rules.

Record types:
- NodeEnrollmentRecord
- NodeRevocationRecord
- NodeMigrationRecord
- NodeRecoveryRecord

Crypto representation: Ed25519 raw public key 32 bytes -> 64 lowercase hex; signature 64 bytes -> 128 lowercase hex. Signature domain is action-specific ASCII prefix + LF + canonical unsigned Wire-v1 record bytes. Crypto execution/conformance is NOT claimed.

Clone conflict: `DERIVED_DECISION_ONLY`; no fifth record required by this gate.
Migration: same NodeIdentity continues ACTIVE; old host incarnation closes.
Recovery: cannot bypass CLONE_CONFLICT; replacement requires separate valid enrollment/new origin namespace.
DIST-04: only externally determined AUTHORIZED peers may enter ordinary replication; DIST-04 unchanged.

## Accepted artifacts
- `decisions/VK_NODE_LIFECYCLE_CONTROL_RECORD_WIRE_EXTENSION_2026-09-16.md`
- `evidence/VK-NODE-WIRE-01/control_schema_profile_v1.json`
- `evidence/VK-NODE-WIRE-01/golden_vectors_v1.json`
- `evidence/VK-NODE-WIRE-01/rejection_vectors_v1.json`
- `evidence/VK-NODE-WIRE-01/lifecycle_transition_matrix_v1.json`
- `planning/VK_NODE_WIRE_01_IMPLEMENTATION_CONFORMANCE_BACKLOG_2026-09-16.md`
- `review/VK-NODE-WIRE-01.md` — PASS

## Vector scope
8 golden specification fixtures with deterministic canonical-byte/signing-domain byte identities and integrity digests; 28 rejection fixtures. Placeholder signatures are encoding-only and explicitly do not claim Ed25519 verification.

## Protected scope
No LIVE runtime change. No DIST-04 change. No existing Wire-v1 canonical/vector change. No NODE-02. No transport. No Windows-Pi communication. No distributed runtime activation. No Codex.

## Next gate
`VK-NODE-WIRE-02-PY` — bounded Python schema/codec validator extension and execution against NODE-WIRE-01 vectors, without runtime activation. NODE-02 cryptographic implementation remains a separate subsequent gate unless explicitly reordered by task authority.
