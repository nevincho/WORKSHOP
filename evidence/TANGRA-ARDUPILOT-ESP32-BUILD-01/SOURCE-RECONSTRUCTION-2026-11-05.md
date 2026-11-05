# TANGRA-ARDUPILOT-ESP32-BUILD-01 — reconstructed source checkpoint evidence

DATE: 2026-11-05
TASK: TANGRA-ARDUPILOT-ESP32-BUILD-01
RESULT: BLOCKED_ESP_IDF_PREREQUISITES

## Reconstructed archive
Three existing user attachments combined in numerical order with shell stream redirection (not held in RAM). Rebuilt TAR.GZ SHA-256 `63df137f110449c339668357b52aaedefeee6627a430eccaaf097d513eedd1f5`. `gzip -t` PASS; `tar -tzf` PASS, 30,461 entries. Extracted in isolated `/mnt/data/tangra_ardupilot_recovery/extracted/ardupilot`.

## Exact Git revision
`git -c safe.directory='*' rev-parse HEAD`: `adb3766244981e0cd5c4f7fa58d9fc4142278e9f`, exact match. The archive's ownership triggered Git's `dubious ownership` guard, so read-only invocations used `git -c safe.directory='*'` without modifying global config. `git submodule status --recursive` timed out; a bounded Python read-only walk of Git index gitlinks and each local nested checkout returned 16 pinned gitlinks across 17 repositories, 0 mismatch. `modules/waf`, `modules/mavlink` and their Git metadata exist and are populated.

## First missing dependency
`Tools/scripts/esp32_get_idf.sh` pins ESP-IDF `cc3203dc4f087ab41b434afff1ed7520c6d90993`; `modules/esp_idf` missing. The user-provided `esp-idf-release-v5.3.zip` is accessible but Git metadata absent, 23/23 declared submodule dirs unpopulated. Missing examples: `components/mbedtls/mbedtls`, `components/lwip/lwip`, `components/esp_wifi/lib`, `components/esp_phy/lib`. Therefore neither exact IDF revision nor dependency completeness is established. Official source recovery: checkout pinned ESP-IDF commit with recursive git submodules (`git -C modules/esp_idf submodule update --init --recursive` after pinned clone); avoid arbitrary ZIP versions. Current `flex`, `bison` absent; IDF Python package dependencies not qualified.

## Other checks
Supplied Xtensa archive `xz -t`: PASS. Earlier toolchain execution evidence exists, but not repeated after reaching first prerequisite blocker. Available provisional `board/hwdef.dat` is SOURCE-ONLY; IMU orientation, RCOUT and actual board compatibility NOT VERIFIED. No waf configure/copter compilation attempted; no firmware metrics or binary; no independently validated build checkpoint.

## Protected
No Codex, flashing, motors, Pi5, physical FC access or production modification. Original source and user archives protected. Isolated extraction is the sole working copy.
