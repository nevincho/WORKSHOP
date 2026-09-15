# VK Universal NodeCapability / NodeState / Host Inspector Architecture

Date: 2026-09-15
Status: ARCHITECTURE CONTRACT — IMPLEMENTATION NOT STARTED

## Boundary
`NodeIdentity` answers **which VK node is this?**
`NodeCapability` answers **what functions/resources can this node provide?**
`NodeState` answers **what is their current observed condition/availability?**

Node type labels such as Windows PC, Raspberry Pi or Android never confer capabilities. Capabilities arise only from configured evidence plus bounded observation.

Distributed synchronization remains separate: it determines what VK state may be exchanged/reconciled. Capability discovery determines what a local node can currently do. Future routing may consume both, but scheduling/routing is outside this task.

## Language-independent NodeCapability contract
Minimum semantic fields:
- `capability_id`: stable protocol identifier for a capability kind;
- `category`: OS, compute, memory, storage, accelerator, inference, model, camera, microphone, audio_output, network, service, hardware_interface, thermal, power, or extensible namespaced category;
- `status`: `AVAILABLE | UNAVAILABLE | UNKNOWN | DEGRADED`;
- `attributes`: schema-defined portable primitive values only;
- `source`: typed observation/configuration source identifier;
- `observed_at`: optional non-authoritative observation time;
- `freshness`: optional validity/age metadata;
- `constraints`: bounded capability limits where safely observable;
- `evidence_state`: separate evidence quality such as VERIFIED / NOT_SUPPORTED / PERMISSION_DENIED / SOURCE_GAP when needed;
- `schema_version`.

`AVAILABLE` means evidence supports present usability within stated constraints. `UNAVAILABLE` means a valid probe establishes absence/non-usability. `UNKNOWN` means no defensible conclusion. `DEGRADED` means usable with a known material limitation. Capability status is operational state, not authority.

## NodeState contract
NodeState is dynamic NODE_LOCAL state and references the stable NodeIdentity. It may contain:
- CPU load/available execution capacity;
- available RAM;
- storage free capacity/read-only/full conditions;
- accelerator availability/load where observable;
- network interface/link/connectivity state;
- service/provider health;
- model loaded/available state;
- camera/microphone availability;
- thermal condition;
- power/battery/external-power constraints;
- bounded errors/degradation reasons;
- observation provenance/freshness.

Snapshots must never become canonical identity. Remote copies, if retained as evidence, must be explicitly labelled as remote historical observations.

## Host Inspector model
Common semantic operation:
`inspect(request) -> {node_identity_ref, capabilities[], node_state, observations[]}`

The wire/contract semantics are language-independent. Platform adapters implement allow-listed probes appropriate to their host:
- Windows implementation may use documented OS/runtime APIs and narrowly bounded read-only queries.
- Linux x86/ARM implementation may use documented kernel/filesystem APIs and bounded device/service enumeration.
- Android implementation may use permitted Android APIs and report inaccessible fields as UNKNOWN/UNAVAILABLE with evidence state.
- future adapters follow the same contract without changing NodeCapability semantics.

Inspection coverage where observable:
OS/version/architecture; CPU resources; RAM; persistent storage/free capacity; GPU; NPU/AI accelerators; inference runtimes; local models; cameras; microphones; audio output; network interfaces/connectivity; local services/endpoints; relevant hardware interfaces; thermal state; power constraints; other namespaced usable capabilities.

## Security / authority invariant
Inspection is observational and read-only by default. It MUST NOT itself install/download software or models, install drivers, mutate host configuration, start privileged hardware, expose credentials/secrets, escalate privileges, grant new authority, or expose a general shell/command execution interface.

A failed or denied probe changes evidence/status only; it does not authorize remediation.

## Canonical representation
Platform adapters emit the same logical NodeCapability/NodeState schema using the portable wire value algebra. Platform-native objects, paths, handles, pointers, registry objects, file descriptors and device objects never cross the contract boundary directly. Host-specific details may appear only in explicitly namespaced portable attributes and must not be interpreted as universal capability semantics.

## Relationship to existing HostInspector contract
This extends `VK_HOST_INSPECTOR_CONTRACT_2026-09-15.md` without invalidating its read-only boundary. Existing VERIFIED/UNAVAILABLE/NOT_SUPPORTED/PERMISSION_DENIED/SOURCE_GAP values describe evidence/probe outcome; the new AVAILABLE/UNAVAILABLE/UNKNOWN/DEGRADED values describe operational capability status. Implementations must not collapse those two dimensions.

## NOT VERIFIED
- Exact Windows, Linux/Pi and Android probe APIs remain implementation-gate decisions.
- Current Pi VK runtime/service topology remains NOT VERIFIED.
- Capability schema registry and namespacing governance are not implemented.
- Freshness thresholds are capability-specific and remain to be specified.
- No autonomous task routing/scheduling is designed here.
