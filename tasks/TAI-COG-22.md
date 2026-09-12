# TAI-COG-22

TYPE: WORKSHOP ENGINEERING / IMPLEMENTATION-READY UNIT

Objective: build the bounded TANGRA Experience Store over reviewed COG-00..21 dependencies.

Required constraints: immutable historical ExperienceRecord; exact lifecycle RAW_EVIDENCE -> CANDIDATE_LESSON -> VALIDATED_EXPERIENCE -> CANONICAL_SYSTEM_KNOWLEDGE; no automatic promotion; explicit transition lineage; outcomes IMPROVED / NO_MEASURABLE_VALUE / REGRESSED / INCONCLUSIVE / UNKNOWN; deterministic bounded retrieval; duplicate suppression; zero authority; COG-01 remains raw airborne recorder; MISSION_CONSTRAINED unsupported; no DB/vector/embedding/LLM/runtime integration.

Engineering repository: nevincho/TANGRA-2.0
Branch: tai-cog-22
Base reviewed COG-21: 7d8e4d2804ef9f59dd33f206fb490c2ae9f9ab37
