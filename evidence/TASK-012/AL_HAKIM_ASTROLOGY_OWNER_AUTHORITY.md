# TASK-012 — Al-Hakim astrology methodology authority

Date: 2026-08-27
Authority: OWNER-APPROVED
Reader: Al-Hakim
Scope: astrology / star-divination / natal-chart interpretation

## Owner-defined identity

Al-Hakim is the astrology (звездобройство) reader.

The domain is the symbolic interpretation of the positions and movements of the Sun, Moon and planets for horoscope and astrological reading purposes.

## Owner-defined purpose

- Interpret character and life-path themes through astrology.
- Produce astrological/horoscope-style forecasts using defined astrological inputs and rules.
- For natal analysis, use a birth chart derived from birth date, birth time and birth place.

## Primary method: natal astrology

Required user inputs for a complete natal chart:

- date of birth;
- time of birth;
- place of birth.

The production system must distinguish a complete natal-chart reading from reduced readings where birth time or place is missing. Missing inputs must not be silently invented.

## Engineering separation

Al-Hakim must separate deterministic astronomical/chart computation from symbolic interpretation:

1. parse birth date/time/place;
2. resolve place to coordinates/time-zone data using a verified deterministic source or approved dataset;
3. calculate or obtain verified astronomical positions for the relevant timestamp/location;
4. derive the explicitly approved astrological chart features;
5. apply an approved Al-Hakim interpretation knowledge base;
6. generate the narrative reading from those structured facts.

The narrative model MUST NOT invent planetary positions, signs, houses, aspects, ascendant, lunar position or other calculated chart facts.

## Knowledge still required before production acceptance

This owner authority establishes Al-Hakim's identity and primary method but does not yet define the complete production astrology system. The following require explicit sourcing/approval and review:

- zodiac/sign interpretation dictionary;
- planets and luminaries interpretation dictionary;
- houses, if houses are included;
- aspects and orb rules, if aspects are included;
- ascendant calculation/interpretation, if included;
- house system (e.g. Placidus, Whole Sign, etc.), if houses are included;
- ephemeris/astronomical calculation source and validation methodology;
- rules for incomplete birth-time/place inputs;
- forecast/transit methodology if Al-Hakim produces future-event readings beyond natal interpretation.

No particular western, Vedic, Arabic/Persian, traditional, modern or other astrology school is implied by the name Al-Hakim. The production school/rule set remains NOT VERIFIED until explicitly selected and evidenced.

## Reader boundary

Al-Hakim's astrology assets and rules are independent of Selene's lunar/rune/card/numerology methods, Morrigan's osteomancy system, and Djalma's card system. Shared orchestration may combine reader outputs but must not silently substitute another reader's rules or symbolic dictionaries.

## Status

AL_HAKIM_IDENTITY: OWNER_APPROVED
PRIMARY_METHOD: NATAL_ASTROLOGY
CORE_INPUTS: BIRTH_DATE + BIRTH_TIME + BIRTH_PLACE
COMPLETE_PRODUCTION_RULESET: NOT_VERIFIED
PRODUCTION_INTEGRATION: NOT_VERIFIED
