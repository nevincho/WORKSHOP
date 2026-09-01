# HOROS / LOCAL 3D — PHASE A SCOUT EVIDENCE

STATUS: READY_FOR_WORKER

## Scope validation
Phase A common contracts are the required common dependency for later time/geometry/range/map/recorder/replay work.

## Authorized inputs
Only curated `Workshop/HOROS_3D/**` material and campaign-local handoff/task material were used. No wider TANGRA discovery was performed.

## Duplicate check
Within the authorized campaign root, no implementation artifacts existed before this campaign except the four curated architecture/input documents. No competing campaign contract implementation was identified.

## Dependencies
- Curated architecture boundary: satisfied.
- Physical calibration/timing/pose evidence: not required for abstract contracts; remains NOT VERIFIED for metric/runtime claims.

## Acceptance
Use deterministic standard-library tests for construction, missing fields, validity/unavailable states, frame/timebase/timestamp mismatch, stale data, confidence bounds, non-finite numeric rejection, unknown preservation, and serialization round trip.

## Protected boundary
No production detector/Hailo, NanoTracker, CA Kalman, CURRENT_TARGET, command/actuation, runtime/configuration access or mutation is authorized.
