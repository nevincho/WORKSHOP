# TANGRA-RESEARCH-LAB-02 — Physical-State Evidence and Error-Budget Qualification

TASK_ID: TANGRA-RESEARCH-LAB-02
PROJECT: TANGRA
CAMPAIGN: TANGRA-RESEARCH-LAB
PRIORITY: HIGH
STATUS: READY
TYPE: WORKER / READ-ONLY RESEARCH / QUANTITATIVE QUALIFICATION
OBJECTIVE: Determine which measured parameters presently support TANGRA detection-to-range and detection-to-world-position claims, quantify defensible first-order sensitivity/error bounds across the evidenced operating envelope, identify missing uncertainty terms and circular or cross-domain validation, and specify the smallest physical experiments required to close the material gaps. Do not modify or redesign TANGRA.
SOURCE_PLAN_OR_REQUEST: Qualified TANGRA-RESEARCH-LAB programme; JOB-01 independent Reviewer PASS and checkpoint.
CURRENT_STATE:
- JOB-01 is COMPLETE / independent Reviewer PASS.
- One bounded physical near-field point records 4.36 m measured versus 4.366 m reported.
- Camera intrinsics and paired-capture evidence are provisional/bounded; final HQ-WIDE extrinsics, carrier pose/LOCAL_ENU, known-geometry metric accuracy and operational-distance qualification remain incomplete or NOT VERIFIED.
- An earlier global-scale attempt crossed incompatible bbox domains and was rolled back.
- Fresh production source/runtime and authentic new measurements are not authorized and remain NOT VERIFIED.
PREREQUISITES:
- TANGRA-RESEARCH-LAB-01 checkpoint and Worker evidence.
- Exact qualified target refs from JOB-01.
- Reuse existing physical/calibration/geometry evidence without repeating completed component work.
DEPENDENCIES:
- TANGRA-RESEARCH-LAB-01: COMPLETE / PASS.
AFFECTED_COMPONENTS:
- WORKSHOP evidence/review/checkpoint artifacts only.
- Read-only target repository files and retained measurement artifacts.
PROTECTED_COMPONENTS:
- All TANGRA repositories, runtime, Pi, firmware, services, models and configuration.
- Existing perception, tracker, range, projection, Fusion, HOROS and authority behavior.
EXECUTION_CLASS: WORKER
CODEX_ALLOWED: NO

REQUIRED_WORK:
1. Inventory every parameter and transform used or claimed from detector bbox/crop domain through range, camera ray/projection, extrinsics, attitude/pose, time/measurement age and world frame.
2. Classify each input as measured, calibrated, assumed/prior, derived, proposed, missing or NOT VERIFIED; cite exact ref/path/date.
3. Audit ground-truth independence and detect self-comparison, circular validation, incompatible processing domains and downstream claims resting on unqualified upstream inputs.
4. Produce a first-order physical-state error budget. Use deterministic parameter sweeps across evidenced or explicitly declared bounds unless defensible probability distributions and correlations exist. Monte Carlo is permitted only when those distributions are evidenced.
5. Separate range-only, line-of-sight, camera-frame and world-frame conclusions. Do not imply world-position validation from range-only evidence.
6. Quantify what can legitimately be bounded and leave unevidenced terms NOT VERIFIED; do not invent TANGRA parameters.
7. Define the smallest physical experiments required to close the highest-impact unknowns, including falsification criteria.
8. Produce an execution ledger and independent Reviewer request.

REQUIRED_DELIVERABLES:
- parameter/transform authority table;
- ground-truth and methodology audit;
- deterministic sensitivity results and reproducible calculation artifact where justified;
- first-order error-budget table with assumptions/limitations;
- supported/partial/unsupported claim classification;
- ranked minimum experiment set;
- execution ledger;
- independent Reviewer request.

ACCEPTANCE_CRITERIA:
1. Every numerical input is traceable to exact evidence or explicitly labelled assumed/synthetic/NOT VERIFIED.
2. Processing domains and coordinate frames are explicit; incompatible domains are not combined.
3. Physical ground truth is independent of the estimator under evaluation.
4. The 4.36 m/4.366 m point is treated as one bounded point, not a full curve qualification.
5. Range-only evidence is not promoted to camera/world-position validation.
6. Sensitivity/error calculations are reproducible and do not use invented probability distributions.
7. Missing extrinsics, pose, time and world-frame terms remain visible in the budget.
8. Recommended experiments are the smallest needed to resolve material unknowns and include pass/fail measurements.
9. Existing validated behavior is protected; no TANGRA/runtime mutation or external actuation occurs.
10. Independent Reviewer verifies actual evidence, calculations, scope and hygiene before PASS.

VALIDATION_METHOD:
- Exact-ref source and retained-evidence cross-check.
- Re-run any calculation artifact deterministically and compare outputs/hashes.
- Independently sample parameter provenance and frame/domain consistency.
- Reviewer challenges ground-truth independence, uncertainty propagation and claim scope.
- Verify target repositories/runtime remained read-only.

NON_GOALS:
- No implementation, calibration change, architecture redesign or performance optimization.
- No live camera/Pi/runtime access, flight, command, flash or actuation.
- No external state-of-the-art research.
- No estimator CV/CA comparison; that belongs to JOB-04.
- No HOROS/Fusion authority conclusion beyond inputs needed for this budget; that belongs to JOB-05.
- Do not create JOB-03 or later before this task reaches independent terminal review.

EVIDENCE_PATHS:
- evidence/TANGRA-RESEARCH-LAB-02/WORKER.md
- evidence/TANGRA-RESEARCH-LAB-02/physical_state_sensitivity.py if justified
- evidence/TANGRA-RESEARCH-LAB-02/physical_state_sensitivity.json if justified
- review/TANGRA-RESEARCH-LAB-02.md
- checkpoints/TANGRA-RESEARCH-LAB-02.md

PRE_CHANGE_CHECKPOINT: checkpoints/TANGRA-RESEARCH-LAB-01.md
ROLLBACK_METHOD: Revert only WORKSHOP task/evidence/review artifacts; no target rollback applies.

STOP_CONDITION:
- REVIEW after Worker evidence is complete; then independent PASS / REWORK / BLOCKED / NOT VERIFIED.
- Continue campaign only after independent PASS and checkpoint.

CODEX: NOT USED
PI_CHANGES: NONE
TANGRA_CHANGES: NONE
