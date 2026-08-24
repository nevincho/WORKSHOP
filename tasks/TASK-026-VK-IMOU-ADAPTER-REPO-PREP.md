# TASK-026 — VK IMOU Adapter Repository Preparation

TASK_ID: TASK-026
PROJECT: VK
PRIORITY: HIGH
STATUS: BLOCKED
DEPENDS_ON: TASK-025 PASS
TYPE: REPOSITORY-ONLY PREPARATION / IMPLEMENTATION SCAFFOLD
OBJECTIVE: Prepare the IMOU IPC-K7C adapter path against the shared node/device layer using verified LAN evidence, without claiming live stream operation.

VERIFIED INPUT EVIDENCE:
- camera model IPC-K7C / Cruiser SE+
- LAN IP 192.168.0.154 observed by user
- TCP/554 reachable
- TCP/80 reachable
- TCP/443 not reachable
- RTSP endpoint/auth/frame retrieval NOT VERIFIED

RELATION TO TASK-008:
- TASK-026 is repository-only adapter preparation/scaffold.
- TASK-008 remains the later live camera integration/validation task.

BOUNDARY:
- no credentials in repository;
- no local runtime deploy;
- no cloud dependency assumption;
- no claim of RTSP/ONVIF success until live evidence exists.

VALIDATION: adapter/unit tests using mocks/fixtures, capability/status normalization, clean failure behavior, independent review.
