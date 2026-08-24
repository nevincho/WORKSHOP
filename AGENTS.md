# WORKSHOP Agent Bootstrap

STATUS: MANDATORY ENTRYPOINT FOR ALL AGENTS, CONTROLLERS AND CODEX HANDOFF PREPARATION

Before processing any task, in this order:

1. Read `README.md`.
2. Read all applicable files in `policies/`, especially AUTONOMY, REPOSITORY_COMMUNICATION, VALIDATION, EXECUTION_ROUTING, CODEX_BUDGET, HUMAN_GATE, CHECKPOINT_AND_BACKUP and REPORTING.
3. Read your role definition in `agents/`.
4. Read `registry/PROJECTS.md` and `registry/CONNECTIONS.md`.
5. Read the target `projects/<PROJECT>.md` profile.
6. Read `status/WORKSHOP_STATE.yaml` and `control_room/CURRENT.md`.
7. Read `schemas/TASK_SCHEMA.md`, `schemas/QUEUE_PROTOCOL.md`, `schemas/STATE_MACHINE.md` and any artifact schema relevant to the task.
8. Read the task from `tasks/` and current evidence/review/checkpoint/blocker/handoff artifacts for that TASK_ID.
9. Verify current target repository/runtime state before implementation claims or modifications.

Hard rules:
- WORKSHOP is coordination authority only; target repository/runtime evidence is implementation authority.
- Conversation history is not project state.
- Persist all substantive output to WORKSHOP.
- Never guess unavailable state; use NOT VERIFIED.
- Never duplicate work without checking existing state/evidence.
- Preserve protected components and validated behavior.
- Use the cheapest capable execution route.
- Codex is scarce and gated.
- COMPLETE requires independent Reviewer PASS and checkpoint evidence when implementation changed.

If instructions conflict, stop only the affected chain and record the conflict/blocker for Control Room resolution.