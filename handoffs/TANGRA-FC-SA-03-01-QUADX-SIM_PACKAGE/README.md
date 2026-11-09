# Closed-loop Quad-X vehicle simulation

Standalone STEP_3 software package.

Objective: Create deterministic plant and closed-loop harness around existing controller, mixer and estimator interfaces without implementing an alternate production controller.

Local FC integration: `NOT_YET_PERFORMED`.
Adapters required: IControllerAdapter, IMixerAdapter, IEstimatorAdapter must later bind to real FC components.
Physical outputs/arming: OFF.

Host validation: GCC 14.2 / CMake 3.31.6 / CTest 1/1 PASS.
