# TASK-046 — Codex Gate

STATUS: READY_FOR_CODEX_REVIEW
DATE: 2026-08-25
CODEX_EXECUTION: HUMAN-GATED / NOT INVOKED

## Task
TASK-046 — ESP32 Minimal Wi-Fi Toolchain Diagnostic

## Exact objective
On the authoritative Windows development host, re-run the previously isolating minimal Wi-Fi compile diagnostic using the exact current Arduino/ESP32 environment. Compile only. Produce bounded evidence sufficient to classify the environment/toolchain state.

## Verified current state
- TASK-045 PASS / reviewed.
- Active source/build/hardware authority: `D:\RaspberryPi5\ЕСП32_БЛОГ`.
- Documented board history: ESP32-WROOM-32.
- Historical Arduino CLI: 1.5.0 -> 1.5.1.
- Historical ESP32 core: 3.3.5 before a 3.3.11-era update began.
- Post-update exact installed versions and completion result: NOT VERIFIED.
- Prior minimal Wi-Fi compile reproduced the same stall as v0.7, isolating the problem away from product source at that time.

## Prerequisites to collect before compile
1. exact current minimal Wi-Fi diagnostic sketch path and file identity/hash;
2. exact FQBN/board target;
3. `arduino-cli version`;
4. installed ESP32 platform/core version;
5. relevant compiler/tool package versions;
6. confirmation whether the 3.3.11-era board-package update completed;
7. bounded compile timeout/elapsed-time capture method.

## Permitted execution
- Read local environment/toolchain state.
- Run compile-only minimal Wi-Fi diagnostic.
- Capture command, elapsed time, stdout/stderr and exact error if any.

## Prohibited
- No v0.7 source edits.
- No firmware upload/flash.
- No board erase/reset operations.
- No package/core/toolchain upgrade or repair during this task.
- No broad refactor or feature work.

## Acceptance
PASS if compile completes successfully OR a concrete reproducible environment/toolchain error is captured and classifiable. An unbounded/ambiguous hang is not PASS.

## Rollback / checkpoint
No source or device state should change. Before execution, record current tool versions and sketch identity. If any environment mutation becomes necessary, stop and return for a separate authorized task rather than modifying the environment under TASK-046.

## Non-goals
Do not compile v0.7 itself; that belongs to TASK-047 after TASK-046 PASS. Do not diagnose product-source defects from this test.

## Human gate
Explicit Vlad approval for TASK-046 Codex execution is required. No approval is inferred from any other task. Codex_used: no.
