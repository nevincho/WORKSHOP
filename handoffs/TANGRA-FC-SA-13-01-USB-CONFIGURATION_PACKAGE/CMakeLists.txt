cmake_minimum_required(VERSION 3.16)
project(tangra_fc_step13 LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
add_library(usb_config
    ../TANGRA-FC-SA-09-01-PARAMETERS_PACKAGE/src/parameters.cpp
    src/usb_configuration.cpp)
target_include_directories(usb_config PUBLIC
    ../TANGRA-FC-SA-09-01-PARAMETERS_PACKAGE/include
    include)
add_executable(test_usb_configuration tests/test_usb_configuration.cpp)
target_link_libraries(test_usb_configuration PRIVATE usb_config)
enable_testing()
add_test(NAME usb_configuration COMMAND test_usb_configuration)
