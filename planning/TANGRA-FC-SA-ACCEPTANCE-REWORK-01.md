# Planner — TANGRA-FC-SA-ACCEPTANCE-REWORK-01

STATUS: IMPLEMENTATION_READY

## Minimal repair plan
- STEP_2: make per-source sequence replay semantics explicit: equal sequence = DuplicateSequence, lower = OutOfOrderSequence, neither may overwrite accepted state.
- STEP_3: retain existing plant/controller/mixer/estimator contracts; add only missing simple X/Y kinematics so the actual plant can satisfy a local spatial objective in end-to-end simulation.
- STEP_4/5: add real observation-to-state producers with timestamp/freshness/validity behavior.
- STEP_7: remove lifecycle enum/interface ownership from waypoint package; consume one shared Mission Lifecycle v1 contract.
- STEP_8: add configurable MAVLink message binding for goal/ACK/telemetry payloads while keeping actual USB/frame transport an integration adapter.
- STEP_9: replace throwing string conversions with fail-closed numeric parsing and validate malformed numeric fields with valid checksums.
- STEP_10-12: exercise real watchdog, navigation observation and Mission Planner adapter behavior inside the end-to-end gate.
- Integration: STEP_12 -> MAVLink/STEP_8 -> STEP_7/Lifecycle -> STEP_11 -> STEP_5/4 -> STEP_6 -> STEP_2 -> STEP_3 closed loop, with STEP_9 configuring limits and STEP_10 causing safety takeover on deadline expiry.

No physical actuation. No alternate production controller.
