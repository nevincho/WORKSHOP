cmake_minimum_required(VERSION 3.16)
project(tangra_fc_autonomy_integration LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 17)
set(ROOT "${CMAKE_CURRENT_LIST_DIR}/..")
add_executable(test_autonomy_stack
  test_autonomy_stack.cpp
  ${ROOT}/TANGRA-FC-SA-02-01_COMMAND_ARBITRATION_PACKAGE/src/command_arbitration.cpp
  ${ROOT}/TANGRA-FC-SA-03-01-QUADX-SIM_PACKAGE/src/quadx_simulation.cpp
  ${ROOT}/TANGRA-FC-SA-04-01-VERTICAL_PACKAGE/src/vertical_control.cpp
  ${ROOT}/TANGRA-FC-SA-05-01-LOCAL-STATE_PACKAGE/src/local_navigation_state.cpp
  ${ROOT}/TANGRA-FC-SA-06-01-GUIDANCE_PACKAGE/src/horizontal_guidance.cpp
  ${ROOT}/TANGRA-FC-SA-07-01-WAYPOINT-EXECUTOR_PACKAGE/src/waypoint_executor.cpp
  ${ROOT}/TANGRA-FC-SA-08-01-MISSION-PROTOCOL_PACKAGE/src/mission_protocol.cpp
  ${ROOT}/TANGRA-FC-SA-09-01-PARAMETERS_PACKAGE/src/parameters.cpp
  ${ROOT}/TANGRA-FC-SA-10-01-WATCHDOG_PACKAGE/src/watchdog.cpp
  ${ROOT}/TANGRA-FC-SA-11-01-GNSS-COMPASS_PACKAGE/src/navigation_observations.cpp
  ${ROOT}/TANGRA-FC-SA-12-01-MISSION-PLANNER_PACKAGE/src/mission_planner_adapter.cpp)
target_include_directories(test_autonomy_stack PRIVATE
  ${ROOT}/TANGRA-FC-SOFTWARE-AUTONOMY_COMMON/include
  ${ROOT}/TANGRA-FC-SA-02-01_COMMAND_ARBITRATION_PACKAGE/include
  ${ROOT}/TANGRA-FC-SA-03-01-QUADX-SIM_PACKAGE/include
  ${ROOT}/TANGRA-FC-SA-04-01-VERTICAL_PACKAGE/include
  ${ROOT}/TANGRA-FC-SA-05-01-LOCAL-STATE_PACKAGE/include
  ${ROOT}/TANGRA-FC-SA-06-01-GUIDANCE_PACKAGE/include
  ${ROOT}/TANGRA-FC-SA-07-01-WAYPOINT-EXECUTOR_PACKAGE/include
  ${ROOT}/TANGRA-FC-SA-08-01-MISSION-PROTOCOL_PACKAGE/include
  ${ROOT}/TANGRA-FC-SA-09-01-PARAMETERS_PACKAGE/include
  ${ROOT}/TANGRA-FC-SA-10-01-WATCHDOG_PACKAGE/include
  ${ROOT}/TANGRA-FC-SA-11-01-GNSS-COMPASS_PACKAGE/include
  ${ROOT}/TANGRA-FC-SA-12-01-MISSION-PLANNER_PACKAGE/include)
enable_testing()
add_test(NAME autonomy_stack COMMAND test_autonomy_stack)
