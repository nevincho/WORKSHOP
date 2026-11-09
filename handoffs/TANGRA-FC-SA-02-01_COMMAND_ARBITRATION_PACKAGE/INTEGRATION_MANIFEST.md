# STEP_2 Integration Manifest

STATUS: SOFTWARE_IMPLEMENTATION_CANDIDATE
LOCAL_FC_INTEGRATION: NOT_YET_PERFORMED

## Required later adapters

- Map local FC controller/setpoint representation to `ControlSetpoint`.
- Feed the FC monotonic clock into `select(now_ms)`.
- Bind existing bench/test producer to `BenchTest`.
- Bind future Pi supervisor transport output to `PiSupervisor` only after STEP_8 contract is integrated.
- Bind existing safety/failsafe condition to `SafetyOverride` with `force_safe=true`.

## Protected boundary

The adapter must not bypass the existing attitude/rate controller or virtual Quad-X mixer. PiSupervisor is not motor-level authority.

## Assumption

Priority below safety is defined for this standalone package as BenchTest > PiSupervisor > SimulatedAutonomy. If repository-backed FC policy later requires a different non-safety order, Codex may adapt the priority mapping without changing the invariant that SafetyOverride is highest.
