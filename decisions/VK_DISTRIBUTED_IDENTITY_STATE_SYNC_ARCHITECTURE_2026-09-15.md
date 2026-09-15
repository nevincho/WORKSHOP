# VK Distributed Identity / State / Synchronization Architecture

Date: 2026-09-15
Status: CONTROL ROOM ARCHITECTURE DECISION — IMPLEMENTATION NOT STARTED
Scope: VK only. TANGRA is reference evidence only and is not modified.

## Authoritative evidence used
- `projects/VK.md`: VK Core, canonical personality, approved-memory promotion and provenance are protected; runtime path remains only partially verified.
- `nevincho/TANGRA-DOCS`, branch `family-guardian-ai`, `family_guardian_ai/ARCHITECTURE.md` and `VK_CANONICAL_FOUNDATION_2026-08-21.md`: local-first operation, replaceable inference, append-only memory, provenance, synchronization/lineage, one logical distributed VK identity and host capability discovery are already canonical design directions.
- `nevincho/TANGRA-2.0`, branch `tai-cog-32-package`, Cognitive substrate: useful generic contract ideas include `NodeIdentity`, `RuntimeIdentity`, structured state events, provenance, claim/validation classification and bounded capability descriptors. These are reference concepts only; VK must define VK-native contracts.

## Decision
VK is one logical identity with multiple autonomous replicas/nodes. Replication operates on immutable, content-addressed or uniquely identified VK records plus explicit lineage/checkpoints. Runtime databases and indexes are materialized views, not synchronization units.

No SQLite/database-file replication. No newest-file-wins. Wall-clock timestamps are metadata, never causal authority.

## State classes
1. SHARED_REPLICATED
   - admitted canonical memories and their provenance/lineage;
   - durable events/evidence eligible for cross-node use;
   - identity/persona evidence and approved canonical state;
   - durable user/project knowledge whose policy permits replication;
   - reconciliation records and shared checkpoints.
2. NODE_LOCAL
   - host hardware inventory and current host/runtime health;
   - local model/provider availability;
   - local paths, device identifiers, caches tied to hardware;
   - node-specific capability configuration.
3. TRANSIENT
   - active prompt/context windows;
   - in-flight tool calls, UI session state, ephemeral queues;
   - temporary health samples unless promoted as evidence.
4. SECRETS
   - API keys, credentials, tokens, private keys and OS credential-store material;
   - local by default; replication requires a separate explicit secrets design and is outside this phase.
5. DERIVED_REBUILDABLE
   - embeddings, search indexes, caches, summaries that can be deterministically or acceptably rebuilt from authoritative records;
   - never synchronization authority.

## Minimum VK-native contracts
### LogicalIdentity
- `vk_identity_id`: stable ID for the one logical VK identity.
- schema/version metadata.

### NodeIdentity
- stable `node_id` generated once per installed VK node;
- `vk_identity_id`;
- node public identity/fingerprint when authenticated transport is introduced;
- human-readable label is non-authoritative.

### DurableRecord
Minimum fields:
- `record_id` globally unique and immutable;
- `record_type`;
- `vk_identity_id`;
- `origin_node_id`;
- `origin_sequence` monotonically increasing per node;
- `parents[]` or lineage references where semantically required;
- `provenance`;
- `claim_class` / admission state as applicable;
- payload + schema version;
- integrity digest;
- wall-clock observed time as non-causal metadata.

Record identity and `(origin_node_id, origin_sequence)` provide replay/duplicate detection. Imported records retain original IDs and provenance.

### ReplicaFrontier
A version-vector-like map `{node_id -> highest contiguous accepted origin_sequence}` plus explicit gaps when required. This is the causal synchronization summary. It is not derived from timestamps.

### Checkpoint
A durable declaration of a validated replica frontier plus canonical-state digest/manifest and schema version. A checkpoint does not erase underlying history.

### ReconciliationRecord
Records a deterministic or human-authorized resolution when concurrent histories affect the same canonical semantic object. It references all inputs, preserves them, states the chosen/consolidated result, provenance, policy/rule used and authority.

## Synchronization semantics
1. Handshake: verify logical identity compatibility, protocol/schema compatibility and peer node identity.
2. Exchange replica frontiers/checkpoint IDs.
3. Determine last common accepted frontier/checkpoint.
4. Exchange only records absent from the peer, by origin sequence/range and integrity identity.
5. Validate schema, integrity, provenance/admission constraints and dependencies before acceptance.
6. Persist received immutable records idempotently.
7. Advance frontier only across contiguous validated records.
8. Rebuild/update derived views after durable acceptance.
9. Create a new shared checkpoint only after both sides agree on the accepted frontier and canonical-state validation succeeds.

### Fast-forward
If one frontier causally dominates the other and there are no conflicting canonical consolidations, transfer missing records and advance the lagging replica.

### Divergence
If both frontiers contain unique advances, exchange both histories. Immutable histories are unioned, not overwritten. Independent non-conflicting records coexist. Semantic conflicts enter reconciliation. A later reconciliation record references all conflicting inputs; original records remain auditable.

### Duplicate/replayed records
Same `record_id` + same digest: idempotent no-op. Same `record_id` + different digest: integrity conflict, reject/quarantine. Already-covered `(origin_node_id, origin_sequence)` with a different record: lineage/integrity conflict, reject/quarantine.

### Interrupted synchronization
Acceptance is record-atomic. Frontier advances only after durable validation. Restart resumes from the persisted frontier/gaps; already accepted records replay idempotently.

### Clock disagreement
Wall-clock time does not establish order or winner. Causality uses node sequence + lineage/frontier. Clock anomalies may be recorded as diagnostics.

### Canonical-memory consolidation
Raw evidence/events and admitted canonical memory are separate semantic layers. Synchronization replicates records; it does not silently promote candidates. Existing VK human-authorized admission rules remain protected. Concurrent canonical-memory edits require deterministic merge only where the schema defines a safe commutative merge; otherwise create a reconciliation candidate requiring the existing admission authority. Provenance from every contributing record must survive consolidation.

## TANGRA Cognitive reuse decision
ADAPT CONCEPTS, DO NOT COPY IMPLEMENTATION.
Reusable concepts: system/node/runtime identity separation, structured provenance, explicit unknown/source-gap states, validation/claim classification, bounded capability descriptors, serialization discipline.
Not reusable mechanically: TANGRA mission/embodiment semantics, TANGRA-specific enums/authority, package names, runtime hooks, or production integration.

## Protected invariants
- one VK identity;
- offline autonomous node operation;
- eventual validated convergence;
- explicit provenance/lineage;
- protected canonical-memory admission;
- replaceable inference providers;
- secrets local by default;
- host/runtime state remains node-local;
- existing VK data is migrated by adapters/importers, never destructively rewritten in place during first implementation.
