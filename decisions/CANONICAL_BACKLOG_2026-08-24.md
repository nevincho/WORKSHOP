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
- TASK-010 — PASS / reviewed; bounded authorized LAN discovery implemented at LIVE commit `cf911176be543393f1a05e578b4ea30d70f010bb`, controlled `192.168.0.0/24` execution evidenced; IMOU protocol capability/stream ingestion remains NOT VERIFIED.
- TASK-014 — PASS / reviewed; deterministic core verified at `f4adb7c43ccf0aaa710bb1b03069ad5c5aff38cf`; repository tests PASS; Pi4/runtime NOT VERIFIED.
- TASK-015 — PASS / reviewed; Djalma tarot repository pipeline verified at `4792b406d5ba1e440a8709c3aeca60aefa00a403`; runtime/content depth NOT VERIFIED.
- TASK-016 — PASS / reviewed; Morrigan runes/bones repository pipeline verified at `16acfbc9788981067c12bb1c0ec1e41ce27e982b`; runtime/content depth NOT VERIFIED.
- TASK-017 — PASS / reviewed; Selene structured repository pipeline verified at `c5a62fbbde73d085b56a2338f08883b907a98018`; runtime/content depth NOT VERIFIED.
- TASK-018 — PASS / reviewed; Al-Hakim structured interpretation pipeline verified at `39f84019d161231e30efc3f3c92bb1a59104013e`; astronomical calculation/runtime NOT VERIFIED.
- TASK-019 — PASS / reviewed; ephemeral session/privacy and temporary-media repository layer verified at `4f5a63dc6680783d010bd92d730220470d0b0d2a`; live filesystem/provider behavior NOT VERIFIED.
- TASK-020 — PASS / reviewed; provider-neutral Oracle gateway scaffold verified at `c088aa064f468e4b6c2ce074bba3a91647330b4f`; external provider/payment/runtime NOT VERIFIED.

## Current Human Codex / Runtime Gates
- TASK-008 — VK IMOU Camera Integration — READY_FOR_CODEX_REVIEW. Live credentialed RTSP integration remains HUMAN-GATED; current authorized device availability/runtime read is NOT VERIFIED.
- TASK-046 — ESP32 Minimal Wi-Fi Toolchain Diagnostic — READY_FOR_CODEX_REVIEW. Compile-only Windows diagnostic requires task-specific Vlad approval; no source edits or flash are authorized.
- TASK-011 — Mysticarium Pi4 Implementation Reconciliation — BLOCKED on direct Pi4 read-only/runtime evidence. It is discovery/audit work and does not justify Codex coding; repository-only evidence cannot satisfy it.
- TASK-058 — AI_COMPANY Repository Onboarding — HUMAN_LOCAL_ACTION_REQUIRED; authoritative local project tree/state is NOT VERIFIED from GitHub.

## TASK-007 / TASK-028 / TASK-041 ownership lock
This boundary is canonical and overrides older broader wording:
- TASK-041 — PASS — owns registry schema/contract/fixtures only.
- TASK-007 — PASS — owns only the shared Home Node/device base abstraction and device-agnostic adapter-facing interface; it reuses TASK-041 semantics.
- TASK-028 — PASS — owns runtime/in-memory registry service behavior and add/update/remove/get/list operations.

TASK-007 MUST NOT implement registry service operations. TASK-028 MUST NOT redefine TASK-041 schema or create a second device abstraction.

## Independent Daytime Package — COMPLETE / REVIEWED
TASK-035 through TASK-044 are PASS/reviewed repository/simulation preparation. Their PASS does not establish live runtime behavior.

## Mysticarium implementation chain
TASK-014 PASS -> TASK-015 PASS -> TASK-016 PASS -> TASK-017 PASS -> TASK-018 PASS -> TASK-019 PASS -> TASK-020 PASS -> TASK-012.

TASK-012 remains BLOCKED because its acceptance explicitly requires TASK-011 PASS plus Pi4 end-to-end runtime validation. TASK-011 remains runtime-dependent. Later duplicate planning series TASK-023 through TASK-027 is SUPERSEDED where it overlaps TASK-016 through TASK-020.

## VK implementation chain
TASK-007 PASS -> TASK-028 PASS -> TASK-032 PASS -> TASK-029 PASS -> TASK-010 PASS -> TASK-008 -> TASK-030 -> TASK-031 -> TASK-009.

TASK-008 is re-gated and READY_FOR_CODEX_REVIEW. Its operational PASS still requires live camera connection/read evidence against the actual device; repository-only evidence is insufficient.

## Global implementation gate
Repository-side preparation may proceed when a task is explicitly READY and has bounded repository/simulation validation plus independent review. Live runtime deployment remains human-gated.

## Codex rule
Codex execution is HUMAN-GATED. Agents/controller MUST NOT invoke Codex automatically. Codex Gate may prepare a minimal handoff and mark READY_FOR_CODEX_REVIEW only when agent-only completion is technically insufficient.

## Controller behavior
Process all independent READY tasks before declaring HUMAN_GATE_BLOCKED. After independent PASS, recompute dependencies and continue in the same run when safe. A Human Codex Gate on one chain MUST NOT block independent READY tasks on another chain or preparation layer. Do not create new task IDs merely to restate blockers.
