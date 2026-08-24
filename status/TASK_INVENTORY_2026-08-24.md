# WORKSHOP Task Inventory — 2026-08-24

PURPOSE: Reconcile task files against available evidence, independent reviews, blockers and current coordination state. This inventory does not promote a task merely because a task file exists.

## Classification rules
- DONE+REVIEWED: task completion and independent PASS are directly evidenced.
- DONE-NOT-REVIEWED: implementation/work appears complete but required independent review is absent.
- READY-FOR-IMPLEMENTATION: prerequisites are satisfied and the task is explicitly safe/eligible to enter implementation now.
- BLOCKED: an explicit prerequisite, validation route, runtime route, dependency, or coordination defect prevents implementation/completion.
- SUPERSEDED: a later canonical task replaces the entry.
- NOT-VERIFIED: repository evidence is insufficient to assign a stronger state.

## DONE+REVIEWED
- TASK-003 — Execution Capability Audit — PASS.
- TASK-004 — Read-only Project Routing — PASS.
- TASK-013 — Mysticarium Canon Audit — PASS. Repository canon/backlog mapped; no Pi4/runtime claim.
- TASK-021 — VK Repository Implementation Audit — PASS. Repository implementation state mapped; Windows runtime remains NOT VERIFIED.

## DONE-NOT-REVIEWED
- None verified in this inventory.

## READY-FOR-IMPLEMENTATION
- None currently verified as READY.

Important: several tasks are well specified and implementation-oriented, but specification quality is not the same as execution readiness. Their declared prerequisites/validation routes remain blocked.

## BLOCKED — shared/gating chain
- TASK-005 — Controlled Implementation Candidate — blocked: no verified implementation runtime route.
- TASK-006 — First Real Implementation — blocked behind TASK-005.

## BLOCKED — VK
- TASK-007 — Home Node Layer — blocked by implementation/runtime gating.
- TASK-008 — IMOU Integration — blocked by node-layer/implementation gating. Direct LAN evidence exists separately under `evidence/TASK-008/`, but this is not implementation PASS.
- TASK-009 — Echo Show 5 Voice/Audio — blocked by node-layer/implementation gating and unverified device integration route.
- TASK-010 — Home Network Discovery — blocked by node-layer/implementation gating.
- TASK-032 — Capability Discovery Layer — canonical replacement for the former duplicate TASK-022 VK capability task; blocked pending authorization/validated repository implementation route.
- TASK-023 — VK Backup / Integrity / Rollback Baseline — blocked and also affected by duplicate numeric task identity.
- TASK-024 — VK Home Network Discovery Chain — blocked and also affected by duplicate numeric task identity.
- TASK-025 — VK Home Node Layer Repo Prep — blocked and also affected by duplicate numeric task identity.
- TASK-026 — VK IMOU Adapter Repo Prep — blocked and also affected by duplicate numeric task identity.
- TASK-027 — VK Echo5 Audio Repo Prep — blocked and also affected by duplicate numeric task identity.
- TASK-028 — VK Device Registry — blocked by upstream VK chain.
- TASK-029 — VK Capability Health Model — blocked by upstream VK chain.
- TASK-030 — VK IMOU Adapter Tests — blocked by upstream VK/adapter chain.
- TASK-031 — VK Echo Voice Contract — blocked by upstream VK/audio chain.

## BLOCKED — Mysticarium / Horoscopes
- TASK-011 — Pi4 Implementation Reconciliation — blocked on verified Pi4 read-only/runtime route. Repository-only canon audit proceeded independently as TASK-013.
- TASK-012 — End-to-End Chain — blocked on implementation/runtime prerequisites.
- TASK-014 — Deterministic Divination Engine — blocked on executable deterministic validation route; TASK-022 is its prerequisite.
- TASK-015 — Djalma Pipeline — blocked on TASK-014 PASS.
- TASK-016 — Morrigan Pipeline — blocked on TASK-015 PASS.
- TASK-017 — Selene Pipeline — blocked on TASK-016 PASS.
- TASK-018 — Al-Hakim Pipeline — blocked on TASK-017 PASS.
- TASK-019 — Session/Privacy Layer — blocked on TASK-018 PASS.
- TASK-020 — Oracle Gateway Scaffold — blocked on TASK-019 PASS.
- TASK-022 — Mysticarium Test Route Verification — work/evidence exists, but task remains BLOCKED because no verified provenance-preserving executable deterministic-test route/harness has been demonstrated. Identity collision with VK TASK-022 has been removed; engineering blocker remains.
- TASK-023 — Mysticarium Morrigan Pipeline — blocked and also affected by duplicate numeric task identity; overlaps earlier TASK-016 scope and requires canonical deduplication before execution.
- TASK-024 — Mysticarium Selene Pipeline — blocked and also affected by duplicate numeric task identity; overlaps earlier TASK-017 scope and requires canonical deduplication before execution.
- TASK-025 — Mysticarium Al-Hakim Pipeline — blocked and also affected by duplicate numeric task identity; overlaps earlier TASK-018 scope and requires canonical deduplication before execution.
- TASK-026 — Mysticarium Common Reader Contract — blocked and affected by duplicate numeric task identity.
- TASK-027 — Mysticarium Session Memory — blocked and affected by duplicate numeric task identity; overlaps TASK-019 area and requires canonical deduplication before execution.

## SUPERSEDED
- Former VK `TASK-022 — Capability Discovery Layer` identity is superseded by canonical TASK-032. The old duplicate task file was removed after migration.

No other task is marked SUPERSEDED without an explicit repository-backed canonical replacement decision. Overlapping Mysticarium TASK-023/024/025/027 entries are therefore BLOCKED pending deduplication rather than silently discarded.

## NOT-VERIFIED
- Any task not explicitly listed above should be treated as NOT VERIFIED until reconciled.
- Target-runtime deployment/live-validation status for VK and Mysticarium remains NOT VERIFIED.

## Coordination defects found
1. `status/WORKSHOP_STATE.yaml` was stale and omitted completed TASK-013; reconciled on 2026-08-24.
2. Reviewer status was stale after the TASK-022 collision changed; reconciled on 2026-08-24.
3. Duplicate numeric IDs remain for TASK-023 through TASK-027 across VK and Mysticarium. This is an OPEN coordination blocker for evidence/review routing.
4. Several later Mysticarium tasks duplicate/overlap earlier TASK-016..020 scope. They require canonical deduplication, not parallel implementation.

## Implementation conclusion
At this checkpoint there are many implementation-prepared task definitions, but **zero tasks are independently verified as READY-FOR-IMPLEMENTATION** under the current gates. The immediate unblock work is validation/execution-route establishment and task-ID/backlog deduplication, not sending blocked tasks to Codex.
