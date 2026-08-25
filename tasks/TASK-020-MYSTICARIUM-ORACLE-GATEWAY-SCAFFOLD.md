# TASK-020 — Mysticarium Oracle Gateway Scaffold

TASK_ID: TASK-020
PROJECT: HOROSCOPES / MYSTICARIUM
PRIORITY: MEDIUM
STATUS: PASS / REVIEWED
DEPENDS_ON: TASK-019 PASS
TYPE: REPOSITORY-ONLY IMPLEMENTATION
OBJECTIVE: Define and implement the provider-neutral Oracle gateway interface and premium-reading contract without selecting or calling a paid/external provider.

BOUNDARY: repository branch only; no Pi4 deploy; no provider credentials; no payment provider integration; preserve Oracle as functionally distinct from free readers and preserve locked formless visual canon.
VALIDATION: interface contract tests/mocks, no live external call, independent review.

IMPLEMENTATION_HEAD: `c088aa064f468e4b6c2ce074bba3a91647330b4f`
ROLLBACK: `4f5a63dc6680783d010bd92d730220470d0b0d2a`
EVIDENCE: `evidence/TASK-020/RUN.md`
REVIEW: `review/TASK-020.md`
RUNTIME_VALIDATION: NOT VERIFIED
