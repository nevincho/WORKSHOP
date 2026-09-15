# TANGRA-COG-MODEL-EVAL-01 — Synthetic Simulation Evidence

RESULT: PASS
DATE: 2026-09-15
SCOPE: evaluator/fixture simulation only; no real model execution.

## Grounding verified before build
`nevincho/TANGRA-CL` main tree: `a85512a2831938099094c406aae07a38ce8fdd67`.
Relevant identity, Self-Discovery, self-model schema and strict prompt blobs were inspected before fixture construction.

## Synthetic discrimination results
- A_CORRECT / T2 -> PASS; no failure categories.
- B_HALLUCINATED / T1 -> FAIL; `INVENTED_TELEMETRY`.
- C_UNSUPPORTED_CAUSAL / T5 -> FAIL; `UNSUPPORTED_CAUSAL_CLAIM`.
- D_EVIDENCE_OMITTING / T2 -> FAIL; `EVIDENCE_OMISSION`.
- E_CONTRADICTION_MISHANDLED / T4 -> FAIL; `CONTRADICTION_MISHANDLING`.
- F_INCOMPLETE / T3 -> FAIL; `INCOMPLETE_ANSWER`.

Additional deterministic controls:
- malformed structured output -> FAIL / `MALFORMED_STRUCTURED_OUTPUT`.
- EXPECTED/undemonstrated current Hailo promoted to VERIFIED -> FAIL / `EXPECTED_PROMOTED_TO_VERIFIED`.
- unsupported extra hardware fact (`gps_device_present`) -> FAIL / `INVENTED_HARDWARE_RUNTIME_STATE`.

The T3 fixture independently requires preservation of both `UNKNOWN` and `NOT_VERIFIED`; wrong promotion is classified `FAILURE_TO_PRESERVE_UNKNOWN_NOT_VERIFIED`.

## T2 ground truth
The frozen Hailo packet records the requested PCIe/device/firmware/kernel/PID/network/throttling/WinSCP/SSH observations. The causal semantic fact `hailo_caused_winscp` is frozen as `NOT_VERIFIED`. The correct synthetic answer passes only when it preserves that status and cites the required incident evidence.

## Validation method
The committed deterministic evaluator logic was exercised against the committed synthetic case semantics. This validates the evaluator decision rules, not model quality and not local-runtime performance. No load time, token throughput, wall time or other runtime metric was fabricated.

## Boundary
REAL_MODEL_RESULTS: NOT_VERIFIED / NOT EXECUTED.
PI_RUNTIME: NOT ACCESSED.
GGUF/LLAMA.CPP: NOT ACCESSED.
LIVE_TANGRA: NOT ACCESSED.
