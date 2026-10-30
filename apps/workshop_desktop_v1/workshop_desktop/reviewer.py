"""Separate-process deterministic reviewer: independent from worker process."""
import hashlib
import json
import os
import sys
from pathlib import Path
from .github_api import validate_target


def review(plan_file, output_file, report_file):
    plan = json.loads(Path(plan_file).read_text(encoding="utf-8"))
    validate_target(plan["repo"], plan["ref"], plan["path"])
    data = Path(output_file).read_bytes()
    expected = plan["content"].encode("utf-8")
    checks = {
        "approved_operation": plan["executor"] == "markdown-writer-v1" and plan["operation"] == "CREATE_MARKDOWN",
        "path_allowlist": plan["path"].startswith("docs/") and plan["path"].endswith(".md"),
        "exact_bytes": data == expected,
        "bounded_bytes": 0 < len(data) <= 16384,
        "no_null": b"\0" not in data,
    }
    result = {"reviewer_pid": os.getpid(), "verdict": "PASS" if all(checks.values()) else "REWORK",
              "checks": checks, "sha256": hashlib.sha256(data).hexdigest()}
    Path(report_file).write_text(json.dumps(result, sort_keys=True, indent=2), encoding="utf-8")
    return result


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 3:
        return 2
    try:
        result = review(*args)
        if sys.stdout is not None:
            print(json.dumps(result, sort_keys=True))
        return 0 if result["verdict"] == "PASS" else 1
    except (OSError, ValueError, KeyError, TypeError) as exc:
        if sys.stderr is not None:
            print("REVIEW_ERROR:" + type(exc).__name__, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
