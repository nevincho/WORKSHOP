# TASK-008 — CODEX GATE

ROLE: WORKSHOP CODEX GATE
TASK_ID: TASK-008
DECISION: HOLD / CODEX NOT AUTHORIZED
DATE: 2026-08-24

## Gate basis
- `policies/CODEX_BUDGET_POLICY.md` is mandatory.
- TASK-008 is marked `BLOCKED`, `CODEX_CANDIDATE`, and `GATE_REQUIRED`.
- TASK-008 explicitly depends on TASK-007 PASS.
- TASK-007 is currently `BLOCKED`; no TASK-007 PASS evidence is present in the inspected WORKSHOP state.
- `status/WORKSHOP_STATE.yaml` records the VK runtime as `NOT_VERIFIED` and TASK-005 blocked by `NO_VERIFIED_IMPLEMENTATION_RUNTIME_ROUTE`.
- `blockers/TASK-003-EXECUTION-ROUTES.md` records the active Windows runtime execution bridge as NOT VERIFIED.
- Direct IMOU LAN evidence exists for IPC-K7C: host reachability and TCP listeners on 554/80 are verified, but RTSP path/auth/frame retrieval, ONVIF, PTZ/control API, and runtime integration remain NOT VERIFIED.

## Codex-budget decision
Codex would be premature. Required prerequisites and inexpensive preparation are incomplete, and implementation/runtime validation cannot currently be executed through a verified route. Sending Codex now would consume scarce capacity on dependency discovery and environment uncertainty that policy explicitly forbids.

## Required before re-gating
1. TASK-007 must PASS or an equivalent shared node/device abstraction must be directly verified.
2. A controlled non-Core VK Windows execution/test/checkpoint/rollback route must be directly verified.
3. Current target implementation state must be inspected to confirm no equivalent IMOU/camera adapter already exists.
4. Exact shared interfaces, affected files/components, validation commands, checkpoint, rollback, protected scope, and explicit non-goals must be assembled into the minimal implementation package.
5. Camera connection method must be narrowed beyond open TCP ports using direct evidence sufficient for the requested adapter path.

## Protected scope
Do not modify VK Core, canonical personality/memory, approved-memory promotion, or provenance semantics. Do not create a parallel vision/memory architecture.

## Outcome
CODEX HANDOFF: NOT CREATED.
CODEX USAGE: NONE.
RE-GATE: REQUIRED after prerequisites are evidence-backed.
