# TANGRA-COG-BRIDGE-01 — Real Pi precheck, 2026-09-20

RESULT: BLOCKED_BASELINE_MISMATCH. Integration and qualification were not executed.
Classification: expected-runtime/coordination mismatch, not a demonstrated Cognitive bridge implementation failure.

## Source and scope

Human authorized the real-Pi handoff for cognitive-bridge-integration@bd11d92f396b68de00a0f3636ae49ed8310ce420. The bridge blob was independently verified as 5f4a6346fa70e369452067d9d96f776a84468a64. The handoff requires STOP when actual runtime materially contradicts expected state and protects WIDE capture/detection from unrelated changes.

## Verified actual baseline

Host tangra-ai, Raspberry Pi 5 Model B Rev 1.1, aarch64, Python 3.11.2. Runtime /home/khan/ai-drone/tangra; service tangra-droneguard-1-0.service; ExecStart /usr/bin/python3 /home/khan/ai-drone/tangra/main.py.
Initial controller GET http://127.0.0.1:8082/status: STANDBY, null runtime PID, API/telemetry IDLE, camera CLOSED. STANDBY is legal and was not itself classified as a contradiction.
After rollback archive creation, the unchanged service was started with sudo -n systemctl start tangra-droneguard-1-0.service for baseline measurement. Controller reported ACTIVE, Hailo true, API/telemetry HEALTHY, PID 1978886. /api/health returned ok=true; NRestarts=0. One telemetry snapshot showed fps=41.05984278176425, detector_backend=hailo, hailo_inference_ms=21.75344900751952, cpu_temp=50.15, cpu_usage=8.0, ram_usage=5.7, CA_KALMAN_PRIMARY, zero trackers, SEARCHING, HOROS errors=0 and target_evidence_unavailable. This is one NO_TARGET snapshot, not sustained performance or tracking/range qualification.
WIDE camera index 0 initialized successfully in the current startup log; HQ camera index 1 initialized successfully. Environment processing is disabled by WideHorosLatestWorker.ENVIRONMENT_PROCESSING_ENABLED=False in horos3d/runtime.py:185, guarded at line 395. COGNITIVE_SHADOW_ENABLED=False; command send, IFF and readiness flags False. No distinct CONTROL_ENABLED setting was established; no new Cognitive control was enabled.

## Material mismatch

Actual main.py:1823-1836 constructs WideAcquisitionRuntime and wires WideCameraPreview to process_wide_latest_frame, whose only processing call is wide_acquisition_runtime.process_latest_frame. camera/camera_manager.py:170 calls this callback. acquisition/runtime.py uses WideCueGenerator, whose documented implementation is stable-background difference with no neural inference, tracking or metric geometry.
The existing WideHorosLatestWorker detector implementation occurs in horos3d/runtime.py, but recursive inspection of main.py, acquisition, camera, core, horos3d and vision found no external instantiation/reference. No live WIDE detector/HOROS output was established. Thus the expected protected WIDE detection path cannot be qualified as an existing operational baseline. WIDE motion cues must not be silently equated to neural detection or wired differently within this Cognitive task.
Relevant read-only commands: grep -Rnl 'WideHorosLatestWorker' --include='*.py' main.py acquisition camera core horos3d vision; inspected main.py:1820-1836, camera/camera_manager.py:152-174 and acquisition/runtime.py/cue.py.
Required resolution: reconcile whether the observed capture-plus-motion-cue configuration is the intended protected baseline, or restore/qualify the expected WIDE detection path under its own authorized scope. Do not infer a bridge defect or repair protected WIDE code in this task.

## Rollback and final state

Verified backup: /home/khan/ai-drone/backups/COG-BRIDGE-01-20260920T1730/prechange.tgz
SHA256: 68ddf4a1e8408b2060e7323b35086db9d585dc93451213ad6f0ae69f50c37062
Archive contains main.py, core/config.py, cognitive/, cognitive_backend/package/ and horos3d/runtime.py. gzip -t and tar -tzf succeeded. Adjacent protected.sha256, service.txt, lifecycle.json and baseline-telemetry.json retain evidence. Restoration if needed: tar -xzf prechange.tgz -C /home/khan/ai-drone/tangra; restore original service STANDBY. No source restoration was necessary.
At 2026-09-20T17:33:13+01:00, sudo -n systemctl stop tangra-droneguard-1-0.service restored STANDBY, inactive/dead, MainPID=0, controller errors=[]. sha256sum -c protected.sha256 returned OK for all four protected files.
main.py SHA256 f469c082d85c0d4767e5ad8a2e55843cecc61a760b80a87adcc433acfbcc0ce4
core/config.py SHA256 c53527e497f1137d57b6faa3640fe8d08815a53892e72553ec73aba52421b109
cognitive/runtime.py SHA256 e231ba9b4143fbbd9abaee97d661ac6f92aade7be6593aa6751fe55b21f06001

No production source/configuration files changed. Only backup/evidence files were added; service was temporarily started and restored. Bridge installation, full ingress, COG-20 execution, experience restart persistence, Pi bridge tests and cumulative 317 regression: NOT EXECUTED. No deployment, promotion, regression PASS or REAL_PI_QUALIFICATION PASS claimed. Historical 17/17 repository qualification remains historical. Review/checkpoint documents were not rewritten.
