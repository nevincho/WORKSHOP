# TANGRA-COG-V1-INT-01 — Reviewed COG-20 Input Composition Connection

TASK_ID: TANGRA-COG-V1-INT-01
PROJECT: TANGRA
PRIORITY: HIGH
STATUS: IN_PROGRESS
OBJECTIVE: Compose an existing validated COG-02 EvidencePacket plus WORKSHOP_QUALIFIED DIAG-01, CORR-01 and HYP-01 outputs into the existing reviewed COG-20 CognitiveDiagnosticInterpretationRequest and execute the existing reviewed CognitiveDiagnosticInterpreter through an injected reviewed backend contract.
UPSTREAM_CHECKPOINTS:
- TANGRA-COG-V1-DIAG-01: WORKSHOP_QUALIFIED
- TANGRA-COG-V1-CORR-01: WORKSHOP_QUALIFIED
- TANGRA-COG-V1-HYP-01: WORKSHOP_QUALIFIED
- TAI-COG-20: REVIEWER PASS
CURRENT_STATE:
- Qualified HYP-01 base: nevincho/TANGRA-2.0:tangra-cog-v1-hyp-01@6247f1b6e42131319dd5e3d3094d12b99974c97e
- COG-20 implementation already exists and must not be rewritten.
- Real async LFM2.5/COG-20 execution has separate prior Pi evidence; this task does not revalidate model quality or Pi wiring.
PREREQUISITES:
- A genuine validated EvidencePacket must be supplied; it must not be reconstructed from diagnostic evidence refs.
- Reuse reviewed COG-20 request/interpreter and COG-06 backend interfaces unchanged.
DEPENDENCIES:
- DIAG-01
- CORR-01
- HYP-01
- COG-02 EvidencePacket
- reviewed COG-20
AFFECTED_COMPONENTS:
- One thin COG-20 composition adapter.
- Bounded integration qualification tests.
PROTECTED_COMPONENTS:
- Cognitive Bridge.
- DIAG-01, CORR-01, HYP-01 adapters.
- COG-02, COG-06, COG-16, COG-18, COG-19, COG-20.
- real LFM2.5 adapter/runtime.
- production TANGRA / Raspberry Pi / operational stack.
EXECUTION_CLASS: WORKER
CODEX_ALLOWED: NO
ACCEPTANCE_CRITERIA:
1. Existing reviewed COG-20 is reused, not duplicated.
2. Adapter requires a valid existing EvidencePacket.
3. Qualified COG-16 execution results containing DiagnosticResult map unchanged into COG-20 diagnostic_results.
4. Qualified COG-18 correlation records map unchanged from DiagnosticCorrelationResult.
5. Qualified COG-19 hypotheses map unchanged from DiagnosticHypothesisResult.
6. Invalid/non-result upstream values are rejected deterministically.
7. Request serialization is deterministic.
8. Evidence refs, correlation refs and hypothesis refs remain traceable.
9. Genuine reviewed COG-20 interpreter executes with StubBackend/deterministic fixture backend.
10. HIGH hypothesis confidence cannot be promoted to FACT/VERIFIED_CAUSE.
11. Backend unsupported epistemic promotion remains REJECTED by reviewed COG-20.
12. MISSION_CONSTRAINED remains unsupported.
13. Backend failure remains isolated.
14. AUTHORITY=NONE and operational_authority=[] remain invariant.
15. No model invocation is required.
16. Bridge, DIAG-01, CORR-01 and HYP-01 tests remain PASS.
17. Current reviewed COG-20 source tests remain PASS.
VALIDATION_METHOD:
- Bounded authoritative GitHub Actions execution against branch content.
- Execute upstream qualification suites + INT-01 + reviewed COG-20 tests.
PRE_CHANGE_CHECKPOINT:
- nevincho/TANGRA-2.0:tangra-cog-v1-hyp-01@6247f1b6e42131319dd5e3d3094d12b99974c97e
ROLLBACK_METHOD:
- Revert/remove INT-01 files to exact HYP-01 checkpoint.
EVIDENCE_PATHS:
- evidence/TANGRA-COG-V1-INT-01/WORKER.md
- review/TANGRA-COG-V1-INT-01.md
- checkpoints/TANGRA-COG-V1-INT-01.md

COG-21: NOT STARTED
CODEX: NOT USED
PI_CHANGES: NONE
