# VK Portable Seed / Micro-LIVE Architecture

Date: 2026-09-15
Status: ARCHITECTURE DECISION — IMPLEMENTATION NOT STARTED

## Decision
`VK PORTABLE SEED = CORE + MICRO-LIVE + BOOTSTRAP MICRO-MODEL + POLICY/SCENARIO ENGINE + HOST INSPECTOR + CAPABILITY ENGINE + DISTRIBUTED CLIENT + PLATFORM ADAPTERS + RECOVERY/INTEGRITY MATERIAL`

Core alone is protected identity/personality/canonical-state material; it is not a useful portable executable instance. Micro-LIVE plus Bootstrap Intelligence form the minimum autonomous survival substrate. The bootstrap model target is approximately 0.2–0.5 GB as a planning envelope only; no model is selected.

The planned 256 GB SSD is the first physical Portable Seed carrier, not a Raspberry-Pi-specific system disk. Seed semantics remain independent of physical medium, OS, CPU, transport and implementation language. NodeIdentity remains installation/node-specific and distinct from LogicalIdentity.

## Logical storage roles
CORE: logical identity, personality/system material, canonical memory/state/admission metadata, protected contracts/manifests.

MICRO_LIVE: bounded launcher/bootstrap, Core loader/verifier, NodeIdentity manager, Host Inspector, capability engine, policy/scenario engine interface, distributed client interface, persistence adapters, inference discovery/selection interface, minimal status/control.

BOOTSTRAP_INTELLIGENCE: replaceable micro-model satisfying the Bootstrap Intelligence Contract. It is operational survival authority, never semantic identity authority.

CONTRACTS: distributed semantics, normative wire/schema/versioning, NodeCapability/NodeState, Bootstrap Intelligence, operating modes/scenarios, compatibility/conformance material.

PLATFORM_ADAPTERS: Windows, Linux x86, Linux ARM, future Android and future runtime/language implementations. No assumption that Python already exists.

STATE: node-local identity/operational state, local replica material, permitted shared records, frontiers/checkpoints/reconciliation metadata. Database files are not sync authority.

OPTIONAL_RESOURCES: stronger local models/runtimes, caches/indexes, UI/media. Optional resources are not bootstrap identity requirements.

RECOVERY: integrity manifests, versions, validated checkpoints/frontiers, rollback and migration provenance, survival-layer recovery material.

## Minimum bootstrap sequence
1. Start a platform-compatible bounded bootstrap substrate.
2. Locate and integrity-verify Core and LogicalIdentity.
3. Load/create valid NodeIdentity under enrollment rules.
4. Inspect host read-only.
5. Construct NodeCapability + NodeState.
6. Start Policy/Scenario Engine and determine scenario/mode.
7. Start Bootstrap Intelligence if no stronger permitted inference is available or if survival reasoning is required.
8. Discover compatible local runtimes/models without installing/downloading them.
9. Initialize permitted local persistence/adapters without changing canonical admission authority.
10. Discover configured/permitted distributed peers/services when connectivity exists.
11. Escalate to stronger compatible inference when policy permits.
12. Remain capable of fallback to survival/recovery when stronger capability disappears.

## Operating modes
SURVIVAL_MODE, LOCAL_MODE, DISTRIBUTED_MODE, FULL_MODE, DEGRADED_MODE, RECOVERY_MODE. Transitions must be explicit, observable and policy-guarded. They never change VK identity/personality.

## No-large-model bootstrap invariant
A large LLM is not required to start, verify Core, establish NodeIdentity, inspect/report host capabilities, initialize bounded persistence/protocol compatibility, or enter a valid survival/degraded/recovery state. CPU-only slow bootstrap is acceptable.

## Core protection boundary
Micro-LIVE/Bootstrap Intelligence may preserve and verify Core and invoke authorized interfaces. They cannot silently rewrite identity/personality, promote candidate memory, replace provenance, redefine distributed/integrity/causal semantics, infer identity from hardware, or make node-local capability state canonical.

## Layer separation
Distributed synchronization answers what VK state can be exchanged/reconciled. Capability inspection answers what the node can currently do. Survival policy may consume both, but neither layer redefines the other. Autonomous workload scheduling is outside this architecture task.

## Portability substrate
No universal language/runtime is assumed. Each supported platform class requires a minimal bootstrap substrate capable of launching Micro-LIVE, integrity verification, structured local inspection and the Bootstrap Intelligence Contract. Exact Windows/Linux x86/Linux ARM/Android packaging/runtime choices remain implementation research, not architectural identity.

## Recovery persistence
The survival layer remains available after FULL_MODE. Required architectural fallback: FULL_MODE -> DEGRADED_MODE -> SURVIVAL_MODE or RECOVERY_MODE, with later re-escalation possible.

## Governing companion
See `decisions/VK_BOOTSTRAP_SURVIVAL_AUTHORITY_2026-09-15.md`.

## FACT
VK-DIST-03 remains IMPLEMENTED / STATIC REVIEW PASS / BEHAVIORAL VALIDATION BLOCKED. This architecture work does not change that gate.

## ASSUMPTION
The 0.2–0.5 GB planning envelope may contain a sufficiently reliable bootstrap model. Benchmark evidence is required before selection.

## NOT VERIFIED / unresolved
Portable packaging/filesystem layout; platform bootstrap substrate; NodeIdentity enrollment/clone recovery; Core manifest portability; minimal UI; replica persistence store; current Pi runtime/migration; Android packaging/permissions; candidate bootstrap model; candidate RAM/CPU/latency/tool/Bulgarian performance; peer discovery; recovery execution; cross-platform survival validation.