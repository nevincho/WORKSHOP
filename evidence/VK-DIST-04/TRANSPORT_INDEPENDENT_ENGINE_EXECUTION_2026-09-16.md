# VK-DIST-04 — Transport-independent replication engine execution evidence

Status: BEHAVIORAL_PASS

## Provenance
- Target repository: `nevincho/LIVE`
- Base / rollback: `354162717abed5cb8b5ff33b2b31579fa0d71571` (`vk-wire-02-codec` reviewed head)
- Branch: `vk-dist-04-engine`
- Tested head: `6befa60eaeedb5b3646cd20e6a555f4c523ccd9f`
- Base→head: exactly three added files: engine, bounded test module, Actions workflow. No pre-existing source/test/runtime/UI file modified.
- `distributed_contracts.py` blob: `cdbad261235710caac16b7079797b5599f5924d4` PASS
- `distributed_persistence_adapter.py` blob: `8a7eaec09e2ab144fb69f263245789ad435d82f5` PASS
- `distributed_wire_v1.py` blob: `8e753ac5bd3072750e8f87450acac65bba9e0071` PASS

## Execution
- GitHub Actions run: `35038206161`
- Job: `104611963423`
- Runner: Ubuntu 24.04.5, image `ubuntu-24.04` 20260907.300.1
- Python: CPython 3.12.14
- Command: `python -m unittest -v tests.test_distributed_replication_engine`
- Result: 24 unittest methods, 24 PASS, 0 failures, 0 errors, 0.028 s.

The 24 methods cover the requested 30-case matrix; combined methods explicitly cover cases 05–09, 14–16, and 29–30.

## Behavioral coverage
PASS:
1. equal frontier no transfer;
2. local dominance send set;
3. remote dominance request set;
4. divergence plan;
5–9. explicit StateClass gate (only SHARED_REPLICATED transfers);
10. idempotent replay;
11. record-ID conflict;
12. origin-sequence conflict;
13. single sequence gap;
14–16. multiple gaps, no false contiguous advance, deterministic held release;
17. missing lineage dependency;
18. later dependency release;
19. tampered Wire integrity rejected;
20. noncanonical Wire bytes rejected;
21. unsupported Wire version rejected;
22. deterministic transfer ordering;
23. repeated planning equality;
24. reconciliation preserves both causal inputs/provenance;
25. timestamps do not select winner;
26. replicated memory enters existing add_memory path as `candidate`;
27. disabled engine is a no-op;
28. frontier excludes unresolved gaps from contiguous history;
29–30. two replicas with distinct valid histories converge and second synchronization is no-op.
Additional bounded case: non-SHARED received record rejected.

## Architecture boundary
`distributed_replication_engine.py` is transport-neutral. It imports no HTTP/WebSocket/socket/discovery/removable-storage/cloud/Bluetooth/LoRa implementation. TransferPlan contains logical record IDs, sequence requests, gaps/dependencies and frontier state only.

External serialized receive boundary is `decode_json` + `validate_durable_record` from accepted Wire Profile v1 before conversion to the internal DIST-02 DurableRecord representation. No pickle/database-row protocol is introduced.

The engine owns pending causal records and passes only causally-ready records to the existing DIST-03 persistence compatibility adapter. This preserves DIST-03 semantics without changing that adapter: pending records do not falsely advance its ledger, and memory imports remain candidate-only through existing `add_memory` semantics.

## Runtime safety
Engine constructor defaults `enabled=False`. No production runtime hook, endpoint, service, UI, network path or transport was added. Standalone VK behavior is unchanged unless the engine is explicitly instantiated and enabled by a future integration gate.

## Convergence scenario
Node A begins with A:1,A:2. Node B begins with B:1,B:2. Each receives the other's Wire-v1 records through the transport-neutral receive API. Final states contain all four records; frontiers become equal; no history is removed; timestamps play no authority role; subsequent planning in both directions returns NO_SYNC_REQUIRED.
