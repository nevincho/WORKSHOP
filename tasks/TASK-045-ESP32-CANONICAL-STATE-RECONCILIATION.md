# TASK-045 — ESP32 MicroBlog Canonical State Reconciliation

STATUS: READY_FOR_WORKER
PROJECT: ESP32 MICROBLOG / AGENT 32 — independent commercial funding track
TYPE: environment/state preparation

## Objective
Prepare the exact authoritative implementation/build state required before any firmware source modification or device upload.

## Authority
- Documentation: `nevincho/nova`, branch `esp32-microblog-agent32`, path `ESP32_MICROBLOG/`
- Active implementation state: local Windows workspace `D:\RaspberryPi5\ЕСП32_БЛОГ`
- Do not infer local state from repository documentation.

## Work
1. Read the project documentation and existing validation history.
2. Reconcile all repository-verifiable facts about v0.7, v0.6.1, board/core/toolchain assumptions and prior blocker.
3. Determine exactly what local facts must be collected to establish current v0.7 source path/files, board target, Arduino CLI/core/tool versions, COM route and completion state of the ESP32 3.3.11-era update.
4. Use an already-authorized verified Windows execution route only if one exists in WORKSHOP. Otherwise record the minimum missing live evidence; do not invent it.
5. Produce evidence under `evidence/TASK-045/`.

## Constraints
- NO firmware source changes.
- NO upload/flash.
- Preserve v0.6.1 baseline.
- Do not spend Codex capacity on inventory/documentation work.
- Local implementation claims without direct evidence are `NOT VERIFIED`.

## Acceptance
PASS only if the next diagnostic can be specified against an exact verified environment/state, or if a precise external/live blocker is identified with no false implementation claims.

## Next
TASK-046 may proceed only when TASK-045 provides sufficient exact state for the diagnostic.
