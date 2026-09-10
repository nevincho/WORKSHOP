# HB-00 — Dashboard 2.1 System Health / Heartbeat Source Forensic

STATUS: READY_FOR_WORKSHOP
DATE: 2026-09-10
MODE: READ-ONLY / FORENSIC / NO IMPLEMENTATION
CAMPAIGN: Dashboard 2.1 → Settings → System Health / Heartbeat Monitor

## Objective
Establish the factual current health-signal surface before any health model, heartbeat contract, UI, or source modification is proposed.

Canonical boundary: **Pi reports cheap facts; PC derives health information.** System Health is passive. Production runtime is protected.

## Scope
Inspect current Dashboard 2.1 and only the minimum direct TANGRA/telemetry dependencies required to determine what the Dashboard already receives and what can be reliably derived on Windows.

Determine existing: telemetry/API fields; timestamps; counters; states/enums; timings/latencies; freshness indicators; worker/queue/error states; safety/authority states; and source evidence required for candidate health signals.

Candidate areas: Runtime/System, Performance, HQ Camera, async WIDE Camera, Hailo/Detector, Tracking, Range/Metric, HOROS, Telemetry/EDGE LINK, Communications, Safety/Authority, Workers/Queues.

## Required classification
Every candidate signal MUST be exactly one of:
- AVAILABLE — directly exists in current telemetry/API/state.
- DERIVABLE_PC — reliably calculable on Windows from existing source data with no new Pi instrumentation.
- SOURCE_GAP — required source fact is genuinely absent.

SOURCE_GAP is evidence only; it is NOT authorization for Pi modification.

## Required record per signal
AREA | SIGNAL | SOURCE | TELEMETRY/API KEY | UNIT | UPDATE/FRESHNESS SOURCE | CLASSIFICATION | CURRENT COST | EXISTING THRESHOLD | EVIDENCE | NOTES

Use `NOT_VERIFIED` where evidence is absent and `NOT_DEFINED` where no threshold exists. Do not invent thresholds, enums, operational state, or authority names.

## Required forensic questions
1. What does Dashboard 2.1 currently receive from Pi?
2. Which timestamps, counters, states/enums and timings already exist?
3. Which freshness, worker, queue and error facts already exist?
4. Which safety/authority facts already exist?
5. Which candidate signals are reliably PC-derivable?
6. Which candidate signals are genuine SOURCE_GAPs?
7. What is the current acquisition/transport cost of each available signal where evidence permits determination?

## Protected / forbidden
NO implementation. NO production changes. NO Pi instrumentation. NO new polling/background workers. NO monitoring framework/profiler/history engine. NO telemetry redesign. NO UI work. NO automatic recovery/restart/maintenance. NO performance/algorithm optimization. NO changes to HQ/WIDE roles, Hailo, NanoTracker, CurrentTarget, CA Kalman, range authority, HOROS, Runtime Controller, communications, command-send, IFF, readiness or actuation.

Do not put target/spatial coordinates into a proposed heartbeat during this task. Do not treat configured state as proof of operational state. Missing values are not zero/healthy.

## Threshold provenance
Record only, in order of authority: current validated production threshold; current canonical repository threshold; current measured evidence; historical threshold explicitly labelled historical; otherwise `NOT_DEFINED`.

## Deliverables
1. Evidence-backed signal inventory table using the required schema.
2. Source-path/key map for each AVAILABLE signal.
3. Explicit PC derivation description for each DERIVABLE_PC signal, including required inputs and freshness semantics.
4. SOURCE_GAP register stating the exact missing fact; no remediation implementation.
5. Threshold provenance register.
6. Concise findings: reusable current telemetry, highest-value verified signals, genuine gaps, ambiguities/NOT_VERIFIED items.
7. Changed-files list proving evidence/documentation only.
8. One isolated commit for HB-00 evidence/results.

## Acceptance gate
PASS only if classifications are traceable to current repository evidence, no threshold or operational state is invented, and no implementation/runtime change occurred.

STOP after HB-00 evidence and commit. Do not start HB-01, heartbeat design, UI, or any Pi-side proposal.