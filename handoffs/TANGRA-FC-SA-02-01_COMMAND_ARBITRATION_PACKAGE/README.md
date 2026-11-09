# TANGRA FC STEP_2 — Command Arbitration Package

Standalone C++17 implementation package for command-source arbitration and Safety Supervisor ownership.

## Authority boundary

This package is not integrated into the Windows-local ESP32 FC. Integration status is `INTEGRATION_ADAPTER_REQUIRED`.

Abstract command sources:
1. SafetyOverride — highest authority.
2. BenchTest.
3. PiSupervisor — abstract host-fixture source only in STEP_2.
4. SimulatedAutonomy.

No motor-level command interface exists here. Physical outputs and arming remain outside this package.

## Deterministic behavior

- source-tagged commands;
- monotonically protected per-source sequence handling;
- explicit timestamps and TTL;
- invalid/non-finite/stale/future command rejection;
- deterministic priority/preemption;
- safety override forces safe zero setpoint;
- no eligible source falls back to safe zero setpoint;
- normalized setpoint clamping;
- selected-source/reason observability.

## Build/test

```
cmake -S . -B build
cmake --build build
ctest --test-dir build --output-on-failure
```

Host qualification performed with GCC 14.2 / CMake 3.31.6: 1/1 CTest PASS.
