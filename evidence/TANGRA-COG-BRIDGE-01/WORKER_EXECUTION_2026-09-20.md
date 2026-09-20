# TANGRA-COG-BRIDGE-01 — Worker execution evidence

DATE: 2026-09-20
ROLE: WORKSHOP WORKER
TARGET_BRANCH: nevincho/TANGRA-2.0:cognitive-bridge-integration
ORIGINAL_REQUESTED_HEAD: e2d5cd10b780d87ef5b5ff25b50a2f10c2a9caef
CURRENT_REPAIR_HEAD: bd11d92f396b68de00a0f3636ae49ed8310ce420
RESULT: PARTIAL_EXECUTION / BRIDGE_QUALIFICATION_PASS / CUMULATIVE_REGRESSION_PENDING

## Identity-verified materialized files

| Repository-relative path | Authoritative blob | Local Git blob | Result |
|---|---|---|---|
| TAI_COGNITIVE_INTEGRATION_PACKAGE/integration/cognitive_bridge.py | 5f4a6346fa70e369452067d9d96f776a84468a64 | 5f4a6346fa70e369452067d9d96f776a84468a64 | PASS |
| TAI_COGNITIVE_INTEGRATION_PACKAGE/cognitive/foundation/tangra_cognitive_substrate/__init__.py | b5e32726db671d8dd666c85b9568eeeb2ef7f524 | b5e32726db671d8dd666c85b9568eeeb2ef7f524 | PASS |
| TAI_COGNITIVE_INTEGRATION_PACKAGE/cognitive/foundation/tangra_cognitive_substrate/contracts.py | 228d33108bd7b5494a5814653dd4ee38ab26869c | 228d33108bd7b5494a5814653dd4ee38ab26869c | PASS |
| TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/integration/test_cognitive_bridge.py (original) | c67b9fe1ba85c372947b5e14c43cfdb5d3190695 | c67b9fe1ba85c372947b5e14c43cfdb5d3190695 | PASS |
| TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/integration/test_cognitive_bridge.py (repair 1) | 4389b1d66519734afb4734df4ddf1034f39f629c | 4389b1d66519734afb4734df4ddf1034f39f629c | PASS |
| TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/integration/test_cognitive_bridge.py (repair 2/current) | 8ee11ea297516f6a1452a5c5a2241db14b91e475 | 8ee11ea297516f6a1452a5c5a2241db14b91e475 | PASS |

Local Git blob calculation used:
`sha1(b"blob " + str(len(bytes)).encode() + b"\\0" + bytes)`.

## Executed qualification — original test

Command:
```
python -m pytest -q TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/integration/test_cognitive_bridge.py
```

Exit code: 2

stdout/stderr:
```
ERROR collecting TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/integration/test_cognitive_bridge.py
FileNotFoundError: [Errno 2] No such file or directory:
'/tmp/tangra_bridge/TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/cognitive/foundation'
1 error in 0.18s
```

Executed defect: qualification test computed package ROOT with `parents[1]` although the test is under `tests/integration`.

Repair commit:
`06291d97fe5d093d3e8809426d3dc73a636fd012`
Only test-path defect repaired: `parents[1]` -> `parents[2]`.

## Executed qualification — repair 1

Same command.

Exit code: 2

stdout/stderr:
```
ERROR collecting TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/integration/test_cognitive_bridge.py
ModuleNotFoundError: No module named 'tangra_cognitive_substrate'
1 error in 0.22s
```

Executed defect: qualification test inserted each child package directory into `sys.path`; importing package `tangra_cognitive_substrate` requires its parent `cognitive/foundation` on `sys.path`.

Repair commit:
`bd11d92f396b68de00a0f3636ae49ed8310ce420`
Only test import-path defect repaired.

## Executed qualification — current repaired head

Command:
```
python -m pytest -q TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/integration/test_cognitive_bridge.py
```

Exit code: 0

stdout:
```
.................                                                        [100%]
17 passed in 0.21s
```

stderr: empty

Exact test count: 17 passed / 0 failed / 0 errors.

BRIDGE_QUALIFICATION: PASS

## Existing cumulative regression surface

Authoritative regression runner:
`TAI_COGNITIVE_INTEGRATION_PACKAGE/regression/run_units_1_10.py`
blob: `b7c2cdfc791578174e4356086cc6c0e4b04af5b5`

Authoritative allowlist:
`TAI_COGNITIVE_INTEGRATION_PACKAGE/regression/units_1_10_active_surface.json`
blob: `6e9ede9d5dd71083ca128fb2255d7fdd1a9b2f25`

Expected active regression count: 317 across 15 allowlisted test files.

The cumulative 317-test payload was not fully materialized/executed in this Worker turn. No regression PASS is claimed.

## Current gate state
- repository -> executor materialization: PROVEN AVAILABLE; prior execution-access/materialization blocker is superseded.
- bridge implementation qualification: PASS after two bounded test-harness path repairs.
- Cognitive cumulative regression: PENDING.
- bounded bridge end-to-end behavior covered by the 17 executed integration tests: PASS.
- Reviewer final verdict: NOT YET ELIGIBLE because required cumulative regression evidence is incomplete.
- checkpoint: NOT CREATED.
- Pi: UNTOUCHED.
- Codex: NOT USED.
