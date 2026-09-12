# WIDE-EW-05 — Legacy WIDE Runtime Isolation and Cleanup

PROJECT: TANGRA
CAMPAIGN: WIDE Acquisition Cue / Orientation
STATUS: BLOCKED
TYPE: ENGINEERING / RUNTIME DEPENDENCY AUDIT + SOURCE-LEVEL CLEANUP
CODEX: FORBIDDEN
PRODUCTION/Pi5 MODIFICATION: FORBIDDEN

## Objective
Reduce future active WIDE runtime to the accepted acquisition role only:
`WIDE capture -> latest frame -> cheap deterministic motion -> WideAcquisitionCue -> MC1/M1/M2/M3 passive acquisition/orientation chain`.

## Required acceptance
PASS requires exact current WIDE dependency inventory plus source-level proof that obsolete producers/workers/callbacks/queues/serializers/telemetry/API/Dashboard/environment/Video3D/mapping paths do not execute.

## Repository-grounded state
Current documentation establishes:
- WIDE capture retained;
- latest-only bounded worker semantics retained;
- WIDE detector observations historically publishable;
- environment/Video3D processing disabled by default in the latest checkpoint;
- legacy `world_map_3d` not redesigned;
- historical active WIDE 3D/light mapping carried substantial runtime cost and was explicitly prioritized for retirement;
- accepted WIDE-EW-01..04 acquisition contracts are repository-safe reference packages only.

## Blocker
The connected canonical repository `nevincho/TANGRA-DOCS` explicitly excludes source code, executable scripts and runtime configuration. Implementation authority remains the local/runtime engineering environment. The connected GitHub scope exposes no authoritative current DroneGuard development source tree from which Workshop can trace exact producers/callbacks/workers/serializers or perform source-level disconnection.

Therefore Workshop cannot honestly prove:
- exact current active WIDE dependency graph;
- producer not called;
- worker/thread not started;
- callback not registered;
- queue not populated;
- serializer not invoked;
- telemetry/API/Dashboard producer inactive;
- resource delta after source-level cleanup.

Documentation that a path is `disabled by default` is insufficient for this task's OFFLINE definition.

## Stop
Do not open carrier/FC work. Do not claim PASS. Resume WIDE-EW-05 only when the authoritative development source is available inside the Workshop engineering environment.
