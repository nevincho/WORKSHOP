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
