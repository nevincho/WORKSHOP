# CANONICAL BACKLOG DECISION — 2026-08-24

STATUS: ACTIVE
AUTHORITY: VLAD / CONTROL ROOM

## Purpose
Prevent duplicate implementation, task-ID collisions, wasted Codex capacity, and deadlock on missing prerequisites while preserving all useful planning/evidence produced on 2026-08-24.

## Rule
Existing task files are retained as historical/planning evidence unless explicitly superseded below. Agents MUST use this decision when selecting work. A task listed as SUPERSEDED must not be implemented or sent to Codex.

## Verified completed prerequisites
- TASK-003 — PASS / reviewed.
- TASK-004 — PASS / reviewed.
- TASK-013 — PASS / reviewed.
- TASK-021 — PASS / reviewed.

## Mysticarium canonical chain
1. TASK-033 — Mysticarium Test Harness Bootstrap — READY. Build the missing minimal repository-side deterministic test harness/execution route. No Codex auto-execution; no Pi4 deployment.
2. TASK-022 — Mysticarium Test Route Verification — BLOCKED on TASK-033 PASS. Re-run verification against the newly established harness/route.
3. TASK-014 — Deterministic Engine — BLOCKED on TASK-022 PASS.
4. TASK-015 — Djalma Pipeline — BLOCKED on TASK-014 PASS.
5. TASK-016 — Morrigan Pipeline — BLOCKED on TASK-015 PASS.
6. TASK-017 — Selene Pipeline — BLOCKED on TASK-016 PASS.
7. TASK-018 — Al-Hakim Pipeline — BLOCKED on TASK-017 PASS.
8. TASK-019 — Session / Privacy Layer — BLOCKED on TASK-018 PASS.
9. TASK-020 — Oracle Gateway Scaffold — BLOCKED on TASK-019 PASS.
10. TASK-012 — End-to-End Chain — FINAL integration/validation candidate after the canonical component chain is complete and runtime prerequisites are satisfied.
11. TASK-011 — Pi4 Implementation Reconciliation — remains a separate runtime-dependent prerequisite; do not infer Pi4 state from repository-only work.

### Mysticarium superseded duplicates
The later duplicate planning series TASK-023 through TASK-027 for reader/session work is SUPERSEDED by canonical TASK-016 through TASK-020 where objectives overlap. Preserve files/evidence for provenance; do not execute duplicate implementation.

## VK canonical chain
Verified foundation: TASK-021 PASS.

1. TASK-034 — VK Repository Test / Checkpoint Foundation — READY. Establish the missing bounded repository-side test/checkpoint/rollback route using mocks/fixtures only; no live Windows deployment and no Codex auto-execution.
2. TASK-007 — Home Node Layer — BLOCKED on TASK-034 PASS and review that the route is sufficient.
3. TASK-028 — Device Registry — BLOCKED on node-layer/interface prerequisite.
4. TASK-032 — Capability Discovery — BLOCKED on required node/registry prerequisite and verified test route.
5. TASK-029 — Capability Health Model — BLOCKED on capability discovery/registry contract.
6. TASK-010 — Home Network Discovery — BLOCKED on shared node/registry foundation.
7. TASK-008 — IMOU Integration — BLOCKED on shared node/device layer; direct LAN evidence already exists under evidence/TASK-008/ but stream/auth/frame remain NOT VERIFIED.
8. TASK-030 — IMOU Adapter Tests — BLOCKED on TASK-008 implementation and executable repository validation route.
9. TASK-031 — Echo Voice Contract — BLOCKED on shared node/device/audio capability foundation.
10. TASK-009 — Echo 5 Voice/Audio Integration — BLOCKED on TASK-031 and verified device/runtime capability.
11. VK backup/integrity/rollback work remains required before live deployment; any duplicate-ID legacy task for this objective must be renumbered before activation.

### VK duplicate preparation tasks
Later repo-prep tasks that duplicate TASK-007 through TASK-010 objectives are planning/support artifacts, not parallel implementation authority. Agents must reconcile useful acceptance criteria into the canonical task before execution rather than implement both.

## Global implementation gate
Repository-side implementation may proceed when the selected task is explicitly READY and has a bounded simulated/repository validation method plus independent review. Live runtime deployment remains human-gated and is not required for daytime repository preparation.

## Codex rule
Codex execution is HUMAN-GATED. Agents and controller MUST NOT invoke Codex automatically. Codex Gate may only prepare a minimal handoff and mark a task READY_FOR_CODEX_REVIEW for Vlad when agent-only completion is technically insufficient.

## Controller behavior
Process existing canonical READY tasks in priority order. TASK-033 and TASK-034 are explicitly authorized unblock tasks and MUST be preferred over repeating blocker audits. After a task receives independent PASS, immediately recompute dependencies and continue with the next eligible non-duplicate task in the SAME controller run when safe. Stop only on a real blocker, human gate, protected/destructive operation, unavailable simulation/repository validation route, or no eligible work. Do not create additional task IDs merely to restate a known blocker.
