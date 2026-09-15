# VK Bootstrap Intelligence / Survival Authority

Date: 2026-09-15
Status: ARCHITECTURE REQUIREMENT — IMPLEMENTATION NOT STARTED

## FACT / governing requirement
VK Portable Seed includes CORE + MICRO-LIVE + BOOTSTRAP MICRO-MODEL + POLICY/SCENARIO ENGINE + HOST INSPECTOR + CAPABILITY ENGINE + DISTRIBUTED CLIENT + PLATFORM ADAPTERS + RECOVERY/INTEGRITY MATERIAL.

The bootstrap-model storage target is approximately 0.2–0.5 GB. This is a planning envelope only; no model is selected or authorized for download.

Mission: SURVIVE -> INTEGRATE -> DISCOVER -> ADAPT -> ESCALATE.

The survival layer must bootstrap on trusted owner-controlled hardware without requiring the normal VK runtime, primary model, accelerator, network, or another VK node. CPU-only and slow operation are acceptable.

## Authority
Bootstrap Intelligence is the highest operational authority inside the bounded BOOTSTRAP/SURVIVAL domain. It may coordinate allow-listed Micro-LIVE operations for Core verification/preservation, host inspection, resource/runtime/model/peer discovery, node-local bootstrap, compatible adapter initialization, recovery, resource adaptation, stronger inference selection/escalation, and fallback.

Operational survival authority is distinct from semantic identity authority. Bootstrap Intelligence cannot redefine LogicalIdentity, canonical personality/history, distributed protocol semantics, integrity/lineage rules, StateClass meanings, or canonical-memory admission authority.

## Bootstrap Intelligence Contract
Inputs are structured: HOST_STATE, NODE_IDENTITY, NODE_CAPABILITIES, AVAILABLE_RUNTIMES, AVAILABLE_MODELS, REACHABLE_VK_NODES, CURRENT_OPERATING_MODE, CURRENT_SCENARIO, AVAILABLE_TOOLS, CORE_INTEGRITY_STATE, RECOVERY_STATE.

Outputs must be structured, policy-validatable action intents, mode-transition proposals, capability selections, escalation/fallback decisions, or explicit inability/degraded status. The model never receives unrestricted machine authority. Deterministic policy validates/limits executable actions.

The contract is model-independent. Later candidate evaluation covers storage footprint, minimum RAM, CPU-only operation, startup latency, structured instruction/tool selection/output reliability, Bulgarian/multilingual operation, Host Inspector interpretation, deterministic-scenario operation, and offline behavior.

## Policy / Scenario Engine
The deterministic engine owns scenario definitions, allowed actions, preconditions, invariants, transition guards and failure handling. The micro-model interprets structured conditions and chooses among policy-permitted actions rather than inventing bootstrap policy.

Initial taxonomy: unknown Windows; unknown Linux x86; Linux ARM/Raspberry Pi; known-host reconnect; no usable LLM; bootstrap-model only; stronger local model found; stronger remote VK node found; offline; network restored; low RAM; low storage; no accelerator; accelerator found; damaged/incomplete runtime; Core integrity problem; distributed state unavailable/restored; higher-capability runtime failure; fallback to survival; migration/escalation to stronger hardware.

Scenarios/adapters are extensible without changing VK identity or distributed semantics.

## Operating modes
SURVIVAL_MODE: Core + Micro-LIVE + Bootstrap Intelligence.
LOCAL_MODE: stronger compatible local inference available.
DISTRIBUTED_MODE: reachable VK node supplies permitted capabilities/inference.
FULL_MODE: normal high-capability VK runtime/resources available.
DEGRADED_MODE: previously available capability failed/disappeared.
RECOVERY_MODE: integrity/runtime/state recovery required.

Transitions are explicit, observable, policy-guarded and recorded as node-local operational evidence where appropriate. Mode changes never change VK personality/identity.

## Escalation / fallback
Bootstrap Intelligence actively seeks a better compatible execution environment when policy and resources justify it. Provider/model/node changes are capability changes, not identity changes.

The survival layer remains installed/available in FULL_MODE. Required fallback path: FULL_MODE -> DEGRADED_MODE -> SURVIVAL_MODE or RECOVERY_MODE. Recovery may later re-escalate.

## Security / integrity boundary
Trusted-owner autonomy removes repetitive permission prompts for ordinary allow-listed survival operations; it does not remove technical policy boundaries. No arbitrary shell/root/admin authority is implied. Installing software, downloading models, changing drivers/host configuration, destructive state repair, secret exposure or redefining protected VK semantics requires separately authorized implementation/policy.

## ASSUMPTION
A suitably small model can meet enough structured tool-selection and Bulgarian requirements within the target storage envelope. This must be benchmarked; architecture does not depend on the assumption being true for any particular model.

## NOT VERIFIED
No micro-model benchmark, RAM/latency measurement, platform bootstrap substrate, cross-platform launcher, installer, recovery implementation, peer discovery implementation, or runtime validation has been performed.