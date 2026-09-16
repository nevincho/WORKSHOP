# VK-NODE-01 — Node Identity Enrollment / Trust / Clone-Recovery Contract

Date: 2026-09-16
Status: NORMATIVE ARCHITECTURE

## 1. Scope and invariants

This contract defines identity and authorization semantics for owner-controlled VK nodes. It does not implement transport, runtime integration, Wire changes, secret provisioning, or NODE-02.

Normative invariants:
1. `LogicalIdentity != NodeIdentity`.
2. One LogicalIdentity MAY have many explicitly enrolled NodeIdentities.
3. A NodeIdentity is a durable cryptographic lineage identity, not a hostname, device fingerprint, MAC/IP address, filesystem path, disk, VM, Portable Seed, runtime directory, or host incarnation.
4. Wall-clock time and device recency have zero authority for identity conflict resolution.
5. Historical valid provenance is immutable. Revocation, retirement, migration, recovery, and authorized split do not rewrite prior records.
6. `SECRETS != SHARED_REPLICATED`. DIST-04 synchronization is never secret provisioning.
7. DIST-04 consumes an authorization decision; DIST-04 is not enrollment, recovery, migration, or revocation authority.

## 2. Identifiers and cryptographic binding

Each enrolled node has `logical_identity_id`, a unique stable `node_identity_id`, `node_public_key`, secret `node_private_key`, `enrollment_record_ref`, and optional `recovery_binding`. NodeIdentity identifiers MUST be independent of hostname/hardware/network/storage identifiers.

Minimum implementation profile is Ed25519 unless replaced by a later bounded cryptographic-profile gate. Standard raw/public-key or explicitly versioned portable encodings are normative; OS key stores MAY protect local material but cannot define identity semantics.

The enrollment authorization signature MUST cover a canonical statement containing at least profile version, logical_identity_id, node_identity_id, node_public_key, enrollment event identifier, authorization type, optional predecessor/recovery/migration reference, and initial trust state. Ordinary identity proof is a node-key signature over a fresh protocol challenge/context. Replay resistance is implementation work; wall-clock ordering is prohibited as causal authority.

## 3. Lifecycle

Normative NodeIdentity lifecycle states:
- `UNENROLLED`: no accepted enrollment binds the identity.
- `ACTIVE`: enrolled/trusted/not revoked or retired and eligible to prove identity.
- `SUSPENDED`: enrolled lineage retained but ordinary replication withheld temporarily.
- `RECOVERY_REQUIRED`: recognized lineage but proof/material is insufficient or damaged.
- `CLONE_CONFLICT`: competing live incarnations claim the same NodeIdentity without proven exclusive continuation.
- `REVOKED`: future authority permanently withdrawn; historical provenance remains valid.
- `RETIRED`: NodeIdentity lineage intentionally closed; historical provenance remains valid.

Allowed transitions:
- UNENROLLED -> ACTIVE: successful enrollment only.
- ACTIVE -> SUSPENDED: owner authority or deterministic safety policy.
- SUSPENDED -> ACTIVE: owner authority after validation.
- ACTIVE/SUSPENDED -> RECOVERY_REQUIRED: loss/damage of proof or recovery precondition.
- RECOVERY_REQUIRED -> ACTIVE: authenticated same-NodeIdentity recovery only.
- ACTIVE/SUSPENDED/RECOVERY_REQUIRED -> CLONE_CONFLICT: credible duplicate-lineage evidence.
- CLONE_CONFLICT -> ACTIVE: owner-authorized resolution establishes exactly one continuing incarnation; other incarnations lose continuation authority or become new enrolled NodeIdentities.
- ACTIVE/SUSPENDED/RECOVERY_REQUIRED/CLONE_CONFLICT -> REVOKED: owner revocation authority.
- ACTIVE/SUSPENDED -> RETIRED: explicit permanent closure of the NodeIdentity lineage.
- REVOKED and RETIRED are terminal for that NodeIdentity.

Migration does NOT retire the NodeIdentity: it closes the old host incarnation's continuation authority while the same NodeIdentity remains/returns ACTIVE at the target. Host-incarnation closure is evidenced by NodeMigrationRecord, not by assigning the NodeIdentity lifecycle RETIRED.

No automatic transition may select a winner by timestamp, uptime, hardware novelty, hostname, MAC, IP, disk identity, path, or last-seen status.

## 4. Enrollment authority

The owner-controlled VK installation has a `LogicalIdentity Enrollment Authority` (LEA): a small separately protected signing/recovery root controlled by the owner. It MAY be offline or MAY delegate bounded enrollment/recovery/revocation authority to an explicitly authorized signer. Enterprise PKI is not required.

A durable NodeIdentity is accepted only when its enrollment statement is signed by LEA or a currently valid delegated signer chaining to LEA. Claiming logical_identity_id alone yields UNENROLLED / NOT_AUTHORIZED. Already enrolled ACTIVE nodes need no repeated human approval for ordinary operation; they prove possession of their node key and accepted enrollment/current lifecycle evidence. Ordinary DIST-04 peers gain no enrollment authority merely by being ACTIVE.

## 5. First-node bootstrap

1. Generate LEA/recovery root independently of runtime replication storage.
2. Create stable logical_identity_id.
3. Generate fresh first-node keypair and node_identity_id.
4. LEA signs first enrollment and establishes ACTIVE.
5. Initialize the replication frontier/checkpoint using the existing authoritative empty/bootstrap semantics; do not fabricate prior history.
6. Preserve LEA/recovery authority outside the first physical machine.

Loss of the first machine MUST NOT destroy LogicalIdentity. At minimum logical_identity_id, LEA/recovery authority, cryptographic profile/version and recovery instructions survive separately. Same-NodeIdentity recovery requires intentionally provisioned recovery capability; otherwise enroll a replacement NodeIdentity.

## 6. Additional-node enrollment

A new host starts UNENROLLED, generates fresh per-node key material and unique node_identity_id, and becomes ACTIVE only after a signed enrollment is durably accepted. It then receives a verified bootstrap frontier/checkpoint and valid SHARED_REPLICATED history. Existing provenance/origin sequences remain unchanged. The new NodeIdentity starts its own future origin_sequence namespace and never continues another node's namespace except explicit same-NodeIdentity migration/recovery.

Interrupted enrollment is atomic at the authority boundary: no accepted signed enrollment means UNENROLLED. Identical accepted enrollment replay is idempotent; conflicting binding for the same node_identity_id is NOT_AUTHORIZED pending owner resolution.

SECRETS are provisioned separately. DIST-04 shared history MUST NOT carry node/LEA/recovery private keys, credentials or other SECRETS.

## 7. Clone detection

Copying SSD, Portable Seed, VM, disk image, VK directory/runtime or identity metadata MUST NOT authorize two active incarnations of one NodeIdentity. Credible simultaneous duplicate continuation produces `CLONE_CONFLICT`. Evidence includes mutually incompatible signed continuation, concurrent proof sessions from independently established incarnations, or divergent valid records in the same NodeIdentity/origin_sequence namespace that cannot be one ordered lineage.

On CLONE_CONFLICT replication is withheld; neither claimant wins automatically; both valid histories/evidence are preserved; owner resolution must establish one continuing incarnation, revoke/retire the lineage, migrate exclusively, or perform authorized identity split. Hardware/network identifiers are diagnostic only.

## 8. Authorized identity split

Copied valid history becomes a legitimate additional node only through NEW NodeIdentity enrollment. Preserve prior SHARED_REPLICATED history/provenance unchanged; generate new keypair/node_identity_id; LEA signs `AUTHORIZED_SPLIT` provenance referencing source lineage/checkpoint; new node starts a new future origin_sequence namespace; old records are never relabeled/re-signed. Source node MAY remain ACTIVE.

## 9. Migration

Migration is exclusive continuation of the SAME NodeIdentity lineage on another execution/storage environment, distinct from enrollment and cloning. A signed migration intent binds node_identity_id, old incarnation reference, target incarnation proof, handoff frontier/checkpoint and exclusivity transition. Old incarnation continuation authority MUST be cryptographically/policy closed before target continuation is accepted. The NodeIdentity itself remains ACTIVE at the target and continues its origin_sequence from the verified contiguous frontier.

Old-host return is NOT_AUTHORIZED as an execution incarnation. If old and target both appear capable of continuation because exclusivity cannot be established, result is CLONE_CONFLICT. Migration never rewrites history and never chooses by host recency.

## 10. Recovery

### Same-NodeIdentity recovery
Allowed only when separately protected recovery authority authenticates the existing node_identity_id and establishes no competing active incarnation. Applies to OS reinstall, runtime loss, recoverable disk loss or hardware replacement. A recovery statement binds old identity, replacement public key/material, recovery event and verified frontier; old compromised key loses future authority. Existing provenance remains unchanged and future origin_sequence continues the same NodeIdentity namespace.

### Replacement-NodeIdentity recovery
When same-identity continuation cannot be safely proven, enroll a NEW NodeIdentity with `REPLACEMENT_RECOVERY` provenance. Preserve valid shared history; future records use the new origin_sequence namespace. Revoke or retire the unsafe/lost old NodeIdentity as appropriate.

Missing LEA/recovery material yields RECOVERY_REQUIRED. Peers, copied Seeds, hardware identifiers, timestamps and shared history cannot manufacture enrollment/recovery authority.

## 11. Revocation and retirement

Revocation permanently withdraws future authority; retirement intentionally and permanently closes a NodeIdentity lineage. Both preserve historical provenance. Revoked reconnect and retired-lineage reconnect are NOT_AUTHORIZED even with an old valid key. Records validly created while authorized remain historical evidence. Revocation evidence is authenticated by LEA/delegated authority and cannot be overridden by wall-clock recency.

An old migrated host is different: its host incarnation is migration-closed while the NodeIdentity remains ACTIVE at the authorized target; the old host is NOT_AUTHORIZED to continue that lineage.

## 12. Portable Seed

Portable Seed is recovery/bootstrap media, never NodeIdentity.
- Known host: Seed may restore runtime/bootstrap material; enrolled identity still requires valid proof.
- New host: Seed alone leaves UNENROLLED; enroll or authenticate recovery/migration.
- Original host lost: Seed restores code/history/recovery metadata; same identity requires recovery authority, otherwise replacement enrollment.
- Replacement bootstrap: restore valid history, then establish identity separately.
- Seed copied/two copies: duplication grants no authority; concurrent use of duplicated node secret creates CLONE_CONFLICT.
- Damaged identity metadata: RECOVERY_REQUIRED unless authenticated recovery reconstructs it.
- Offline enrollment/recovery is allowed only when all required signed authority, applicable control state, identity proof and deterministic bootstrap evidence are locally available; otherwise remain UNENROLLED/RECOVERY_REQUIRED.

## 13. SECRETS isolation

Node/LEA/delegation private keys, recovery secrets and provisioning payloads are SECRETS, never SHARED_REPLICATED. DIST-04 MUST exclude/reject them under existing StateClass semantics. Secret provisioning is a separate bounded mechanism. Public lifecycle-control evidence may become synchronization-relevant only after a separately validated Wire extension.

## 14. DIST-04 authorization boundary

Identity authorization evaluates:
`NodeIdentity + lifecycle/trust state + enrollment proof + identity proof + applicable revocation/migration/recovery evidence -> decision`.

Decisions:
- `AUTHORIZED`: accepted enrollment, valid identity proof, ACTIVE, no unresolved clone/revocation/migration conflict.
- `NOT_AUTHORIZED`: unknown/unaccepted enrollment, invalid proof, REVOKED/RETIRED lineage, migration-closed old incarnation, or explicit denial.
- `RECOVERY_REQUIRED`: recognized lineage but required proof/recovery material/metadata missing or damaged, or safe continuation needs recovery authority.
- `CLONE_CONFLICT`: credible competing incarnations claim one NodeIdentity and exclusivity is unresolved.

Only AUTHORIZED permits ordinary DIST-04 participation. DIST-04 consumes this decision and MUST NOT enroll, recover, revoke, migrate, choose clone winners, or provision secrets.

## 15. Wire extension assessment

Wire Profile v1 is unchanged. Durable independently verifiable lifecycle-control evidence requires bounded new normative objects:
- `NodeEnrollmentRecord`: `BOUNDED_WIRE_EXTENSION_REQUIRED` — signed LogicalIdentity/NodeIdentity/public-key binding, authorization chain/type, initial lifecycle, event ID and optional predecessor/split/recovery reference.
- `NodeRevocationRecord`: `BOUNDED_WIRE_EXTENSION_REQUIRED` — signed irreversible future-authority withdrawal; history remains valid.
- `NodeMigrationRecord`: `BOUNDED_WIRE_EXTENSION_REQUIRED` — signed exclusive host-incarnation handoff binding NodeIdentity, old/target incarnation evidence and handoff frontier/checkpoint.
- `NodeRecoveryRecord`: `BOUNDED_WIRE_EXTENSION_REQUIRED` — signed same-identity key recovery/rotation or replacement-recovery relationship with verified frontier.

Next bounded Wire-extension gate must define closed schemas, canonicalization/digest/signature preimages, versioning, exact validation/rejection categories, causal ordering independent of wall-clock, idempotency/conflict rules, golden/rejection vectors, Python+C++ conformance impact, and compatibility with existing Wire v1 without modifying current vectors in place. No extension is implemented here.
