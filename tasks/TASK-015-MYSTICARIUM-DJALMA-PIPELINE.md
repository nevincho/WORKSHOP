# TASK-015 — Mysticarium Djalma Free-Reading Pipeline

TASK_ID: TASK-015
PROJECT: HOROSCOPES / MYSTICARIUM
PRIORITY: HIGH
STATUS: BLOCKED
DEPENDS_ON: TASK-014 PASS
TYPE: REPOSITORY-ONLY IMPLEMENTATION
OBJECTIVE: Implement the Djalma free-reading path justified by canon and TASK-014 engine interfaces: tarot first, with palm/coffee interfaces scaffolded only where evidence supports them.

BOUNDARY:
- repository branch only; no Pi4 deploy;
- no external vision provider selection;
- preserve Djalma locked visual/persona canon;
- deterministic reading contract must remain intact.

VALIDATION:
- deterministic repeat test;
- input -> divination -> knowledge -> interpretation -> persona/presentation metadata path demonstrated in repository tests or harness;
- independent review.
