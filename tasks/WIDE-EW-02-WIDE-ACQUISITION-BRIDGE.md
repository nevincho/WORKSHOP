# WIDE-EW-02 — WideAcquisitionCue → MC1/M1 Acquisition Bridge

PROJECT: TANGRA
CAMPAIGN: WIDE Acquisition Cue / Orientation
STATUS: COMPLETE
TYPE: ENGINEERING / MC1-M1 CONTRACT EXTENSION + DETERMINISTIC TESTS
CODEX: FORBIDDEN
PRODUCTION/Pi5 MODIFICATION: FORBIDDEN

## Objective
Integrate frozen WideAcquisitionCue v1 semantics into a bounded MC1/M1 acquisition bridge without touching M2, M3, FC, N1, HQ authority or production.

## Authoritative input
Frozen `WideAcquisitionCue v1` from WIDE-EW-01, non-metric only.

## Required flow
`WideAcquisitionCue -> acquisition bridge -> MC1 authority validation -> M1 acquisition decision`

N1 is excluded pre-confirmation.

## Scope
- inspect current documented MC1 authority boundary and M1 mission-decision boundary only;
- define and implement a repository-safe reference bridge package;
- enforce MC1 mission/readiness/safety gates and WIDE cue validation;
- implement only M1 SEARCH -> ACQUIRE / ORIENT_REQUEST_PENDING semantics plus deterministic timeout/reject return to SEARCH;
- suppress WIDE acquisition whenever authoritative HQ target is active;
- deterministic tests for LEFT/CENTER/RIGHT, stale, low quality, low persistence, malformed, mission inactive, HQ authoritative, timeout and return to SEARCH.

## Protected
No changes to HQ detector, NanoTracker, CA Kalman, CurrentTargetManager, HOROS, N1, M2, M3, FC/carrier adapter, command-send authority or production. No metric bearing/range/XYZ claims.

## Acceptance
PASS only if exact bridge contract, MC1 validation, M1 acquisition semantics, timeout/rejection, HQ conflict behavior, required tests and independent review are present and no downstream guidance/command authority is activated.

## Completion
Engineering evidence: `evidence/WIDE-EW-02/RESULT.md`.
Independent review: `review/WIDE-EW-02.md` — PASS.
Reference package:
- `handoffs/WIDE-EW-02/wide_acquisition_bridge.py`
- `handoffs/WIDE-EW-02/test_wide_acquisition_bridge.py`

## STOP
WIDE-EW-02 is complete. Do not start WIDE-EW-03 in this cycle.