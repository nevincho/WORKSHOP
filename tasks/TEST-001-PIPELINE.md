# TEST-001 — WORKSHOP Pipeline Dry Run

STATUS: READY
TYPE: NON-DESTRUCTIVE DIAGNOSTIC
PROJECT: WORKSHOP
PRIORITY: HIGH
CODEX: FORBIDDEN
TARGET PROJECT MODIFICATION: FORBIDDEN

## Objective
Verify that WORKSHOP roles can discover one repository-only task, process it according to role, and persist all substantive output back to `nevincho/WORKSHOP` without relying on chat content.

## Required role behaviour

### SCOUT / PLANNER
- Read current WORKSHOP policies.
- Verify this task is safe and still required.
- Identify applicable policies and dependencies.
- Record findings in `evidence/TEST-001/SCOUT.md`.
- Do not modify target projects.

### WORKER
- Read current WORKSHOP policies and Scout evidence if present.
- Perform no target-project changes.
- Verify that the required WORKSHOP paths/policies needed for this dry run are readable.
- Record findings in `evidence/TEST-001/WORKER.md`.

### CODEX GATE
- Read current WORKSHOP policies and task.
- Determine whether Codex is justified.
- Expected decision: Codex is NOT justified for this diagnostic task.
- Record decision and reasoning in `evidence/TEST-001/CODEX_GATE.md`.
- Do not invoke Codex.

### REVIEWER
- Independently verify the task objective, role evidence, policy compliance, and absence of target-project changes.
- Record verdict in `review/TEST-001.md` using one of: PASS, REWORK, BLOCKED, NOT VERIFIED.

## Acceptance criteria
1. No substantive agent output is written in agent chats.
2. All substantive role outputs are persisted in WORKSHOP.
3. No VK, Horoscopes, or TANGRA repository/runtime is modified.
4. Codex is not used.
5. Reviewer independently determines whether the repository-only workflow succeeded.
6. Missing evidence is reported as NOT VERIFIED rather than guessed.

## Completion
The task is complete only after Reviewer evidence exists in `review/TEST-001.md` and the verdict is based on repository evidence.
