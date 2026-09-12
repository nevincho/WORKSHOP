# WIDE-EW-00 — Architecture Review Evidence

DATE: 2026-09-12
VERDICT: REQUIRES_BOUNDED_EXTENSION
MODE: REPOSITORY-GROUNDED / ARCHITECTURE ONLY

## CURRENT_WIDE_ROLE
Current verified camera mapping is IMX708 WIDE on camera 0 and IMX477 HQ+50mm on camera 1. HQ is the authoritative detection/tracking camera. WIDE is secondary. Current 2026-09-09 checkpoint records WIDE capture available, latest-only worker preserved, WIDE detector observations publishable, environment/Video3D disabled by default, and HQ authority unchanged.

Relevant current evidence:
- `REPORTS/CAMERA_AUTHORITY_AND_MAPPING_AUDIT_2026-09-04.md`
- `REPORTS/TANGRA_PROGRESS_CHECKPOINT_2026-09-09.md`
- `ARCHITECTURE/TANGRA_PRE_FREEZE_ARCHITECTURE_AUDIT_20260909.md`
- `ARCHITECTURE/HOROS_SURVEYED_LANDMARK_METRIC_MAP_DECISION_20260908.md`

The active continuous WIDE 3D/light environment-mapping workload is already identified as a retirement candidate because of high cost/staleness and is not required for the acquisition-cue role.

## EXISTING_MISSION_CHAIN
Current integrated passive mission chain:
`MC1 -> M1 -> N1 -> M2 -> M3`

Protected perception authority:
`HQ IMX477 -> primary detector -> NanoTracker -> CA Kalman -> CurrentTargetManager -> HOROS`

MC1 owns mission activation/operator intent/system readiness/safety availability. M1 decides mission state without control authority. N1 only converts trustworthy CurrentTarget/HOROS geometry into M2 NavigationEvidence. M2 remains passive guidance. M3 remains passive representation-only high-level command contract with no transport/FC authority.

## REUSABLE_COMPONENTS
- MC1: REUSE_AS_IS as mission/safety/intent gating authority.
- M1: BOUNDED_EXTENSION. Existing mission-decision role is the correct place to decide whether a non-authoritative WIDE cue justifies acquisition/orientation, but current documented inputs are MC1 plus matching CurrentTarget/HOROS evidence; pre-confirmation WIDE cue is not CurrentTarget/HOROS evidence.
- N1: REUSE_AS_IS and BYPASS for pre-confirmation acquisition. N1 explicitly requires trusted authoritative CurrentTarget/HOROS metric semantics and must not be used to legitimize WIDE pre-confirmation geometry.
- M2: BOUNDED_EXTENSION. Existing guidance role is appropriate for converting an accepted acquisition decision into a carrier-independent orientation intent, but current documented TRACK navigation semantics do not establish a LOOK/ORIENT cue contract.
- M3: BOUNDED_EXTENSION. Existing high-level command representation is the correct downstream semantic boundary, but repository evidence does not prove a frozen LOOK/ORIENT/observation-axis command type exists.
- FC/carrier boundary: REUSE_AS_IS conceptually. Current FC architecture already requires high-level commands only, keeps motor/PWM authority inside FC, and lists `SET_HEADING` as an allowed high-level example for multirotor realization. Carrier-specific realization must remain adapter-side.

## MISSING_BRIDGE
One minimal pre-confirmation acquisition bridge is required between WIDE observation and M1 mission decision.

Required semantic role:
`WideAcquisitionCue` = non-authoritative, expiring sensor cue. It must never instantiate CurrentTarget, HOROS target state or NavigationEvidence.

No second mission architecture is required.

## PROPOSED_DATA_FLOW
`WIDE capture/cheap motion observation`
`-> WideAcquisitionCue`
`-> MC1 authority gate + M1 acquisition decision`
`-> M2 carrier-independent ORIENT_OBSERVATION_AXIS intent`
`-> M3 high-level orientation request representation`
`-> carrier/FC adapter`
`-> platform-specific bounded realization (e.g. yaw / gimbal / turret / heading)`
`-> HQ FOV moves`
`-> HQ detector confirms or rejects`
`-> on confirmation: existing CurrentTargetManager/HOROS mission chain resumes`

WIDE never feeds N1 as authoritative navigation evidence before HQ confirmation.

## ACQUISITION_CUE_CONTRACT
Minimum justified non-metric contract:
- `schema_version`
- `cue_id` — needed to correlate attempt/timeout/repeated-false-cue suppression
- `source` — fixed identity/provenance, e.g. WIDE_IMX708
- `timestamp_monotonic` or equivalent source timestamp
- `max_age`/expiry or an equivalent freshness contract
- `image_x_norm`
- `image_y_norm`
- `sector`
- `quality` or bounded confidence score only if produced by the actual cue detector
- `persistence` only if used by the acquisition gate
- `provenance/status`

Do not require metric bearing, range, XYZ, target ID, tracker ID, class or velocity.

WIDE bearing/angular offset: NOT_VERIFIED for this review because verified current WIDE geometry/extrinsics sufficient for metric orientation conversion were not established by the inspected current evidence. First-stage cue therefore remains normalized image position / sector / signed image offset.

## INSERTION_POINT
Correct insertion is a minimal cue adapter immediately upstream of M1 acquisition decision, gated by MC1. Do not route pre-confirmation WIDE cue through CurrentTargetManager, HOROS or N1.

Reason:
- MC1 already owns mission/safety readiness gates.
- M1 already owns mission-level state decisions without control authority.
- N1 requires authoritative CurrentTarget/HOROS geometry and exact carrier-relative metric semantics.
- M2/M3 are downstream guidance/command-representation layers and should receive an accepted mission decision, not raw WIDE perception.

## M1_ROLE
Add only one bounded acquisition decision semantic:
- if MC1 permits acquisition and no authoritative HQ target conflicts, evaluate a fresh valid WIDE cue;
- produce ACQUIRE/ORIENT decision referencing the cue ID;
- do not create a target identity;
- do not assign metric geometry;
- timeout/reject deterministically.

## N1_ROLE
Unchanged.
N1 remains exclusively the trusted adapter from authoritative CurrentTarget/HOROS geometry into M2 NavigationEvidence. It is not part of pre-confirmation WIDE cueing. After HQ confirms and authoritative CurrentTarget/HOROS state exists, normal N1 behavior may resume.

## M2_ROLE
Translate an accepted acquisition decision into carrier-independent guidance semantic equivalent to:
`ORIENT_OBSERVATION_AXIS toward signed non-metric image offset/sector`

M2 must not convert WIDE image offset into arbitrary metric bearing. If a later verified camera/carrier transform exists, that can be a separately reviewed extension.

## M3_ROLE
Represent the accepted orientation request as a bounded, expiring high-level command intent. M3 remains representation-only/passive until later authorized integration. The request must identify intent, source decision/cue, expiry, and required capability, without motor/servo semantics.

## FC_CARRIER_BOUNDARY
Required semantic boundary:
`orient authoritative observation axis toward direction/cue X`

Carrier adapter chooses platform realization:
- multirotor: bounded yaw/heading request where capability is verified;
- gimbal: pan/tilt;
- turret: pan;
- fixed-wing: bounded heading/course maneuver;
- unsupported platform: reject.

Current FC architecture explicitly keeps stabilization/PID/mixer/ESC authority in FC and allows high-level `SET_HEADING` as an example. Raspberry Pi must not emit PWM/motor commands.

Portability classification: ARCHITECTURALLY_DECOUPLED, not PORTABILITY_VALIDATED.

## HQ_CONFIRMATION_HANDOFF
Only HQ may convert acquisition into authoritative perception.

On HQ detection/confirmation:
`HQ -> NanoTracker -> CA Kalman -> CurrentTargetManager -> HOROS`
becomes authoritative exactly as today.

WIDE cue ID may remain diagnostic provenance only. It must not become CurrentTarget identity.

If HQ fails to confirm before acquisition timeout, no authoritative target is created and the system returns to SEARCH.

## STATE_TRANSITIONS
Nominal:
`SEARCH`
`-> fresh valid WIDE candidate`
`-> ACQUIRE_PENDING`
`-> ORIENTING`
`-> HQ candidate enters FOV`
`-> HQ CONFIRMS`
`-> existing authoritative TRACK path`

Reject path:
`SEARCH -> WIDE candidate -> ACQUIRE_PENDING/ORIENTING -> HQ NO_CONFIRM -> timeout/reject -> SEARCH`

Conflict path:
If HQ already owns an authoritative current target, WIDE acquisition cue is suppressed/ignored for orientation authority. Existing HQ tracking/mission continuity wins.

Abort/safety path:
Any MC1 safety/mission invalidation, FC unavailability, stale cue or command expiry cancels acquisition and produces no orientation request.

## FAIL_CLOSED_RULES
Reject/suppress orientation when any applies:
- stale/expired WIDE cue;
- malformed/non-finite coordinates;
- unsupported source/provenance;
- insufficient quality/persistence when those gates are configured;
- mission inactive or MC1 authority invalid/incomplete;
- FC/carrier unavailable or required capability absent;
- HQ already tracking authoritative target or conflicting CurrentTarget exists;
- acquisition timeout;
- repeated false cue exceeds bounded retry policy;
- requested orientation exceeds carrier/profile envelope;
- command-send disabled;
- adapter cannot map cue semantics without inventing metric/bearing authority;
- missing carrier-relative observation-axis semantics;
- M2/M3 unsupported orientation semantic;
- any unknown state that current safety policy requires to be explicit.

No fallback to direct FC or motor/servo control.

## REDUNDANT_WIDE_PATH_CANDIDATES
Classification only for later task:
- WIDE capture/latest-value acquisition: KEEP.
- WIDE detector observation publication: REPLACE candidate if a cheaper motion/acquisition cue can satisfy the new role.
- active WIDE environment/Video3D processing: REMOVE_CANDIDATE / already disabled by default and already identified for retirement.
- WIDE continuous 3D/light map contribution: REMOVE_CANDIDATE.
- legacy `world_map_3d` WIDE-specific contribution: BLOCK_CANDIDATE pending exact dependency trace.
- WIDE telemetry with no consumer after cue adoption: REMOVE_CANDIDATE, exact fields NOT_VERIFIED in this bounded architecture review.

## ARCHITECTURAL_CONFLICTS
No fundamental conflict with the existing TANGRA separation of perception, mission/guidance and FC authority.

The conflict is contractual, not architectural: current frozen mission chain is target/HOROS-centric and does not document a pre-confirmation acquisition-cue input or carrier-independent LOOK/ORIENT semantic. Therefore direct reuse as-is would either misuse N1/CurrentTarget/HOROS authority or invent an unsupported command semantic.

## MINIMUM_REQUIRED_CHANGE
1. Add one versioned `WideAcquisitionCue` non-authoritative contract/adapter.
2. Bounded M1 extension for ACQUIRE/ORIENT decision state gated by MC1 and subordinate to existing HQ target authority.
3. Bounded M2 extension for carrier-independent `ORIENT_OBSERVATION_AXIS` guidance with non-metric cue semantics.
4. Bounded M3 extension for expiring high-level orientation intent representation, if repository inspection of the frozen M3 schema confirms no equivalent existing command type.
5. Later carrier-adapter binding to existing FC high-level capability contract; no actuator semantics in TANGRA core.
6. Keep N1 unchanged.

## VERDICT
REQUIRES_BOUNDED_EXTENSION

## NEXT_BOUNDED_WORKSHOP_TASK
WIDE-EW-01 should be redefined as a contract-design unit only: freeze the `WideAcquisitionCue` + M1 acquisition-decision + M2/M3 orientation-intent interface package and deterministic state-machine tests, with no runtime integration, no Pi5 and no Codex.

## Repository-grounding summary
Current-state evidence supports all core authority decisions above. Exact frozen M2/M3 schema field names and any existing orientation enum beyond documented behaviors remain NOT_VERIFIED in this review and must be inspected in the next bounded contract-design task before extending them.