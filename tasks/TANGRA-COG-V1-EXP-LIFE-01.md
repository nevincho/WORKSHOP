# TANGRA-COG-V1-EXP-LIFE-01 — Reviewed COG-30 Lifecycle Baseline Integration

TASK_ID: TANGRA-COG-V1-EXP-LIFE-01
PROJECT: TANGRA
PRIORITY: HIGH
STATUS: REVIEW
OBJECTIVE: Attach the reviewed COG-30 ExperienceLifecyclePolicy to a restart-restored reviewed COG-22 ExperienceStore and qualify only baseline lifecycle semantics for persisted EXP-01 RAW_EVIDENCE records.
UPSTREAM_CHECKPOINTS:
- TANGRA-COG-V1-EXP-01: WORKSHOP_QUALIFIED
- TANGRA-COG-V1-EXP-PERSIST-01: WORKSHOP_QUALIFIED
- TAI-COG-22: REVIEWER PASS
- TAI-COG-30 Experience Lifecycle Artifact: REVIEWER PASS
CURRENT_STATE:
- Qualified base: nevincho/TANGRA-2.0:tangra-cog-v1-exp-persist-01@437211b0bfd69a387ed6c6d852168c4a9482c6ba
- Persisted RAW_EVIDENCE can be restored into reviewed COG-22.
- Reviewed COG-30 provides default ACTIVE lifecycle state, RETAIN for active records, exact semantic dedup, reviewed disposition/canonical gates.
- No reviewed RAW->CANDIDATE or CANDIDATE->VALIDATED policy exists.
AFFECTED_COMPONENTS:
- One thin lifecycle baseline integration adapter.
- Bounded integration qualification tests.
PROTECTED_COMPONENTS:
- COG-22 ExperienceStore and contracts.
- COG-30 lifecycle implementation.
- EXP-01 and EXP-PERSIST-01 adapters.
- COG-21.
- Pi/production/runtime/model layers.
EXECUTION_CLASS: WORKER
CODEX_ALLOWED: NO
ACCEPTANCE_CRITERIA:
1. Reviewed ExperienceLifecyclePolicy is instantiated unchanged beside a reviewed/restored ExperienceStore.
2. Persisted EXP-01 RAW_EVIDENCE resolves to LifecycleDisposition.ACTIVE.
3. retention_action() for that ACTIVE RAW_EVIDENCE is RETAIN.
4. exact semantic duplicate lookup operates against restored COG-22 ExperienceRecords.
5. COG-22 ExperienceRecord remains byte/JSON/semantic-hash unchanged before and after lifecycle inspection.
6. No RAW_EVIDENCE->CANDIDATE_LESSON transition is created or invoked.
7. No CANDIDATE_LESSON->VALIDATED_EXPERIENCE transition is created or invoked.
8. No canonical promotion is invoked.
9. No DispositionReview/CanonicalPromotionReview is fabricated.
10. COG-30 policy state is not persisted, imported, or reconstructed.
11. Adapter exposes no promotion/disposition/state-persistence/model/command surface.
12. AUTHORITY=NONE and operational_authority=[] remain invariant.
13. EXP-01 and EXP-PERSIST-01 regressions remain PASS.
14. Current reviewed COG-22 tests remain PASS.
15. Reviewed COG-30 lifecycle tests remain PASS.
VALIDATION_METHOD:
- Bounded GitHub Actions qualification.
- Execute upstream suites through EXP-PERSIST-01 + EXP-LIFE-01 + reviewed COG-22 + reviewed COG-30 lifecycle tests.
PRE_CHANGE_CHECKPOINT:
- nevincho/TANGRA-2.0:tangra-cog-v1-exp-persist-01@437211b0bfd69a387ed6c6d852168c4a9482c6ba
ROLLBACK_METHOD:
- Revert/remove EXP-LIFE-01 files to exact EXP-PERSIST-01 checkpoint.
EVIDENCE_PATHS:
- evidence/TANGRA-COG-V1-EXP-LIFE-01/WORKER.md
- review/TANGRA-COG-V1-EXP-LIFE-01.md
- checkpoints/TANGRA-COG-V1-EXP-LIFE-01.md

RAW_TO_CANDIDATE_POLICY: NOT_DEFINED / NOT_IMPLEMENTED
CANDIDATE_TO_VALIDATED_POLICY: NOT_DEFINED / NOT_IMPLEMENTED
COG30_POLICY_STATE_PERSISTENCE: NOT_STARTED
COG21: NOT_STARTED
CODEX: NOT_USED
PI_CHANGES: NONE
