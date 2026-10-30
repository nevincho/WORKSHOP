"""Consolidated integration and negative/security tests; no live GitHub writes."""
import json
import os
import uuid
import subprocess
import tempfile
import unittest
from pathlib import Path

from workshop_desktop.engine import Controller, ControllerError, CoordinationRepo
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

    def test_full_g1_to_g7_candidate_draft_pr(self):
        rows, errors = inspect_workspace(self.root, trusted_bundle(), require_metadata=True)
        self.assertEqual((rows, errors), ([], []))
        identifier = self.make_plan()
        self.assertEqual(self.controller.status()["tasks"][identifier]["status"], "READY")
        approval = self.controller.approve(identifier)
        run = self.controller.run(identifier)
        self.assertEqual(run["worker_exit"], 0, run)
        self.assertIsNone(run["error"])
        review = self.controller.review(identifier)
        self.assertEqual(review["verdict"], "PASS", review)
        self.assertNotEqual(review["reviewer_pid"], review["worker_pid"])
        checkpoint = self.controller.publish(identifier)
        self.assertEqual(checkpoint["kind"], "DRAFT_PR_NOT_MERGED")
        self.assertEqual(checkpoint["proposal"]["pr_url"], "https://github.com/example/demo/pull/1")
        self.assertEqual(self.controller.status()["tasks"][identifier]["status"], "COMPLETE")
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
        self.controller.approve(identifier)
        with self.assertRaisesRegex(ControllerError, "REVIEW_REQUIRED"):
            self.controller.publish(identifier)

    def test_head_change_invalidates_approval(self):
        identifier = self.make_plan()
        self.controller.approve(identifier)
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
        approval_id = self.controller.approve(identifier)
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
        self.controller.approve(identifier)
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
        self.controller.store.transaction(state, {"kind": "INJECTED_INTERRUPTION", "id": identifier})
        with self.assertRaisesRegex(ControllerError, "INTERRUPTED_RUN_REQUIRES_REVIEW"):
            self.controller.status()
        recovered = self.controller.recover_interrupted()
        self.assertEqual(recovered, [identifier])
        self.assertEqual(self.controller.status()["tasks"][identifier]["status"], "BLOCKED")
        self.assertEqual(self.github.proposals, [])

    def test_staged_artifact_tamper_refused(self):
        identifier = self.make_plan()
        self.controller.approve(identifier)
        run = self.controller.run(identifier)
        output = self.controller.store.staging / run["id"] / "artifact.md"
        output.write_text("tampered", encoding="utf-8")
        with self.assertRaisesRegex(ControllerError, "STAGED_ARTIFACT_CHANGED"):
            self.controller.review(identifier)

    def test_no_automatic_remote_write(self):
        identifier = self.make_plan()
        self.controller.approve(identifier)
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


class GitHubAdapterTests(unittest.TestCase):
    def test_read_only_default_and_approved_draft_pr(self):
        calls = []
        def transport(method, route, payload, authorized):
            calls.append((method, route, payload, authorized))
            if method == "GET" and "/branches/" in route:
                return {"commit": {"sha": SHA}}
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
