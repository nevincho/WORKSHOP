# LORA-03 — Receiver Link Observer

Status: PASS / isolated Workshop implementation for deterministic receiver-side link/order semantics.

Authoritative dependency: accepted LORA-02 v1 codec package at commit `f24e5c3064b0331df0c231f752f3ff5571c931a6`.

Validation: LORA-03 tests 31/31 PASS; LORA-02 regression 47/47 PASS; Python compileall PASS.

No wire-format changes. No physical transport. No production, Dashboard, DroneGuard, WIDE, command, IFF, readiness, or actuation changes.

The observer supports independent state per `source_id`; this is source isolation only, not a fleet/swarm architecture.

Files:
- `SEMANTICS.md`
- `TEST_EVIDENCE.md`
- `lora03_link/observer.py`
- `lora03_link/mock_channel.py`
- `tests/test_link_observer.py`

Local complete archive produced during validation: `LORA_03_LINK_OBSERVER.tar.gz`.
