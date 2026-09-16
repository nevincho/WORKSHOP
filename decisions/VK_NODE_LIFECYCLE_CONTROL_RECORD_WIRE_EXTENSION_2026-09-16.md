# VK-NODE-WIRE-01 — Node Lifecycle Control-Record Wire Extension

Date: 2026-09-16
Status: NORMATIVE SPECIFICATION — NO IMPLEMENTATION
Authority: VK-NODE-01 and VK Distributed Wire Profile v1.

## 1. Extension model
Wire Profile v1 canonical JSON, UTF-8, integer, identifier, versioning and integrity rules remain unchanged. Lifecycle authority is represented as specialized `DurableRecord` objects, reusing `record_id`, `vk_identity_id`, `origin_node_id`, `origin_sequence`, `state_class`, `parents`, `provenance`, `schema_version`, `observed_at`, and `integrity_digest`. No second causal system is created.

The four permitted `record_type` values are exactly `NodeEnrollmentRecord`, `NodeRevocationRecord`, `NodeMigrationRecord`, and `NodeRecoveryRecord`. For these record types `schema_version` is the lifecycle control schema version and MUST equal integer 1. `state_class` MUST equal `SHARED_REPLICATED`. `claim_class` and `admission_state` MUST be null. `payload` is a closed record-specific object. Unknown payload fields are `UNSUPPORTED_REQUIRED_FIELD`.

## 2. Common lifecycle payload fields
Every lifecycle payload contains:
- `action_id`: v1 identifier, unique lifecycle action identifier.
- `issuer_node_id`: v1 identifier naming the authorized signing NodeIdentity or LEA identity label.
- `issuer_public_key`: exactly 64 lowercase hexadecimal ASCII characters encoding the 32 raw Ed25519 public-key bytes.
- `subject_node_id`: v1 identifier for the lifecycle subject.
- `authorization_ref`: v1 identifier referring to the enrollment/delegation/recovery authority basis; for first-root enrollment this is the LEA root identifier.
- `signature`: exactly 128 lowercase hexadecimal ASCII characters encoding the 64 raw Ed25519 signature bytes.

Private keys, recovery secrets, tokens, passwords and arbitrary secret payloads are forbidden. Lifecycle records are public authority evidence and explicitly SHARED_REPLICATED.

`origin_node_id` identifies the causal record-producing namespace and does not by itself grant issuer authority. `issuer_node_id` identifies the asserted signing authority. Authorization verification is a later gate.

## 3. Cryptographic representation and signing domain
Ed25519 public keys use lowercase hex of exactly 32 raw bytes; signatures use lowercase hex of exactly 64 raw bytes. No prefixes, whitespace, base64 variants, PEM, platform objects, or key-store identifiers are normative.

The signature is NOT over the transmitted JSON including `signature` or `integrity_digest`.

For each lifecycle DurableRecord, construct `unsigned_record` by removing exactly top-level `integrity_digest` and exactly `payload.signature`, leaving every other field unchanged. Canonicalize `unsigned_record` using Wire Profile v1 canonical JSON. Let `C` be those canonical UTF-8 bytes.

The exact Ed25519 message is ASCII domain bytes followed by one LF byte (`0x0a`) followed by C:
- Enrollment: `VK-NODE-CONTROL-V1/ENROLLMENT` + LF + C
- Revocation: `VK-NODE-CONTROL-V1/REVOCATION` + LF + C
- Migration: `VK-NODE-CONTROL-V1/MIGRATION` + LF + C
- Recovery: `VK-NODE-CONTROL-V1/RECOVERY` + LF + C

Because C contains `vk_identity_id`, `record_type`, subject and issuer fields, signatures are bound to the LogicalIdentity and exact object type/content. Domain prefix additionally prevents cross-action signature reuse.

After signature insertion, Wire integrity is computed by the existing DurableRecord rule: remove exactly top-level `integrity_digest`, canonicalize the remaining complete record INCLUDING `payload.signature`, SHA-256, lowercase 64-hex digest. Thus integrity and authenticity are distinct.

## 4. Validation order
1. Wire-v1 UTF-8/JSON/canonical-byte acceptance.
2. `wire_profile_version == 1` and closed DurableRecord/lifecycle schema validation.
3. StateClass/identifier/sequence/lineage validation.
4. DurableRecord integrity verification.
5. Ed25519 key/signature textual encoding and exact decoded lengths.
6. Lifecycle payload semantic consistency and referenced-parent/control evidence availability.
7. Construct exact signing-domain bytes.
8. Cryptographic signature verification — REQUIRED by later implementation gate, NOT claimed here.
9. Enrollment/lifecycle authority evaluation and four-way NODE-01 authorization decision outside DIST-04.

## 5. NodeEnrollmentRecord payload
Closed fields:
`action_id`, `issuer_node_id`, `issuer_public_key`, `subject_node_id`, `subject_public_key`, `authorization_ref`, `enrollment_kind`, `initial_state`, `origin_namespace`, `bootstrap_checkpoint_ref`, `predecessor_node_id`, `predecessor_checkpoint_ref`, `signature`.

Rules:
- `subject_public_key`: 64 lowercase hex.
- `enrollment_kind`: exactly `FIRST_NODE`, `ADDITIONAL_NODE`, `AUTHORIZED_SPLIT`, or `REPLACEMENT_RECOVERY`.
- `initial_state`: exactly `ACTIVE`; no enrollment record grants another lifecycle state.
- `origin_namespace`: MUST equal `subject_node_id`; new NodeIdentity means new future origin_sequence namespace.
- `bootstrap_checkpoint_ref`: nullable v1 identifier; references bootstrap state but does not embed replica state.
- `predecessor_node_id` and `predecessor_checkpoint_ref`: both null for FIRST_NODE/ADDITIONAL_NODE; both required non-null for AUTHORIZED_SPLIT/REPLACEMENT_RECOVERY.
- FIRST_NODE issuer may be the LEA identity label rather than an enrolled node; its authority basis is `authorization_ref`.
- inherited history is never rewritten and SECRETS are absent.

## 6. NodeRevocationRecord payload
Closed fields:
`action_id`, `issuer_node_id`, `issuer_public_key`, `subject_node_id`, `authorization_ref`, `reason_class`, `prior_control_ref`, `target_state`, `signature`.

Rules:
- `reason_class`: `LOST`, `COMPROMISED`, `OWNER_REVOKED`, or `OTHER`.
- `prior_control_ref`: required v1 identifier referencing accepted subject enrollment/control state.
- `target_state`: exactly `REVOKED`.
- Revocation withdraws future ordinary authorization only; historical valid provenance remains valid.
- No timestamp field determines revocation precedence.

## 7. NodeMigrationRecord payload
Host incarnation is a minimal opaque identifier: `incarnation_id`, a v1 identifier generated for an execution incarnation. It is NOT a hardware fingerprint and carries no authority by itself.

Closed fields:
`action_id`, `issuer_node_id`, `issuer_public_key`, `subject_node_id`, `authorization_ref`, `old_incarnation_id`, `new_incarnation_id`, `handoff_checkpoint_ref`, `prior_control_ref`, `target_state`, `signature`.

Rules:
- old/new incarnation IDs are distinct.
- `subject_node_id` is the SAME continuing NodeIdentity.
- `handoff_checkpoint_ref` and `prior_control_ref` are required identifiers.
- `target_state` is exactly `ACTIVE`; it describes the continuing NodeIdentity after exclusive handoff.
- The migration closes authority of `old_incarnation_id`; it MUST NOT revoke/retire/replace `subject_node_id`.
- Exclusivity and clone checks are lifecycle semantics evaluated before acceptance; hardware observations are non-authoritative.

## 8. NodeRecoveryRecord payload
Closed fields:
`action_id`, `issuer_node_id`, `issuer_public_key`, `subject_node_id`, `authorization_ref`, `recovery_kind`, `prior_control_ref`, `recovery_checkpoint_ref`, `old_public_key`, `new_public_key`, `replacement_node_id`, `replacement_enrollment_ref`, `target_state`, `signature`.

Rules:
- `recovery_kind`: `SAME_NODE` or `REPLACEMENT_NODE`.
- `prior_control_ref` and `recovery_checkpoint_ref` required.
- `old_public_key` and `new_public_key`: 64 lowercase hex.
- SAME_NODE: `replacement_node_id` and `replacement_enrollment_ref` MUST be null; subject remains same NodeIdentity; `target_state` exactly ACTIVE; future origin namespace remains subject_node_id.
- REPLACEMENT_NODE: `replacement_node_id` and `replacement_enrollment_ref` required; replacement_node_id MUST differ from subject_node_id; referenced enrollment MUST be a valid `NodeEnrollmentRecord` with enrollment_kind REPLACEMENT_RECOVERY; `target_state` exactly RETIRED or REVOKED for the old subject according to accepted authority evidence. Replacement uses its own origin namespace.
- Recovery record cannot resolve unresolved CLONE_CONFLICT by itself. Required clone-resolution authority/evidence must already be established by lifecycle authority; otherwise decision remains CLONE_CONFLICT.

## 9. Lifecycle transition authority
- NodeEnrollmentRecord: UNENROLLED -> ACTIVE only.
- NodeRevocationRecord: ACTIVE/SUSPENDED/RECOVERY_REQUIRED/CLONE_CONFLICT -> REVOKED.
- NodeMigrationRecord: exclusive host-incarnation handoff while NodeIdentity remains/returns ACTIVE; it does not terminate NodeIdentity.
- NodeRecoveryRecord SAME_NODE: RECOVERY_REQUIRED -> ACTIVE only after clone-safe recovery authority.
- NodeRecoveryRecord REPLACEMENT_NODE: closes old subject to RETIRED/REVOKED and links to separately enrolled replacement NodeIdentity.
- SUSPENDED transitions and CLONE_CONFLICT detection/resolution are lifecycle decisions; these four records do not create a general arbitrary state-transition mechanism.

## 10. Clone conflict
`CLONE_CONFLICT = DERIVED_DECISION_ONLY` for this extension. It is derived from competing identity/lineage evidence and does not require a fifth control record to detect or withhold replication. A future durable clone-resolution/audit record MAY be separately proposed if operational audit requirements justify it; it is not required for the four schemas.

## 11. Replay/conflict/causal rules
Existing DurableRecord rules apply first: exact record_id+digest replay = IDEMPOTENT_REPLAY; same record_id different digest = RECORD_ID_CONFLICT; occupied origin_node_id+origin_sequence with different record = ORIGIN_SEQUENCE_CONFLICT; missing causal parents = HELD_SEQUENCE_GAP/dependency hold.

Lifecycle action rules add:
- same `action_id` with different lifecycle content = `LIFECYCLE_ACTION_CONFLICT`;
- conflicting accepted enrollment binding same subject_node_id to different public keys without valid recovery/split authority = `IDENTITY_BINDING_CONFLICT`;
- a revoked subject cannot regain ACTIVE via migration/enrollment/recovery = `LIFECYCLE_AUTHORITY_CONFLICT`;
- recovery conflicting with causally established revocation is rejected;
- migration conflicting with causally established revocation is rejected;
- duplicate semantically identical migration/recovery with different record IDs is `LIFECYCLE_ACTION_CONFLICT`, not a second transition;
- causally unordered conflicting lifecycle actions produce `LIFECYCLE_AUTHORITY_CONFLICT`/CLONE_CONFLICT as applicable and are preserved for resolution; wall clock never chooses.
- an old record arriving later is evaluated against causal references/frontier and authority state, never arrival time.

## 12. Error model extension
Reuse Wire-v1 errors wherever applicable. Add only:
- `INVALID_CRYPTO_ENCODING`: malformed/non-lowercase-hex key/signature or wrong decoded length.
- `INVALID_CONTROL_REFERENCE`: missing, self, wrong-type, wrong-subject or semantically incompatible lifecycle reference.
- `INVALID_CONTROL_SEMANTICS`: schema-valid object whose fixed lifecycle invariants conflict (e.g. migration terminates NodeIdentity; replacement reuses origin namespace; forbidden state transition).
- `UNAUTHORIZED_ISSUER`: issuer/delegation/recovery authority is not accepted.
- `INVALID_SIGNATURE`: later crypto verifier reports signature mismatch.
- semantic outcomes `LIFECYCLE_ACTION_CONFLICT`, `IDENTITY_BINDING_CONFLICT`, `LIFECYCLE_AUTHORITY_CONFLICT`.

Wrong `vk_identity_id` at peer context boundary is `INVALID_CONTROL_SEMANTICS`. Unknown record_type = INVALID_ENUM when parsed as lifecycle control record. Unsupported lifecycle `schema_version` = UNSUPPORTED_VERSION. Unknown required payload field = UNSUPPORTED_REQUIRED_FIELD.

## 13. DIST-04 boundary
Lifecycle control records are processed by the identity/lifecycle authority layer, not ordinary memory admission. A remote peer must have validated enrollment/control evidence, cryptographic identity proof, and a NODE-01 decision of exactly AUTHORIZED before ordinary DIST-04 replicated state is accepted. NOT_AUTHORIZED, RECOVERY_REQUIRED and CLONE_CONFLICT are hard precondition failures for ordinary replication. DIST-04 remains unchanged and cannot issue or override lifecycle authority.

## 14. Transport/platform independence
Schemas and signing domains contain no HTTP/WebSocket/TCP/IP/port/path/OS/hardware authority. Canonical bytes and signature-domain bytes are reproducible in Python, C++, Kotlin and Rust.
