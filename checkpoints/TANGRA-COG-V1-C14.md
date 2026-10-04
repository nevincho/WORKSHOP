# TANGRA C14 — QUALIFIED CHECKPOINT

DATE: 2026-10-04
TASK_ID: C14
STATE: WORKSHOP_QUALIFIED_WITH_LIMITATIONS
C14_RESULT: PASS_WITH_LIMITATIONS
SCOPE_QUALIFIER: REPOSITORY_AND_SIMULATION_ONLY
REVIEW: PASS_WITH_LIMITATIONS
AUTHORITY: NONE
OPERATIONAL_AUTHORITY: []

TARGET_REPOSITORY: nevincho/TANGRA-2.0
BRANCH: tangra-cog-v1-c14-longitudinal
QUALIFIED_HEAD: 6cd6cee4e99557c8f8ca78205c46e0d0ae673403
BASE: tangra-cog-v1-c13-bulgarian-quality@db4caf931c6f4947d5eaef8665c3bb7234caf973

## Qualified evidence

- 18 synthetic controlled longitudinal scenarios A-R.
- Scenario provenance is explicitly SIMULATION / SYNTHETIC_CONTROLLED / production=false.
- Experience creation, duplicate behavior, contradiction handling, staleness, restart/reload, corrupt snapshots, lifecycle review, Experience->Self-Model references, Self-Model state changes, authority and scale were exercised.
- No live production runtime was accessed.

## Defect repaired

EXPERIENCE_PERSISTENCE_DEFECT:
valid promoted lifecycle records could fail snapshot save/reload when canonical lexical ID order placed children before predecessors.

Repair:
COG-22 from_fixture now resolves dependency-ready records in bounded passes, preserves snapshot schema/export ordering, and rejects unresolved/orphan/cyclic chains.

Regression:
promoted RAW -> CANDIDATE -> VALIDATED chain with deliberately adverse lexical IDs roundtrips exactly.

## Authoritative test evidence

GitHub Actions run: 37215455433
Result: SUCCESS

- C14 longitudinal suite: 16/16 PASS
- Experience integration regressions: 32/32 PASS
- reviewed COG-22: 37/37 PASS
- reviewed COG-30: 15/15 PASS
- reviewed COG-26: 37/37 PASS
- TOTAL: 137 PASS / 0 FAIL

Repository/simulation scale sample:
- records 256
- snapshot 235221 bytes
- save 50.704 ms
- load 38.082 ms
- query 0.172 ms
- tracemalloc peak 337319 bytes
- query cap 100
- production=false

## Remaining limitations

EXPERIENCE_STALENESS_LIMITATION:
- no age/decay/expiration policy;
- COG-30 disposition state is not durable across restart.

NOT_SPECIFIED_BY_CURRENT_CONTRACT:
- automatic Experience conflict winner/reconciliation;
- durable COG-30 policy-state import/reconstruction;
- COG-26 referential validation of experience_refs;
- longitudinal confidence accumulation in COG-26.

These limitations did not create false current-state override, evidence fabrication, false certainty or authority acquisition in the qualified simulation.

## Self-Model conclusion

COG-26 is a deterministic stateless assembler, not a learning engine:
- UNKNOWN remains UNKNOWN when supplied;
- current supplied state remains current;
- old Experience refs do not override it;
- no confidence/global score is accumulated;
- invalid authority input is rejected;
- authority remains NONE.

## Final delta

- integrated COG-22 store.py — 5ea1bc96d35cae16191aea161b59203d16956246
- C14 scenarios JSON — f31a18ffef29e6bca1c44dd9d518b340753257d6
- C14 qualification test — 4659b2a0e5cc8d43c2b4a1ec3025fd58e8f0d1c7
- foundation COG-22 store.py — 5ea1bc96d35cae16191aea161b59203d16956246
- foundation COG-22 regression test — 050e5ba0dd9ead1713326dc4e687f9732c443698
- foundation COG-26 source-test contract repair — 939359977e54dc5d2e785a92464e9a2d5b36fb0f

Temporary workflow removed.

## Live boundary

LIVE_PRODUCTION_LONG_TERM_QUALIFIED: NO

Future separate gate:
C14-LIVE-LONGITUDINAL-01, only when an authorized production execution route exists.

FINAL:
PASS_WITH_LIMITATIONS / REPOSITORY_AND_SIMULATION_ONLY
