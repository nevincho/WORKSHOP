# WORKSHOP Task Schema

STATUS: MANDATORY FORMAT FOR NEW TASKS

Every task must define at least:

- `TASK_ID`
- `PROJECT`
- `PRIORITY`: CRITICAL / HIGH / MEDIUM / LOW
- `STATUS`: READY / IN_PROGRESS / BLOCKED / REVIEW / COMPLETE / HOLD
- `OBJECTIVE`
- `SOURCE_PLAN_OR_REQUEST`
- `CURRENT_STATE`: VERIFIED evidence or NOT VERIFIED
- `PREREQUISITES`
- `DEPENDENCIES`
- `AFFECTED_COMPONENTS`
- `PROTECTED_COMPONENTS`
- `EXECUTION_CLASS`: WORKER / CODEX_CANDIDATE / HUMAN_GATE / MONITOR_ONLY
- `CODEX_ALLOWED`: YES / NO / GATE_REQUIRED
- `ACCEPTANCE_CRITERIA`
- `VALIDATION_METHOD`
- `PRE_CHANGE_CHECKPOINT`
- `ROLLBACK_METHOD`
- `EVIDENCE_PATHS`

## Pre-execution gate
Before execution, verify:
1. task is still required;
2. task is not already implemented;
3. prerequisites exist;
4. dependencies are satisfied;
5. objective belongs to current project phase;
6. validation can measure the intended objective;
7. protected scope is respected;
8. the cheapest capable execution path is selected.

## Completion rule
A task is COMPLETE only after independent review establishes acceptance criteria against repository/runtime evidence and a validated checkpoint is recorded where implementation changed.