# TASK-022 — VK Capability Discovery Layer

TASK_ID: TASK-022
PROJECT: VK
PRIORITY: HIGH
STATUS: BLOCKED
DEPENDS_ON: TASK-021 PASS
TYPE: REPOSITORY-ONLY IMPLEMENTATION
OBJECTIVE: Implement or complete the repository-side capability-discovery layer justified by TASK-021 evidence for CPU/GPU/RAM/storage/network/display/audio/camera/microphone/sensor/tool/model capability reporting.

BOUNDARY:
- repository branch only; no local runtime deployment;
- no Core/personality mutation;
- no new heavy dependencies without review;
- preserve existing interfaces and rollback.

VALIDATION: deterministic capability schema/tests using mocks/fixtures where real host access is unavailable; independent review.
