# AUTONOMY POLICY

STATUS: MANDATORY
APPLIES TO: ALL AGENTS, CODEX, AUTOMATIONS
OVERRIDE: ONLY VLAD / WORKSHOP CONTROL ROOM

1. Target repositories/runtime evidence are authoritative for implementation state.
2. WORKSHOP is authoritative for coordination state only.
3. Agents must inspect current target state before execution.
4. Tasks must be checked for relevance, duplication, prerequisites, current phase, protected components, and valid acceptance criteria.
5. Autonomous work may continue task-to-task without human approval when policy allows and validation passes.
6. Stop or isolate a dependency chain on real blocker, protected change, destructive operation, missing prerequisite, or unverifiable acceptance method.
7. Prefer the smallest justified change. No speculative redesign or unrelated refactoring.
8. Never claim completion without evidence.
9. `decisions/CANONICAL_BACKLOG_2026-08-24.md` is the active deduplication/routing authority for the current VK and Mysticarium backlog. Tasks marked SUPERSEDED there MUST NOT be implemented or sent to Codex.
10. SAME-RUN CHAINING: after independent PASS, recompute dependencies immediately. If another non-duplicate task is eligible and all execution, validation, checkpoint/rollback and protection requirements are satisfied, continue to that task in the same controller run. Do not wait for the next hourly trigger solely because a prior task completed.
11. Same-run chaining stops on a real blocker, human gate, protected/destructive operation, unavailable validation method, unavailable required Codex capacity, or when no eligible task remains.
12. A BLOCKED task may become READY only when its stated prerequisite is directly evidenced as satisfied; do not mass-promote backlog tasks.
13. WORKER ROUTING: a canonical task with Scout evidence marked `READY_FOR_WORKER` is an executable Worker handoff. Worker MUST read the task file, canonical backlog and current `evidence/TASK-xxx/SCOUT.md` before consulting summary state. `status/WORKSHOP_STATE.yaml` is an index and MUST NOT override a newer explicit canonical handoff.
14. If `WORKSHOP_STATE.yaml` is stale relative to a canonical task/handoff, continue from the newer task/handoff when policy permits and then reconcile the state index. Do not return `NO SAFE EXECUTABLE WORKER TASK` solely because the summary state has not yet been updated.
15. Worker may perform repository-side low-risk implementation, fixtures, mocks, deterministic/simulation tests, test infrastructure and evidence required by the active task. Real runtime deployment/integration, protected changes and Codex execution remain human-gated where specified.
16. Reviewer must review actual Worker output/diffs/test evidence, not Scout preparation alone. If Worker output is absent, report `NOT YET REVIEWABLE` rather than re-auditing an already known blocker.
