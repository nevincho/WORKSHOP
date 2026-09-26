# TANGRA-COG-V1-CORR-01 — Reviewed COG-18 Correlation Connection

TASK_ID: TANGRA-COG-V1-CORR-01
PROJECT: TANGRA
PRIORITY: HIGH
STATUS: REVIEW
OBJECTIVE: Connect qualified DIAG-01 COG-16 DiagnosticExecutionResult outputs to the existing reviewed COG-18 deterministic correlation layer through the smallest repository-side adapter.
SOURCE_PLAN_OR_REQUEST: Vlad Control Room authorization, 2026-09-26; NEXT_DEPENDENCY after TANGRA-COG-V1-DIAG-01.
CURRENT_STATE:
- DIAG-01 WORKSHOP_QUALIFIED at nevincho/TANGRA-2.0:tangra-cog-v1-diag-01@a7df01456ef27e08caf5090cf34818e837e248ca.
- TAI-COG-18 already PASS / REVIEWED; do not reimplement it.
PREREQUISITES:
- Reuse qualified DIAG-01 output contract unchanged.
- Reuse reviewed COG-18 DiagnosticCorrelationInput/Request/Engine unchanged.
DEPENDENCIES:
- TANGRA-COG-V1-DIAG-01.
- TAI-COG-18 reviewed checkpoint.
AFFECTED_COMPONENTS:
- New thin correlation integration adapter only.
- New bounded integration qualification tests only.
PROTECTED_COMPONENTS:
- cognitive_bridge.py.
- cognitive_diagnostic_adapter.py semantics.
- COG-15, COG-16, COG-17, COG-18, COG-19 and later cognitive units.
- production TANGRA, Raspberry Pi and all operational/command paths.
EXECUTION_CLASS: WORKER
CODEX_ALLOWED: NO
ACCEPTANCE_CRITERIA:
1. Existing reviewed COG-18 is reused, not duplicated.
2. Qualified DIAG-01 DiagnosticExecutionResult outputs with DiagnosticResult payloads convert into COG-18 DiagnosticCorrelationInput.
3. Domain, explicit timestamp, explicit sequence_id and source_ref are supplied without inference.
4. COG-16 result provenance/evidence remains traceable through COG-18 input/result.
5. Genuine COG-18 engine executes deterministic supported correlations.
6. Results retain causal_claim=NONE, authority=NONE, operational_authority=[].
7. Non-result COG-16 statuses that carry no DiagnosticResult are rejected deterministically and do not become facts.
8. Duplicate/malformed bindings are rejected deterministically.
9. UNKNOWN / NOT_TESTED inputs do not self-promote to causal or state conclusions.
10. MISSION_CONSTRAINED remains unsupported for COG-18 correlation.
11. Correlation-engine failures are isolated; no operational state mutation occurs.
12. No model invocation is required.
13. Existing DIAG-01 tests remain PASS.
14. Existing reviewed COG-18 source tests remain PASS.
15. Existing Bridge qualification remains PASS.
VALIDATION_METHOD:
- Execute bounded GitHub Actions qualification on authoritative branch content.
- Run Bridge tests, DIAG-01 tests, new CORR-01 tests and original reviewed COG-18 source tests.
PRE_CHANGE_CHECKPOINT:
- nevincho/TANGRA-2.0:tangra-cog-v1-diag-01@a7df01456ef27e08caf5090cf34818e837e248ca
ROLLBACK_METHOD:
- Revert/remove CORR-01 added files to exact DIAG-01 checkpoint.
EVIDENCE_PATHS:
- evidence/TANGRA-COG-V1-CORR-01/WORKER.md
- review/TANGRA-COG-V1-CORR-01.md
- checkpoints/TANGRA-COG-V1-CORR-01.md

CODEX: NOT USED
PI_CHANGES: NONE
