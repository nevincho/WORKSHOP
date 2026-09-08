# M2 Passive Guidance Decision / Translation Layer — Evidence

TASK_ID: TASK-TANGRA-MISSION-GUIDANCE-M2-20260908
STATUS: RE-REVIEW
BASE_M1_REVIEWED: 88ffcf4932545304c5a82c83c65ad01b99000680
BASE_M1_COMPLETE_METADATA: 4fc48e0a8bcb25807e84dd94d9e2c7c22ffd5cbd
SCOPE: PASSIVE/SHADOW/non-authoritative translation only. No production integration. HOROS TASK8 untouched.

INPUT_CONTRACT: exact frozen M1 MissionDecision object + optional NavigationEvidence + evaluated_at. Tests load the real frozen M1 implementation from its repository path. M2 validates version M1_SHADOW_V1 and production_authority=False.

OUTPUT_CONTRACT: PassiveGuidanceDecision exposes GuidanceState {AVAILABLE,DEGRADED,SUPPRESSED}, semantic GuidanceIntent {NO_GUIDANCE,HOLD,ABORT_HOLD,MAINTAIN_OBSERVATION,REACQUIRE_TARGET,MOVE_RELATIVE,SET_ALTITUDE,SET_HEADING}, identity/time/frame, unchanged metric status, preserved source M1 state/action/reason, optional movement fields, reason/provenance and production_authority=False.

M1_TO_M2: NO_ACTION->NO_GUIDANCE; HOLD->HOLD; ABORT->ABORT_HOLD semantic only; MISSION_COMPLETE->HOLD; OBSERVE_TARGET/MAINTAIN_TRACK->geometry-gated MAINTAIN_OBSERVATION or NO_GUIDANCE; REACQUIRE->REACQUIRE_TARGET; TARGET_LOST without REACQUIRE->SUPPRESSED. M1 DEGRADED is never promoted above M2 DEGRADED.

GEOMETRY_GATING: target/frame/timestamps must match and be fresh. LOST suppresses navigation except semantic REACQUIRE. Metric mismatch suppresses. UNUSABLE/CONFLICT/INVALID=>DEGRADED/HOLD. NOT_VERIFIED=>DEGRADED without movement authority. Missing/non-finite target/carrier/search geometry, heading, altitude or uncertainty fails closed. Missing carrier pose cannot produce world-frame movement. M2 does not derive MOVE_RELATIVE/SET_ALTITUDE/SET_HEADING from target XYZ alone. Explicit search_relative_vector_m may be preserved only for VERIFIED REACQUIRE evidence; no search trajectory is generated.

REVIEW_CYCLE_1: candidate b19d5dd50c4593dd55a6ca474738fb1a34d98786 PASS_WITH_CONDITIONS — M1 DEGRADED could be promoted to M2 AVAILABLE. Corrected M2-only in 832579d4da702ad8146fb2bec37d686f3cb77465.
REVIEW_CYCLE_2: 832579d4da702ad8146fb2bec37d686f3cb77465 PASS_WITH_CONDITIONS — output did not explicitly preserve source M1 state/action/reason. Corrected M2-only by adding source_mission_state/source_mission_action/source_mission_reason.

VALIDATION: 31/31 HOST deterministic tests PASS after cycle-2 correction, including source-context preservation, no downstream DEGRADED promotion, no fabricated movement-coordinate audit and no control-side-effect audit.

PERFORMANCE: HOST only n=100000 mean=0.00549206273 ms median=0.005227 ms p95=0.005418 ms max=0.843524 ms. Pi5/E2E NOT_VERIFIED.

CONTROL_SIDE_EFFECTS: NONE. No serial/socket/radio/hardware/control imports or UART, LoRa, ESP-NOW, PWM, DShot, PID, mixer, ESC, ARM, TAKEOFF, LAND, payload or actuation behavior.

PRODUCTION_GATES NOT_VERIFIED: production M1 runtime integration; production M2 integration; exact production navigation inputs; Pi5 E2E; Master ESP32 transport; Flight Controller command acceptance; physical flight behavior.

KNOWN_LIMITATIONS: no autonomous intercept/search trajectory or observation-offset policy. stale_after_s=0.5 and degrade_uncertainty_m=5.0 are SHADOW test defaults only. Future high-level command-boundary work remains separate.
