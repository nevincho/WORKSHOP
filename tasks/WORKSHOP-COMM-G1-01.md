# WORKSHOP-COMM-G1-01 — First Windows Read-Only Workspace Browser

TASK_ID: WORKSHOP-COMM-G1-01
PROJECT: WORKSHOP COMMERCIAL EDITION
PRIORITY: HIGH
STATUS: BLOCKED
EXECUTION_CLASS: WORKER
CODEX_ALLOWED: NO
OBJECTIVE: Implement only a minimal Windows-first local read-only workspace/task browser with separately confirmed CREATE scaffolding, verified bundled policy/schema snapshot, and deterministic inert parser diagnostics.
SOURCE_PLAN_OR_REQUEST: owner-directed G1 PRE-01 readiness closure; not yet implementation authorization.
CURRENT_STATE: Local prototype produced, 14/15 local tests passed (one Windows-specific skipped), source NOT repository-persisted, independent review NOT VERIFIED; see evidence/WORKSHOP-COMM-G1-01.md. COMM-APP-01 independent CONDITIONAL PASS at a2ec5b3c16c4b21548ce1570bcac20d6276b2b7a; PORT-01 independently reviewed synthetic-only. No Desktop app/source implemented. G1 trusted-source, workspace and parser contract in planning/WORKSHOP_COMM_G1_READINESS_CONTRACT.md.
PREREQUISITES: owner explicitly approves first G1 implementation; verify current branch/ref, reviewed contract, and protected scope immediately before coding.
DEPENDENCIES: verified bundled trust manifest/fixture; no GitHub credentials/execution requirements.
AFFECTED_COMPONENTS: future new isolated application source/tests and app-owned fixture outputs only, paths to be designated and checked before implementation. This task file is documentation, not write authorization.
PROTECTED_COMPONENTS: WORKSHOP canonical policies, schemas, status, existing controller/staging, PORT-01 simulation, production, all target repositories and TANGRA.
ACCEPTANCE_CRITERIA: all G1 acceptance bullets in planning/WORKSHOP_COMM_G1_READINESS_CONTRACT.md, including offline manifest hash pin, CREATE-only authorized scaffold, OPEN/IMPORT no writes, inert parser diagnostics, malformed/malicious/path fixtures, Windows reparse escape rejection, no token/network/hook/executor, independently demonstrated zero mutation.
VALIDATION_METHOD: a single bounded test suite for parser/trust guards plus independent Windows filesystem observation comparing pre/post snapshots across CREATE/OPEN/IMPORT and adversarial fixtures; reproduce full command/output/test identity; no simulation-only PASS for Windows-specific enforcement.
PRE_CHANGE_CHECKPOINT: a2ec5b3c16c4b21548ce1570bcac20d6276b2b7a (design review reference); confirm actual implementation baseline at authorization.
ROLLBACK_METHOD: isolate on dedicated future implementation branch; revert/delete only newly created application files; never touch main/existing customer repo; check before/after tree identity.
EVIDENCE_PATHS: future task-local evidence, independent review and checkpoint in canonical WORKSHOP directories only after execution authorization.
NON_GOALS: no AI executor, controller state changes, scheduler, GitHub API/credentials, installer/packaging, network, repository mutation, approvals/reviews of engineering implementation, G2-G7, Codex, Work, paid API.
STOP: no implementation until owner authorization; after first independently reviewed G1 gate return to owner.

BLOCKER: Repository-persisted runnable G1 implementation, Windows reparse/path acceptance, cross-document references and independent Reviewer all NOT VERIFIED.
SMALLEST_UNBLOCK: Persist exact local source artifact with hash verification; complete missing contract acceptance in a separate bounded authorization; real Windows validation and independent review.
