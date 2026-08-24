# WORKSHOP

WORKSHOP is the coordination/control-plane repository for autonomous engineering work across linked projects.

It does not replace target repositories or runtimes as implementation source of truth.

Current bootstrap status: **BOOTSTRAPPED FOR AUTONOMY TESTING**.

Execution principle:

`inspect -> validate task -> route cheapest capable executor -> execute -> test -> checkpoint -> independent review -> continue`

## Mandatory bootstrap order for agents/controllers
1. Read `policies/`.
2. Read `registry/PROJECTS.md` and `registry/CONNECTIONS.md`.
3. Read the relevant `projects/<PROJECT>.md` profile.
4. Read `status/WORKSHOP_STATE.yaml` and `control_room/CURRENT.md`.
5. Read task/queue schemas and the assigned task.
6. Verify target repository/runtime state before implementation claims or changes.

## Core directories
- `policies/` — mandatory operating rules.
- `agents/` — role definitions.
- `projects/` — project-specific boundaries/routing.
- `registry/` — connection and coordination map.
- `tasks/` — canonical task definitions.
- `queue/` — queue protocol reference; task STATUS is canonical queue state.
- `evidence/` — role/task evidence.
- `handoffs/` — cross-role and Codex implementation packages.
- `review/` — independent review verdicts.
- `checkpoints/` — validated working points and rollback references.
- `blockers/` — evidence-backed blockers.
- `decisions/` — explicit human/Control Room decisions.
- `reports/` — 8h/12h/24h summaries.
- `schemas/` — mandatory artifact formats/state machine.
- `status/` — machine-readable/current coordination state.
- `control_room/` — human coordination handoff state.

## Authority
WORKSHOP is authoritative for coordination state only. Target project repository/runtime evidence is authoritative for architecture, implementation, validation, completed work and blockers.

All substantive agent communication must be persisted in WORKSHOP. Agent chat history is non-authoritative.