# TANGRA-COG-V1-DIAG-01 — Reviewed COG-16 Deterministic Diagnostics Connection

TASK_ID: TANGRA-COG-V1-DIAG-01
PROJECT: TANGRA
PRIORITY: HIGH
STATUS: IN_PROGRESS
OBJECTIVE: Create and independently qualify the smallest repository-side integration adapter that converts structured Cognitive Bridge/post-mission evidence into the existing reviewed COG-16 DiagnosticExecutionRequest contract and executes the existing reviewed COG-15/16 deterministic diagnostic path.
SOURCE_PLAN_OR_REQUEST: Vlad Control Room authorization, 2026-09-26; bounded task accepted from repository reconciliation.
CURRENT_STATE:
- Frozen reviewed Cognitive baseline: nevincho/TANGRA-2.0:tai-cog-32-package@9629a624358b8ae539ac1af54af72b9828ba5632.
- Qualified Bridge baseline: nevincho/TANGRA-2.0:cognitive-bridge-integration@bd11d92f396b68de00a0f3636ae49ed8310ce420.
- COG-15/16 implementations exist and must be reused.
- Historical Bridge cumulative 317-test regression remains NOT EXECUTED.
PREREQUISITES:
- Reuse reviewed COG-15 registry and COG-16 executor unchanged.
- Preserve Bridge authority/lifecycle/fail-open contracts.
DEPENDENCIES:
- COG-00 StateEvent contract.
- Qualified Cognitive Bridge.
- Reviewed COG-04/15/16 contracts.
AFFECTED_COMPONENTS:
- New thin integration adapter only.
- New bounded adapter qualification tests only.
PROTECTED_COMPONENTS:
- cognitive_bridge.py semantics.
- COG-15, COG-16, COG-18, COG-19, COG-20, COG-21, COG-22, COG-26, COG-27, COG-30.
- production TANGRA, Raspberry Pi, Hailo, NanoTracker, CA Kalman, CurrentTarget, range, HOROS, command/control/IFF/readiness/LoRa.
EXECUTION_CLASS: WORKER
CODEX_ALLOWED: NO
ACCEPTANCE_CRITERIA:
1. Reviewed COG-16 is reused, not duplicated.
2. Valid structured StateEvent evidence is deterministically projected into valid DiagnosticEvidenceBundle/DiagnosticExecutionRequest.
3. Evidence refs and source/provenance metadata survive the adapter boundary.
4. Registered deterministic diagnostic executes through genuine COG-15/16.
5. Result remains reviewed DiagnosticExecutionResult/DiagnosticResult.
6. Missing tool/dependency/evidence use existing bounded statuses.
7. Malformed/duplicate evidence is rejected deterministically.
8. NO_CONCLUSION/UNKNOWN semantics are preserved.
9. Failures do not mutate or escape into operational state.
10. MISSION_CONSTRAINED cannot execute reviewed heavy post-mission diagnostics.
11. No model invocation is required.
12. Existing Bridge qualification remains PASS.
13. Existing COG-16 tests remain PASS.
14. No mutation/command/authority surface is added.
15. AUTHORITY=NONE and operational_authority=[] remain invariant.
VALIDATION_METHOD:
- Exact-content repository mirror in isolated Python execution environment.
- Run new adapter tests, reviewed COG-16 tests, and existing 17-test Bridge qualification.
- Verify executed source identities against authoritative repository blobs/commit after execution.
PRE_CHANGE_CHECKPOINT:
- nevincho/TANGRA-2.0:cognitive-bridge-integration@bd11d92f396b68de00a0f3636ae49ed8310ce420
ROLLBACK_METHOD:
- Delete/revert task-created adapter/test delta to the pre-change commit; reviewed components are not modified.
EVIDENCE_PATHS:
- evidence/TANGRA-COG-V1-DIAG-01/WORKER.md
- review/TANGRA-COG-V1-DIAG-01.md
- checkpoints/TANGRA-COG-V1-DIAG-01.md

CODEX: NOT USED
PI_CHANGES: NONE
