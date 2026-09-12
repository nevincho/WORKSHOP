# WIDE-EW-05 — Engineering Result

DATE: 2026-09-12
MODE: WORKSHOP ENGINEERING / SOURCE-LEVEL CLEANUP REQUIRED
VERDICT: BLOCKED

## ACTIVE_WIDE_BEFORE
Repository-grounded current evidence supports only this bounded view:

1. `WIDE IMX708 capture` — active/available; required by accepted acquisition role.
2. `latest-only bounded WIDE worker/path` — retained; historically introduced to decouple WIDE from HQ critical loop.
3. `WIDE detector observation publication` — documented as publishable in current checkpoint; exact current producer/consumer code not available here.
4. `WIDE environment / Video3D processing` — documented as disabled by default in current checkpoint, but source-level non-instantiation/non-scheduling is NOT VERIFIED.
5. `WIDE -> HOROS local environment/map` — historical active path; architecture decision prioritizes retirement of active 3D/light mapping workload. Exact current source-level bindings are NOT VERIFIED.
6. `world_map_3d` legacy contribution — documented as not redesigned; exact current WIDE dependency is NOT VERIFIED.
7. WIDE telemetry/API/Dashboard plumbing — exact fields, serializers, producers and consumers are NOT VERIFIED from the connected documentation-only repository.

Historical evidence establishes why cleanup is required: active WIDE 3D/light mapping previously showed ~507 ms average sampled worker latency, stale outputs, shared detector-lock contention path and explicit retirement priority. This evidence is historical diagnostic evidence, not proof of current execution.

## KEEP_ACTIVE
Required by accepted WIDE-EW architecture:
- WIDE capture;
- latest-frame/latest-value semantics;
- deterministic `WideCueGenerator` candidate from WIDE-EW-01;
- `WideAcquisitionCue v1`;
- MC1/M1 acquisition bridge;
- M2 `ORIENT_OBSERVATION_AXIS` passive guidance;
- M3 passive `ORIENT_OBSERVATION_AXIS` intent.

Exact runtime integration points for these repository-safe packages are not yet available in authoritative source and are therefore not claimed as live.

## DISCONNECTED
NOT VERIFIED at source level.

Documentation says environment processing is disabled by default, but WIDE-EW-05 requires stronger proof: not instantiated, scheduled, polled, subscribed, producing, consuming, queueing, serializing, publishing telemetry, updating API/Dashboard state or running background workers. The connected evidence cannot establish those conditions.

## DELETED
NONE.

No source deletion was performed because authoritative development source is unavailable in the connected Workshop/GitHub scope.

## ARCHIVED_OFFLINE
Candidate classifications only, not execution claims:
- legacy WIDE continuous 3D/light environment mapping: ARCHIVE_OFFLINE candidate;
- legacy Video3D WIDE environment contribution: ARCHIVE_OFFLINE candidate;
- obsolete WIDE-to-local-world mapping producer chain: ARCHIVE_OFFLINE candidate;
- legacy `world_map_3d` WIDE-specific contribution: requires exact dependency trace before archive/delete;
- obsolete WIDE detector inference/publication path: DISCONNECT candidate if no accepted acquisition consumer remains.

## PRODUCERS_STOPPED
NOT VERIFIED.

## WORKERS_STOPPED
NOT VERIFIED. Current docs prove only that environment processing is disabled by default, not that every legacy WIDE worker/thread/task is absent.

## CALLBACKS_REMOVED
NOT VERIFIED.

## QUEUES_REMOVED_OR_INACTIVE
NOT VERIFIED. Historical latest-only queue capacity 1 is known; exact current queue topology and whether obsolete queues are populated cannot be established without source/runtime inspection.

## SERIALIZERS_REMOVED_OR_INACTIVE
NOT VERIFIED.

## TELEMETRY_REMOVED_OR_INACTIVE
NOT VERIFIED. No cosmetic telemetry deletion was attempted.

## API_DASHBOARD_PLUMBING
NOT VERIFIED. Exact WIDE serializers/API fields/Dashboard feed consumers require authoritative source inspection. No display-only cleanup was claimed.

## ENVIRONMENT_VIDEO3D_MAPPING_STATUS
Architecture classification: active continuous WIDE environment/Video3D/mapping is NOT REQUIRED by the accepted acquisition role and should be disconnected at source and retained only offline/archive where useful.

Current implementation fact available from docs: environment processing is `disabled by default`.

WIDE-EW-05 acceptance fact: ZERO ACTIVE EXECUTION is NOT VERIFIED.

## ACTIVE_WIDE_AFTER
Cannot be truthfully established without authoritative source-level implementation and execution evidence.

Desired post-cleanup active path remains:
`WIDE capture -> latest frame -> WideCueGenerator -> WideAcquisitionCue -> MC1 -> M1 -> M2 -> M3 passive intent`.

No carrier/FC output is part of this path.

## RESOURCE_BEFORE
Historical evidence only:
- active WIDE mapping diagnostic window: sampled WIDE worker latency avg ~507.371 ms, min 439.569 ms, max 562.422 ms;
- WIDE freshness failed in that historical window;
- later decoupled WIDE path achieved substantially better HQ FPS and WIDE cadence.

These values are not a current WIDE-EW-05 before-measurement.

## RESOURCE_AFTER
NOT MEASURED.

## RESOURCE_DELTA
NOT MEASURED.

`PI5_NOT_MEASURED`.

## REGRESSION
Cannot execute the required retained-runtime regression because authoritative current DroneGuard development source/runtime is unavailable inside the connected Workshop engineering scope.

Repository-safe WIDE-EW-01..04 contract packages remain unchanged.

Required live/source regressions remain OPEN:
- WIDE_CAPTURE_RETAINED;
- LATEST_FRAME_RETAINED;
- WIDE_CUE_PATH_RETAINED;
- MC1_M1_M2_M3_CONTRACTS_UNCHANGED;
- HQ_AUTHORITY_UNCHANGED;
- N1_UNCHANGED;
- HOROS_AUTHORITY_UNCHANGED;
- LEGACY_ENVIRONMENT_PATH_INACTIVE;
- LEGACY_VIDEO3D_PATH_INACTIVE;
- OBSOLETE_TELEMETRY_PRODUCERS_INACTIVE;
- NO_COMMAND_AUTHORITY.

## PROTECTED_AUTHORITIES
No modifications were made to HQ detector, NanoTracker, CA Kalman, CurrentTargetManager, HOROS, N1, MC1/M1/M2/M3 accepted semantics, FC/carrier adapter, command-send authority or production.

## BLOCKER
`nevincho/TANGRA-DOCS` explicitly states that it is documentation/evidence only and excludes source code, executable scripts and runtime configuration; implementation authority remains the real local/runtime engineering environment. The connected GitHub repositories do not expose the authoritative current DroneGuard development source tree required for exact dependency tracing and source-level isolation.

Because WIDE-EW-05 explicitly rejects `disabled but still computing`, documentation-only evidence cannot satisfy acceptance.

## FILES
- `tasks/WIDE-EW-05-LEGACY-WIDE-RUNTIME-ISOLATION-CLEANUP.md`
- this evidence file
- `review/WIDE-EW-05.md`

## ENGINEERING_VERDICT
BLOCKED — authoritative development source/runtime access is required to complete this unit without fabricating execution evidence.
