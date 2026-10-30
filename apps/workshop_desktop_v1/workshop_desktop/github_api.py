"""Scoped GitHub API adapter: read-only until explicit reviewed PR submission."""
import base64
import json
import re
import urllib.error
import urllib.parse
import urllib.request

REPO = re.compile(r"^[A-Za-z0-9_.-]{1,100}/[A-Za-z0-9_.-]{1,100}$")
REF = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_./-]{0,120}$")
SHA = re.compile(r"^[0-9a-f]{40}$")
SAFE_FILE = re.compile(r"^docs/(?:[A-Za-z0-9][A-Za-z0-9_.-]*/)*[A-Za-z0-9][A-Za-z0-9_.-]*\.md$")


class GitHubError(RuntimeError):
    pass


def validate_target(repo, ref, path):
    if not REPO.fullmatch(repo) or not REF.fullmatch(ref) or ".." in ref or ref.endswith(("/", ".")):
        raise GitHubError("INVALID_REPOSITORY_OR_REF")
    if not SAFE_FILE.fullmatch(path) or ".." in path or "\\" in path:
        raise GitHubError("INVALID_PROPOSAL_PATH")
    if any(part.upper().split(".")[0] in {"CON", "PRN", "AUX", "NUL"} for part in path.split("/")):
        raise GitHubError("INVALID_PROPOSAL_PATH")


class GitHubClient:
    def __init__(self, token_provider=None, transport=None):
        self.token_provider = token_provider or (lambda: None)
        self.transport = transport

    def request(self, method, route, payload=None, authorized=False):
        token = self.token_provider() if authorized or method == "GET" else None
        if authorized and not token:
            raise GitHubError("GITHUB_CREDENTIAL_REQUIRED")
        if not route.startswith("/") or "//" in route:
            raise GitHubError("INVALID_ROUTE")
        data = None if payload is None else json.dumps(payload, sort_keys=True).encode("utf-8")
        headers = {"Accept": "application/vnd.github+json", "User-Agent": "WORKSHOP-Desktop-V1",
                   "X-GitHub-Api-Version": "2022-11-28"}
        if token:
            headers["Authorization"] = "Bearer " + token
        if data is not None:
            headers["Content-Type"] = "application/json"
        if self.transport is not None:
            return self.transport(method, route, payload, authorized)
        request = urllib.request.Request("https://api.github.com" + route, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=12) as response:
                return json.loads(response.read(256000).decode("utf-8"))
        except urllib.error.HTTPError as exc:
            raise GitHubError("GITHUB_HTTP_" + str(exc.code)) from None
        except (urllib.error.URLError, TimeoutError) as exc:
            raise GitHubError("GITHUB_NETWORK_UNAVAILABLE") from None

    def head(self, repo, ref):
        validate_target(repo, ref, "docs/check.md")
        encoded = urllib.parse.quote(ref, safe="")
        data = self.request("GET", "/repos/" + repo + "/branches/" + encoded)
        sha = data.get("commit", {}).get("sha")
        if not isinstance(sha, str) or not SHA.fullmatch(sha):
            raise GitHubError("INVALID_REMOTE_HEAD")
        return sha

    def file_exists(self, repo, ref, path):
        validate_target(repo, ref, path)
        route = "/repos/" + repo + "/contents/" + urllib.parse.quote(path, safe="/")
        route += "?ref=" + urllib.parse.quote(ref, safe="")
        try:
            self.request("GET", route)
            return True
        except GitHubError as exc:
            if str(exc) == "GITHUB_HTTP_404":
                return False
            raise

    def read_file(self, repo, ref, path):
        validate_target(repo, ref, path)
        route = "/repos/" + repo + "/contents/" + urllib.parse.quote(path, safe="/")
        route += "?ref=" + urllib.parse.quote(ref, safe="")
        response = self.request("GET", route)
        if response.get("encoding") != "base64" or not isinstance(response.get("content"), str):
            raise GitHubError("INVALID_REMOTE_FILE")
        try:
            return base64.b64decode(response["content"], validate=False)
        except (ValueError, base64.binascii.Error):
            raise GitHubError("INVALID_REMOTE_FILE") from None

    def propose(self, plan, content, approval_id):
        """Create new isolated branch and PR. Never push to the selected base ref."""
        repo, ref, path = plan["repo"], plan["ref"], plan["path"]
        validate_target(repo, ref, path)
        if not SHA.fullmatch(plan["target_sha"]):
            raise GitHubError("INVALID_TARGET_SHA")
        if self.head(repo, ref) != plan["target_sha"]:
            raise GitHubError("REMOTE_HEAD_CHANGED")
        if self.file_exists(repo, ref, path):
            raise GitHubError("REMOTE_PATH_EXISTS")
        branch = "workshop-proposal-" + approval_id[:20]
        self.request("POST", "/repos/" + repo + "/git/refs",
                     {"ref": "refs/heads/" + branch, "sha": plan["target_sha"]}, authorized=True)
        # The remote branch is a durable external side effect even if a later API call fails.
        result = {"branch": branch, "remote_created": True, "pr_url": None, "proposal_sha": None}
        try:
            response = self.request("PUT", "/repos/" + repo + "/contents/" + urllib.parse.quote(path, safe="/"),
                                    {"message": "WORKSHOP reviewed Markdown proposal " + plan["task_id"],
                                     "content": base64.b64encode(content).decode("ascii"), "branch": branch},
                                    authorized=True)
            result["proposal_sha"] = response.get("commit", {}).get("sha")
            if self.read_file(repo, branch, path) != content:
                raise GitHubError("REMOTE_CONTENT_MISMATCH")
            pr = self.request("POST", "/repos/" + repo + "/pulls",
                              {"title": "WORKSHOP proposal: " + plan["task_id"],
                               "head": branch, "base": ref,
                               "body": "Deterministic Markdown-only proposal. Review before merging.",
                               "draft": True}, authorized=True)
            result["pr_url"] = pr.get("html_url")
            if not result["pr_url"] or not SHA.fullmatch(str(result["proposal_sha"])):
                raise GitHubError("INVALID_PROPOSAL_RESPONSE")
            return result
        except Exception as exc:
            raise PartialProposal(result, str(exc)) from None


class PartialProposal(GitHubError):
    def __init__(self, partial, reason):
        self.partial = partial
        super().__init__("REMOTE_PARTIAL:" + reason)
