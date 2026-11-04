# WORKSHOP Commercial AI Desktop — active execution handoff

DATE: 2026-11-04
PROJECT: WORKSHOP Commercial Edition
TASK_ID: WORKSHOP-COMM-AI-PARITY-INTEGRATED-01
STATE: IN_PROGRESS / PARTIAL IMPLEMENTATION / NOT RELEASE
CODEx: FORBIDDEN by current owner direction

## Authoritative continuation points

- Work task (same branch): tasks/WORKSHOP-COMM-AI-PARITY-INTEGRATED-01.md
- Active implementation branch: feature/workshop-ai-local-provider-20261104
- Active draft PR: https://github.com/nevincho/WORKSHOP/pull/6
- Protected baseline: feature/desktop-v1-d1-d3-repair-20261101, PR #4
- Initial separate planning PR #5 is not the active implementation branch.
- The current implementation branch now contains the full task, so workers need not reconstruct it from conversation.
- Latest source and CI HEAD: discover fresh GitHub PR #6 state; do not freeze this document's dates or commits as current.
- Hosted Windows CI: https://github.com/nevincho/WORKSHOP/actions/runs/41800365547 (success: current Ollama adapter unit, not product integration).

## True startup sequence

1. Bootstrap AGENTS.md -> README.md -> mandatory WORKSHOP policies -> role -> registry -> canonical task and evidence -> actual target source.
2. Inspect PR #6 HEAD and its complete diff against the protected Desktop V1 base. Do not recreate task or branch.
3. Confirm one smallest eligible *implementation* unit, and verify tested prerequisites, rollback, path scope and current phase.
4. Worker changes real source in isolated branch; pushes commit. This is the actual execution trigger. Merely creating a task or pressing a ChatGPT scheduled run button does NOT launch Worker.
5. The branch PR automatically triggers relevant GitHub Actions tests when their configured paths/events match. Hosted CI validates code; it is NOT a coding agent.
6. Independent Reviewer checks frozen source, actual CI logs, objective/criteria, protection and repository hygiene. No self-review labeled independent.
7. If PASS, record checkpoint and continue to next eligible dependent unit in the same run when the actual execution environment remains available; otherwise persist exact handoff and blocker.
8. Notify owner only when product fully qualified, or when an unavoidable owner-only action blocks completion.

## Current unit evidence and limits

- ai_provider_contract.py + ollama_provider.py + test_ollama_provider.py: provider-neutral reply interface, opt-in localhost-only Ollama text API, redirect/proxy blocking, mocked tests.
- Windows hosted CI unit: pass on 2026-11-04; NOT verified against live Ollama; NOT a coding Worker.
- No verified end-to-end AI coding, independent reviewer, provider settings UI, external API, GitHub coding-agent delivery, advanced-friendly UI or sellable installer.
- Next: independent review of this small unit. Fix any reviewable defects, then implement the smallest approved model/Controller integration that preserves trust boundaries. No automatic arbitrary shell or file writes; no paid API.

## Continuity failure discovered

Earlier initial implementation involved direct Worker source commits + CI + evidence/review. Daily ChatGPT automation is a scheduler, not evidence of a persistent Worker. No repository mechanism has been proven that dispatches queued WORKSHOP tasks to a general AI coding agent. A scheduler that merely reads task files or starts CI cannot be called autonomous implementation. When true autonomous executor entitlement/connection is missing, record the precise prerequisite, rather than claiming WORKSHOP is coding in the background.

This single handoff file is intended to prevent repeated re-discovery after Control Room rotation.
