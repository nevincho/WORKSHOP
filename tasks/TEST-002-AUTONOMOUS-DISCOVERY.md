# TEST-002 — Autonomous Repository Discovery

STATUS: READY
TYPE: NON-DESTRUCTIVE AUTONOMY DIAGNOSTIC
PROJECT: WORKSHOP
PRIORITY: HIGH
CODEX: FORBIDDEN
TARGET PROJECT MODIFICATION: FORBIDDEN
HUMAN CHAT TRIGGER: FORBIDDEN

## Objective
Verify that the WORKSHOP Controller can discover and process a repository-only task autonomously from WORKSHOP state, without Vlad manually triggering the four agent chats.

The Controller must identify the registered/detectable TANGRA, VK, and Horoscopes project repositories and/or execution paths using repository evidence only, verify accessible source repositories, locate a canonical plan, TODO, roadmap, or equivalent planning artifact where evidence supports it, and persist an evidence-backed inventory plus independent review in WORKSHOP.

## Required Controller behaviour

1. Discover this task from the WORKSHOP task queue/state without a manual chat command.
2. Read all applicable WORKSHOP policies before acting.
3. Identify TANGRA, VK, and Horoscopes from repository-visible evidence. Do not use conversation memory as authoritative project state.
4. For each project, determine and record only what can be established from evidence:
   - project identifier;
   - repository name and URL/path, if established;
   - branch/ref, if established;
   - execution/runtime path, if established from repository evidence;
   - repository accessibility/readability;
   - canonical plan/TODO/roadmap or equivalent artifact, if found;
   - source evidence used for each claim.
5. Use `NOT VERIFIED` for any item that cannot be established from current evidence.
6. Do not modify TANGRA, VK, Horoscopes, or any other target project repository/runtime.
7. Do not invoke Codex.
8. Persist all substantive findings in WORKSHOP. Minimum expected task evidence:
   - `evidence/TEST-002/INVENTORY.md`
   - role-specific evidence as required by current WORKSHOP policy/role architecture, where applicable.
9. Independent Reviewer must evaluate whether the stated autonomy objective was actually tested and whether the evidence supports the result.
10. Persist final independent review in `review/TEST-002.md` using one of: `PASS`, `REWORK`, `BLOCKED`, `NOT VERIFIED`.

## Evidence quality requirements

- Repository state is authoritative.
- Another agent report is not sufficient proof when direct repository evidence is available.
- Do not infer inaccessible or missing repositories from memory or assumptions.
- Do not treat an unverified local runtime path as repository evidence.
- Do not claim that autonomous discovery succeeded merely because this task file exists; success requires evidence that the Controller discovered and processed it without a human chat trigger.
- Where the validation method cannot distinguish autonomous discovery from externally triggered execution, Reviewer must return `NOT VERIFIED` or `REWORK`, not PASS.

## Acceptance criteria

1. This task is discovered by the WORKSHOP Controller without Vlad sending `PROCESS WORKSHOP QUEUE` or equivalent commands to the four agent chats.
2. TANGRA, VK, and Horoscopes are inventoried from repository evidence only.
3. Accessible source repositories are directly verified where possible.
4. Canonical plan/TODO/roadmap artifacts are identified only where supported by evidence.
5. Unknowns are explicitly marked `NOT VERIFIED`.
6. No target-project repository/runtime is modified.
7. Codex is not used.
8. Substantive output is persisted in WORKSHOP.
9. Independent Reviewer verifies the actual test objective and methodology rather than merely checking artifact presence.

## Completion
TEST-002 is complete only when repository evidence exists for the autonomous Controller processing path, `evidence/TEST-002/INVENTORY.md` exists, and `review/TEST-002.md` contains an independent verdict based on current evidence.
