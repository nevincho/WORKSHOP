# TANGRA-COG-V1-FAST-MODEL-TEXT-01 — Bounded Read-Only Model-Backed FAST Text Response Gate

TASK_ID: TANGRA-COG-V1-FAST-MODEL-TEXT-01
PROJECT: TANGRA
STATUS: COMPLETE — WORKSHOP_QUALIFIED / REVIEWER_PASS
TYPE: BOUNDED READ-ONLY TEXT RESPONSE COMPOSITION / QUALIFICATION

OBJECTIVE:
Extend qualified FAST-TEXT-01 only for COG-07 UNSUPPORTED text questions by using the existing reviewed COG-06 CognitiveBackend.explain() contract with COG-28-compatible structured output semantics.

BASE:
nevincho/TANGRA-2.0:tangra-cog-v1-fast-text-01@aec6a3d85cad8330f6c1bc09127d7c5e61378aed

PRECEDENCE:
1. Always execute qualified FAST-TEXT-01 first.
2. If COG-07 intent is recognized, return that deterministic result unchanged and do not call backend.
3. Only QueryIntent.UNSUPPORTED may enter model-backed explain gate.

CONTEXT:
- original reviewed TextQuery
- genuine zero-authority COG-26 Self-Model
- qualified post-mission CognitivePipelineResult
- explicit genuine COG-22 VALIDATED_EXPERIENCE records whose IDs exactly match post-mission experience output refs
- evidence/provenance/limitations from those read-only records
- BG/EN language only

BACKEND:
- reviewed COG-06 CognitiveBackend only
- operation EXPLAIN only
- require backend available and explain capability
- no propose/analyze fallback
- validate structured response before rendering
- allowed model-origin claim classes only: INFERENCE, HYPOTHESIS, UNKNOWN, SOURCE_GAP
- every claim evidence_ref must be present in supplied validated Experience evidence context
- authority must be NONE and operational_authority empty
- backend failure/unavailable/unsupported/malformed/promotion attempt returns bounded failure; never fabricate text

OUTPUT:
- deterministic wrapper result marking DETERMINISTIC or MODEL source
- model text rendered deterministically from validated structured claims/unknowns/limitations
- approval_state=NOT_APPROVED
- execution_state=NOT_EXECUTED
- authority=NONE
- operational_authority=[]

PROTECTED:
- COG-06 unchanged
- COG-28 unchanged
- COG-07 unchanged
- COG-05 unchanged
- COG-26 unchanged
- FAST-TEXT-01 unchanged
- post-mission/Experience chain unchanged

PROHIBITED:
- real-model runtime qualification
- model install/download/selection/benchmarking
- STT/TTS/audio
- voice wiring
- Codex
- Pi
- Canonical Promotion
- face/gesture/dashboard
- command/tool/action execution
- Experience/Self-Model/identity mutation

QUALIFICATION:
- deterministic recognized intent never invokes backend
- normal unsupported question reaches explain only
- deterministic stub success path
- malformed/promoted/authority-bearing/unbound-evidence response rejected
- backend unavailable/failure isolated
- exact Experience-ref chain validation
- BG/EN bounded context
- protected regression suites where compatible
- independent Reviewer PASS

NEXT_IF_QUALIFIED:
Reconcile actual local model runtime qualification requirements for this gate. Do not execute real-model runtime in this task.

REAL_MODEL_RUNTIME: NOT_RUN
CODEX: NOT_USED
PI_CHANGES: NONE
VOICE_AUDIO: NOT_STARTED
CANONICAL_PROMOTION: DEFERRED


RESULT:
- WORKSHOP_QUALIFIED
- REVIEWER_PASS
- CHECKPOINT: checkpoints/TANGRA-COG-V1-FAST-MODEL-TEXT-01.md
- TARGET_HEAD: nevincho/TANGRA-2.0:tangra-cog-v1-fast-model-text-01@e43e0bd24f276ec9a3acb725e0888853e0eb8762
- TESTS: 307 PASS / 0 FAIL
- DETERMINISTIC_COG07_PRECEDENCE: QUALIFIED
- COG06_EXPLAIN_ONLY_MODEL_GATE: QUALIFIED
- COG28_MOCKED_INTEGRATION: 5/5 PASS
- REAL_MODEL_RUNTIME: NOT RUN
- MODEL_INSTALL_SELECTION: NOT STARTED
- VOICE_AUDIO: NOT STARTED
- CODEX: NOT USED
- PI_CHANGES: NONE
- CANONICAL_PROMOTION: DEFERRED
- HISTORICAL_317_REGRESSION: NOT EXECUTED
- NEXT_DEPENDENCY: reconcile and qualify one actual local model/runtime pair against reviewed COG-28 and qualified FAST-MODEL-TEXT gate
