# N1 Independent Review — Cycle 2

TASK_ID: TASK-TANGRA-M2-NAVIGATION-EVIDENCE-N1-20260909
REVIEWED_COMMIT: 8bbcdb58fb7963147d73fe57f85a68361bcecc43
RESULT: FAIL
FREEZE_RECOMMENDATION: NO

Cycle 1 findings are repaired: malformed provenance fails closed and freshness policy cannot be NaN, negative or looser than frozen M2's 0.5 s threshold.

New adversarial findings:
1. `covariance_semantics` is compared by equality without exact type validation. A directly constructed field object with custom equality can spoof the required semantic tag and allow covariance to be accepted.
2. `expected_target_ref` and `expected_frame_ref` are not exact-type validated before equality comparison. Malformed objects with custom equality can satisfy source-ref comparison at the public adapter boundary.
3. `ExplicitSearchGeometry.target_ref/frame_ref` are compared before exact string validation, allowing the same malformed-equality path and possible exception propagation.
4. Whitespace-only refs are not rejected explicitly when both sides match.

Required bounded repair:
- exact non-empty string validation for expected/source/search refs;
- exact string type for covariance semantics before matching `POSITION_COVARIANCE_3X3_M2`;
- add adversarial tests for equality-spoof objects and whitespace refs.

No redesign required. No frozen M1/M2/M3 changes.
BLOCKER: bounded implementation defect only.
