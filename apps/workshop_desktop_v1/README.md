# WORKSHOP Desktop V1 — Integrated implementation candidate (G1–G7)

**Not a finished or independently accepted commercial release.** The owner requested a combined G2–G7 implementation candidate before consolidated testing. This directory is isolated from the existing G1 application and WORKSHOP policy/coordination files.

## Implemented surfaces

- **G1 reuse:** import the existing apps/workshop_g1/workshop_g1/core.py for trusted CREATE and strict read-only OPEN; the G1 source and bundled trusted manifest are not copied or changed.
- **G2:** Git-backed local coordination store in .workshop_v1/coordination, explicit immutable plan hash, current remote Git SHA, HMAC-authenticated approval bound to local OS user, zero-cost executor, event hash chain, dirty-repo and interrupted-run fail-closed behavior.
- **G3:** fixed subprocess Markdown writer. Creates only a staged file, never runs user commands, never modifies the selected repository and never contacts an AI API. Timeout/cancel available.
- **G4:** separate reviewer subprocess checks exact output bytes, SHA-256, path allowlist and operation; human final acceptance is separate. This is deterministic review, **not an independent human/security review**. Accepted proposal references are checkpointed in Git.
- **G5:** public GitHub read-only branch HEAD and file existence checks. Optional fine-grained PAT stored in Windows Credential Manager. Only after explicit approval, separate-process review and a second human confirmation can the app create a new proposal branch, add ONE Markdown file and open a **draft** pull request. It never pushes to the base branch or merges a PR.
- **G6:** Tkinter tabbed desktop UI with G1 task browser, planning, approval, execution/review, GitHub credential controls and evidence browser. Windows onedir PyInstaller build script.
- **G7:** Inno Setup per-user installer script and consolidated integration/negative tests.

## Run from source (Windows)

Requires Python 3.11+, Git for Windows on PATH, a current checkout of WORKSHOP with both apps/workshop_g1/ and apps/workshop_desktop_v1/, and internet for live GitHub reads.

    cd apps\workshop_desktop_v1
    python main.py

Create a new G1 workspace or select an existing one. Consent to creation of the separate .workshop_v1/coordination Git repository. Enter an owner/repo, branch, docs/*.md path and Markdown content. Create plan -> approve -> run/review -> explicitly submit draft PR. Store a fine-grained GitHub PAT only when draft PR submission is intended. The PAT must have repository Contents write and Pull Requests write for the selected test repository. Revoke the token locally from the UI and separately on GitHub.

## Consolidated test/build

    cd apps\workshop_desktop_v1
    python -B -m unittest discover -s tests -v
    powershell -ExecutionPolicy Bypass -File .\build_windows.ps1

The build script generates dist/WORKSHOPDesktopV1/ and, only if Inno Setup ISCC.exe is installed, installer-output/WORKSHOPDesktopV1-Setup.exe. Git for Windows remains an external runtime dependency. Packaging alone is **not** clean-client installation qualification.

## Important security boundaries

The fixed Markdown writer is **not** a sandbox for arbitrary Python, shell, LLM or third-party code. No general-purpose autonomous coding agent is implemented. No OS network isolation is claimed. The audit hash chain detects accidental changes but is not cryptographic authenticity against a privileged attacker. Local user approval uses an HMAC key in Windows Credential Manager, not a server-backed identity. The remote PR API can partially succeed; the controller records a remote branch/partial error and does not silently retry or delete remote objects. A draft PR is not a merged, deployed or released change.

**NOT VERIFIED:** live GitHub PAT authentication and draft PR against a separate customer test account; clean Windows 10/11 client GUI interactions, Inno installer/uninstall and credential removal, production Windows Credential Manager interoperability, hostile concurrent NTFS races, security isolation for general-purpose worker code, and independent product acceptance.

## Recovery and uninstall

An interrupted local run is never automatically replayed. On next workspace open, the GUI can, after explicit confirmation, mark its task BLOCKED and retain staged evidence for manual review. The Inno uninstaller removes the local GitHub PAT and approval HMAC key from Windows Credential Manager; preserved workspaces remain on disk, but pending approvals become invalid after uninstall/reinstall. This is intentional fail-closed behavior.
