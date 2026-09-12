# WIDE-EW-01 — WIDE Runtime / Interface Inventory

PROJECT: TANGRA
CAMPAIGN: WIDE V3 EARLY-WARNING SENSOR CLEANUP
STATUS: READY_FOR_WORKSHOP
TYPE: FORENSIC / INVENTORY
CODEX: FORBIDDEN
PRODUCTION/Pi5 MODIFICATION: FORBIDDEN

## Objective
Establish the exact evidence-backed current WIDE IMX708 software role before any implementation work. Inventory every documented/current WIDE-derived processing path, interface, telemetry output and consumer, and classify each as KEEP, REPLACE_WITH_MOTION_HINT, BLOCK, REMOVE_CANDIDATE, or NOT VERIFIED where evidence is insufficient.

This task is forensic only. Do not implement the motion detector yet.

## Authoritative context
Canonical project evidence repository: `nevincho/TANGRA-DOCS` main.
WORKSHOP is coordination authority only.
Current documented protected HQ authority:
`HQ -> primary Hailo detector -> NanoTracker -> CA Kalman -> CurrentTargetManager -> HOROS`.

Current repository evidence indicates WIDE has/had an asynchronous inference path and contribution to HOROS local environment/map. Treat this as a fact to verify/reconcile against the latest available authoritative evidence, not as permission to preserve it.

## Required inspection
Trace WIDE from capture through all documented current stages:
`capture -> preprocessing -> inference/processing -> worker/thread/queue -> observation/state -> HOROS/environment -> API/telemetry -> Dashboard/other consumers`.

Inventory every WIDE-derived:
- computation/preprocessing;
- Hailo/inference invocation;
- worker/thread/queue/cache;
- observation/state object;
- HOROS/environment/map input;
- telemetry/API field;
- Dashboard consumer;
- diagnostic counter;
- WIDE image stream and any other consumer-facing interface.

For each item record:
- exact evidence source/path;
- producer;
- consumer(s);
- demonstrated current purpose;
- authority implications;
- known resource evidence if available;
- classification: KEEP / REPLACE_WITH_MOTION_HINT / BLOCK / REMOVE_CANDIDATE / NOT VERIFIED;
- rationale.

## Mandatory questions
1. Which WIDE processing currently exists solely to feed WIDE inference/HOROS/environment functionality?
2. Which telemetry fields have an actual current consumer?
3. Which WIDE outputs are diagnostic/display-only?
4. Does any WIDE-derived path enter target creation/confirmation, NanoTracker, CA Kalman, CurrentTargetManager, metric range, HOROS target XYZ/lifecycle, or mission/navigation authority? If evidence cannot resolve this, mark NOT VERIFIED.
5. Which components could later be retired at source without changing HQ authority?
6. What minimum existing WIDE capture/interface must be retained to support a future MOTION_HINT implementation?

## Protected
Do not redesign or modify HQ detector, NanoTracker, CA Kalman, CurrentTargetManager, HOROS target path, camera calibration authority, LoRa/EDGE LINK, mission/navigation, production authority, or Pi5 runtime.

## Evidence requirements
Produce `evidence/WIDE-EW-01/INVENTORY.md` containing:
- current WIDE path diagram;
- complete interface/output inventory;
- producer/consumer trace;
- KEEP / REPLACE_WITH_MOTION_HINT / BLOCK / REMOVE_CANDIDATE / NOT VERIFIED decision table;
- exact source evidence references;
- unresolved gaps;
- recommendation for the smallest next Workshop engineering task.

No implementation claims without source evidence. Documentation-only evidence must be labelled as such. No live/runtime validation may be inferred.

## Acceptance criteria
PASS only if:
- the currently evidenced WIDE path is traced end-to-end as far as authoritative sources permit;
- active/documented outputs and consumers are individually classified;
- WIDE authority boundaries are explicitly resolved or marked NOT VERIFIED;
- likely obsolete computation is identified at its producer, not merely at Dashboard presentation;
- minimum retained boundary for future MOTION_HINT is identified;
- no production/Pi5 changes occur;
- no Codex is used.

## Verdict
Return PASS / FAIL / BLOCKED with evidence-backed reasons.

## STOP
After evidence and verdict are persisted, STOP. Do not implement WIDE motion detection and do not start the next campaign task.