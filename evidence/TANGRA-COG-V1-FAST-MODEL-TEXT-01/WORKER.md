# TANGRA-COG-V1-FAST-MODEL-TEXT-01 — Worker Evidence
DATE: 2026-09-26
STATE: IMPLEMENTED / QUALIFICATION_PASS / REVIEW_REQUIRED

TARGET: nevincho/TANGRA-2.0:tangra-cog-v1-fast-model-text-01@e43e0bd24f276ec9a3acb725e0888853e0eb8762
BASE: tangra-cog-v1-fast-text-01@aec6a3d85cad8330f6c1bc09127d7c5e61378aed

FINAL_DELTA:
- integration/cognitive_fast_model_text_response.py
  blob 92474d02ebd138cd3bccb9f3c9011411ba26af01
- tests/integration/test_cognitive_fast_model_text_response.py
  blob 8b93a832f22aad8b6eaca10e1781e48bc1379602

PROTECTED_UNCHANGED:
- FAST-TEXT-01 597fb3bd439432d660b59822f3bd6579033d6a94
- COG-06 backend 1be7d65daaa4a7a415da4dd30b135b54e1c64908
- COG-28 real-backend adapter 9200bbba8d3c89f4ffc116b2a8a33e5210aca26d
- COG-07 349b7e845139577a0ec9837ae58ce8b1742fd928
- COG-26 8a0bac04d8092593ec5683e2aa71540b941d6a5b
- POSTMISSION-EXP-01 d0e131114532a8219a211b3257afccc211749764
- qualification workflow restored 9d28f0fd44886b7901f061258b5f028deab4bd8b

IMPLEMENTATION:
- always executes qualified FAST-TEXT-01 first
- recognized COG-07 intent returns deterministic response; backend is never called
- only QueryIntent.UNSUPPORTED may reach model gate
- backend type must satisfy reviewed COG-06 CognitiveBackend
- model operation is explain only; no analyze/propose fallback
- bounded context: TextQuery, zero-authority Self-Model projection, exact post-mission VALIDATED_EXPERIENCE records
- explicit validated records must exactly match post-mission experience output refs and Self-Model refs
- model-origin claim classes restricted to INFERENCE/HYPOTHESIS/UNKNOWN/SOURCE_GAP
- INFERENCE/HYPOTHESIS require bound evidence refs
- OBSERVATION/FACT/VERIFIED_CAUSE rejected
- authority-bearing, malformed or unbound-evidence output rejected
- backend unavailable/unsupported/failure isolated with empty user text
- output remains NOT_APPROVED / NOT_EXECUTED / AUTHORITY=NONE / operational_authority=[]
- no mutations or actions

QUALIFICATION_HISTORY:
- run 36273217447: FAIL only in task-local BG language assertion; reviewed Language.BG.value is "bg"; no implementation defect established
- run 36273267719: PASS; executed head 92892e78fa588ec79d4b7b912face1cd6d7b0254

FINAL_PASS_COUNTS:
Bridge17 DIAG15 CORR12 HYP13 INT13 EXP13 PERSIST13 LIFE8 REVIEW12 CANDIDATE10 VALIDATE_REVIEW13 VALIDATED10 RETRIEVE11 POSTMISSION12 FAST_TEXT9 FAST_MODEL_TEXT13 COG06=14 COG28_MOCKED=5 COG07=16 COG05=13 COG27=14 COG22=36 COG30=15.
TOTAL=307 PASS / 0 FAIL.

REAL_MODEL_RUNTIME:
NOT RUN.
COG-28 qualification here is mocked-runtime integration only.

INHERITED_NOT_QUALIFYING:
- COG-26 legacy source suite stale fixture
- COG-11 legacy source suite stale fixture
- historical 317 regression NOT EXECUTED

OUT_OF_SCOPE:
real model runtime, model install/select/benchmark, voice/audio, Codex, Pi, Canonical Promotion, face, gesture, dashboard.
