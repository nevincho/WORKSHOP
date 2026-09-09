# N1 Navigation Evidence — Engineering Evidence

TASK_ID: TASK-TANGRA-M2-NAVIGATION-EVIDENCE-N1-20260909
STATUS: READY_FOR_INDEPENDENT_REVIEW
ARTIFACT_TYPE: CONTRACT / THIN ADAPTER / VALIDATION PACKAGE

## Source extraction
Frozen M2 reviewed commit: `75417cb4356a79e61d1196f3f859fa7cd7ba08e8`.
Frozen M2 implementation blob: `5616d5930c8ffca0cef7876d6c192bc7627efb2c`.
Frozen M3 reviewed commit: `f041325369edea08888f8ee9ec5fd7ab9ce0e1ce`.
M2 accepts `GuidanceInput(mission_decision, navigation: Optional[NavigationEvidence], evaluated_at)`.
The exact field/use matrix is recorded in `M2_NAVIGATION_FIELD_TABLE.md`.

## Existing authority mapping
- CurrentTargetManager is mission identity authority feeding HOROS identity.
- HOROS is downstream spatial state with XYZ, velocity, covariance/uncertainty, provenance and lifecycle.
- HOROS local scene/map is carrier-relative.
- HOROS metric path is range/LOS -> XYZ; physical class-size accuracy remains not yet validated.
- gps_bridge / MAVLink exist, but exact heading/altitude field/datum/frame contracts were not source-verified for this task and are not consumed by N1.

## Frame rule
N1 performs no frame transform.
Accepted source semantics are exactly `CARRIER_RELATIVE_LOCAL_METRIC`.
`source.frame_ref` must exactly equal M1 expected frame_ref.
`carrier_xyz_m=(0,0,0)` is emitted only when `carrier_origin_is_zero=True` and exact carrier-relative frame semantics are present. This is the frame-origin definition, not target-position reuse or carrier-position estimation.
Any other frame semantic or frame mismatch fails closed.

## Uncertainty rule
For VERIFIED non-LOST target geometry, N1 requires explicit 3x3 symmetric positive-semidefinite position covariance with semantics exactly `POSITION_COVARIANCE_3X3_M2`.
Row-major covariance units are m^2.
N1 maps `uncertainty_m = sqrt(trace(P_xyz))`.
For PSD P, `trace(P) >= lambda_max(P)`, so the scalar does not understate standard deviation along any unit spatial direction. It is the Euclidean RMS 1-sigma position error implied by P.
Missing/malformed/semantically unidentified covariance fails closed for VERIFIED active TRACK.

## Search geometry
N1 never derives search vectors from target XYZ, velocity, image orientation or heading.
`search_relative_vector_m` is None unless an explicit same-target, same-frame, fresh, VERIFIED `ExplicitSearchGeometry` is supplied.

## Fail-closed
No M2 payload is emitted for target mismatch, frame mismatch/unsupported semantics, missing carrier-origin authority, stale/future/malformed timestamps, stale observation age, malformed/absent VERIFIED target XYZ, missing/invalid VERIFIED covariance, malformed covariance, invalid explicit search geometry, or source marked production_authority=True.
NOT_VERIFIED evidence may be preserved as NOT_VERIFIED; it is never promoted to VERIFIED and frozen M2 degrades it.

## Tests
27 deterministic tests PASS locally.
Compatibility tests load the real frozen M1, M2 and M3 artifact implementations from WORKSHOP paths.
Exact behavior:
- valid VERIFIED carrier-relative HOROS fixture -> M2 AVAILABLE / MAINTAIN_OBSERVATION;
- same M2 output -> M3 SUPPRESSED / NO_COMMAND because no movement vector is fabricated;
- HOLD -> M2 HOLD -> M3 HOLD;
- ABORT -> M2 ABORT_HOLD -> M3 HOLD with abort_semantic=True;
- high uncertainty -> M2 DEGRADED;
- target/frame/staleness/covariance failures fail closed.

## Runtime availability boundary
The adapter package is software-complete and deterministic.
Before future Codex runtime integration may supply active VERIFIED TRACK evidence, local source inspection must bind:
1. exact HOROS frame_ref and prove it is the carrier-relative metric frame used by M1;
2. exact HOROS 3x3 target position covariance layout and units as m^2;
3. CurrentTarget/HOROS target_ref continuity at the call point;
4. current metric_status truth; physical VERIFIED must not be claimed from provisional/non-validated range evidence.

CONTROL_AUTHORITY: NONE
PRODUCTION_INTEGRATION: NO
