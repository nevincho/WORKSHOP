# WORKSHOP Desktop G1 — read-only prototype

Source baseline: `nevincho/WORKSHOP`, `workshop-comm-g1-pre-01` `0274eaac323381e7140527e3579f68a141b1fc14`.

Run from this directory with Python 3.11+ and Tkinter installed: `python main.py`.
Tests: `python -m unittest discover -s tests -v`.

The bundle pins exact task/state schema source bytes to WORKSHOP commit `a2ec5b3c16c4b21548ce1570bcac20d6276b2b7a` and validates their SHA-256 before interpreting tasks. No Git CLI, AI API, subprocess, credentials or network operations. CREATE creates one empty new workspace with `workspace.json` and `tasks/`. OPEN/IMPORT inspect local directories only; they do not write to the inspected tree.

Scope and qualification limits:
- This is a source prototype, not Windows installer or qualified application.
- No independent review and no actual Windows NTFS reparse/junction tests; Linux symlink check alone is insufficient.
- No guarantee against hostile filesystem race or simultaneous attacker-controlled rename: TOCTOU containment and Windows reparse test still need an implementation/review gate.
- IMPORT currently accepts directory selections, not an individual file.
- Task parser validates required fields, enums and duplicate IDs, but does not yet resolve cross-document dependencies/references, and does not yet implement all declared Windows path diagnostics.
- UI cannot run engineering tasks, change canonical statuses, or connect to GitHub.
- Bundled trust assumes an intact installed application: not a distribution signature.
- No source was added to main.

Next: independent reviewer, real Windows tests, and contract-gap repair under owner-directed bounded scope. Do not promote task to COMPLETE.

## G1 parser classification patch (2026-10-29)

- In `tasks/`, ordinary Markdown files without a TASK_ID declaration or task-like filename are ignored as documentation (not `INVALID_TASK`).
- Legacy task-like filenames without TASK_ID are reported as `LEGACY_TASK_FORMAT`.
- Files declaring TASK_ID but lacking mandatory canonical fields are reported as `INCOMPLETE_TASK_SCHEMA`.
- Canonical task validation rules remain unchanged. CREATE/OPEN/IMPORT UI and write behaviour remain unchanged.
- Tests: 17 executed; 16 passed, 1 skipped (real Windows NTFS reparse test). Real-world 120 diagnostic count has not been re-checked on the user's Windows directory.
