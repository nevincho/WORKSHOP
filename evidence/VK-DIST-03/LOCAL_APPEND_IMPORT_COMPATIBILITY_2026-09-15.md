# VK-DIST-03 — Local Append / Import Compatibility Layer

Date: 2026-09-15
Status: IMPLEMENTED / EXECUTION_VALIDATION_NOT_VERIFIED

## Target evidence
Inspected `nevincho/LIVE`, branch `Legacy`, `family_guardian_ai/SOURCE_V09/app/db.py` before modification. Verified persistence interfaces used by the adapter boundary:
- `add_memory(...)` inserts into existing SQLite `memories` and accepts explicit `status`, default `candidate`;
- `set_status(event_id,status)` remains the existing status transition interface and is not called by the distributed adapter;
- `list_candidates()` exposes candidate state;
- `search_memories()` activates only `status='canonical'` memories.
No existing persistence file or schema was modified.

## Implementation
Implementation branch: `nevincho/LIVE` `vk-dist-03-compat`, based on reviewed `vk-dist-02-contracts`.
Files added only:
- `app/distributed_persistence_adapter.py`
- `tests/test_distributed_persistence_adapter.py`

The adapter:
- is disabled by default;
- requires explicit `StateClass.SHARED_REPLICATED` for export/import eligibility;
- never infers eligibility from durability/table/path/timestamp/existence;
- maps explicit eligible memory rows to deterministic DIST-02 `DurableRecord` objects preserving legacy provenance, status evidence, semantic relations and parent lineage;
- uses DIST-02 integrity and duplicate classification;
- holds sequence-gap records without advancing contiguous frontier;
- includes held records in duplicate/conflict checks;
- preserves independent valid per-node histories in the compatibility ledger;
- imports memory-related records only through injected existing `add_memory(...)` semantics and forcibly sets `status='candidate'`, `provenance='DISTRIBUTED_IMPORT'`, `source='distributed_import'` regardless of exported legacy status;
- never calls `set_status` and cannot promote canonical memory;
- does not modify `db.py`, SQLite schema, Core, runtime composition or network code.

The compatibility ledger is explicitly non-canonical and is currently in-memory only; it is a bounded contract/adapter validation mechanism, not a second production persistence authority.

## Validation artifacts
Repository test suite added for the required scenarios:
1. deterministic SHARED_REPLICATED export;
2-5. NODE_LOCAL / SECRETS / TRANSIENT / DERIVED_REBUILDABLE export rejection;
6. idempotent repeated import;
7. tamper rejection;
8. conflicting duplicate rejection;
9. sequence gap held without contiguous advancement;
10. divergent PC/Pi histories preserved;
11. exported canonical-status evidence imports through existing persistence callback as candidate only;
12. disabled adapter performs no persistence callback.
Additional regression checks cover conflict detection against a held gap record.

## Execution evidence
No repository execution environment or CI workflow is available through the current WORKSHOP/GitHub connection for this branch. The local analysis container cannot resolve GitHub and therefore cannot check out the target branch. GitHub reports no workflow runs for head `7ec4a6b291c127cf4d299a06b77fcaf2c5289cb1`.

Per WORKSHOP VALIDATION_POLICY, authored tests without execution are not sufficient to claim runtime PASS. Test execution result is therefore NOT VERIFIED.

## Rollback
Remove the two added files or discard branch `vk-dist-03-compat`. Existing `db.py` and VK persistence behavior are unchanged.

## Scope
No network transport, PC/Pi communication, DB/WAL replication, schema migration, production binding, Core modification or automatic canonical-memory promotion was implemented.
