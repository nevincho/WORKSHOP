# TANGRA-RESEARCH-LAB-01 — Current Architecture and Evidence-Boundary Audit

TASK_ID: TANGRA-RESEARCH-LAB-01
PROJECT: TANGRA
CAMPAIGN: TANGRA-RESEARCH-LAB
PRIORITY: HIGH
STATUS: READY
TYPE: WORKER / READ-ONLY RESEARCH
OBJECTIVE: Build a current claim-to-source matrix for the TANGRA full system at the refs qualified by TANGRA-RESEARCH-LAB-00. Trace subsystem ownership, authority, interfaces, evidence maturity, dated validation, current limitations, conflicts and source gaps across perception/tracking, range/camera geometry, HOROS/Fusion/world model, timing/performance, communications/flight and Cognitive. Reconcile current documents against relevant WORKSHOP reviewed evidence. Do not resolve specialist research questions, conduct external literature research, run quantitative experiments, access production/runtime, or propose implementation.
SOURCE_PLAN_OR_REQUEST: TANGRA-RESEARCH-LAB-00 Scout/Planner qualification and handoff, accepted by Control Room 2026-10-05.
PREREQUISITES:
- TANGRA-RESEARCH-LAB-00 SCOUT_COMPLETE / READY_FOR_CONTROL_ROOM.
- Use exact qualified refs unless newer repository evidence must be explicitly reconciled:
  - nevincho/TANGRA-DOCS main@2c9ec56fe3b8a07dc12d4600dd6549f318a365ba
  - nevincho/TANGRA-CL main@7a720af7fe5b4321b1ba47c8d2be58c815677fd7
  - nevincho/TANGRA-2.0 main@7fb29d1b88b4e40ba993f68d9dac4d37405a41cb
- Reuse existing WORKSHOP reviewed evidence; do not repeat completed component investigations.
DEPENDENCIES:
- TANGRA-RESEARCH-LAB-00
AFFECTED_COMPONENTS:
- WORKSHOP task/evidence/review/checkpoint artifacts only.
- Read-only inspection of verified target repository refs.
PROTECTED_COMPONENTS:
- All TANGRA target repository contents.
- Production/Pi/runtime/services.
- Perception/tracking/range/HOROS/Fusion/Mission/communications/flight-control/Cognitive behavior and authority.
EXECUTION_CLASS: WORKER
CODEX_ALLOWED: NO

REQUIRED_DELIVERABLES:
1. Subsystem and interface map with authoritative source/ref for every edge.
2. Claim-to-evidence table with provenance class and evidence date.
3. Protected authority matrix.
4. Contradiction/staleness/source-gap register.
5. Dependency recommendation for JOB-02..07.
6. Execution ledger.
7. Independent Reviewer request.

PROVENANCE_CLASSES:
- REPOSITORY FACT
- EXTERNAL FACT
- EXPERIMENT RESULT
- SYNTHETIC RESULT
- ENGINEERING INFERENCE
- HYPOTHESIS
- NOT VERIFIED

ACCEPTANCE_CRITERIA:
1. Every material current-state claim points to an exact repository/ref/path or is NOT VERIFIED.
2. Repository facts are separated from retained runtime evidence and fresh runtime state.
3. Current and proposed/future architectures are not conflated.
4. Target/Fusion/HOROS/Cognitive/flight authority boundaries are explicit.
5. Conflicts and stale documents are recorded without selecting a preferred claim unless authority/date evidence supports it.
6. Existing reviewed evidence is reused and no completed component investigation is repeated.
7. Output narrows dependencies for JOB-02..07 without executing them.
8. Read-only target boundary and repository hygiene pass.
9. Independent Reviewer verifies the actual Worker artifact before Control Room advances.

VALIDATION_METHOD:
- Cross-check matrix against exact files at qualified repository refs.
- Sample every subsystem row back to cited source.
- Compare current documents with dated WORKSHOP review/checkpoint evidence.
- Verify no target repository diff and no runtime action.
- Independent Reviewer classifies scope coverage, authority correctness, provenance separation, contradiction handling and hygiene.

NON_GOALS:
- No answer to H1-H9.
- No production recommendation, architecture redesign or optimization.
- No external state-of-the-art research.
- No Monte Carlo, replay or error-budget execution.
- No target-repository write, Codex, Pi/runtime action, command, flight, flash or actuation.
- Do not create JOB-02 or later before independent Reviewer PASS.

EVIDENCE_PATHS:
- evidence/TANGRA-RESEARCH-LAB-01/WORKER.md
- review/TANGRA-RESEARCH-LAB-01.md
- checkpoints/TANGRA-RESEARCH-LAB-01.md

PRE_CHANGE_CHECKPOINT: NOT APPLICABLE — read-only research.
ROLLBACK_METHOD: Revert only WORKSHOP coordination/evidence artifacts; no target rollback applies.

STOP_CONDITION:
- REVIEW_REQUIRED after Worker evidence is complete.
- Then independent Reviewer PASS / REWORK / BLOCKED / NOT VERIFIED.
- Control Room advances only after Reviewer PASS.

CODEX: NOT USED
PI_CHANGES: NONE
TANGRA_CHANGES: NONE
