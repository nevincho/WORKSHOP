# TASK-012 — Production Knowledge Completion Blocker

DATE: 2026-08-28
STATE: OPEN / NARROWED
AFFECTS: TASK-012 only and downstream Mysticarium production deployment

## Reconciliation result

The previous blocker statement that Mysticarium had **no authoritative Selene / Al-Hakim / Morrigan-bones authority** is no longer accurate.

Owner-approved reader-method authority has now been promoted into the authoritative target repository:

- repository: `nevincho/TANGRA-DOCS`
- branch: `agent/mysticarium`
- canonical authority: `projects/mysticarium/PRODUCTION_READER_AUTHORITY.md`
- authority commit: `5dd5c2f989f1004400d40d137c78d6aa2afdcbf5`
- README/canonical routing update: `0e8077d3a9a383baae03f0cb3833a3dbcaf87821`
- newer reader-method-flow commit: `f24d653f854011885c102e659501fe65b1be2b12`

The target repository already contains reader engines, contracts and tests. The canonical authority defines the owner-approved method identities, reader asset boundaries, deterministic-vs-narrative separation and visual requirements.

The 2026-08-28 reader-method-flow commit adds `projects/mysticarium/tests/web-reader-integration.test.mjs` and updates `projects/mysticarium/web/app.js` to expose the approved reader/method routing and input contracts. Its own tests deliberately preserve unsupported methods as unavailable and keep Oracle mock-only. This is useful integration preparation, but it does **not** evidence the missing production dictionaries, licensed/provenanced visual assets, exact numerology/astronomy rules, or other production knowledge listed below. Therefore it does not satisfy the remaining TASK-012 unblock conditions.

## Remaining blocker

TASK-012 is still not production-ready because several **complete production mappings/assets and provenance details** remain undefined or unvalidated. The blocker is content completion/integration, not absence of reader identity, method authority, or web method-routing structure.

### Morrigan

Established:
- runes, bones/osteomancy, Fate Mirror;
- owner-approved osteomancy operational reference: `https://bonethrowing.org/`;
- casting/position/orientation/proximity foundation;
- web method routing now identifies `runes`, `bones`, and `fate_mirror`; the first two route only to existing engine interfaces while unsupported behavior remains unavailable.

Still required before production acceptance:
- complete Morrigan bones/object symbol dictionary and meanings;
- complete Morrigan rune symbol dictionary/casting mappings if not already present in authoritative production data;
- Fate Mirror mechanics/state mapping;
- deployable visual assets with provenance/licensing.

### Selene

Established:
- lunar-divination identity and four-phase baseline;
- Selene-specific runes/cards are separate from Morrigan/Djalma;
- crystal-ball mode;
- Love mode = two-person birth-date numerology compatibility;
- deterministic astronomical/numerology facts must be separated from narrative interpretation;
- web method routing/input validation now represents `lunar_divination`, `runes`, `lunar_cards`, `crystal_ball`, and `love_numerology`, while methods without an evidenced engine remain unavailable.

Still required before production acceptance:
- complete Selene rune symbol dictionary;
- selected lunar/oracle card deck, meanings and deployable licensed/provenanced assets;
- crystal-ball mechanics/state mapping;
- exact numerology reduction rules and compatibility mapping;
- deterministic lunar-state calculation/data source validation where exact real lunar facts are displayed.

### Al-Hakim

Established:
- astrology/star-divination identity;
- complete natal input = birth date + time + place;
- deterministic chart facts separated from narrative interpretation;
- Al-Hakim-specific cards;
- constellation, nebula and horoscope/chart visual requirements;
- web method routing/input validation now represents `natal_astrology`, `cards`, and `horoscopes`, including date/time/place validation for natal input.

Still required before production acceptance:
- selected astrology school/ruleset;
- house system if houses are used;
- aspect/orb rules if aspects are used;
- ephemeris/astronomical calculation source and validation;
- transit/forecast rules where used;
- incomplete birth-data behavior;
- Al-Hakim card deck/mappings;
- deployable astronomy/card visual assets with provenance/licensing.

## Why this remains a blocker

- Test fixtures and web routing metadata must not be promoted silently to production knowledge.
- AI/Codex must not invent missing symbolic dictionaries, decks, astrology rules or licensing provenance.
- Production orchestration/API integration should use complete, traceable inputs rather than placeholders presented as final knowledge.
- Runtime/Pi4 acceptance must test the completed production chain, not only previously validated component fixtures or web-routing contracts.

## Next repository-safe action

No autonomous Worker implementation is justified for the still-missing production knowledge itself. When new owner/source authority or licensed/provenanced production data appears, Scout should reconcile only the affected gap against the current target repository and cite the exact target file/commit rather than duplicate it.

After the required production data for an implementation slice is evidenced, that slice may become `READY_FOR_WORKER` for repository implementation/tests. Pi4 deployment/runtime validation remains a later human-gated Codex step after repository Reviewer PASS where required.

## Hygiene

No disposable target-repository working files were introduced by this reconciliation. WORKSHOP keeps the blocker as the single concise coordination record; the authoritative implementation and tests remain in the target repository. Git history provides rollback for the target changes and this blocker update.
