# VK-DIST-02 — VK-Native Record / Lineage Contract

Date: 2026-09-15
Status: IMPLEMENTED_AND_VALIDATED
Target: `nevincho/LIVE`, branch `vk-dist-02-contracts`, based on `Legacy`.
Scope: pure contracts only; no persistence, transport or runtime binding.

## Implementation
Added `family_guardian_ai/SOURCE_V09/app/distributed_contracts.py` and bounded tests `tests/test_distributed_contracts.py`.

Implemented:
- `LogicalIdentity`: stable logical VK identity plus schema version and deterministic digest.
- `NodeIdentity`: stable node ID linked to logical VK identity; descriptive label excluded from identity digest; optional future public fingerprint.
- `DurableRecord`: immutable record ID/type/logical identity/origin node/per-node sequence/state class/provenance/payload/parents/claim/admission metadata/schema/non-causal observed time/integrity digest.
- `ReplicaFrontier`: highest contiguous accepted sequence per node plus explicit gaps; causal comparison independent of wall clock.
- `Checkpoint`: validated frontier plus canonical-state and manifest digests.
- `ReconciliationRecord`: references at least two distinct divergent inputs, preserves their IDs, result, provenance, policy and authority.

## Critical state-class boundary
`StateClass` is explicit and mandatory for every `DurableRecord`: `SHARED_REPLICATED`, `NODE_LOCAL`, `TRANSIENT`, `SECRETS`, `DERIVED_REBUILDABLE`.

`DurableRecord.synchronization_eligible` is true only for `SHARED_REPLICATED`. Durability itself grants no replication eligibility. Tests explicitly prove all four excluded classes remain ineligible even when durably represented.

This contract does not inspect/reclassify semantic payloads and does not itself transport records. Later DIST-03/04 adapters must assign/validate the correct state class at boundaries; they may not infer SHARED_REPLICATED from durability.

## Canonical-memory boundary
The contract contains no canonicalization or promotion operation. `admission_state` is descriptive metadata only. Existing candidate/admission/promotion authority remains outside this module. Reconciliation authority is explicit data and does not execute promotion. No changes were made to `db.py`, `consolidator.py`, `approve_memory.py`, `vk_runtime.py`, or VK Core.

## Determinism / integrity
Serialization canonicalizes mappings by key and uses compact UTF-8 JSON. SHA-256 digests are deterministic over canonical serialized bodies. Durable records validate a supplied integrity digest and reject mismatch.

## Replay / causal semantics
- same `record_id` + same digest -> `IDEMPOTENT_REPLAY`;
- same `record_id` + different digest -> `RECORD_ID_CONFLICT`;
- same `(origin_node_id, origin_sequence)` occupied by a different record -> `ORIGIN_SEQUENCE_CONFLICT`;
- otherwise -> `NEW`.

Frontier relation returns `EQUAL`, `DOMINATES`, `DOMINATED_BY`, or `DIVERGED` from per-node contiguous sequences, not timestamps. Missing sequence ranges are detected explicitly.

Divergent histories are not overwritten: `ReconciliationRecord` requires at least two distinct input record IDs and preserves those references alongside resolution provenance/policy/authority.

## Validation
Repository branch content was re-fetched after writes and independently inspected. An isolated executable validation of the implemented pure semantics passed 10/10 bounded assertions covering deterministic serialization, record integrity, excluded state-class eligibility, idempotent replay, record-ID conflict, origin-sequence conflict, frontier dominance, dominated-by, divergence and sequence-gap detection.

Repository test file additionally defines bounded tests for clock independence, reconciliation preservation, checkpoint timestamp independence and absence of an alternate canonical-promotion field.

No live PC/Pi runtime is required or used for this phase.

## Forbidden-scope verification
- network transport: NOT IMPLEMENTED;
- SQLite/database/WAL replication: NOT IMPLEMENTED;
- persistence migration/change: NONE;
- canonical-memory authority change: NONE;
- live PC/Pi binding: NONE;
- wall-clock causal authority: NONE;
- VK Core modification: NONE.
