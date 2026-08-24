# CANONICAL BACKLOG DECISION — 2026-08-24

STATUS: ACTIVE
AUTHORITY: VLAD / CONTROL ROOM

## Purpose
Prevent duplicate implementation, task-ID collisions, and wasted Codex capacity while preserving all useful planning/evidence produced on 2026-08-24.

## Rule
Existing task files are retained as historical/planning evidence unless explicitly superseded below. Agents MUST use this decision when selecting work. A task listed as SUPERSEDED must not be implemented or sent to Codex.

## Verified completed prerequisites
- TASK-003 — PASS / reviewed.
- TASK-004 — PASS / reviewed.
- TASK-013 — PASS / reviewed.
- TASK-021 — PASS / reviewed.

## Mysticarium canonical chain
1. TASK-022 — Mysticarium Test Route Verification — ACTIVE BLOCKER / first eligible prerequisite once the missing bounded validation route/harness is established.
2. TASK-014 — Deterministic Engine — BLOCKED on TASK-022 PASS.
3. TASK-015 — Djalma Pipeline — BLOCKED on TASK-014 PASS.
4. TASK-016 — Morrigan Pipeline — BLOCKED on TASK-015 PASS.
5. TASK-017 — Selene Pipeline — BLOCKED on TASK-016 PASS.
6. TASK-018 — Al-Hakim Pipeline — BLOCKED on TASK-017 PASS.
7. TASK-019 — Session / Privacy Layer — BLOCKED on TASK-018 PASS.
8. TASK-020 — Oracle Gateway Scaffold — BLOCKED on TASK-019 PASS.
9. TASK-012 — End-to-End Chain — FINAL integration/validation candidate after the canonical component chain is complete and runtime prerequisites are satisfied.
10. TASK-011 — Pi4 Implementation Reconciliation — remains a separate runtime-dependent prerequisite; do not infer Pi4 state from repository-only work.

### Mysticarium superseded duplicates
The later duplicate planning series TASK-023 through TASK-027 for reader/session work is SUPERSEDED by canonical TASK-016 through TASK-020 where objectives overlap. Preserve files/evidence for provenance; do not execute duplicate implementation.

## VK canonical chain
Verified foundation: TASK-021 PASS.

Use the original architecture-oriented series as canonical where it defines the implementation objective:
1. TASK-007 — Home Node Layer — BLOCKED until repository execution/test/checkpoint route required by policy is proven.
2. TASK-028 — Device Registry — BLOCKED on node-layer/interface prerequisite.
3. TASK-032 — Capability Discovery — BLOCKED on required node/registry prerequisite and verified test route.
4. TASK-029 — Capability Health Model — BLOCKED on capability discovery/registry contract.
5. TASK-010 — Home Network Discovery — BLOCKED on shared node/registry foundation.
6. TASK-008 — IMOU Integration — BLOCKED on shared node/device layer; direct LAN evidence already exists under evidence/TASK-008/ but stream/auth/frame remain NOT VERIFIED.
7. TASK-030 — IMOU Adapter Tests — BLOCKED on TASK-008 implementation and executable repository validation route.
8. TASK-031 — Echo Voice Contract — BLOCKED on shared node/device/audio capability foundation.
9. TASK-009 — Echo 5 Voice/Audio Integration — BLOCKED on TASK-031 and verified device/runtime capability.
10. VK backup/integrity/rollback work remains required before live deployment; any duplicate-ID legacy task for this objective must be renumbered before activation.

### VK duplicate preparation tasks
Later repo-prep tasks that duplicate TASK-007 through TASK-010 objectives are planning/support artifacts, not parallel implementation authority. Agents must reconcile useful acceptance criteria into the canonical task before execution rather than implement both.

## Global implementation gate
TASK-005 remains the general controlled-implementation gate. Repository-only implementation may proceed only when the selected task has a verified bounded execution/test route, valid checkpoint/rollback method where changes occur, and independent review path. Live runtime deployment requires its own verified runtime route and human/protected-operation policy compliance.

## Controller behavior
After a task receives independent PASS, immediately recompute dependencies and continue with the next eligible non-duplicate task in the SAME controller run when safe. Stop only on a real blocker, human gate, protected/destructive operation, unavailable validation route, Codex gate decision requiring unavailable capacity, or no eligible work. Do not wait for the next hourly trigger merely because one task completed early.

## Codex conservation
Do not use Codex for discovery, inventory, duplicate reconciliation, file movement, evidence summarization, routine test invocation, or work already implemented. Codex is reserved for justified precision implementation/debugging after Scout/Worker preparation and Codex Gate approval.
