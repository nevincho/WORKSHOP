# VK Bounded Host Inspector Contract

Date: 2026-09-15
Status: CONTROL ROOM CONTRACT — IMPLEMENTATION NOT STARTED

## Purpose
Provide VK with verified, read-only knowledge of the machine on which the current node runs, without exposing unrestricted shell, PowerShell, Administrator or root authority to the LLM.

## Architectural boundary
`LLM / VK reasoning -> Capability Gateway -> HostInspector interface -> OS-specific read-only adapter -> allow-listed OS/API probes`

The LLM never supplies arbitrary executable commands. The gateway accepts typed operations only.

## Common interface
`HostInspector.snapshot(request: HostInspectionRequest) -> HostSnapshot`

Allow-listed request sections:
- `os`: OS name/version, kernel/build, architecture, hostname/node label where policy permits;
- `cpu`: model/architecture, logical/physical cores where available, bounded utilization sample;
- `memory`: total/available RAM and swap/pagefile summary;
- `accelerators`: GPU/NPU/Hailo/other accelerator inventory and bounded status where supported;
- `storage`: mounted/local volumes, capacity/free space, filesystem/type where safely available;
- `network`: interface inventory, link state, local addresses subject to policy; no packet capture;
- `devices`: cameras and USB/device inventory available through read-only enumeration;
- `vk_runtime`: VK processes/services known through explicit VK service registry or allow-listed process inspection;
- `models`: configured/discovered local model providers, model identities and availability through provider adapters.

Every field carries one of: `VERIFIED`, `UNAVAILABLE`, `NOT_SUPPORTED`, `PERMISSION_DENIED`, `SOURCE_GAP`, plus source/probe metadata and observation time.

## OS-specific implementations
- Windows adapter: typed calls using documented Windows/Python APIs and narrowly allow-listed system queries. No general PowerShell/cmd execution endpoint.
- Linux/Raspberry Pi adapter: typed calls using `/proc`, `/sys`, standard library/platform APIs and narrowly allow-listed read-only device/service probes. No general shell/root endpoint.
- Future Android/other adapters implement the same common contract and return explicit unsupported states for unavailable probes.

## Security rules
- read-only by contract;
- no arbitrary command string parameter;
- no file mutation;
- no service start/stop/restart;
- no package install/update;
- no privilege escalation;
- no credential/secret enumeration;
- no unrestricted filesystem traversal;
- bounded timeouts and output sizes;
- adapter errors fail closed for authority and fail informatively for reporting.

## Node-local semantics
Host snapshots are NODE_LOCAL operational state. They may generate durable evidence when useful, but they are not canonical VK identity and are not blindly replicated as current state to another node. A remote node may receive explicitly labelled historical/remote-reported evidence without treating it as its own host state.

## Required user-facing behavior
For the Bulgarian query `Можеш ли да ми дадеш информация за хардуера, на който работиш?`, VK invokes the local HostInspector and reports only returned verified facts, clearly marking unavailable/unsupported fields. It must not answer from generic model assumptions or claim no hardware access when the capability is available.
