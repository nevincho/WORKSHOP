# TANGRA-ARDUPILOT-ESP32-BUILD-01

TASK_ID: TANGRA-ARDUPILOT-ESP32-BUILD-01
PROJECT: TANGRA
PRIORITY: HIGH
MODE: WORKSHOP_CONTROL_ROOM
EXECUTION_CLASS: HUMAN_DIRECTED_REPOSITORY_SAFE
STATUS: BLOCKED_BUILD_PREREQUISITES
RESULT: BLOCKED
CODEX_AUTHORIZED: NO

## Objective
Produce a build-validated ArduCopter firmware binary for ESP32-WROOM-32 4MB with official ArduPilot AP_HAL_ESP32 and an isolated TANGRA board profile.

## Authoritative baseline/evidence
- Official `ArduPilot/ardupilot` repository: examined `libraries/AP_HAL_ESP32/README.md`, `hwdef/esp32diy/hwdef.dat`, `hwdef/esp32empty/hwdef.dat`, `libraries/AP_InertialSensor/AP_InertialSensor_Invensense.cpp` through GitHub connector (current repository default ref at read; exact HEAD commit not materialized locally).
- Source archive `TANGRA_FC_ESP32.zip` SHA-256 `fe917ba2cc8bc87b59e5b38f2ad817b12ad99c712b38a9bd6d1761bbd2c2ee32`, examined `config.h`, `src/sensors/sensor_config.h`, `mpu6050_driver.cpp`, `bmp280_driver.cpp`.
- Current local FC software uses `Wire.begin(21,22,100000)`, MPU6050 0x68, BMP280 probing 0x76 or 0x77. Physical wiring/address NOT VERIFIED. Original FC source has GPS enabled, but THIS isolated ArduPilot build requires GPS disabled; no original firmware changes.
- Official esp32diy targets ICM20948 at 0x68 and I2C 5/18, 22/23, and BMP280 at 0x77; not an as-is TANGRA board match.
- Official Invensense driver has I2C probe, MPU60XX device classification and MPU_WHOAMI_6000 case. Actual MPU6050 FIFO compatibility and runtime boot are NOT VERIFIED.

## Local execution environment evidence
- No ArduPilot source checkout, ESP-IDF checkout, `idf.py`, `xtensa-esp32-elf-gcc`, or flex/bison detected.
- `git ls-remote https://github.com/ArduPilot/ardupilot.git HEAD` failed with `Could not resolve host: github.com` in the container.
- GitHub connector can read selected upstream files but did not provide a complete clone/submodules/compiler as a local build tree.
- `bash -n build_instructions.sh`: PASS.
- Attempt to execute guarded build script with missing checkout fails at `cd: /mnt/data/no-ardupilot: No such file or directory`.
- No `./waf configure` or `./waf copter` compilation was executed because the required source checkout is absent.

## Output artifact
- Local `TANGRA-ARDUPILOT-ESP32-BUILD-01-prebuild.zip` SHA-256 `94fc2137bd22307fcf2e7173e2e48cc3bd2aac88a59267c5584e5151cbfb1787`.
- Contains isolated `board/hwdef.dat` (**provisional, not compile-validated**), build instructions, original source excerpts, and manifest. It is a research/prebuild snapshot, NOT a firmware candidate.
- Provisional board intentionally has no ESP32_RCOUT motor pin allocation. It is not flashable or integrated. GPIO21/22 is only evidenced as current FC source wiring; BMP280 0x76/0x77 are alternative probes, not verified physical address.
- Official HAL board registration and specific hwdef directives have NOT been compiled; errors may remain. Do not claim build-ready.

## Phase/validation
ACCEPTANCE: NOT MET — no ArduCopter binary, no build size, no independent Reviewer PASS.
REVIEW: BLOCKED — missing full source/toolchain prevents independent build qualification. No source-level validation substituted for requested binary.
CHECKPOINT: provenance-only prebuild snapshot, NOT qualified.
NO_ACTION: No Codex, Pi5 access, ESP32 flashing, motors, ESC, Master, MicroNodes or production changes.

## Exact dependency unblock
In an isolated repository-safe execution environment, acquire official ArduPilot checkout with exact commit and recursive submodules/ESP-IDF (per upstream AP_HAL_ESP32 README), installed ESP32 toolchain, and enough build resources. Verify target board recognition, hardware-safe output pin strategy and 4MB flash partition. Then run `./waf configure`, `./waf configure --board=<isolated_board> --debug`, `./waf copter`; capture logs, ELF/BIN, map and flash/RAM and independent Reviewer. Physical BMP address/wiring verification can remain a later hardware gate if compile is otherwise possible.

EVIDENCE: `evidence/TANGRA-ARDUPILOT-ESP32-BUILD-01/PREFLIGHT.md`
BLOCKER: `blockers/TANGRA-ARDUPILOT-ESP32-BUILD-01-ENVIRONMENT.md`

## Offline dependency recovery continuation — 2026-11-04

User supplied and verified three archives in isolated workspace. The pre-existing task is resumed, not duplicated.

- ArduPilot ZIP SHA256 `cb8dcec727294e7330e320bba6dff2a8ede4409925c0380e236055ee4b81d027`, integrity PASS; `ArduCopter/version.h` reports `V4.8.0-dev`; exact Git commit NOT VERIFIED (ZIP lacks .git/gitlink pins).
- ESP-IDF ZIP SHA256 `e147a851e0e9fd0fa03d39e21ce58529612982e515e4b6ab3e37731c73398e52`, integrity PASS; `esp_idf_version.h` reports 5.3.6.
- Xtensa archive SHA256 `4e43e56cd533a39c6b0ccc8b30320b19ce66b0b17e646b53fa84c9bf956b2c83`, integrity PASS; linux compiler `xtensa-esp32-elf-gcc/g++ --version` PASS (13.2.0_20240305). SHA equals official Espressif 20240305 release published SHA.
- ESP-IDF 5.3.6 tools.json currently recommends `xtensa-esp-elf 13.2.0_20250707` instead; exact compiler compatibility NOT VERIFIED.
- ArduPilot source `Tools/scripts/esp32_get_idf.sh` pins IDF commit `cc3203dc4f087ab41b434afff1ed7520c6d90993`; supplied branch ZIP does not establish it contains that commit.
- ArduPilot .gitmodules has 14 submodule paths, all empty in source ZIP, including `modules/waf` and `modules/mavlink`.
- ESP-IDF .gitmodules has 23 submodule paths, all empty, including `components/mbedtls/mbedtls`, `components/lwip/lwip`, `components/esp_wifi/lib`.
- Bounded `./waf --version` startup attempted, exit 1: `Missing waf submodule`; `./waf configure` and `./waf copter` NOT EXECUTED.
- System `flex`, `bison` absent. Other native/Python IDF dependencies NOT VERIFIED.
- Current board draft has no ESC pin mapping. PROPOSED ONLY: GPIO25,27,32,33; avoids GPIO21/22 I²C, UART0 1/3 and ESP32 strapping pins. Do not assume these are free/connected on physical board. Existing draft IMU rotation YAW_90 has no physical orientation evidence.
- Supplied AP_HAL_ESP32 ESP32 sdkconfig defaults specify 4MB and partition table includes 3M factory app. Binary fit NOT VERIFIED.
- Extracted source and compiler into isolated workspace only. No firmware binary, RAM/flash report, compilation, native integration, flashing, Codex, Pi5 or motor operations.
- Full missing list, official source URLs and archive hashes are preserved in `TANGRA-ARDUPILOT-ESP32-BUILD-01-offline-recovery-report.zip` SHA256 `a4dec3c227e49c0b817b63cbbcb5dab756eced610fd738d2d6bbe30de5bb5612` generated as conversation artifact.

Status remains `BLOCKED_BUILD_PREREQUISITES`; prior reviewer gate remains BLOCKED. No qualified checkpoint.
