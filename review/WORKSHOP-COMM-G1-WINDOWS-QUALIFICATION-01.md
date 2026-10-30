# WORKSHOP-COMM-G1-QUALIFICATION-01 — Evidence review and bounded REWORK decision

DATE: 2026-10-30
ROLE: Control Room technical review of actual Worker/CI evidence (NOT final independent acceptance)
VERDICT: REWORK
SOURCE_FROZEN: windows@d5369ec0300fe836dc673dbe9e8f5ea1ccdb5c23
EVIDENCE: evidence/WORKSHOP-COMM-G1-WINDOWS-QUALIFICATION-01/WORKER.md
BASELINE_CI_PASS: https://github.com/nevincho/WORKSHOP/actions/runs/41135365108 (25 unit PASS + 6 Windows NTFS PASS; Tkinter process smoke PASS)
NEGATIVE_CI_FAIL: https://github.com/nevincho/WORKSHOP/actions/runs/41136200148 (fenced Markdown field classified as task_candidate, expected inert document)
CODE_SCOPE: apps/workshop_g1/workshop_g1/core.py document_kind() and parse_task(); add focused tests in apps/workshop_g1/tests/test_g1.py.
CLASSIFICATION: IMPLEMENTATION DEFECT / CONTRACT NEGATIVE FIXTURE. Original 31 PASS are genuine but insufficient to prove inert parsing for fenced Markdown. No Windows harness issue in this failure.
CONTRACT: planning/WORKSHOP_COMM_G1_READINESS_CONTRACT.md section C requires inert Markdown code samples and no interpretation of task-like content in untrusted documents as machine instruction.
SMALLEST_CORRECTION: deterministic, bounded skip of fenced Markdown code blocks for task-candidate detection and field parsing; support standard backtick and tilde fences, preserve existing canonical plain-text field parsing. Add explicit negative tests for documentation-only fenced TASK_ID, fenced duplicate TASK_ID in otherwise valid task, and tilde fence. No parser redesign, no executor/Git/G2.
PRE_CHANGE_CHECKPOINT: d5369ec0300fe836dc673dbe9e8f5ea1ccdb5c23 frozen G1 source. Implementation repair must record exact source commit and rollback method; keep main and other project paths untouched.
VALIDATION: rerun existing 25 unit and 6 Windows fixtures plus new contract negatives on GitHub-hosted Windows runner; record raw logs and source SHA-256. Reviewer must assess updated code/acceptance independently before any COMPLETE.
INDEPENDENCE_LIMIT: This is a negative evidence-based Control Room correction decision, NOT an independent final Reviewer PASS; no G1 promotion authorized.
STOP: return to bounded Worker correction, then fresh independent acceptance review.
