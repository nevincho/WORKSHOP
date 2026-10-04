# TANGRA-COG-V1-C13 — WORKER EVIDENCE

DATE: 2026-10-04
TASK: C13 Bulgarian Cognitive quality qualification
RESULT: QUALIFICATION_INCOMPLETE / FAIL
FAILURE_CLASS: TEST_HARNESS_DEFECT
AUTHORITY: NONE
OPERATIONAL_AUTHORITY: []
MISSION_RUNTIME_CHANGES: NONE
PI_CHANGES: NONE
MODEL_CONFIG_CHANGES: NONE

BASE:
nevincho/TANGRA-2.0:tangra-cog-v1-obs-rec-04@be1996f32f3dcc93b6665d4aaf58f3c95ecf96da

QUALITY_BRANCH:
tangra-cog-v1-c13-bulgarian-quality@db4caf931c6f4947d5eaef8665c3bb7234caf973

FINAL_DELTA:
- TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/quality/c13_bulgarian_quality_cases.json
  blob 1ecda59f143bce008ab3a7d18eee7575f538225b
- TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/quality/c13_quality_harness.py
  blob 9092eaf6a038419c991d50fa7be24be2ea2351a1
- TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/quality/test_c13_quality_harness.py
  blob edb32a638c1d741de7b713e1300e11eccc48105b

TEST_SET:
- 24 controlled Bulgarian cases
- 12 required test surfaces
- complete/partial/missing/contradictory evidence
- healthy/anomaly cases
- ambiguous operator wording
- overconfidence and causal-certainty traps
- capability/authority challenges
- MISSION_ACTIVE deferral
- mixed Bulgarian/English terminology

HARNESS:
- deterministic checks for required factual boundaries, uncertainty, forbidden claims, terminology and authority
- human review required for factual correctness, grounding, uncertainty, terminology, Bulgarian fluency, technical precision, subsystem-name preservation, epistemic/state distinction, authority, concision and readability
- closed failure-class taxonomy enforced
- STUB/SIMULATED model identity rejected
- all 24 live results required
- current/unmodified configuration identity required
- per-case latency required
- aggregate requested metrics supported

HARNESS QUALIFICATION HISTORY:
- run 37213416764: TEST_HARNESS_DEFECT, dynamic import/dataclass collection defect
- run 37213458627: TEST_HARNESS_DEFECT, English-heavy positive control did not meet Bulgarian threshold
- run 37213498807: TEST_HARNESS_DEFECT, positive-control uncertainty phrase mismatch
- run 37213530726: TEST_HARNESS_DEFECT, positive-control fact-boundary exact-match mismatch
- authoritative run 37213664396: SUCCESS
  - py_compile PASS
  - harness tests 7/7 PASS

LIVE MODEL EXECUTION:
- NOT EXECUTED
- current production Cognitive model/configuration could not be reached from the available execution environment
- no SSH/remote production-host connector was available in the task environment
- no synthetic/stub response is accepted as substitute
- no claim about current LFM2.5 Bulgarian quality is made

METRICS:
- controlled cases defined: 24
- live current-model cases executed: 0
- grounding/factual/hallucination/uncertainty/terminology/readability/latency metrics: NOT MEASURED

DOCUMENTATION:
- TANGRA-DOCS/COGNITIVE_C13_BULGARIAN_QUALITY_20261004.md
- TODO.md updated: C13 OPEN / NOT_QUALIFIED
- ROADMAP.md updated: live C13 execution remains next
- COGNITIVE_V1_EXECUTION_PLAN.md updated: C13-LIVE-BG-01 required

FINAL_RESULT:
C13=FAIL / LIVE_CURRENT_MODEL_QUALIFICATION_NOT_EXECUTED / HARNESS_READY
