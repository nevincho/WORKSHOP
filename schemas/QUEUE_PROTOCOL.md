# WORKSHOP Queue Protocol

STATUS: MANDATORY

Queue priority: CRITICAL -> HIGH -> MEDIUM -> LOW, then oldest eligible task first unless project policy overrides.

Before claiming a task, Controller/Scout must verify: current state, prerequisites, dependencies, project phase, protected scope, validation method, execution access and cheapest capable route.

Eligible task: STATUS READY; dependencies COMPLETE or explicitly non-blocking; no unresolved human gate; execution path available or diagnostic task can proceed read-only.

## Dependency / blocker auto-unlock
A BLOCKED task may be promoted automatically to READY only when ALL explicit unblock conditions recorded in that task are independently verified as satisfied.

Rules:
- A dependency PASS/COMPLETE alone is insufficient when the task defines additional prerequisites, execution-route, validation, credential, hardware, policy, checkpoint, rollback or human-gate conditions.
- Controller must re-read the full task and current evidence before promotion.
- Promotion must record which unblock conditions were satisfied and the supporting evidence.
- If any unblock condition remains unsatisfied or NOT VERIFIED, keep the task BLOCKED and continue independent eligible work.
- Never change BLOCKED -> READY merely because an upstream task changed state.
- After a valid promotion, the Controller may process the newly READY task in the same run, subject to normal priority and safety rules.

Routing:
- SCOUT/PREP: reconnaissance and task validation.
- WORKER: low-cost/mechanical/low-risk execution.
- CODEX_CANDIDATE: pass through Codex Gate only.
- REVIEW: independent verification.
- HUMAN_GATE: Control Room decision required.

Blocked chains do not stall independent eligible work.

Every claim/release/routing decision must be persisted in the task or evidence/handoff artifact. Do not use agent-chat chronology as queue state.

A task must not be executed twice merely because multiple agents discover it. Existing IN_PROGRESS/REVIEW/COMPLETE evidence must be checked before action.