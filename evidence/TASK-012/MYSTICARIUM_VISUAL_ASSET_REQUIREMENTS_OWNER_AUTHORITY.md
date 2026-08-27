# TASK-012 — Mysticarium visual asset requirements

Date: 2026-08-27
Authority: OWNER-APPROVED
Status: DESIGN/CONTENT REQUIREMENT — IMPLEMENTATION NOT YET VERIFIED

## Global visual rule

Mysticarium must use authentic/recognizable divination and astronomy imagery appropriate to the selected reader/method, but assets MUST be integrated into the established Mysticarium visual language.

This explicitly excludes a collage of raw/cropped photographs or visually unrelated web images.

Required treatment:
- preserve factual/symbolic identity of the depicted card, rune, bone/object, palm/coffee pattern, lunar card, constellation, nebula, horoscope/chart, etc.;
- present assets through a consistent Mysticarium frame, background, typography, spacing, lighting/tonal treatment and UI composition;
- source assets must have documented provenance and a license/permission compatible with the intended deployment;
- styling must not change the identity or semantic content required by the reading engine;
- the displayed visual must correspond to the actual selected/drawn/calculated result, not a generic decorative substitute.

## Djalma

Reader modes/assets include:

1. **Tarot**
   - Display the real/recognizable Tarot card corresponding exactly to the card selected by the reading engine.
   - Tarot imagery must be visually integrated into the Mysticarium style rather than shown as an arbitrary cropped source image.

2. **Coffee reading / tasseography**
   - Visual presentation must represent the coffee-reading method and the symbols/patterns used by Djalma.
   - Exact production visual assets and mapping remain to be evidenced.

3. **Palm reading / palmistry**
   - Visual presentation must use an appropriate hand/palm diagram or image tied to the actual palm-reading features used by the method.
   - Exact production visual assets and mapping remain to be evidenced.

## Morrigan

Reader modes/assets include:

1. **Bones / osteomancy**
   - Use recognizable bone/osteomancy objects corresponding to the actual cast/result.
   - The visual composition may be stylized to Mysticarium, but object identity, orientation and spatial relationships required by the reading must be preserved.

2. **Runes**
   - Morrigan has a distinct rune mode.
   - Display the actual rune(s) selected by Morrigan's rune engine, using a Morrigan-specific visual set.
   - Do not substitute Selene rune assets or meanings.

3. **Fate Mirror / Съдбовно огледало**
   - Morrigan has a Fate Mirror mode.
   - Visual design must be a reader-specific Mysticarium mirror experience tied to that mode, not a generic decorative image.
   - Exact mechanics/knowledge and visual-state mapping remain NOT VERIFIED until separately defined.

## Selene

Reader modes/assets include:

1. **Lunar cards**
   - Use recognizable/real lunar-oracle card imagery for the specific selected card/result.
   - Selene's cards are distinct from Djalma's Tarot/card assets.
   - Visual integration must follow the Mysticarium style.

2. **Crystal ball**
   - Selene has a crystal-ball mode.
   - The crystal-ball visual should be an integrated Mysticarium scene/component whose displayed state is tied to the actual reading result where applicable.
   - Exact mechanics/knowledge and visual-state mapping remain NOT VERIFIED until separately defined.

3. **Other Selene methods already authorized**
   - Lunar-divination context, Selene-specific runes, and Love/numerology remain separate methods and must retain their own asset/knowledge namespaces.

## Al-Hakim

Reader modes/assets include:

1. **Constellations**
   - Use recognizable astronomical constellation diagrams: star points with the conventional connecting-line pattern where applicable.
   - Do not replace these with unrelated fantasy constellation artwork.
   - Presentation may be restyled into Mysticarium's visual language while preserving constellation identity.

2. **Nebulae / deep-sky imagery**
   - Use authentic astronomical imagery or scientifically recognizable representations of the relevant nebula/deep-sky object when that object is part of the experience.
   - Preserve object identity while adapting framing/composition to Mysticarium.

3. **Cards**
   - Al-Hakim has a card mode distinct from Djalma and Selene.
   - Exact deck, meanings, mechanics and production visual assets remain NOT VERIFIED until separately defined.

4. **Horoscopes / astrology charts**
   - Al-Hakim has horoscope/astrology output.
   - Chart visuals must correspond to deterministic astrological calculations where chart facts are shown; decorative graphics must not fabricate astronomical/chart state.

## Asset architecture requirement

Assets must be namespaced by reader and method. Example conceptual boundary:

- DJALMA/TAROT
- DJALMA/COFFEE
- DJALMA/PALM
- MORRIGAN/BONES
- MORRIGAN/RUNES
- MORRIGAN/FATE_MIRROR
- SELENE/LUNAR_CARDS
- SELENE/CRYSTAL_BALL
- SELENE/RUNES
- SELENE/LOVE_NUMEROLOGY
- AL_HAKIM/CONSTELLATIONS
- AL_HAKIM/NEBULAE
- AL_HAKIM/CARDS
- AL_HAKIM/HOROSCOPE

Cross-reader asset substitution is prohibited unless the owner explicitly authorizes a shared asset.

## Acceptance principle

A production mode is not visually complete merely because it has an image. Acceptance requires:

1. correct semantic asset for the actual reading/result;
2. verified provenance/licensing;
3. consistent Mysticarium visual treatment;
4. no semantic distortion from styling;
5. correct responsive/UI integration;
6. mapping between reading-engine state and displayed visual tested.

This document defines requirements only. It does not claim that these visual assets already exist or are production-integrated.
