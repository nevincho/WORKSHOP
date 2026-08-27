# TASK-012 — Morrigan / Bones knowledge authority

Date: 2026-08-27
Status: OWNER-APPROVED SOURCE / STRUCTURED KNOWLEDGE ARTIFACT PENDING

## Owner decision

The owner explicitly approves `https://bonethrowing.org/` as an operational reference source for the Morrigan / bones (osteomancy / bone throwing) reader.

This approval resolves the previous authority question for the source selection. It does **not** by itself assert that every statement on the site is historically universal, academically authoritative, or already integrated into production.

## Owner-supplied foundation

The Morrigan reader may use the following owner-approved conceptual foundation:

- Bone throwing / osteomancy uses a personal collection of bones, shells, stones, coins, and/or symbolic small objects.
- Objects are shaken/cast onto a cloth, circle, or other defined reading field.
- Each object has a symbolic meaning defined by the selected tradition/system and the reader's configured interpretation rules.
- Position is meaningful; the owner supplied center as the main situation/question, left/right as past/future, and outside the cloth/field as rejected or insignificant influences.
- Proximity between objects may represent relationships between life areas or influences.
- Face-down / orientation state may represent hidden or weakened influences where applicable to the selected object/system.

## Approved operational reference

Primary operational reference for building the Morrigan knowledge artifact:

- `https://bonethrowing.org/`

The source is approved for extracting and structuring practical bone-throwing concepts such as object/bone meanings, casting layout, orientation, proximity/clustering, crossing/isolation/pointing, and reading procedures where present.

## Engineering constraints

- Do not copy the website wholesale into the repository.
- Build a structured, provenance-tagged knowledge artifact using concise paraphrases/facts/rules needed by the reader.
- Preserve the source URL and per-rule provenance where practical.
- Do not silently invent missing bone meanings or interpretation rules.
- Conflicts between the owner-supplied foundation and external reference material must be surfaced for owner decision rather than silently reconciled.
- Production integration remains subject to Worker implementation and Independent Reviewer validation.

## Blocker impact

`Morrigan / bones: PRODUCTION_KNOWLEDGE_AUTHORITY_MISSING` is resolved at the source-authority level.

Remaining Morrigan work:
1. research/extract the approved operational rules;
2. construct the structured knowledge artifact;
3. validate coverage/provenance;
4. integrate only through the existing reviewed Mysticarium architecture.

TASK-012 as a whole is **not yet unblocked**, because Selene and Al-Hakim knowledge authority/content still require reconciliation unless separately resolved by repository evidence.
