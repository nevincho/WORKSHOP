# TANGRA-COG-BRIDGE-01 — Incremental regression payload progress

DATE: 2026-09-20
TARGET_HEAD: bd11d92f396b68de00a0f3636ae49ed8310ce420
WORKSPACE: /tmp/tangra_bridge
MODE: incremental bounded materialization

FILES_REQUIRED_TOTAL: 88
FILES_ALREADY_VERIFIED_BEFORE_THIS_BATCH: 8
FILES_ADDED_THIS_BATCH: 2
FILES_VERIFIED_TOTAL: 10
FILES_REMAINING: 78
FAILED_OR_TRUNCATED_RETRIEVAL_THIS_BATCH: NONE

The required-total count covers the active 317-test regression surface, its seven test fixtures, the regression runner/allowlist, the Cognitive Python package files used as the runner's import surface, and the two Phase-B package/test dependency surfaces referenced by the allowlist. The bridge integration test/file is not counted as part of this remaining regression payload.

## Newly materialized and identity-verified

| Repository-relative path | Authoritative blob SHA | Local Git blob SHA | Result |
|---|---|---|---|
| TAI_COGNITIVE_INTEGRATION_PACKAGE/cognitive/backend/tangra_cognitive_backend/__init__.py | 8b6c5f3315661e798a0c14844d63ad30c5aa1274 | 8b6c5f3315661e798a0c14844d63ad30c5aa1274 | PASS |
| TAI_COGNITIVE_INTEGRATION_PACKAGE/cognitive/foundation/tangra_text_boundary/__init__.py | 14637ae55dca7b0e5b01f88e6fca4cf1250143fb | 14637ae55dca7b0e5b01f88e6fca4cf1250143fb | PASS |

Local identity formula:
`sha1(b"blob " + str(len(file_bytes)).encode() + b"\\0" + file_bytes)`

Both files remain in the existing persistent workspace with repository-relative paths.

REGRESSION_EXECUTED: NO
REASON: required payload remains incomplete by design; 78 required files remain.
BRIDGE_TESTS_RERUN: NO


## 2026-09-20 — workspace persistence verification before next batch

Before retrieving any additional repository files, Worker inspected the instructed existing execution workspace:

Command:
```
find /tmp/tangra_bridge -type f | sort | sed 's#^/tmp/tangra_bridge/##'
```

Exit code: 1

stdout: empty

stderr:
```
find: '/tmp/tangra_bridge': No such file or directory
```

ACTUAL_EXECUTION_STATE: the previously materialized `/tmp/tangra_bridge` workspace is not present in the current executor instance.

NEW_FILES_RETRIEVED_THIS_BATCH: 0
NEW_FILES_MATERIALIZED_THIS_BATCH: 0
NEW_FILES_IDENTITY_VERIFIED_THIS_BATCH: 0
REGRESSION_EXECUTED: NO

The repository evidence that 10 files were previously identity-verified remains valid historical evidence, but those local bytes are not present in the current executor and therefore cannot be counted as an executable current 10/88 payload. Continuing while pretending those files still exist would violate the exact-byte/identity requirement.

CURRENT_CONCRETE_BLOCKER: EXECUTION WORKSPACE STATE DID NOT PERSIST ACROSS THIS WORKER TURN.
This is distinct from the superseded repository-to-executor transfer blocker: transfer is proven; persistence of the specific temporary workspace across turns is disproven by direct filesystem inspection in this turn.
