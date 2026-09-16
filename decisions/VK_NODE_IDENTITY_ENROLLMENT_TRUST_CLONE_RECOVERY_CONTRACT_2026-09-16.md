# VK-NODE-01 — Node Identity Enrollment / Trust / Clone-Recovery Contract

Date: 2026-09-16
Status: NORMATIVE ARCHITECTURE

## 1. Scope and invariants

This contract defines identity and authorization semantics for owner-controlled VK nodes. It does not implement transport, runtime integration, Wire changes, secret provisioning, or NODE-02.

Normative invariants:

1. `LogicalIdentity != NodeIdentity`.
2. One LogicalIdentity MAY have many explicitly enrolled NodeIdentities.
3. A NodeIdentity is a durable cryptographic lineage identity, not a hostname, device fingerprint, MAC/IP address, filesystem path, disk, VM, Portable Seed, or runtime directory.
4. Wall-clock time and device recency have zero authority for identity conflict resolution.
5. Historical valid provenance is immutable. Revocation, retirement, migration, recovery, and authorized split do not rewrite prior records.
6. `SECRETS != SHARED_REPLICATED`. DIST-04 synchronization is never secret provisioning.
7. DIST-04 consumes an authorization decision; DIST-04 is not enrollment, recovery, migration, or revocation authority.

## 2. Identifiers and cryptographic binding

Each enrolled node has:

- `logical_identity_id`: stable identifier of the VK LogicalIdentity.
- `node_identity_id`: stable unique identifier for one node lineage. It MUST be generated independently of hostname/hardware/network/storage identifiers.
- `node_public_key`: public verification key for that NodeIdentity.
- `node_private_key`: private signing key held as SECRETS and never replicated through DIST-04.
- `enrollment_record_ref`: reference to the authoritative enrollment event binding logical_identity_id, node_identity_id and node_public_key.
- `recovery_binding`: reference/digest identifying separately protected recovery authority/material where configured.

Minimum algorithm profile for implementation gates MUST use a portable, deterministic, widely implemented signature primitive. Ed25519 is the required baseline unless a later bounded cryptographic-profile gate replaces it. Implementations MUST exchange standard raw/public-key or explicitly versioned portable encodings and MUST NOT make OS-specific key-store representation normative. Secure OS stores MAY protect local material but cannot define identity semantics.

`node_identity_id` MUST be bound by an enrollment authorization signature over a canonical enrollment statement containing at least: contract/profile version, logical_identity_id, node_identity_id, node_public_key, enrollment event identifier, authorization type, predecessor/recovery/migration reference when applicable, and initial trust state. The signing authority is defined below. Identity proof for ordinary operation is a signature by the enrolled node key over a fresh protocol challenge/context. Replay resistance belongs to the future implementation/conformance gate; wall-clock ordering is prohibited as causal authority.

## 3. Lifecycle

Normative lifecycle states:

- `UNENROLLED`: no accepted enrollment binds the presented NodeIdentity to the LogicalIdentity.
- `ACTIVE`: enrolled, trusted, not revoked/retired, and permitted to prove identity for ordinary replication.
- `SUSPENDED`: enrolled lineage retained but ordinary replication authorization withheld temporarily.
- `RECOVERY_REQUIRED`: enrolled lineage exists but current proof/material is insufficient or damaged; ordinary replication withheld pending recovery.
- `CLONE_CONFLICT`: two or more live claimants present valid material for the same NodeIdentity without an authorized migration handoff proving exclusive continuation.
- `REVOKED`: authority permanently withdrawn. Historical provenance remains valid; this NodeIdentity can never return to ACTIVE.
- `RETIRED`: intentionally closed lineage. Historical provenance remains valid; ordinary operation cannot resume under this NodeIdentity.

Allowed transitions:

- UNENROLLED -> ACTIVE: successful enrollment only.
- ACTIVE -> SUSPENDED: owner enrollment authority or deterministic safety policy on unresolved availability/security condition.
- SUSPENDED -> ACTIVE: owner enrollment authority after validation.
- ACTIVE/SUSPENDED -> RECOVERY_REQUIRED: loss/damage of identity proof or recovery precondition.
- RECOVERY_REQUIRED -> ACTIVE: authenticated same-NodeIdentity recovery only.
- ACTIVE/SUSPENDED/RECOVERY_REQUIRED -> CLONE_CONFLICT: credible simultaneous duplicate-lineage evidence.
- CLONE_CONFLICT -> ACTIVE: only after owner-authorized resolution identifies exactly one continuing incarnation or performs authorized split/migration; all other claimants lose that lineage authority.
- ACTIVE/SUSPENDED/RECOVERY_REQUIRED/CLONE_CONFLICT -> REVOKED: owner revocation authority.
- ACTIVE/SUSPENDED -> RETIRED: owner retirement authority or completed migration closure.
- REVOKED and RETIRED are terminal for that NodeIdentity.

No automatic transition may select a winner by timestamp, uptime, hardware novelty, hostname, MAC, IP, disk identity, path, or last-seen status.

## 4. Enrollment authority

The owner-controlled VK installation has a `LogicalIdentity Enrollment Authority` (LEA): a small, separately protected signing authority/recovery root controlled by the owner. It MAY be implemented as an offline recovery key or owner-approved existing active node delegated by a signed LEA policy. Enterprise PKI is not required.

A durable NodeIdentity is accepted only when an enrollment statement is signed by the LEA or by an explicitly delegated currently valid enrollment signer whose delegation chains to the LEA. A node claiming only logical_identity_id is UNENROLLED and NOT_AUTHORIZED.

Already enrolled ACTIVE nodes do not require repeated human approval for ordinary operation; they prove possession of their node private key and present the accepted enrollment binding and current non-revoked lifecycle evidence.

Delegation MUST be explicit, bounded to enrollment/recovery actions, and revocable. Ordinary DIST-04 peers do not gain enrollment authority merely by being ACTIVE.

## 5. First-node bootstrap

For a new LogicalIdentity:

1. Generate the LEA/recovery root independently of the runtime replication store.
2. Create the stable logical_identity_id.
3. Generate a fresh first node keypair and node_identity_id.
4. LEA signs the first enrollment statement, binding the node to the LogicalIdentity and setting state ACTIVE.
5. Initialize the node replication frontier/checkpoint as the authoritative empty/bootstrap state defined by DIST contracts; bootstrap does not fabricate prior shared history.
6. Preserve enough LEA/recovery material outside the first physical machine to enroll a replacement if that machine is destroyed.

Loss of the first machine MUST NOT destroy the LogicalIdentity. At minimum the LogicalIdentity identifier, LEA/recovery authority, cryptographic profile/version and recovery instructions must survive separately. Node private keys MAY be recoverable only if same-NodeIdentity recovery was intentionally provisioned; otherwise replacement-NodeIdentity enrollment is required.

## 6. Additional-node enrollment

A new host begins UNENROLLED. It generates fresh per-node key material and a unique node_identity_id. Enrollment authority verifies the request and signs a new enrollment statement. Initial lifecycle is ACTIVE only after the signed enrollment is durably accepted; before that it remains UNENROLLED.

The new node receives a verified bootstrap frontier/checkpoint and valid SHARED_REPLICATED history through normal replication after authorization. Existing record provenance and origin sequences are preserved exactly. The new NodeIdentity starts its own future `origin_sequence` namespace at the contract-defined initial sequence; it never continues another node's sequence unless performing an explicit same-NodeIdentity migration/recovery.

Interrupted enrollment is atomic at the authority boundary: absence of a durably accepted signed enrollment leaves the node UNENROLLED. Replaying the identical accepted enrollment is idempotent; a conflicting binding for the same node_identity_id is NOT_AUTHORIZED and requires owner resolution.

SECRETS are provisioned by a separate owner-controlled channel/process. Shared history synchronization MUST NOT carry node private keys, LEA keys, recovery secrets, API credentials, model secrets, or other SECRETS.

## 7. Clone detection and CLONE_CONFLICT

Copying an SSD, Portable Seed, VM, disk image, VK directory, runtime, or identity metadata can duplicate node private material but MUST NOT authorize two active incarnations of one NodeIdentity.

Credible evidence of simultaneous independent continuation under the same node_identity_id causes `CLONE_CONFLICT`. Evidence can include mutually incompatible signed continuation claims, concurrent identity-proof sessions from independently established incarnations, or divergent valid records using the same NodeIdentity/origin sequence namespace in a way impossible for one ordered lineage.

On CLONE_CONFLICT:

- replication authorization for that NodeIdentity is withheld;
- neither claimant wins automatically;
- both valid histories are preserved as evidence; no timestamp winner or silent merge is permitted;
- owner-authorized resolution is required: select one incarnation to continue, migrate exclusively, revoke/retire the old lineage, or perform authorized identity split for a copied history.

Hardware/network identifiers MAY be diagnostic evidence but never identity authority or winner criteria.

## 8. Authorized identity split

A copied valid history may become a legitimate additional node only through explicit enrollment as a NEW NodeIdentity.

The split procedure:

1. Preserve all already-valid SHARED_REPLICATED history byte/provenance semantics unchanged.
2. Generate a new node keypair and node_identity_id.
3. LEA signs an enrollment statement carrying explicit `AUTHORIZED_SPLIT` provenance and reference to the source lineage/checkpoint.
4. The new node begins a new origin_sequence namespace for future records.
5. No old record is relabeled or re-signed as originating from the new node.
6. Source node may remain ACTIVE if the split was intentional and authorized.

## 9. Migration

Migration is exclusive continuation of the SAME NodeIdentity lineage on a different execution/storage environment. It is distinct from adding a node and from cloning.

A migration requires owner/LEA-authorized migration intent binding: node_identity_id, old incarnation reference, target incarnation proof, handoff frontier/checkpoint, and an exclusivity transition. The old incarnation must enter SUSPENDED then RETIRED (or otherwise have its continuation authority cryptographically disabled) before the target becomes ACTIVE for future lineage continuation.

The target uses the same NodeIdentity and continues its origin_sequence namespace from the verified contiguous frontier. Migration does not rewrite history.

If the old host later returns with copied credentials, it is NOT_AUTHORIZED as an execution incarnation. If both old and target appear capable of continuing because exclusivity cannot be established, result is CLONE_CONFLICT, not newest-host wins.

## 10. Recovery

### Same-NodeIdentity recovery

Allowed only when separately protected recovery material/authority can authenticate the existing node_identity_id and establish that no competing active incarnation remains. It applies to OS reinstall, runtime loss, recoverable disk loss, or hardware replacement where continuation of the same lineage is intended.

Recovery rotates/re-establishes node private material only under an authenticated recovery statement binding the old identity, new public key/material, recovery event and verified frontier. Old compromised key material must lose future authority. Existing provenance remains unchanged; future origin_sequence continues the same NodeIdentity namespace.

### Replacement-NodeIdentity recovery

When same-identity recovery cannot be safely proven, create a NEW NodeIdentity through enrollment with `REPLACEMENT_RECOVERY` provenance. Valid shared history is preserved; future records use the new node's origin_sequence namespace. The lost/unsafe old node is REVOKED or RETIRED as appropriate.

Missing LEA/recovery material means `RECOVERY_REQUIRED`; no peer, copied Seed, hardware identifier, timestamp, or shared history can manufacture enrollment authority. Owner escalation/restoration from separately protected authority is required.

## 11. Revocation and retirement

Revocation permanently withdraws future operational authority from a NodeIdentity. Retirement intentionally closes a lineage without asserting compromise. Both preserve historical provenance.

A revoked reconnect is NOT_AUTHORIZED even with a cryptographically valid old node key. A retired/migrated old host is NOT_AUTHORIZED for continuation. Valid records created while the node was authorized remain historically valid; revocation is not retroactive deletion.

Revocation evidence must be authenticated by LEA/delegated revocation authority and must identify the NodeIdentity and revocation event. Implementations must not use wall-clock recency to override revocation.

## 12. Portable Seed relationship

Portable Seed is recovery/bootstrap media, not NodeIdentity.

- Known host: Seed may restore runtime/bootstrap material, but NodeIdentity remains the host's enrolled lineage and requires its valid identity proof.
- New host: Seed copy alone leaves host UNENROLLED; new-node enrollment or authenticated recovery is required.
- Original host lost: Seed can restore code/history and recovery metadata; same-identity recovery requires recovery authority, otherwise replacement enrollment.
- Replacement bootstrap: restore valid shared history, then establish identity separately.
- Seed copied / two copies active: media duplication creates no additional authority. If both copies contain and use the same node secret concurrently, CLONE_CONFLICT.
- Identity metadata damaged: RECOVERY_REQUIRED unless a separately authenticated recovery path reconstructs the binding.
- Offline: recovery/enrollment may be performed offline only when all required signed authority, revocation state needed by the policy, identity proof and deterministic bootstrap evidence are locally available. Otherwise remain RECOVERY_REQUIRED/UNENROLLED until authority is available.

## 13. SECRETS isolation

Node private keys, LEA/delegation private keys, recovery secrets and secret provisioning payloads are `SECRETS`, never `SHARED_REPLICATED`. DIST-04 MUST reject or exclude them under existing StateClass semantics. Identity/recovery secret provisioning is a separate bounded mechanism with its own authorization and audit requirements.

Public enrollment/revocation/migration/recovery evidence MAY be synchronization-relevant only after the required Wire extension is specified and validated; that does not change secret classification.

## 14. DIST-04 authorization boundary

Before a peer may use DIST-04 as a node, an identity authorization layer evaluates:

`NodeIdentity + lifecycle/trust state + enrollment proof + identity proof + applicable revocation/migration/recovery evidence -> decision`.

Normative decisions:

- `AUTHORIZED`: enrollment binding valid, identity proof valid, lifecycle ACTIVE, no unresolved clone/revocation/migration conflict.
- `NOT_AUTHORIZED`: unknown/unaccepted enrollment, invalid identity proof, REVOKED/RETIRED lineage, prohibited continuation, or explicit denial.
- `RECOVERY_REQUIRED`: recognized lineage but required identity/recovery material or metadata is missing/damaged, or safe continuation cannot yet be established without recovery authority.
- `CLONE_CONFLICT`: credible competing incarnations claim the same NodeIdentity lineage and exclusivity cannot be established.

Only AUTHORIZED permits ordinary DIST-04 replication participation. DIST-04 MUST consume the decision and MUST NOT issue enrollment, select clone winners, provision secrets, perform recovery, or override revocation.

## 15. Wire extension assessment

Wire Profile v1 is unchanged by NODE-01. Lifecycle authority requires durable, independently verifiable distributed control evidence not represented by the current DurableRecord/state payload alone. Therefore:

- `NodeEnrollmentRecord`: `BOUNDED_WIRE_EXTENSION_REQUIRED` — signed binding of LogicalIdentity, NodeIdentity, public key, authorization chain/type, initial lifecycle, event ID and optional predecessor/split/recovery reference.
- `NodeRevocationRecord`: `BOUNDED_WIRE_EXTENSION_REQUIRED` — signed irreversible future-authority withdrawal with NodeIdentity/event/reason-class/authority reference; history remains valid.
- `NodeMigrationRecord`: `BOUNDED_WIRE_EXTENSION_REQUIRED` — signed exclusive handoff binding old/target incarnation evidence, NodeIdentity and handoff frontier/checkpoint.
- `NodeRecoveryRecord`: `BOUNDED_WIRE_EXTENSION_REQUIRED` — signed same-identity key recovery/rotation or replacement-recovery relationship, with old/new key/identity references and verified frontier.

Next Wire-extension gate must define closed schemas, canonicalization/digest/signature preimages, versioning, exact validation/rejection categories, causal ordering independent of wall-clock, idempotency/conflict rules, golden/rejection vectors, Python+C++ conformance impact, and compatibility with existing Wire v1 without modifying current vectors in place. No extension is implemented here.
