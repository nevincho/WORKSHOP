# TAI-COG-12

TYPE: WORKSHOP ENGINEERING / IMPLEMENTATION-READY UNIT

OBJECTIVE: Build the Diagnostic / Replay Voice Request Boundary so reviewed COG-11 text can create only bounded, pre-declared read-only diagnostic/replay/status request objects with zero execution, approval, authentication or operational authority.

ENGINEERING_REPOSITORY: nevincho/TANGRA-2.0
BRANCH: tai-cog-12
BASE: 4ca2c0a5814256ab498337b31b4f3eacd27aeedc

PROTECTED: COG-00..11; existing TANGRA runtime; HQ/Hailo/Nano/CA/CurrentTarget/HOROS; FC/carrier/communications authority; production.

FORBIDDEN: diagnostic/replay/Digital-Twin execution, shell/tool/model execution, arbitrary parameters/files/paths, command dispatch, mission/target/config changes, remediation, voice authentication/speaker recognition, Pi5/runtime integration, Codex, COG-13.
