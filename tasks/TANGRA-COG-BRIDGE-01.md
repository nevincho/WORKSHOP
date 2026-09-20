# TANGRA-COG-BRIDGE-01 — Cognitive Bridge Local Integration

TASK_ID: TANGRA-COG-BRIDGE-01
PROJECT: TANGRA
PRIORITY: HIGH
STATUS: REVIEW
OBJECTIVE: Implement and independently qualify the minimal read-only Cognitive bridge between current TANGRA operational evidence and the reviewed Cognitive Layer, stopping at READY FOR REAL PI QUALIFICATION.
SOURCE_PLAN_OR_REQUEST: Vlad Control Room authorization, 2026-09-20.
CURRENT_STATE: Gate-1 bridge implementation and qualification tests exist on nevincho/TANGRA-2.0 branch cognitive-bridge-integration, PR #1. Test execution and independent Reviewer PASS are NOT VERIFIED.
PREREQUISITES:
- TANGRA-2.0 reviewed Cognitive integration package at 9629a624358b8ae539ac1af54af72b9828ba5632.
- TANGRA-CL shadow contract a48fb4889217c7d6b33433a9a4eeeafdefbee000.
- Current production state from TANGRA-DOCS CURRENT_SYSTEM.md, evidence cutoff 2026-09-20.
DEPENDENCIES:
- Existing COG-00 StateEvent contracts.
- Existing COG-01 recorder and COG-02 EvidencePacket components.
- Existing COG-26 Self Model and COG-27 pipeline.
- Existing experience/lifecycle components where long-term promotion is required.
AFFECTED_COMPONENTS:
- TAI_COGNITIVE_INTEGRATION_PACKAGE/integration/cognitive_bridge.py
- TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/integration/test_cognitive_bridge.py
PROTECTED_COMPONENTS:
- Production HQ/Hailo/NanoTracker/CA Kalman/current-target/range/HOROS chain.
- Flight/actuator/target/mission/command/configuration/IFF/readiness/LoRa-command authority.
EXECUTION_CLASS: WORKER
CODEX_ALLOWED: NO
ACCEPTANCE_CRITERIA:
- Preserve authority=NONE and operational_authority=[].
- Structured StateEvent ingress preserves provenance/epistemic/realism/evidence/correlation.
- ACTIVE is record-only; STANDBY may run cognition; unknown lifecycle cannot run cognition.
- Selective Self Knowledge retrieval and deterministic disclosure boundary.
- Atomic checkpoint save/restore/corruption/failed-write behavior.
- Cognitive failures fail open relative to operations.
- Future Cognitive Vision ingress reserved only.
- Independent review and bounded regression PASS before COMPLETE.
VALIDATION_METHOD:
- Repository tests plus existing-package regression.
- Independent Reviewer inspection against authoritative contracts.
- Real Pi/runtime lifecycle/resource/isolation/storage validation deferred to later human-authorized Codex gate.
PRE_CHANGE_CHECKPOINT: nevincho/TANGRA-2.0:tai-cog-32-package@9629a624358b8ae539ac1af54af72b9828ba5632
ROLLBACK_METHOD: discard cognitive-bridge-integration branch / PR #1; production untouched.
EVIDENCE_PATHS:
- evidence/TANGRA-COG-BRIDGE-01/IMPLEMENTATION.md
- review/TANGRA-COG-BRIDGE-01.md (pending)
