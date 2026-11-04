# TANGRA-FC-CONFIG-01 — SOURCE ACCESS BLOCKER

TASK_ID: TANGRA-FC-CONFIG-01  
PROJECT: TANGRA  
BLOCKER_TYPE: ACCESS

## EXACT_BLOCKER
The current authoritative TANGRA ESP32 Flight Controller source tree at
`D:\RaspberryPi5\TANGRA\WORKSPACE\TANGRA_FC_ESP32`
is not directly readable from the current WORKSHOP execution boundary, and no current GitHub repository/branch/ref containing that FC source could be established.

Because the requested implementation must be derived from the actual existing MAVLink/config/init/safety interfaces, source-dependent implementation would require guessing and is therefore prohibited.

## EVIDENCE
Repository access was attempted before declaring the blocker.

Inspected repositories:
- `nevincho/TANGRA-DOCS` (canonical TANGRA repository)
- `nevincho/TANGRA-2.0`
- `nevincho/WORKSHOP`

GitHub searches returned no authoritative FC source for:
- `TANGRA_FC_ESP32`
- `v0.7.0-quad-x-usb-bench`
- `MANUAL_CONTROL 69`
- FC `config.h` / MAVLink ESP32 identifiers

Project/Library retrieval found historical transcripts/inventory that reference the Windows FC path and earlier compile/upload activity. Those records are navigation/history only; they are not the current authoritative source and cannot establish present interfaces or source state.

No FC source file such as `TANGRA_FC_ESP32.ino`, current `config.h`, MAVLink implementation source, or initialization/consumer source is available as an authoritative current file in the execution context.

## ROOT_CAUSE
Required local Windows source access is outside the current WORKSHOP repository execution boundary, and the FC source has not been identified in an accessible authoritative repository/ref.

## AFFECTED_DEPENDENCY_CHAIN
Current-source verification
-> parameter inventory
-> runtime registry design
-> MAVLink PARAM implementation
-> NVS persistence
-> consumer wiring
-> deterministic tests
-> independent review
-> reviewed Codex integration package

The chain is blocked at current-source verification.

## SAFE_CURRENT_CHECKPOINT
No target FC source or firmware was modified.
No FC flashing occurred.
No serial ports were opened.
No motors/ESCs were activated.
No Codex invocation occurred.
WORKSHOP coordination repository only was updated with this task/blocker record.

## SMALLEST_REQUIRED_UNBLOCK_ACTION
Make the exact current FC source tree available to WORKSHOP as either:
1. an accessible GitHub repository + branch/ref/commit containing `TANGRA_FC_ESP32`, or
2. an uploaded exact source snapshot/archive from `D:\RaspberryPi5\TANGRA\WORKSPACE\TANGRA_FC_ESP32`.

The source package must include the existing `config.h`, MAVLink implementation, FC entrypoint/initialization, affected parameter consumers, and build metadata needed to establish an exact pre-change checkpoint.

## HUMAN_DECISION_REQUIRED
YES

## INDEPENDENT_WORK_ALLOWED
None within TANGRA-FC-CONFIG-01 that would require inferring current FC interfaces. Source-independent implementation is intentionally not permitted by the task.

## NOT_VERIFIED_ITEMS
- Human-supplied baseline findings against the current source.
- Current flashed firmware identity.
- Exact current FC source revision/checkpoint.
- Exact current parameter inventory and limits.
- Existing MAVLink library/version and framing helpers.
- Current initialization ordering.
- Current NVS/Preferences usage elsewhere in the FC.
- Current build reproducibility.
- Hardware behavior.
