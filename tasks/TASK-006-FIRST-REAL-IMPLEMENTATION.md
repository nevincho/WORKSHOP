# TASK-006 — First Real Controlled Implementation

STATUS: BLOCKED
PRIORITY: MEDIUM
DEPENDS_ON: TASK-005 PASS
TYPE: IMPLEMENTATION

## Objective
Execute the implementation task selected and prepared by TASK-005 using the cheapest safe execution path, with checkpoint, validation, independent review, and rollback protection.

## Mandatory constraints
- Execute only the exact scope approved/prepared in TASK-005.
- Verify current target state again before change.
- Create/record pre-change checkpoint.
- Preserve protected components and validated interfaces.
- Use Codex only if Codex Gate authorizes it.
- Run the validation method defined in TASK-005.
- Independent Reviewer must verify the actual resulting repository/runtime state before PASS.
- If live/hardware validation is required and unavailable, record NOT VERIFIED/HUMAN GATE rather than claiming PASS.

## Required outputs
- implementation evidence under `evidence/TASK-006/`;
- checkpoint reference under `checkpoints/`;
- `review/TASK-006.md`;
- blocker/human-gate record if live validation cannot be completed autonomously.

## Unblock condition
TASK-005 independent review is PASS and the prepared implementation task does not require an unresolved human gate.

## Completion meaning
PASS means the exact prepared change is implemented and independently validated against its acceptance criteria. Where evening live validation is explicitly required, repository implementation may be complete while final live validation remains pending and must not be misreported.
