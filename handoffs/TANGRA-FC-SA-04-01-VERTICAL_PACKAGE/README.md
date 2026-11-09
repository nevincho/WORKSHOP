# Vertical state and altitude control

Create simulation-first vertical state/velocity target and bounded altitude-hold control contract with validity/freshness handling.

Host validation: GCC 14.2 / CMake 3.31.6 / CTest vertical 1/1 PASS.
Local FC integration: NOT_YET_PERFORMED.
Map existing estimator/barometer state into VerticalState and map collective_delta into the existing controller architecture.
