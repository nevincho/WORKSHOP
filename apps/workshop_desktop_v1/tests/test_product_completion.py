"""Desktop V1 product completion gates: no remote writes or paid services."""
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from workshop_desktop.engine import Controller, ControllerError, canonical, digest, _git
from workshop_desktop.g1_adapter import create_workspace, trusted_bundle
from workshop_desktop.github_api import GitHubClient, GitHubError
from workshop_desktop.vault import MemoryVault

BASE = "a" * 40
PROPOSED = "b" * 40


class ReviewFixture:
    def __init__(self):
        self.sha = BASE
        self.approved = True
        self.review_calls = 0
        self.remote_writes = 0

    def head(self, repo, ref):
        return self.sha

    def file_exists(self, repo, ref, path):
        return False

    def propose(self, plan, content, approval_id):
        self.remote_writes += 1
        return {"branch": "workshop-proposal-" + approval_id[:20],
                "proposal_sha": PROPOSED,
                "pr_url": "https://github.com/example/demo/pull/3"}

    def verified_independent_review(self, plan, proposal):
        self.review_calls += 1
        if not self.approved:
            raise GitHubError("INDEPENDENT_GITHUB_APPROVAL_REQUIRED")
        return {"provider": "GITHUB_AUTHENTICATED_PR_REVIEW",
                "reviewer": "external-reviewer", "author": "proposal-author",
                "review_id": 72, "reviewed_commit": PROPOSED,
                "submitted_at": "2026-10-31T12:00:00Z", "pr_url": proposal["pr_url"]}


class ProductCompletionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="workshop_product_")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "g1"
        create_workspace(self.root, trusted_bundle())
        self.github = ReviewFixture()
        self.ctrl = Controller(self.root, github=self.github, vault=MemoryVault())
        self.ctrl.initialize()

    def plan(self):
        return self.ctrl.plan("TASK-01", "Demo", "example/demo", "main",
                              "docs/demo.md", "# Demo\n")

    def ready_for_acceptance(self):
        identifier = self.plan()
        _, plan, _ = self.ctrl._plan(identifier)
        self.ctrl.approve(identifier, expected_plan_hash=digest(canonical(plan)))
        self.assertIsNone(self.ctrl.run(identifier)["error"])
        self.assertEqual(self.ctrl.review(identifier)["verdict"], "PASS")
        self.ctrl.publish(identifier)
        return identifier

    def test_complete_requires_remote_proposal_and_independent_review(self):
        identifier = self.plan()
        with self.assertRaisesRegex(ControllerError, "PUBLISHED_REVIEW_REQUIRED"):
            self.ctrl.accept_review(identifier)
        _, plan, _ = self.ctrl._plan(identifier)
        self.ctrl.approve(identifier, expected_plan_hash=digest(canonical(plan)))
        self.ctrl.run(identifier)
        self.ctrl.review(identifier)
        with self.assertRaisesRegex(ControllerError, "PUBLISHED_REVIEW_REQUIRED"):
            self.ctrl.accept_review(identifier)
        self.assertEqual(self.github.review_calls, 0)

    def test_no_independent_review_keeps_review_state_and_git_head(self):
        identifier = self.ready_for_acceptance()
        self.github.approved = False
        head = self.ctrl.store.head()
        with self.assertRaisesRegex(GitHubError, "INDEPENDENT_GITHUB_APPROVAL_REQUIRED"):
            self.ctrl.accept_review(identifier)
        self.assertEqual(self.ctrl.store.head(), head)
        self.assertEqual(self.ctrl.status()["tasks"][identifier]["status"], "REVIEW")
        self.assertFalse((self.ctrl.store.repo / "checkpoints" / (identifier + ".json")).exists())

    def test_complete_records_git_checkpoint_without_remote_merge(self):
        identifier = self.ready_for_acceptance()
        before = self.github.remote_writes
        _, plan, _ = self.ctrl._plan(identifier)
        proposal = self.ctrl.store.read("proposals/" + identifier + ".json")["proposal"]
        displayed = self.github.verified_independent_review(plan, proposal)
        checkpoint = self.ctrl.accept_review(
            identifier, expected_review_id=displayed["review_id"],
            expected_reviewed_commit=displayed["reviewed_commit"],
            expected_reviewer=displayed["reviewer"],
            expected_pr_url=displayed["pr_url"])
        self.assertEqual(checkpoint["kind"], "LOCAL_PROPOSAL_ACCEPTED_PR_UNMERGED")
        self.assertEqual(checkpoint["independent_review"]["reviewer"], "external-reviewer")
        self.assertEqual(checkpoint["proposal_sha"], PROPOSED)
        self.assertEqual(self.ctrl.status()["tasks"][identifier]["status"], "COMPLETE")
        self.assertEqual(self.ctrl.task_detail(identifier)["checkpoint"], checkpoint)
        self.assertEqual(self.github.remote_writes, before)
        self.assertEqual(self.ctrl.project_summary()[0]["active"], 0)
        with self.assertRaisesRegex(ControllerError, "PUBLISHED_REVIEW_REQUIRED"):
            self.ctrl.accept_review(identifier)
        self.assertEqual(self.github.remote_writes, 1)

    def test_bounded_worker_progress_callback_does_not_change_result(self):
        identifier = self.plan()
        _, plan, _ = self.ctrl._plan(identifier)
        self.ctrl.approve(identifier, expected_plan_hash=digest(canonical(plan)))
        events = []
        result = self.ctrl.run(identifier, progress=events.append)
        self.assertIsNone(result["error"])
        self.assertTrue(events)
        self.assertEqual(events[-1]["phase"], "EXITED")
        self.assertTrue(all(len(item["stdout"]) <= 32768 and
                            len(item["stderr"]) <= 32768 for item in events))

    def test_transaction_journal_rolls_back_partial_local_commit(self):
        real_git = _git
        def fail_commit(repo, *args, **kwargs):
            if args and args[0] == "commit":
                raise ControllerError("INJECTED_COMMIT_FAILURE")
            return real_git(repo, *args, **kwargs)
        with patch("workshop_desktop.engine._git", side_effect=fail_commit):
            with self.assertRaisesRegex(ControllerError, "INJECTED_COMMIT_FAILURE"):
                self.plan()
        self.assertTrue(self.ctrl.store.journal.is_file())
        with self.assertRaisesRegex(ControllerError, "TRANSACTION_JOURNAL_REQUIRES_RECOVERY"):
            self.ctrl.status()
        result = self.ctrl.recover_transaction()
        self.assertEqual(result["outcome"], "ROLLED_BACK")
        self.assertEqual(self.ctrl.status()["tasks"], {})
        self.assertFalse(self.ctrl.store.journal.exists())

    def test_transaction_journal_refuses_foreign_content(self):
        real_git = _git
        def fail_commit(repo, *args, **kwargs):
            if args and args[0] == "commit":
                raise ControllerError("INJECTED_COMMIT_FAILURE")
            return real_git(repo, *args, **kwargs)
        with patch("workshop_desktop.engine._git", side_effect=fail_commit):
            with self.assertRaises(ControllerError):
                self.plan()
        (self.ctrl.store.repo / "state.json").write_text('{"foreign":true}', encoding="utf-8")
        with self.assertRaisesRegex(ControllerError, "TRANSACTION_CONTENT_MISMATCH"):
            self.ctrl.recover_transaction()
        self.assertTrue(self.ctrl.store.journal.exists())

    def test_transaction_journal_recognizes_committed_git_head(self):
        journal = self.ctrl.store.journal
        real_unlink = Path.unlink
        def fail_cleanup(path, *args, **kwargs):
            if path == journal:
                raise OSError("INJECTED_JOURNAL_CLEANUP_FAILURE")
            return real_unlink(path, *args, **kwargs)
        with patch.object(Path, "unlink", fail_cleanup):
            with self.assertRaisesRegex(OSError, "INJECTED_JOURNAL_CLEANUP_FAILURE"):
                self.plan()
        self.assertTrue(journal.is_file())
        result = self.ctrl.recover_transaction()
        self.assertEqual(result["outcome"], "COMMITTED")
        self.assertEqual(len(self.ctrl.status()["tasks"]), 1)
        self.assertFalse(journal.exists())

    def test_malformed_worker_metadata_is_durable_blocked_not_stranded(self):
        for payload in ("{broken", "[]"):
            with self.subTest(payload=payload):
                # Each subtest needs a fresh workspace and coordination Git.
                with tempfile.TemporaryDirectory(prefix="workshop_bad_worker_") as temp:
                    root = Path(temp) / "g1"
                    create_workspace(root, trusted_bundle())
                    ctrl = Controller(root, github=ReviewFixture(), vault=MemoryVault())
                    ctrl.initialize()
                    identifier = ctrl.plan("TASK-01", "Demo", "example/demo", "main",
                                           "docs/demo.md", "# Demo\\n")
                    _, plan, _ = ctrl._plan(identifier)
                    ctrl.approve(identifier, expected_plan_hash=digest(canonical(plan)))
                    def corrupt_worker(role, arguments, cwd, **kwargs):
                        self.assertEqual(role, "worker")
                        (Path(cwd) / "worker_result.json").write_text(payload, encoding="utf-8")
                        (Path(cwd) / "artifact.md").write_text("# Demo\\n", encoding="utf-8")
                        return 0, "", ""
                    with patch("workshop_desktop.engine._launch", side_effect=corrupt_worker):
                        result = ctrl.run(identifier)
                    expected = "WORKER_OUTPUT_INVALID" if payload == "{broken" else "WORKER_METADATA_INVALID"
                    self.assertEqual(result["error"], expected)
                    self.assertEqual(ctrl.status()["tasks"][identifier]["status"], "BLOCKED")
                    self.assertEqual(ctrl.store.read("runs/" + result["id"] + ".json")["error"],
                                     expected)

    def test_worker_launch_oserror_is_durable_blocked(self):
        identifier = self.plan()
        _, plan, _ = self.ctrl._plan(identifier)
        self.ctrl.approve(identifier, expected_plan_hash=digest(canonical(plan)))
        with patch("workshop_desktop.engine._launch", side_effect=OSError("cannot launch")):
            result = self.ctrl.run(identifier)
        self.assertEqual(result["error"], "WORKER_OUTPUT_INVALID")
        self.assertEqual(self.ctrl.status()["tasks"][identifier]["status"], "BLOCKED")

    def test_reviewer_crash_is_durable_rework_not_stranded_review(self):
        identifier = self.plan()
        _, plan, _ = self.ctrl._plan(identifier)
        self.ctrl.approve(identifier, expected_plan_hash=digest(canonical(plan)))
        self.assertIsNone(self.ctrl.run(identifier)["error"])
        with patch("workshop_desktop.engine._launch",
                   side_effect=ControllerError("EXECUTOR_CANCELLED_OR_TIMED_OUT")):
            report = self.ctrl.review(identifier)
        self.assertEqual(report["verdict"], "REWORK")
        self.assertEqual(report["reason"], "REVIEWER_EXECUTION_FAILED")
        self.assertEqual(self.ctrl.status()["tasks"][identifier]["status"], "REWORK")
        self.assertEqual(self.ctrl.store.read("reviews/" + report["id"] + ".json")["verdict"], "REWORK")

    def test_reviewer_missing_report_is_rework_and_can_replan(self):
        identifier = self.plan()
        _, plan, _ = self.ctrl._plan(identifier)
        self.ctrl.approve(identifier, expected_plan_hash=digest(canonical(plan)))
        self.assertIsNone(self.ctrl.run(identifier)["error"])
        with patch("workshop_desktop.engine._launch", return_value=(0, "", "")):
            report = self.ctrl.review(identifier)
        self.assertEqual(report["reason"], "REVIEWER_EXECUTION_FAILED")
        self.assertEqual(self.ctrl.status()["tasks"][identifier]["status"], "REWORK")
        new_hash = self.ctrl.rework(identifier)
        self.assertEqual(self.ctrl.status()["tasks"][identifier]["status"], "READY")
        self.assertEqual(self.ctrl.status()["tasks"][identifier]["plan_hash"], new_hash)
        self.assertIsNone(self.ctrl.status()["tasks"][identifier]["approval"])

    def test_reviewer_malformed_report_is_durable_rework(self):
        identifier = self.plan()
        _, plan, _ = self.ctrl._plan(identifier)
        self.ctrl.approve(identifier, expected_plan_hash=digest(canonical(plan)))
        self.assertIsNone(self.ctrl.run(identifier)["error"])
        def corrupt(role, arguments, cwd, **kwargs):
            Path(arguments[-1]).write_text("{not-json", encoding="utf-8")
            return 0, "", ""
        with patch("workshop_desktop.engine._launch", side_effect=corrupt):
            report = self.ctrl.review(identifier)
        self.assertEqual(report["verdict"], "REWORK")
        self.assertEqual(report["reason"], "REVIEWER_EXECUTION_FAILED")
        self.assertEqual(self.ctrl.status()["tasks"][identifier]["status"], "REWORK")

    def test_human_acceptance_refuses_changed_displayed_review(self):
        identifier = self.ready_for_acceptance()
        head = self.ctrl.store.head()
        with self.assertRaisesRegex(ControllerError, "DISPLAYED_REVIEW_CHANGED"):
            self.ctrl.accept_review(identifier, expected_review_id=999,
                                    expected_reviewed_commit=PROPOSED,
                                    expected_reviewer="external-reviewer",
                                    expected_pr_url="https://github.com/example/demo/pull/3")
        self.assertEqual(self.ctrl.store.head(), head)
        self.assertEqual(self.ctrl.status()["tasks"][identifier]["status"], "REVIEW")

    def test_programmatic_acceptance_cannot_skip_displayed_receipt(self):
        identifier = self.ready_for_acceptance()
        with self.assertRaisesRegex(ControllerError, "DISPLAYED_REVIEW_RECEIPT_REQUIRED"):
            self.ctrl.accept_review(identifier)
        self.assertEqual(self.ctrl.status()["tasks"][identifier]["status"], "REVIEW")

    def test_safe_settings_are_git_backed_and_bounded(self):
        original = self.ctrl.settings()
        self.assertEqual(original["max_cost"], 0)
        self.assertEqual(original["executor"], "markdown-writer-v1")
        with self.assertRaisesRegex(ControllerError, "INVALID_TIMEOUT"):
            self.ctrl.update_settings(worker_timeout_seconds=21)
        with self.assertRaisesRegex(ControllerError, "INVALID_TIMEOUT"):
            self.ctrl.update_settings(worker_timeout_seconds=True)
        self.assertEqual(self.ctrl.update_settings(worker_timeout_seconds=10)["worker_timeout_seconds"], 10)
        self.assertEqual(self.ctrl.settings()["worker_timeout_seconds"], 10)
        self.assertEqual(self.ctrl.status()["tasks"], {})
        self.assertEqual(self.ctrl.executor_capabilities()[0]["arbitrary_commands"], False)

    def test_timeout_is_immutable_plan_scope_and_settings_cannot_drift(self):
        self.ctrl.update_settings(worker_timeout_seconds=10)
        identifier = self.plan()
        _, plan, _ = self.ctrl._plan(identifier)
        self.assertEqual(plan["timeout_seconds"], 10)
        with self.assertRaisesRegex(ControllerError, "SETTINGS_CHANGE_WITH_ACTIVE_TASK"):
            self.ctrl.update_settings(worker_timeout_seconds=20)
        self.assertEqual(self.ctrl.settings()["worker_timeout_seconds"], 10)
        self.assertEqual(self.ctrl.store.read("plans/" + identifier + ".json")["timeout_seconds"], 10)

    def test_g1_discovery_is_read_only_and_never_grants_execution(self):
        head = self.ctrl.store.head()
        inventory = self.ctrl.discover_g1_tasks()
        self.assertEqual(inventory["authority"], "G1_READ_ONLY_DISCOVERY_NOT_EXECUTION")
        self.assertEqual(inventory["tasks"], [])
        self.assertEqual(inventory["diagnostics"], [])
        self.assertEqual(self.ctrl.store.head(), head)

    def test_task_eligibility_is_read_only(self):
        identifier = self.plan()
        head = self.ctrl.store.head()
        report = self.ctrl.evaluate_task(identifier)
        self.assertIn("HUMAN_PLAN_APPROVAL_REQUIRED", report["reasons"])
        self.assertFalse(report["eligible_for_run"])
        self.assertEqual(self.ctrl.store.head(), head)
        _, plan, _ = self.ctrl._plan(identifier)
        self.ctrl.approve(identifier, expected_plan_hash=digest(canonical(plan)))
        head = self.ctrl.store.head()
        self.assertTrue(self.ctrl.evaluate_task(identifier)["eligible_for_run"])
        self.assertEqual(self.ctrl.store.head(), head)


class WindowsDesktopScreenTests(unittest.TestCase):
    @unittest.skipUnless(os.name == "nt", "Windows GUI qualification only")
    def test_first_launch_all_product_screens_without_implicit_writes(self):
        import tkinter as tk
        from workshop_desktop.gui import Desktop
        root = tk.Tk()
        root.withdraw()
        try:
            app = Desktop(root)
            names = [app.tabs.tab(i, "text") for i in range(app.tabs.index("end"))]
            self.assertEqual(names, ["Welcome", "Tasks", "Projects", "Detail",
                                     "Approvals", "Plan", "Run", "Review", "Recovery",
                                     "GitHub", "Evidence", "Settings"])
            self.assertIsNone(app.controller)
            self.assertFalse(app.busy)
        finally:
            root.destroy()


class WindowsWizardFlowTests(unittest.TestCase):
    @unittest.skipUnless(os.name == "nt", "Windows Tkinter wizard qualification only")
    def test_first_run_wizard_requires_real_workspace_and_coordination(self):
        import tkinter as tk
        from workshop_desktop.gui import Desktop
        with tempfile.TemporaryDirectory(prefix="workshop_wizard_") as tmp:
            path = Path(tmp) / "g1"
            create_workspace(path, trusted_bundle())
            root = tk.Tk()
            root.withdraw()
            try:
                app = Desktop(root)
                self.assertEqual(app.wizard_step, 0)
                app._attach(path)
                app.advance_wizard()
                self.assertEqual(app.wizard_step, 1)
                app.controller.initialize()
                app.advance_wizard()
                self.assertEqual(app.wizard_step, 2)
                app.advance_wizard()
                self.assertEqual(app.wizard_step, 3)
                app.advance_wizard()
                self.assertEqual(app.wizard_step, 4)
                self.assertIn("Wizard complete", app.wizard_status_var.get())
            finally:
                root.destroy()


class GitHubIndependentReviewTests(unittest.TestCase):
    def fixture(self, reviews, *, author="author", head_sha=PROPOSED):
        calls = []
        def transport(method, route, payload, authorized):
            calls.append((method, route, authorized))
            if route.endswith("/pulls/3"):
                return {"state": "open", "merged_at": None, "user": {"login": author},
                        "head": {"sha": head_sha, "ref": "proposal",
                                 "repo": {"full_name": "example/demo"}},
                        "base": {"ref": "main"}}
            if "/reviews?" in route:
                return reviews
            if "/branches/" in route:
                return {"commit": {"sha": BASE}}
            if "/contents/" in route:
                import base64
                return {"encoding": "base64", "content": base64.b64encode(b"# Demo\n").decode("ascii")}
            raise AssertionError(route)
        client = GitHubClient(lambda: "fake-token", transport=transport)
        plan = {"repo": "example/demo", "ref": "main", "path": "docs/demo.md",
                "content": "# Demo\n", "target_sha": BASE}
        proposal = {"pr_url": "https://github.com/example/demo/pull/3",
                    "proposal_sha": PROPOSED, "branch": "proposal"}
        return client, plan, proposal, calls

    def approval(self, *, login="reviewer", state="APPROVED", commit=PROPOSED, id=12):
        return {"id": id, "user": {"login": login}, "state": state,
                "commit_id": commit, "submitted_at": "2026-10-31T12:00:00Z"}

    def test_distinct_github_authenticated_approval(self):
        client, plan, proposal, calls = self.fixture([self.approval()])
        receipt = client.verified_independent_review(plan, proposal)
        self.assertEqual(receipt["reviewer"], "reviewer")
        self.assertEqual(receipt["reviewed_commit"], PROPOSED)
        self.assertTrue(all(method == "GET" for method, _, _ in calls))

    def test_self_review_and_stale_commit_refused(self):
        for review in [self.approval(login="author"), self.approval(commit=BASE)]:
            with self.subTest(review=review):
                client, plan, proposal, _ = self.fixture([review])
                with self.assertRaisesRegex(GitHubError, "INDEPENDENT_GITHUB_APPROVAL_REQUIRED"):
                    client.verified_independent_review(plan, proposal)

    def test_latest_changes_requested_revokes_prior_approval(self):
        client, plan, proposal, _ = self.fixture([
            self.approval(id=10), self.approval(state="CHANGES_REQUESTED", id=11)])
        with self.assertRaisesRegex(GitHubError, "UNRESOLVED_CHANGES_REQUESTED"):
            client.verified_independent_review(plan, proposal)

    def test_conflicting_reviewers_fail_closed(self):
        client, plan, proposal, _ = self.fixture([
            self.approval(login="reviewer-a", state="APPROVED", id=21),
            self.approval(login="reviewer-b", state="CHANGES_REQUESTED", id=22)])
        with self.assertRaisesRegex(GitHubError, "UNRESOLVED_CHANGES_REQUESTED"):
            client.verified_independent_review(plan, proposal)

    def test_conflicting_review_resolved_by_same_reviewer_approval(self):
        client, plan, proposal, _ = self.fixture([
            self.approval(login="reviewer-a", state="APPROVED", id=21),
            self.approval(login="reviewer-b", state="CHANGES_REQUESTED", id=22),
            self.approval(login="reviewer-b", state="APPROVED", id=23)])
        receipt = client.verified_independent_review(plan, proposal)
        self.assertEqual(receipt["reviewed_commit"], PROPOSED)

    def test_review_history_order_cannot_hide_newer_veto(self):
        client, plan, proposal, _ = self.fixture([
            self.approval(login="reviewer-a", state="CHANGES_REQUESTED", id=42),
            self.approval(login="reviewer-b", state="APPROVED", id=41),
            self.approval(login="reviewer-a", state="APPROVED", id=40)])
        with self.assertRaisesRegex(GitHubError, "UNRESOLVED_CHANGES_REQUESTED"):
            client.verified_independent_review(plan, proposal)

    def test_remote_commit_change_refused(self):
        client, plan, proposal, _ = self.fixture([self.approval()], head_sha="c" * 40)
        with self.assertRaisesRegex(GitHubError, "PROPOSAL_REMOTE_IDENTITY_CHANGED"):
            client.verified_independent_review(plan, proposal)


if __name__ == "__main__":
    unittest.main()
