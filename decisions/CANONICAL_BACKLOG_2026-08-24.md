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

## Current Human Codex Gates
- TASK-014 — Mysticarium Deterministic Engine — READY_FOR_CODEX_REVIEW; do not invoke Codex without Vlad approval.
- TASK-007 — VK Home Node Layer — READY_FOR_CODEX_REVIEW; do not invoke Codex without Vlad approval.

Downstream implementation chains remain blocked on these gates, but independent daytime preparation below MUST continue.

## Independent Daytime Package — READY_FOR_WORKER
These tasks are intentionally independent of TASK-014/TASK-007 implementation and are safe repository/simulation preparation. Controller should process them instead of repeatedly rechecking the Human Codex Gates.

### Mysticarium
1. TASK-035 — Knowledge Fragment Schema — READY_FOR_WORKER.
2. TASK-036 — Presentation Metadata Contract — READY_FOR_WORKER.
3. TASK-037 — Ephemeral Session TTL Contract — READY_FOR_WORKER.
4. TASK-038 — Temporary Media Lifecycle Contract — READY_FOR_WORKER.
5. TASK-039 — Reader Fixture Corpus — READY_FOR_WORKER.

### VK
6. TASK-040 — Sensor/Event Envelope + Provenance Contract — READY_FOR_WORKER.
7. TASK-041 — Device Registry Contract + Fixtures — READY_FOR_WORKER; supports later TASK-028, does not implement it.
8. TASK-042 — Capability Discovery Fixture Corpus — READY_FOR_WORKER; supports later TASK-032, does not implement host probing.
9. TASK-043 — Network Discovery Fixture Corpus — READY_FOR_WORKER; supports later TASK-010, no live LAN scanning.
10. TASK-044 — Backup / Integrity Manifest + Restore Simulation — READY_FOR_WORKER; no live Core backup.

## Mysticarium implementation chain
TASK-014 -> TASK-015 -> TASK-016 -> TASK-017 -> TASK-018 -> TASK-019 -> TASK-020 -> TASK-012. TASK-011 remains runtime-dependent. Later duplicate planning series TASK-023 through TASK-027 is SUPERSEDED where it overlaps TASK-016 through TASK-020.

## VK implementation chain
TASK-007 -> TASK-028 -> TASK-032 -> TASK-029 -> TASK-010 -> TASK-008 -> TASK-030 -> TASK-031 -> TASK-009. Later repo-prep duplicates are support artifacts only; do not implement duplicate objectives.

## Global implementation gate
Repository-side preparation may proceed when a task is explicitly READY and has bounded repository/simulation validation plus independent review. Live runtime deployment remains human-gated.

## Codex rule
Codex execution is HUMAN-GATED. Agents/controller MUST NOT invoke Codex automatically. Codex Gate may prepare a minimal handoff and mark READY_FOR_CODEX_REVIEW only when agent-only completion is technically insufficient.

## Controller behavior
Process all independent READY tasks before declaring HUMAN_GATE_BLOCKED. After independent PASS, recompute dependencies and continue in the same run when safe. A Human Codex Gate on one chain MUST NOT block independent READY tasks on another chain or preparation layer. Do not create new task IDs merely to restate blockers.
