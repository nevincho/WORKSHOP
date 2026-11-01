"""Tkinter integrated candidate UI; no hidden scheduling, API charges, or agent dispatch."""
import json
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk

from .engine import Controller, ControllerError, canonical, digest
from .g1_adapter import create_workspace, inspect_workspace, trusted_bundle, verified_trust, safe_display


def approval_scope(plan):
    """Exact, untruncated immutable payload for the scrollable human approval dialog."""
    content = plan["content"]
    return ("Task: " + plan["task_id"] + "\nProject: " + plan["project"] +
            "\nRepository: " + plan["repo"] + "\nBase ref: " + plan["ref"] +
            "\nImmutable base SHA: " + plan["target_sha"] +
            "\nOperation: " + plan["operation"] + "\nNew file: " + plan["path"] +
            "\nExecutor: " + plan["executor"] +
            "\nMaximum cost: " + str(plan["max_cost"]) +
            "\nWorker timeout seconds: " + str(plan.get("timeout_seconds", 20)) +
            "\nUTF-8 bytes: " + str(len(content.encode("utf-8"))) +
            "\nContent SHA-256: " + digest(content.encode("utf-8")) +
            "\nPlan SHA-256: " + digest(canonical(plan)) +
            "\n\nFULL PROPOSED MARKDOWN (NOT TRUNCATED):\n" + content)


class Desktop:
    def __init__(self, root):
        self.root = root
        self.root.title("WORKSHOP Desktop V1 — Integrated Candidate")
        self.root.geometry("1200x760")
        self.controller = None
        self.selected = None
        self.g1_selected = None
        self.cancel_event = threading.Event()
        self.busy = False
        self.path_var = tk.StringVar(value="No workspace selected")
        self.status_var = tk.StringVar(value="Local-first. No paid AI or automatic repository writes.")
        self.wizard_step = 0
        self.wizard_status_var = tk.StringVar(value="Step 1/4: CREATE or OPEN a trusted workspace.")
        self.repo_var = tk.StringVar(value="")
        self.ref_var = tk.StringVar(value="main")
        self.task_var = tk.StringVar(value="TASK-DEMO-01")
        self.project_var = tk.StringVar(value="Customer project")
        self.file_var = tk.StringVar(value="docs/workshop-demo.md")
        self.timeout_var = tk.StringVar(value="20")
        self._build()
        try:
            trust = verified_trust(trusted_bundle())
            self.trust_var.set("G1 trusted schemas: " + trust["commit"] + " | " +
                               " ".join(k + ":" + v["sha256"] for k, v in trust["files"].items()))
        except Exception as exc:
            self.trust_var.set("G1 trust unavailable: " + type(exc).__name__)

    def _build(self):
        bar = ttk.Frame(self.root, padding=8)
        bar.pack(fill="x")
        ttk.Button(bar, text="CREATE G1 WORKSPACE", command=self.create_workspace).pack(side="left", padx=4)
        ttk.Button(bar, text="OPEN WORKSPACE", command=self.open_workspace).pack(side="left", padx=4)
        ttk.Button(bar, text="INITIALIZE COORDINATION", command=self.initialize_coordination).pack(side="left", padx=4)
        ttk.Button(bar, text="RECOVER INTERRUPTED", command=self.recover_coordination).pack(side="left", padx=4)
        ttk.Button(bar, text="REFRESH", command=self.refresh).pack(side="left", padx=4)
        ttk.Label(bar, textvariable=self.path_var).pack(side="left", padx=10)
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True, padx=8, pady=5)
        self.welcome_page = ttk.Frame(self.tabs, padding=12)
        self.board = ttk.Frame(self.tabs, padding=12)
        self.projects_page = ttk.Frame(self.tabs, padding=12)
        self.detail_page = ttk.Frame(self.tabs, padding=12)
        self.approval_page = ttk.Frame(self.tabs, padding=12)
        self.plan_page = ttk.Frame(self.tabs, padding=12)
        self.run_page = ttk.Frame(self.tabs, padding=12)
        self.review_page = ttk.Frame(self.tabs, padding=12)
        self.checkpoint_page = ttk.Frame(self.tabs, padding=12)
        self.github_page = ttk.Frame(self.tabs, padding=12)
        self.audit_page = ttk.Frame(self.tabs, padding=12)
        self.settings_page = ttk.Frame(self.tabs, padding=12)
        for name, page in [("Welcome", self.welcome_page), ("Tasks", self.board),
                           ("Projects", self.projects_page), ("Detail", self.detail_page),
                           ("Approvals", self.approval_page), ("Plan", self.plan_page),
                           ("Run", self.run_page), ("Review", self.review_page),
                           ("Recovery", self.checkpoint_page), ("GitHub", self.github_page),
                           ("Evidence", self.audit_page), ("Settings", self.settings_page)]:
            self.tabs.add(page, text=name)
        ttk.Label(self.welcome_page, text="WORKSHOP Desktop V1 — guided first launch",
                  font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=10)
        ttk.Label(self.welcome_page, textvariable=self.wizard_status_var,
                  wraplength=850).pack(anchor="w", pady=8)
        ttk.Button(self.welcome_page, text="VERIFY STEP / CONTINUE WIZARD",
                   command=self.advance_wizard).pack(anchor="w", pady=6)
        ttk.Label(self.welcome_page, text="1. CREATE a trusted G1 workspace, or OPEN an existing one. "
                  "OPEN never repairs or writes to the workspace.", wraplength=860).pack(anchor="w", pady=8)
        ttk.Button(self.welcome_page, text="1A. CREATE WORKSPACE",
                   command=self.create_workspace).pack(anchor="w", pady=3)
        ttk.Button(self.welcome_page, text="1B. OPEN EXISTING",
                   command=self.open_workspace).pack(anchor="w", pady=3)
        ttk.Label(self.welcome_page, text="2. Review G1 trust diagnostics, then explicitly initialize "
                  "the separate local coordination Git. This is never automatic.",
                  wraplength=860).pack(anchor="w", pady=8)
        ttk.Button(self.welcome_page, text="2. INITIALIZE COORDINATION",
                   command=self.initialize_coordination).pack(anchor="w", pady=3)
        ttk.Label(self.welcome_page, text="3. Configure the safe executor and scoped GitHub access. "
                  "No paid AI, arbitrary commands, or background execution.",
                  wraplength=860).pack(anchor="w", pady=8)
        ttk.Button(self.welcome_page, text="3A. SAFE SETTINGS",
                   command=lambda: self.tabs.select(self.settings_page)).pack(anchor="w", pady=3)
        ttk.Button(self.welcome_page, text="3B. GITHUB CONNECTIONS",
                   command=lambda: self.tabs.select(self.github_page)).pack(anchor="w", pady=3)
        ttk.Label(self.welcome_page, text="4. Create a bounded Markdown proposal, approve the exact "
                  "plan, run preflight, submit a draft PR, obtain a distinct GitHub reviewer approval, "
                  "then explicitly accept the local proposal. COMPLETE never means merged/deployed.",
                  wraplength=860).pack(anchor="w", pady=8)
        ttk.Button(self.welcome_page, text="4. OPEN TASK PLANNER",
                   command=lambda: self.tabs.select(self.plan_page)).pack(anchor="w", pady=4)
        ttk.Label(self.board, text="G1 trusted read-only workspace browser", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        self.g1_tree = ttk.Treeview(self.board, columns=("id", "status", "project"), show="headings", height=8)
        for col in ("id", "status", "project"):
            self.g1_tree.heading(col, text=col.upper())
        self.g1_tree.pack(fill="both", expand=True, pady=6)
        self.g1_tree.bind("<<TreeviewSelect>>", self._select_g1_task)
        ttk.Button(self.board, text="INSPECT G1 TASK PREREQUISITES (READ ONLY)",
                   command=self.show_g1_task).pack(anchor="w", pady=3)
        ttk.Label(self.board, text="G2 coordination tasks (Git-backed)").pack(anchor="w")
        self.task_tree = ttk.Treeview(self.board, columns=("task", "status", "identifier"), show="headings", height=6)
        for col in ("task", "status", "identifier"):
            self.task_tree.heading(col, text=col.upper())
        self.task_tree.pack(fill="both", expand=True)
        self.task_tree.bind("<<TreeviewSelect>>", self._select_task)
        ttk.Button(self.board, text="CHECK SELECTED TASK ELIGIBILITY (READ ONLY)",
                   command=self.check_eligibility).pack(anchor="w", pady=4)
        ttk.Button(self.board, text="VIEW SELECTED TASK SCOPE & EVIDENCE",
                   command=self.open_task_detail).pack(anchor="w", pady=4)
        ttk.Label(self.projects_page, text="Verified local project inventory (read-only)",
                  font=("Segoe UI", 11, "bold")).pack(anchor="w")
        self.project_tree = ttk.Treeview(self.projects_page, columns=("project", "tasks", "active"),
                                         show="headings", height=15)
        for col in ("project", "tasks", "active"):
            self.project_tree.heading(col, text=col.upper())
        self.project_tree.pack(fill="both", expand=True, pady=8)
        ttk.Label(self.detail_page, text="Immutable task scope, execution and review evidence (read-only)",
                  font=("Segoe UI", 11, "bold")).pack(anchor="w")
        detail_frame = ttk.Frame(self.detail_page)
        detail_frame.pack(fill="both", expand=True, pady=8)
        detail_scroll = ttk.Scrollbar(detail_frame)
        detail_scroll.pack(side="right", fill="y")
        self.task_detail_text = tk.Text(detail_frame, wrap="word", state="disabled",
                                        yscrollcommand=detail_scroll.set)
        self.task_detail_text.pack(side="left", fill="both", expand=True)
        detail_scroll.config(command=self.task_detail_text.yview)
        ttk.Label(self.approval_page, text="Pending human approvals — no automatic execution",
                  font=("Segoe UI", 11, "bold")).pack(anchor="w")
        self.approval_tree = ttk.Treeview(self.approval_page,
                                         columns=("task", "project", "plan_hash"),
                                         show="headings", height=12)
        for col in ("task", "project", "plan_hash"):
            self.approval_tree.heading(col, text=col.upper())
        self.approval_tree.pack(fill="both", expand=True, pady=8)
        self.approval_tree.bind("<<TreeviewSelect>>", self._select_approval)
        ttk.Button(self.approval_page, text="REVIEW EXACT PLAN & APPROVE",
                   command=self.approve).pack(anchor="w", pady=6)
        self.diagnostics = tk.Text(self.board, height=4, wrap="word")
        self.diagnostics.pack(fill="x", pady=5)
        form = ttk.Frame(self.plan_page)
        form.pack(fill="x")
        for i, (label, variable) in enumerate([
            ("Task ID", self.task_var), ("Project", self.project_var), ("GitHub owner/repo", self.repo_var),
            ("Base branch", self.ref_var), ("New Markdown path (docs/ only)", self.file_var)
        ]):
            ttk.Label(form, text=label).grid(row=i, column=0, sticky="w", pady=3)
            ttk.Entry(form, textvariable=variable, width=75).grid(row=i, column=1, sticky="ew", padx=10, pady=3)
        form.columnconfigure(1, weight=1)
        ttk.Label(self.plan_page, text="Proposed Markdown content (inert data; never executed)").pack(anchor="w", pady=(12, 3))
        self.content = tk.Text(self.plan_page, height=13, wrap="word")
        self.content.pack(fill="both", expand=True)
        actions = ttk.Frame(self.plan_page)
        actions.pack(fill="x", pady=9)
        ttk.Button(actions, text="1. CREATE IMMUTABLE PLAN", command=self.create_plan).pack(side="left", padx=4)
        ttk.Button(actions, text="2. REVIEW & APPROVE", command=self.approve).pack(side="left", padx=4)
        ttk.Label(self.run_page, text="Worker is a fixed Markdown writer, not an arbitrary code sandbox.",
                  wraplength=850).pack(anchor="w", pady=12)
        runbar = ttk.Frame(self.run_page)
        runbar.pack(fill="x")
        ttk.Button(runbar, text="3. RUN & DETERMINISTIC PREFLIGHT", command=self.run_and_review).pack(side="left", padx=4)
        ttk.Button(runbar, text="REWORK: RESET PLAN / REAPPROVE", command=self.rework).pack(side="left", padx=4)
        ttk.Button(runbar, text="REJECT REVIEW", command=self.reject_review).pack(side="left", padx=4)
        ttk.Button(runbar, text="CANCEL RUN", command=self.cancel_run).pack(side="left", padx=4)
        ttk.Button(runbar, text="4. SUBMIT DRAFT PR (NOT ACCEPTANCE)", command=self.publish).pack(side="left", padx=4)
        acceptbar = ttk.Frame(self.run_page)
        acceptbar.pack(fill="x", pady=8)
        ttk.Button(acceptbar, text="5. ACCEPT INDEPENDENTLY REVIEWED PR (LOCAL COMPLETE)",
                   command=self.accept_review).pack(side="left", padx=4)
        ttk.Label(acceptbar, text="Requires distinct GitHub reviewer approval on exact PR commit; never merges.",
                  wraplength=450).pack(side="left", padx=10)
        self.runlog = tk.Text(self.run_page, wrap="word", state="disabled")
        self.runlog.pack(fill="both", expand=True, pady=12)
        ttk.Label(self.review_page, text="Independent GitHub review and explicit local human acceptance",
                  font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=8)
        ttk.Label(self.review_page, text="Deterministic subprocess preflight is not independent acceptance. "
                  "A distinct GitHub account must APPROVE the exact proposal commit. "
                  "COMPLETE records a local checkpoint; the draft PR remains unmerged.",
                  wraplength=900).pack(anchor="w", pady=8)
        ttk.Button(self.review_page, text="INSPECT SELECTED TASK / REVIEW EVIDENCE",
                   command=self.open_task_detail).pack(anchor="w", pady=5)
        ttk.Button(self.review_page, text="ACCEPT EXTERNALLY REVIEWED PROPOSAL",
                   command=self.accept_review).pack(anchor="w", pady=5)
        ttk.Button(self.review_page, text="REJECT SELECTED REVIEW",
                   command=self.reject_review).pack(anchor="w", pady=5)
        ttk.Label(self.checkpoint_page, text="Git-backed accepted checkpoints and explicit recovery",
                  font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=8)
        self.checkpoint_tree = ttk.Treeview(self.checkpoint_page,
                   columns=("task", "checkpoint", "status"), show="headings", height=10)
        for col in ("task", "checkpoint", "status"):
            self.checkpoint_tree.heading(col, text=col.upper())
        self.checkpoint_tree.pack(fill="both", expand=True, pady=6)
        self.checkpoint_tree.bind("<<TreeviewSelect>>", self._select_checkpoint)
        ttk.Button(self.checkpoint_page, text="VIEW SELECTED CHECKPOINT",
                   command=self.show_checkpoint).pack(anchor="w", pady=5)
        ttk.Button(self.checkpoint_page, text="RECOVER INTERRUPTED LOCAL GIT TRANSACTION",
                   command=self.recover_transaction).pack(anchor="w", pady=5)
        ttk.Button(self.checkpoint_page, text="EXPLICIT INTERRUPTED-RUN RECOVERY",
                   command=self.recover_coordination).pack(anchor="w", pady=5)
        ttk.Label(self.checkpoint_page, text="No automatic remote rollback: close a draft PR and "
                  "delete its isolated branch manually if recovery requires it.",
                  wraplength=900).pack(anchor="w", pady=8)
        ttk.Label(self.github_page, text="GitHub access: public read-only by default. Scoped PAT stays in Windows Credential Manager.",
                  wraplength=900).pack(anchor="w", pady=12)
        ghbar = ttk.Frame(self.github_page)
        ghbar.pack(fill="x")
        ttk.Button(ghbar, text="STORE SCOPED PAT", command=self.store_token).pack(side="left", padx=4)
        ttk.Button(ghbar, text="REVOKE LOCAL PAT", command=self.revoke_token).pack(side="left", padx=4)
        ttk.Button(ghbar, text="CHECK SELECTED BRANCH HEAD", command=self.check_head).pack(side="left", padx=4)
        ttk.Label(self.github_page, text="No direct base-branch writes. Approved changes create an isolated branch and draft PR. "
                  "Revocation here removes the locally stored token; revoke remotely in GitHub settings too.",
                  wraplength=900).pack(anchor="w", pady=20)
        ttk.Label(self.audit_page, text="Immutable Git coordination history; SHA chain is not cryptographic authenticity.",
                  wraplength=900).pack(anchor="w")
        ttk.Button(self.audit_page, text="REFRESH EVIDENCE", command=self.show_evidence).pack(anchor="w", pady=6)
        self.evidence = tk.Text(self.audit_page, wrap="word")
        self.evidence.pack(fill="both", expand=True)
        ttk.Label(self.settings_page, text="Safe local settings — no provider credentials in Git",
                  font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=10)
        ttk.Label(self.settings_page, text="Executor: markdown-writer-v1 only | CREATE_MARKDOWN | "
                  "docs/*.md | zero paid API cost | no arbitrary commands.",
                  wraplength=900).pack(anchor="w", pady=8)
        ttk.Label(self.settings_page, text="Independent review: GitHub-authenticated approval by "
                  "a different account on the exact draft PR commit. Local preflight alone cannot COMPLETE.",
                  wraplength=900).pack(anchor="w", pady=8)
        timeout_row = ttk.Frame(self.settings_page)
        timeout_row.pack(anchor="w", pady=8)
        ttk.Label(timeout_row, text="Worker timeout (seconds):").pack(side="left", padx=4)
        ttk.Combobox(timeout_row, textvariable=self.timeout_var, values=("5", "10", "15", "20"),
                     width=7, state="readonly").pack(side="left", padx=4)
        ttk.Button(timeout_row, text="SAVE VERIFIED SETTINGS",
                   command=self.save_settings).pack(side="left", padx=8)
        ttk.Label(self.settings_page, text="Checkpoint / recovery: COMPLETE records a Git-backed "
                  "immutable local acceptance reference. No remote PR merge, close, or rollback is automatic. "
                  "Interrupted runs must be explicitly marked BLOCKED.",
                  wraplength=900).pack(anchor="w", pady=15)
        ttk.Button(self.settings_page, text="VIEW SELECTED CHECKPOINT / RECOVERY",
                   command=self.show_checkpoint).pack(anchor="w", pady=4)
        self.trust_var = tk.StringVar(value="Checking G1 trust…")
        ttk.Label(self.root, textvariable=self.trust_var, padding=(8, 4), wraplength=1000).pack(fill="x")
        ttk.Label(self.root, textvariable=self.status_var, padding=8).pack(fill="x")

    def _log(self, message):
        self.runlog.configure(state="normal")
        self.runlog.insert("end", message + "\n")
        self.runlog.see("end")
        self.runlog.configure(state="disabled")
        self.status_var.set(message[:180])

    def _error(self, exc):
        messagebox.showerror("WORKSHOP", str(exc), parent=self.root)
        self.status_var.set(type(exc).__name__ + ": " + str(exc))

    def advance_wizard(self):
        """Guided, explicitly gated navigation; no implicit filesystem or remote writes."""
        try:
            ctrl = self._require()
            if self.wizard_step == 0:
                self.wizard_step = 1
                self.wizard_status_var.set("Step 2/4: Initialize local coordination Git explicitly.")
            elif self.wizard_step == 1:
                if not ctrl.store.repo.is_dir():
                    raise ControllerError("INITIALIZE_COORDINATION_FIRST")
                ctrl.status()
                self.wizard_step = 2
                self.wizard_status_var.set("Step 3/4: Verify bounded executor settings.")
                self.tabs.select(self.settings_page)
            elif self.wizard_step == 2:
                settings = ctrl.settings()
                if settings["executor"] != "markdown-writer-v1" or settings["max_cost"] != 0:
                    raise ControllerError("UNSUPPORTED_WIZARD_EXECUTOR")
                self.wizard_step = 3
                self.wizard_status_var.set("Step 4/4: Optional scoped GitHub PAT; offline planning remains available.")
                self.tabs.select(self.github_page)
            elif self.wizard_step == 3:
                self.wizard_step = 4
                self.wizard_status_var.set("Wizard complete: create and explicitly approve a bounded task. "
                                           "GitHub connection is required only before remote operations.")
                self.tabs.select(self.plan_page)
            else:
                self.tabs.select(self.plan_page)
        except Exception as exc:
            self._error(exc)

    def _require(self):
        if self.controller is None:
            raise ControllerError("OPEN_WORKSPACE_FIRST")
        return self.controller

    def _attach(self, path, initialize=False):
        if initialize:
            create_workspace(path, trusted_bundle())
        # G1 OPEN must be strictly read-only, including malformed/untrusted paths.
        tasks, errors = inspect_workspace(path, trusted_bundle(), require_metadata=True)
        if any(item[0] == "workspace.json" for item in errors):
            raise ControllerError("G1_WORKSPACE_METADATA_INVALID")
        ctrl = Controller(path)
        # G1 CREATE writes only its previewed bootstrap.  Git coordination
        # requires the separate, explicitly confirmed INITIALIZE action.
        # OPEN never repairs or initializes coordination; recovery is a separate action.
        self.controller = ctrl
        self.wizard_step = 0
        self.wizard_status_var.set("Step 1/4: Workspace opened. Verify and continue.")
        self.selected = None
        self.g1_selected = None
        self.path_var.set(str(path))
        self.refresh()

    def initialize_coordination(self):
        try:
            ctrl = self._require()
            if ctrl.store.repo.exists() or ctrl.store.home.exists():
                raise ControllerError("COORDINATION_ALREADY_EXISTS")
            _, errors = inspect_workspace(ctrl.store.workspace, trusted_bundle(), require_metadata=True)
            if errors:
                raise ControllerError("G1_DIAGNOSTICS_REQUIRE_REVIEW")
            if not messagebox.askyesno("Explicit coordination initialization",
                    "CREATE local .workshop_v1 coordination Git in this verified G1 workspace? "
                    "OPEN itself performs no writes.", parent=self.root):
                return
            ctrl.initialize()
            self.refresh()
        except Exception as exc:
            self._error(exc)

    def recover_transaction(self):
        try:
            ctrl = self._require()
            if not ctrl.store.journal.is_file():
                raise ControllerError("NO_TRANSACTION_JOURNAL")
            if not messagebox.askyesno("Recover local Git transaction",
                    "Inspect and reconcile the recorded local Git transaction? "
                    "Only known journal files may be rolled back, and only if their "
                    "content and Git HEAD still match. No remote actions are retried.",
                    parent=self.root):
                return
            outcome = ctrl.recover_transaction()
            self._log("Local Git transaction: " + json.dumps(outcome, sort_keys=True))
            self.refresh()
        except Exception as exc:
            self._error(exc)

    def recover_coordination(self):
        try:
            ctrl = self._require()
            try:
                ctrl.status()
                raise ControllerError("NO_INTERRUPTED_COORDINATION")
            except ControllerError as exc:
                if str(exc) not in ("INTERRUPTED_RUN_REQUIRES_REVIEW",
                                    "REMOTE_INTENT_REQUIRES_RECONCILIATION"):
                    raise
                if not messagebox.askyesno("Explicit recovery",
                        "Mark interrupted operations BLOCKED for manual review? "
                        "No remote retry or external writes will occur.", parent=self.root):
                    return
                if str(exc) == "INTERRUPTED_RUN_REQUIRES_REVIEW":
                    ctrl.recover_interrupted()
                else:
                    ctrl.recover_remote_intent()
                self.refresh()
        except Exception as exc:
            self._error(exc)

    def create_workspace(self):
        parent = filedialog.askdirectory(title="Choose parent directory")
        if not parent:
            return
        name = simpledialog.askstring("Workspace", "New empty directory name:", parent=self.root)
        if not name:
            return
        if name in (".", "..") or "/" in name or "\\" in name:
            self._error(ControllerError("INVALID_DIRECTORY_NAME"))
            return
        path = Path(parent) / name
        if not messagebox.askyesno("Create", "Create new G1 workspace at:\n" + str(path), parent=self.root):
            return
        try:
            self._attach(path, initialize=True)
        except Exception as exc:
            self._error(exc)

    def open_workspace(self):
        path = filedialog.askdirectory(title="Open existing G1 workspace")
        if path:
            try:
                self._attach(Path(path))
            except Exception as exc:
                self._error(exc)

    def refresh(self):
        if not self.controller:
            return
        try:
            ctrl = self._require()
            tasks, errors = inspect_workspace(ctrl.store.workspace, trusted_bundle(), require_metadata=True)
            for item in self.g1_tree.get_children():
                self.g1_tree.delete(item)
            for filename, fields in tasks:
                self.g1_tree.insert("", "end", iid=filename,
                                    values=(safe_display(fields["TASK_ID"]), safe_display(fields["STATUS"]), safe_display(fields["PROJECT"])))
            for item in self.task_tree.get_children():
                self.task_tree.delete(item)
            state = ctrl.status() if ctrl.store.repo.exists() else {"tasks": {}}
            for identifier, entry in state["tasks"].items():
                self.task_tree.insert("", "end", iid=identifier,
                                      values=(entry["task_id"], entry["status"], identifier))
            for item in self.project_tree.get_children():
                self.project_tree.delete(item)
            if ctrl.store.repo.exists():
                for row in ctrl.project_summary():
                    self.project_tree.insert("", "end",
                                             values=(row["project"], row["tasks"], row["active"]))
            for item in self.approval_tree.get_children():
                self.approval_tree.delete(item)
            for item in self.checkpoint_tree.get_children():
                self.checkpoint_tree.delete(item)
            for identifier, entry in state["tasks"].items():
                if entry["status"] == "COMPLETE" and entry.get("checkpoint"):
                    self.checkpoint_tree.insert("", "end", iid=identifier,
                                                values=(entry["task_id"], entry["checkpoint"],
                                                        entry["status"]))
            for identifier, entry in state["tasks"].items():
                if entry["status"] == "READY" and not entry.get("approval"):
                    detail = ctrl.task_detail(identifier)
                    self.approval_tree.insert("", "end", iid=identifier,
                                              values=(entry["task_id"], detail["plan"]["project"],
                                                      detail["plan_sha256"]))
            if self.selected in state["tasks"]:
                self.show_task_detail()
            if ctrl.store.repo.exists():
                self.timeout_var.set(str(ctrl.settings()["worker_timeout_seconds"]))
            self.diagnostics.delete("1.0", "end")
            self.diagnostics.insert("end", "\n".join(str(e) for e in errors) or "No G1 diagnostics")
            self.status_var.set("Coordination Git HEAD " + ctrl.store.head()[:12] if ctrl.store.repo.exists()
                                else "G1 OPEN: read-only. Initialize coordination explicitly to enable tasks.")
        except Exception as exc:
            self._error(exc)

    def _select_g1_task(self, event=None):
        selection = self.g1_tree.selection()
        if selection:
            self.g1_selected = selection[0]

    def show_g1_task(self):
        try:
            ctrl = self._require()
            if not self.g1_selected:
                raise ControllerError("SELECT_G1_TASK_FIRST")
            inventory = ctrl.discover_g1_tasks()
            entry = next((row for row in inventory["tasks"]
                          if row["filename"] == self.g1_selected), None)
            if entry is None:
                raise ControllerError("G1_TASK_NO_LONGER_PRESENT")
            self.task_detail_text.configure(state="normal")
            self.task_detail_text.delete("1.0", "end")
            self.task_detail_text.insert("end", json.dumps(entry, indent=2, sort_keys=True,
                                                             ensure_ascii=False))
            self.task_detail_text.configure(state="disabled")
            self.tabs.select(self.detail_page)
        except Exception as exc:
            self._error(exc)

    def _select_task(self, event=None):
        selection = self.task_tree.selection()
        if selection:
            self.selected = selection[0]
            self.show_task_detail()

    def _select_checkpoint(self, event=None):
        selection = self.checkpoint_tree.selection()
        if selection:
            self.selected = selection[0]
            self.show_task_detail()

    def _select_approval(self, event=None):
        selection = self.approval_tree.selection()
        if selection:
            self.selected = selection[0]
            self.show_task_detail()

    def show_task_detail(self):
        try:
            ctrl = self._require()
            if not self.selected:
                raise ControllerError("SELECT_TASK_FIRST")
            detail = ctrl.task_detail(self.selected)
            self.task_detail_text.configure(state="normal")
            self.task_detail_text.delete("1.0", "end")
            self.task_detail_text.insert("end", json.dumps(detail, indent=2, sort_keys=True,
                                                             ensure_ascii=False))
            self.task_detail_text.configure(state="disabled")
        except Exception as exc:
            self._error(exc)

    def open_task_detail(self):
        if not self.selected:
            self._error(ControllerError("SELECT_TASK_FIRST"))
            return
        self.show_task_detail()
        self.tabs.select(self.detail_page)

    def check_eligibility(self):
        try:
            ctrl = self._require()
            if not self.selected:
                raise ControllerError("SELECT_TASK_FIRST")
            result = ctrl.evaluate_task(self.selected)
            self._log(json.dumps(result, sort_keys=True))
        except Exception as exc:
            self._error(exc)

    def save_settings(self):
        try:
            ctrl = self._require()
            timeout = int(self.timeout_var.get())
            if not messagebox.askyesno("Save safe settings",
                    "Persist timeout " + str(timeout) + " seconds to local Git coordination? "
                    "Executor, cost, protection and review policy cannot be weakened.",
                    parent=self.root):
                return
            result = ctrl.update_settings(worker_timeout_seconds=timeout)
            self._log("Settings saved: " + json.dumps(result, sort_keys=True))
            self.refresh()
        except Exception as exc:
            self._error(exc)

    def show_checkpoint(self):
        try:
            ctrl = self._require()
            if not self.selected:
                raise ControllerError("SELECT_TASK_FIRST")
            detail = ctrl.task_detail(self.selected)
            if not detail.get("checkpoint"):
                raise ControllerError("NO_ACCEPTED_CHECKPOINT")
            self.tabs.select(self.detail_page)
            self.show_task_detail()
        except Exception as exc:
            self._error(exc)

    def create_plan(self):
        try:
            ctrl = self._require()
            identifier = ctrl.plan(self.task_var.get(), self.project_var.get(),
                                   self.repo_var.get().strip(), self.ref_var.get().strip(),
                                   self.file_var.get().strip(), self.content.get("1.0", "end-1c"))
            self.selected = identifier
            self.refresh()
            self._log("Plan created: " + identifier)
        except Exception as exc:
            self._error(exc)

    def _approval_dialog(self, summary):
        dialog = tk.Toplevel(self.root)
        dialog.title("Inspect EXACT immutable plan before approval")
        dialog.geometry("860x620")
        dialog.transient(self.root)
        dialog.grab_set()
        frame = ttk.Frame(dialog, padding=12)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="Review the entire content, SHA-256 and target identity. "
                  "Approval is valid for one immutable plan only.", wraplength=820).pack(anchor="w")
        body = ttk.Frame(frame)
        body.pack(fill="both", expand=True, pady=8)
        scrollbar = ttk.Scrollbar(body)
        scrollbar.pack(side="right", fill="y")
        text = tk.Text(body, wrap="word", yscrollcommand=scrollbar.set)
        text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=text.yview)
        text.insert("1.0", summary)
        text.configure(state="disabled")
        result = {"approved": False}
        def finish(value):
            result["approved"] = value
            dialog.destroy()
        buttons = ttk.Frame(frame)
        buttons.pack(fill="x")
        ttk.Button(buttons, text="CANCEL", command=lambda: finish(False)).pack(side="left")
        ttk.Button(buttons, text="APPROVE EXACT PLAN", command=lambda: finish(True)).pack(side="right")
        dialog.protocol("WM_DELETE_WINDOW", lambda: finish(False))
        self.root.wait_window(dialog)
        return result["approved"]

    def approve(self):
        try:
            ctrl = self._require()
            if not self.selected:
                raise ControllerError("SELECT_TASK_FIRST")
            identifier = self.selected
            _, plan, _ = ctrl._plan(identifier)
            displayed_plan_hash = digest(canonical(plan))
            if self._approval_dialog(approval_scope(plan)):
                self._log("Approval stored: " + ctrl.approve(
                    identifier, expected_plan_hash=displayed_plan_hash))
                self.refresh()
        except Exception as exc:
            self._error(exc)

    def _background(self, action):
        if self.busy:
            self._error(ControllerError("OPERATION_IN_PROGRESS"))
            return
        self.busy = True
        def work():
            try:
                result = action()
                self.root.after(0, lambda: self._log(json.dumps(result, sort_keys=True, default=str)[:3000]))
            except Exception as exc:
                self.root.after(0, lambda e=exc: self._error(e))
            finally:
                self.root.after(0, self._finish_background)
        threading.Thread(target=work, daemon=True).start()

    def _finish_background(self):
        self.busy = False
        self.refresh()

    def run_and_review(self):
        try:
            ctrl = self._require()
            if not self.selected:
                raise ControllerError("SELECT_TASK_FIRST")
            identifier = self.selected
            self.cancel_event.clear()
            def on_progress(event):
                def display():
                    label = "Worker " + event["phase"] + " (" + str(event["elapsed_seconds"]) + "s)"
                    self._log(label)
                    for key in ("stdout", "stderr"):
                        if event.get(key):
                            self._log(key.upper() + ": " + event[key][:1200])
                self.root.after(0, display)
            def action():
                run = ctrl.run(identifier, cancel=self.cancel_event, progress=on_progress)
                if run["error"]:
                    return run
                review = ctrl.review(identifier)
                return {"run": run["id"], "review": review}
            self._background(action)
        except Exception as exc:
            self._error(exc)

    def rework(self):
        try:
            ctrl = self._require()
            if not self.selected:
                raise ControllerError("SELECT_TASK_FIRST")
            _, plan, _ = ctrl._plan(self.selected)
            if not messagebox.askyesno("Explicit REWORK",
                    "Discard the previous approval, replan the selected REWORK task with the "
                    "current Markdown editor content, and require fresh approval?", parent=self.root):
                return
            content = self.content.get("1.0", "end-1c")
            self._log("REWORK plan SHA-256: " + ctrl.rework(self.selected, content))
            self.refresh()
        except Exception as exc:
            self._error(exc)

    def reject_review(self):
        try:
            ctrl = self._require()
            if not self.selected:
                raise ControllerError("SELECT_TASK_FIRST")
            detail = ctrl.task_detail(self.selected)
            if detail["status"] != "REVIEW" or not detail["review"]:
                raise ControllerError("REVIEW_STATE_REQUIRED")
            remote = detail["proposal"] is not None
            reason = simpledialog.askstring(
                "Reject review", "Reason for rejection (required, maximum 500 characters):",
                parent=self.root)
            if reason is None:
                return
            warning = ("A remote draft PR already exists. It will NOT be closed or deleted; "
                       "manual GitHub cleanup is required. Task becomes BLOCKED."
                       if remote else "Task will become REWORK and require a new plan and approval.")
            if not messagebox.askyesno("Confirm human rejection", warning, parent=self.root):
                return
            result = ctrl.reject_review(self.selected, reason)
            self._log("Human review rejected: " + json.dumps(result, sort_keys=True))
            self.refresh()
        except Exception as exc:
            self._error(exc)

    def cancel_run(self):
        self.cancel_event.set()
        self.status_var.set("Cancellation requested; active subprocess will be terminated.")

    def publish(self):
        try:
            ctrl = self._require()
            if not self.selected:
                raise ControllerError("SELECT_TASK_FIRST")
            _, plan, _ = ctrl._plan(self.selected)
            if not messagebox.askyesno("External GitHub write",
                    "Submit reviewed file as a NEW DRAFT PR (never merge automatically)?\n\n" +
                    plan["repo"] + "\n" + plan["path"] + "\nBase " + plan["target_sha"], parent=self.root):
                return
            identifier = self.selected
            self._background(lambda: ctrl.publish(identifier))
        except Exception as exc:
            self._error(exc)

    def accept_review(self):
        try:
            ctrl = self._require()
            if not self.selected:
                raise ControllerError("SELECT_TASK_FIRST")
            identifier = self.selected
            detail = ctrl.task_detail(identifier)
            if detail["status"] != "REVIEW" or not detail["proposal"]:
                raise ControllerError("PUBLISHED_REVIEW_REQUIRED")
            _, plan, _ = ctrl._plan(identifier)
            proposal = ctrl.store.read("proposals/" + identifier + ".json")["proposal"]
            receipt = ctrl.github.verified_independent_review(plan, proposal)
            summary = ("GitHub-authenticated independent review\\nReviewer: " +
                       receipt["reviewer"] + "\\nPR author: " + receipt["author"] +
                       "\\nReviewed commit: " + receipt["reviewed_commit"] +
                       "\\nPR: " + receipt["pr_url"] +
                       "\\n\\nAccept this LOCAL proposal as COMPLETE? "
                       "The draft PR will NOT be merged or deployed.")
            if not messagebox.askyesno("Human acceptance of reviewed proposal",
                                       summary, parent=self.root):
                return
            checkpoint = ctrl.accept_review(
                identifier, expected_review_id=receipt["review_id"],
                expected_reviewed_commit=receipt["reviewed_commit"])
            self._log("Accepted local proposal checkpoint: " + checkpoint["id"])
            self.refresh()
        except Exception as exc:
            self._error(exc)

    def store_token(self):
        try:
            ctrl = self._require()
            token = simpledialog.askstring("GitHub", "Fine-grained GitHub PAT (not saved in files):",
                                           show="*", parent=self.root)
            if token:
                ctrl.set_github_token(token)
                self.status_var.set("Credential stored in Windows Credential Manager.")
        except Exception as exc:
            self._error(exc)

    def revoke_token(self):
        try:
            self._require().revoke_github()
            self.status_var.set("Local GitHub credential removed; revoke token remotely as well.")
        except Exception as exc:
            self._error(exc)

    def check_head(self):
        try:
            ctrl = self._require()
            self.status_var.set("GitHub HEAD: " + ctrl.github.head(self.repo_var.get(), self.ref_var.get()))
        except Exception as exc:
            self._error(exc)

    def show_evidence(self):
        try:
            ctrl = self._require()
            state = ctrl.status()
            files = [str(path.relative_to(ctrl.store.repo)) for path in ctrl.store.repo.rglob("*.json")
                     if ".git" not in path.parts]
            summary = {"head": ctrl.store.head(), "tasks": state["tasks"], "artifacts": sorted(files),
                       "note": "Reviewer is deterministic separate process, not independent human security acceptance."}
            self.evidence.delete("1.0", "end")
            self.evidence.insert("end", json.dumps(summary, indent=2, sort_keys=True))
        except Exception as exc:
            self._error(exc)


def main():
    root = tk.Tk()
    Desktop(root)
    root.mainloop()
