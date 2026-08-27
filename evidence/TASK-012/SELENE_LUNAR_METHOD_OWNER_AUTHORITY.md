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

- Lunar/oracle cards may be used to reflect emotional and symbolic lunar rhythm.
- Internal reflection and intuition are part of the reading model.
- Full Moon is treated symbolically as a high-clarity/high-intensity point in the cycle.

## Engineering separation

The production implementation must separate:

1. astronomical facts for a requested date/time (calculated/verified, not invented);
2. deterministic phase classification;
3. owner-approved symbolic meaning of that phase;
4. optional rune/card spread inputs;
5. generated narrative interpretation.

The narrative layer must not fabricate astronomical state. If an exact phase, illumination, waxing/waning state, lunar age or timing is used, it must come from a deterministic astronomy calculation or a verified external data source.

## Future refinement

The owner-approved four-phase baseline may be refined into an eight-phase model (waxing crescent, first quarter, waxing gibbous, full, waning gibbous, last quarter, waning crescent, new) only after the symbolic mapping for the additional phases is explicitly approved or sourced and reviewed.

## Relationship to rune methodology

Selene may combine lunar context with the separately approved rune-spread methodology, but these are independent layers. The lunar phase must not alter the mechanics of a rune cast unless an explicit rule is later approved.

## Status

This file resolves the identity/method ambiguity for Selene: Selene is the lunar-divination reader. It supplies an owner-authorized lunar interpretation foundation. It does not by itself establish the complete rune-symbol dictionary or complete production integration.
