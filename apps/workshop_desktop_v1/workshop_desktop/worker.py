"""Separate-process deterministic worker. No Git, network, shell, or arbitrary code."""
import hashlib
import json
import os
import sys
from pathlib import Path
from .github_api import validate_target


def execute(plan_file, output_file):
    plan = json.loads(Path(plan_file).read_text(encoding="utf-8"))
    validate_target(plan["repo"], plan["ref"], plan["path"])
    if plan["executor"] != "markdown-writer-v1" or plan["operation"] != "CREATE_MARKDOWN":
        raise ValueError("UNSUPPORTED_EXECUTOR")
    data = plan["content"].encode("utf-8")
    if not data or len(data) > 16384 or b"\0" in data:
        raise ValueError("INVALID_CONTENT")
    output = Path(output_file)
    if output.exists() or output.is_symlink():
        raise ValueError("OUTPUT_EXISTS")
    fd = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    result = {"pid": os.getpid(), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
              "executor": "markdown-writer-v1"}
    metadata = output.with_name("worker_result.json")
    fd = os.open(metadata, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(json.dumps(result, sort_keys=True).encode("utf-8"))
        stream.flush()
        os.fsync(stream.fileno())
    return result


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 2:
        return 2
    try:
        result = execute(args[0], args[1])
        if sys.stdout is not None:
            print(json.dumps(result, sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        if sys.stderr is not None:
            print("WORKER_ERROR:" + type(exc).__name__, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
