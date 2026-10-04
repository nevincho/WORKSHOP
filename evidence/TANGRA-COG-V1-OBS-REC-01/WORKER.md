# TANGRA-COG-V1-OBS-REC-01 — WORKER EVIDENCE

DATE: 2026-10-04
RESULT: ENGINEERING COMPLETE
CODEX: NOT USED
PI_CHANGES: NONE
AUTHORITY: NONE
OPERATIONAL_AUTHORITY: []

TARGET_REPOSITORY: nevincho/TANGRA-2.0
BASE: tangra-cog-v1-postmission-exp-01@be03bd0a40c6c95c5e624babc57d36f56827773f
BRANCH: tangra-cog-v1-obs-rec-01
FINAL_HEAD: ef9db4b3691e3807982d4cdc0cddd80dfe310195

FINAL_DELTA:
- TAI_COGNITIVE_INTEGRATION_PACKAGE/integration/cognitive_mission_evidence_capture.py
  blob: f369f8f9d5cf11afbdfeeeebd225fc6424edb295
- TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/integration/mission_evidence_capture_fixture.json
  blob: b74b5a85bb8dced05f3e7456dca963db207b0b74
- TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/integration/test_cognitive_mission_evidence_capture.py
  blob: 94d473cce7ff3effec3b57103e370c38e70a9142

BASE_TO_FINAL_DIFF:
- exactly 3 added files;
- COG-01 unchanged;
- Cognitive Bridge unchanged;
- COG-15 unchanged;
- COG-16 unchanged;
- no production/Pi/runtime files changed.

IMPLEMENTED:
- MissionEvidenceCaptureAdapter consumes existing structured telemetry only.
- Delegates ProducerEvidence through existing CognitiveBridge -> COG-00 StateEvent -> COG-01 StateEventRecorder.
- Explicit mission_id/run_id retained in every event payload and correlation_id.
- Source telemetry timestamp preserved in StateEvent payload as source_timestamp.
- Significant state/error transitions emit immediately.
- Unchanged state is suppressed.
- Numeric observations are incrementally summarized in bounded accumulators.
- Aggregate window defaults to 1.0 second and is configurable.
- Queue-full/recorder rejection remains fail-open and is surfaced through counters.
- No raw snapshot history is retained in adapter RAM.
- No TRACK_HISTORY or PREDICTION_HISTORY is fabricated.

CAPTURED NUMERIC FIELDS:
runtime_uptime_sec, fps, cpu_usage, ram_usage, cpu_temp, active_trackers,
runtime_profile.loop_ms, capture_ms, yolo_ms, tracker_ms, behavior_ms,
dashboard_ms, snapshot_ms, swarm_ms, detector_timing.hailo_inference_ms,
detector_latency_ms, hailo_preprocess_ms, hailo_postprocess_ms,
horos_shadow.wide_worker.last_age_s, pi_http_age_sec, remote_ingest_age_sec.

CAPTURED STATE FIELDS:
runtime state, camera_status, WIDE running/freshness/failure/drop/error states,
detector_backend, hailo_status, HOROS mode/errors, pi_http_status,
pc_cache_status, remote_ingest_status, pi_telemetry_source,
pi_telemetry_error, runtime_controller_error, lora_connected,
lora_link_status, lora_status.

RAM BOUND:
- 21 fixed numeric accumulator slots;
- 24 fixed state slots;
- fixed capture counters;
- no unbounded snapshot/event list;
- persistence queue remains the existing separately bounded COG-01 queue.

QUALIFICATION:
Final authoritative GitHub Actions run: 37195675981
Executed head: eac0fae76c767465373a1367609a1ad41e0981b1
- py_compile: PASS
- OBS-REC-01 pytest: 6/6 PASS in 0.27s

The final branch head differs from the executed qualification head only by deletion of the temporary qualification workflow. The implementation, fixture and test blobs are identical to the successfully executed blobs listed above.

TEST COVERAGE:
1. producer path performs no disk I/O before the existing COG-01 worker;
2. unchanged state suppression and numeric aggregation;
3. immediate compact transition emission;
4. queue overflow fail-open and visible;
5. mission start -> active stream -> stop -> chronological JSONL replay with mission/run correlation;
6. no TRACK_HISTORY/PREDICTION_HISTORY fabrication.

MEASURED FIXTURE WRITE REDUCTION:
- input telemetry snapshots: 20
- naive every-snapshot records: 20
- actual persisted records: 6
- reduction: 70%
- actual sequence: START, BASELINE, aggregate, error/state transition, aggregate, STOP.

LIMITATIONS / DEFERRED:
- production/Pi wiring not performed by task scope;
- no per-track TRACK_HISTORY source added;
- no CA PREDICTION_HISTORY source added;
- no diagnostics, LLM inference, remediation, Dashboard or control added.

FINAL_RESULT:
ENGINEERING_COMPLETE / QUALIFICATION_PASS / AUTHORITY_NONE
