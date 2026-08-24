# CODEX BUDGET POLICY

STATUS: MANDATORY
APPLIES TO: ALL AGENTS, CODEX, AUTOMATIONS
OVERRIDE: ONLY VLAD / WORKSHOP CONTROL ROOM

Codex capacity is scarce and must be conserved.

Codex MUST NOT be used for repository discovery, general audits, inventory, documentation reading, task decomposition, mechanical file work, log summarization, evidence collection, or validation that another capable worker can perform.

Before escalation to Codex, WORKSHOP must provide a minimal implementation package containing: task ID, exact objective, verified current state, affected components, prerequisites, protected components, acceptance criteria, validation method, rollback/checkpoint, and explicit non-goals.

CURRENT OPERATING MODE — HUMAN CODEX GATE:
1. Agents and automations MUST NOT invoke Codex automatically.
2. Codex Gate may inspect a task and prepare a minimal Codex handoff package, but execution requires explicit approval from Vlad / WORKSHOP Control Room for that specific task.
3. Agents should complete all repository-side analysis, preparation, low-risk implementation, fixtures, tests, documentation, evidence and review that can be done without Codex.
4. When a task reaches the point where Codex is justified, record it as `READY_FOR_CODEX_REVIEW` with the prepared handoff; do not execute Codex.
5. Vlad may then take tasks one at a time for Codex-assisted integration/testing on the relevant runtime or host.
6. No implicit approval carries from one task to another. Each Codex execution requires a fresh explicit approval unless Vlad later changes this operating mode.

Use Codex only after explicit approval for non-trivial implementation, difficult debugging, sensitive integration, architecture-dependent precision work, or work beyond validated worker capability.

Never resend a failed Codex task without first identifying why the previous attempt was insufficient.
