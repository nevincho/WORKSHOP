# TASK-TANGRA-HOROS-GEOMETRY-RANGE-TEMPORAL-STABILITY-T5-20260908
TASK_ID: TASK-TANGRA-HOROS-GEOMETRY-RANGE-TEMPORAL-STABILITY-T5-20260908
PROJECT: TANGRA
STATUS: REVIEW
OBJECTIVE: Measure temporal stability of every-frame geometry/range recomputation before considering propagation.
FROZEN_INPUTS:
- TASK1: c7b378841979f82b037c47be3571fa72a7b70e51
- TASK2: 4bd4b5d38357db501de07511aeabaa4c0ae058e1
- TASK3: c121ce25dbba84520c6f8e644281a7cb2bf3ee73
- TASK4: 7f628a727b89599ea6977053ea12211b10e0ffcd
PROTECTED: TASK 1-4, production runtime, detector, NanoTracker, CA Kalman, CurrentTargetManager, range estimator, HOROS runtime, Guidance, Dashboard, command paths.
IMPLEMENTATION_SCOPE: standalone synthetic temporal stability harness + fixtures + metrics/tests/benchmark only.
PRODUCTION_INTEGRATION: NO
TEMPORAL_PROPAGATION_IMPLEMENTED: NO
ACCEPTANCE_GATES: static center RMS <=1.5 px; stable span CV <=2%; stable fused range CV <=3%; recovery <=1 frame after fault; no cross-target state leakage.
PRODUCTION_GATES: AI→CAL transform NOT_VERIFIED; physical point/span correspondence NOT_VERIFIED; physical metric accuracy NOT_VERIFIED; Pi5 E2E NOT_VERIFIED.
