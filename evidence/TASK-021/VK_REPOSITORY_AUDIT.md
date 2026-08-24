# TASK-021 — VK Repository Implementation Audit

ROLE: WORKSHOP SCOUT / PLANNER
DATE: 2026-08-24
STATUS: REVIEWABLE

## Objective actually tested
Repository-only implementation-state reconciliation for VK using:
- design/canonical repository: `nevincho/TANGRA-DOCS`, branch `family-guardian-ai`, path `family_guardian_ai/`;
- implementation/UI repository: `nevincho/LIVE`, branch `Legacy`, path `family_guardian_ai/`.

No claim is made about the current `D:\Store\AI` Windows runtime. No local runtime, Core, canonical personality, memory promotion, deployment, or TANGRA state was modified or inspected.

## Repository evidence inspected

### Canonical/design side — TANGRA-DOCS
- `VK_CANONICAL_FOUNDATION_2026-08-21.md`
- `ROADMAP.md`
- `SOURCE_V09/` recursive repository tree

### LIVE Legacy side
- `VK_V09_CURRENT_STATE_CHECKPOINT_2026-08-21.md`
- `VK_CORE_MIGRATION_CHECKPOINT_2026-08-23.md`
- `SOURCE_V09/README.md`
- `SOURCE_V09/config/capabilities.json`
- `SOURCE_V09/app/perception_ingress.py`
- `SOURCE_V09/app/camera_adapter.py`
- `SOURCE_V09/app/vision_adapter.py`
- `SOURCE_V09/app/cognitive_activation.py`
- `SOURCE_V09/app/vk_runtime.py`
- `SOURCE_V09/web/index.html`
- recursive `family_guardian_ai/` tree on Legacy

## Repository relationship / source-state finding

The two repositories are not identical implementation snapshots.

`nevincho/TANGRA-DOCS:family-guardian-ai/family_guardian_ai/SOURCE_V09` contains a substantial v0.9 source snapshot including chat, memory, inference, context routing, indexing, perception ingress and tests.

`nevincho/LIVE:Legacy/family_guardian_ai/SOURCE_V09` contains a richer/newer repository snapshot with additional implementation artifacts, including `camera_adapter.py`, `vision_adapter.py`, `cognitive_activation.py`, `core_access.py`, `remote_work_gateway.py`, `vk_runtime.py`, `vk_web_server.py`, capability/privacy/settings configuration, additional tests, active web UI, and workshop/model-lab code.

This divergence must not be interpreted as proof of the live Windows runtime state. LIVE Legacy is repository implementation evidence only; `D:\Store\AI` remains NOT VERIFIED in this task.

## Capability map

| Capability area | Repository classification | Evidence-backed conclusion |
|---|---|---|
| Chat / Free Talk | IMPLEMENTED IN REPOSITORY | `vk_runtime.py` contains conversation orchestration and inference integration; active web UI exposes Chat. Runtime operation in current Windows environment is NOT VERIFIED here. |
| Memory review / admission | IMPLEMENTED / PARTIAL | Web UI contains Memory candidate table/actions; repository contains memory DB/admission modules and explicit no-auto-promotion perception boundary. Protected canonical memory semantics must remain unchanged. Current live DB/schema is NOT VERIFIED. |
| System / Capability Status | IMPLEMENTED / PARTIAL | UI exposes Settings/runtime/model status; `capabilities.json` defines a capability registry; `vk_runtime.py` exposes runtime capability provider logic. Canonical host-wide discovery requirements are broader than the static registry/current probes. |
| Capability discovery | PARTIAL | Camera and vision can probe their own availability; shared roots and inference/model state have status paths. No repository evidence was found for a complete canonical discovery layer covering CPU, GPU, RAM, storage, network, display, audio, microphone, sensors, Bluetooth/Wi-Fi/LAN and tool inventory as one normalized host capability contract. |
| Sensor/input ingestion | IMPLEMENTED FOUNDATION | `PerceptionIngress` provides a shared in-memory `PERCEPTION_OBSERVATION` event contract with source, type, timestamp, confidence, significance, provenance and raw reference; it explicitly does not auto-promote canonical memory. |
| Vision / camera | IMPLEMENTED FOUNDATION / DEVICE-LIMITED | `CameraAdapter` supports explicit local camera probe/capture; `VisionAdapter` supports local TFLite/MediaPipe or OpenCV HOG fallback; `vk_runtime.py` integrates camera/vision with shared perception. Physical live-camera validation is NOT VERIFIED by this repository audit. |
| Nodes / device abstraction | DESIGN-ONLY / NOT IMPLEMENTED AS SHARED LAYER | Active UI explicitly labels Nodes `NOT IMPLEMENTED`; no evidence in inspected repository establishes the shared node/device registry/interface required by current canonical architecture and WORKSHOP TASK-007/TASK-025. Existing camera code is device-specific capability code, not proof of a general node layer. |
| Home-network discovery | NOT VERIFIED / NOT IMPLEMENTED AS CANONICAL LAYER | No evidence from inspected source establishes bounded LAN device discovery/status normalization. Do not infer this from camera support or shared-folder capability code. |
| Audio / microphone / voice | DESIGN-ONLY / NOT VERIFIED | Canonical roadmap/foundation describes future audio/voice capability, but inspected repository source did not establish a microphone/audio adapter or a device-neutral STT/TTS I/O capability layer. Echo-specific access is NOT VERIFIED. |
| Associations | PARTIAL IMPLEMENTATION | `CognitiveActivation` explicitly recognizes association activity, routes it, activates related concepts and constrains one-word responses. `vk_runtime.py` contains association-specific handling. This does not by itself prove the full canonical Association Game v0.1 methodology/T0 evidence lifecycle is complete in current runtime. |
| Backup / integrity / rollback | PARTIAL DOCUMENTATION / NOT VERIFIED AS GENERAL MECHANISM | Checkpoint documents preserve migration/rollback coordination state and refer to rollback requirements. No inspected repository evidence establishes a complete general repository-side backup-manifest, integrity and restore mechanism for mutable non-Core VK components. |
| UI shell | IMPLEMENTED IN REPOSITORY | Legacy `web/index.html` implements VK-branded Chat, Workspace, Memory, Sensors and Settings; Nodes and Tasks are explicitly disabled/later. |
| Core materialization | PREPARED / NOT LIVE PROMOTED PER REPOSITORY CHECKPOINT | Core migration checkpoint explicitly records isolated preparation and says live materialization/promotion/rollback package were not completed. This is coordination evidence, not current runtime proof. |

## Phase assessment

Repository evidence places VK beyond the earlier documentation-only/bootstrap stage. The implementation repository has a working-source structure with chat/inference/memory/context/perception/vision/UI foundations and tests.

However the canonical distributed capability/node/device architecture is incomplete in repository scope, and the current local Windows runtime remains outside this task's evidence boundary.

Best repository-only phase classification:

`VK v0.9 — IMPLEMENTATION FOUNDATION PRESENT / CAPABILITY-NODE EXPANSION INCOMPLETE / LIVE RUNTIME NOT VERIFIED`

## Stale naming and compatibility debt

Canonical identity authority explicitly states current project identity is `VK` and user-facing `Virtual Vladimir` / `VV` terminology is retired except for historical/compatibility lineage.

Repository evidence still contains historical names such as:
- `VIRTUAL_VLADIMIR_V08.md`;
- `START_VIRTUAL_VLADIMIR.bat`;
- `ARCHITECTURE/VV_INTERFACE_AND_DISTRIBUTED_RUNTIME_PLAN.md`;
- predecessor DB/file naming referenced by checkpoints.

The active Legacy UI is already VK-branded. Historical files must not be blindly renamed or deleted because rollback/dependency significance is not fully verified. Classification: compatibility/stale naming debt, not justification for broad cleanup.

## Duplication / contradiction findings

### 1. Divergent SOURCE_V09 snapshots
The canonical-design repository and LIVE repository both carry `SOURCE_V09`, but the trees differ. Treating both as a single synchronized implementation source would be incorrect.

Smallest coordination correction: future repository implementation work should identify one explicit target implementation repository/ref per task and treat the other copy as design/archive/reference unless a synchronization policy is independently defined.

### 2. Camera-specific implementation exists before shared node/device abstraction
Camera/vision foundations exist while the canonical shared node/device layer remains absent. Do not respond by creating another camera-specific registry. Later device integration should converge through one shared node/capability/status/input interface.

### 3. Static capability registry is narrower than canonical capability discovery
`capabilities.json` is a useful policy/status registry, but it does not satisfy the canonical requirement for actual host capability discovery across compute, storage, network, display/audio, sensors and tools. TASK-022 remains justified if Reviewer confirms this audit.

### 4. Checkpoint claims are not current runtime proof
Repository checkpoint documents contain historical isolated/live-test reports. Under WORKSHOP validation policy they are evidence of recorded prior validation only, not proof of the current Windows runtime state. This audit does not upgrade those reports into current runtime claims.

## Missing prerequisites / actual blockers

For repository-only work:
- GitHub read/write access is available.
- Current repository code-execution/test capability is NOT VERIFIED in this Scout execution context. Presence of Python tests does not prove they can be executed here against a safe checkout.

For live/runtime work:
- `D:\Store\AI` current filesystem/process/runtime state: NOT VERIFIED.
- live checkpoint/rollback route: NOT VERIFIED.
- device/network/audio hardware paths: NOT VERIFIED except separate WORKSHOP evidence where explicitly recorded.

Therefore repository implementation tasks that require executable unit/mock tests must not be promoted solely because source write access exists.

## Protected components

Do not modify without explicit authorization:
- VK Core;
- canonical personality state;
- approved-memory promotion/admission semantics;
- provenance semantics.

Existing validated interfaces and rollback lineage must be preserved.

## Smallest safe repository-only implementation sequence

Subject to independent TASK-021 review and verification of a safe test execution route:

1. Complete a normalized repository-side capability-discovery contract around existing status/probe mechanisms rather than replacing them. This corresponds to TASK-022.
2. Add/verify repository-side backup/integrity/rollback baseline for mutable non-Core components before broader device integration. This corresponds to TASK-023.
3. Add bounded repository-only home-network discovery scaffold reusing capability primitives, with no live LAN claims. TASK-024.
4. Establish the shared non-Core node/device abstraction before additional device-specific adapters. TASK-025.
5. Attach IMOU preparation through that shared layer using existing verified LAN evidence only. TASK-026.
6. Add provider/device-neutral audio capability seam before any Echo-specific integration assumptions. TASK-027.
7. Live TASK-007/TASK-008/TASK-009/TASK-010 remain separate runtime validation phases and must not be conflated with repository preparation.

## Dependency decision

TASK-021 Scout objective is satisfied and evidence is reviewable.

TASK-022 remains BLOCKED until:
- TASK-021 independent Reviewer PASS; and
- a safe code-execution/test route sufficient for its required mock/fixture validation is independently verified.

Repository write capability alone is insufficient validation evidence.

## Scout conclusion

SCOUT / PLANNER RESULT: COMPLETE FOR TASK-021 PREPARATION/AUDIT STAGE.

FINAL TASK-021 VERDICT: NOT VERIFIED — independent Reviewer required.

No target repository modification was performed. No Windows runtime claim was made. No Codex was invoked.
