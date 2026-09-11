# HB-04 — Independent Review Request

Status: READY_FOR_RE-REVIEW AFTER BOUNDED CORRECTION
Package: `handoffs/HB-04_SYSTEM_HEALTH_V1_ENGINE_PACKAGE/`
Package tip commit: `0a4bb367e29d9b361c5677cd2a1de3d4718f817d`
Prior failed review commit: `a67058eb8eacefdcd16e7fb6cd16703cf38b9e20`
Authority:
- TANGRA-DOCS `REPORTS/HB-02_SYSTEM_HEALTH_V1_PC_DERIVATION_MODEL_20260910.md`
- TANGRA-DOCS `REPORTS/HB-03_SYSTEM_HEALTH_V1_PC_DATA_CONTRACT_20260910.md`
- HB-03 base `8038bf770e09aa2330447d5baca33a515c2a215c`

Review only this corrected HB-04 package. Do not implement, integrate, deploy, use Codex, modify Dashboard/Pi/runtime, add telemetry, thresholds, SOURCE_GAP fixes, UI, history, recovery, or Performance Observatory scope.

Bounded correction under review:
- cumulative `wide_worker.failures > 0` no longer independently triggers current `FAULT`;
- cumulative `failures` remains diagnostic context in WIDE values;
- regression fixture semantics: `running=true`, `last_fresh=true`, `last_age_s=0.1`, `max_age_s=0.5`, no current errors, `failures=1` MUST NOT become `FAULT` solely because `failures=1`.

Verify independently:
1. exactly 12 canonical health concepts and no extra top-level components;
2. HB-02/HB-03 state/reason-code semantics;
3. corrected WIDE cumulative-counter semantics;
4. merged/DEMOTE fields are supporting context only;
5. SOURCE_GAP is not synthesized;
6. no invented numeric thresholds; WIDE uses only source-provided `max_age_s`;
7. STALE/UNAVAILABLE/NOT_VERIFIED false-green protection;
8. fixtures are reduced captured HB-00 evidence, not a new telemetry contract;
9. all original tests plus exact WIDE regression pass; expected minimum 16/16;
10. integration manifest reuses existing `dashboard.py` merged telemetry and `pi_runtime_control.py` status surface without new Pi polling/protocol;
11. protected authorities remain untouched;
12. package is independently testable and integration-ready for later Dashboard COPY integration.

Required reviewer output:
- RESULT: PASS/FAIL
- CONTRACT_FIDELITY: PASS/FAIL
- TEST_EVIDENCE: <facts>
- BOUNDARY_EVIDENCE: <facts>
- DEFECTS: NONE/<specific defects>
- REVIEW_COMMIT: <sha>
- STOP
