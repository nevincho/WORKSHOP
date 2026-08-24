# TASK-034 — VK Repository Test / Checkpoint Foundation

TASK_ID: TASK-034
PROJECT: VK
PRIORITY: HIGH
STATUS: READY
TYPE: REPOSITORY-SIDE UNBLOCK IMPLEMENTATION
DEPENDS_ON: TASK-021 PASS
UNBLOCKS: TASK-007 and downstream VK repository implementation tasks once verified

## Objective
Create the smallest repository-side test/checkpoint/rollback foundation needed so VK implementation work can proceed safely without requiring live Windows runtime deployment during the day.

## Required work
- inspect the verified VK implementation target(s) and preserve current interfaces/protected Core boundaries;
- establish a bounded repository-side test entrypoint for node/device-layer work using mocks/fixtures/simulated devices;
- establish a lightweight checkpoint/rollback convention tied to exact repository commits/refs;
- provide one reproducible repository-side validation command or clearly documented command sequence;
- prove that a harmless fixture-based test can run without access to live devices, credentials, Echo, IMOU, or protected VK Core;
- record exact files changed, commands, results, commit/ref provenance and rollback instructions;
- independent Reviewer verifies that this is only test/checkpoint infrastructure and does not claim live runtime validation.

## Boundaries
- DO NOT deploy into `D:\Store\AI`.
- DO NOT modify protected Core/personality/canonical memory.
- DO NOT connect to real IMOU/Echo devices.
- DO NOT invoke Codex automatically. If precision work exceeds agent capability, prepare a minimal `READY_FOR_CODEX_REVIEW` handoff for Vlad.
- No broad redesign or unrelated dependency upgrades.

## Acceptance criteria
1. A bounded repository-side test route exists for future VK node/device work.
2. At least one mock/fixture-based harmless test executes successfully or the task reaches `READY_FOR_CODEX_REVIEW` with a precise missing step.
3. A checkpoint/rollback method tied to repository commits/refs is documented and usable.
4. Reviewer confirms the route is sufficient to reconsider TASK-007 eligibility.
5. No live Windows runtime or protected Core claim is made.
