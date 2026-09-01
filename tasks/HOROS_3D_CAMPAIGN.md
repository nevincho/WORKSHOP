# TANGRA — HOROS / LOCAL 3D / MISSION REPLAY CAMPAIGN

STATUS: READY_FOR_CODEX_REVIEW

## Objective
Prepare an isolated, shadow/off-by-default repository-side implementation package for HOROS spatial evidence, Local 3D estimation, persistent sparse mapping, Mission Recorder, Mission Replay/Tactical Replay and diagnostic/retraining-preparation interfaces.

## Target
`nevincho/TANGRA-DOCS` branch `workshop-horos-3d`, restricted to `Workshop/HOROS_3D/**`.

## Protected components
Production detector/Hailo, NanoTracker, existing CA Kalman, CURRENT_TARGET, command/actuation and validated production runtime/configuration remain untouched.

## Repository-side result
Implemented and deterministically validated contracts, time/geometry/range/Local3D algorithms, carrier transforms, sparse local map, localization contract, HOROS coordinator/fail-open behavior, bounded Mission Recorder/replay parser, Tactical Replay model and diagnostic/retraining-preparation interfaces.

## Validation
31 deterministic tests PASS; compileall PASS. Exact executed-file blob identities are documented in the target repository implementation manifest.

## Review
Independent consolidated review: PASS for repository-side scope.

## NOT VERIFIED
Physical calibration/metric accuracy, authoritative active-source adapter compatibility, recorder sizing under actual runtime rate, dashboard/runtime integration, shadow runtime behavior and `HOROS OFF` baseline equivalence.

## Execution boundary
No Codex execution, no Pi/runtime access, no production deployment or production-source mutation occurred.
