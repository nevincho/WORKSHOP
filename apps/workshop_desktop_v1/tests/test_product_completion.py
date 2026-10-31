"""Desktop V1 product completion gates: no remote writes or paid services."""
import json
import os
import tempfile
import unittest
from pathlib import Path

from workshop_desktop.engine import Controller, ControllerError, canonical, digest
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
        checkpoint = self.ctrl.accept_review(identifier)
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
        with self.assertRaisesRegex(GitHubError, "INDEPENDENT_GITHUB_APPROVAL_REQUIRED"):
            client.verified_independent_review(plan, proposal)

    def test_remote_commit_change_refused(self):
        client, plan, proposal, _ = self.fixture([self.approval()], head_sha="c" * 40)
        with self.assertRaisesRegex(GitHubError, "PROPOSAL_REMOTE_IDENTITY_CHANGED"):
            client.verified_independent_review(plan, proposal)


if __name__ == "__main__":
    unittest.main()
