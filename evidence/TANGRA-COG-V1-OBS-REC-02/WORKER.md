# TANGRA-COG-V1-OBS-REC-02 — WORKER EVIDENCE

DATE: 2026-10-04
RESULT: ENGINEERING COMPLETE
CODEX: NOT USED
PI_CHANGES: NONE
AUTHORITY: NONE
OPERATIONAL_AUTHORITY: []

TARGET_REPOSITORY: nevincho/TANGRA-2.0
BASE: tangra-cog-v1-obs-rec-01@ef9db4b3691e3807982d4cdc0cddd80dfe310195
BRANCH: tangra-cog-v1-obs-rec-02
FINAL_HEAD: c1b4c171f4747ab0d2936a32633284084a01638a

FINAL_DELTA:
- TAI_COGNITIVE_INTEGRATION_PACKAGE/cognitive/state_evidence/tangra_state_recorder/recorder.py
  blob: 998b03a7b30cd23739902a17b0e058887c72da5d
- TAI_COGNITIVE_INTEGRATION_PACKAGE/integration/cognitive_mission_evidence_capture.py
  blob: 7daed227f0ab2bbe752106fc7f6d7013f023c6fc
- TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/fixtures/sample_record.jsonl
  blob: eccc4dcaab80e20c9970b0a9f8676d8a547fff74
  provenance: exact copy of frozen COG-01 fixture TANGRA_2_0/00_FOUNDATION/TAI_COG_01/fixtures/sample_record.jsonl
- TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/integration/test_cognitive_mission_evidence_durability.py
  blob: 5a5bd309e7d9916b2ec2416727d0b6b7fdac3467

IMPLEMENTED:
- automatic next-sequence recovery from highest valid retained record;
- restart cannot reuse a retained sequence even if configured start_sequence is lower;
- conservative torn-tail recovery for only the newest incomplete non-newline-terminated JSONL line;
- torn bytes are quarantined to one overwrite-only recorder-torn-tail.quarantine file and removed from active JSONL;
- complete malformed/corrupt records remain hard replay errors;
- tail recovery metadata persists and binds to the last valid sequence so a historical crash cannot classify a later mission as recovered;
- mission status classifies COMPLETE, INCOMPLETE, or RECOVERED_AFTER_CRASH;
- OBS-REC-01 STOP now persists completion_state=COMPLETE and recorder loss counters;
- bounded drain timeout added; stop remains fail-open/bounded;
- configurable max_total_bytes and max_mission_bytes for JSONL event evidence;
- count/file retention preserved;
- byte pressure discards MISSION_NUMERIC_AGGREGATE before other records, with lifecycle/error/transition/loss evidence highest priority;
- retention removals are explicitly accounted;
- atomic recorder-status.json sidecar persists queue overflow, I/O, malformed, retention and tail-recovery counters;
- no database or second recorder introduced.

STORAGE BOUNDARY:
- configured byte caps apply to JSONL event evidence;
- recorder-status.json is one atomic fixed-shape sidecar;
- recorder-torn-tail.quarantine is one overwrite-only bounded auxiliary file containing at most the current recovered torn tail;
- Mission producer submit path remains queue-only and performs no filesystem I/O.

QUALIFICATION HISTORY:
- run 37197004007: NOT QUALIFYING; one compatibility defect found: complete malformed record raised during constructor rather than existing replay-time contract. Fixed.
- run 37197052748: task 9/9 PASS and OBS-REC-01 6/6 PASS; COG-01 collection blocked by missing PYTHONPATH. Workflow environment defect.
- run 37197082947: task 9/9 PASS, OBS-REC-01 6/6 PASS, COG-01 11/12 PASS; final baseline test blocked because integration package lacked its referenced canonical fixture. Exact frozen fixture restored.
- run 37197124897: PASS before final reviewer hardening.
- final authoritative run 37197316122: SUCCESS after sequence-bound crash classification and bounded quarantine hardening.
  - py_compile PASS
  - OBS-REC-02: 9/9 PASS
  - OBS-REC-01 regression: 6/6 PASS
  - COG-01 regression: 12/12 PASS
  - bounded total: 27 PASS / 0 FAIL

BOUNDARIES:
- COG-15 unchanged
- COG-16 unchanged
- COG-22 unchanged
- Cognitive Bridge unchanged
- Mission runtime/IPC unchanged
- cameras/Hailo/tracker/Kalman/CurrentTargetManager/HOROS unchanged
- no Pi/production wiring

FINAL_RESULT:
ENGINEERING_COMPLETE / QUALIFICATION_PASS / AUTHORITY_NONE
