# WORKSHOP-COMM-G1-QUALIFICATION-01 — Windows G1 acceptance evidence closure

TASK_ID: WORKSHOP-COMM-G1-QUALIFICATION-01
PROJECT: WORKSHOP Commercial Edition Desktop V1
PRIORITY: HIGH
STATUS: IN_PROGRESS
OBJECTIVE: Qualify the existing G1 implementation at exact frozen commit d5369ec0300fe836dc673dbe9e8f5ea1ccdb5c23 by obtaining independently auditable genuine Windows filesystem and GUI execution evidence; change no G1 implementation unless testing proves a specific defect.
SOURCE_PLAN_OR_REQUEST: Owner-directed end-to-end WORKSHOP Desktop V1 campaign, with WORKSHOP internal role routing and minimum human involvement; planning/WORKSHOP_COMM_DESKTOP_V1_SPEC.md and planning/WORKSHOP_COMM_G1_READINESS_CONTRACT.md.
CURRENT_STATE: Bounded fenced-Markdown parser contract defect demonstrated by run 41136200148 and repaired in core.py/tests only; current Windows Server 2022 CI run 41136583397 shows 28/28 unit PASS + 6/6 NTFS fixtures PASS, fenced negative PASS, GUI entrypoint smoke PASS, no skips. Independent Reviewer and customer Windows GUI acceptance remain NOT VERIFIED. G1 COMPLETE NOT VERIFIED.
PREREQUISITES: Verify exact frozen repository state, code and G1 contract; check Windows host, Python, filesystem, test/harness availability and safe temporary fixture paths before execution; read prior G1 review and evidence.
DEPENDENCIES: NONE — G1 implementation already available; this task is the immediate acceptance prerequisite of G2.
AFFECTED_COMPONENTS: apps/workshop_g1/ Windows G1 test and qualification artifacts; bounded source repair in apps/workshop_g1/workshop_g1/core.py and regression tests in apps/workshop_g1/tests/test_g1.py only, authorized by demonstrated contract failure at Actions run 41136200148.
PROTECTED_COMPONENTS: main branch, all G1 source outside the two explicitly permitted parser repair files, trusted schemas/manifest, existing workspaces, .git contents, production paths, TANGRA, unrelated repositories.
EXECUTION_CLASS: WORKER
CODEX_ALLOWED: GATE_REQUIRED
ACCEPTANCE_CRITERIA: Actual Windows 10 NTFS test results bound to exact commit, clean launch and reproducible suite; authentic raw stdout/stderr, command exit codes and environment; per-case negative filesystem evidence for junction, file-symlink or documented equivalent, root-swap and CREATE rollback; OPEN/IMPORT before-after content hashes and filesystem metadata including .git; independent Reviewer validates the evidence and code together against G1 canonical acceptance. If symlink fixture unavailable, record SKIP and a specific capability blocker, not PASS. No false claim of independently run tests. Upon evidence-based PASS, write qualified G1 checkpoint before G2 authorization.
VALIDATION_METHOD: WORKSHOP routes Worker evidence acquisition first; Windows host operations via cheapest verified capable executor, with Codex only via policy gate. Compare raw evidence/hashes against source/fixture requirements; independent reviewer assesses coverage, threats and limitations. Tests that don't observe Windows NTFS behavior cannot qualify those acceptance objectives.
PRE_CHANGE_CHECKPOINT: windows@d5369ec0300fe836dc673dbe9e8f5ea1ccdb5c23; after evidenced parser contract failure, only the two bounded parser/test repair files above may change; record repair commit and revert path.
ROLLBACK_METHOD: Evidence-only task: remove/revert only newly created candidate evidence after preserving reviewed material; never modify user workspace. Any bounded code repair requires a distinct commit checkpoint and rollback plan.
EVIDENCE_PATHS: evidence/WORKSHOP-COMM-G1-WINDOWS-QUALIFICATION-01/WORKER.md; review/WORKSHOP-COMM-G1-WINDOWS-QUALIFICATION-01.md; review/WORKSHOP-COMM-G1-WINDOWS-QUALIFICATION-01.md; checkpoints/WORKSHOP-COMM-G1-01.md (only after PASS).

## WORKSHOP service-boundary handoff
- Control Room supplies this one objective; WORKSHOP routes Worker, required Codex Gate and independent Reviewer internally under its existing policies.
- Do not ask owner to act as courier between agents.
- No G2/G3/G4/G5/G6/G7 development until the G1 acceptance prerequisite is satisfied; then accept current task and define one next bounded integration task, preserving the reviewed Desktop V1 spec. Owner's ultimate target remains integrated, installable, sale-candidate Desktop V1 through G7, not G1 Markdown viewing.
- This task file establishes authorization/scope only; it DOES NOT constitute evidence that a Worker started or a Windows test executed.

STOP: WORKSHOP returns PASS with independently reviewed Windows evidence and checkpoint, or BLOCKED with the exact external execution prerequisite, or REWORK with a demonstrated defect; do not invent completion.

## Authorized bounded REWORK (2026-10-30)
GitHub Actions run 41136200148 demonstrates that fenced Markdown example containing TASK_ID is misclassified as executable task candidate. Control Room authorizes Worker to implement only deterministic fence exclusion in document_kind and parse_task with focused regressions, without changing trusted schema, manifest, other G1 behavior or unrelated paths. After tests, return to REVIEW; G1 COMPLETE remains unverified pending independent acceptance.
