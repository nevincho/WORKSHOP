# Planner — TANGRA-FC-SA-05-01-LOCAL-STATE

STATUS: IMPLEMENTATION_READY
OBJECTIVE: Create versioned internal local-frame state contract for X/Y/Z and VX/VY/VZ with origin, timestamps, freshness, validity, health and uncertainty.
BOUNDARY: portable C++17 module with deterministic host tests only for STEP_5.
ADAPTERS: Simulation/estimator producers must populate LocalNavigationState; physical GNSS is not required.
ACCEPTANCE: build/test PASS; repository read-back equals executed payload; no physical actuation; integration NOT_YET_PERFORMED.
