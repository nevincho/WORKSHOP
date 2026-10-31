"""Separate-process deterministic reviewer: independent from worker process."""
import hashlib
import json
import os
import stat
import sys
from pathlib import Path
from .github_api import validate_target


def _exclusive_report(report_file, output_file, payload):
    """Refuse existing report/reparse points; create new file exclusively in stage."""
    report = Path(os.path.abspath(report_file))
    output = Path(os.path.abspath(output_file))
    if report.parent != output.parent or report.name != "review.json":
        raise ValueError("REVIEW_REPORT_OUTSIDE_STAGE")
    for part in (report, *report.parents):
        try:
            mode = part.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(mode.st_mode) or getattr(mode, "st_file_attributes", 0) & 0x400:
            raise ValueError("REVIEW_REPARSE_POINT")
    before = report.parent.stat(follow_symlinks=False)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(report, flags, 0o600)
    with os.fdopen(fd, "wb") as stream:
        opened = os.fstat(stream.fileno())
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
        after = report.parent.stat(follow_symlinks=False)
        visible = report.stat(follow_symlinks=False)
        if ((before.st_dev, before.st_ino) != (after.st_dev, after.st_ino) or
                (opened.st_dev, opened.st_ino) != (visible.st_dev, visible.st_ino)):
            raise ValueError("REVIEW_OUTPUT_IDENTITY_CHANGED")


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
    _exclusive_report(report_file, output_file, json.dumps(result, sort_keys=True, indent=2).encode("utf-8"))
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
