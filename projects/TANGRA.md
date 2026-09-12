# TANGRA — WORKSHOP Project Profile

PRIORITY: 1 — HIGHEST WHEN ACTIVE
CANONICAL REPOSITORY: `nevincho/TANGRA-DOCS`
PROJECT_STATE: LIMITED_REACTIVATION
ACTIVE_CAMPAIGN: WIDE-EW
REACTIVATED: 2026-09-12
REACTIVATION_AUTHORITY: Vlad explicit Control Room authorization
SCOPE: WIDE V3 Early-Warning / WIDE-EW campaign only
DEFAULT MODE OUTSIDE ACTIVE_CAMPAIGN: HOLD / OFFLINE
AUTONOMOUS IMPLEMENTATION: AUTHORIZED ONLY FOR REPOSITORY-SAFE AI WORKSHOP ENGINEERING WITHIN WIDE-EW; NO Pi5/production integration.

## Active campaign rule
TANGRA is reactivated only for the WIDE V3 Early-Warning / WIDE-EW campaign. WORKSHOP may create, queue, execute, test, review, checkpoint and persist repository-safe engineering artifacts required by this campaign.

Forbidden during this limited reactivation:
- unrelated TANGRA campaigns;
- Codex dispatch;
- Pi5/production integration or modification;
- production authority changes;
- modification/redesign of protected HQ detector, NanoTracker, CA Kalman, CurrentTargetManager, HOROS authoritative target path, camera calibration authority, LoRa/EDGE LINK, navigation/mission authority.

## Campaign objective
Transform WIDE IMX708 into a minimal low-resource early-warning sensor:
`WIDE -> cheap motion observation -> approximate direction/sector -> MOTION_HINT`
while eliminating or blocking obsolete WIDE processing and telemetry that no longer provides useful system value.

HQ remains sole authoritative vision chain:
`HQ -> Hailo detector -> NanoTracker -> CA Kalman -> CurrentTargetManager -> HOROS`.

WIDE has no authority for target detection/confirmation, tracking, metric range, HOROS target XYZ, 3D mapping, navigation or mission authority.

## Agent rules
- Inspect current canonical repository/runtime evidence before conclusions.
- Preserve validated/production components and interfaces.
- Do not infer Pi5 production/runtime paths from memory.
- Do not convert reported validation into current state without repository/runtime evidence.
- Detect phase mismatch, duplicated work and invalid validation methodology before proposing implementation.
- Missing evidence is NOT VERIFIED.

## Runtime/host
Production/Pi5 integration remains prohibited for WIDE-EW Workshop engineering. Runtime facts may be consumed from existing authoritative evidence; no live Pi5 action is authorized.

## Codex
No Codex work is authorized during the WIDE-EW Workshop campaign. Codex integration may be considered only after FINAL WORKSHOP PASS and separate human authorization.
