# VK Portable Seed / Micro-LIVE Architecture

Date: 2026-09-15
Status: ARCHITECTURE DECISION — IMPLEMENTATION NOT STARTED

## Decision
`VK PORTABLE SEED = VK CORE + MICRO-LIVE`

Core alone is protected identity/personality/canonical-state material; it is not a useful portable executable instance. Micro-LIVE is the minimum bounded executable substrate that can verify Core, establish the local node, inspect an unknown compatible host and enter an appropriate operating mode without requiring a large LLM.

The SSD planned for the Raspberry Pi is the first physical carrier candidate, not a Pi-specific VK architecture. Portable Seed semantics are independent of physical medium, OS, CPU and implementation language. Moving/copying an authorized seed to a compatible carrier must not change logical VK identity or distributed semantics. NodeIdentity remains installation/node-specific and must not be confused with Core identity.

## Logical storage model
No fixed filesystem paths are normative.

### CORE
- logical VK identity;
- personality/system material;
- canonical memory/state and admission metadata;
- protected Core contracts/manifests.

### MICRO_LIVE
- bounded launcher/bootstrap;
- Core loader/verifier;
- NodeIdentity manager;
- Host Inspector;
- capability engine;
- distributed protocol client interface;
- local persistence/adapters;
- inference-provider discovery interface;
- minimal local status/control interface.

### CONTRACTS
- distributed semantic contracts;
- wire/schema/versioning profile;
- NodeCapability/NodeState contracts;
- compatibility manifests and conformance vectors.

### PLATFORM_ADAPTERS
- Windows;
- Linux x86;
- Linux ARM;
- future Android;
- future language/runtime-specific implementations.

Adapters are replaceable. They cannot redefine Core identity, distributed semantics or capability meanings.

### STATE
- node-local NodeIdentity and operational state;
- local replica records/materialized state;
- shared-replicated records as permitted;
- frontiers/checkpoints/reconciliation metadata;
- no database-file-as-sync-authority.

### OPTIONAL_RESOURCES
- local models;
- inference runtimes;
- rebuildable indexes/caches;
- optional UI/media resources.

Optional resources are not required for seed identity or bootstrap validity.

### RECOVERY
- integrity manifests;
- component/schema versions;
- last validated checkpoints/frontiers;
- rollback metadata;
- migration provenance.

## Micro-LIVE minimum bootstrap sequence
1. Start bounded bootstrap runtime.
2. Locate Core through carrier/platform configuration, not a globally fixed path.
3. Verify Core manifest/integrity and logical VK identity before use.
4. Load existing local NodeIdentity or create/persist a new one according to node-enrollment rules.
5. Run bounded read-only host inspection.
6. Construct NodeCapability and NodeState.
7. Determine which local VK components are compatible with observed capabilities.
8. Discover configured/permitted inference providers/runtimes/models without installing or downloading them.
9. Initialize local persistence/compatibility adapters without changing canonical-memory admission authority.
10. If compatible connectivity and peer configuration exist, make distributed protocol participation available; transport remains a separate adapter.
11. Expose bounded local operation/status even when no peer or large-model inference is available.

## No-large-LLM bootstrap invariant
Micro-LIVE MUST NOT require a large LLM to start, verify Core, establish NodeIdentity, inspect the host, report capabilities, initialize persistence, validate protocol compatibility or report degraded/offline state.

Inference may be:
- local optional resource carried with the seed;
- already installed on the host;
- provided by another reachable VK node;
- provided by another permitted inference service;
- unavailable.

If unavailable, Micro-LIVE remains a valid bounded VK bootstrap/control/status instance. It must report inference as unavailable/unknown rather than fail identity/bootstrap.

## Core protection boundary
Micro-LIVE may read/verify Core and invoke existing authorized admission interfaces. It MUST NOT silently rewrite identity/personality, promote candidate memory, replace provenance, infer a new logical identity from host hardware, or make node-local capability state canonical VK identity.

NodeIdentity is separate from Core identity. Reinstall/clone/migration rules must prevent accidental duplicate active node IDs; exact enrollment/recovery procedure is a later contract.

## Portability boundary
The logical seed manifest identifies component roles and compatibility, not OS-specific absolute paths. Platform adapters may have host-specific packaging/layout. Distributed wire semantics, Core identity semantics, NodeCapability semantics and protected admission authority remain unchanged across implementations.

## Degraded modes
At minimum:
- CORE_VERIFIED_NO_INFERENCE: identity/core/status/inspection/local persistence maintenance available; conversational inference unavailable.
- LOCAL_INFERENCE: bounded local assistant using discovered permitted provider.
- REMOTE_INFERENCE: assistant may use a permitted reachable provider while Core/state authority remains local according to policy.
- OFFLINE_NODE: local capabilities/state continue; distributed exchange deferred.
- INSPECTION_DEGRADED: bootstrap continues with UNKNOWN/DEGRADED capability fields where safe.

These are capability modes, not changes to VK identity.

## NOT VERIFIED / unresolved
- Portable Seed packaging format and physical filesystem layout.
- Cross-platform launcher technology; no language is mandated by architecture.
- NodeIdentity enrollment/recovery/clone-detection procedure.
- Core manifest portability across current Windows layout and future layouts.
- Minimum local UI technology.
- Exact persistence store for the portable replica layer.
- Current Pi deployment/runtime and how existing Pi assets migrate into this model.
- Android packaging/permission model.
- Whether optional models are carried on the first SSD and which models fit available resources.
