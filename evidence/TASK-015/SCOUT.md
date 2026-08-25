# TASK-015 — SCOUT / PLANNER

STATUS: READY_FOR_WORKER
DATE: 2026-08-25
PROJECT: HOROSCOPES / MYSTICARIUM

## Eligibility and necessity
- TASK-014 is independently verified PASS at target commit `f4adb7c43ccf0aaa710bb1b03069ad5c5aff38cf`.
- TASK-015 is the next canonical Mysticarium implementation task and is not superseded by the duplicate TASK-023–027 planning series.
- Current target already contains the deterministic core, knowledge-fragment contract/fixture, presentation-metadata contract/fixture and reader-domain corpus needed for a bounded repository-only Djalma tarot path.
- No existing Djalma pipeline implementation was found in the current project tree.

## Authoritative target
- repo: `nevincho/TANGRA-DOCS`
- branch: `agent/mysticarium`
- pre-change checkpoint: `f4adb7c43ccf0aaa710bb1b03069ad5c5aff38cf`

## Verified interfaces / boundaries
- Djalma allowed domains: tarot, palm, coffee.
- TASK-015 explicitly requires tarot first; palm/coffee may only be scaffolded where evidence supports them.
- Deterministic core exports versioned normalization, deterministic seed and bounded selection.
- Knowledge fragments are structured by `knowledge-fragment.schema.json`.
- Presentation metadata v1 permits tone = hopeful/uncertain/warning/ominous with bounded intensity.
- Canon requires Djalma identity to remain locked and free readings to preserve deterministic fate.

## Smallest justified Worker implementation
Implement only a pure repository-side Djalma tarot pipeline that:
1. accepts an already-normalized question/context and a supplied knowledge-fragment collection;
2. builds the deterministic input with `reader=djalma` and `method=tarot`;
3. filters/sorts eligible tarot fragments deterministically and selects through TASK-014 bounded selection;
4. returns selected knowledge, interpretation text without inventing new canon prose, Djalma persona identity metadata and contract-compatible presentation metadata;
5. carries an explicit fragment-set version in the deterministic input so content-set revisions cannot be silently treated as the same contract;
6. adds deterministic repeat and end-to-end repository tests using committed fixtures.

## Protected / non-goals
- no Pi4 deploy/runtime/service work;
- no web scene changes;
- no canon edits;
- no palm/coffee vision implementation or provider selection;
- no external AI/payment/session work;
- no new prose corpus or speculative tarot content;
- no reader pipelines other than Djalma tarot.

## Validation
- exact committed source/test/fixture provenance;
- Node repository test command;
- same normalized input/context/content version => identical selected fragment/output;
- changed relevant input changes seed path;
- input -> deterministic divination -> knowledge -> interpretation -> persona identity/presentation metadata demonstrated;
- existing TASK-014 tests remain PASS;
- independent Reviewer diff/contract check.

## Codex decision pre-check
The bounded pure pipeline is mechanically implementable from already-verified contracts and fixtures. No runtime integration or ambiguous architecture decision is required. Codex is not justified unless implementation reveals a non-trivial contract conflict.

SCOUT RESULT: READY_FOR_WORKER
