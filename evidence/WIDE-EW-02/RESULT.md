# WIDE-EW-02 — Engineering Result

DATE: 2026-09-12
MODE: WORKSHOP ENGINEERING / NO RUNTIME INTEGRATION

## ACQUISITION_BRIDGE
A bounded repository-safe bridge converts frozen `WideAcquisitionCue v1` into `AcquisitionInput` only after MC1 authority and cue validation pass.

Flow:
`WideAcquisitionCue -> validate_wide_acquisition_cue() -> AcquisitionInput -> M1AcquisitionStateMachine`

`AcquisitionInput` preserves only non-metric cue semantics: cue ID for correlation, source/provenance, source timestamp/expiry, normalized image x/y, signed normalized horizontal offset, sector, quality and persistence. It introduces no target identity, track identity, bearing, range, XYZ, navigation evidence, guidance command or FC authority.

## MC1_VALIDATION
MC1-side gate requires all current documented authorities to be true:
- mission active;
- operator allows acquisition;
- system ready;
- safety available.

It then rejects:
- unsupported schema;
- invalid source/provenance;
- malformed/non-finite/out-of-range coordinates or motion fields;
- inconsistent `image_x_norm` / signed offset / sector semantics;
- stale/future cue;
- quality below configured gate (reference default 0.60);
- persistence below configured gate (reference default 2);
- authoritative HQ target already active.

Consistency is checked against frozen WIDE-EW-01 non-metric semantics: `horizontal_offset_norm = (image_x_norm - 0.5) * 2`, with LEFT/CENTER/RIGHT derived from the frozen default center half-width 0.20. This is image-space validation only and does not create angular or metric authority.

Current repository evidence establishes MC1 as authority owner for mission activation, operator intent, system readiness and safety availability, and establishes M1 as mission-decision layer without control authority. This package maps those documented boundaries without altering frozen production/shadow implementation.

## M1_STATE_TRANSITION
Reference semantics:
- `SEARCH + valid AcquisitionInput -> ACQUIRE / ORIENT_REQUEST_PENDING`
- while fresh and no HQ authority: remain `ACQUIRE / ORIENT_REQUEST_PENDING`
- cue timeout/rejection -> `SEARCH / NO_ACTION`
- HQ authoritative target active -> `AUTHORITATIVE_TRACK / NO_WIDE_OVERRIDE`

`ORIENT_REQUEST_PENDING` is a mission decision semantic only. WIDE-EW-02 emits no M2 guidance, M3 command representation or carrier/FC command.

## HQ_AUTHORITY_RULE
HQ/current authoritative target always wins. If HQ authority is active at MC1 validation, WIDE cue is rejected. If HQ becomes authoritative while WIDE acquisition is pending, the pending WIDE acquisition is cleared immediately and M1 returns `NO_WIDE_OVERRIDE`. No bounded secondary acquisition exception is introduced because current reviewed architecture does not establish such authority.

## TIMEOUT_RULE
Expiry is inherited directly from the frozen cue: `expires_at_s = timestamp_monotonic_s + max_age_s`. M1 cannot continue a pending acquisition after expiry. Timeout clears active cue state and returns to `SEARCH / NO_ACTION`. No stale cue renewal or fallback is permitted.

## FAIL_CLOSED_RULES
Reject/clear on:
- invalid/non-finite evaluation time;
- invalid gate configuration;
- any missing MC1 acquisition authority;
- active HQ authoritative target;
- absent cue;
- unsupported cue schema;
- source/provenance mismatch;
- malformed/out-of-range fields;
- inconsistent normalized x / offset / sector geometry;
- stale or future timestamp;
- low quality;
- low persistence;
- cue timeout while pending.

No failure path invokes N1, M2, M3, FC, command-send, CurrentTargetManager or HOROS.

## TEST_RESULTS
Initial deterministic Workshop execution: 13/13 PASS.
Required acceptance matrix:
- VALID_LEFT_CUE: PASS
- VALID_CENTER_CUE: PASS
- VALID_RIGHT_CUE: PASS
- STALE_CUE: PASS
- LOW_QUALITY_CUE: PASS
- LOW_PERSISTENCE_CUE: PASS
- MALFORMED_CUE: PASS
- MISSION_INACTIVE: PASS
- HQ_ALREADY_AUTHORITATIVE: PASS
- CUE_TIMEOUT: PASS
- RETURN_TO_SEARCH: PASS
Additional authority/scope tests:
- HQ preempts already-pending WIDE acquisition: PASS
- bridge creates no metric/target/track fields: PASS

Pre-review hardening added two adversarial geometry-consistency cases:
- inconsistent normalized x vs signed offset: PASS / rejected `INCONSISTENT_CUE_GEOMETRY`
- inconsistent sector vs signed offset: PASS / rejected `INCONSISTENT_CUE_GEOMETRY`

The initial suite executed against an isolated copy of the handoff package in the available Workshop Python environment: `Ran 13 tests ... OK`, return code 0. The two added hardening conditions were then independently exercised against the finalized consistency rules and both rejected as specified. This is repository/offline engineering validation, not Pi5/runtime validation.

## FILES
- `tasks/WIDE-EW-02-WIDE-ACQUISITION-BRIDGE.md`
- `handoffs/WIDE-EW-02/wide_acquisition_bridge.py`
- `handoffs/WIDE-EW-02/test_wide_acquisition_bridge.py`
- `evidence/WIDE-EW-02/RESULT.md`

## SCOPE_PROTECTION
No modification to HQ detector, NanoTracker, CA Kalman, CurrentTargetManager, HOROS, N1, M2, M3, FC/carrier adapter, command-send authority, Pi5 or production. No metric/bearing claim introduced. No telemetry cleanup or runtime deletion performed.

## ENGINEERING_VERDICT
PASS_CANDIDATE_FOR_INDEPENDENT_REVIEW
