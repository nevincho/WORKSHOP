# TASK-017 — SCOUT / PLANNER

STATUS: READY_FOR_WORKER
DATE: 2026-08-25
PROJECT: HOROSCOPES / MYSTICARIUM

## Eligibility
TASK-016 is PASS/reviewed. TASK-017 is the next canonical Mysticarium task. No Selene engine/pipeline implementation is present in the current target tree.

## Verified boundaries
Canon locks Selene to zodiac, daily/love horoscopes and lunar themes. The reader corpus independently lists `zodiac`, `daily_horoscope`, `love_horoscope`, `lunar`. TASK-014 deterministic core and existing knowledge/presentation contracts are reusable. There is no committed Selene production knowledge corpus, so implementation must remain content-neutral and tests may use bounded schema-shaped fixtures only.

## Smallest justified implementation
A pure Selene structured-reading pipeline that accepts one of the four verified methods, normalized question/topic/context, supplied knowledge fragments and explicit fragment-set version; reuses TASK-014 deterministic seed/bounded selection; uses locale-independent fragment ordering; returns selected knowledge, interpretation, Selene identity and presentation metadata. No astrology calculation or ephemeris is introduced.

## Protected / non-goals
No Pi4/web/canon changes; no external astrology/API dependency; no new production horoscope corpus; no parallel deterministic engine; no session/payment/Oracle work.

## Validation
Deterministic repeat, method participates in seed, all four verified methods accepted using bounded test fixtures, unsupported method explicit failure, fragment input-order stability, presentation metadata shape and independent review.

## Codex decision
Bounded repository-only adaptation over verified contracts; Codex not justified unless an unforeseen contract conflict appears.

SCOUT RESULT: READY_FOR_WORKER
