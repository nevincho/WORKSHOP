# TANGRA-RESEARCH-LAB-00 — Full-System Research Campaign Scout / Planner Qualification

TASK_ID: TANGRA-RESEARCH-LAB-00
PROJECT: TANGRA
PRIORITY: HIGH
STATUS: READY
TYPE: SCOUT / PREPARATION / READ-ONLY RESEARCH CAMPAIGN
OBJECTIVE: Independently reconstruct and qualify the bounded research programme required to test TANGRA full-system architecture, evidence quality, physical-state validity and research priorities before any research Worker job is released. Treat the existing Control Room preliminary report only as hypotheses to challenge, not as accepted conclusions.
SOURCE_PLAN_OR_REQUEST: Vlad explicit Control Room authorization, 2026-10-05 — mandatory full WORKSHOP research pass and repository-mediated submission.
CURRENT_STATE:
- Coordination authority: nevincho/WORKSHOP.
- Canonical TANGRA architecture/documentation authority: nevincho/TANGRA-DOCS, current main unless repository evidence establishes a more specific authoritative ref.
- Cognitive implementation/research authority must be verified from current repository evidence; TANGRA-CL and any linked current implementation repository must not be inferred from conversation history.
- Previous Control Room research report is PRELIMINARY CONTROL-ROOM ANALYSIS only and is NOT WORKSHOP_QUALIFIED.
- TANGRA production/Pi/runtime modification is not authorized.
- WORKSHOP repository coordination writes required by canonical protocol are authorized for this campaign.
PREREQUISITES:
- Read AGENTS.md, applicable policies, registry, projects/TANGRA.md, status/WORKSHOP_STATE.yaml, control_room/CURRENT.md and mandatory schemas.
- Verify current target repositories/refs before repository-dependent conclusions.
- Check existing WORKSHOP tasks/evidence/reviews to prevent duplicate research.
DEPENDENCIES:
- NONE. This is the campaign Scout/Planner entry task.
AFFECTED_COMPONENTS:
- WORKSHOP task/evidence coordination artifacts only.
- Read-only inspection of TANGRA-DOCS, TANGRA-CL and other currently verified TANGRA repositories.
PROTECTED_COMPONENTS:
- TANGRA-DOCS contents.
- TANGRA-CL contents.
- Production TANGRA/Pi5/runtime.
- Validated perception, tracking, estimation, HOROS, Fusion, Mission, communications, flight-control and Cognitive implementation.
- WORKSHOP controller/scheduler architecture and state-machine semantics.
EXECUTION_CLASS: WORKER
CODEX_ALLOWED: NO

HYPOTHESES_TO_CHALLENGE:
- H1: Existing perception architecture should remain substantially unchanged before airborne PoC.
- H2: Physical measurement/evidence qualification is currently more valuable than estimator sophistication.
- H3: HOROS should remain downstream and non-authoritative.
- H4: Current CV estimator should remain production primary.
- H5: Cognitive Layer isolation and zero operational authority are appropriate.
- H6: Current compute performance does not justify optimization work.
- H7: Independent synchronized physical ground truth is the largest validation deficiency.
- H8: A01/A03/A04/A08/A16 form one coherent Physical State Evidence Qualification programme.
- H9: No major architectural weakness was missed by the preliminary Control Room pass.

REQUIRED_RESEARCH_LANES_TO_DECOMPOSE:
1. System Architecture Audit.
2. Perception / Tracking / Estimation.
3. Range / Camera / Physical Geometry.
4. HOROS / Fusion / World Model.
5. Timing / Concurrency / Performance.
6. Communications / Flight Interfaces.
7. Cognitive Layer.
8. Validation / Scientific Method Red Team.
9. External State-of-the-Art Research.

QUANTITATIVE_RESEARCH_TO_ROUTE_WHERE_EVIDENCE_PERMITS:
- Range-error Monte Carlo or parameter sweep without invented TANGRA distributions.
- Temporal-error modelling for velocity, observation age, latency, jitter and dropout.
- Identical-observation CV versus genuine-CA replay where authentic replay evidence exists; otherwise explicitly bounded SYNTHETIC stress testing.
- First-order physical-state error budget from detection/bbox through range, camera geometry, extrinsics, attitude, timing and world position.

SCOUT / PLANNER WORK:
1. Reconstruct the current authoritative TANGRA research baseline from repository evidence; do not perform the nine investigations themselves.
2. Search existing WORKSHOP task/evidence/review/checkpoint history for already-completed work relevant to each lane and mark reusable evidence versus obsolete/insufficient evidence.
3. Test whether each proposed lane is still required, duplicated, premature, blocked or needs narrower decomposition.
4. Determine dependency order. Do not assume nine simultaneous jobs.
5. Define the smallest bounded downstream research jobs needed to cover the authorized programme, including cross-examination and independent review gates.
6. For every proposed downstream job identify: exact question, authoritative inputs, protected scope, execution class, acceptance evidence, validation method, dependencies, and required independent reviewer.
7. Preserve explicit provenance classes for later synthesis: REPOSITORY FACT / EXTERNAL FACT / EXPERIMENT RESULT / SYNTHETIC RESULT / ENGINEERING INFERENCE / HYPOTHESIS / NOT VERIFIED.
8. Ensure the downstream programme can produce a WORKSHOP EXECUTION LEDGER without exposing hidden chain-of-thought.
9. Explicitly identify any part that cannot be executed through current repository-safe WORKSHOP routes and the exact evidence for that limitation.
10. Do not research or defend the preliminary conclusions. Scout output is programme qualification and dependency planning only.

REQUIRED_LATER_CAMPAIGN_GATES:
- Independent investigations by WORKSHOP Workers.
- Quantitative experiments where responsibly supportable.
- Validation/scientific-method Red Team.
- Cross-examination between findings before consolidation.
- Independent Reviewer not authoring the primary finding.
- Reviewer classification: SUPPORTED / PARTIALLY SUPPORTED / INSUFFICIENT EVIDENCE / CONTRADICTED / UNNECESSARY / SPECULATIVE.
- Final Control Room synthesis only after reviewed WORKSHOP evidence exists.
- Mandatory difference analysis against PRELIMINARY CONTROL-ROOM ANALYSIS.

ACCEPTANCE_CRITERIA:
1. Current authoritative repositories/refs and relevant existing WORKSHOP evidence are identified without relying on conversation history as authority.
2. H1-H9 are preserved as challengeable hypotheses, not accepted findings.
3. All nine required research domains are mapped to bounded downstream work or explicitly rejected/deferred with evidence.
4. Quantitative experiments A-D are mapped only where inputs/validation can be established responsibly.
5. Dependencies and safe sequencing are explicit.
6. Duplicate/already-completed work is not recreated.
7. Read-only target-project boundary is preserved.
8. No Codex production task is created or invoked.
9. No Worker/Reviewer result is manufactured by Control Room.
10. Scout evidence is persisted under evidence/TANGRA-RESEARCH-LAB-00/SCOUT.md with a precise routing verdict.
11. If downstream work is justified, Scout returns a bounded handoff sufficient for Control Room to issue the first research Worker task according to canonical one-task-at-a-time policy.
12. If blocked, the exact missing transition/evidence is recorded rather than using lack of direct chat invocation as a generic blocker.

VALIDATION_METHOD:
- Repository cross-check against current WORKSHOP policies/state/history and current authoritative TANGRA repository evidence.
- No production execution.
- No Pi/runtime action.
- No implementation test required at Scout stage.
PRE_CHANGE_CHECKPOINT: NOT APPLICABLE — coordination/read-only research task; no target implementation change.
ROLLBACK_METHOD: Delete/revert only this WORKSHOP coordination task and task-local evidence if submission itself is invalidated; no TANGRA rollback is applicable.
EVIDENCE_PATHS:
- evidence/TANGRA-RESEARCH-LAB-00/SCOUT.md
- handoffs/TANGRA-RESEARCH-LAB-00.md if canonical routing requires a separate handoff
- subsequent task/review paths only after Scout qualification and Control Room issuance

STOP_CONDITION:
- Stop Scout stage at READY_FOR_CONTROL_ROOM / READY_FOR_WORKER-equivalent bounded handoff, BLOCKED with exact evidence, or REWORK_REQUIRED.
- Do not execute any of the nine research lanes as part of this Scout task.
- Do not modify TANGRA repositories or runtime.
