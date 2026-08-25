# TASK-007 — SCOUT / PLANNER PREPARATION

STATUS: READY_FOR_CODEX_GATE
DATE: 2026-08-25
PROJECT: VK

## Eligibility
- TASK-021: PASS.
- TASK-034: PASS with repository-side mock test route and checkpoint convention.
- TASK-040 through TASK-044: PASS/reviewed.
- TASK-041 now supplies the canonical device registry contract/fixtures.

## Authoritative target
- repository: `nevincho/LIVE`
- branch: `Legacy`
- current verified head: `078a534b6f0241507349f182626d308f2c0ff284`
- implementation path: `family_guardian_ai/SOURCE_V09/`

## Reconciliation finding
The earlier TASK-007 preparation incorrectly included in-memory registry operations. That overlaps TASK-028, while TASK-041 has already completed the registry schema/fixtures. The overlap is now removed.

## Smallest justified implementation objective
TASK-007 is narrowed to the shared non-Core Home Node/device base abstraction and adapter-facing boundary only.

Minimum responsibilities:
- stable identity representation by reusing TASK-041 contract semantics;
- shared node/device base model/interface;
- narrow capability/status exposure needed by concrete adapters;
- adapter-facing boundary without device-specific behavior;
- repository tests proving compatibility with TASK-041 fixtures and preserving existing camera adapter behavior.

Explicitly excluded:
- registry service/operations (TASK-028);
- schema/fixtures already supplied by TASK-041;
- capability discovery (TASK-032);
- network discovery (TASK-010);
- IMOU/Echo integration (TASK-008/TASK-009);
- live `D:\Store\AI` deployment.

## Protected boundaries
- VK Core/personality/canonical memory;
- memory promotion/provenance semantics;
- existing validated chat/memory behavior;
- real device access and local runtime.

## Checkpoint / rollback
Pre-change checkpoint is exact LIVE Legacy head immediately before implementation; currently `078a534b6f0241507349f182626d308f2c0ff284`.

## Validation route
Use repository-side tests and TASK-041 contract/fixtures. Do not claim live device/runtime validation.

SCOUT RESULT: READY_FOR_CODEX_GATE
