# TANGRA-RESEARCH-LAB-03 — Temporal Integrity and Performance Qualification

TASK_ID: TANGRA-RESEARCH-LAB-03
PROJECT: TANGRA
CAMPAIGN: TANGRA-RESEARCH-LAB
PRIORITY: HIGH
STATUS: REVIEW
TYPE: WORKER / READ-ONLY RESEARCH / QUANTITATIVE QUALIFICATION
OBJECTIVE: Determine which timing, cadence, latency, jitter, dropout and measurement-age quantities are actually evidenced across the current TANGRA perception-to-output chain; quantify defensible state-freshness sensitivity; identify missing timestamps/clock provenance that prevent measurement; and specify the smallest observations required to close those gaps. Do not optimize or modify TANGRA.
SOURCE_PLAN_OR_REQUEST: Qualified campaign; JOB-01 and JOB-02 independent PASS/checkpoints.
CURRENT_STATE:
- Aggregate FPS, WIDE cadence, long-runtime and selected stale-frame evidence exist.
- Per-stage timestamps, clock domains, queue age and end-to-end synchronized latency are incomplete or NOT VERIFIED.
- JOB-02 left measurement-age, pose timing and world-frame timing explicitly open.
- Fresh production/runtime access is unauthorized.
PREREQUISITES:
- TANGRA-RESEARCH-LAB-01 and -02 COMPLETE / Reviewer PASS.
- Exact qualified refs and retained evidence only.
DEPENDENCIES:
- TANGRA-RESEARCH-LAB-01: COMPLETE.
- TANGRA-RESEARCH-LAB-02: COMPLETE; consume its missing time/pose terms without redefining physical accuracy.
AFFECTED_COMPONENTS:
- WORKSHOP evidence/review/checkpoint artifacts only.
- Read-only timing/performance documents, schemas, logs and retained measurements.
PROTECTED_COMPONENTS:
- All TANGRA repositories/runtime/Pi/services/models/configuration and existing scheduling/concurrency behavior.
EXECUTION_CLASS: WORKER
CODEX_ALLOWED: NO

REQUIRED_WORK:
1. Map timestamps, clock domains, capture/inference/tracker/range/HOROS/Fusion/telemetry stages, queues and freshness/stale decisions supported by exact evidence.
2. Separate measured aggregate throughput from stage latency and measurement age.
3. Audit whether reported FPS/uptime/stale-frame results measure the claimed temporal property.
4. Quantify deterministic displacement/error sensitivity over evidenced or clearly synthetic velocity, age, jitter and dropout ranges; keep measured and hypothetical inputs separate.
5. Identify where clock-source, timestamp semantics, queue depth, frame identity or synchronization absence prevents end-to-end conclusions.
6. Assess throughput/headroom only from evidenced measurements; do not recommend optimization solely from synthetic stress.
7. Define the smallest instrumentation/experiments needed to establish temporal integrity and fair JOB-04 replay semantics.
8. Produce reproducible artifacts where calculations are justified, execution ledger and Reviewer request.

REQUIRED_DELIVERABLES:
- stage/timestamp/clock-domain map;
- evidence-quality table for cadence/latency/jitter/dropout/age;
- deterministic temporal sensitivity results;
- stale-measurement and dropout consequence bounds;
- missing-observability register;
- minimum validation/instrumentation experiment set;
- JOB-04 timing/replay prerequisites;
- execution ledger and independent review request.

ACCEPTANCE_CRITERIA:
1. Every measured value cites exact source/ref/date; synthetic ranges are explicit.
2. FPS is not treated as latency, freshness or synchronization proof.
3. Timestamp semantics and clock domains are explicit or NOT VERIFIED.
4. Sensitivity calculations are reproducible and separate measured from hypothetical inputs.
5. Dropout/jitter/age conclusions do not claim physical accuracy absent ground truth.
6. JOB-04 receives exact fair-comparison timing/horizon/coverage prerequisites.
7. Optimization is HOLD unless evidence shows actual headroom failure.
8. No TANGRA/runtime mutation or access occurs.
9. Independent Reviewer verifies actual evidence/calculations and hygiene.

VALIDATION_METHOD:
- Exact-ref cross-check of timing/performance sources.
- Deterministic rerun and independent arithmetic assertions for generated analysis.
- Reviewer challenges objective-to-metric fit, clock provenance, measured/synthetic separation and claim scope.
- Verify read-only boundary and hygiene.

NON_GOALS:
- No code/runtime optimization, instrumentation implementation or configuration change.
- No live Pi/camera access, command, flight, flash or actuation.
- No CV/CA comparison beyond defining JOB-04 prerequisites.
- No external literature research.
- Do not create JOB-04 or later before independent PASS/checkpoint.

EVIDENCE_PATHS:
- evidence/TANGRA-RESEARCH-LAB-03/WORKER.md
- evidence/TANGRA-RESEARCH-LAB-03/temporal_sensitivity.py if justified
- evidence/TANGRA-RESEARCH-LAB-03/temporal_sensitivity.json if justified
- review/TANGRA-RESEARCH-LAB-03.md
- checkpoints/TANGRA-RESEARCH-LAB-03.md

PRE_CHANGE_CHECKPOINT: checkpoints/TANGRA-RESEARCH-LAB-02.md
ROLLBACK_METHOD: Revert WORKSHOP task-local artifacts only.
STOP_CONDITION: REVIEW after Worker evidence; continue campaign only after independent PASS and checkpoint.
CODEX: NOT USED
PI_CHANGES: NONE
TANGRA_CHANGES: NONE
