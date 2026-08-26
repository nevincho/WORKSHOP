# TASK-012 — Production Knowledge Authority Blocker

DATE: 2026-08-26
STATE: OPEN
AFFECTS: TASK-012 only and downstream Mysticarium production deployment

## Blocker
The canonical Mysticarium repository contains reviewed reader engines and test fixtures, but no authoritative production knowledge/input corpus with provenance for Selene, Al-Hakim and Morrigan/bones. TASK-012 explicitly requires those production inputs to be traceable before the five-reader chain can satisfy acceptance.

## Why this is a blocker
- Test fixtures are validation data and must not be silently promoted to production knowledge.
- The controller must not invent occult/astrology/bones production content or its provenance/licensing.
- Building production API/orchestration around absent inputs would create an integration that cannot meet its own end-to-end acceptance criteria.
- Codex does not resolve missing content authority and is not justified for this blocker.

## Unblock conditions
All of the following must be satisfied:
1. canonical source(s) for Selene, Al-Hakim and Morrigan/bones production knowledge are identified or committed;
2. provenance/licensing/ownership status is explicit enough for use;
3. production file/data format is defined or directly inferable from reviewed contracts;
4. Independent Scout confirms the sources are not merely test fixtures and do not duplicate an existing production corpus.

After these conditions are satisfied, TASK-012 may return to READY_FOR_WORKER for repository implementation and tests. Pi4 deployment remains a later human-gated Codex step after repository Reviewer PASS.
