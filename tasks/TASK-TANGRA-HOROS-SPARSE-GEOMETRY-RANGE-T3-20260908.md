# TASK-TANGRA-HOROS-SPARSE-GEOMETRY-RANGE-T3-20260908

TASK_ID: TASK-TANGRA-HOROS-SPARSE-GEOMETRY-RANGE-T3-20260908
PROJECT: TANGRA
PRIORITY: HIGH
STATUS: COMPLETE
OBJECTIVE: Standalone passive SHADOW monocular metric-range source from TASK 1 sparse geometry after TASK 2 calibrated-plane mapping, with explicit physical-span correspondences, robust multi-span fusion, uncertainty and provenance.
SOURCE_PLAN_OR_REQUEST: Vlad Control Room TASK 3, 2026-09-08.
CURRENT_STATE: COMPLETE after independent bounded review cycle. Final reviewed implementation commit: c121ce25dbba84520c6f8e644281a7cb2bf3ee73. Production metric usability remains NOT_VERIFIED.
PREREQUISITES: TASK 1 frozen commit c7b378841979f82b037c47be3571fa72a7b70e51; TASK 2 frozen commit 4bd4b5d38357db501de07511aeabaa4c0ae058e1.
DEPENDENCIES: Python 3, NumPy, standard dataclasses/enum/statistics/math/time/typing.
AFFECTED_COMPONENTS: Standalone TASK 3 handoff/evidence/review artifacts only; no runtime integration.
PROTECTED_COMPONENTS: TASK 1, TASK 2, HQ acquisition, primary detector, NanoTracker, CA Kalman, CurrentTargetManager, existing range estimator, HOROS authoritative estimator, Guidance, Dashboard, command paths.
ACCEPTANCE_CRITERIA: PASS — explicit physical-span contract; no fabricated production dimensions/correspondence; anisotropic calibrated geometry; bounded orientation model; candidate evidence with calibrated pixel/normalized spans and full provenance; robust group-aware outlier/disagreement handling; uncertainty propagation; TASK 1/2 compatibility; production NOT_VERIFIED gate; passive existing-range comparison; deterministic tests; host benchmark.
VALIDATION_METHOD: deterministic Python unittest 18/18 PASS + standalone host microbenchmark n=50,000. All physical ground-truth fixtures SYNTHETIC.
PRE_CHANGE_CHECKPOINT: WORKSHOP main 51faa24190deaf53d22d5253912c38cfd155384e.
ROLLBACK_METHOD: revert TASK 3 implementation/review commits; no production runtime modified.
EVIDENCE_PATHS: evidence/TASK-TANGRA-HOROS-SPARSE-GEOMETRY-RANGE-T3-20260908/; handoffs/TASK-TANGRA-HOROS-SPARSE-GEOMETRY-RANGE-T3-20260908/; review/TASK-TANGRA-HOROS-SPARSE-GEOMETRY-RANGE-T3-20260908.md.
CORRECTION_CYCLES: 1
FROZEN_REVIEWED_COMMIT: c121ce25dbba84520c6f8e644281a7cb2bf3ee73
PRODUCTION_METRIC_STATUS: NOT_VERIFIED
BLOCKER: NONE for standalone TASK 3. Production use requires verified live transform, verified physical span correspondences/profile and physical metric validation.
