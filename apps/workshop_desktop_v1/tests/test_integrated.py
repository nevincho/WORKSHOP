"""Consolidated integration and negative/security tests; no live GitHub writes."""
import hashlib
import json
import os
import uuid
import subprocess
import tempfile
import unittest
from unittest import mock
from pathlib import Path

from workshop_desktop.engine import Controller, ControllerError, CoordinationRepo, canonical, digest
from workshop_desktop import gui, reviewer
from workshop_desktop.g1_adapter import create_workspace, inspect_workspace, trusted_bundle
from workshop_desktop.github_api import GitHubClient, GitHubError, PartialProposal, validate_target
from workshop_desktop.vault import MemoryVault, WindowsVault, SIGNING

SHA = "a" * 40


class FakeGitHub:
    def __init__(self):
        self.sha = SHA
        self.exists = False
        self.proposals = []

    def head(self, repo, ref):
        return self.sha

    def file_exists(self, repo, ref, path):
        return self.exists

    def propose(self, plan, content, approval_id):
        self.proposals.append((plan, content, approval_id))
        return {"branch": "workshop-proposal-" + approval_id[:20], "remote_created": True,
                "proposal_sha": "b" * 40, "pr_url": "https://github.com/example/demo/pull/1"}


class IntegratedTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='WORKSHOP_G1_WIN_TEST_')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "workspace"
        create_workspace(self.root, trusted_bundle())
        self.github = FakeGitHub()
        self.vault = MemoryVault()
        self.controller = Controller(self.root, github=self.github, vault=self.vault)
        self.controller.initialize()

    def make_plan(self):
        return self.controller.plan("TASK-01", "Demo", "example/demo", "main",
                                    "docs/workshop-demo.md", "# Verified demo\n")

    def approve_plan(self, identifier, controller=None):
        ctrl = controller or self.controller
        _, plan, _ = ctrl._plan(identifier)
        return ctrl.approve(identifier, expected_plan_hash=digest(canonical(plan)))

    def test_approval_requires_exact_displayed_plan_hash(self):
        identifier = self.make_plan()
        with self.assertRaises(TypeError):
            self.controller.approve(identifier)
        with self.assertRaisesRegex(ControllerError, "PLAN_CHANGED_REVIEW_AGAIN"):
            self.controller.approve(identifier, expected_plan_hash="0" * 64)
        self.assertIsNone(self.controller.status()["tasks"][identifier]["approval"])
        self.assertIsNone(self.vault.get(SIGNING))
        self.assertTrue(self.approve_plan(identifier))

    def test_approval_dialog_rejects_replan_during_display(self):
        identifier = self.make_plan()
        second = Controller(self.root, github=self.github, vault=self.vault)
        desktop = object.__new__(gui.Desktop)
        desktop.controller = self.controller
        desktop.selected = identifier
        desktop._log = mock.Mock()
        desktop.refresh = mock.Mock()
        desktop._error = mock.Mock()
        after_replan = {}

        def concurrent_replan(displayed_text):
            self.assertIn("# Verified demo", displayed_text)
            self.approve_plan(identifier, controller=second)
            run = second.run(identifier)
            self.assertIsNone(run["error"])

            def reject(role, arguments, cwd, timeout=20, cancel=None):
                Path(arguments[2]).write_text(json.dumps({
                    "verdict": "REWORK", "sha256": run["artifact_sha256"],
                    "reviewer_pid": -1}), encoding="utf-8")
                return 1, "", ""

            with mock.patch("workshop_desktop.engine._launch", side_effect=reject):
                self.assertEqual(second.review(identifier)["verdict"], "REWORK")
            second.rework(identifier, "# Changed while dialog open\n")
            after_replan["head"] = self.controller.store.head()
            after_replan["state"] = self.controller.status()
            return True

        desktop._approval_dialog = mock.Mock(side_effect=concurrent_replan)
        desktop.approve()
        desktop._error.assert_called_once()
        self.assertEqual(str(desktop._error.call_args.args[0]), "PLAN_CHANGED_REVIEW_AGAIN")
        self.assertEqual(self.controller.store.head(), after_replan["head"])
        self.assertEqual(self.controller.status(), after_replan["state"])
        self.assertIsNone(self.controller.status()["tasks"][identifier]["approval"])
        with self.assertRaisesRegex(ControllerError, "APPROVAL_REQUIRED"):
            self.controller.run(identifier)
        self.assertEqual(self.github.proposals, [])

        desktop._error.reset_mock()
        desktop._approval_dialog = mock.Mock(return_value=True)
        desktop.approve()
        desktop._error.assert_not_called()
        self.assertTrue(self.controller.status()["tasks"][identifier]["approval"])
        self.assertIn("# Changed while dialog open", desktop._approval_dialog.call_args.args[0])

    def test_full_g1_to_g7_candidate_draft_pr(self):
        rows, errors = inspect_workspace(self.root, trusted_bundle(), require_metadata=True)
        self.assertEqual((rows, errors), ([], []))
        identifier = self.make_plan()
        self.assertEqual(self.controller.status()["tasks"][identifier]["status"], "READY")
        approval = self.approve_plan(identifier)
        run = self.controller.run(identifier)
        self.assertEqual(run["worker_exit"], 0, run)
        self.assertIsNone(run["error"])
        review = self.controller.review(identifier)
        self.assertEqual(review["verdict"], "PASS", review)
        self.assertNotEqual(review["reviewer_pid"], review["worker_pid"])
        checkpoint = self.controller.publish(identifier)
        self.assertEqual(checkpoint["kind"], "DRAFT_PR_PENDING_INDEPENDENT_ACCEPTANCE")
        self.assertEqual(checkpoint["proposal"]["pr_url"], "https://github.com/example/demo/pull/1")
        self.assertEqual(self.controller.status()["tasks"][identifier]["status"], "REVIEW")
        self.assertTrue(self.controller.status()["tasks"][identifier]["draft_pr_submitted"])
        with self.assertRaisesRegex(ControllerError, "PROPOSAL_ALREADY_SUBMITTED"):
            self.controller.publish(identifier)
        self.assertEqual(len(self.github.proposals), 1)
        self.assertEqual(self.github.proposals[0][1], b"# Verified demo\n")
        self.assertEqual(self.github.proposals[0][2], approval)
        self.assertFalse((self.root / ".git").exists())
        self.assertFalse((self.root / "docs").exists())
        self.assertEqual(self.controller.store.head(), subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=self.controller.store.repo,
            capture_output=True, text=True, check=True).stdout.strip())

    def test_no_approval_no_run(self):
        identifier = self.make_plan()
        with self.assertRaisesRegex(ControllerError, "APPROVAL_REQUIRED"):
            self.controller.run(identifier)
        self.assertEqual(self.controller.status()["tasks"][identifier]["status"], "READY")

    def test_review_required_for_publish(self):
        identifier = self.make_plan()
        self.approve_plan(identifier)
        with self.assertRaisesRegex(ControllerError, "REVIEW_REQUIRED"):
            self.controller.publish(identifier)

    def test_head_change_invalidates_approval(self):
        identifier = self.make_plan()
        self.approve_plan(identifier)
        self.github.sha = "c" * 40
        with self.assertRaisesRegex(ControllerError, "TARGET_HEAD_CHANGED"):
            self.controller.run(identifier)
        self.assertEqual(self.controller.status()["tasks"][identifier]["status"], "READY")

    def test_remote_existing_path_refused(self):
        self.github.exists = True
        with self.assertRaisesRegex(ControllerError, "TARGET_FILE_ALREADY_EXISTS"):
            self.make_plan()

    def test_no_second_active_task(self):
        self.make_plan()
        with self.assertRaisesRegex(ControllerError, "ONLY_ONE_ACTIVE_TASK"):
            self.make_plan()

    def test_path_allowlist(self):
        for path in ("../escape.md", ".git/config", "tasks/run.py", "docs/../evil.md",
                     "docs/file.txt", "docs/CON.md", "docs/a\\b.md"):
            with self.subTest(path=path), self.assertRaises(GitHubError):
                validate_target("example/demo", "main", path)

    def test_approval_hmac_tamper(self):
        identifier = self.make_plan()
        approval_id = self.approve_plan(identifier)
        approval = self.controller.store.read("approvals/" + approval_id + ".json")
        approval["target_sha"] = "b" * 40
        path = self.controller.store.repo / "approvals" / (approval_id + ".json")
        path.write_text(json.dumps(approval), encoding="utf-8")
        subprocess.run(["git", "add", str(path)], cwd=self.controller.store.repo, check=True)
        subprocess.run(["git", "-c", "user.name=test", "-c", "user.email=test@example.invalid",
                        "commit", "-qm", "malicious alteration"], cwd=self.controller.store.repo, check=True)
        with self.assertRaisesRegex(ControllerError, "APPROVAL_TAMPERED"):
            self.controller.run(identifier)

    def test_missing_signing_secret_blocks_run(self):
        identifier = self.make_plan()
        self.approve_plan(identifier)
        self.vault.delete(SIGNING)
        with self.assertRaisesRegex(ControllerError, "APPROVAL_KEY_MISSING"):
            self.controller.run(identifier)

    def test_dirty_git_fails_closed(self):
        self.make_plan()
        (self.controller.store.repo / "state.json").write_text("{}", encoding="utf-8")
        with self.assertRaisesRegex(ControllerError, "DIRTY_COORDINATION"):
            self.controller.status()

    def test_interrupted_run_requires_recovery(self):
        identifier = self.make_plan()
        state = self.controller.status()
        state["tasks"][identifier]["status"] = "IN_PROGRESS"
        self.controller.store.transaction(state, {"kind": "INJECTED_INTERRUPTION", "id": identifier},
                                          expected_head=self.controller.store.head())
        with self.assertRaisesRegex(ControllerError, "INTERRUPTED_RUN_REQUIRES_REVIEW"):
            self.controller.status()
        recovered = self.controller.recover_interrupted()
        self.assertEqual(recovered, [identifier])
        self.assertEqual(self.controller.status()["tasks"][identifier]["status"], "BLOCKED")
        self.assertEqual(self.github.proposals, [])

    def test_staged_artifact_tamper_refused(self):
        identifier = self.make_plan()
        self.approve_plan(identifier)
        run = self.controller.run(identifier)
        output = self.controller.store.staging / run["id"] / "artifact.md"
        output.write_text("tampered", encoding="utf-8")
        with self.assertRaisesRegex(ControllerError, "STAGED_ARTIFACT_CHANGED"):
            self.controller.review(identifier)

    def test_no_automatic_remote_write(self):
        identifier = self.make_plan()
        self.approve_plan(identifier)
        self.controller.run(identifier)
        self.controller.review(identifier)
        self.assertEqual(self.github.proposals, [])
        self.assertEqual(self.controller.status()["tasks"][identifier]["status"], "REVIEW")

    def test_symlink_workspace_rejected(self):
        target = Path(self.tmp.name) / "other"
        target.mkdir()
        link = Path(self.tmp.name) / "linked"
        try:
            link.symlink_to(target, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("Symlink creation unavailable")
        with self.assertRaisesRegex(ControllerError, "UNSAFE_LINK"):
            CoordinationRepo(link)

    def test_two_controller_stale_snapshot_cannot_overwrite(self):
        second = Controller(self.root, github=self.github, vault=self.vault)
        stale_state, stale_head = second._snapshot()
        first = self.make_plan()
        with mock.patch.object(second, "_snapshot", return_value=(stale_state, stale_head)):
            with self.assertRaisesRegex(ControllerError, "COORDINATION_HEAD_CHANGED"):
                second.plan("TASK-02", "Demo", "example/demo", "main",
                            "docs/other.md", "# Stale\\n")
        self.assertEqual(list(self.controller.status()["tasks"]), [first])

    def test_transaction_requires_expected_head(self):
        state = self.controller.status()
        with self.assertRaisesRegex(TypeError, "expected_head"):
            self.controller.store.transaction(state, {"kind": "INVALID_NO_LEASE"})

    def test_rework_replan_requires_new_approval_and_completes_preflight(self):
        identifier = self.make_plan()
        self.approve_plan(identifier)
        run = self.controller.run(identifier)
        def reject(role, arguments, cwd, timeout=20, cancel=None):
            Path(arguments[2]).write_text(json.dumps({
                "verdict": "REWORK", "sha256": run["artifact_sha256"],
                "reviewer_pid": -1}), encoding="utf-8")
            return 1, "", ""
        with mock.patch("workshop_desktop.engine._launch", side_effect=reject):
            review = self.controller.review(identifier)
        self.assertEqual(review["verdict"], "REWORK")
        new_hash = self.controller.rework(identifier, "# Corrected\\n")
        self.assertNotEqual(new_hash, review["plan_hash"])
        with self.assertRaisesRegex(ControllerError, "APPROVAL_REQUIRED"):
            self.controller.run(identifier)
        self.approve_plan(identifier)
        retry = self.controller.run(identifier)
        self.assertIsNone(retry["error"])
        passed = self.controller.review(identifier)
        self.assertEqual(passed["verdict"], "PASS")
        self.assertEqual(self.controller.status()["tasks"][identifier]["status"], "REVIEW")

    def test_remote_intent_persisted_before_ambiguous_write(self):
        identifier = self.make_plan()
        self.approve_plan(identifier)
        self.controller.run(identifier)
        self.controller.review(identifier)
        def ambiguous(plan, data, approval):
            state = self.controller.store.state()
            self.assertEqual(state["tasks"][identifier]["status"], "PUBLISHING")
            self.assertEqual(state["tasks"][identifier]["remote_intent"]["base_sha"], SHA)
            raise PartialProposal({"branch": "workshop-proposal-" + approval[:20],
                                   "remote_created": "UNKNOWN"}, "TIMEOUT")
        with mock.patch.object(self.github, "propose", side_effect=ambiguous):
            with self.assertRaises(PartialProposal):
                self.controller.publish(identifier)
        task = self.controller.status()["tasks"][identifier]
        self.assertEqual(task["status"], "BLOCKED")
        self.assertIn("remote_uncertainty", task)
        with self.assertRaisesRegex(ControllerError, "REVIEW_REQUIRED"):
            self.controller.publish(identifier)

    def test_create_g1_never_initializes_git_coordination_implicitly(self):
        separate = Path(self.tmp.name) / "create_only"
        desktop = object.__new__(gui.Desktop)
        desktop.path_var = mock.Mock()
        desktop.refresh = mock.Mock()
        with mock.patch.object(gui, "Controller",
                side_effect=lambda p: Controller(p, github=self.github, vault=self.vault)):
            desktop._attach(separate, initialize=True)
        self.assertTrue((separate / "workspace.json").is_file())
        self.assertTrue((separate / "tasks").is_dir())
        self.assertFalse((separate / ".workshop_v1").exists(),
                         "G1 CREATE must not silently git init coordination")

    def test_open_g1_is_read_only_and_rejects_bad_metadata(self):
        separate = Path(self.tmp.name) / "open_only"
        create_workspace(separate, trusted_bundle())
        desktop = object.__new__(gui.Desktop)
        desktop.path_var = mock.Mock()
        desktop.refresh = mock.Mock()
        with mock.patch.object(gui, "Controller",
                side_effect=lambda p: Controller(p, github=self.github, vault=self.vault)):
            desktop._attach(separate)
            self.assertFalse((separate / ".workshop_v1").exists())
            (separate / "workspace.json").write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(ControllerError, "G1_WORKSPACE_METADATA_INVALID"):
                desktop._attach(separate)
            self.assertFalse((separate / ".workshop_v1").exists())

    def test_open_existing_interrupted_coordination_never_writes(self):
        identifier = self.make_plan()
        state = self.controller.status()
        state["tasks"][identifier]["status"] = "IN_PROGRESS"
        self.controller.store.transaction(state, {"kind": "SIMULATE_INTERRUPTION"},
                                          expected_head=self.controller.store.head())
        before = self.controller.store.head()
        desktop = object.__new__(gui.Desktop)
        desktop.path_var = mock.Mock()
        desktop.refresh = mock.Mock()
        with mock.patch.object(gui, "Controller", return_value=self.controller):
            desktop._attach(self.root)
        self.assertEqual(self.controller.store.head(), before)
        self.assertEqual(self.controller.store.state()["tasks"][identifier]["status"], "IN_PROGRESS")

    def test_approval_scope_full_payload_and_identity(self):
        identifier = self.make_plan()
        _, plan, _ = self.controller._plan(identifier)
        summary = gui.approval_scope(plan)
        self.assertTrue(summary.endswith(plan["content"]))
        self.assertIn(plan["target_sha"], summary)
        self.assertIn(hashlib.sha256(plan["content"].encode()).hexdigest(), summary)
        self.assertIn(plan["path"], summary)
        self.assertIn("Plan SHA-256", summary)

    def test_reviewer_refuses_existing_symlink_report(self):
        stage = Path(self.tmp.name) / "review_stage"
        stage.mkdir()
        plan = stage / "plan.json"
        output = stage / "artifact.md"
        victim = Path(self.tmp.name) / "victim.txt"
        victim.write_text("PROTECTED", encoding="utf-8")
        plan.write_text(json.dumps({"repo": "example/demo", "ref": "main",
                                    "path": "docs/a.md", "content": "# Demo",
                                    "executor": "markdown-writer-v1",
                                    "operation": "CREATE_MARKDOWN"}), encoding="utf-8")
        output.write_text("# Demo", encoding="utf-8")
        link = stage / "review.json"
        try:
            link.symlink_to(victim)
        except (OSError, NotImplementedError):
            self.skipTest("File symlink unavailable on this runner")
        with self.assertRaises((ValueError, FileExistsError, OSError)):
            reviewer.review(plan, output, link)
        self.assertEqual(victim.read_text(encoding="utf-8"), "PROTECTED")

    @unittest.skipUnless(os.name == "nt", "NTFS junction check")
    def test_reviewer_refuses_junction_stage(self):
        real = Path(self.tmp.name) / "real_stage"
        real.mkdir()
        junction = Path(self.tmp.name) / "junction_stage"
        created = subprocess.run(["cmd", "/c", "mklink", "/J", str(junction), str(real)],
                                 capture_output=True, text=True)
        self.assertEqual(created.returncode, 0, created.stderr)
        plan = real / "plan.json"
        plan.write_text(json.dumps({"repo": "example/demo", "ref": "main",
                                    "path": "docs/a.md", "content": "# Demo",
                                    "executor": "markdown-writer-v1",
                                    "operation": "CREATE_MARKDOWN"}), encoding="utf-8")
        (real / "artifact.md").write_text("# Demo", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "REVIEW_REPARSE_POINT"):
            reviewer.review(plan, junction / "artifact.md", junction / "review.json")

    def test_audit_chain_rejects_tampered_committed_event(self):
        self.make_plan()
        log = self.controller.store.repo / "events.jsonl"
        content = log.read_text(encoding="utf-8").replace("PLAN_CREATED", "PLAN_CHANGED")
        log.write_text(content, encoding="utf-8")
        subprocess.run(["git", "add", "events.jsonl"], cwd=self.controller.store.repo, check=True)
        subprocess.run(["git", "-c", "user.name=test", "-c", "user.email=test@example.invalid",
                        "commit", "-qm", "tamper"], cwd=self.controller.store.repo, check=True)
        with self.assertRaisesRegex(ControllerError, "AUDIT_CHAIN_MISMATCH|DIRTY_COORDINATION_REQUIRES_RECOVERY"):
            self.controller.status()


    def test_project_inventory_and_task_detail_are_read_only(self):
        identifier = self.make_plan()
        before = self.controller.store.head()
        self.assertEqual(self.controller.project_summary(), [
            {"project": "Demo", "tasks": 1, "active": 1}])
        detail = self.controller.task_detail(identifier)
        self.assertEqual(detail["id"], identifier)
        self.assertEqual(detail["status"], "READY")
        self.assertEqual(detail["plan"]["content"], "# Verified demo" + chr(10))
        self.assertEqual(detail["plan_sha256"], self.controller.status()["tasks"][identifier]["plan_hash"])
        self.assertFalse(detail["approval_recorded"])
        self.assertIsNone(detail["run"])
        self.assertIsNone(detail["review"])
        self.assertIsNone(detail["proposal"])
        self.assertEqual(self.controller.store.head(), before)

        self.approve_plan(identifier)
        run = self.controller.run(identifier)
        review = self.controller.review(identifier)
        proposal = self.controller.publish(identifier)
        before = self.controller.store.head()
        detail = self.controller.task_detail(identifier)
        self.assertEqual(detail["status"], "REVIEW")
        self.assertTrue(detail["approval_recorded"])
        self.assertEqual(detail["run"]["id"], run["id"])
        self.assertEqual(detail["review"]["id"], review["id"])
        self.assertEqual(detail["review"]["review_kind"],
                         "DETERMINISTIC_PREFLIGHT_NOT_INDEPENDENT_ACCEPTANCE")
        self.assertEqual(detail["proposal"]["pr_url"], proposal["proposal"]["pr_url"])
        self.assertEqual(self.controller.store.head(), before)
        self.assertEqual(len(self.github.proposals), 1)

    def test_task_detail_refuses_unknown_task_without_writes(self):
        before = self.controller.store.head()
        with self.assertRaisesRegex(ControllerError, "UNKNOWN_TASK"):
            self.controller.task_detail("0" * 32)
        self.assertEqual(self.controller.project_summary(), [])
        self.assertEqual(self.controller.store.head(), before)

    def test_task_detail_refuses_mismatched_run_evidence(self):
        identifier = self.make_plan()
        self.approve_plan(identifier)
        run = self.controller.run(identifier)
        path = self.controller.store.repo / "runs" / (run["id"] + ".json")
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["task"] = "0" * 32
        path.write_text(json.dumps(payload), encoding="utf-8")
        subprocess.run(["git", "add", str(path)], cwd=self.controller.store.repo, check=True)
        subprocess.run(["git", "-c", "user.name=test", "-c", "user.email=test@example.invalid",
                        "commit", "-qm", "tamper run evidence"], cwd=self.controller.store.repo, check=True)
        with self.assertRaisesRegex(ControllerError, "RUN_EVIDENCE_IDENTITY_MISMATCH"):
            self.controller.task_detail(identifier)

    def test_task_selection_updates_detail_without_executing(self):
        desktop = object.__new__(gui.Desktop)
        desktop.task_tree = mock.Mock()
        desktop.task_tree.selection.return_value = ("abc123",)
        desktop.show_task_detail = mock.Mock()
        desktop._select_task()
        self.assertEqual(desktop.selected, "abc123")
        desktop.show_task_detail.assert_called_once_with()


    def test_human_rejection_before_remote_proposal_requires_rework(self):
        identifier = self.make_plan()
        self.approve_plan(identifier)
        self.controller.run(identifier)
        self.controller.review(identifier)
        before = len(self.github.proposals)
        with self.assertRaisesRegex(ControllerError, "REJECTION_REASON_REQUIRED"):
            self.controller.reject_review(identifier, " ")
        with self.assertRaisesRegex(ControllerError, "INVALID_REJECTION_REASON"):
            self.controller.reject_review(identifier, chr(0) + "bad")
        result = self.controller.reject_review(identifier, "Scope rejected")
        self.assertFalse(result["remote_cleanup_required"])
        self.assertEqual(self.controller.status()["tasks"][identifier]["status"], "REWORK")
        self.assertEqual(len(self.github.proposals), before)
        with self.assertRaisesRegex(ControllerError, "REVIEW_STATE_REQUIRED"):
            self.controller.reject_review(identifier, "Again")
        with self.assertRaisesRegex(ControllerError, "REVIEW_REQUIRED"):
            self.controller.publish(identifier)

    def test_human_rejection_after_draft_pr_blocks_and_preserves_remote(self):
        identifier = self.make_plan()
        self.approve_plan(identifier)
        self.controller.run(identifier)
        self.controller.review(identifier)
        self.controller.publish(identifier)
        before = len(self.github.proposals)
        result = self.controller.reject_review(identifier, "Reject proposed change")
        self.assertTrue(result["remote_cleanup_required"])
        task = self.controller.status()["tasks"][identifier]
        self.assertEqual(task["status"], "BLOCKED")
        self.assertTrue(task["draft_pr_submitted"])
        self.assertEqual(len(self.github.proposals), before)
        with self.assertRaisesRegex(ControllerError, "REWORK_STATE_REQUIRED"):
            self.controller.rework(identifier, "# New")
        self.assertTrue(self.controller.task_detail(identifier)["proposal"]["pr_url"])


class GitHubAdapterTests(unittest.TestCase):
    def test_branch_post_timeout_after_server_creation_is_not_retried(self):
        calls = []
        def transport(method, route, payload, authorized):
            calls.append((method, route))
            if method == "GET" and "/branches/" in route:
                return {"commit": {"sha": SHA}}
            if method == "GET" and "/git/ref/heads/" in route:
                return {"object": {"sha": SHA}}
            if method == "GET" and "/git/ref/heads/" in route:
                return {"object": {"sha": SHA}}
            if method == "GET" and "/contents/" in route:
                raise GitHubError("GITHUB_HTTP_404")
            if method == "POST" and route.endswith("/git/refs"):
                raise GitHubError("GITHUB_NETWORK_UNAVAILABLE")
            raise AssertionError((method, route))
        client = GitHubClient(lambda: "token", transport=transport)
        plan = {"repo": "example/demo", "ref": "main", "path": "docs/demo.md",
                "target_sha": SHA, "task_id": "TASK-01"}
        with self.assertRaises(PartialProposal) as caught:
            client.propose(plan, b"# Demo", "d" * 32)
        self.assertTrue(caught.exception.partial["remote_created"])
        self.assertEqual(caught.exception.partial["observed_branch_sha"], SHA)
        self.assertFalse(any(method == "PUT" for method, _ in calls))

    def test_wrong_remote_branch_sha_refuses_write(self):
        calls = []
        def transport(method, route, payload, authorized):
            calls.append((method, route))
            if method == "GET" and "/branches/" in route:
                return {"commit": {"sha": SHA}}
            if method == "GET" and "/git/ref/heads/" in route:
                return {"object": {"sha": "b" * 40}}
            if method == "GET" and "/contents/" in route:
                raise GitHubError("GITHUB_HTTP_404")
            if method == "POST" and route.endswith("/git/refs"):
                return {}
            raise AssertionError((method, route))
        client = GitHubClient(lambda: "token", transport=transport)
        plan = {"repo": "example/demo", "ref": "main", "path": "docs/demo.md",
                "target_sha": SHA, "task_id": "TASK-01"}
        with self.assertRaises(PartialProposal) as caught:
            client.propose(plan, b"# Demo", "d" * 32)
        self.assertIn("PROPOSAL_BRANCH_SHA_MISMATCH", str(caught.exception))
        self.assertFalse(any(method == "PUT" for method, _ in calls))

    def test_read_only_default_and_approved_draft_pr(self):
        calls = []
        def transport(method, route, payload, authorized):
            calls.append((method, route, payload, authorized))
            if method == "GET" and "/branches/" in route:
                return {"commit": {"sha": SHA}}
            if method == "GET" and "/git/ref/heads/" in route:
                return {"object": {"sha": SHA}}
            if method == "GET" and "/contents/" in route:
                if "ref=workshop-proposal-" in route:
                    return {"encoding": "base64", "content": "IyBEZW1vCg=="}
                raise GitHubError("GITHUB_HTTP_404")
            if method == "POST" and route.endswith("/git/refs"):
                return {"ref": payload["ref"]}
            if method == "PUT":
                return {"commit": {"sha": "b" * 40}}
            if method == "POST" and route.endswith("/pulls"):
                return {"html_url": "https://github.com/example/demo/pull/3"}
            raise AssertionError((method, route))
        client = GitHubClient(lambda: "test-secret", transport=transport)
        plan = {"repo": "example/demo", "ref": "main", "path": "docs/example.md",
                "target_sha": SHA, "task_id": "TASK-01"}
        self.assertEqual(client.head("example/demo", "main"), SHA)
        self.assertFalse(calls[0][3])
        result = client.propose(plan, b"# Demo\n", "d" * 32)
        self.assertEqual(result["pr_url"], "https://github.com/example/demo/pull/3")
        self.assertEqual([c[0] for c in calls].count("PUT"), 1)
        self.assertTrue(all(c[3] for c in calls if c[0] in ("PUT", "POST")))
        self.assertTrue(any(c[1].endswith("/pulls") and c[2]["draft"] for c in calls))

    def test_remote_readback_mismatch_blocks_pr(self):
        calls = []
        def transport(method, route, payload, authorized):
            calls.append((method, route))
            if method == "GET" and "/branches/" in route:
                return {"commit": {"sha": SHA}}
            if method == "GET" and "/git/ref/heads/" in route:
                return {"object": {"sha": SHA}}
            if method == "GET" and "/contents/" in route:
                if "ref=workshop-proposal-" in route:
                    return {"encoding": "base64", "content": "dGFtcGVyZWQ="}
                raise GitHubError("GITHUB_HTTP_404")
            if method == "POST" and route.endswith("/git/refs"):
                return {}
            if method == "PUT":
                return {"commit": {"sha": "b" * 40}}
            raise AssertionError((method, route))
        client = GitHubClient(lambda: "token", transport=transport)
        plan = {"repo": "example/demo", "ref": "main", "path": "docs/demo.md",
                "target_sha": SHA, "task_id": "TASK-01"}
        with self.assertRaises(PartialProposal) as caught:
            client.propose(plan, b"# Demo", "d" * 32)
        self.assertIn("REMOTE_CONTENT_MISMATCH", str(caught.exception))
        self.assertFalse(any(route.endswith("/pulls") for _, route in calls))

    def test_remote_branch_partial_failure_is_explicit(self):
        def transport(method, route, payload, authorized):
            if method == "GET" and "/branches/" in route:
                return {"commit": {"sha": SHA}}
            if method == "GET" and "/git/ref/heads/" in route:
                return {"object": {"sha": SHA}}
            if method == "GET":
                raise GitHubError("GITHUB_HTTP_404")
            if method == "POST" and route.endswith("/git/refs"):
                return {}
            raise GitHubError("GITHUB_HTTP_403")
        client = GitHubClient(lambda: "token", transport=transport)
        plan = {"repo": "example/demo", "ref": "main", "path": "docs/demo.md",
                "target_sha": SHA, "task_id": "TASK-01"}
        with self.assertRaises(PartialProposal) as caught:
            client.propose(plan, b"# Demo", "d" * 32)
        self.assertTrue(caught.exception.partial["remote_created"])
        self.assertIsNone(caught.exception.partial["pr_url"])



class WindowsVaultTests(unittest.TestCase):
    @unittest.skipUnless(os.name == "nt", "Windows Credential Manager only")
    def test_real_credential_manager_roundtrip(self):
        vault = WindowsVault()
        name = "WORKSHOP_DESKTOP_V1_TEST_" + uuid.uuid4().hex
        try:
            self.assertIsNone(vault.get(name))
            vault.put(name, "temporary-test-value")
            self.assertEqual(vault.get(name), "temporary-test-value")
        finally:
            vault.delete(name)
        self.assertIsNone(vault.get(name))


if __name__ == "__main__":
    unittest.main()
