# HOROS / LOCAL 3D — PHASE A COMMON CONTRACTS

STATUS: READY_FOR_WORKER
CAMPAIGN: TANGRA HOROS / LOCAL 3D / MISSION REPLAY
TARGET: nevincho/TANGRA-DOCS branch workshop-horos-3d
WRITE_SCOPE: Workshop/HOROS_3D/** only

## Objective
Create the minimal common repository-side contract/state foundation required by all later HOROS / Local 3D / Mission Replay lanes.

## Authorized inputs
Only files under `Workshop/HOROS_3D/` and this task package. General TANGRA discovery is forbidden.

## Protected components
Do not modify detector/Hailo, NanoTracker, existing CA Kalman, CURRENT_TARGET, command/actuation, production runtime/configuration.

## Required implementation
Under `Workshop/HOROS_3D/implementation/horos3d/`, create small dependency-free Python modules for:

- schema/version primitive;
- timestamp/timebase representation;
- coordinate-frame representation;
- validity state;
- provenance/source identity;
- quality/confidence representation;
- optional uncertainty/covariance representation with explicit unavailable state;
- `HorosObservation`;
- `CarrierPoseObservation`;
- `CameraLOSObservation`;
- `RangeHypothesis`;
- `Local3DState`;
- `MapConstraint`;
- `HorosSpatialEvidence`;
- `HorosHealth`.

Use explicit `None`/unavailable state for unknown values. Never substitute zero for unavailable range/depth/position/covariance/timestamp precision/pose/calibration.

## Contract invariants

1. Every spatial/evidence object carries schema version, timestamp, timebase, frame, validity, provenance, and freshness/age information where applicable.
2. Confidence, if present, is bounded to [0,1].
3. Numerical vectors must be finite when present.
4. Invalid/unavailable states must be representable without fabricated geometry.
5. Frame mismatch and timestamp mismatch are detectable and must not silently coerce.
6. Physical calibration values are not embedded in production-like defaults.
7. Serialization, if implemented, round-trips without converting unknown into zero.
8. Cross-camera target identity is represented explicitly; contracts do not infer identity.

## Tests
Create deterministic unit tests under `Workshop/HOROS_3D/tests/` covering at minimum:

- valid construction;
- missing required-field rejection;
- invalid-state behavior;
- frame mismatch detection;
- stale-data detection;
- timestamp mismatch detection;
- confidence bounds;
- non-finite numeric rejection;
- unknown remains unknown;
- serialization round trip for serializable contracts.

## Acceptance criteria

- Tests execute successfully using only standard Python library.
- No access outside authorized campaign root is required.
- No production/runtime component is imported or modified.
- No synthetic value is presented as physical calibration/runtime truth.
- Repository hygiene: no caches, generated output, scratch variants, or obsolete task-local files remain.
- Worker evidence lists exact files and test command/result.

## Evidence classification
Repository-side algorithm/contracts validation may become VERIFIED when tests pass. Physical metric accuracy and production integration remain NOT VERIFIED.
