# TASK-031 — Scout / Planner

DATE: 2026-08-26
ROLE: SCOUT / PLANNER
RESULT: READY_FOR_WORKER

## Necessity / duplication
TASK-030 is PASS. `nevincho/LIVE@Legacy` has shared `HomeNode`/device-registry and event-envelope boundaries, but no committed voice endpoint contract under `family_guardian_ai/SOURCE_V09/contracts/`. A small contract is therefore justified; a new audio subsystem is not.

## Current verified target state
- Target repository: `nevincho/LIVE`, branch `Legacy`.
- Pre-change target head: `4a0cc9253bcc890f64de678e64708de6b8368980`.
- `device_registry_v1.json` already supports `audio_endpoint` as a device type.
- `HomeNode` is device-neutral and validates against the shared registry contract.
- Existing contracts include device registry, event envelope and backup manifest.
- Direct Echo Show 5 generation/API/raw microphone/raw speaker/local transport capability remains NOT VERIFIED.

## Smallest justified implementation
Add only:
1. `contracts/voice_endpoint_v1.json` describing a conservative provider/device-neutral voice endpoint boundary and explicit evidence gates;
2. `tests/test_voice_endpoint_contract.py` validating the contract and ensuring unverified Echo capabilities are not silently enabled.

Do not modify VK Core/personality/memory. Do not add Alexa SDK/API assumptions, runtime bridge, credentials, network access, microphone capture or speaker control.

## Validation method
Run the committed standard-library contract test against exact repository bytes. This validates only the repository contract, not Echo runtime capability.

## Checkpoint / rollback
Pre-change rollback: `4a0cc9253bcc890f64de678e64708de6b8368980`.
Rollback any TASK-031 implementation by reverting the contract/test commits; no runtime change is authorized.

## Codex gate
NOT REQUIRED. This is bounded repository-safe contract work.
