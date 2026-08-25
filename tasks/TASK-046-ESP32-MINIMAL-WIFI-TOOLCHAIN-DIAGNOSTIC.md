# TASK-046 — ESP32 Minimal Wi-Fi Toolchain Diagnostic

STATUS: READY_FOR_CODEX_REVIEW
PROJECT: ESP32 MICROBLOG / AGENT 32
TYPE: environment validation
DEPENDS_ON: TASK-045 PASS

## Objective
Re-run the minimal Wi-Fi compile diagnostic that previously reproduced the Arduino/ESP32 toolchain stall, using the exact environment established by TASK-045.

## Work
1. Use the same minimal Wi-Fi diagnostic intent as the prior isolation test.
2. Compile only; do not upload firmware.
3. Record exact board/FQBN, Arduino CLI/core/toolchain versions, command, elapsed result and complete actionable error if failure occurs.
4. Distinguish environment/toolchain failure from product-source failure.
5. Write evidence under `evidence/TASK-046/`.

## Constraints
- NO v0.7 source modification.
- NO device flash/upload.
- NO Codex implementation work unless a later task demonstrates a real source defect.

## Acceptance
PASS if compile completes successfully OR produces a concrete reproducible environment/toolchain error sufficient to classify the blocker. Hanging/ambiguous execution without bounded evidence is not PASS.

## Current gate
TASK-045 prerequisite is PASS / REVIEWED. Repository preparation is complete, but actual compile execution requires the authoritative Windows host. No autonomous Windows-local execution route is currently verified in WORKSHOP. A minimal Codex execution handoff is prepared under `evidence/TASK-046/CODEX_GATE.md`; execution remains HUMAN-GATED and Codex has not been invoked.

## Next
TASK-047 only after TASK-046 demonstrates that testing the exact v0.7 source is technically meaningful.
