# TANGRA-COG-V1-HYP-01 — Reviewed COG-19 Hypothesis Connection

TASK_ID: TANGRA-COG-V1-HYP-01
PROJECT: TANGRA
PRIORITY: HIGH
STATUS: COMPLETE — WORKSHOP_QUALIFIED / REVIEWER_PASS
OBJECTIVE: Connect WORKSHOP_QUALIFIED DIAG-01 COG-16 outputs and CORR-01 COG-18 correlation results into the existing reviewed COG-19 deterministic hypothesis layer through the smallest repository-side adapter.
SOURCE_PLAN_OR_REQUEST: Vlad Control Room authorization, 2026-09-26; COG-19 NEXT_DEPENDENCY only.
UPSTREAM_CHECKPOINTS:
- TANGRA-COG-V1-DIAG-01 WORKSHOP_QUALIFIED.
- TANGRA-COG-V1-CORR-01 WORKSHOP_QUALIFIED.
CURRENT_STATE:
- Qualified CORR-01 head: nevincho/TANGRA-2.0:tangra-cog-v1-corr-01@e5cf7a7e3f28eef1c97442c723d6a547dd1895ea.
- TAI-COG-19 is already PASS / REVIEWED at historical reviewed checkpoint dfc786da7cc07bbb11cba6bdb3d23f7de064ee47.
PREREQUISITES:
- Reuse qualified DIAG-01 and CORR-01 contracts unchanged.
- Reuse reviewed COG-19 HypothesisInput/DiagnosticHypothesisRequest/DiagnosticHypothesisEngine unchanged.
DEPENDENCIES:
- TANGRA-COG-V1-DIAG-01.
- TANGRA-COG-V1-CORR-01.
- TAI-COG-19 reviewed implementation.
AFFECTED_COMPONENTS:
- New thin COG-19 integration adapter only.
- New bounded integration qualification tests only.
PROTECTED_COMPONENTS:
- Cognitive Bridge.
- DIAG-01 adapter.
- CORR-01 adapter.
- COG-15/16/17/18/19 and all later reviewed Cognitive units.
- production TANGRA, Raspberry Pi and operational/command paths.
EXECUTION_CLASS: WORKER
CODEX_ALLOWED: NO
ACCEPTANCE_CRITERIA:
1. Reviewed COG-19 is reused, not duplicated.
2. Qualified COG-16 DiagnosticExecutionResult values with DiagnosticResult payloads map through reviewed HypothesisInput.from_execution.
3. Qualified COG-18 DiagnosticCorrelationResult records are reused directly after validation; no causal reinterpretation is added.
4. Diagnostic domain/result identity is explicit and deterministic.
5. Genuine reviewed COG-19 engine executes from DIAG-01 + CORR-01 outputs.
6. Evidence refs and supporting correlation refs remain traceable in hypotheses.
7. Every produced claim remains ClaimClass.HYPOTHESIS, verified_cause=NONE, authority=NONE, operational_authority=[].
8. HIGH confidence remains hypothesis/confidence, never proof or cause.
9. COG-16 outputs without DiagnosticResult are rejected deterministically.
10. Invalid/causal/duplicate correlation input is rejected by existing reviewed contracts.
11. UNKNOWN/NOT_TESTED inputs do not become degradation facts.
12. MISSION_CONSTRAINED remains unsupported.
13. Suggested next diagnostic is recommendation-only; execution_performed=False.
14. Engine exceptions are isolated without operational mutation.
15. No LLM/model invocation is required.
16. Bridge, DIAG-01 and CORR-01 tests remain PASS.
17. Current reviewed COG-19 source tests remain PASS.
VALIDATION_METHOD:
- Bounded authoritative GitHub Actions run.
- Execute Bridge, DIAG-01, CORR-01, new HYP-01 integration tests and current reviewed COG-19 source tests.
PRE_CHANGE_CHECKPOINT:
- nevincho/TANGRA-2.0:tangra-cog-v1-corr-01@e5cf7a7e3f28eef1c97442c723d6a547dd1895ea
ROLLBACK_METHOD:
- Revert/remove HYP-01 files to exact CORR-01 checkpoint.
EVIDENCE_PATHS:
- evidence/TANGRA-COG-V1-HYP-01/WORKER.md
- review/TANGRA-COG-V1-HYP-01.md
- checkpoints/TANGRA-COG-V1-HYP-01.md

CODEX: NOT USED
PI_CHANGES: NONE

RESULT:
- WORKSHOP_QUALIFIED
- REVIEWER_PASS
- CHECKPOINT: checkpoints/TANGRA-COG-V1-HYP-01.md
- TARGET_HEAD: nevincho/TANGRA-2.0:tangra-cog-v1-hyp-01@6247f1b6e42131319dd5e3d3094d12b99974c97e
- TESTS: 78 PASS / 0 FAIL on bounded qualification surface
- HISTORICAL_317_REGRESSION: NOT EXECUTED
- COG-20: NOT STARTED
- CODEX: NOT USED
- PI_CHANGES: NONE
