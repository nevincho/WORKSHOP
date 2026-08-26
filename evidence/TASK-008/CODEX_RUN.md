# TASK-008 — Codex implementation and runtime integration

Date: 2026-08-26
Status: IMPLEMENTED / LIVE VALIDATION NOT COMPLETED
Reviewer verdict: NOT ASSIGNED; this record does not mark TASK-008 PASS.

## Authority and checkpoint

- Coordination: `nevincho/WORKSHOP@main`
- Source: `nevincho/LIVE@Legacy`
- Pre-change LIVE checkpoint / rollback: `cf911176be543393f1a05e578b4ea30d70f010bb`
- Implementation commit: `840f94abb18f10c87798c2e4a54796dd6dab2bc2`
- Actual runtime: `D:\Store\AI`
- Local rollback copies: `D:\Store\AI\archive\task008_rtsp_rollback_cf911176`

## Implemented

- Existing `CameraAdapter` accepts integer/local sources unchanged and explicit `rtsp://` or `rtsps://` sources.
- Network open uses OpenCV FFmpeg with 5,000 ms open/read timeouts and one-frame buffered capture.
- Errors and metadata redact RTSP credentials; OpenCV/FFmpeg diagnostics are suppressed before network open.
- Captures report safe source, source type, width, height, channels, dtype and saved-frame path.
- Existing `VKRuntime` perception metadata uses sanitized captured source.
- Existing `PerceptionIngress` remains candidate-only with `canonical_memory=false`, `memory_status=not_admitted`, and `auto_memory_promotion=false`.
- Credential-free bounded live validator added and synchronized to `D:\Store\AI\tools\validate_rtsp_perception.py`.
- Repository and local runtime `camera_adapter.py` SHA-256 were byte-identical after integration.

## Validation

Commands:

- `python -m unittest family_guardian_ai.SOURCE_V09.tests.test_camera_rtsp_integration family_guardian_ai.SOURCE_V09.tests.test_event_envelope_contract`
- `python -m unittest discover -s family_guardian_ai\SOURCE_V09\tests -p 'test_*.py'`
- `python -m py_compile family_guardian_ai\SOURCE_V09\app\camera_adapter.py family_guardian_ai\SOURCE_V09\app\vk_runtime.py family_guardian_ai\SOURCE_V09\app\perception_ingress.py`
- `D:\Store\AI\.venv\Scripts\python.exe` OpenCV capability and candidate-only ingress checks.

Results:

- Focused tests: 8/8 PASS.
- Full SOURCE_V09 tests: 67/67 PASS.
- Actual VK venv: OpenCV 5.0.0; FFmpeg backend and open/read timeout properties available.
- Local integer source compatibility, credential redaction and candidate-only ingress: PASS.
- Real IMOU RTSP authentication: NOT VALIDLY TESTED.
- Real subtype=1 stream open: NOT VALIDLY TESTED.
- Real frame decode and dimensions/type: NOT VALIDLY TESTED.
- Real-frame perception event: NOT VALIDLY TESTED.
- Automatic canonical-memory promotion: no implementation path added; contract/regression PASS. Real-frame proof remains pending.

## Live blocker

A local credential prompt was launched so secrets would not enter chat, Git, commands or logs. Runtime credential entry was not completed successfully; no valid credentialed frame-read result was produced. No credential was stored. Live acceptance therefore remains pending human-supplied runtime credentials and must not be inferred from repository tests.

Independent WORKSHOP Reviewer retains final PASS authority.
