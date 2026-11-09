# TANGRA-FC-SA-02-01 — Scout evidence

DATE: 2026-11-09
CAMPAIGN: TANGRA-FC-SOFTWARE-AUTONOMY
SCOUT_RESULT: READY_FOR_PLANNER
MODE: STANDALONE_SOFTWARE_ENGINEERING

## Reconciliation

Human decision establishes that Windows-local FC source access is not required for this campaign's standalone software creation. Unknown local internals are an integration concern and must be represented by explicit adapter contracts.

Authoritative architecture remains Pi5 <-> USB/MAVLink <-> custom ESP32 FC, with physical output and arming OFF. Mission Lifecycle v1 is COMPLETE and protected.

## STEP_2 actual standalone gap

No existing WORKSHOP package was found implementing the requested command-source arbitration contract. Duplicate risk for a WORKSHOP standalone implementation is therefore acceptable; compatibility with unknown local FC internals remains NOT VERIFIED.

## Smallest useful boundary

Portable C++17 module providing:
- source-tagged commands;
- deterministic priority/preemption;
- stale/invalid rejection;
- timeout/fallback;
- SafetyOverride highest authority;
- selected-source observability;
- deterministic host tests.

Local controller/clock/safety bindings are `INTEGRATION_ADAPTER_REQUIRED`.

## Protected / deferred

No Mission Lifecycle rewrite. No STEP_8 transport behavior. No motor/ESC/arming. No production Pi5 modification.

NEXT_ROUTE: PLANNER
