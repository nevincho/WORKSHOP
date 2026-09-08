# M2 — Passive Guidance Decision / Translation Layer

TASK_ID: TASK-TANGRA-MISSION-GUIDANCE-M2-20260908
STATUS: REVIEW
CAMPAIGN: TANGRA Mission Management / Guidance Layer
BASE_M1_REVIEWED: 88ffcf4932545304c5a82c83c65ad01b99000680
BASE_M1_COMPLETE_METADATA: 4fc48e0a8bcb25807e84dd94d9e2c7c22ffd5cbd
SCOPE: isolated PASSIVE/SHADOW M1 MissionDecision -> typed high-level guidance intent only.

IMPLEMENTATION: handoffs/TASK-TANGRA-MISSION-GUIDANCE-M2-20260908/passive_guidance_translation.py
TESTS: 28/28 PASS host deterministic
HOST_BENCHMARK_N: 100000
HOST_MEAN_MS: 0.00491857134
HOST_MEDIAN_MS: 0.004517
HOST_P95_MS: 0.004717
HOST_MAX_MS: 0.877862
PRODUCTION_INTEGRATION: NO
PRODUCTION_AUTHORITY: FALSE
CONTROL_SIDE_EFFECTS: NONE
M1_MODIFIED: NO
HOROS_T8_TOUCHED: NO
M3_STARTED: NO

Production gates NOT_VERIFIED: production M1 runtime integration; production M2 integration; exact production navigation inputs; Pi5 E2E; Master ESP32 transport; FC command acceptance; physical flight behavior.
