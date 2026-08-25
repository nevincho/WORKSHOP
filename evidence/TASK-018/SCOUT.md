# TASK-018 — SCOUT / PLANNER

STATUS: READY_FOR_WORKER
DATE: 2026-08-25
PROJECT: HOROSCOPES / MYSTICARIUM

## Eligibility
TASK-017 is PASS/reviewed. TASK-018 is the next canonical Mysticarium task. No Al-Hakim pipeline exists in the current target tree.

## Verified scope
Canon/reader corpus support `natal_chart`, `astrology`, `planetary_aspects`, `transits`, `forecast`. The task expressly forbids adding unsupported astronomy/ephemeris dependencies. No verified ephemeris/calculation provider or production Al-Hakim knowledge corpus exists.

## Smallest justified implementation
Implement only a pure structured interpretation pipeline over caller-supplied **already-normalized/calculated context** and supplied knowledge fragments. It must not calculate astronomical positions. Reuse TASK-014 deterministic seed/bounded selection, include method/question/topic/context/content-version in deterministic input, use locale-independent fragment ordering, and return knowledge/interpretation/Al-Hakim identity/presentation metadata.

## Protected / non-goals
No ephemeris/astronomy library, external API, Pi4 deploy, web/canon edit, invented birth-chart calculation, new production content corpus, session/payment/Oracle work or parallel deterministic engine.

## Validation
All five verified methods accepted with bounded test fixtures; deterministic repeat; supplied calculation/context affects seed; unsupported method explicit failure; input-order stability; presentation metadata contract; independent review.

## Codex decision
The bounded content-neutral adapter is mechanically implementable over existing contracts. No Codex required unless an astronomy calculation requirement appears; none is evidenced in this phase.

SCOUT RESULT: READY_FOR_WORKER
