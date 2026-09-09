# N1 Navigation Evidence — Engineering Evidence

TASK_ID: TASK-TANGRA-M2-NAVIGATION-EVIDENCE-N1-20260909
STATUS: READY_FOR_INDEPENDENT_REREVIEW_CYCLE3
ARTIFACT_TYPE: CONTRACT / THIN ADAPTER / VALIDATION PACKAGE

Frozen M2 reviewed commit: `75417cb4356a79e61d1196f3f859fa7cd7ba08e8`.
Frozen M2 implementation blob: `5616d5930c8ffca0cef7876d6c192bc7627efb2c`.
Frozen M3 reviewed commit: `f041325369edea08888f8ee9ec5fd7ab9ce0e1ce`.

## Exact purpose
Convert explicitly typed existing HOROS carrier-relative metric target evidence into kwargs for frozen M2 `NavigationEvidence` without frame conversion, new estimation, target/carrier confusion, search synthesis or authority escalation.

## Frame contract
Accepted frame semantics: `CARRIER_RELATIVE_LOCAL_METRIC` only.
Expected M1 target/frame refs, HOROS source refs and explicit search refs must be exact non-whitespace strings and match exactly.
No ENU/NED/body/camera/world conversion is performed.
When the source explicitly proves carrier-relative frame semantics and `carrier_origin_is_zero=True`, N1 emits `carrier_xyz_m=(0,0,0)` as the mathematical frame origin. It never substitutes target XYZ as carrier XYZ.

## Uncertainty contract
For VERIFIED non-LOST target geometry N1 requires exact covariance semantics string `POSITION_COVARIANCE_3X3_M2` and a finite symmetric PSD 3x3 row-major position covariance in m^2.
Scalar rule: `uncertainty_m = sqrt(trace(P_xyz))`.
For PSD P, `trace(P) >= lambda_max(P)`; therefore this value does not understate the standard deviation along any unit spatial direction and equals Euclidean RMS one-sigma positional error implied by P.
No constant uncertainty is used.

## Field authority
CurrentTargetManager/HOROS supplies target identity continuity; HOROS supplies target XYZ/lifecycle/freshness/provenance and covariance/uncertainty contractually; HOROS local map is documented carrier-relative. Exact runtime frame string and exact local covariance layout/units remain future integration binding gates. gps_bridge/MAVLink exist but heading/altitude are not required for current frozen M2 TRACK and N1 emits both as None. Search vector remains None unless a separate explicit fresh same-target/same-frame VERIFIED search-geometry source is supplied.

## Fail closed
No M2 payload is emitted for malformed source type, malformed provenance, invalid freshness policy, malformed expected/source refs, frame mismatch/unsupported semantics, non-authoritative carrier-origin evidence, stale/future data, stale observation age, malformed or missing VERIFIED target XYZ, missing/malformed/wrong-semantics VERIFIED covariance, malformed search type/ref/frame/metric/timestamp/vector/provenance, or any input flagged production_authority=True.
NOT_VERIFIED remains NOT_VERIFIED and is never promoted.

## Compatibility behavior
With a valid VERIFIED software fixture using the real frozen artifacts:
M1 TRACK/MAINTAIN_TRACK -> M2 AVAILABLE/MAINTAIN_OBSERVATION (`verified_geometry_observation_guidance`).
That exact M2 output -> M3 SUPPRESSED/NO_COMMAND (`semantic_guidance_without_explicit_movement`) because N1 does not fabricate movement geometry.
HOLD -> M2 HOLD -> M3 HOLD.
ABORT -> M2 ABORT_HOLD -> M3 HOLD with abort_semantic=True.
High uncertainty (>5 m frozen M2 threshold) -> M2 DEGRADED/MAINTAIN_OBSERVATION.

## Validation
Core/compatibility suite: 31/31 PASS.
Additional strict boundary regression suite: 5/5 PASS.
TOTAL: 36/36 PASS.

## Review history
Cycle 1 candidate `b34abc9ddda315b0fc903424bb65e51d18d18f5a`: FAIL — provenance and freshness-policy boundary defects.
Cycle 1 repair `8bbcdb58fb7963147d73fe57f85a68361bcecc43`: FAIL on rereview — equality-spoof paths for covariance semantic tag and expected/search refs, plus whitespace refs.
Cycle 2 bounded repair: exact non-whitespace refs; exact covariance-semantics string type; adversarial equality-spoof tests added.

## Runtime availability boundary
Software contract is complete/testable. Future runtime integration must source-verify the exact current `horos_shadow_runtime.py`/HOROS state fields before asserting live VERIFIED NavigationEvidence: exact frame_ref semantics, exact 3x3 target covariance layout/units, CurrentTarget identity continuity at call point, and truthful metric status. Physical class-size metric accuracy remains NOT VERIFIED in current documentation.

CONTROL_AUTHORITY: NONE
PRODUCTION_INTEGRATION: NO
