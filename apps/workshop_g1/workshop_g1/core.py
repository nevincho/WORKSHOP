"""G1 read-only local workspace model. Never invokes Git, network or subprocesses."""
import hashlib
import json
import os
import re
import stat
import uuid
from pathlib import Path

MAX_FILE = 1024 * 1024
MAX_LINE = 16 * 1024
MAX_TOTAL = 32 * 1024 * 1024
MAX_TASKS = 1000
MAX_DEPTH = 16
REQUIRED = ('TASK_ID','PROJECT','PRIORITY','STATUS','OBJECTIVE','SOURCE_PLAN_OR_REQUEST','CURRENT_STATE', 'PREREQUISITES','DEPENDENCIES','AFFECTED_COMPONENTS','PROTECTED_COMPONENTS','EXECUTION_CLASS','CODEX_ALLOWED','ACCEPTANCE_CRITERIA','VALIDATION_METHOD','PRE_CHANGE_CHECKPOINT','ROLLBACK_METHOD','EVIDENCE_PATHS')
ENUMS = {'PRIORITY': {'CRITICAL','HIGH','MEDIUM','LOW'}, 'STATUS': {'READY','IN_PROGRESS','BLOCKED','REVIEW','COMPLETE','HOLD'}, 'EXECUTION_CLASS': {'WORKER','CODEX_CANDIDATE','HUMAN_GATE','MONITOR_ONLY'}, 'CODEX_ALLOWED': {'YES','NO','GATE_REQUIRED'}}
FIELD = re.compile(r'^([A-Z][A-Z0-9_]*):\s*(.*)$')
TASK_NAME = re.compile(r'^(?:TASK[-_]|WORKSHOP[-_]|[A-Z][A-Z0-9]*[-_]\d+)', re.I)
TASK_ID_LINE = re.compile(r'^\s*(?:TASK_ID\s*:|[-*]\s*\*\*TASK_ID\*\*\s*:)', re.M)
WINDOWS_BAD = re.compile(r'[<>:"|?*\x00-\x1f]')

class G1Error(ValueError):
    pass


def safe_path(path):
    """Reject links/reparse points on every existing component without resolving them."""
    raw = os.fspath(path)
    if not raw or '\x00' in raw:
        raise G1Error('INVALID_PATH')
    p = Path(os.path.abspath(raw))
    if os.name == 'nt' and (str(p).startswith('\\\\') or p.drive.startswith('\\\\')):
        raise G1Error('UNSAFE_NETWORK_PATH')
    for component in (p, *p.parents):
        try:
            s = component.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(s.st_mode) or (getattr(s, 'st_file_attributes', 0) & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0)):
            raise G1Error('UNSAFE_LINK')
    return p


def contained(root, relative):
    if not isinstance(relative, str) or not relative or '/' in relative.replace('\\', '/')[:0]:
        raise G1Error('INVALID_PATH')
    parts = re.split(r'[/\\]', relative)
    if (len(parts) > MAX_DEPTH or any(x in ('', '.', '..') or WINDOWS_BAD.search(x) or x.rstrip(' .') != x or x.split('.')[0].upper() in {'CON','PRN','AUX','NUL',*(f'COM{i}' for i in range(1,10)),*(f'LPT{i}' for i in range(1,10))} for x in parts)):
        raise G1Error('INVALID_PATH')
    root = safe_path(root)
    p = safe_path(root.joinpath(*parts))
    if not p.is_relative_to(root):
        raise G1Error('INVALID_PATH')
    return p


def verified_trust(bundle):
    bundle = safe_path(bundle)
    manifest_file = contained(bundle, 'manifest.json')
    manifest = json.loads(read_limited(manifest_file, max_bytes=65536))
    if manifest.get('manifest_version') != 1 or manifest.get('profile') != 'workshop-markdown-v1' or not re.fullmatch(r'[a-f0-9]{40}', manifest.get('commit', '')):
        raise G1Error('UNSUPPORTED_SCHEMA')
    if manifest.get('repository') != 'nevincho/WORKSHOP' or not isinstance(manifest.get('files'), dict):
        raise G1Error('UNTRUSTED_SOURCE')
    for name in ('TASK_SCHEMA.md', 'STATE_MACHINE.md'):
        expected = manifest['files'].get(name)
        if not isinstance(expected, str) or not re.fullmatch('[0-9a-f]{64}', expected):
            raise G1Error('TRUST_MISSING')
        raw = read_limited(contained(bundle, name), raw=True)
        if hashlib.sha256(raw).hexdigest() != expected:
            raise G1Error('TRUST_MODIFIED')
    return manifest


def read_limited(path, max_bytes=MAX_FILE, raw=False):
    p = safe_path(path)
    if not p.is_file() or p.stat().st_size > max_bytes:
        raise G1Error('MISSING_OR_OVERSIZED')
    # Avoid broad decode/following additional paths. Recheck identity after reading.
    before = p.lstat()
    with p.open('rb') as f:
        b = f.read(max_bytes + 1)
    after = p.lstat()
    if len(b) > max_bytes or (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns):
        raise G1Error('CHANGED_DURING_READ')
    if b'\0' in b:
        raise G1Error('MALFORMED')
    if raw:
        return b
    try:
        t = b.decode('utf-8')
    except UnicodeDecodeError as e:
        raise G1Error('MALFORMED_UTF8') from e
    if any(len(line) > MAX_LINE for line in t.splitlines()):
        raise G1Error('OVERSIZED_LINE')
    return t


def parse_task(text):
    fields = {}
    for line in text.splitlines():
        m = FIELD.match(line)
        if m:
            if m[1] in fields:
                raise G1Error('DUPLICATE_FIELD')
            fields[m[1]] = m[2].strip()
    if any(not fields.get(k) for k in REQUIRED):
        raise G1Error('INVALID_TASK')
    if any(fields.get(k) not in allowed for k, allowed in ENUMS.items()):
        raise G1Error('INVALID_ENUM')
    if 'SCHEMA_VERSION' in fields and fields['SCHEMA_VERSION'] != 'workshop-markdown-v1':
        raise G1Error('UNSUPPORTED_SCHEMA')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{1,127}', fields['TASK_ID']):
        raise G1Error('INVALID_TASK_ID')
    return fields


def document_kind(filename, text):
    """Classify only; non-task documents never become authoritative tasks."""
    if TASK_ID_LINE.search(text):
        return 'task_candidate'
    if TASK_NAME.match(filename):
        return 'legacy_candidate'
    return 'document'


def inspect_workspace(root, bundle):
    verified_trust(bundle)
    root = safe_path(root)
    if not root.is_dir():
        raise G1Error('NOT_A_DIRECTORY')
    tasks = []
    diagnostics = []
    seen = {}
    total = 0
    task_root = contained(root, 'tasks')
    if not task_root.exists():
        return tasks, [('tasks', 'MISSING_REFERENCE')]
    if not task_root.is_dir():
        raise G1Error('INVALID_PATH')
    # Non-recursive, bounded. No .git traversal, no following links.
    entries = list(task_root.iterdir())
    if len(entries) > MAX_TASKS:
        raise G1Error('TOO_MANY_TASKS')
    for p in sorted(entries, key=lambda v: v.name.casefold()):
        try:
            contained(task_root, p.name)
            if p.suffix.lower() != '.md':
                continue
            n = p.stat().st_size
            total += n
            if total > MAX_TOTAL:
                raise G1Error('CORPUS_OVERSIZED')
            raw_text = read_limited(p)
            kind = document_kind(p.name, raw_text)
            if kind == 'document':
                continue  # Markdown documentation is data, not an invalid task.
            if kind == 'legacy_candidate':
                diagnostics.append((p.name, 'LEGACY_TASK_FORMAT'))
                continue
            try:
                fields = parse_task(raw_text)
            except G1Error as exc:
                if str(exc) == 'INVALID_TASK':
                    diagnostics.append((p.name, 'INCOMPLETE_TASK_SCHEMA'))
                    continue
                raise
            key = fields['TASK_ID'].casefold()
            if key in seen:
                diagnostics.append((str(p.name), 'DUPLICATE_TASK_ID'))
                diagnostics.append((str(seen[key]), 'DUPLICATE_TASK_ID'))
            seen[key] = p.name
            tasks.append((p.name, fields))
        except (G1Error, OSError, UnicodeError) as e:
            diagnostics.append((p.name, str(e)))
    return tasks, diagnostics


def create_workspace(dest, bundle):
    manifest = verified_trust(bundle)
    p = safe_path(dest)
    if p.exists():
        raise G1Error('DESTINATION_EXISTS')
    if not p.parent.is_dir():
        raise G1Error('MISSING_PARENT')
    # Exactly one new root, workspace.json and tasks directory, no git init.
    p.mkdir()
    try:
        payload = {'workspace_version': 1, 'workspace_id': str(uuid.uuid4()), 'trusted_commit': manifest['commit']}
        contained(p, 'workspace.json').write_text(json.dumps(payload, indent=2), encoding='utf-8')
        contained(p, 'tasks').mkdir()
        return p
    except Exception:
        # Attempt rollback only known new objects.
        (p / 'workspace.json').unlink(missing_ok=True)
        try:
            (p / 'tasks').rmdir()
            p.rmdir()
        except OSError:
            pass
        raise

