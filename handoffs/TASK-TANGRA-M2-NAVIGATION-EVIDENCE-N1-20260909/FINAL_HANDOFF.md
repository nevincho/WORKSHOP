# N1 Final Handoff

RESULT=PASS
TASK_ID=TASK-TANGRA-M2-NAVIGATION-EVIDENCE-N1-20260909
STATUS=COMPLETE / FROZEN
ARTIFACT_TYPE=CONTRACT / THIN ADAPTER / VALIDATION PACKAGE
FINAL_COMMIT=81d734f6040b9ceb84adb365b5ea2d9152d78237
IMPLEMENTATION_BLOB=74c7794e7edbaf4b2d80955dc6eec8e0b147bd0b

INPUT_AUTHORITIES=CurrentTargetManager/HOROS target identity continuity; HOROS target spatial state for timestamp/frame/lifecycle/metric status/observation age/target XYZ/covariance/provenance; optional ExplicitSearchGeometry only when separately authoritative and VERIFIED. M1 expected target_ref/frame_ref are matching constraints, not new geometry sources.

NAVIGATION_FIELDS=target_ref,timestamp,frame_ref,lifecycle,metric_status,observation_age_s,uncertainty_m,target_xyz_m,carrier_xyz_m,carrier_heading_deg=None,carrier_altitude_m=None,search_relative_vector_m=None unless explicit search evidence,provenance.

FRAME_CONTRACT=Exact same non-whitespace frame_ref as M1; accepted semantics only CARRIER_RELATIVE_LOCAL_METRIC; no ENU/NED/body/camera/world conversion. carrier_xyz_m=(0,0,0) only when carrier-relative frame origin is explicitly asserted by source contract. Target XYZ is never reused as carrier XYZ.

UNCERTAINTY_RULE=For VERIFIED non-LOST geometry require exact POSITION_COVARIANCE_3X3_M2 semantics and finite symmetric PSD 3x3 position covariance in m^2; uncertainty_m=sqrt(trace(P_xyz)). Missing/invalid/wrong-semantics covariance blocks VERIFIED active evidence.

FAIL_CLOSED_RULES=Reject malformed source/provenance/policy/refs/enums/frame semantics/carrier-origin evidence/timestamps/observation age/target XYZ/covariance/search evidence and any production_authority=True input. Freshness policy cannot exceed frozen M2 0.5 s. NOT_VERIFIED is preserved and never upgraded. No search vector is synthesized.

M2_COMPATIBILITY=PASS — real frozen M2: M1 TRACK/MAINTAIN_TRACK + valid VERIFIED N1 evidence -> AVAILABLE / MAINTAIN_OBSERVATION / verified_geometry_observation_guidance. High uncertainty or NOT_VERIFIED remains DEGRADED. HOLD/ABORT unchanged.

M3_COMPATIBILITY=PASS — exact active M2 MAINTAIN_OBSERVATION without explicit movement geometry -> SUPPRESSED / NO_COMMAND / semantic_guidance_without_explicit_movement. HOLD -> HOLD. ABORT_HOLD -> HOLD with abort_semantic=True.

ACTIVE_TRACK_RESULT=SOFTWARE_TESTABLE: YES. Valid trustworthy N1 fixture makes frozen M2 active/AVAILABLE passive observation guidance without inventing movement geometry. Frozen M3 remains NO_COMMAND because no explicit movement vector is invented. LIVE VERIFIED TRACK remains conditional on future runtime source binding and truthful metric status.

TEST_RESULT=36/36 PASS committed (31 core/compatibility + 5 boundary regression)
ADVERSARIAL_TEST_RESULT=11/11 PASS review-only after two bounded repair cycles
CONTROL_AUTHORITY=NONE
PRODUCTION_INTEGRATION=NO
FREEZE_STATUS=COMPLETE / FROZEN; independent review PASS; FREEZE_RECOMMENDATION=YES

FUTURE_CODEX_INTEGRATION_UNIT=One narrow mission_shadow_runtime.py wiring unit: bind exact current HOROS/CurrentTarget source fields -> HorosTargetNavigationSource -> build_m2_navigation_evidence() -> construct frozen M2 NavigationEvidence with explicit enum conversion -> pass as GuidanceInput.navigation. No frozen MC1/M1/M2/M3 semantic changes.

BLOCKER=NONE for N1 package. Future live integration gates: verify exact current HOROS frame_ref as carrier-relative metric frame, exact target position covariance layout/units as 3x3 m^2, CurrentTarget identity continuity at call point, and truthful live metric_status; current documentation does not justify promoting provisional/non-physically-validated range to VERIFIED.
