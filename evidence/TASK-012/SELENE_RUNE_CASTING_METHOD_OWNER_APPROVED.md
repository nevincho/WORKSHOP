# TASK-012 — Selene rune casting methodology

Date: 2026-08-27
Status: OWNER-APPROVED METHODOLOGY REFERENCE
Reader: Selene
Domain: rune divination / rune casting

## Source and provenance

Owner-approved source:
- Scribd document: `ПОДРЕДБИ С РУНИ`
- URL: https://www.scribd.com/document/661438015/ПОДРЕДБИ-С-РУНИ
- Observed metadata: 34 pages; uploaded by PlamenaGirginova; marked All Rights Reserved.

Copyright boundary: this WORKSHOP artifact does **not** reproduce the source document. It records a concise functional abstraction of the owner-approved casting methodology for engineering use. Rune meanings themselves require separate authoritative/reference coverage.

## General casting rules abstracted from the approved methodology

- Begin from a clearly formulated question or situation.
- Rune selection may be by drawing from a bag/container or by casting onto a surface, depending on the selected spread.
- Ordered spreads preserve draw order.
- Where a spread uses a line, positions are interpreted according to the spread definition rather than by free-form invention.
- Orientation may be meaningful for runes that support distinct upright/reversed interpretation; the production knowledge layer must define which runes support this and their meanings.
- The system must record the chosen spread, ordered rune identities, orientation where applicable, and semantic role of each position before interpretation.
- Interpretation must combine the rune meaning with the semantic role of its position; the model must not silently change the spread after casting.

## Supported spread templates

### One-rune reading
One selected rune represents the focused answer/theme. Suitable for a bounded question or short-period guidance.

### Three-rune temporal reading
Three ordered positions represent a temporal/situational progression. The source contains more than one three-rune convention, so production must choose and name the convention explicitly rather than mixing them. A canonical implementation may use a declared past/present/future-style template once its exact position convention is selected.

### Three-rune body / mind / spirit reading
1. Physical/body state.
2. Mental/mind state.
3. Spiritual/inner state.

### Four-rune elemental reading
1. Earth — foundation, finances/property/material basis.
2. Air — decisions/thought/action choice.
3. Water — emotional dimension.
4. Fire — execution, communication and action toward the project/desire.

### Five-rune situation reading
A useful five-position template from the source is:
1. Past influences.
2. Present influences.
3. Present situation.
4. Action.
5. Result.

The source also contains alternative five-rune layouts. They must be represented as separately named templates if later adopted; positions from different layouts must not be merged.

### Six-rune cross
A cross-style spread assigns positions to past, present, future, influence, beneficial/decisive influence, and probable outcome. Exact geometric placement should be encoded by the implementation artifact when this spread is selected.

### Seven-rune problem / advice / outcome
1–2. Problem/current issue.
3–4. Past events/causes leading to the current situation.
5–6. Advice.
7. Probable outcome.

This is a strong candidate for Selene's default detailed reading because it separates diagnosis, causal history, advice and outcome.

### Seven-rune extended situation reading
The source also provides a seven-position variant covering current situation, causal past, future situation, relevant personal traits/reactions, causes of obstacles, most favourable solution, and synthesis/commentary. Treat this as a distinct named template.

### V-shaped seven-rune reading
A separate seven-rune template covers past influences, present influences, future events, recommended action, feelings/emotions, possible problems, and future development. Treat separately from the other seven-rune spreads.

### Nine-rune grid
A 3×3 grid groups positions into past, present and future bands, with sub-roles such as hidden/visible influences and emotional relation to events/outcomes. Geometry and semantic position IDs must be deterministic in code.

### Nine-rune temporal sequence
A simpler nine-position sequence groups three runes for past, three for present and three for future, including transitional influence from past→present and present→future.

### Larger specialist spreads
The approved document also describes larger/specialist layouts including Tree of Life/Yggdrasil-style readings, Futhark/year reading, 12-rune and 24-rune layouts. These are acknowledged but should not be implemented as defaults until their exact position maps are separately structured and reviewed.

## Production requirements for Selene

The casting engine should separate four layers:

1. **Random/deterministic cast generation** — chooses rune(s), with reproducible seed support for testing.
2. **Spread schema** — defines position count, order, geometry and semantic role.
3. **Rune knowledge** — rune identity plus upright/reversed meanings where applicable.
4. **Interpretation layer** — synthesizes rune meaning × position role × question context without altering the cast.

Minimum machine-readable cast record should include:

```text
reader = Selene
method = rune_casting
spread_id
question
cast_timestamp
seed_or_cast_id
positions[]:
  position_id
  semantic_role
  rune_id
  orientation
```

## Current blocker impact

This artifact supplies an owner-approved methodology basis for Selene's **casting/spread mechanics**. It does not yet establish a complete authoritative dictionary for the rune meanings. Therefore Selene methodology authority is materially improved but should not be marked fully production-complete until rune-symbol knowledge/provenance is covered and reviewed.
