# TANGRA-RESEARCH-LAB-00 — Scout to Control Room Handoff

TASK_ID: TANGRA-RESEARCH-LAB-00
FROM_ROLE: SCOUT / PLANNER
TO_ROLE: CONTROL ROOM
PROJECT: TANGRA
STATUS: READY_FOR_CONTROL_ROOM

## Objective

Accept the qualified research programme and issue exactly one bounded downstream canonical task for `JOB-01 — Current Architecture and Evidence-Boundary Audit`.

## Verified current state

- WORKSHOP coordination source inspected at `711edb4bf70e88234a0a17c42a1e032b33e6031e` before Scout writes.
- TANGRA-DOCS current evidence inspected at `main@2c9ec56fe3b8a07dc12d4600dd6549f318a365ba`.
- TANGRA-CL current Cognitive evidence inspected at `main@7a720af7fe5b4321b1ba47c8d2be58c815677fd7`.
- TANGRA-2.0 inspected at `main@7fb29d1b88b4e40ba993f68d9dac4d37405a41cb`; it is a separate architecture/validation repository, not current production authority.
- Production/Pi was not accessed. Fresh runtime and exact production-source identity are `NOT VERIFIED` in this Scout run.
- Existing component work is extensive; the first missing campaign artifact is a single reconciled architecture/authority/evidence-boundary matrix.

## Source evidence

- `tasks/TANGRA-RESEARCH-LAB-00.md`
- `evidence/TANGRA-RESEARCH-LAB-00/SCOUT.md`
- Current repository paths and reviewed WORKSHOP artifacts enumerated in the Scout evidence.

## Prerequisites

- Scout qualification accepted by Control Room.
- No Pi/runtime, Codex or production access is required for JOB-01.
- The preliminary Control Room report is not required for JOB-01; it is required before final difference analysis.

## Affected components

- New WORKSHOP task/evidence/review artifacts for one read-only research unit.
- Read-only inspection of current files at the verified repository refs.

## Protected components

- All TANGRA target repository contents.
- Production/Pi/runtime and services.
- HQ/Hailo/NanoTracker/current tracker/CurrentTargetManager/range/HOROS/Fusion/Mission/communications/FC/Cognitive behavior and authority.
- WORKSHOP controller/state-machine semantics.

## Exact requested action

Issue one canonical Worker task with this bounded objective:

> Build a current claim-to-source matrix for the TANGRA full system at the verified refs. Trace subsystem ownership, authority, interfaces, evidence maturity, dated validation, current limitations, conflicts and source gaps across perception/tracking, range/camera geometry, HOROS/Fusion/world model, timing/performance, communications/flight and Cognitive. Reconcile current documents against relevant WORKSHOP reviewed evidence. Do not resolve the specialist research questions, conduct external literature research, run quantitative experiments, access production/runtime, or propose implementation. Return the smallest dependency corrections needed for JOB-02..07.

Required deliverables:

1. subsystem and interface map with authoritative source/ref for every edge;
2. claim-to-evidence table with provenance class and evidence date;
3. protected authority matrix;
4. contradiction/staleness/source-gap register;
5. dependency recommendation for JOB-02..07;
6. execution ledger;
7. independent Reviewer request.

## Non-goals

- No answer to H1-H9.
- No production recommendation, architecture redesign or optimization.
- No external state-of-the-art research.
- No Monte Carlo, replay or error-budget execution.
- No target-repository write, Codex, Pi/runtime action, command, flight, flash or actuation.
- No creation of the remaining programme tasks in advance.

## Acceptance criteria

1. Every material current-state claim points to an exact repository/ref/path or is `NOT VERIFIED`.
2. Repository facts are separated from retained runtime evidence and fresh runtime state.
3. Current and proposed/future architectures are not conflated.
4. Target/Fusion/HOROS/Cognitive/flight authority boundaries are explicit.
5. Conflicts and stale documents are recorded without selecting a preferred claim unless authority/date evidence supports it.
6. Existing reviewed evidence is reused and no completed component investigation is repeated.
7. The output narrows dependencies for JOB-02..07 without executing them.
8. Read-only target boundary and repository hygiene pass.
9. An independent Reviewer verifies the actual Worker artifact before Control Room advances.

## Validation method

- Cross-check the matrix against exact files at the four verified repository refs.
- Sample every subsystem row back to its cited source.
- Compare current documents with dated WORKSHOP review/checkpoint evidence.
- Verify no target repository diff and no runtime action.
- Reviewer classifies scope coverage, authority correctness, provenance separation, contradiction handling and hygiene.

## Pre-change checkpoint

Not applicable to target repositories. WORKSHOP pre-Scout checkpoint: `711edb4bf70e88234a0a17c42a1e032b33e6031e`.

## Rollback method

Revert only the future WORKSHOP task/evidence coordination commit. No target implementation rollback applies.

## Execution access state

Repository read access is verified for WORKSHOP, TANGRA-DOCS, TANGRA-CL and TANGRA-2.0. Runtime access is not required and is not authorized.

## Codex justification

Not applicable. Codex is forbidden for this repository-reading and evidence-reconciliation unit.

## Stop

After Control Room issues JOB-01 as one canonical task, stop. Do not issue JOB-02 or later units until JOB-01 Worker evidence and independent review are complete.
