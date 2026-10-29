# WORKSHOP-COMM-G1-FINAL-01 — Exact Source Manifest and Independent Reviewer Handoff

DATE: 2026-10-29
RESULT: EVIDENCE PREPARED / SOURCE NOT COMMITTED / REVIEW NOT VERIFIED
PARENT_BRANCH_HEAD_BEFORE_THIS_FILE: a6cd881b112155b4f7478122ca981b6ead06615c
SOURCE_OF_TRUTH_FOR_BYTES: original conversation attachment workshop-g1-parser-fix.zip.
BYTE_IDENTITY_CHECK: all nine files in original ZIP exactly match those embedded in WORKSHOP_G1_Windows_Validation.zip (excluding the later Windows validation-only files). The hashes below are SHA-256 over original bytes.

| Original relative path (within workshop_g1/) | SHA-256 |
| --- | --- |
| main.py | 547f1ad74620022c0b28d8d4dbf9f11356ab85635032aa6de6b2aa9637d585a6 |
| tests/test_g1.py | c13de6c8e564afb34dd94dcf597ec227ef7963cabf9daee0b33925a9b97caeb6 |
| README.md | 7afbe248238c653292a3458bfd02553495e1258e790c88dd5d2448ee53873808 |
| workshop_g1/app.py | 63a2a24c417b0fe34de04b76f3fe0d17e9d669d16245c4741c9a4609ec1f278c |
| workshop_g1/trusted/STATE_MACHINE.md | c2153030619b91678b7c48bcfb21fbcf9f5a9584dd9a2e9ea93f824bf5d4f358 |
| workshop_g1/trusted/TASK_SCHEMA.md | d0333fdf46f3b9cec92af69c266ddca75999d7a0ac496033069bc86c21cd9610 |
| workshop_g1/trusted/manifest.json | 28a21ffde79f480324fee2d18d84d2ab8777b60709cebdfe97949570ac4ea933 |
| workshop_g1/__init__.py | e39cef633e7b556585711d102d50deb467c76fc10bcd3a3932e73832477ebf49 |
| workshop_g1/core.py | 4104514788622a1c9c35693c7ba6fd4eebaa20c79e1514abd7b78419883d923c |

ADDITIONAL_WINDOWS_HARNESS: Windows validation ZIP contains windows_validation.py, RUN_WINDOWS_VALIDATION.cmd, README_WINDOWS.txt. These were added after the parser-fix ZIP, and are not part of the original nine-file source identity.

OWNER_WINDOWS_EXECUTION: evidence/WORKSHOP-COMM-G1-WINDOWS-EXECUTION-2026-10-29.md. Reported: 17 base tests -> 15 PASS 2 SKIP; 4 additional Windows tests -> 3 PASS 1 SKIP. Total 18 PASS, 3 SKIP, 0 FAIL. NTFS junction test PASS.

## Independent Reviewer instructions (not executed here)

1. First persist the exact original source files on an isolated branch under a dedicated application directory; for each file compare SHA-256 with the manifest above. If even one file differs, BLOCKED.
2. Inspect source and acceptance clauses in planning/WORKSHOP_COMM_G1_READINESS_CONTRACT.md, then inspect Git diff against 0274eaac323381e7140527e3579f68a141b1fc14 and exclude production/canonical changes.
3. Reproduce standard tests in isolated Windows environment and NTFS junction fixture. Document skip conditions distinctly.
4. Review whether OPEN and IMPORT are truly no-write; link/reparse handling; path swaps; task parsing; missing references; trusted manifest version and auth boundary.
5. Evaluate user-provided terminal output as owner-run evidence, not independent reproduction.
6. Return PASS, FAIL or BLOCKED with precise evidence and checkpoint recommendation. Do not conflate tested fixture with comprehensive TOCTOU proof.
7. Only a distinct independent Reviewer may sign off; the original author/coordinator cannot self-certify.

## Remaining blocker

The exact Python source is recoverable from available original artifact but has not been persisted into GitHub by this handoff. The current GitHub connector has no upload-from-local-file capability, and manual transcription would risk byte changes. Independent review and G1 COMPLETE promotion are NOT AUTHORIZED by this evidence alone.

NO CODE CHANGE. NO G2. NO CODEX. NO WORK. NO PAID API.
