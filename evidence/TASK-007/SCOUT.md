# TASK-007 — SCOUT / PLANNER PREPARATION

STATUS: READY_FOR_CODEX_GATE
DATE: 2026-08-25
PROJECT: VK

## Eligibility
- TASK-021: PASS.
- TASK-034: PASS with repository-side mock test route and commit-based checkpoint/rollback convention.
- TASK-007 may therefore enter implementation review.

## Authoritative target
- repository: `nevincho/LIVE`
- branch: `Legacy`
- current verified head after TASK-034: `3ad02e4ddd298088d3bb51bf0b3cf7ecacf3217b`
- implementation path: `family_guardian_ai/SOURCE_V09/`

## Current repository findings
The existing `app/` tree includes device-adjacent code such as `camera_adapter.py`, but no shared Home Node / device registry abstraction was verified in the inspected target state.

`camera_adapter.py` is a concrete local camera adapter. It probes OpenCV devices and writes captures under the configured install root. It is not a shared node/device registry or capability/status contract and should not be duplicated or hard-coded into the new abstraction.

## Smallest justified implementation objective
Introduce the shared non-Core node/device abstraction only, designed so concrete adapters such as camera/IMOU/Echo can attach later without separate memory stacks or protected Core changes.

Minimum responsibilities:
- immutable/stable node/device identity fields;
- explicit device kind/type and capability set;
- explicit availability/health/status representation;
- registry operations for add/update/remove/query using in-memory repository-safe behavior first;
- adapter-facing contract that does not require live discovery;
- tests using TASK-034 mock/fixture route.

## Protected boundaries
- do not modify protected VK Core/personality/canonical memory;
- do not alter memory promotion/provenance semantics;
- do not connect to real IMOU/Echo/camera devices in repository tests;
- do not deploy into `D:\Store\AI`;
- do not implement TASK-008/009/010/028/029/032 behavior inside TASK-007;
- preserve existing `camera_adapter.py` behavior unless a minimal interface-only adaptation is later proven necessary.

## Checkpoint / rollback
Pre-change checkpoint for TASK-007 must be exact branch head immediately before implementation; currently `3ad02e4ddd298088d3bb51bf0b3cf7ecacf3217b` if no intervening target commit occurs.

Repository-side validation foundation:
`python -m unittest family_guardian_ai.SOURCE_V09.tests.test_node_device_fixture`

## Acceptance preparation
Implementation must provide repository diff + unit tests for registry/node semantics. Live device validation is explicitly outside repository PASS and remains required later for device-specific operational claims.

## Why Codex Gate is justified
TASK-007 defines shared interfaces consumed by multiple downstream adapters and capability-discovery layers. The abstraction boundary must reconcile existing adapter code and future device registry/capability tasks without duplicate stacks. This is architecture-dependent precision implementation, not a mechanical fixture task.

SCOUT RESULT: READY_FOR_CODEX_GATE
