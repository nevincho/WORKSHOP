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
- TASK-035 — PASS / reviewed; Mysticarium knowledge-fragment schema/fixtures established.
- TASK-036 — PASS / reviewed; Mysticarium presentation metadata contract established.
- TASK-037 — PASS / reviewed; Mysticarium ephemeral-session TTL contract established.
- TASK-038 — PASS / reviewed; Mysticarium temporary-media lifecycle contract established.
- TASK-039 — PASS / reviewed; Mysticarium four-reader fixture corpus established.
- TASK-040 — PASS / reviewed; VK shared sensor/event envelope + provenance contract established.
- TASK-041 — PASS / reviewed; VK device-registry contract/fixtures established for later TASK-028.
- TASK-042 — PASS / reviewed; VK capability-discovery fixture corpus established for later TASK-032.
- TASK-043 — PASS / reviewed; VK sanitized network-discovery fixture corpus established for later TASK-010.
- TASK-044 — PASS / reviewed; VK backup/integrity manifest + restore simulation established; live Core backup NOT VERIFIED.

## Current Human Codex Gates
- TASK-014 — Mysticarium Deterministic Engine — READY_FOR_CODEX_REVIEW; do not invoke Codex without Vlad approval.
- TASK-007 — VK Home Node Layer — READY_FOR_CODEX_REVIEW; do not invoke Codex without Vlad approval.

Downstream implementation chains remain blocked on these gates.

## Independent Daytime Package — COMPLETE / REVIEWED
These tasks were intentionally independent of TASK-014/TASK-007 implementation and were completed with bounded repository/simulation validation. Their PASS does not establish live runtime behavior.

### Mysticarium
1. TASK-035 — Knowledge Fragment Schema — PASS / reviewed.
2. TASK-036 — Presentation Metadata Contract — PASS / reviewed.
3. TASK-037 — Ephemeral Session TTL Contract — PASS / reviewed.
4. TASK-038 — Temporary Media Lifecycle Contract — PASS / reviewed.
5. TASK-039 — Reader Fixture Corpus — PASS / reviewed.

### VK
6. TASK-040 — Sensor/Event Envelope + Provenance Contract — PASS / reviewed.
7. TASK-041 — Device Registry Contract + Fixtures — PASS / reviewed; supports later TASK-028, does not implement it.
8. TASK-042 — Capability Discovery Fixture Corpus — PASS / reviewed; supports later TASK-032, does not implement host probing.
9. TASK-043 — Network Discovery Fixture Corpus — PASS / reviewed; supports later TASK-010, no live LAN scanning.
10. TASK-044 — Backup / Integrity Manifest + Restore Simulation — PASS / reviewed; no live Core backup was performed.

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
