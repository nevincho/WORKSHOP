# N1 Navigation Evidence — Final Evidence

TASK_ID: TASK-TANGRA-M2-NAVIGATION-EVIDENCE-N1-20260909
STATUS: COMPLETE / FROZEN
ARTIFACT_TYPE: CONTRACT / THIN ADAPTER / VALIDATION PACKAGE
FROZEN_REVIEWED_COMMIT: 81d734f6040b9ceb84adb365b5ea2d9152d78237
IMPLEMENTATION_BLOB: 74c7794e7edbaf4b2d80955dc6eec8e0b147bd0b
CORE_TEST_BLOB: e3ceab179d5b33ea81abb98a39cc02ebd74d8a94
BOUNDARY_TEST_BLOB: 9df512018e857cc42e3b884de6c4c80b3f36e2cc
INDEPENDENT_REVIEW: PASS
FREEZE_RECOMMENDATION: YES

Frozen M2 contract source: reviewed commit 75417cb4356a79e61d1196f3f859fa7cd7ba08e8, implementation blob 5616d5930c8ffca0cef7876d6c192bc7627efb2c.
Frozen M3 source: reviewed commit f041325369edea08888f8ee9ec5fd7ab9ce0e1ce, implementation blob 2c634c1f4698606a056e6bfab8cb7568c5f05466.

FRAME_CONTRACT: exact same non-whitespace M1/HOROS frame_ref; only CARRIER_RELATIVE_LOCAL_METRIC accepted; no coordinate conversion. carrier_xyz_m=(0,0,0) only as explicit carrier-relative frame-origin semantics, never from target XYZ.

UNCERTAINTY_RULE: VERIFIED non-LOST target state requires exact POSITION_COVARIANCE_3X3_M2 semantics and finite symmetric PSD 3x3 position covariance in m^2. `uncertainty_m=sqrt(trace(P_xyz))`. No arbitrary constants.

FIELD_POLICY: target identity/timestamp/frame/lifecycle/metric/observation age/target XYZ/covariance/provenance come from CurrentTarget/HOROS evidence. Heading and altitude are not required for current frozen M2 TRACK and remain None. Search vector is never synthesized and remains None without separate explicit VERIFIED search evidence.

FAIL_CLOSED: malformed source/provenance/policy/refs/enums/frame semantics/carrier-origin state/timestamps/observation age/target XYZ/covariance/search evidence and any production_authority=True input produce no M2 payload. Freshness cannot be looser than 0.5 s. NOT_VERIFIED is never promoted.

COMPATIBILITY: valid VERIFIED software fixture -> M1 TRACK/MAINTAIN_TRACK -> frozen M2 AVAILABLE/MAINTAIN_OBSERVATION. That exact M2 result -> frozen M3 SUPPRESSED/NO_COMMAND because no movement geometry is invented. HOLD and ABORT semantics preserved.

VALIDATION: 36/36 committed tests PASS. 11/11 additional review-only adversarial checks PASS.
REVIEW_CYCLES: 2 bounded FAIL/repair cycles, then PASS.
CONTROL_AUTHORITY: NONE.
PRODUCTION_INTEGRATION: NO.

FUTURE_RUNTIME_GATES: exact current HOROS frame_ref semantics, exact target position covariance layout/units, CurrentTarget identity continuity at call point, and truthful live metric_status must be source-bound before live VERIFIED use. Current documentation does not justify upgrading provisional/non-physically-validated range to VERIFIED.

BLOCKER: NONE for N1 COMPLETE/FROZEN package.
