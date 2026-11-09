# Planner — TANGRA-FC-SA-02-01

STATUS: IMPLEMENTATION_READY
MODE: STANDALONE_SOFTWARE_ENGINEERING
DATE: 2026-11-09

## Objective

Create a portable command arbitration module that selects one bounded high-level control setpoint from source-tagged inputs and guarantees safety ownership.

## Interfaces

Input: `SourceCommand`.
Output: `ArbitrationDecision`.
Clock: caller-supplied monotonic milliseconds.
Local FC binding: `INTEGRATION_ADAPTER_REQUIRED`.

## Required reuse / protection

Reuse documented Mission Lifecycle v1 contract only as adjacent state supervision; do not modify or recreate it.
Do not implement live Pi protocol, motors, ESC output, arming, reconnect/resync, navigation or STEP_3+ behavior.

## Deterministic authority

SafetyOverride > BenchTest > PiSupervisor > SimulatedAutonomy.
Safety override with `force_safe` always produces safe fallback.

## Validation

Host compile plus deterministic tests for:
- empty fallback;
- source precedence and preemption;
- safety override;
- expiry/stale rejection;
- invalid/non-finite rejection;
- stale sequence rejection;
- clamping/observable selected source.

## Acceptance

All tests PASS; no physical-output interface; local integration explicitly remains NOT_YET_PERFORMED.
Rollback: remove the standalone package/checkpoint; no production state is changed.
