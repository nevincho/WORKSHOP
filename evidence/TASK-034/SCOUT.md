# TASK-034 — SCOUT / PLANNER PREPARATION

ROLE: WORKSHOP SCOUT / PLANNER
DATE: 2026-08-24
STATUS: READY_FOR_WORKER

## Authority and prerequisite
Canonical backlog authority lists TASK-034 as READY and as the first VK unblock task. TASK-021 has independent PASS. TASK-007 and downstream VK node/device implementation remain blocked until this repository-side test/checkpoint foundation is independently validated.

## Authoritative target state verified
Primary implementation repository: `nevincho/LIVE`
Branch: `Legacy`
Observed branch head: `76dd0daf469f71e2809cbeae5e3f1b50afb58448`
Target implementation path: `family_guardian_ai/SOURCE_V09/`

The repository already contains a `tests/` directory with at least:
- `test_conversation_recovery.py`
- `test_remote_work_gateway.py`

This proves test artifacts exist, but it does NOT prove a bounded node/device-layer test entrypoint, fixture contract, checkpoint/rollback convention, or reproducible execution route satisfying TASK-034.

## Task validity
STILL REQUIRED: YES.
ALREADY IMPLEMENTED: PARTIAL infrastructure exists, but TASK-034 acceptance is NOT VERIFIED and no evidence shows the specific node/device mock route plus checkpoint/rollback foundation is complete.
DUPLICATE / SUPERSEDED: NO. Canonical backlog selects TASK-034 as the active VK unblock task and treats later repo-prep duplicates as support/planning artifacts only.
CURRENT PHASE: repository-side safety/validation foundation before shared node/device implementation.

## Smallest justified implementation package
Objective: extend existing repository testing structure rather than replace it.

Preferred affected area:
- `family_guardian_ai/SOURCE_V09/tests/` for one minimal mock/fixture node/device sanity test;
- smallest necessary non-Core test helper/configuration/documentation location already consistent with repository structure;
- lightweight checkpoint/rollback documentation tied to exact git refs/commits.

Protected / preserved components:
- `Core/` and protected VK Core behavior;
- canonical personality state;
- approved-memory promotion/admission semantics;
- provenance semantics;
- current runtime interfaces and existing tests;
- no live `D:\Store\AI` deployment;
- no real IMOU/Echo/device connection.

## Dependencies
Satisfied: TASK-021 PASS.
Downstream: TASK-007 must remain BLOCKED until TASK-034 independent PASS and explicit review that the route is sufficient.

## Validation requirement
Worker must provide one reproducible repository-side command or command sequence, execute at least one harmless mock/fixture test without live devices/credentials/Core mutation, record exact files changed and exact target commit/ref provenance, and document rollback to a known repository ref.

Presence of tests alone is insufficient evidence. If the available execution route cannot actually run the test against a known repository revision, acceptance is NOT MET. Codex must not be auto-invoked; only a minimal `READY_FOR_CODEX_REVIEW` handoff is permitted if agent-only completion is technically insufficient.

## Actual blocker
No Scout-stage blocker. The implementation-stage requirement is to convert the existing generic test presence into a bounded, reproducible node/device test route plus explicit checkpoint/rollback convention.

## Non-goals
- no Home Node implementation;
- no capability discovery implementation;
- no IMOU/Echo integration;
- no live Windows runtime validation;
- no Core/personality/memory/provenance changes;
- no broad test-framework migration or dependency upgrade.

SCOUT RESULT: READY_FOR_WORKER.
