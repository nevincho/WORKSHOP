# TANGRA-ARDUPILOT-ESP32-BUILD-01 — verified build environment blocker

TASK_ID: TANGRA-ARDUPILOT-ESP32-BUILD-01
BLOCKER_TYPE: BUILD_ENVIRONMENT_ACQUISITION
STATE: OPEN
DATE: 2026-11-04

The required complete official ArduPilot source checkout including AP_HAL_ESP32, recursive ESP-IDF submodules and Xtensa ESP32 compiler is not present in the available isolated build environment. Local git cannot resolve github.com (`git ls-remote` fails with DNS). GitHub connector read individual official files but cannot substitute for full local source and submodules. `./waf configure` and `./waf copter` were NOT RUN.

This is a prerequisite/environment blocker, NOT an established firmware implementation defect.
Flash/RAM, binary, compiler diagnostics and Reviewer PASS cannot be produced. The generated provisional board file is NOT build validated. No affected production/runtime sources modified.

SMALLEST_UNBLOCK:
Provide a reproducible official ArduPilot source checkout including submodules and ESP-IDF toolchain in the isolated build executor, or enable its repository/network acquisition. Pin ArduPilot commit, ESP-IDF toolchain version, verify board registration and attempt actual `./waf copter`. Preserve 4MB flash constraints and do not flash.

HARDWARE_GATE (NOT BUILD PRECONDITION): verify actual SDA/SCL wiring and BMP280 I2C address on separate authorized isolated bench. Sensor FIFO and physical MAVLink/USB are not validated.

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
