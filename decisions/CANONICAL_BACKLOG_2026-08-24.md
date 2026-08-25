# CANONICAL BACKLOG DECISION — 2026-08-24

STATUS: ACTIVE
AUTHORITY: VLAD / CONTROL ROOM

## Purpose
Prevent duplicate implementation, task-ID collisions, wasted Codex capacity, and deadlock on missing prerequisites while preserving useful planning/evidence.

## Rule
Existing task files are retained as historical/planning evidence unless explicitly superseded. Tasks marked SUPERSEDED must not be implemented or sent to Codex.

## Verified completed prerequisites
- TASK-003 — PASS / reviewed.
- TASK-004 — PASS / reviewed.
- TASK-013 — PASS / reviewed.
- TASK-021 — PASS / reviewed.
- TASK-033 — PASS / reviewed; Mysticarium repository-side harness established.
- TASK-022 — PASS / reviewed; provenance-preserving repository-to-executor test route verified.
- TASK-034 — PASS / reviewed; VK repository-side mock test/checkpoint foundation established.
- TASK-035 through TASK-039 — PASS / reviewed; Mysticarium independent preparation complete.
- TASK-040 through TASK-044 — PASS / reviewed; VK independent preparation complete.

## Current Human Codex Gates
- TASK-014 — Mysticarium Deterministic Engine — READY_FOR_CODEX_REVIEW; handoff baseline refreshed and scope remains narrow.
- TASK-007 — VK Home Node Abstraction — READY_FOR_CODEX_REVIEW after scope reconciliation; verified LIVE Legacy baseline `078a534b6f0241507349f182626d308f2c0ff284`.

## TASK-007 / TASK-028 / TASK-041 ownership lock
This boundary is canonical and overrides older broader wording:
- TASK-041 — PASS — owns registry schema/contract/fixtures only.
- TASK-007 — READY_FOR_CODEX_REVIEW — owns only the shared Home Node/device base abstraction and device-agnostic adapter-facing interface; it must reuse TASK-041 semantics.
- TASK-028 — BLOCKED on TASK-007 PASS + TASK-041 PASS — sole owner of runtime/in-memory registry service behavior and add/update/remove/query/list operations.

TASK-007 MUST NOT implement registry service operations. TASK-028 MUST NOT redefine TASK-041 schema or create a second device abstraction.

## Independent Daytime Package — COMPLETE / REVIEWED
TASK-035 through TASK-044 are PASS/reviewed repository/simulation preparation. Their PASS does not establish live runtime behavior.

## Mysticarium implementation chain
TASK-014 -> TASK-015 -> TASK-016 -> TASK-017 -> TASK-018 -> TASK-019 -> TASK-020 -> TASK-012. TASK-011 remains runtime-dependent. Later duplicate planning series TASK-023 through TASK-027 is SUPERSEDED where it overlaps TASK-016 through TASK-020.

## VK implementation chain
TASK-007 -> TASK-028 -> TASK-032 -> TASK-029 -> TASK-010 -> TASK-008 -> TASK-030 -> TASK-031 -> TASK-009.

## Global implementation gate
Repository-side preparation may proceed when a task is explicitly READY and has bounded repository/simulation validation plus independent review. Live runtime deployment remains human-gated.

## Codex rule
Codex execution is HUMAN-GATED. Agents/controller MUST NOT invoke Codex automatically. Codex Gate may prepare a minimal handoff and mark READY_FOR_CODEX_REVIEW only when agent-only completion is technically insufficient.

## Controller behavior
Process all independent READY tasks before declaring HUMAN_GATE_BLOCKED. After independent PASS, recompute dependencies and continue in the same run when safe. A Human Codex Gate on one chain MUST NOT block independent READY tasks on another chain or preparation layer. Do not create new task IDs merely to restate blockers.
