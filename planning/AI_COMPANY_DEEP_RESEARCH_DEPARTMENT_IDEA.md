# AI_COMPANY — Deep Research Department Concept

STATUS: IDEA / DESIGN INPUT ONLY — DO NOT IMPLEMENT YET
DATE CAPTURED: 2026-08-25
OWNER: Vlad
TARGET LOCAL SYSTEM: `F:\AI_COMPANY`
REPOSITORY STATUS: dedicated AI_COMPANY GitHub repository NOT FOUND as of capture date; local project must be inspected/onboarded before implementation work.

## Why this file exists
Preserve the current design discussion independently of ChatGPT conversation history. This document is intentionally an idea record, not authorization to modify AI_COMPANY or any production project.

## Core idea
Extend the existing deterministic AI_COMPANY R&D architecture into a long-running Deep Research Department capable of investigating difficult engineering questions for hours rather than optimizing for fast conversational answers.

Example question:
> Given TANGRA's actual carrier, compute, detector/tracker, optical geometry, mass, interface, cost and operational constraints, which camera is technically preferable to the current camera and why?

The desired output is not an LLM opinion based on a few product pages. The system should gather evidence, construct candidate sets, design controlled experiments/simulations, execute deterministic measurements where possible, independently challenge the conclusions, and return a traceable recommendation with uncertainties and evidence gaps.

## Preserve existing AI_COMPANY principle
LLMs MUST NOT control workflow state.

The deterministic Python controller remains responsible for:
- stage transitions;
- budgets and hard caps;
- retries;
- persistence;
- validation;
- audit;
- founder approvals;
- termination/convergence.

Founder remains final decision maker: GO / REVISE / HOLD / KILL.

## Proposed research roles
These are conceptual roles. They do not imply one model/process per role and MUST NOT be instantiated before repository/local-state inspection and capability evaluation.

1. **Research Director / Problem Framer**
   - converts founder question into bounded research objectives;
   - defines required evidence and decision criteria;
   - prevents scope drift.

2. **Requirements Analyst**
   - derives the verified engineering envelope from authoritative project sources;
   - identifies hard constraints, interfaces, prerequisites and unknowns;
   - separates requirements from assumptions.

3. **Technology Scout**
   - searches relevant technologies and solution classes;
   - expands the candidate space without selecting a winner prematurely.

4. **Product / Primary-Source Researcher**
   - collects concrete candidate products, manufacturer datasheets/specifications, availability and cost evidence;
   - prioritizes primary sources for specifications.

5. **Evidence Curator**
   - classifies each material claim as manufacturer fact, independent measurement, calculated value, engineering assumption, hypothesis, or unknown;
   - detects conflicts, stale evidence and missing evidence;
   - maintains traceability/provenance.

6. **Systems Engineer**
   - evaluates candidates against the complete system, not isolated specifications;
   - considers compute, interfaces, bandwidth, power, mass, optics, latency, integration and downstream algorithm effects.

7. **Simulation / Experiment Engineer**
   - converts hypotheses into deterministic experiment specifications;
   - uses Python/simulation/datasets/synthetic data where technically justified;
   - does NOT allow an LLM to invent experiment results.

8. **Adversarial / Independent Reviewer**
   - independently attacks assumptions, methodology, evidence quality and recommendation;
   - checks whether experiments actually measured the claimed objective;
   - searches for disconfirming evidence and alternative explanations.

9. **Decision Synthesizer**
   - consolidates verified evidence, experiment outputs, trade-offs, uncertainty and dissent;
   - produces a recommendation without overriding Founder authority.

Existing Local Utility Worker remains appropriate for cheap extraction, routing, summarisation and query generation.

## Example: camera research experiment pipeline
For a TANGRA camera comparison, candidate cameras should be evaluated under a common controlled envelope rather than by comparing headline specifications only.

Possible pipeline:

`authoritative TANGRA requirements -> candidate cameras -> normalized optical/sensor models -> common synthetic/recorded scenes -> distance/altitude/illumination/motion/noise/compression sweeps -> existing detector/tracker/range pipeline where feasible -> metrics -> statistical comparison -> adversarial review`

Potential metrics include, where technically measurable:
- pixels on target;
- effective field of view / coverage;
- detection probability and miss rate;
- confidence distribution;
- false positives/false negatives;
- tracker continuity/reacquisition;
- motion/rolling-shutter sensitivity;
- range-estimation error;
- frame rate and end-to-end latency;
- compute and memory load;
- interface/bandwidth requirements;
- power and mass impact;
- integration complexity;
- price and availability.

Synthetic datasets/video may be used only when the simulation assumptions are explicit and validated enough for the claimed conclusion. Real recorded data should be used where available and relevant.

## Deterministic experiment rule
The intended pattern is:

`LLM research/hypothesis -> deterministic experiment specification -> Python/simulator execution -> raw measurements -> statistics -> LLM interpretation -> independent critique`

LLMs MUST NOT fabricate simulation output or treat qualitative reasoning as measured evidence.

## Long-running research
Research may intentionally run for hours. Speed is not the primary objective. The controller should enforce explicit budgets and convergence criteria so that multi-agent research does not become endless LLM dialogue.

Illustrative budget dimensions (NOT approved fixed values):
- wall-clock research duration;
- number of research queries;
- number/quality of sources;
- number of primary sources;
- candidate count;
- experiment/simulation count;
- independent analysis/review passes;
- model calls/tokens/retries;
- CPU/GPU/runtime caps.

Operating-cost policy remains £0 unless Founder explicitly changes it. No paid fallback should be introduced implicitly.

## Model capability boundary
Current known architecture brief states:
- Qwen3-1.7B is primarily Utility/fast tier and has already shown inadequate serious engineering reasoning in a controlled test;
- Qwen3.5-4B Research/Analysis/Reviewer quality remains NOT VERIFIED pending controlled evaluation;
- serious autonomous engineering/research quality remains NOT VERIFIED.

Therefore additional research roles do not by themselves improve epistemic quality. Role expansion must follow controlled model evaluation on known-answer cases.

## Relationship to WORKSHOP
Proposed separation of responsibilities:

- **AI_COMPANY:** investigate unknowns; research; evidence curation; feasibility; simulation/experiment planning/execution; alternatives; critique; advisory recommendation.
- **WORKSHOP:** authoritative project coordination; bounded implementation tasks; repository changes; validation gates; Codex budgeting/handoff; project-state tracking.

A future interface should be job/artifact based:

`WORKSHOP -> bounded AI_COMPANY research job -> AI_COMPANY deterministic pipeline -> traceable artifact/evidence package -> WORKSHOP independent verification/gating`

AI_COMPANY outputs remain advisory until their capability and evidence are independently validated. They MUST NOT automatically mutate authoritative WORKSHOP project state.

## Proposed WORKSHOP ensemble ideas captured from the same discussion
Potential future roles, subject to separate review:
- `05 CODEX TASK ENGINEER`: minimize and engineer precision Codex implementation packages after Codex Gate approval;
- `06 TEST & VALIDATION ENGINEER`: challenge whether validation methodology actually proves acceptance criteria;
- `07 REPOSITORY HYGIENE / CONTEXT ENGINEER`: compact completed task documentation and minimize future context/token cost;
- `08 SYSTEM INTEGRATION AUDITOR`: milestone-level cross-component/interface validation rather than per-patch review.

These are proposals only. Do not activate them solely because they appear in this document.

## Preconditions before implementation
1. Vlad regains local access to `F:\AI_COMPANY`.
2. Execute existing `TASK-058 — AI_COMPANY Repository Onboarding`.
3. Inspect actual controller/source/tests/runtime boundaries before changing architecture.
4. Exclude secrets, SQLite runtime state, caches, private artifacts and central model files from Git as appropriate.
5. Establish the authoritative AI_COMPANY repository/ref.
6. Evaluate Qwen3.5-4B on controlled known-answer Research/Analysis/Reviewer cases.
7. Only then design the smallest justified Research Department extension.

## Non-goals at this stage
- no immediate implementation;
- no architecture rewrite;
- no uncontrolled agent proliferation;
- no assumption that more agents automatically means better research;
- no paid model/API dependency;
- no replacement of deterministic orchestration with LLM-controlled workflow;
- no autonomous authority over production projects.
