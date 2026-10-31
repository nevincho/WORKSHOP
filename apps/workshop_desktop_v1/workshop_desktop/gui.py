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
            "\nUTF-8 bytes: " + str(len(content.encode("utf-8"))) +
            "\nContent SHA-256: " + digest(content.encode("utf-8")) +
            "\nPlan SHA-256: " + digest(canonical(plan)) +
            "\n\nFULL PROPOSED MARKDOWN (NOT TRUNCATED):\n" + content)


class Desktop:
    def __init__(self, root):
        self.root = root
        self.root.title("WORKSHOP Desktop V1 — Integrated Candidate")
        self.root.geometry("1060x720")
        self.controller = None
        self.selected = None
        self.cancel_event = threading.Event()
        self.busy = False
        self.path_var = tk.StringVar(value="No workspace selected")
        self.status_var = tk.StringVar(value="Local-first. No paid AI or automatic repository writes.")
        self.repo_var = tk.StringVar(value="")
        self.ref_var = tk.StringVar(value="main")
        self.task_var = tk.StringVar(value="TASK-DEMO-01")
        self.project_var = tk.StringVar(value="Customer project")
        self.file_var = tk.StringVar(value="docs/workshop-demo.md")
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
        self.board = ttk.Frame(self.tabs, padding=12)
        self.projects_page = ttk.Frame(self.tabs, padding=12)
        self.detail_page = ttk.Frame(self.tabs, padding=12)
        self.plan_page = ttk.Frame(self.tabs, padding=12)
        self.run_page = ttk.Frame(self.tabs, padding=12)
        self.github_page = ttk.Frame(self.tabs, padding=12)
        self.audit_page = ttk.Frame(self.tabs, padding=12)
        for name, page in [("G1 / Task Board", self.board), ("Projects", self.projects_page),
                           ("Task Detail & Scope", self.detail_page), ("G2 / Plan & Approval", self.plan_page),
                           ("G3–G4 / Run & Review", self.run_page), ("G5 / GitHub", self.github_page),
                           ("G6–G7 / Evidence & Build", self.audit_page)]:
            self.tabs.add(page, text=name)
        ttk.Label(self.board, text="G1 trusted read-only workspace browser", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        self.g1_tree = ttk.Treeview(self.board, columns=("id", "status", "project"), show="headings", height=8)
        for col in ("id", "status", "project"):
            self.g1_tree.heading(col, text=col.upper())
        self.g1_tree.pack(fill="both", expand=True, pady=6)
        ttk.Label(self.board, text="G2 coordination tasks (Git-backed)").pack(anchor="w")
        self.task_tree = ttk.Treeview(self.board, columns=("task", "status", "identifier"), show="headings", height=6)
        for col in ("task", "status", "identifier"):
            self.task_tree.heading(col, text=col.upper())
        self.task_tree.pack(fill="both", expand=True)
        self.task_tree.bind("<<TreeviewSelect>>", self._select_task)
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
        self.task_detail_text = tk.Text(self.detail_page, wrap="word", state="disabled")
        self.task_detail_text.pack(fill="both", expand=True, pady=8)
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
        self.runlog = tk.Text(self.run_page, wrap="word", state="disabled")
        self.runlog.pack(fill="both", expand=True, pady=12)
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
        self.selected = None
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
                self.g1_tree.insert("", "end", values=(safe_display(fields["TASK_ID"]), safe_display(fields["STATUS"]), safe_display(fields["PROJECT"])))
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
            if self.selected in state["tasks"]:
                self.show_task_detail()
            self.diagnostics.delete("1.0", "end")
            self.diagnostics.insert("end", "\n".join(str(e) for e in errors) or "No G1 diagnostics")
            self.status_var.set("Coordination Git HEAD " + ctrl.store.head()[:12] if ctrl.store.repo.exists()
                                else "G1 OPEN: read-only. Initialize coordination explicitly to enable tasks.")
        except Exception as exc:
            self._error(exc)

    def _select_task(self, event=None):
        selection = self.task_tree.selection()
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
            def action():
                run = ctrl.run(identifier, cancel=self.cancel_event)
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
