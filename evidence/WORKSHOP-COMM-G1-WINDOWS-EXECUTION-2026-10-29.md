# WORKSHOP-COMM-G1-01 — Windows Execution Evidence (Owner-Reported)

DATE: 2026-10-29
RESULT: 18 PASS, 3 SKIP, 0 FAIL from 21 executed/discovered tests.
STATUS: REPORTED_BY_OWNER — raw terminal text supplied in chat; independent reviewer has NOT inspected/reproduced the run.
EXECUTION_CONTEXT: Windows command prompt at F:\WORKSHOP_DESKTOP\WORKSHOP_G1_Windows_Validation, RUN_WINDOWS_VALIDATION.cmd.
BASE_REFERENCE: workshop-comm-g1-final-01 @ c557ee6190dca5749d0a11be16034dcd2cfc15ce.

## Run 1 — original test_g1 suite
Command: python -m unittest discover -s tests -v (as invoked by batch file)
Observed: 17 tests in 0.244s; OK (skipped=2): 15 PASS, 2 SKIP.
Skipped:
- test_symlinks — 'symlinks unavailable'
- test_windows_reparse_attribute — 'Requires real Windows NTFS junction/reparse fixture and post-snapshot'
All other reported tests including trust bundle, missing trust, invalid paths, injection and open-no-mutation PASS.

## Run 2 — standalone WindowsQualification
Command: python windows_validation.py (as invoked by batch file)
Observed: 4 tests in 0.112s; OK (skipped=1): 3 PASS, 1 SKIP.
PASS: test_create_exact_files_and_repeat_denied; test_ntfs_junction_denied; test_open_import_no_mutation.
Skipped: test_ntfs_file_symlink_denied_if_available — 'Windows file symlinks unavailable without privileges/Developer Mode'.

## Qualification limits
- A real NTFS junction path denial test PASS is now observed, superseding previous statement that no Windows junction test had run. This is only the covered fixture, not a proof of race-resistant comprehensive reparse security.
- Owner-reported execution output is not an independent Reviewer verdict.
- Filesystem snapshot checks are for disposable fixtures, not for arbitrary customer repositories.
- Actual GitHub source persistence/identity of Python implementation and independent review remain NOT VERIFIED.
- Full dependency/reference resolution and path TOCTOU still not fully qualified.
- No G1 COMPLETE promotion. No main, production or target repository modifications.

NEXT_STEP: Exact source persistence and independent Windows-focused review of frozen code/evidence, followed by checkpoint only if independently accepted.
