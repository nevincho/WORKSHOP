# TASK-016 — SCOUT / PLANNER

STATUS: READY_FOR_WORKER
DATE: 2026-08-25
PROJECT: HOROSCOPES / MYSTICARIUM

## Eligibility
- TASK-015 is PASS/reviewed at `nevincho/TANGRA-DOCS@agent/mysticarium` head `4792b406d5ba1e440a8709c3aeca60aefa00a403`.
- TASK-016 is therefore the next canonical Mysticarium task.
- No Morrigan pipeline implementation exists in the current engine tree.

## Existing interfaces / evidence
- canon: Morrigan domains are runes, bones and darker fate; locked character/canon must not be altered;
- reader corpus: allowed domains include `runes` and `bones`;
- representative knowledge fixture uses semantic fragment domain `rune` (singular), establishing a distinction between reader capability name (`runes`) and knowledge-fragment taxonomy (`rune`);
- TASK-014 deterministic core and presentation metadata v1 are already verified;
- TASK-015 proves the current repository-side reader-pipeline pattern without adding a parallel engine.

## Smallest justified implementation
Implement a pure Morrigan repository pipeline supporting `runes` and `bones`, with explicit mapping to knowledge-fragment domains `rune` and `bone`. It must:
- reuse TASK-014 deterministic seed/bounded selection;
- include reader, method, normalized question, topic, content-set version and pipeline version in relevant deterministic input;
- use locale-independent fragment ordering;
- return structured divination/knowledge/interpretation/Morrigan identity/presentation metadata;
- fail explicitly when a requested method has no eligible knowledge;
- use only test-local representative bone data unless/until a canonical content corpus exists.

## Protected / non-goals
No Pi4 deploy, web/canon edits, memory/session architecture, new deterministic engine, external provider, or production prose corpus. No implementation of generic `dark_fate` unless evidence defines its divination/knowledge contract.

## Validation
Repository tests for repeated-input determinism, runes path using committed fixture, bones path using bounded test fixture, method separation, input-order stability, presentation contract and TASK-014 regression; independent review.

## Codex decision
This is a bounded adaptation over verified deterministic/knowledge/presentation interfaces. Codex is not justified unless a contract conflict emerges.

SCOUT RESULT: READY_FOR_WORKER
