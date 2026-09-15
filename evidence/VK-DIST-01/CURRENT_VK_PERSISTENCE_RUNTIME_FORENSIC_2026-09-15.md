# VK-DIST-01 — Current VK Persistence / Runtime Forensic

Date: 2026-09-15
Status: COMPLETE_WITH_RUNTIME_GAP
Mode: read-only repository forensic. No synchronization implementation, database migration or production persistence modification.

## Authoritative implementation evidence inspected
Target implementation repository: `nevincho/LIVE`, branch `Legacy`, `family_guardian_ai/SOURCE_V09/`.
WORKSHOP `projects/VK.md` states that the local runtime host/path is NOT VERIFIED and must be established from current execution evidence before modification. Therefore repository paths below are implementation evidence, not claims that a currently running PC/Pi instance uses them.

## Persistence inventory
### `app/db.py`
Current repository default root is `VK_INSTALL_ROOT` or `D:\Store\AI`; default DB is `VK_DB_PATH` or `<root>/memory/vv08.db`.
SQLite WAL schema contains:
- `memories`: durable candidate/canonical memory records with `event_id`, provenance, privacy, persona eligibility, type, source, status, importance, supersession and contradiction metadata;
- `conversations` and `conversation_sessions`: durable conversation history/session metadata;
- `conversation_attachments`: durable attachment BLOBs;
- `people`: relationship/trust/disclosure metadata;
- `shared_roots`, `repo_roots`: configured local source roots;
- `knowledge_chunks`: materialized/indexed local knowledge;
- `tool_events`: operational tool log;
- FTS tables/indexes/triggers: derived search acceleration.

Classification for later distributed work:
- `memories`: MIXED — candidate/canonical durable semantic state; eligibility for SHARED_REPLICATED must be policy/admission aware, not table-copy based.
- `conversations`, sessions, attachments: durable user history, but replication/privacy policy is not defined by current code -> NOT YET ELIGIBLE until DIST-02/03 policy contract.
- `people`: durable semantic state, protected/privacy-sensitive -> NOT YET ELIGIBLE without explicit contract.
- `shared_roots`, `repo_roots`: NODE_LOCAL because paths/authority bind to local filesystems.
- `knowledge_chunks`, FTS: DERIVED_REBUILDABLE from roots/files and must not be sync authority.
- `tool_events`: NODE_LOCAL operational evidence by default; any promotion to shared evidence must be explicit.
- SQLite DB file/WAL: runtime materialization only; forbidden as sync unit by Gate-0.

### Legacy `app/memory_core.py`
An older `vv07.db` implementation exists with `memory_events`, conversations, people, shared roots and file index. This is a legacy persistence mechanism, not evidence of current runtime selection. It must be treated as a compatibility/migration source only if current runtime evidence proves data remains authoritative/useful.

## Candidate / admission / promotion path
Repository evidence establishes:
1. `VKRuntime` accumulates conversation history and invokes `consolidator.consolidate` through its memory workflow.
2. `consolidator.py` examines user messages and emits durable memories through `db.add_memory(... status="candidate")` with `provenance="USER_STATED"`.
3. `db.list_candidates()` exposes only candidate records.
4. `VKRuntime` exposes explicit approve/reject operations; CLI `chat_vk.py` maps `/approve ID` and `/reject ID` to those methods.
5. Repository `approve_memory.py` similarly invokes explicit canonicalization in the older memory-core path.
6. `db.search_memories()` retrieves only `status='canonical'` for normal memory activation.

Conclusion: candidate creation and canonical use are separate. Gate-0 sync must not convert replicated candidate records into canonical memories. Existing explicit promotion authority is protected.

## Canonical-memory authority
The repository stores canonicality as memory status and retrieves only canonical records for memory activation. The project profile separately protects approved-memory promotion. Exact human-authentication/authorization enforcement around approve/reject is NOT VERIFIED from the inspected repository slice; this is a protected seam and must not be weakened by distributed work.

## Provenance / lineage
Verified provenance fields exist in memory rows and runtime activated-context items. Consolidator creates `USER_STATED`; runtime providers label evidence such as `RUNTIME_STATE`, `CONFIG_STATE`, `SHARED_INDEX`, `SENSOR_OBSERVATION` and `INFERENCE`.
Existing distributed causal lineage primitives (`origin_node_id`, per-node sequence, replica frontier, checkpoint, reconciliation record) were NOT found in current implementation evidence. `supersedes_event_id` and `contradiction_group` are semantic relationship fields, not a distributed causal history protocol.

## Identity storage
`app/core_access.py` implements a read-only materialized VK Core boundary rooted at `<VK_INSTALL_ROOT>/Core`, reading:
- `Core/manifest.json`;
- `Core/identity/core_identity.json`;
- `Core/persona/persona_system.md`.
It verifies `manifest.core_id == "VK"` and can fingerprint these files. This is the current repository identity read seam. It is protected canonical/Core state and must not be replaced by node identity. Distributed `NodeIdentity` must be stored separately from the logical VK Core identity.

## Runtime state and inference/provider components
`app/vk_runtime.py` is the shared runtime composition seam. It constructs `InferenceAdapter`, `PerceptionIngress`, `CameraAdapter`, `VisionAdapter`, `CognitiveActivation`, `CoreAccess` and `ModelLab`, initializes DB persistence, and holds transient session/history/pending/activity/visual state in memory.

`app/inference_adapter.py` is provider-neutral and supports local `llama_server_http` plus OpenAI-compatible cloud provider classes. Provider/model selection is configuration/runtime state, not VK identity. Cloud profiles obtain API keys from environment variables and deliberately strip local dynamic/private context. Secrets therefore remain local.

Classification:
- active session/history/pending/activity/locks/worker state: TRANSIENT;
- inference profile/provider availability/model endpoint: NODE_LOCAL;
- model weights/runtime binaries: NODE_LOCAL or DERIVED/replaceable capability assets, not identity;
- API keys and camera credentials: SECRETS;
- Core identity/persona material: protected durable VK state.

## PC deployment/runtime seams
Repository launch artifacts explicitly target Windows `D:\Store\AI`:
- `START_VK.vbs` starts `.venv\Scripts\python.exe`, `app/start_llama_server.py`, `app/start_vk_web.py`, then opens `http://127.0.0.1:8090/`.
- `start_llama_server.py` starts a configured local `llama-server.exe` and model.
- `start_vk_web.py` starts `vk_web_server.py` via `pythonw.exe`, checks `/api/status`, writes logs, and loads an IMOU password from Windows DPAPI protected `runtime/secrets/imou_password.dpapi` into process environment.

These are concrete Windows implementation seams in the repository. Current live Windows deployment/path/process state remains NOT VERIFIED because WORKSHOP has no current host-runtime evidence in this task.

## Pi deployment/runtime seams
No authoritative current Raspberry Pi VK deployment path, service unit, launcher, database location, provider configuration or process topology was established from the inspected current repository evidence. Legacy/general design documents are not accepted as runtime proof.

PI_RUNTIME = NOT VERIFIED.

This is the genuine external/runtime evidence gap for live Pi integration. It does not block architecture/contract implementation, but it blocks any claim of a safe concrete Pi production integration point or live two-node deployment.

## Existing synchronization mechanisms
No current VK record/frontier/checkpoint synchronization implementation was identified in the inspected repository implementation. No evidence was found for an existing valid PC/Pi sync protocol. This is a repository finding only; uncommitted/local mechanisms remain NOT VERIFIED.

## Exact safe integration points for later work
1. `db.py` persistence API boundary is the safest initial compatibility seam for DIST-03. Add record emission/import beside existing `add_memory`, conversation/persistence operations rather than copying `vv08.db` or rewriting schema authority in place.
2. Candidate/canonical status transitions are a protected admission seam. Distributed code may observe/record them but must not bypass explicit approval.
3. `CoreAccess` is the logical identity read boundary. Add separate node identity/replica metadata outside Core; do not mutate Core to represent host identity.
4. `VKRuntime` is the composition point for later capability registration, HostInspector and sync orchestration after their pure contracts exist. Do not put causal sync logic inside inference adapters.
5. `InferenceAdapter` remains replaceable and node-local. Sync must not depend on a specific model/provider.
6. `shared_roots`/`repo_roots` and knowledge indexes must remain node-local/rebuildable. Replicate durable source records only when separately policy-authorized; never replicate local path registries as universal state.
7. Secrets under environment/DPAPI/runtime secrets are explicitly excluded from shared synchronization.
8. Pi binding cannot be selected until current Pi runtime/deployment evidence is obtained.

## Gate conclusion
VK-DIST-01 repository forensic objective is complete for the accessible authoritative implementation repository. The current source establishes enough safe seams to begin VK-DIST-02 pure VK-native record/lineage contracts without touching production persistence.

Live runtime persistence validation is PARTIAL: Windows repository deployment seams are concrete but live process/files are NOT VERIFIED; Pi runtime/deployment is NOT VERIFIED. Therefore DIST-06/07 and any production migration remain blocked on later runtime evidence, but DIST-02 is not blocked.
