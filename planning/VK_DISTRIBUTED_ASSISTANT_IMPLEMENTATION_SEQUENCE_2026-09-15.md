# VK Distributed Assistant — Bounded Implementation Sequence

Date: 2026-09-15
Status: READY FOR INDEPENDENT REVIEW; PRODUCTION IMPLEMENTATION NOT STARTED

## Gate 0 — architecture/contracts
Evidence: `decisions/VK_DISTRIBUTED_IDENTITY_STATE_SYNC_ARCHITECTURE_2026-09-15.md` and `decisions/VK_HOST_INSPECTOR_CONTRACT_2026-09-15.md`.
Required before implementation: independent WORKSHOP Reviewer PASS against VK protected boundaries and current target source.

## Task VK-DIST-01 — current VK persistence/runtime forensic
Objective: inspect the authoritative VK source/runtime implementation and map every persistent store, memory type, provenance/admission path, model/provider adapter, service/process and current PC/Pi deployment evidence into SHARED_REPLICATED / NODE_LOCAL / TRANSIENT / SECRETS / DERIVED_REBUILDABLE.
No production changes.
Acceptance: no UNKNOWN persistent store is assigned a migration policy without source evidence; existing useful data has a preservation path; exact integration seams for later tasks are identified.

## Task VK-DIST-02 — VK-native record/lineage contract
Objective: implement repository-local pure data contracts for LogicalIdentity, NodeIdentity, DurableRecord, ReplicaFrontier, Checkpoint and ReconciliationRecord plus deterministic serialization/integrity rules.
No network transport. No DB replication. No canonical-memory behavior change.
Acceptance: unit tests cover stable identity, idempotence, duplicate conflict, frontier dominance, divergence detection, gap handling and clock-independence.

## Task VK-DIST-03 — local append/import compatibility layer
Objective: add a non-destructive adapter that emits new durable records from current VK persistence events while preserving the existing store as rollback authority during migration.
Acceptance: existing behavior unchanged; old data remains readable; migration/import is repeatable/idempotent; no automatic memory promotion.

## Task VK-DIST-04 — synchronization engine, transport-independent
Objective: implement frontier comparison, missing-range calculation, validation, atomic acceptance, fast-forward and divergence/reconciliation-candidate generation against two local simulated replicas.
Acceptance: required scenarios 1–3 pass deterministically; interrupted sync resumes; replay is idempotent; timestamps are not causal authority.

## Task VK-DIST-05 — bounded HostInspector
Objective: implement common HostInspector plus Windows and Raspberry Pi/Linux read-only adapters using typed allow-listed probes.
Acceptance: contract/security tests prove no arbitrary command execution path; representative fixture/integration tests classify unavailable fields explicitly; hardware query routes to HostInspector.

## Task VK-DIST-06 — PC/Pi authenticated transport
Objective: after runtime endpoints are verified, bind the transport-independent sync engine to the smallest justified authenticated LAN transport.
Acceptance: secrets remain local; peer identity checked; interrupted transfer resumable; no unrestricted remote machine authority.

## Task VK-DIST-07 — two-node live migration/shadow validation
Objective: deploy behind a feature flag/shadow path on PC and Pi without replacing current persistence authority initially.
Acceptance: required scenarios 1–5 pass on real nodes; existing VK data preserved; rollback verified; offline assistant remains usable on each node with locally available state/capabilities.

## Promotion rule
Only after VK-DIST-07 Reviewer PASS may the new distributed record layer become canonical synchronization authority. Existing persistence must not be destructively removed in the same gate.

## Required scenario matrix
1. Common checkpoint N; PC offline; Pi advances; PC returns -> only missing validated Pi delta transferred -> convergence.
2. Common checkpoint N; Pi offline; PC advances; Pi returns -> fast-forward -> convergence.
3. Both offline and advance -> union valid histories -> semantic conflicts become explicit reconciliation records/candidates -> convergence without history loss.
4. Disconnected node -> chat/memory/tool operation continues with local state/capabilities; unavailable remote capabilities degrade explicitly.
5. PC and Pi hardware question -> local HostInspector returns verified node-specific hardware/runtime information.
