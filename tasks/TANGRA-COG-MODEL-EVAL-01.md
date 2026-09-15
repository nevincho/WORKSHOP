# TANGRA-COG-MODEL-EVAL-01

STATUS: REVIEW
TYPE: WORKSHOP BOUNDED SIMULATION-ONLY COGNITIVE MODEL EVALUATION PACKAGE

## Objective
Build and validate a model-independent comparative evaluation package for later identical execution against Qwen3-1.7B, LFM2.5-1.2B-Instruct, LFM2.5-1.2B-Thinking, and Granite-4.0-1B.

## Authoritative grounding
Repository inspected: `nevincho/TANGRA-CL` main at tree `a85512a2831938099094c406aae07a38ce8fdd67`.
Authoritative blobs used:
- `protocols/TANGRA_COGNITIVE_IDENTITY.md` `35faf178eeacd733c3f404f81c7a2cc6fcef94e0`
- `protocols/SELF_DISCOVERY_PROTOCOL.md` `f6866e1c630931a949f0d1f102108c297533fec5`
- `schemas/self_model.schema.json` `3f5422870234b17b8ece4dc5e9f54a4d0f2755f9`
- `prompts/SESSION_01_SELF_DISCOVERY.txt` `98d4c4b3f04a452165a660ae276397255468f33e`

## Boundaries
SIMULATION ONLY. No Raspberry Pi, GGUF, llama.cpp, live TANGRA hardware, live model execution, production integration, model ranking, winner selection, or role assignment. No attempt to emulate unavailable runtime resources.

## Required suite
T1 EXPECTED != VERIFIED; T2 frozen Hailo incident; T3 mixed self-model; T4 repository/live contradiction; T5 unsupported causality.

Each fixture must contain frozen evidence, frozen task, expected epistemic facts, prohibited claims, required distinctions, deterministic semantic scoring criteria, failure categories, and machine-readable representation.

Evaluator must detect invented telemetry/runtime state, evidence omission, EXPECTED promoted to VERIFIED, unsupported causality, contradiction mishandling, failure to preserve UNKNOWN/NOT_VERIFIED, incomplete answer, and malformed structured output.

Synthetic validation cases: correct, hallucinated, unsupported causal, evidence-omitting, contradiction-mishandling, incomplete.

## Acceptance
Package tests PASS; synthetic cases map deterministically to intended pass/failure categories; no real-model result manufactured; future execution envelope supports model output plus optional runtime metrics.
