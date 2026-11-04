# TANGRA-ARDUPILOT-ESP32-BUILD-01 — preflight / build evidence

DATE: 2026-11-04
RESULT: BLOCKED_ENVIRONMENT

## Source-of-truth verified
Upstream GitHub API blobs:
- ArduPilot/ardupilot `libraries/AP_HAL_ESP32/README.md` blob `c1feb797b84109e4461bb77ba04eb5a54ee6f506`;
- `libraries/AP_HAL_ESP32/hwdef/esp32diy/hwdef.dat` blob `46b95c5a8ac6fcfb43e1080c0b832b336cb630c7`;
- `libraries/AP_HAL_ESP32/hwdef/esp32empty/hwdef.dat` blob `ee143e83b0873216916f47609e87cfc12c024887`;
- `libraries/AP_InertialSensor/AP_InertialSensor_Invensense.cpp` blob `5895ce5c2f1e5a181cb36e87d3949d456889617d`.
These are individual blob IDs, NOT a consistent pinned ArduPilot repository commit. Exact checkout required before an authoritative build.
Upstream instructions explicitly require recursive submodules, ESP-IDF and `./waf configure` followed by `./waf configure --board=esp32diy --debug`, `./waf copter`.
Source code shows Invensense I2C probe and MPU60XX support but no demonstrated MPU6050 FIFO hardware operation.

User source archive SHA256 `fe917ba2cc8bc87b59e5b38f2ad817b12ad99c712b38a9bd6d1761bbd2c2ee32`.
Relevant file lines: `src/sensors/mpu6050_driver.cpp` uses `Wire.begin(21,22,100000)`; `src/sensors/sensor_config.h` sets pins and MPU6050 0x68; `src/sensors/bmp280_driver.cpp` enumerates both 0x76, 0x77. These are *source facts*, not confirmed physical connections. Existing original FC GPS is enabled; no changes to it.

## Commands / results
`command -v git` -> /usr/bin/git
`command -v ninja` -> /usr/bin/ninja
`command -v cmake` -> /usr/bin/cmake
`command -v idf.py` -> missing
`command -v xtensa-esp32-elf-gcc` -> missing
`command -v flex` / `bison` -> missing
`ls /mnt/data/ardupilot` -> No such file or directory
`git ls-remote https://github.com/ArduPilot/ardupilot.git HEAD` -> fatal: Could not resolve host github.com
`bash -n build_instructions.sh` -> PASS
Guarded build script test with `ARDUPILOT_CHECKOUT=/mnt/data/no-ardupilot` -> FAIL, missing directory before configure.

No waf compile launched; no compiler diagnostics, .elf, .bin, memory map or 4MB fit data exist.

## Prebuild package
`TANGRA-ARDUPILOT-ESP32-BUILD-01-prebuild.zip` SHA256 `94fc2137bd22307fcf2e7173e2e48cc3bd2aac88a59267c5584e5151cbfb1787`.
Contains provisional uncompiled board/hwdef.dat, build_instructions.sh, manifest.json and source evidence excerpts. No ESP32_RCOUT assignments by design; no motor output hardware claims. Syntax of hwdef not checked by ArduPilot generator, and no board compile. GPS serial default disabled *in draft only*.
Review: BLOCKED for build qualification, no qualified binary/source checkpoint.
