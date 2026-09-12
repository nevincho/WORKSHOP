# TAI-COG-21 — Cognitive Signal Layer

STATUS: COMPLETE
TYPE: WORKSHOP ENGINEERING / IMPLEMENTATION-READY UNIT

Objective: provide a bounded passive signal abstraction over reviewed COG-04/18/19/20 outputs with optional COG-09 passive observer identity/context.

Engineering repo: `nevincho/TANGRA-2.0`
Branch: `tai-cog-21`
Base: `ea9777ee9f5b57bde75e641ad7885d5069228c26`
Reviewed head: `7d8e4d2804ef9f59dd33f206fb490c2ae9f9ab37`

Hard invariants: SIGNAL != COMMAND; SIGNAL != AUTHORITY; SIGNAL != ACTION. No backend invocation, diagnostic/replay/Twin execution, transport, remediation, tuning, approval, configuration/mission/target mutation, command dispatch, Pi integration, Codex, or COG-22 work. MISSION_CONSTRAINED performs lightweight deterministic formatting/filtering over pre-existing bounded inputs only.