# VK Bootstrap / Survival Implementation Backlog

Date: 2026-09-15
Status: PLANNING ONLY — NO MODEL SELECTION / NO IMPLEMENTATION

## Dependencies
DIST-03 status remains unchanged and must eventually obtain behavioral validation/Reviewer PASS/checkpoint. Before DIST-04 implementation, the universal wire profile/conformance gate and the already-defined capability/HostInspector/Portable Seed/Bootstrap Survival architecture gates must be satisfied.

## Later bounded work
1. BOOT-01 Bootstrap Intelligence Contract schema: language-independent structured inputs, action intents, errors and policy-validation boundary.
2. BOOT-02 Policy/Scenario Engine contract: deterministic scenarios, transition guards, allowed actions, failure/fallback behavior.
3. BOOT-03 Operating-mode state machine tests: SURVIVAL/LOCAL/DISTRIBUTED/FULL/DEGRADED/RECOVERY transitions and identity invariance.
4. BOOT-04 Platform bootstrap substrate research: Windows, Linux x86, Linux ARM; Android later. Determine minimum self-contained execution requirements without assuming Python/dependencies.
5. BOOT-05 Micro-model benchmark harness and corpus. No model download until separately authorized.
6. BOOT-06 Candidate benchmark: storage, RAM, CPU startup/runtime, structured instruction following, tool selection, schema-valid output, Bulgarian/multilingual behavior, Host Inspector interpretation, scenario adherence, offline operation.
7. BOOT-07 Recovery/integrity contract: Core verification failures, incomplete runtime, rollback and safe recovery boundaries.
8. BOOT-08 Escalation/fallback integration contract: stronger local/remote inference discovery, compatibility checks, explicit mode transitions, survival persistence.
9. BOOT-09 Portable Seed packaging plan after platform substrate evidence.
10. BOOT-10 Physical 256 GB carrier validation only after implementation gates authorize it.

## Benchmark acceptance dimensions
No single score is sufficient. Record model artifact size/version/hash, minimum and practical RAM, CPU architecture/runtime, cold startup, task latency, deterministic structured-output validity, tool-choice correctness, policy violations, Bulgarian comprehension/output, offline behavior and failure recovery. Compare candidates behind the same contract; model identity must not leak into VK semantic identity.

## FACT
No micro-model has been selected, downloaded, benchmarked or validated. No installer/bootstrap implementation is authorized by this artifact.

## ASSUMPTION
A candidate in the approximate 0.2–0.5 GB storage class may be adequate for bounded survival tasks. This is a research hypothesis only.

## NOT VERIFIED
Cross-platform execution substrate, benchmark thresholds, suitable model availability, weak-host performance, Android feasibility, recovery implementation and real Portable Seed boot behavior.