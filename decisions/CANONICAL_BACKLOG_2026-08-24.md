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
- TASK-007 — PASS / reviewed; shared Home Node/device abstraction verified at LIVE commit `c4f524cac0054e400a1fb2cb6049697f8971fba3`; live Windows behavior NOT VERIFIED.
- TASK-028 — PASS / reviewed; bounded in-memory registry implemented and repository-tested.
- TASK-032 — PASS / reviewed; provider-neutral normalized capability discovery layer implemented and repository-tested; live host probing NOT VERIFIED.
- TASK-029 — PASS / reviewed; non-Core device capability/health model implemented and repository-tested; live health state NOT VERIFIED.
- TASK-010 — PASS / reviewed; bounded authorized LAN discovery implemented at LIVE commit `cf911176be543393f1a05e578b4ea30d70f010bb`, controlled `192.168.0.0/24` execution evidenced, known inventory compared; IMOU protocol capability/stream ingestion remains NOT VERIFIED.

## Current Human Codex / Runtime Gates
- TASK-014 — Mysticarium Deterministic Engine — READY_FOR_CODEX_REVIEW; handoff baseline `beebf9884e450cc29f4d0bbae3d89a27a0fc41c0`; requires task-specific Vlad approval before Codex execution.
- TASK-008 — VK IMOU Camera Integration — dependency TASK-010 is now PASS. Re-gating is required against current LIVE state and direct IMOU RTSP evidence. Any live camera integration/credentialed stream test remains HUMAN-GATED and must not be executed automatically.

## TASK-007 / TASK-028 / TASK-041 ownership lock
This boundary is canonical and overrides older broader wording:
- TASK-041 — PASS — owns registry schema/contract/fixtures only.
- TASK-007 — PASS — owns only the shared Home Node/device base abstraction and device-agnostic adapter-facing interface; it reuses TASK-041 semantics.
- TASK-028 — PASS — owns runtime/in-memory registry service behavior and add/update/remove/get/list operations.

TASK-007 MUST NOT implement registry service operations. TASK-028 MUST NOT redefine TASK-041 schema or create a second device abstraction.

## Independent Daytime Package — COMPLETE / REVIEWED
TASK-035 through TASK-044 are PASS/reviewed repository/simulation preparation. Their PASS does not establish live runtime behavior.

## Mysticarium implementation chain
TASK-014 -> TASK-015 -> TASK-016 -> TASK-017 -> TASK-018 -> TASK-019 -> TASK-020 -> TASK-012. TASK-011 remains runtime-dependent. Later duplicate planning series TASK-023 through TASK-027 is SUPERSEDED where it overlaps TASK-016 through TASK-020.

## VK implementation chain
TASK-007 PASS -> TASK-028 PASS -> TASK-032 PASS -> TASK-029 PASS -> TASK-010 PASS -> TASK-008 -> TASK-030 -> TASK-031 -> TASK-009.

TASK-008 may now be re-gated. Its operational PASS still requires live camera connection/read evidence against the actual device; repository-only evidence is insufficient.

## Global implementation gate
Repository-side preparation may proceed when a task is explicitly READY and has bounded repository/simulation validation plus independent review. Live runtime deployment remains human-gated.

## Codex rule
Codex execution is HUMAN-GATED. Agents/controller MUST NOT invoke Codex automatically. Codex Gate may prepare a minimal handoff and mark READY_FOR_CODEX_REVIEW only when agent-only completion is technically insufficient.

## Controller behavior
Process all independent READY tasks before declaring HUMAN_GATE_BLOCKED. After independent PASS, recompute dependencies and continue in the same run when safe. A Human Codex Gate on one chain MUST NOT block independent READY tasks on another chain or preparation layer. Do not create new task IDs merely to restate blockers.
