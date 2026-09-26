# TANGRA-COG-V1-EXP-01 — Reviewed COG-22 RAW Experience Creation Connection

TASK_ID: TANGRA-COG-V1-EXP-01
PROJECT: TANGRA
PRIORITY: HIGH
STATUS: REVIEW
OBJECTIVE: Create and store one reviewed COG-22 RAW_EVIDENCE ExperienceRecord from the WORKSHOP_QUALIFIED Cognitive V1 upstream chain through INT-01, using only preserved upstream references and explicit caller context.
UPSTREAM_CHECKPOINTS:
- TANGRA-COG-V1-DIAG-01: WORKSHOP_QUALIFIED
- TANGRA-COG-V1-CORR-01: WORKSHOP_QUALIFIED
- TANGRA-COG-V1-HYP-01: WORKSHOP_QUALIFIED
- TANGRA-COG-V1-INT-01: WORKSHOP_QUALIFIED
- TAI-COG-22: REVIEWER PASS
CURRENT_STATE:
- Qualified INT-01 base: nevincho/TANGRA-2.0:tangra-cog-v1-int-01@e669eb7a70057b054c40dc153146b4034543592e
- COG-22 implementation already exists and must not be rewritten.
- COG-21 signals are optional/deferred for this minimum Experience path.
PREREQUISITES:
- Use a genuine validated COG-02 EvidencePacket.
- Use qualified COG-16 DiagnosticExecutionResult values, COG-18 DiagnosticCorrelationResult, COG-19 DiagnosticHypothesisResult, and reviewed COG-20 CognitiveDiagnosticInterpretationResult.
- Do not invent state transition or outcome semantics.
DEPENDENCIES:
- DIAG-01
- CORR-01
- HYP-01
- INT-01
- reviewed COG-22
AFFECTED_COMPONENTS:
- One thin RAW Experience composition/store adapter.
- Bounded integration qualification tests.
PROTECTED_COMPONENTS:
- Cognitive Bridge.
- DIAG-01, CORR-01, HYP-01, INT-01 adapters.
- COG-02, COG-06, COG-16, COG-18, COG-19, COG-20, COG-22.
- COG-21.
- COG-30 and all durable persistence/lifecycle components.
- production TANGRA / Raspberry Pi / operational stack.
EXECUTION_CLASS: WORKER
CODEX_ALLOWED: NO
ACCEPTANCE_CRITERIA:
1. Existing reviewed COG-22 ExperienceRecord/ExperienceStore are reused, not duplicated.
2. Adapter requires a valid existing EvidencePacket.
3. RAW_EVIDENCE is the only lifecycle created.
4. Evidence refs come from the EvidencePacket and qualified upstream result bindings; no synthetic evidence ref is invented.
5. Diagnostic refs identify supplied qualified COG-16 execution results.
6. Correlation refs identify supplied qualified COG-18 correlation records.
7. Hypothesis refs identify supplied qualified COG-19 hypotheses.
8. Interpretation ref identifies the supplied reviewed COG-20 result when COMPLETED.
9. signal_refs remain empty; COG-21 is not required.
10. state_before/change/state_after remain unasserted unless explicitly supplied; default is None.
11. outcome defaults to UNKNOWN and no result is promoted to lesson/validated/canonical.
12. mission/runtime/subsystem context refs are explicit caller inputs only, never inferred.
13. ExperienceRecord serialization/semantic hash is deterministic for identical inputs.
14. Existing reviewed ExperienceStore.append stores POST_MISSION_FULL/OFFLINE_ENGINEERING RAW record.
15. Duplicate semantic record is handled by existing COG-22 deterministic dedup semantics.
16. MISSION_CONSTRAINED remains unsupported.
17. AUTHORITY=NONE and operational_authority=[] remain invariant.
18. No filesystem/network/database/model/persistence/lifecycle/COG-30 surface is added.
19. All upstream qualification suites through INT-01 remain PASS.
20. Current reviewed COG-22 source tests remain PASS.
VALIDATION_METHOD:
- Bounded authoritative GitHub Actions execution.
- Execute Bridge, DIAG-01, CORR-01, HYP-01, INT-01, EXP-01 and reviewed COG-22 source tests.
PRE_CHANGE_CHECKPOINT:
- nevincho/TANGRA-2.0:tangra-cog-v1-int-01@e669eb7a70057b054c40dc153146b4034543592e
ROLLBACK_METHOD:
- Revert/remove EXP-01 files to exact INT-01 checkpoint.
EVIDENCE_PATHS:
- evidence/TANGRA-COG-V1-EXP-01/WORKER.md
- review/TANGRA-COG-V1-EXP-01.md
- checkpoints/TANGRA-COG-V1-EXP-01.md

COG-21: NOT STARTED
COG-30: NOT STARTED
DURABLE_PERSISTENCE: NOT STARTED
CODEX: NOT USED
PI_CHANGES: NONE
