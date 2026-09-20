# TANGRA-COG-BRIDGE-01 — Cognitive Bridge Local Integration

TASK_ID: TANGRA-COG-BRIDGE-01
PROJECT: TANGRA
PRIORITY: HIGH
STATUS: REVIEW — QUALIFIED WITH REGRESSION LIMITATION
OBJECTIVE: Implement and independently qualify the minimal read-only Cognitive bridge between current TANGRA operational evidence and the reviewed Cognitive Layer, stopping at READY FOR REAL PI QUALIFICATION.
SOURCE_PLAN_OR_REQUEST: Vlad Control Room authorization, 2026-09-20.
CURRENT_STATE: Repository-to-executor transfer and Python/shell execution are proven. Existing bridge implementation at nevincho/TANGRA-2.0:cognitive-bridge-integration@bd11d92f396b68de00a0f3636ae49ed8310ce420 passed the bounded bridge qualification 17/17 after two qualification-test harness/path defects were repaired. No bridge implementation defect is established. The cumulative 317-test regression was NOT EXECUTED because complete exact regression-environment acquisition/persistence hit demonstrated connector/tool lifecycle limits. No 317/317 PASS is claimed. Pi remains untouched. Codex has not been used.
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
EXECUTION_CLASS: REVIEWER
CODEX_ALLOWED: HUMAN_HANDOFF_ONLY_AFTER_REVIEW
ACCEPTANCE_CRITERIA:
- Preserve authority=NONE and operational_authority=[].
- Structured StateEvent ingress preserves provenance/epistemic/realism/evidence/correlation.
- ACTIVE is record-only; STANDBY may run cognition; unknown lifecycle cannot run cognition.
- Selective Self Knowledge retrieval and deterministic disclosure boundary.
- Atomic checkpoint save/restore/corruption/failed-write behavior.
- Cognitive failures fail open relative to operations.
- Future Cognitive Vision ingress reserved only.
- Independent Reviewer must assess the implementation and executed evidence without converting the unexecuted cumulative regression into PASS.
VALIDATION_METHOD:
- Executed bridge qualification: 17/17 PASS.
- Cumulative 317-test regression: NOT EXECUTED — demonstrated execution-environment acquisition/persistence limitation; no PASS claim.
- Independent Reviewer inspection against authoritative contracts and evidence.
- Real Pi/runtime lifecycle/resource/isolation/storage and production regression validation deferred to the separately human-run Codex gate.
PRE_CHANGE_CHECKPOINT: nevincho/TANGRA-2.0:tai-cog-32-package@9629a624358b8ae539ac1af54af72b9828ba5632
CANDIDATE_HEAD: nevincho/TANGRA-2.0:cognitive-bridge-integration@bd11d92f396b68de00a0f3636ae49ed8310ce420
ROLLBACK_METHOD: discard cognitive-bridge-integration candidate / restore pre-change checkpoint; production untouched.
EVIDENCE_PATHS:
- evidence/TANGRA-COG-BRIDGE-01/IMPLEMENTATION.md
- evidence/TANGRA-COG-BRIDGE-01/WORKER_EXECUTION_2026-09-20.md
- evidence/TANGRA-COG-BRIDGE-01/EXISTING_PYTHON_EXECUTION_ROUTE_FORENSIC.md
- evidence/TANGRA-COG-BRIDGE-01/EXECUTION_ROUTE_RECOVERY_2026-09-20.md
- control_room/WORKER_EXECUTION_INCIDENT_2026-09-20.md
- review/TANGRA-COG-BRIDGE-01.md

LIMITATION: CUMULATIVE_REGRESSION = NOT_EXECUTED_ENVIRONMENT_LIMITATION.
NEXT_GATE: INDEPENDENT_REVIEW.
