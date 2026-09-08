# M1 — Mission State + Decision Contract

TASK_ID: TASK-TANGRA-MISSION-MANAGEMENT-GUIDANCE-M1-20260908
STATUS: REVIEW
CAMPAIGN: TANGRA Mission Management / Guidance Layer
SCOPE: isolated PASSIVE/SHADOW Mission Management contract only.

AUTHORITIES: Raspberry Pi owns mission logic/guidance generation; Master ESP32 communications; Flight Controller ESP32 stabilization/safety/control and final flight authority.

IMPLEMENTATION: handoffs/TASK-TANGRA-MISSION-MANAGEMENT-GUIDANCE-M1-20260908/mission_management_contract.py
TESTS: 22/22 PASS host deterministic
HOST_BENCHMARK_N: 100000
HOST_MEAN_MS: 0.00472370047
HOST_MEDIAN_MS: 0.003275
HOST_P95_MS: 0.003656
HOST_MAX_MS: 60.227272
PRODUCTION_INTEGRATION: NO
PRODUCTION_AUTHORITY: FALSE
CONTROL_SIDE_EFFECTS: NONE
HOROS_T8_TOUCHED: NO
M2_STARTED: NO

Production gates remain NOT_VERIFIED: Mission Management runtime integration; Guidance runtime integration; real carrier navigation; Pi5 E2E; Master ESP32 command transport; FC command acceptance; physical flight behavior.
