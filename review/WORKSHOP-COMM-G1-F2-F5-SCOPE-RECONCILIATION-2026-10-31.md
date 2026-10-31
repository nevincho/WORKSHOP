# WORKSHOP G1 — F2–F5 scope reconciliation and qualification decision

DATE: 2026-10-31
ROLE: BOUNDED QUALIFICATION WORKER (not independent acceptance Reviewer)
BASELINE: windows@d78976812315448973b9d59fe96d2196dbe89c8e
BRANCH: qualification/g1-windows-f2-f5-20261031
G1_VERDICT: NOT COMPLETE
SCOPE_DECISION: NO RETROACTIVE AUTHORIZATION ESTABLISHED

## Read-only authority check

Canonical contract: `planning/WORKSHOP_COMM_G1_READINESS_CONTRACT.md` (blob `3cdb74a2988d0ab533e61d095441d4e495412ee4`).
Canonical qualification task: `tasks/WORKSHOP-COMM-G1-QUALIFICATION-01.md` (blob `0d2eed7b5a3f030c296e01cac8a6718484fd1623`).
Independent FAIL: `review/WORKSHOP-COMM-G1-CANDIDATE-660d7edf-INDEPENDENT-REVIEW-2026-10-30.md` (blob `3c1e5d1a630e2a819f3150df4d740088bbd3c472`).
The qualification task's 2026-10-30 bounded authorization permits only fenced-Markdown parser correction in `apps/workshop_g1/workshop_g1/core.py` and regression tests in `apps/workshop_g1/tests/test_g1.py`; other G1 production source remains protected.

## F2–F5 reconciliation

| Finding | Source-level change already on windows | Authorization and acceptance |
| --- | --- | --- |
| F2 CREATE rollback / UTF-8 bytes | `core.py` modifications beyond fenced-parser scope | Defect-oriented and previously tested in part; explicit expansion of original bounded authorization NOT VERIFIED. Root-creation early failure and post-open identity-exception cleanup remain unqualified. |
| F3 strict OPEN metadata | `core.py` and `app.py` changes | Useful code path, but `app.py` is protected by the narrow task. No explicit bounded authorization for that prior change found in reviewed G1 task. Strict OPEN NTFS evidence missing in prior review. |
| F4 UTF-8 line byte bound | `core.py` changes | Prior Windows multibyte negative PASS; broader source-scope expansion not separately authorized by G1 qualification task. |
| F5 visible trust provenance | `app.py` changes | Source string exists; user-visible Windows 10/11 UI acceptance NOT VERIFIED. `app.py` protected by original bounded task. |

The later `tasks/WORKSHOP-COMM-V1-INTEGRATED-BUILD-01.md` authorizes an isolated integrated candidate, not an explicit retroactive waiver of the G1 qualification task's protected-file rule. This Worker neither waives nor reverts prior source modifications.

## Authorized action now

Create only an isolated, disposable Windows qualification harness and branch-specific CI workflow, with no G1 production-source modifications. Tests must differentiate actual Windows Server 2022 NTFS evidence from a Windows 10/11 client acceptance. Any demonstrated CREATE source defect requires separate explicit authorization for a minimal repair. Do not create G1 COMPLETE checkpoint, merge, or authorize G2–G7 as accepted. Independent Reviewer must reconcile this scope issue before final acceptance.

## Rollback

Delete the isolated qualification branch only after preserving its review evidence; `windows`, `main`, trusted files, agents and existing workspaces are unchanged.
