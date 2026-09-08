# M1 Mission Management — Evidence

TASK_ID: TASK-TANGRA-MISSION-MANAGEMENT-GUIDANCE-M1-20260908
STATUS: REVIEW
SCOPE: isolated PASSIVE/SHADOW mission state + decision contract. No Guidance generation or production integration.

## Architecture authority
TANGRA_FLIGHT_CONTROL_ARCHITECTURE.md assigns AI/tracking/CA prediction/mission logic/guidance generation to Raspberry Pi; Master ESP32 owns communications/routing; Flight Controller ESP32 owns stabilization, safety, PID/mixer/ESC and final flight authority. M1 preserves this split and emits mission-level state only.

## Input contract
MissionInput preserves operator intent, authoritative target reference, timestamp/frame, lifecycle, optional authoritative XYZ/Vxyz/prediction, covariance, metric status, target class, freshness, provenance, optional externally supplied carrier pose, readiness and safety availability. Missing values are not fabricated.

## State model
IDLE, OBSERVE, TRACK, DEGRADED, TARGET_LOST, HOLD, MISSION_COMPLETE, ABORT.

Priority order: malformed/regressed input -> fail closed; operator ABORT/COMPLETE/HOLD; inactive mission; readiness/safety; freshness; target availability/identity; LOST; degraded/coasting/unusable metric; observed/no XYZ; valid observed/track.

A bounded 2-frame degradation policy prevents a single invalid frame from silently changing stable mission intent while still emitting DEGRADED immediately. Persistent degradation changes action to REACQUIRE. This is SHADOW test policy, not a production threshold.

## Output contract
MissionDecision emits state, mission-level action, target/timestamp/frame, unchanged metric status, reason/provenance, world-guidance-context availability, version and production_authority=False. Actions: NO_ACTION, OBSERVE_TARGET, MAINTAIN_TRACK, HOLD, REACQUIRE, MISSION_COMPLETE, ABORT.

No movement vector, trajectory, UART packet, PWM, DShot, PID, mixer, ESC or actuator field exists.

## Transition summary
- inactive -> IDLE / NO_ACTION
- OBSERVED -> OBSERVE / OBSERVE_TARGET
- valid authoritative estimated/predicted state -> TRACK / MAINTAIN_TRACK
- degraded/coasting/unusable/conflict/invalid -> DEGRADED; bounded transient OBSERVE_TARGET, persistent REACQUIRE
- LOST/no target -> TARGET_LOST / REACQUIRE
- stale/malformed/readiness unavailable -> HOLD / NO_ACTION or HOLD
- operator HOLD -> HOLD
- operator COMPLETE -> MISSION_COMPLETE
- operator ABORT -> ABORT
- target identity change -> OBSERVE new target; no continuity inherited

## Host validation
22/22 deterministic unittest cases PASS in isolated local execution.
Coverage: no mission; observed; tracked; degraded; transient degradation; stale; LOST; identity change; malformed XYZ; non-finite covariance; missing carrier pose; unavailable readiness; operator HOLD; ABORT; completion; NOT_VERIFIED propagation; timestamp regression; deterministic repeatability; valid carrier pose; forbidden side-effect import audit; unavailable-vs-negative freshness; persistent degradation.

## Performance
HOST only, 100000 fresh-manager decision evaluations:
mean 0.00472370047 ms; median 0.003275 ms; p95 0.003656 ms; max 60.227272 ms. The max is a host scheduling/runtime outlier and is not used as a Pi5 claim.

## Authority/failure audit
No detector/tracker/Kalman/HOROS/range/guidance/flight-control logic is implemented. No serial/network/radio/hardware library is imported. No control or transport side effect exists. Metric NOT_VERIFIED is copied unchanged. Carrier pose is optional and never estimated.

## Production gates
NOT_VERIFIED: Mission Management runtime integration; Guidance runtime integration; real carrier navigation behavior; Pi5 E2E performance; Master ESP32 command transport; Flight Controller command acceptance; physical flight behavior.

## Integration note
A future Guidance task may consume MissionDecision but must remain downstream and separately define high-level movement intent. M1 does not authorize Guidance implementation.

## Known limitations
Freshness 0.5 s and transient_degrade_frames=2 are explicit SHADOW/TEST defaults, not production-authoritative thresholds. CurrentTargetManager/HOROS executable source compatibility must be verified at future integration time. HOROS T8 remains untouched and blocked independently.
