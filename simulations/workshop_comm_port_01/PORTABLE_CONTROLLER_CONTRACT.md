# WORKSHOP-COMM-PORT-01 — Portable Controller Contract

Reference: WORKSHOP main 484240cddc47c489bc2787c433963e37079589c5. This bounded simulation does not modify canonical policy.

Inputs: fresh synthetic customer, repository and one task ID/scope, human-gate flag, permitted executors and positive write allowlist. No historical chats, owner credentials or paid services.

Deterministic contract:
1. Load explicit configuration and immutable canonical model constraints.
2. Discover one configured synthetic task (live repo enumeration NOT TESTED).
3. Validate prerequisites, protected scope and executor allowlist.
4. Admit READY -> IN_PROGRESS only when human gate (if set) is approved.
5. Select a zero-cost mock executor and persist structured Worker evidence.
6. Transition IN_PROGRESS -> REVIEW; verify evidence and write review verdict.
7. Only accept REVIEW -> COMPLETE with a PASS and checkpoint reference.
8. Enforce BLOCKED -> READY only when explicit unblock verification supplied.
9. Persist hash-linked event sequence for fresh-controller restart readback.
10. Reject unauthorized writes, invalid transitions, scope expansion, paid/unapproved executor selection and corrupt event chain.

Canonical state machine remains the authority. Simulation covers a subset, not every canonical transition. Human approval provenance is NOT VERIFIED. Reviewer in simulated flow is an automated verifier, not an independently instantiated WORKSHOP Reviewer. Interruption readback is tested, but interrupted Worker idempotence and filesystem power-loss atomicity are NOT VERIFIED.

Configuration format (illustrative):
```json
{"customer":"synthetic-customer","repository":"synthetic/demo","task":{"id":"DEMO-001","scope":"synthetic","human_gate":false},"executors":{"mock":{"paid":false},"codex":{"paid":true}},"allowed_executors":["mock"],"writable_paths":["state/events.json","evidence/worker.json","review/verdict.json","checkpoints/snapshot.json"]}
```

Commercial gaps: real GitHub account onboarding/auth, live task discovery, separate Reviewer, scheduler, credential/approval provenance, multi-user isolation, crash-safe persistence, GUI and installer.
