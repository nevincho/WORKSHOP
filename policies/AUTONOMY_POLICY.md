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
