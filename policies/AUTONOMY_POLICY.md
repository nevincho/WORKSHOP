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
