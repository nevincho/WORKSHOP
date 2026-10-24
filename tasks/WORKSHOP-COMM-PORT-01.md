# WORKSHOP-COMM-PORT-01 — Deterministic Portable Controller Contract & Account-Neutral Simulation

TASK_ID: WORKSHOP-COMM-PORT-01
PROJECT: WORKSHOP COMMERCIAL EDITION
PRIORITY: HIGH
STATUS: COMPLETE
EXECUTION_CLASS: WORKER
CODEX_ALLOWED: NO
OBJECTIVE: bounded account-neutral simulation using repository-artifact semantics and explicit synthetic configuration.
SOURCE_PLAN_OR_REQUEST: owner-authorized campaign, 2026-10-24.
CURRENT_STATE: main 484240cddc47c489bc2787c433963e37079589c5; no executable canonical controller on main.
PREREQUISITES: canonical policies, schemas, coordination state and inactive staging controller reviewed.
DEPENDENCIES: no paid API, Codex, Work, or target runtime.
AFFECTED_COMPONENTS: only isolated simulation and this task registration.
PROTECTED_COMPONENTS: canonical WORKSHOP policies, schemas, status, scheduler and all target repos/TANGRA.
ACCEPTANCE_CRITERIA: isolated positive/negative scenarios, restart/readback, persisted evidence, separate independent Reviewer.
VALIDATION_METHOD: Python unittest discover (one bounded pass).
PRE_CHANGE_CHECKPOINT: main 484240cddc47c489bc2787c433963e37079589c5.
ROLLBACK_METHOD: delete isolated workshop-comm-port-01-simulation branch.
EVIDENCE_PATHS: simulations/workshop_comm_port_01/VALIDATION.md and PORTABLE_CONTROLLER_CONTRACT.md.
REVIEW_GATE: Independent Reviewer PASS for bounded synthetic simulation only, review/WORKSHOP-COMM-PORT-01.md at e0861b3b0de1bbfddc16645cdf36ab06f1e10ba4; no real account integration established.
IMPLEMENTATION_CHECKPOINT: 0d248fad2aa48ce28d073b489447a63a08bae207.
VALIDATED_CHECKPOINT: checkpoints/WORKSHOP-COMM-PORT-01.md.
CLOSURE_SCOPE: Documentation/coordination closure only; no deployment, Desktop build, cross-account trial or other work authorized.
