# TASK-033 — Mysticarium Test Harness Bootstrap

TASK_ID: TASK-033
PROJECT: HOROSCOPES / MYSTICARIUM
PRIORITY: HIGH
STATUS: READY
TYPE: REPOSITORY-SIDE UNBLOCK IMPLEMENTATION
DEPENDS_ON: TASK-013 PASS
UNBLOCKS: TASK-022 re-verification, then TASK-014 if TASK-022 PASS

## Objective
Create the smallest repository-side deterministic test harness and reproducible execution route needed so TASK-022 can verify a real test path for the future TASK-014 deterministic engine.

## Required work
- inspect the authoritative Mysticarium repository/branch and preserve its current architecture;
- add only the minimum test runner/harness/configuration needed for pure deterministic logic tests;
- provide one documented deterministic test command;
- ensure the harness can run against the exact repository revision/checkout used for evidence;
- use fixtures/mocks/sample inputs only; no live Pi4 dependency is required for this repository-side preparation;
- record exact files changed, command used, results, commit/ref provenance and rollback point;
- independent Reviewer verifies that the harness measures deterministic behavior and that it does not implement TASK-014 itself.

## Boundaries
- DO NOT implement the deterministic engine itself.
- DO NOT deploy to Pi4.
- DO NOT invoke Codex automatically. If precision work exceeds agent capability, prepare a minimal `READY_FOR_CODEX_REVIEW` handoff for Vlad.
- No unrelated refactor or dependency expansion.

## Acceptance criteria
1. A committed minimal deterministic test harness exists in the authoritative target repository/branch.
2. There is one reproducible documented test command.
3. The command is shown to execute against a known exact repository revision using repository-side/isolated execution available to the agents.
4. At least one fixture/mock deterministic sanity test passes.
5. Reviewer confirms the harness is sufficient to rerun TASK-022 and does not falsely claim TASK-014 implementation.
6. Result is either PASS or `READY_FOR_CODEX_REVIEW` with a minimal handoff if agent-only completion is technically impossible.
