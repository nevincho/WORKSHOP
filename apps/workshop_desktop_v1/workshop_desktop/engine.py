"""Git-backed, single-task WORKSHOP Desktop V1 candidate controller.

This is NOT an OS sandbox or general coding agent. Only a fixed Markdown writer
may run, and remote mutation is a separately approved draft-PR operation.
"""
import getpass
import hashlib
import hmac
import json
import os
import re
import secrets
import shutil
import stat
import subprocess
import sys
import threading
import time
import uuid
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .github_api import GitHubClient, GitHubError, PartialProposal, validate_target
from .vault import SIGNING, TARGET, WindowsVault

APP = ".workshop_v1"
MAX_LOG = 32768
TASK_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{1,80}$")


class ControllerError(RuntimeError):
    pass


def local_actor():
    """Read actual Windows login identity rather than spoofable USERNAME env."""
    if os.name == "nt":
        import ctypes
        from ctypes import wintypes
        size = wintypes.DWORD(256)
        buffer = ctypes.create_unicode_buffer(size.value)
        fn = ctypes.WinDLL("Advapi32", use_last_error=True).GetUserNameW
        fn.argtypes = (wintypes.LPWSTR, ctypes.POINTER(wintypes.DWORD))
        fn.restype = wintypes.BOOL
        if not fn(buffer, ctypes.byref(size)):
            raise ControllerError("OS_IDENTITY_UNAVAILABLE")
        return buffer.value
    return getpass.getuser()


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def _safe_path(path):
    p = Path(os.path.abspath(path))
    for part in (p, *p.parents):
        try:
            st = part.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(st.st_mode) or getattr(st, "st_file_attributes", 0) & 0x400:
            raise ControllerError("UNSAFE_LINK_OR_REPARSE_POINT")
    return p


def _write_atomic(path, data):
    path = _safe_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".new-" + uuid.uuid4().hex)
    try:
        with open(temp, "xb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, path)
    finally:
        try:
            temp.unlink(missing_ok=True)
        except OSError:
            pass


def _git(repo, *args, timeout=20):
    if not shutil.which("git"):
        raise ControllerError("GIT_NOT_INSTALLED")
    repo = _safe_path(repo)
    env = dict(os.environ)
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["GIT_OPTIONAL_LOCKS"] = "0"
    # Fixed commands, no shell, no untrusted hooks, no global config or credential helper.
    command = ["git", "-c", "core.hooksPath=" + str(repo / "disabled_hooks"),
               "-c", "commit.gpgsign=false", "-c", "core.fsmonitor=false",
               "-c", "user.name=WORKSHOP Desktop", "-c", "user.email=desktop@localhost", *args]
    try:
        result = subprocess.run(command, cwd=repo, env=env, capture_output=True, text=True,
                                timeout=timeout, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ControllerError("GIT_EXECUTION_FAILED") from exc
    if result.returncode:
        raise ControllerError("GIT_COMMAND_FAILED:" + args[0])
    return result.stdout.strip()


class CoordinationRepo:
    def __init__(self, workspace):
        self.workspace = _safe_path(workspace)
        if not self.workspace.is_dir():
            raise ControllerError("WORKSPACE_NOT_FOUND")
        self.home = self.workspace / APP
        self.repo = self.home / "coordination"
        self.staging = self.home / "staging"

    def initialize(self):
        if self.home.exists():
            raise ControllerError("COORDINATION_ALREADY_EXISTS")
        self.repo.mkdir(parents=True)
        self.staging.mkdir()
        (self.repo / "disabled_hooks").mkdir()
        _git(self.repo, "init", "-q")
        _write_atomic(self.repo / "state.json", canonical({"version": 1, "tasks": {}}))
        self._append_event({"kind": "INITIALIZED", "workspace": self.workspace.name})
        _git(self.repo, "add", "--", "state.json", "events.jsonl")
        _git(self.repo, "commit", "-qm", "WORKSHOP Desktop coordination initialized")
        return self.head()

    def head(self):
        return _git(self.repo, "rev-parse", "HEAD")

    def _clean(self):
        if not (self.repo / ".git").is_dir():
            raise ControllerError("COORDINATION_GIT_MISSING")
        if _git(self.repo, "status", "--porcelain"):
            raise ControllerError("DIRTY_COORDINATION_REQUIRES_RECOVERY")

    def read(self, relative):
        return json.loads((self.repo / relative).read_text(encoding="utf-8"))

    def state(self):
        return self.read("state.json")

    def _append_event(self, event):
        path = self.repo / "events.jsonl"
        lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
        previous = json.loads(lines[-1])["hash"] if lines else "0" * 64
        record = {"previous": previous, "event": event, "time": now()}
        record["hash"] = digest(canonical(record))
        lines.append(json.dumps(record, sort_keys=True, ensure_ascii=False))
        _write_atomic(path, ("\n".join(lines) + "\n").encode("utf-8"))

    def verify(self):
        self._clean()
        previous = "0" * 64
        for line in (self.repo / "events.jsonl").read_text(encoding="utf-8").splitlines():
            record = json.loads(line)
            h = record.pop("hash")
            if record["previous"] != previous or digest(canonical(record)) != h:
                raise ControllerError("AUDIT_CHAIN_MISMATCH")
            previous = h
        state = self.state()
        if state.get("version") != 1 or not isinstance(state.get("tasks"), dict):
            raise ControllerError("UNSUPPORTED_COORDINATION_VERSION")
        if any(t.get("status") == "IN_PROGRESS" for t in state["tasks"].values()):
            raise ControllerError("INTERRUPTED_RUN_REQUIRES_REVIEW")
        return state

    def recover_interrupted(self, actor):
        """Explicit recovery: isolate interrupted tasks, never resume or publish."""
        self._clean()
        state = self.state()
        ids = [identifier for identifier, task in state["tasks"].items()
               if task["status"] == "IN_PROGRESS"]
        if not ids:
            raise ControllerError("NO_INTERRUPTED_RUN")
        for identifier in ids:
            state["tasks"][identifier]["status"] = "BLOCKED"
        self.transaction(state, {"kind": "INTERRUPTED_RUN_BLOCKED", "actor": actor, "ids": ids})
        return ids

    @contextmanager
    def _lock(self):
        lock = self.home / "transaction.lock"
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError as exc:
            raise ControllerError("CONCURRENT_TRANSACTION_OR_STALE_LOCK") from exc
        os.close(fd)
        try:
            yield
        finally:
            lock.unlink(missing_ok=True)

    def transaction(self, state, event, artifacts=None, expected_head=None):
        artifacts = artifacts or {}
        with self._lock():
            self._clean()
            before = self.head()
            if expected_head is not None and before != expected_head:
                raise ControllerError("COORDINATION_HEAD_CHANGED")
            files = {"state.json": canonical(state)}
            for name, value in artifacts.items():
                if not re.fullmatch(r"(plans|approvals|runs|reviews|checkpoints)/[a-f0-9]{32}\.json", name):
                    raise ControllerError("INVALID_ARTIFACT_PATH")
                files[name] = canonical(value)
            for name, data in files.items():
                _write_atomic(self.repo / name, data)
            self._append_event(event)
            _git(self.repo, "add", "--", *files.keys(), "events.jsonl")
            _git(self.repo, "commit", "-qm", "WORKSHOP Desktop: " + event["kind"])
            return self.head()


def _launch(role, arguments, cwd, timeout=20, cancel=None):
    entrypoint = Path(__file__).resolve().parents[1] / "main.py"
    if getattr(sys, "frozen", False):
        command = [sys.executable, "--" + role, *map(str, arguments)]
    else:
        command = [sys.executable, str(entrypoint), "--" + role, *map(str, arguments)]
    env = {k: v for k, v in os.environ.items()
           if not (k.upper().endswith(("_TOKEN", "_SECRET", "_PASSWORD", "_KEY"))
                   or k.upper() in {"PYTHONPATH", "PYTHONSTARTUP", "GIT_ASKPASS"})}
    flags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
    proc = subprocess.Popen(command, cwd=cwd, env=env, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, creationflags=flags)
    started = time.monotonic()
    while True:
        try:
            out, err = proc.communicate(timeout=0.2)
            break
        except subprocess.TimeoutExpired:
            if (cancel is not None and cancel.is_set()) or time.monotonic() - started > timeout:
                proc.kill()
                out, err = proc.communicate()
                raise ControllerError("EXECUTOR_CANCELLED_OR_TIMED_OUT")
    return proc.returncode, out[:MAX_LOG].decode("utf-8", "replace"), err[:MAX_LOG].decode("utf-8", "replace")


class Controller:
    def __init__(self, workspace, github=None, vault=None):
        self.store = CoordinationRepo(workspace)
        self.vault = vault if vault is not None else WindowsVault()
        self.github = github if github is not None else GitHubClient(lambda: self.vault.get(TARGET))
        self.actor = local_actor()

    def initialize(self):
        return self.store.initialize()

    def status(self):
        return self.store.verify()

    def plan(self, task_id, project, repo, ref, path, content):
        state = self.status()
        if any(t["status"] not in ("COMPLETE", "BLOCKED", "HOLD") for t in state["tasks"].values()):
            raise ControllerError("ONLY_ONE_ACTIVE_TASK")
        if not TASK_ID.fullmatch(task_id) or not project.strip() or len(project) > 100:
            raise ControllerError("INVALID_TASK")
        validate_target(repo, ref, path)
        raw = content.encode("utf-8")
        if not raw or len(raw) > 16384 or b"\0" in raw:
            raise ControllerError("INVALID_CONTENT")
        sha = self.github.head(repo, ref)
        if self.github.file_exists(repo, ref, path):
            raise ControllerError("TARGET_FILE_ALREADY_EXISTS")
        identifier = uuid.uuid4().hex
        plan = {"id": identifier, "task_id": task_id, "project": project, "repo": repo,
                "ref": ref, "path": path, "content": content, "target_sha": sha,
                "executor": "markdown-writer-v1", "operation": "CREATE_MARKDOWN",
                "max_cost": 0, "created_by": self.actor, "created_at": now()}
        plan_hash = digest(canonical(plan))
        state["tasks"][identifier] = {"task_id": task_id, "status": "READY", "plan_hash": plan_hash,
                                      "approval": None, "run": None, "review": None}
        self.store.transaction(state, {"kind": "PLAN_CREATED", "id": identifier, "sha256": plan_hash},
                               {"plans/" + identifier + ".json": plan})
        return identifier

    def _plan(self, identifier):
        state = self.status()
        if identifier not in state["tasks"]:
            raise ControllerError("UNKNOWN_TASK")
        plan = self.store.read("plans/" + identifier + ".json")
        if digest(canonical(plan)) != state["tasks"][identifier]["plan_hash"]:
            raise ControllerError("PLAN_TAMPERED")
        return state, plan

    def _approval(self, identifier, state, plan):
        approval_id = state["tasks"][identifier].get("approval")
        if not approval_id:
            raise ControllerError("APPROVAL_REQUIRED")
        approval = self.store.read("approvals/" + approval_id + ".json")
        secret = self.vault.get(SIGNING)
        if not secret:
            raise ControllerError("APPROVAL_KEY_MISSING")
        payload = {key: value for key, value in approval.items() if key != "signature"}
        if not hmac.compare_digest(hmac.new(secret.encode(), canonical(payload), hashlib.sha256).hexdigest(),
                                   approval["signature"]):
            raise ControllerError("APPROVAL_TAMPERED")
        if (approval["plan_hash"] != digest(canonical(plan)) or
                approval["actor"] != self.actor or
                approval["target_sha"] != plan["target_sha"] or
                datetime.fromisoformat(approval["expires"]) <= datetime.now(timezone.utc)):
            raise ControllerError("APPROVAL_STALE_OR_INVALID")
        return approval

    def approve(self, identifier):
        state, plan = self._plan(identifier)
        if state["tasks"][identifier]["status"] != "READY":
            raise ControllerError("INVALID_APPROVAL_STATE")
        if self.github.head(plan["repo"], plan["ref"]) != plan["target_sha"]:
            raise ControllerError("TARGET_HEAD_CHANGED")
        secret = self.vault.get(SIGNING)
        if not secret:
            secret = secrets.token_hex(32)
            self.vault.put(SIGNING, secret)
        approval_id = uuid.uuid4().hex
        approval = {"id": approval_id, "plan_hash": digest(canonical(plan)), "actor": self.actor,
                    "target_sha": plan["target_sha"], "executor": plan["executor"],
                    "max_cost": 0, "expires": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()}
        approval["signature"] = hmac.new(secret.encode(), canonical(approval), hashlib.sha256).hexdigest()
        state["tasks"][identifier]["approval"] = approval_id
        self.store.transaction(state, {"kind": "APPROVED", "id": identifier, "actor": self.actor},
                               {"approvals/" + approval_id + ".json": approval})
        return approval_id

    def run(self, identifier, cancel=None):
        state, plan = self._plan(identifier)
        if state["tasks"][identifier]["status"] != "READY":
            raise ControllerError("INVALID_RUN_STATE")
        self._approval(identifier, state, plan)
        if self.github.head(plan["repo"], plan["ref"]) != plan["target_sha"]:
            raise ControllerError("TARGET_HEAD_CHANGED")
        run_id = uuid.uuid4().hex
        stage = self.store.staging / run_id
        stage.mkdir()
        output = stage / "artifact.md"
        state["tasks"][identifier]["status"] = "IN_PROGRESS"
        state["tasks"][identifier]["run"] = run_id
        self.store.transaction(state, {"kind": "RUN_STARTED", "id": identifier, "run": run_id})
        error = None
        metadata = {}
        try:
            code, stdout, stderr = _launch("worker",
                [self.store.repo / "plans" / (identifier + ".json"), output],
                stage, timeout=20, cancel=cancel)
            metadata_path = stage / "worker_result.json"
            metadata = json.loads(metadata_path.read_text(encoding="utf-8")) if metadata_path.is_file() else {}
            if (code != 0 or not output.is_file() or
                    metadata.get("sha256") != digest(output.read_bytes()) or
                    not isinstance(metadata.get("pid"), int)):
                error = "WORKER_FAILED"
        except ControllerError as exc:
            code, stdout, stderr = -1, "", str(exc)
            error = str(exc)
        result = {"id": run_id, "task": identifier, "worker_exit": code,
                  "stdout": stdout, "stderr": stderr, "error": error,
                  "worker_pid": metadata.get("pid"),
                  "artifact_sha256": digest(output.read_bytes()) if output.is_file() else None,
                  "time": now()}
        state = self.store.state()
        state["tasks"][identifier]["status"] = "BLOCKED" if error else "REVIEW"
        self.store.transaction(state, {"kind": "RUN_BLOCKED" if error else "RUN_FINISHED",
                                       "id": identifier, "run": run_id},
                               {"runs/" + run_id + ".json": result})
        return result

    def review(self, identifier):
        state, plan = self._plan(identifier)
        task = state["tasks"][identifier]
        if task["status"] != "REVIEW" or not task["run"]:
            raise ControllerError("INVALID_REVIEW_STATE")
        run = self.store.read("runs/" + task["run"] + ".json")
        stage = self.store.staging / task["run"]
        output = stage / "artifact.md"
        if not output.is_file() or digest(output.read_bytes()) != run["artifact_sha256"]:
            raise ControllerError("STAGED_ARTIFACT_CHANGED")
        report_file = stage / "review.json"
        code, stdout, stderr = _launch("reviewer",
            [self.store.repo / "plans" / (identifier + ".json"), output, report_file], stage, timeout=20)
        if not report_file.is_file():
            raise ControllerError("REVIEWER_DID_NOT_REPORT")
        report = json.loads(report_file.read_text(encoding="utf-8"))
        worker_pid = run.get("worker_pid")
        if report.get("reviewer_pid") == worker_pid:
            raise ControllerError("REVIEWER_IDENTITY_COLLISION")
        if code != 0 or report.get("verdict") != "PASS" or report.get("sha256") != run["artifact_sha256"]:
            report["verdict"] = "REWORK"
        review_id = uuid.uuid4().hex
        report.update({"id": review_id, "task": identifier, "worker_pid": worker_pid,
                       "reviewer_stdout": stdout, "reviewer_stderr": stderr})
        state["tasks"][identifier]["review"] = review_id
        state["tasks"][identifier]["status"] = "REVIEW" if report["verdict"] == "PASS" else "REWORK"
        self.store.transaction(state, {"kind": "REVIEW_RECORDED", "id": identifier,
                                       "verdict": report["verdict"]},
                               {"reviews/" + review_id + ".json": report})
        return report

    def publish(self, identifier):
        """Explicit human accept action. Remote write only via reviewed draft PR."""
        state, plan = self._plan(identifier)
        task = state["tasks"][identifier]
        if task["status"] != "REVIEW" or not task["review"]:
            raise ControllerError("REVIEW_REQUIRED")
        approval = self._approval(identifier, state, plan)
        report = self.store.read("reviews/" + task["review"] + ".json")
        if report["verdict"] != "PASS":
            raise ControllerError("REVIEW_NOT_PASS")
        run = self.store.read("runs/" + task["run"] + ".json")
        output = self.store.staging / task["run"] / "artifact.md"
        data = output.read_bytes()
        if digest(data) != run["artifact_sha256"] or digest(data) != report["sha256"]:
            raise ControllerError("STAGED_ARTIFACT_CHANGED")
        if self.github.head(plan["repo"], plan["ref"]) != plan["target_sha"]:
            raise ControllerError("TARGET_HEAD_CHANGED")
        try:
            proposal = self.github.propose(plan, data, approval["id"])
        except PartialProposal as exc:
            state["tasks"][identifier]["status"] = "BLOCKED"
            self.store.transaction(state, {"kind": "REMOTE_PARTIAL", "id": identifier,
                                           "partial": exc.partial, "reason": str(exc)})
            raise
        checkpoint = {"id": identifier, "kind": "DRAFT_PR_NOT_MERGED", "baseline": plan["target_sha"],
                      "proposal": proposal, "review": task["review"], "accepted_by": self.actor,
                      "rollback": "Close draft PR and delete proposal branch after manual review; no automatic remote rollback."}
        state["tasks"][identifier]["status"] = "COMPLETE"
        self.store.transaction(state, {"kind": "PROPOSAL_SUBMITTED", "id": identifier,
                                       "pr_url": proposal["pr_url"]},
                               {"checkpoints/" + identifier + ".json": checkpoint})
        return checkpoint

    def recover_interrupted(self):
        return self.store.recover_interrupted(self.actor)

    def revoke_github(self):
        self.vault.delete(TARGET)

    def set_github_token(self, token):
        if not isinstance(token, str) or not token.strip() or len(token) > 2048:
            raise ControllerError("INVALID_TOKEN")
        self.vault.put(TARGET, token.strip())
