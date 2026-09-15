# VK-WIRE-05 — Independent C++ Wire Profile v1 conformance evidence

Date: 2026-09-15
Status: CROSS_LANGUAGE_CONFORMANCE_PASS candidate

## Independence / authority
The C++ codec was first committed as `fd2676844144e1716ccd9c2569bfe47ed240f27d` after reading the normative WORKSHOP Wire Profile specification/vectors. The Python implementation source was not fetched for comparison until after that C++ implementation commit. Python is not linked, embedded, invoked by the C++ codec, or used for C++ canonicalization. Later comparison uses a Python harness only as permitted by the task.

Normative authority: `decisions/VK_DISTRIBUTED_WIRE_PROFILE_V1_2026-09-15.md`, schema profile, golden/rejection vectors, conformance plan and WIRE-01 review.

Vector provenance verified from current repository authority before execution:
- golden Git blob `be675835c4f32ea1ae6b24cc37575a2238572ce8`
- rejection Git blob `ac79eb094fea32529d3c8f4652f19ad217b1afe3`
No normative vector was modified.

## Implementation
Branch: `vk-wire-05-cpp`
Validated implementation/workflow head: `5b97561ae3931c05c9f9060b9db95358952de06d`
Files: `cpp/vk_wire_v1/wire_v1.cpp`, strict canonical-wire entrypoint `wire_v1_strict.cpp`, logical-domain probe, CMake build, conformance harness.
Boundary is pure parse/validate/canonicalize/digest/semantic interpretation. No SQLite, runtime, networking, DIST-04, LLM, Host Inspector or device integration.

Dependencies are bounded: ICU `uc` for Unicode NFC/UTF-8 validation and OpenSSL Crypto for SHA-256. JSON parsing/canonical emission is controlled by the VK implementation rather than a JSON framework default.

## Execution
GitHub Actions run `35034044628`; job `104598919933`; conclusion SUCCESS.
OS: Ubuntu 24.04.5.
Compiler: g++ 13.3.0; CMake 3.31.6.
ICU: 74.2. OpenSSL: 3.0.13.
Build: `cmake -S . -B build -DCMAKE_BUILD_TYPE=Release` then `cmake --build build --config Release -j2`.
Test: `python3 cpp/vk_wire_v1/conformance.py` then `python3 cpp/vk_wire_v1/verify_logical_domain.py`. Python is comparison/orchestration only; codec work is executed by C++ binaries.

Results from run logs:
- GOLDEN 12/12
- REJECTION 26/26
- FRONTIER 4/4
- R05 bytes/set/implementation_object => INVALID_TYPE PASS
- CROSS_LANGUAGE_CONFORMANCE_PASS

The strict entrypoint byte-compares C++ canonical output with received bytes before protocol admission, enforcing the normative canonical-wire acceptance rule.

## Comparison basis
The Python reference had already passed its authoritative WIRE-02 suite and the same 12 golden / 26 rejection authority. The comparison harness records that validated Python result per vector and independently computes the normative canonical byte representation for direct C++ byte comparison; expected SHA-256 values are the authoritative vector digests. This does not use Python source as semantic authority.

Machine-readable per-vector matrix: `evidence/VK-WIRE-05/cross_language_matrix.json`. It records every G01..G12, R01..R26 and explicit frontier fixtures F01..F04 without summarizing away mismatches.

## Protected state
VK-DIST-03 source/tests unchanged. VK-WIRE-02 semantics/source unchanged. VK-DIST-04 not started.
