# WORKSHOP-COMM-APP-01 — Windows-first Desktop V1 Product Design

TASK_ID: WORKSHOP-COMM-APP-01
PROJECT: WORKSHOP COMMERCIAL EDITION
PRIORITY: HIGH
STATUS: REVIEW
OBJECTIVE: produce implementation-ready architectural specification for installable local-first Windows Desktop V1 using canonical WORKSHOP model without application implementation.
SOURCE_PLAN_OR_REQUEST: Owner-directed commercial design campaign, 2026-10-24.
CURRENT_STATE: PORT-01 synthetic contract is COMPLETE on isolated branch, reviewed implementation 0d248fad2aa48ce28d073b489447a63a08bae207, independent review e0861b3b0de1bbfddc16645cdf36ab06f1e10ba4. Real account portability NOT VERIFIED.
PREREQUISITES: README, AGENTS, policies, schemas, registry, controller staging and PORT-01 reviewed evidence.
DEPENDENCIES: Desktop implementation must await owner authorization after design review; no live platform integration proven.
AFFECTED_COMPONENTS: this document and planning/WORKSHOP_COMM_DESKTOP_V1_SPEC.md only.
PROTECTED_COMPONENTS: WORKSHOP main/canonical policies/state machine, current scheduler and controllers, Python simulator/test files, project runtimes and TANGRA.
EXECUTION_CLASS: WORKER
CODEX_ALLOWED: NO
IMPLEMENTATION_ALLOWED: NO
ACCEPTANCE_CRITERIA: design addresses UX, component reuse/gaps, execution/security isolation, identity/gates, cost/provider bounds, local-first technology tradeoffs, packaging, minimum release acceptance and explicit non-goals.
VALIDATION_METHOD: source-evidence trace and architectural consistency review; no build/test/security claim or live account simulation.
PRE_CHANGE_CHECKPOINT: 3d01055514e8a7bdfee880fee2ea8847f31832b9
ROLLBACK_METHOD: revert this task and the companion planning document on isolated branch; no main changes.
EVIDENCE_PATHS: planning/WORKSHOP_COMM_DESKTOP_V1_SPEC.md
REVIEW_GATE: Independent design review NOT VERIFIED. REVIEW state must not be promoted to COMPLETE without separate review.
