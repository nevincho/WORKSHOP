# CONTROL ROOM CHECKPOINT — 2026-08-26

STATUS: CURRENT CHAT HANDOFF / READ FIRST IN NEW CONTROL ROOM CHAT
AUTHORITATIVE COORDINATION REPO: `nevincho/WORKSHOP@main`

## How the next ChatGPT Control Room should start
The next chat MUST NOT rely on conversation history as project state.

First read, in this order:
1. `control_room/CONTROL_ROOM_CHECKPOINT_2026-08-26.md` (this file)
2. `status/WORKSHOP_STATE.yaml`
3. latest ~20 commits in `nevincho/WORKSHOP`
4. relevant task/evidence/review files for any task under discussion
5. authoritative target repository/ref for the specific project before making implementation/state claims

If this checkpoint conflicts with newer repository evidence, the repository wins.

## Operating model
Vlad uses ChatGPT as Control Room / engineering coordinator and quality controller.

WORKSHOP roles currently configured:
1. Scout & Planner
2. Worker
3. Independent Reviewer
4. Codex Gate

Proposed future roles (IDEAS ONLY; not yet activated):
5. Codex Task Engineer — precision/minimal Codex task packages
6. Test & Validation Engineer — challenges whether tests actually prove acceptance criteria
7. Repository Hygiene / Context Engineer — compacts completed task documentation and minimizes token/context cost
8. System Integration Auditor — milestone-level cross-component/interface review

Canonical rule: repository-side work is autonomous when authorized. LAN/Windows/Pi4/physical-device execution is not available to repository-only agents and remains Codex/human-gated according to current policy.

## Documentation policy
Repository must represent current working state, not a narrative archive.

`policies/REPORTING_POLICY.md` now requires aggressive compaction when a task reaches final validation or Codex gate:
- retain authoritative task/current state;
- retain one consolidated report when needed;
- retain only genuinely required machine/evidence artifacts;
- retain rollback/checkpoint references;
- delete obsolete intermediate Worker/Reviewer/planning/status variants;
- do not move clutter into archive/old/legacy/backup/superseded/recovery folders merely to preserve it;
- rely on Git history for deleted tracked narrative history.

Codex must not be used for repository audits, inventory, general documentation reading, task decomposition, mechanical file work, log summaries or evidence collection where WORKSHOP agents can do it.

## Current project lines
### VK
Repositories:
- canonical design/docs: `nevincho/TANGRA-DOCS`, ref `family-guardian-ai`
- implementation/UI: `nevincho/LIVE`, ref `Legacy`
- actual Windows runtime: `D:\Store\AI`

Protected components include VK Core/canonical personality/approved memory-promotion behavior.

Important completed/progress state:
- TASK-010 bounded home-network discovery was implemented/reviewed PASS earlier; controlled LAN evidence exists.
- IMOU camera exact model: `IPC-K7CP-3H1WE`.
- Local RTSP `subtype=1` was previously physically verified in VLC.
- Latest TASK-008 repository evidence (2026-08-26) records Codex implementation/runtime integration at LIVE commit `840f94abb18f10c87798c2e4a54796dd6dab2bc2`, rollback `cf911176be543393f1a05e578b4ea30d70f010bb`.
- TASK-008 `CODEX_RUN.md` reports real live IMOU frame decode on the actual `D:\Store\AI` runtime: subtype=1 PASS, real 640x480 uint8 frame, existing `PerceptionIngress` candidate event PASS, canonical memory count unchanged, credentials redacted/unset after execution, full SOURCE_V09 tests 67/67 PASS.
- TASK-008 evidence currently says `IMPLEMENTED / REAL LIVE VALIDATION COMPLETED / REVIEW PENDING`; do NOT call TASK-008 final PASS unless an independent reviewer file/state update exists after this checkpoint.
- Safety/device credential must NEVER be committed to GitHub or repeated in repository documentation.

VK future capability ideas were recorded in the VK canonical repository as idea-only / do-not-implement-yet. They include local filesystem stewardship, Work-style tasks, scheduler, typed tool registry, repository operations, device/camera/audio capabilities, local model routing, deterministic orchestration and permission gates. They require separate future analysis.

### Mysticarium / Horoscopes
Canonical repo/ref:
- `nevincho/TANGRA-DOCS`, ref `agent/mysticarium`, path `projects/mysticarium/`

Repository-side chain TASK-014 through TASK-020 reached PASS/reviewed and exact reviewed artifacts were later deployed/tested on Pi4 (WORKSHOP state records 43/43 tested).

TASK-011 Pi4 reconciliation is PASS.

Current important blocker in WORKSHOP state:
- TASK-012 production five-reader chain is NOT complete.
- Reviewed source/runtime lacks a verified production five-reader orchestrator/API/output route and production Selene/Al-Hakim/bones knowledge inputs.
- Do not claim the full website chain is integrated until repository/runtime evidence demonstrates it.

### ESP32 MicroBlog / Agent 32
Independent commercial funding track; technically independent from TANGRA/VK/Horoscopes. Business purpose: produce a sale-ready software product whose revenue can fund other project lines.

Documentation:
- `nevincho/nova`, branch `esp32-microblog-agent32`, path `ESP32_MICROBLOG/`
- local authoritative implementation/build state: `D:\RaspberryPi5\ЕСП32_БЛОГ`

Known product state:
- v0.6.1 previously physically working baseline
- v0.7 lean source/runtime NOT VERIFIED until current toolchain compile/physical validation
- previous minimal Wi-Fi compile stall was evidence of environment/toolchain problem; do not modify v0.7 source merely because of the historical stall without a new compile demonstrating a source defect
- offline release candidate first; Connected Mode/Web Search must not block offline sale-ready release

WORKSHOP staged backlog exists TASK-045 onward.
- TASK-045 repository reconciliation PASS/reviewed
- TASK-046 is the next compile-only Windows diagnostic gate; no source edit and no flash are authorized by that task
- TASK-047 exact untouched v0.7 compile follows only after TASK-046 evidence permits it
- later stages cover physical upload/smoke, AGENT 32 regression, stress, reproducible binary, Windows installer/customer package, customer-flow acceptance and offline release review; Connected Mode/Web Search are post-offline-RC work

### TANGRA
`nevincho/TANGRA-DOCS` is authoritative for repository state.

Current WORKSHOP state holds TANGRA offline from autonomous runtime work because physical rebuild/new chassis/camera integration is in progress. Do not restart Pi5/TANGRA runtime work from stale chat context.

A separate future test idea exists: after the camera cassette is physically ready, run a camera-only daylight characterization/calibration experiment independent of the production TANGRA stack, measuring resolutions/distances/calibration behavior; HQ focus stays at infinity and WIDE is script-adjustable where supported. This is a future physical-test planning item, not current autonomous execution authorization.

## AI_COMPANY
Actual system currently local at `F:\AI_COMPANY` and has not yet been faithfully onboarded into a dedicated GitHub repository.

Existing architecture brief supplied by Vlad:
- deterministic Python controller owns workflow/stage transitions/budgets/retries/validation/persistence/audit/approvals/termination
- AI roles: Research, Analysis, Independent Reviewer, Local Utility Worker
- SQLite runtime/project state, append-only audit, SHA-256 content-addressed artifacts, Git for source/docs/policies
- model store external at `D:\Store\AI\models`
- LOCAL_FAST Qwen3-1.7B; LOCAL_STRONG Qwen3.5-4B
- £0 operating-cost rule; no paid fallback
- Founder is final decision maker
- current infrastructure/controller pipeline has functioned to Founder Decision Gate
- 1.7B is known inadequate for serious engineering reasoning; use primarily Utility/fast tier
- 4B serious Research/Analysis/Reviewer quality is NOT VERIFIED pending controlled known-answer evaluation

TASK-058 exists for evening/local repository onboarding:
1. inspect actual `F:\AI_COMPANY` files/Git/config/tests first
2. identify secrets/SQLite runtime/caches/private artifacts/model references that must not be committed
3. establish correct repository boundary/.gitignore
4. only then create/select GitHub repository/ref and commit faithful source/docs/policies/tests
5. record exact commit/ref in WORKSHOP
6. only after onboarding define WORKSHOP <-> AI_COMPANY job/artifact interface

Do NOT reconstruct or redesign AI_COMPANY from chat summaries before inspecting local state.

### AI_COMPANY Deep Research Department idea
Preserved at:
`planning/AI_COMPANY_DEEP_RESEARCH_DEPARTMENT_IDEA.md`

Status: IDEA / DO NOT IMPLEMENT YET.

Concept: long-running (potentially hours) deterministic multi-agent research department for hard engineering questions. Proposed conceptual roles include Research Director/Problem Framer, Requirements Analyst, Technology Scout, Product/Primary-Source Researcher, Evidence Curator, Systems Engineer, Simulation/Experiment Engineer, Adversarial Reviewer and Decision Synthesizer.

Key principle:
`LLM hypothesis/research -> deterministic experiment specification -> Python/simulator/dataset execution -> raw measurements/statistics -> LLM interpretation -> independent critique`

LLMs must not invent simulation results.

Example use case: evaluate TANGRA camera candidates using manufacturer specs + authoritative TANGRA constraints + controlled synthetic/recorded scenes + common distance/altitude/illumination/motion/noise/compression sweeps + detector/tracker/range metrics, then compare detection/miss/confidence/tracking/latency/range error/bandwidth/power/mass/integration/cost.

## ChatGPT local-work experiment planned
A separate exploration concerns ChatGPT (NOT Codex) Plus capabilities for local computer file manipulation.

Planned safe evening test: use ChatGPT Desktop/Work with an isolated folder such as `D:\CHATGPT_WORK_TEST`, not production project folders initially.

Test progressively:
1. read file
2. create file
3. edit file
4. create directory
5. rename/move
6. delete test file
7. determine folder-boundary behavior
8. determine Git repository support
9. determine whether any Python/PowerShell/shell execution exists
10. determine localhost/LAN access only if explicitly supported and safely bounded

Important NOT VERIFIED questions:
- whether Plus Windows ChatGPT Work has shell/PowerShell execution versus file/project operations only
- whether cloud Scheduled Tasks can trigger or interact with a local Work session

Do not assume these capabilities exist until physically tested on Vlad's machine.

Potential architecture if useful capabilities are verified: one ChatGPT Control Room chat coordinates GitHub/WORKSHOP plus permitted local Work folders and AI_COMPANY, while Codex remains a scarce precision implementation/runtime resource for tasks that genuinely require it.

## WORKSHOP autonomous scheduling/reporting
Controller is external automation with hourly minimum schedule. Repository agents process independent repository-safe READY_FOR_WORKER tasks, then stop at human/runtime/Codex gates.

Requested report cadence remains 8/12/24 hours; do not generate repetitive narrative clutter when state has not materially changed.

## Immediate next actions for new Control Room
Do not execute these blindly; first refresh repo state/recent commits because some may have changed after this checkpoint.

1. Refresh TASK-008 reviewer/state after the live RTSP evidence. If independent review has passed, reconcile canonical WORKSHOP state and then determine next VK dependency task.
2. Inspect current TASK-046 ESP32 gate and decide with Vlad when to run the bounded Windows compile diagnostic.
3. Inspect Mysticarium TASK-012 current repository/runtime state before preparing any further Codex deployment; repository production chain prerequisites must exist first.
4. When Vlad is at the PC, perform TASK-058 AI_COMPANY local onboarding.
5. When convenient, perform isolated ChatGPT Work local capability audit.
6. Only after AI_COMPANY onboarding/evaluation should Research Department v2 or extra agent roles be designed/activated.
7. Consider cleaning repeated controller fallback/heartbeat telemetry under the new repository-hygiene policy; do not delete evidence required for current acceptance/history without classification.

## Security and coordination rules
- Never store IMOU Safety Code/password or other secrets in GitHub.
- Repo evidence beats chat/memory.
- Never claim runtime/device validation without actual evidence.
- Preserve validated components and rollback paths.
- Smallest justified change only; no opportunistic refactors.
- If Codex correctly performs a bad/duplicated/unnecessary task authored by Control Room, classify as coordination failure, not implementation failure.
- Keep Codex token usage strict and minimal.
