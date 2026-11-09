cmake_minimum_required(VERSION 3.16)
project(tangra_fc_autonomy_integration LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(ROOT "${CMAKE_CURRENT_LIST_DIR}/..")
set(COMMON_SOURCES
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
set(COMMON_INCLUDES
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
add_executable(test_standalone_autonomy_sim test_autonomy_stack.cpp ${COMMON_SOURCES})
target_include_directories(test_standalone_autonomy_sim PRIVATE ${COMMON_INCLUDES})
add_executable(test_adapter_contracts test_adapter_contracts.cpp
  ${ROOT}/TANGRA-FC-SA-03-01-QUADX-SIM_PACKAGE/src/quadx_simulation.cpp
  ${ROOT}/TANGRA-FC-SA-08-01-MISSION-PROTOCOL_PACKAGE/src/mission_protocol.cpp)
target_include_directories(test_adapter_contracts PRIVATE
  ${ROOT}/TANGRA-FC-SA-03-01-QUADX-SIM_PACKAGE/include
  ${ROOT}/TANGRA-FC-SA-08-01-MISSION-PROTOCOL_PACKAGE/include)
enable_testing()
add_test(NAME standalone_autonomy_sim COMMAND test_standalone_autonomy_sim)
add_test(NAME adapter_contracts COMMAND test_adapter_contracts)
