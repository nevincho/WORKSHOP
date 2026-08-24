# TASK-007 — CODEX GATE

STATUS: READY_FOR_CODEX_REVIEW
DATE: 2026-08-25
CODEX_USED: no

## Decision
Codex is justified for TASK-007 implementation because this is a shared architecture/interface layer consumed by device registry, capability discovery, network discovery and later concrete adapters. Incorrect boundaries would create duplicate device stacks or leak device-specific behavior into the shared layer.

Automation MUST NOT invoke Codex. Vlad approval is required for this specific task.

## Minimal Codex handoff
Task: TASK-007 — VK Home Node and Device Layer.

Authoritative target:
- repo: `nevincho/LIVE`
- branch: `Legacy`
- baseline head: `3ad02e4ddd298088d3bb51bf0b3cf7ecacf3217b`
- path: `family_guardian_ai/SOURCE_V09/`

Verified prerequisites:
- TASK-021 PASS;
- TASK-034 PASS;
- repository-side mock test/checkpoint route exists and is provenance-validated.

Objective:
Implement the smallest non-Core shared node/device abstraction: stable identity, kind/type, capabilities, explicit health/status, in-memory registry operations and adapter-facing contract. Reuse existing repository patterns and preserve `camera_adapter.py` behavior.

Protected components:
- VK Core;
- canonical personality;
- approved-memory promotion/provenance semantics;
- live `D:\Store\AI` runtime;
- real IMOU/Echo/camera access.

Non-goals:
- do not implement device-specific integrations;
- do not implement capability discovery beyond the minimal shared contract;
- do not implement network discovery;
- do not redesign existing memory/chat/Core architecture;
- do not deploy to Windows runtime.

Acceptance:
1. shared node/device model and registry are narrow and testable;
2. explicit capability/status information is exposed;
3. no device-specific hard-coding;
4. no duplicate memory/provenance stack;
5. existing adapter behavior preserved;
6. unit tests run through repository-only route;
7. exact commits, diff, test output and rollback checkpoint recorded.

After implementation, Reviewer must inspect actual diff/tests before PASS. Live operational claims remain NOT VERIFIED until later runtime/device validation.
