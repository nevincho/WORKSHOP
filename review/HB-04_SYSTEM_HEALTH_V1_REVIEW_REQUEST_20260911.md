# HB-04 — Independent Review Request

Status: READY_FOR_REVIEW
Package: `handoffs/HB-04_SYSTEM_HEALTH_V1_ENGINE_PACKAGE/`
Package tip commit: `d0763c7722c25fce68480a61e53f2de7d7cd6677`
Authority:
- TANGRA-DOCS `REPORTS/HB-02_SYSTEM_HEALTH_V1_PC_DERIVATION_MODEL_20260910.md`
- TANGRA-DOCS `REPORTS/HB-03_SYSTEM_HEALTH_V1_PC_DATA_CONTRACT_20260910.md`
- HB-03 base `8038bf770e09aa2330447d5baca33a515c2a215c`

Review only this package. Do not implement, integrate, deploy, use Codex, modify Dashboard/Pi/runtime, add telemetry, thresholds, SOURCE_GAP fixes, UI, history, recovery, or Performance Observatory scope.

Verify independently:
1. exactly 12 canonical health concepts and no extra top-level components;
2. HB-02/HB-03 state/reason-code semantics;
3. merged/DEMOTE fields are supporting context only;
4. SOURCE_GAP is not synthesized;
5. no invented numeric thresholds; WIDE uses only source-provided `max_age_s`;
6. STALE/UNAVAILABLE/NOT_VERIFIED false-green protection;
7. fixtures are reduced captured HB-00 evidence, not a new telemetry contract;
8. tests cover all 12 concepts plus missing/stale/false-green cases;
9. integration manifest reuses existing `dashboard.py` merged telemetry and `pi_runtime_control.py` status surface without new Pi polling/protocol;
10. protected authorities remain untouched;
11. package is independently testable and integration-ready for later Dashboard COPY integration.

Required reviewer output:
- RESULT: PASS/FAIL
- CONTRACT_FIDELITY: PASS/FAIL
- TEST_EVIDENCE: <facts>
- BOUNDARY_EVIDENCE: <facts>
- DEFECTS: NONE/<specific defects>
- REVIEW_COMMIT: <sha>
- STOP
