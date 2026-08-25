# TASK-058 — AI_COMPANY Repository Onboarding

STATUS: HUMAN_LOCAL_ACTION_REQUIRED
PROJECT: AI_COMPANY / WORKSHOP integration
TYPE: repository onboarding / architecture preservation
SCHEDULE_INTENT: evening 2026-08-25 when Vlad has access to the Windows PC

## Current authoritative local state
- Project root: `F:\AI_COMPANY`
- AI_COMPANY is currently local and is NOT VERIFIED as represented in any GitHub repository.
- Do not reconstruct, redesign, or replace the local project from this brief.

## Objective
When Vlad has local PC access, inspect the actual `F:\AI_COMPANY` tree and Git state first, then place the existing project under an appropriate GitHub repository/ref without changing validated behavior or architecture. After repository onboarding, prepare a bounded WORKSHOP integration contract so AI_COMPANY can later serve as an advisory research/orchestration backend.

## Architecture to preserve
- deterministic Python controller owns workflow/stage transitions/budgets/retries/validation/persistence/audit/approvals/termination;
- AI roles: Research, Analysis, Independent Reviewer, Local Utility Worker;
- SQLite runtime/project state;
- append-only audit;
- SHA-256 content-addressed artifacts;
- Git for source/docs/policies;
- central models remain external at `D:\Store\AI\models` and MUST NOT be copied into the repository;
- £0 operating-cost policy; no paid fallback;
- Founder remains final decision maker.

## Known validation boundary
- infrastructure/controller/persistence/evaluation/cap tests and local multi-role path to Founder Decision Gate: human-reported as functioning, repository evidence pending;
- Qwen3-1.7B serious Research/Analysis/Reviewer reasoning: known inadequate from controlled test; intended primarily for Utility/fast tier;
- Qwen3.5-4B serious reasoning quality: NOT VERIFIED / evaluation pending;
- serious autonomous engineering/research quality: NOT VERIFIED.

## Required evening procedure
1. Inspect `F:\AI_COMPANY` actual files, Git state, configs, tests and local evidence before deciding repository layout.
2. Identify secrets, databases, runtime artifacts, model references, caches and machine-specific data that MUST NOT be committed.
3. Establish `.gitignore`/repository boundary preserving local runtime data.
4. Create or select the GitHub repository/ref only after inspection; do not invent repository state.
5. Commit source/docs/policies/tests needed to represent the existing system faithfully.
6. Record exact commit/ref and evidence in WORKSHOP.
7. Only after onboarding, prepare the `WORKSHOP <-> AI_COMPANY` advisory job/artifact contract.
8. Do not activate AI_COMPANY as trusted engineering decision authority; outputs remain advisory until capability evaluation passes.

## Explicit exclusions
- NO architecture expansion during onboarding.
- NO model copies into Git.
- NO secrets/runtime DB/private project artifacts unless explicitly reviewed and approved.
- NO replacement of deterministic controller with LLM orchestration.
- NO claim that 4B reasoning is adequate before controlled evaluation.

## Acceptance
Repository onboarding is PASS only when the GitHub representation is traceable to the inspected local project, sensitive/runtime-only material is excluded, rollback/source provenance is clear, and existing local behavior has not been intentionally changed as part of onboarding.
