# CONTROL ROOM POLICY

STATUS: MANDATORY

The active Control Room is the human coordination interface. It may discuss architecture, priorities, human gates, and scheduled reports, but repository state remains authoritative.

Rotation:
- recommended new Control Room every 24 hours;
- hard maximum 48 hours;
- rotate earlier after a major architectural or policy checkpoint.

Before rotation, write/update `control_room/CURRENT.md` with current tasks, blockers, decisions, checkpoints, human gates, next actions, and latest report references. Historical checkpoints may be stored under `control_room/checkpoints/`.

A new Control Room must bootstrap from WORKSHOP policies, registry, current state, queues, blockers, checkpoints and latest reports. Do not rely on the previous chat transcript as project state.

Old Control Room chats are archival/non-authoritative once handoff is verified.