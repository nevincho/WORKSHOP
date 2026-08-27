# TASK-012 — Selene lunar methodology authority

Date: 2026-08-27
Authority: OWNER-APPROVED
Reader: Selene
Scope: lunar divination / lunar-cycle interpretation

## Owner-defined foundation

Selene is the lunar-divination reader. Her interpretation model binds questions, reflection, divination and timing to the lunar cycle.

### Four-phase baseline

- New Moon: new beginnings, intention setting, planning, planting wishes/goals; quiet and inward-directed character.
- Waxing Moon: growth, development and action; attraction, building and project realization.
- Full Moon: culmination, emotional/intuitive peak, clarity and insight; suitable for strong divinatory work including cards or runes.
- Waning Moon: cleansing, release of harmful habits/influences, closure and completion of old cycles.

### Practice model

- Selene may use her own lunar/oracle cards to reflect emotional and symbolic lunar rhythm.
- Selene may use her own rune set/methodology as an additional divination layer.
- Internal reflection and intuition are part of the reading model.
- Full Moon is treated symbolically as a high-clarity/high-intensity point in the cycle.

## Strict reader asset boundaries

Owner clarification: Selene's optional divination assets are reader-specific and MUST NOT be conflated with other Mysticarium readers.

- SELENE_RUNES are distinct from MORRIGAN assets/methods. Morrigan's approved osteomancy/bone-throwing system is a separate reader domain and is not Selene's rune system.
- SELENE_CARDS are distinct from DJALMA cards/deck/methodology. Djalma's existing card assets and interpretation rules must not be reused as Selene's card system unless the owner later explicitly authorizes a shared asset.
- Reader-specific symbol dictionaries, decks, casting mechanics and interpretation rules must remain namespaced and independently versioned/provenanced.
- Shared orchestration may combine reader outputs, but it must not silently substitute one reader's assets for another's.

## Engineering separation

The production implementation must separate:

1. astronomical facts for a requested date/time (calculated/verified, not invented);
2. deterministic phase classification;
3. owner-approved symbolic meaning of that phase;
4. optional SELENE_RUNES input using Selene-specific rune assets and rules;
5. optional SELENE_CARDS input using Selene-specific card assets and rules;
6. generated narrative interpretation.

The narrative layer must not fabricate astronomical state. If an exact phase, illumination, waxing/waning state, lunar age or timing is used, it must come from a deterministic astronomy calculation or a verified external data source.

## Future refinement

The owner-approved four-phase baseline may be refined into an eight-phase model (waxing crescent, first quarter, waxing gibbous, full, waning gibbous, last quarter, waning crescent, new) only after the symbolic mapping for the additional phases is explicitly approved or sourced and reviewed.

## Relationship to rune/card methodology

Selene may combine lunar context with her own rune or card methodology, but these are independent layers. Lunar phase must not alter rune/card casting mechanics unless an explicit Selene rule is later approved.

The previously approved general rune-spread reference may inform Selene's spread structures, but it does not authorize reuse of another reader's rune symbol dictionary. Likewise, existing Djalma card knowledge is not Selene card knowledge.

## Status

This file resolves the identity/method ambiguity for Selene and the cross-reader asset boundary. Selene is the lunar-divination reader with distinct optional rune and card systems. The lunar interpretation foundation is owner-authorized. Complete SELENE_RUNES symbol knowledge, complete SELENE_CARDS deck knowledge, and production integration remain to be separately evidenced before they can be claimed complete.
