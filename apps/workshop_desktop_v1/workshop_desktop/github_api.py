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

    def _proposal_branch_sha(self, repo, branch):
        response = self.request("GET", "/repos/" + repo + "/git/ref/heads/" + branch,
                                authorized=True)
        sha = response.get("object", {}).get("sha")
        if not isinstance(sha, str) or not SHA.fullmatch(sha):
            raise GitHubError("INVALID_PROPOSAL_BRANCH_REF")
        return sha

    def propose(self, plan, content, approval_id):
        """Create a new isolated branch and draft PR; caller must journal intent first."""
        repo, ref, path = plan["repo"], plan["ref"], plan["path"]
        validate_target(repo, ref, path)
        if not SHA.fullmatch(plan["target_sha"]):
            raise GitHubError("INVALID_TARGET_SHA")
        if self.head(repo, ref) != plan["target_sha"]:
            raise GitHubError("REMOTE_HEAD_CHANGED")
        if self.file_exists(repo, ref, path):
            raise GitHubError("REMOTE_PATH_EXISTS")
        branch = "workshop-proposal-" + approval_id[:20]
        result = {"branch": branch, "remote_created": "UNKNOWN",
                  "pr_url": None, "proposal_sha": None}
        try:
            self.request("POST", "/repos/" + repo + "/git/refs",
                         {"ref": "refs/heads/" + branch, "sha": plan["target_sha"]},
                         authorized=True)
        except Exception as exc:
            # POST may have succeeded server-side despite a client timeout.
            try:
                observed = self._proposal_branch_sha(repo, branch)
                result["remote_created"] = True
                result["observed_branch_sha"] = observed
            except Exception as check_exc:
                result["remote_check_error"] = type(check_exc).__name__ + ":" + str(check_exc)
            raise PartialProposal(result, "BRANCH_POST_UNCERTAIN:" + str(exc)) from None
        try:
            observed = self._proposal_branch_sha(repo, branch)
            result["remote_created"] = True
            result["observed_branch_sha"] = observed
            if observed != plan["target_sha"]:
                raise GitHubError("PROPOSAL_BRANCH_SHA_MISMATCH")
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
                               "body": "Deterministic Markdown-only proposal; independent acceptance pending.",
                               "draft": True}, authorized=True)
            result["pr_url"] = pr.get("html_url")
            if not result["pr_url"] or not SHA.fullmatch(str(result["proposal_sha"])):
                raise GitHubError("INVALID_PROPOSAL_RESPONSE")
            return result
        except Exception as exc:
            raise PartialProposal(result, str(exc)) from None


    def verified_independent_review(self, plan, proposal):
        """Read GitHub-authenticated review of the exact immutable draft PR commit.

        A local deterministic preflight is NOT an independent review.  GitHub
        identifies the reviewer and records the reviewed commit.  No writes.
        """
        repo = plan["repo"]
        url = proposal.get("pr_url")
        prefix = "https://github.com/" + repo + "/pull/"
        if not isinstance(url, str) or not url.startswith(prefix):
            raise GitHubError("INVALID_PROPOSAL_URL")
        number = url[len(prefix):]
        if not number.isdecimal() or int(number) < 1:
            raise GitHubError("INVALID_PROPOSAL_NUMBER")
        commit = proposal.get("proposal_sha")
        branch = proposal.get("branch")
        if not isinstance(commit, str) or not SHA.fullmatch(commit):
            raise GitHubError("INVALID_PROPOSAL_SHA")
        pr = self.request("GET", "/repos/" + repo + "/pulls/" + number, authorized=True)
        head = pr.get("head") or {}
        base = pr.get("base") or {}
        author = (pr.get("user") or {}).get("login")
        if (pr.get("state") != "open" or pr.get("merged_at") or
                head.get("sha") != commit or head.get("ref") != branch or
                (head.get("repo") or {}).get("full_name") != repo or
                base.get("ref") != plan["ref"] or
                not isinstance(author, str) or not author):
            raise GitHubError("PROPOSAL_REMOTE_IDENTITY_CHANGED")
        if self.head(repo, plan["ref"]) != plan["target_sha"]:
            raise GitHubError("PROPOSAL_BASE_CHANGED")
        if self.read_file(repo, commit, plan["path"]) != plan["content"].encode("utf-8"):
            raise GitHubError("PROPOSAL_REMOTE_CONTENT_CHANGED")
        reviews = self.request("GET", "/repos/" + repo + "/pulls/" + number + "/reviews?per_page=100",
                               authorized=True)
        if not isinstance(reviews, list) or len(reviews) >= 100:
            raise GitHubError("REVIEW_HISTORY_UNBOUNDED")
        # Review APIs may not guarantee caller-visible ordering. Resolve each
        # reviewer's latest submitted decision by timestamp and immutable ID.
        if any(not isinstance(r, dict) for r in reviews):
            raise GitHubError("INVALID_REVIEW_HISTORY")
        latest = {}
        for review in sorted(reviews, key=lambda r: (r.get("submitted_at") or "", r.get("id") or 0)):
            login = (review.get("user") or {}).get("login")
            if not isinstance(login, str) or not login:
                continue
            if review.get("state") in ("APPROVED", "CHANGES_REQUESTED", "DISMISSED"):
                latest[login.casefold()] = review
        # Fail closed if any other independent reviewer still requests changes.
        # An approval from a different account does not resolve that veto.
        unresolved = [login for login, review in latest.items()
                      if login != author.casefold() and review.get("state") == "CHANGES_REQUESTED"]
        if unresolved:
            raise GitHubError("UNRESOLVED_CHANGES_REQUESTED")
        eligible = [r for login, r in latest.items()
                    if login != author.casefold() and r.get("state") == "APPROVED"
                    and r.get("commit_id") == commit and r.get("submitted_at")]
        if not eligible:
            raise GitHubError("INDEPENDENT_GITHUB_APPROVAL_REQUIRED")
        accepted = sorted(eligible, key=lambda r: (r["submitted_at"], r.get("id", 0)))[-1]
        return {"provider": "GITHUB_AUTHENTICATED_PR_REVIEW",
                "reviewer": accepted["user"]["login"], "author": author,
                "review_id": accepted["id"], "reviewed_commit": commit,
                "submitted_at": accepted["submitted_at"], "pr_url": url}



class PartialProposal(GitHubError):
    def __init__(self, partial, reason):
        self.partial = partial
        super().__init__("REMOTE_PARTIAL:" + reason)
