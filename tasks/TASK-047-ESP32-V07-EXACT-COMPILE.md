# TASK-047 — ESP32 v0.7 Exact Compile and Resource Measurement

STATUS: WAITING_FOR_TASK_046_PASS
PROJECT: ESP32 MICROBLOG / AGENT 32
TYPE: build validation
DEPENDS_ON: TASK-046 PASS

## Objective
Compile the exact untouched v0.7 AGENT32 LEAN source in the verified environment and determine whether the product itself has a build defect.

## Work
1. Fingerprint/identify the exact v0.7 source before build.
2. Compile without source edits.
3. Record build result, exact board/core/tool versions and Flash/RAM usage when available.
4. If compilation fails, classify the failure as implementation, integration, or environment/toolchain based only on evidence.
5. If a genuine source defect is demonstrated, prepare a minimal Codex Gate candidate; do not fix speculatively.
6. Write evidence under `evidence/TASK-047/`.

## Constraints
- Exact v0.7 source must remain unchanged during this task.
- NO upload/flash.
- Preserve v0.6.1.
- Codex tokens only if a concrete implementation defect is proven and separately approved.

## Acceptance
PASS requires a reproducible exact-source compile result and resource measurements when produced by the toolchain. Failure may be a valid diagnostic result only when the actual blocker is evidenced and classified.

## Next
A successful build may advance to TASK-048 physical upload/smoke test. Any required source repair must pass a separate Human/Codex Gate first.
