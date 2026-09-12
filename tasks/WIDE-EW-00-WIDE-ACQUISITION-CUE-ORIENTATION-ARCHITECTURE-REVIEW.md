# WIDE-EW-00 — WIDE Acquisition Cue → Mission/Guidance → FC Orientation Architecture Review

PROJECT: TANGRA
CAMPAIGN: WIDE Acquisition Cue / Orientation
STATUS: COMPLETE
TYPE: ARCHITECTURE REVIEW
CODEX: FORBIDDEN
PRODUCTION/Pi5 MODIFICATION: FORBIDDEN

## Objective
Determine the minimum architecture required for WIDE IMX708 to serve as a non-authoritative early-acquisition sensor that can request safe reorientation of the authoritative HQ observation axis through the existing mission/guidance/FC abstraction.

## Protected authority
`HQ -> primary detector -> NanoTracker -> CA Kalman -> CurrentTargetManager -> HOROS` remains unchanged.

WIDE shall not become authoritative detector/classifier/tracker/range/HOROS/FC/navigation authority.

## Required evaluation
Bounded review of current repository evidence for WIDE, CurrentTargetManager/HOROS, MC1, M1, N1, M2, M3, FC/carrier abstraction and orientation/high-level command semantics. Determine minimum cue contract, insertion point, state transitions, fail-closed rules, redundant WIDE path candidates and whether the architecture fits existing contracts or needs bounded extension.

## Constraints
Architecture review only. No implementation, telemetry removal, production changes, Codex, Pi5 integration, FC activation, motor/servo commands, command-send enablement, HQ authority changes, invented metric authority or broad TANGRA audit.

## Evidence
`evidence/WIDE-EW-00/ARCHITECTURE_REVIEW.md`

## Control Room review
`review/WIDE-EW-00.md`

## STOP
Stop after Control Room review. Do not start WIDE-EW-01 or integration work.