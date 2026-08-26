# TASK-008 — Codex implementation and runtime integration

Date: 2026-08-26
Status: IMPLEMENTED / REAL LIVE VALIDATION COMPLETED / REVIEW PENDING
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
- Real validator command: `VK_RTSP_URL=rtsp://admin:<REDACTED>@192.168.0.154:554/cam/realmonitor?channel=1&subtype=1 D:\Store\AI\.venv\Scripts\python.exe D:\Store\AI\tools\validate_rtsp_perception.py`.
- Real IMOU RTSP authentication: SUCCESS, established by decoded frame.
- Real subtype=1 stream open: PASS.
- Real frame: 640x480, 3 channels, `uint8`.
- Existing `PerceptionIngress`: PASS; produced `PERCEPTION_OBSERVATION` candidate from saved real frame.
- Event contract: `status=candidate`, `canonical_memory=false`, `memory_status=not_admitted`.
- Automatic canonical-memory promotion: `false`.
- Canonical-memory count: 1 before, 1 after; unchanged.
- Runtime credential environment was unset immediately after execution; retained evidence contains no credential.

## USB source recovery validation — 2026-08-26

A later normal-chat attempt temporarily failed with `CAPTURE ERROR: Camera 0 could not be opened`. Focused investigation found no VK integration regression and required no production code change.

- Result: PASS — USB restored without code change.
- Classification: DEVICE / ENVIRONMENT TRANSIENT; no integration regression.
- Root cause: camera was previously not enumerated; brief DirectShow release contention affected the first retry.
- Direct USB test: PASS — fresh `640x480x3`, `uint8` frame.
- Available device indices: `0` only.
- CameraAdapter test: PASS — device `0`, fresh `640x480` frame.
- Normal VK chat explicit USB request: PASS — fresh frame captured.
- Source provenance: `LOCAL_USB_CAMERA_0`.
- No fallback to IMOU: PASS.
- Memory boundary: `candidate`, `not_admitted`, `canonical=false`; canonical-memory count remained 1 before/after.
- Files changed for recovery: NONE.
- LIVE commit for recovery: NONE; no implementation change was justified.
- Blockers: NONE.

## Live result

On 2026-08-26, the actual `D:\Store\AI` validator decoded one real frame from the authorized IMOU camera and passed it through the existing VK `CameraAdapter` and `PerceptionIngress` path. Later focused USB recovery validation also passed through direct OpenCV, CameraAdapter, and normal VK chat with deterministic `LOCAL_USB_CAMERA_0` provenance and no IMOU fallback. No USB implementation change was required.

Independent WORKSHOP Reviewer retains final PASS authority.
