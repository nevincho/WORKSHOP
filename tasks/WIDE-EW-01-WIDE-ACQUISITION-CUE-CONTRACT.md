# WIDE-EW-01 — WideAcquisitionCue Contract + Non-Metric Cue Generation

PROJECT: TANGRA
CAMPAIGN: WIDE Acquisition Cue / Orientation
STATUS: IN_PROGRESS
TYPE: ENGINEERING / CONTRACT + REFERENCE IMPLEMENTATION + DETERMINISTIC TESTS
CODEX: FORBIDDEN
PRODUCTION/Pi5 MODIFICATION: FORBIDDEN

## Objective
Create and independently validate the minimum non-authoritative `WideAcquisitionCue` required by accepted WIDE-EW-00 architecture.

Accepted path:
`WIDE observation -> WideAcquisitionCue -> MC1 gate -> M1 acquisition decision -> M2 ORIENT_OBSERVATION_AXIS -> M3 high-level orientation representation -> carrier/FC adapter -> physical orientation -> HQ confirmation/rejection`.

N1 is not part of pre-confirmation acquisition.

## Scope
- Inspect only current WIDE capture/latest-frame evidence and the exact future MC1/M1 ingress boundary.
- Define minimum cue contract.
- Produce cheapest deterministic non-neural cue generator.
- Keep geometry non-metric.
- Use bounded persistence and latest-only state.
- Validate STATIC, LEFT, CENTER, RIGHT, TRANSIENT_NOISE and STALE cases.
- Benchmark reference implementation sufficiently to characterize processing cost, clearly separating host benchmark from Pi5/runtime evidence.

## Allowed cue semantics
Only fields justified by the consumer boundary: source/provenance, timestamp/freshness, normalized x/y, signed normalized horizontal offset, sector, motion area/magnitude, bounded quality, persistence. No metric bearing/range/XYZ/target identity/tracker identity/class.

## Fail-closed
Reject unavailable frame, malformed frame/coordinates, insufficient motion, insufficient persistence, stale cue, processing error or unsupported source/provenance. No direct FC/M1/M2/M3 action is produced by this unit.

## Protected
No changes to HQ detector, NanoTracker, CA Kalman, CurrentTargetManager, HOROS, N1, FC, command-send authority or production. No M1/M2/M3 implementation changes in this unit.

## Deliverables
- `handoffs/WIDE-EW-01/wide_acquisition_cue.py`
- `handoffs/WIDE-EW-01/test_wide_acquisition_cue.py`
- `evidence/WIDE-EW-01/RESULT.md`
- `review/WIDE-EW-01.md`

## Acceptance
PASS only if exact schema/provenance/freshness semantics, deterministic generation, bounded temporal filtering, fail-closed behavior, required synthetic tests, measured resource cost and exact future MC1/M1 ingress boundary are all present and independently reviewable.

## STOP
After independent review verdict, STOP. Do not start WIDE-EW-02.