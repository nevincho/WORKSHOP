# TANGRA C14 — WORKER EVIDENCE

DATE: 2026-10-04
TASK_ID: C14
MODE: SIMULATION_AND_REPOSITORY_QUALIFICATION
RESULT: PASS_WITH_LIMITATIONS
SCOPE_QUALIFIER: REPOSITORY_AND_SIMULATION_ONLY
LIVE_PRODUCTION: NOT EXECUTED
AUTHORITY: NONE
OPERATIONAL_AUTHORITY: []

## Base and candidate

BASE:
nevincho/TANGRA-2.0:tangra-cog-v1-c13-bulgarian-quality@db4caf931c6f4947d5eaef8665c3bb7234caf973

CANDIDATE:
nevincho/TANGRA-2.0:tangra-cog-v1-c14-longitudinal@6cd6cee4e99557c8f8ca78205c46e0d0ae673403

No Raspberry Pi or production runtime was accessed.

## Repository audit

COG-22:
- immutable ExperienceRecord schema;
- explicit lifecycle chain RAW_EVIDENCE -> CANDIDATE_LESSON -> VALIDATED_EXPERIENCE -> CANONICAL_SYSTEM_KNOWLEDGE;
- deterministic semantic hash and exact duplicate handling;
- explicit mission/subsystem/evidence/diagnostic/correlation/hypothesis/interpretation/signal/configuration references;
- explicit provenance;
- outcome UNKNOWN supported and preserved;
- no scalar confidence mechanism;
- no automatic promotion;
- bounded ExperienceStore and bounded query limit;
- durable COG-22 snapshot adapter uses exact export_fixture()/from_fixture() representation.

COG-30:
- disposition ACTIVE/SUPERSEDED/DEPRECATED/INVALIDATED;
- explicit reviewed disposition/canonical actions only;
- policy state remains in-memory;
- policy-state persistence/import is not part of the current qualified contract.

COG-26:
- 15 domains;
- deterministic stateless aggregation of supplied state;
- no history-learning/confidence accumulation/decay engine;
- no global confidence/health score;
- Experience refs are carried as refs and are not dereferenced;
- authority hard-bounded to NONE.

## Simulation set

18 controlled scenarios A-R were added.
Every scenario explicitly declares:
- synthetic mission/session id;
- synthetic timestamp;
- source;
- evidence class;
- realism class SYNTHETIC_CONTROLLED;
- provenance C14_REPOSITORY_SIMULATION;
- expected behavior;
- production=false.

## Defect discovered before repair

EXPERIENCE_PERSISTENCE_DEFECT.

A valid in-memory promoted chain could fail durable snapshot save/reload.

Root cause:
- export_fixture() intentionally emits canonical records sorted lexically by experience_id;
- from_fixture() previously replayed that lexical order;
- lifecycle child records require their superseded predecessor to exist first;
- a CANDIDATE/VALIDATED ID can sort before a valid RAW predecessor ID;
- therefore persistence correctness depended on identifier lexical ordering rather than lifecycle dependency.

Observed on pre-fix C14 run 37215158266:
- C14: 15 PASS / 1 FAIL;
- only remaining failure was promoted Experience snapshot roundtrip.

## Minimal repair

Changed only ExperienceStore.from_fixture() in the mirrored reviewed COG-22 implementation copies.

New behavior:
- parse all records first;
- replay RAW/dependency-ready records in bounded passes;
- defer lifecycle children until superseded predecessor exists;
- reject orphan/cyclic/unresolvable record sets if no progress can be made;
- preserve snapshot schema;
- preserve export_fixture canonical lexical representation;
- preserve append/transition validation and semantic dedup semantics.

Added promoted-chain lexical-order regression.

No conflict policy, decay policy, lifecycle policy or authority semantics were added.

## Qualification behavior

PASS:
- exact duplicates remain bounded and do not increase record count;
- contradictory records remain separate immutable evidence;
- correlation/hypothesis refs do not become causal facts;
- missing/UNKNOWN supplied Self-Model state remains UNKNOWN;
- current supplied PASS state is not overridden by historical Experience refs;
- temporary DEGRADED -> later PASS is represented by later supplied state;
- stale Experience remains timestamped and can be filtered;
- corrupt/truncated snapshot is rejected;
- promoted chain survives snapshot restart/reload after repair;
- identity/provenance/semantic hash are preserved;
- non-existent COG-26 Experience ref does not fabricate capability/subsystem/authority state;
- duplicate COG-26 Experience refs do not amplify confidence because no confidence mechanism exists;
- non-NONE capability/communication authority inputs are rejected;
- final authority remains NONE.

## Policy limitations

EXPERIENCE_STALENESS_LIMITATION:
- no automatic age/decay/expiration policy;
- old Experience may remain stored until capacity bound;
- COG-30 disposition state is not persisted across restart.

NOT_SPECIFIED_BY_CURRENT_CONTRACT:
- durable restoration of COG-30 policy state;
- automatic contradiction winner/conflict reconciliation;
- referential-integrity verification of COG-26 experience_refs;
- longitudinal confidence accumulation/maturation in COG-26.

These limitations did not produce evidence corruption, false current-state override, false confidence or authority acquisition in the qualified simulation.

## Scale evidence

Repository/GitHub CI simulation only:
- records: 256
- snapshot_bytes: 235221
- build_ms: 69.174
- save_ms: 50.704
- load_ms: 38.082
- query_ms: 0.172
- tracemalloc_current_bytes: 330016
- tracemalloc_peak_bytes: 337319
- configured store bound in scenario: 256
- query limit: 100

Overflow failed closed; no silent eviction/duplication.

## Authoritative qualification

GitHub Actions run 37215455433: SUCCESS

- C14 longitudinal: 16/16 PASS
- Experience persistence/retrieval/lifecycle integration: 32/32 PASS
- reviewed COG-22 source: 37/37 PASS
- reviewed COG-30 source: 15/15 PASS
- reviewed COG-26 source: 37/37 PASS

TOTAL: 137 PASS / 0 FAIL.

Earlier test-only failures:
- outdated DiagnosticResult fixture signature;
- noncanonical RealismClass fixture value;
- old COG-26 source-test DiagnosticResult signature.
Classification: TEST_HARNESS_DEFECT. Repaired in tests only.

## Final repository delta

- TAI_COGNITIVE_INTEGRATION_PACKAGE/cognitive/experience/tangra_experience_store/store.py
  blob 5ea1bc96d35cae16191aea161b59203d16956246
- TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/quality/c14_longitudinal_scenarios.json
  blob f31a18ffef29e6bca1c44dd9d518b340753257d6
- TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/quality/test_c14_longitudinal_qualification.py
  blob 4659b2a0e5cc8d43c2b4a1ec3025fd58e8f0d1c7
- TANGRA_2_0/00_FOUNDATION/TAI_COG_22/tangra_experience_store/store.py
  blob 5ea1bc96d35cae16191aea161b59203d16956246
- TANGRA_2_0/00_FOUNDATION/TAI_COG_22/tests/test_store.py
  blob 050e5ba0dd9ead1713326dc4e687f9732c443698
- TANGRA_2_0/00_FOUNDATION/TAI_COG_26/tests/test_self_model.py
  blob 939359977e54dc5d2e785a92464e9a2d5b36fb0f

Temporary workflow removed.

FINAL:
PASS_WITH_LIMITATIONS / REPOSITORY_AND_SIMULATION_ONLY
