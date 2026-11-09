# Test Provenance — TANGRA-FC-AUTONOMY-INTEGRATION-REWORK-02

Toolchain used: host GCC/CMake C++17 environment.

## Exact commands

```text
cmake -S STEP_02_COMMAND_ARBITRATION -B STEP_02_COMMAND_ARBITRATION/build
cmake --build STEP_02_COMMAND_ARBITRATION/build --clean-first -j2
ctest --test-dir STEP_02_COMMAND_ARBITRATION/build --output-on-failure
cmake -S STEP_03_QUADX_SIMULATION -B STEP_03_QUADX_SIMULATION/build
cmake --build STEP_03_QUADX_SIMULATION/build --clean-first -j2
ctest --test-dir STEP_03_QUADX_SIMULATION/build --output-on-failure
cmake -S STEP_04_VERTICAL_CONTROL -B STEP_04_VERTICAL_CONTROL/build
cmake --build STEP_04_VERTICAL_CONTROL/build --clean-first -j2
ctest --test-dir STEP_04_VERTICAL_CONTROL/build --output-on-failure
cmake -S STEP_05_LOCAL_STATE -B STEP_05_LOCAL_STATE/build
cmake --build STEP_05_LOCAL_STATE/build --clean-first -j2
ctest --test-dir STEP_05_LOCAL_STATE/build --output-on-failure
cmake -S STEP_06_HORIZONTAL_GUIDANCE -B STEP_06_HORIZONTAL_GUIDANCE/build
cmake --build STEP_06_HORIZONTAL_GUIDANCE/build --clean-first -j2
ctest --test-dir STEP_06_HORIZONTAL_GUIDANCE/build --output-on-failure
cmake -S STEP_07_WAYPOINT_EXECUTOR -B STEP_07_WAYPOINT_EXECUTOR/build
cmake --build STEP_07_WAYPOINT_EXECUTOR/build --clean-first -j2
ctest --test-dir STEP_07_WAYPOINT_EXECUTOR/build --output-on-failure
cmake -S STEP_08_MISSION_PROTOCOL -B STEP_08_MISSION_PROTOCOL/build
cmake --build STEP_08_MISSION_PROTOCOL/build --clean-first -j2
ctest --test-dir STEP_08_MISSION_PROTOCOL/build --output-on-failure
cmake -S STEP_09_PARAMETERS -B STEP_09_PARAMETERS/build
cmake --build STEP_09_PARAMETERS/build --clean-first -j2
ctest --test-dir STEP_09_PARAMETERS/build --output-on-failure
cmake -S STEP_10_WATCHDOG -B STEP_10_WATCHDOG/build
cmake --build STEP_10_WATCHDOG/build --clean-first -j2
ctest --test-dir STEP_10_WATCHDOG/build --output-on-failure
cmake -S STEP_11_GNSS_COMPASS -B STEP_11_GNSS_COMPASS/build
cmake --build STEP_11_GNSS_COMPASS/build --clean-first -j2
ctest --test-dir STEP_11_GNSS_COMPASS/build --output-on-failure
cmake -S STEP_12_MISSION_PLANNER -B STEP_12_MISSION_PLANNER/build
cmake --build STEP_12_MISSION_PLANNER/build --clean-first -j2
ctest --test-dir STEP_12_MISSION_PLANNER/build --output-on-failure
cmake -S INTEGRATION -B INTEGRATION/build
cmake --build INTEGRATION/build --clean-first -j2
ctest --test-dir INTEGRATION/build --output-on-failure
cmake -S STEP_13_USB_CONFIGURATION -B STEP_13_USB_CONFIGURATION/build
cmake --build STEP_13_USB_CONFIGURATION/build --clean-first -j2
ctest --test-dir STEP_13_USB_CONFIGURATION/build --output-on-failure
```

## Exit codes

```text
[STEP_02_COMMAND_ARBITRATION configure] exit=0
[STEP_02_COMMAND_ARBITRATION build] exit=0
[STEP_02_COMMAND_ARBITRATION test] exit=0
[STEP_03_QUADX_SIMULATION configure] exit=0
[STEP_03_QUADX_SIMULATION build] exit=0
[STEP_03_QUADX_SIMULATION test] exit=0
[STEP_04_VERTICAL_CONTROL configure] exit=0
[STEP_04_VERTICAL_CONTROL build] exit=0
[STEP_04_VERTICAL_CONTROL test] exit=0
[STEP_05_LOCAL_STATE configure] exit=0
[STEP_05_LOCAL_STATE build] exit=0
[STEP_05_LOCAL_STATE test] exit=0
[STEP_06_HORIZONTAL_GUIDANCE configure] exit=0
[STEP_06_HORIZONTAL_GUIDANCE build] exit=0
[STEP_06_HORIZONTAL_GUIDANCE test] exit=0
[STEP_07_WAYPOINT_EXECUTOR configure] exit=0
[STEP_07_WAYPOINT_EXECUTOR build] exit=0
[STEP_07_WAYPOINT_EXECUTOR test] exit=0
[STEP_08_MISSION_PROTOCOL configure] exit=0
[STEP_08_MISSION_PROTOCOL build] exit=0
[STEP_08_MISSION_PROTOCOL test] exit=0
[STEP_09_PARAMETERS configure] exit=0
[STEP_09_PARAMETERS build] exit=0
[STEP_09_PARAMETERS test] exit=0
[STEP_10_WATCHDOG configure] exit=0
[STEP_10_WATCHDOG build] exit=0
[STEP_10_WATCHDOG test] exit=0
[STEP_11_GNSS_COMPASS configure] exit=0
[STEP_11_GNSS_COMPASS build] exit=0
[STEP_11_GNSS_COMPASS test] exit=0
[STEP_12_MISSION_PLANNER configure] exit=0
[STEP_12_MISSION_PLANNER build] exit=0
[STEP_12_MISSION_PLANNER test] exit=0
[INTEGRATION configure] exit=0
[INTEGRATION build] exit=0
[INTEGRATION test] exit=0
[STEP_13_USB_CONFIGURATION configure] exit=0
[STEP_13_USB_CONFIGURATION build] exit=0
[STEP_13_USB_CONFIGURATION test] exit=0
OVERALL_EXIT=0
```

## Full CTest logs

```text
===== INTEGRATION_test.log =====
Start 1: standalone_autonomy_sim
1/2 Test #1: standalone_autonomy_sim .......... Passed
Start 2: adapter_contracts
2/2 Test #2: adapter_contracts ................ Passed
100% tests passed, 0 tests failed out of 2

===== STEP_02_COMMAND_ARBITRATION_test.log =====
Start 1: command_arbitration
1/1 Test #1: command_arbitration .............. Passed
100% tests passed, 0 tests failed out of 1

===== STEP_03_QUADX_SIMULATION_test.log =====
Start 1: quadx_sim
1/2 Test #1: quadx_sim ........................ Passed
Start 2: real_fc_adapter_contracts
2/2 Test #2: real_fc_adapter_contracts ........ Passed
100% tests passed, 0 tests failed out of 2

===== STEP_04_VERTICAL_CONTROL_test.log =====
Start 1: vertical
1/1 Test #1: vertical ......................... Passed
100% tests passed, 0 tests failed out of 1

===== STEP_05_LOCAL_STATE_test.log =====
Start 1: local_state
1/1 Test #1: local_state ...................... Passed
100% tests passed, 0 tests failed out of 1

===== STEP_06_HORIZONTAL_GUIDANCE_test.log =====
Start 1: guidance
1/1 Test #1: guidance ......................... Passed
100% tests passed, 0 tests failed out of 1

===== STEP_07_WAYPOINT_EXECUTOR_test.log =====
Start 1: waypoint
1/1 Test #1: waypoint ......................... Passed
100% tests passed, 0 tests failed out of 1

===== STEP_08_MISSION_PROTOCOL_test.log =====
Start 1: protocol
1/1 Test #1: protocol ......................... Passed
100% tests passed, 0 tests failed out of 1

===== STEP_09_PARAMETERS_test.log =====
Start 1: parameters
1/1 Test #1: parameters ....................... Passed
100% tests passed, 0 tests failed out of 1

===== STEP_10_WATCHDOG_test.log =====
Start 1: watchdog
1/1 Test #1: watchdog ......................... Passed
100% tests passed, 0 tests failed out of 1

===== STEP_11_GNSS_COMPASS_test.log =====
Start 1: navobs
1/1 Test #1: navobs ........................... Passed
100% tests passed, 0 tests failed out of 1

===== STEP_12_MISSION_PLANNER_test.log =====
Start 1: mp_adapter
1/1 Test #1: mp_adapter ....................... Passed
100% tests passed, 0 tests failed out of 1

===== STEP_13_USB_CONFIGURATION_test.log =====
Start 1: usb_configuration
1/1 Test #1: usb_configuration ................ Passed
100% tests passed, 0 tests failed out of 1
```

The original raw test log files are also included in the generated ZIP under `VALIDATION_LOGS/`.
