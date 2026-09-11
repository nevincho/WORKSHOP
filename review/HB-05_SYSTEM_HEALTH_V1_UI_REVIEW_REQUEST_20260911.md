# HB-05 — Independent Review Request

Status: READY_FOR_REVIEW
Package: `handoffs/HB-05_SYSTEM_HEALTH_V1_UI_PACKAGE/`
Package tip commit: `a588ec56911257c5bf25a95081bfefbed683bca4`
Authority:
- HB-04 reviewed package commit `0a4bb367e29d9b361c5677cd2a1de3d4718f817d`
- accepted HB-02/HB-03 contracts
- Dashboard 2.1 architecture recovery for Settings shell / Diagnostics group and existing PC Dashboard state/polling surfaces

Review HB-05 only. Do not integrate, deploy, use Codex, modify Dashboard/Pi/runtime, add telemetry, health logic, thresholds, SOURCE_GAP fixes, history, recovery, or unrelated UI scope.

Verify independently:
1. UI consumes only normalized `TANGRA_SYSTEM_HEALTH_V1` output and does not reimplement HB-04 health derivation;
2. exactly 12 canonical HB-04 concepts are represented and rendered;
3. all six states render distinctly and verbatim: NOMINAL, DEGRADED, FAULT, STALE, UNAVAILABLE, NOT_VERIFIED;
4. reason codes and `not_verified` context are preserved without semantic rewriting;
5. diagnostic values are display-only and never change supplied health state;
6. false-green presentation is prevented, including invalid/missing contract handling;
7. WIDE cumulative `failures` remains diagnostic-only at the UI layer;
8. fixtures are normalized HB-04 simulation outputs, not a new telemetry contract;
9. standalone test suite passes; expected 14/14;
10. integration manifest reuses existing Dashboard Settings/state/poll path and introduces no direct Pi/EDGE polling or new endpoint;
11. no production Dashboard, Pi/runtime, authority, persistence, recovery, or Codex change exists;
12. package is integration-ready for later bounded Dashboard COPY integration.

Required reviewer output:
- RESULT: PASS/FAIL
- CONTRACT_CONSUMPTION: PASS/FAIL
- 12_CONCEPT_COVERAGE: PASS/FAIL
- STATE_RENDERING: PASS/FAIL
- FALSE_GREEN_PRESENTATION: PASS/FAIL
- TEST_EVIDENCE: <facts>
- INTEGRATION_READINESS: PASS/FAIL
- DEFECTS: NONE/<specific defects>
- REVIEW_COMMIT: <sha>
- STOP
