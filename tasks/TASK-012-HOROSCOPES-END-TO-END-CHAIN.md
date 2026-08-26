# TASK-012 — Horoscopes End-to-End Five-Reader Chain

TASK_ID: TASK-012
PROJECT: HOROSCOPES / MYSTICARIUM
PRIORITY: HIGH
STATUS: BLOCKED
OBJECTIVE: Build the complete production five-reader orchestration/API/output chain in the authoritative repository first, validate and review it there, then prepare ONE consolidated Codex Pi4 deployment/live-validation handoff.
SOURCE_PLAN_OR_REQUEST: canonical Mysticarium plan + verified TASK-011 Pi4 reconciliation + Vlad instruction that repository-ready work must be implemented directly into the real project, with Codex reserved for integration/deployment/live validation.
CURRENT_STATE: TASK-011 PASS and independently reviewed. Reviewed components from TASK-014 through TASK-020 are deployed and tested on Pi4, but the live website still exposes only the existing Djalma production API. The canonical repository still has no production five-reader orchestrator/service/API/output route and, critically, no authoritative production Selene/Al-Hakim/bones-Morrigan knowledge corpus with explicit provenance; existing reader data are test fixtures only.
PREREQUISITES: TASK-011 PASS is satisfied; exact Pi4 runtime route is verified. Production knowledge/input authority must be satisfied before repository production glue is created.
DEPENDENCIES: TASK-011 PASS satisfied; reuse TASK-014 through TASK-020 reviewed components without rewriting them.
AFFECTED_COMPONENTS: authoritative Mysticarium repository only until final deployment gate; production orchestration/service/API/output routing; production knowledge inputs proven necessary for Selene, Al-Hakim and bones/Morrigan paths; integration tests.
PROTECTED_COMPONENTS: existing validated Djalma behavior, existing Pi4 web/backend/data/services, user data, visual/UI canon, unrelated Pi4 applications, reviewed TASK-014 through TASK-020 behavior.
EXECUTION_CLASS: WORKER_THEN_REVIEW_THEN_CODEX_DEPLOYMENT
CODEX_ALLOWED: DEPLOYMENT_GATE_ONLY by default. Repository coding by Codex requires explicit evidence that authorized WORKSHOP workers cannot complete a required implementation step.

BLOCKER: `blockers/TASK-012-PRODUCTION-KNOWLEDGE.md`
UNBLOCK_CONDITION: Canonically identify/commit reviewed production knowledge sources for Selene, Al-Hakim and Morrigan/bones with explicit provenance/licensing/ownership and usable production format; confirm they are not test fixtures or duplicate production content.

REPOSITORY-SIDE REQUIRED WORK AFTER UNBLOCK:
1. Define and implement the smallest production five-reader orchestration contract using existing reviewed reader components.
2. Define and implement the production API/output route needed by the current website/backend without creating a parallel architecture.
3. Integrate only the approved production knowledge/input artifacts required for Selene, Al-Hakim and bones/Morrigan operation; provenance and format must remain explicit.
4. Preserve existing Djalma behavior and interfaces unless a verified integration requirement demands a minimal compatible change.
5. Add deterministic component and end-to-end repository tests proving the five-reader chain, failure handling and output routing.
6. Independent Reviewer must verify code, interfaces, methodology, protected components and acceptance criteria.
7. Only after repository PASS, Codex Gate prepares ONE consolidated Pi4 handoff that deploys the reviewed package into `/home/pi/mysticarium`, wires it to the actual website/backend, performs live browser/API validation, and preserves rollback.

ACCEPTANCE_CRITERIA:
- all five canonical reader roles participate according to reviewed canonical design;
- shared input/normalization/orchestration/output path is production-capable, not mock-only;
- production API/output route exists and is covered by tests;
- required production knowledge inputs for Selene, Al-Hakim and bones/Morrigan exist and are traceable;
- existing Djalma behavior is preserved;
- repository tests prove component and end-to-end behavior before deployment;
- final Codex deployment proves the live Pi4 website/API uses the reviewed chain;
- subjective reading quality remains a separate human validation item and must not be inferred from technical tests;
- no unrelated refactor or duplicate Mysticarium implementation.

VALIDATION_METHOD: repository unit/component/integration tests + Independent Reviewer first; then ONE Codex Pi4 integration/deployment/live HTTP/API/browser validation; evening human product-quality review as needed.
PRE_CHANGE_CHECKPOINT: repository rollback commit required before repository implementation; Pi4 checkpoint required before final deployment.
ROLLBACK_METHOD: revert repository implementation commit(s) and/or restore verified Pi4 checkpoint while preserving pre-existing service/config/data state.
EVIDENCE_PATHS: `evidence/TASK-012/SCOUT.md`, `blockers/TASK-012-PRODUCTION-KNOWLEDGE.md`, later `evidence/TASK-012/`, `review/TASK-012.md` after implementation.

CODEX BUDGET RULE: Do not spend another Codex run merely to inspect, copy tests, deploy mock/scaffold-only artifacts, or invent missing production content. Next Codex use for TASK-012 should normally occur only after the production repository package is independently reviewed and ready to change the real user-visible Pi4 system.
