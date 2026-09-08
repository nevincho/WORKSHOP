# TASK 6 — OPERATIONAL VIEW ENVELOPE REPORT

## Scope
Exact frozen T1→T2→T3→T4 executed on deterministic planar synthetic target projections. No pose/6DoF estimator, tracker, flow, production integration, or physical claim.

## Frozen identity
- T1 blob `91f81e882af557f2d2106a8648ee283bfbdee81e` @ `c7b378841979f82b037c47be3571fa72a7b70e51`
- T2 blob `83202583f93ca43b134132f84d5cd51d7b59bcbe` @ `4bd4b5d38357db501de07511aeabaa4c0ae058e1`
- T3 blob `d15e09dc63384d93719fdab30b50634750cfd65c` @ `c121ce25dbba84520c6f8e644281a7cb2bf3ee73`
- T4 blob `af995bdaab486b0c677bcd35c6166d90d253bbfb` @ `7f628a727b89599ea6977053ea12211b10e0ffcd`
- T5 harness blob `afb024f0baffe58226e933c630b0a6be8cf29939` @ `e48eaa71d49721786b6acc490a32c7af800161bf`; not modified/used as estimator.

## Sweep
Coarse: 0–60° in 5° steps; ranges 12/20/32 m; yaw 0/20/40°; 5 deterministic replicates/condition. Fine sweeps at first RELIABLE transition and first UNUSABLE transition. Exact-chain primary/probe frames: 710.

## Classification basis
RELIABLE/DEGRADED/UNUSABLE are synthetic operational labels, not production metric verification. 10%/30% accuracy/uncertainty bands are inherited from frozen T4 soft/hard disagreement policy; classification additionally requires two usable TASK3 independent spans and no conflict. All T4 metric usability remained NOT_VERIFIED.

## Conservative contiguous envelope
Stop at the first UNUSABLE transition even if re-entrant validity appears at a stronger angle.

| z / scale | yaw | RELIABLE | DEGRADED before first failure | first UNUSABLE |
|---|---:|---|---|---:|
| 12 m | 0° | 0–32° | none | 33° |
| 12 m | 20° | none | 0–31° | 32° |
| 12 m | 40° | none | 0–36° | 37° |
| 20 m | 0° | 0–31° | none | 32° |
| 20 m | 20° | none | 0–30° | 31° |
| 20 m | 40° | none | 0–36° | 37° |
| 32 m | 0° | 0–30° | none | 31° |
| 32 m | 20° | 0–16° | 17–29° | 30° |
| 32 m | 40° | none | 0–37° | 38° |

Aligned yaw=0° scale boundary: large (12 m, ~166.8×238.5 px) reliable through 32°, first unusable 33°; medium (~100.2×143.0 px) reliable through 31°, first unusable 32°; small (~62.2×89.8 px) reliable through 30°, first unusable 31°.

At yaw=20°/40°, image-space LEFT/RIGHT extrema no longer remain a clean fixed physical-width correspondence; sparse bias rises and the envelope becomes conditional. Re-entrant validity after an earlier semantic failure is recorded but excluded from the operational envelope.

## Orientation uncertainty
- Known @ z20/yaw0/20°: T3 sigma 0.3676 m, T3 bias -0.5167 m.
- 10% relative projection uncertainty: T3 sigma 1.5572 m (~4.24×); evidence remains usable but less precise.
- Insufficient orientation knowledge (35% relative sigma + confidence gate): 0 usable TASK3 candidates; fail closed; T4 only retains external class-size evidence as DEGRADED/NOT_VERIFIED.
- Asymmetric wrong projection factors: TASK3 returns `candidate_disagreement`; no sparse range is emitted.

## Fail-closed
Semantic loss, span collapse and partial silhouette suppress NOSE/TAIL, reduce TASK3 below two independent spans, and return `insufficient_independent_evidence`. Incorrect asymmetric orientation returns `candidate_disagreement`. Strong yaw/obliquity cases can reach T4 CONFLICT; no convenient sparse range is selected.

## Representative accuracy
- z20/yaw0/0°: T3 bias -0.4722 m; fused bias -0.2637 m; T3 sigma 0.3562 m; geometry confidence 0.8951.
- z20/yaw0/30°: T3 bias -0.6134 m; fused bias -0.2405 m; T3 sigma 0.4897 m; two candidates remain usable.
- z20/yaw0/32° fine sweep: NOSE/TAIL valid rate falls to 0.667 and mean usable candidate count to 1.667 → UNUSABLE under the two-span requirement.
- z32/yaw20/15°: T3 bias -3.0172 m (9.43%) → RELIABLE band edge; at 17° bias -3.2496 m (10.15%) → DEGRADED.
- z20/yaw40/36°: T3 bias -4.9595 m (24.8%) → DEGRADED; at 37° NOSE/TAIL are lost → UNUSABLE.

Accuracy and temporal stability are separate: replicate-to-replicate T3/fused bias jitter remained small relative to the systematic viewpoint bias. Systematic foreshortening/correspondence error is not reported as jitter.

## Performance (HOST)
- T1 mean 0.922248 ms, median 0.848687, p95 1.298668, max 7.487871.
- T2 mean 0.390267 ms; T3 0.083978 ms; T4 0.032742 ms.
- Complete chain mean 2.645645 ms, median 2.574043, p95 3.204570, max 9.293950, n=710.
- Offline envelope classification helper mean 0.000406 ms, p95 0.000421 ms, n=50,000.

## Architecture decision
TOP_DOWN_OPERATIONAL_MODEL_SUPPORTED=YES (for profile/correspondence-compatible orientation; not universal across arbitrary in-plane yaw).
MILD_OBLIQUE_OPERATION_SUPPORTED=CONDITIONAL.
ARBITRARY_VIEW_SUPPORT_REQUIRED_NOW=NO.
No 6DoF/pose architecture is justified by this task.

## Production gates
AI→CAL production transform NOT_VERIFIED; real point↔physical-span correspondence NOT_VERIFIED; physical metric accuracy NOT_VERIFIED; Pi5 performance NOT_VERIFIED. TASK6 does not promote any gate.

Focused tests: 18/18 PASS.
