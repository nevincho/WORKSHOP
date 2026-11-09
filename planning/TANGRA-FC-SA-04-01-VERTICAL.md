# Planner — TANGRA-FC-SA-04-01-VERTICAL

STATUS: IMPLEMENTATION_READY
OBJECTIVE: Create simulation-first vertical state/velocity target and bounded altitude-hold control contract with validity/freshness handling.
BOUNDARY: portable C++17 module with deterministic host tests only for STEP_4.
ADAPTERS: Map existing estimator/barometer state into VerticalState and map collective_delta into the existing controller architecture.
ACCEPTANCE: build/test PASS; repository read-back equals executed payload; no physical actuation; integration NOT_YET_PERFORMED.
