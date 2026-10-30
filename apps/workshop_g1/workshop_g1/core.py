"""G1 read-only local workspace model. Never invokes Git, network or subprocesses."""
import hashlib
import json
import os
import re
import stat
import unicodedata
import uuid
from pathlib import Path

MAX_FILE = 1024 * 1024
MAX_LINE = 16 * 1024
MAX_TOTAL = 32 * 1024 * 1024
MAX_TASKS = 1000
MAX_DEPTH = 16
PROFILE = 'workshop-markdown-v1'
APP_ID = 'workshop-desktop-g1'
WORKSPACE_VERSION = 1
REQUIRED = ('TASK_ID','PROJECT','PRIORITY','STATUS','OBJECTIVE','SOURCE_PLAN_OR_REQUEST','CURRENT_STATE','PREREQUISITES','DEPENDENCIES','AFFECTED_COMPONENTS','PROTECTED_COMPONENTS','EXECUTION_CLASS','CODEX_ALLOWED','ACCEPTANCE_CRITERIA','VALIDATION_METHOD','PRE_CHANGE_CHECKPOINT','ROLLBACK_METHOD','EVIDENCE_PATHS')
ENUMS = {'PRIORITY': {'CRITICAL','HIGH','MEDIUM','LOW'}, 'STATUS': {'READY','IN_PROGRESS','BLOCKED','REVIEW','COMPLETE','HOLD'}, 'EXECUTION_CLASS': {'WORKER','CODEX_CANDIDATE','HUMAN_GATE','MONITOR_ONLY'}, 'CODEX_ALLOWED': {'YES','NO','GATE_REQUIRED'}}
FIELD = re.compile(r'^([A-Z][A-Z0-9_]*):\s*(.*)$')
TASK_NAME = re.compile(r'^(?:TASK[-_]|WORKSHOP[-_]|[A-Z][A-Z0-9]*[-_]\d+)', re.I)
TASK_ID_LINE = re.compile(r'^\s*(?:TASK_ID\s*:|[-*]\s*\*\*TASK_ID\*\*\s*:)', re.M)
TASK_REF = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_-]{1,127}$')
WINDOWS_BAD = re.compile(r'[<>:"|?*\x00-\x1f]')
NONE_VALUES = {'NONE', 'N/A', 'NOT_APPLICABLE'}
RESERVED = {'CON','PRN','AUX','NUL',*(f'COM{i}' for i in range(1,10)),*(f'LPT{i}' for i in range(1,10))}

class G1Error(ValueError):
    pass

def _absolute(path):
    raw = os.fspath(path)
    if not raw or '\x00' in raw:
        raise G1Error('INVALID_PATH')
    p = Path(os.path.abspath(raw))
    if os.name == 'nt' and (str(p).startswith('\\\\') or p.drive.startswith('\\\\')):
        raise G1Error('UNSAFE_NETWORK_PATH')
    return p

def _windows_handle(path, directory=False):
    import ctypes
    from ctypes import wintypes
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    create = kernel32.CreateFileW
    create.argtypes = (wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID, wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE)
    create.restype = wintypes.HANDLE
    flags = 0x00200000 | (0x02000000 if directory else 0)
    handle = create(str(path), 0x80000000 if not directory else 0x80, 7, None, 3, flags, None)
    if handle == wintypes.HANDLE(-1).value:
        error = ctypes.get_last_error()
        if error in (2, 3):
            raise FileNotFoundError(str(path))
        raise OSError(error, os.strerror(error), str(path))
    return handle

def _windows_handle_info(handle):
    import ctypes
    from ctypes import wintypes
    class Info(ctypes.Structure):
        _fields_ = [('attributes', wintypes.DWORD), ('creation_low', wintypes.DWORD), ('creation_high', wintypes.DWORD), ('access_low', wintypes.DWORD), ('access_high', wintypes.DWORD), ('write_low', wintypes.DWORD), ('write_high', wintypes.DWORD), ('volume', wintypes.DWORD), ('size_high', wintypes.DWORD), ('size_low', wintypes.DWORD), ('links', wintypes.DWORD), ('index_high', wintypes.DWORD), ('index_low', wintypes.DWORD)]
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    info = Info()
    get_info = kernel32.GetFileInformationByHandle
    get_info.argtypes = (wintypes.HANDLE, ctypes.POINTER(Info))
    get_info.restype = wintypes.BOOL
    if not get_info(handle, ctypes.byref(info)):
        raise ctypes.WinError(ctypes.get_last_error())
    buffer = ctypes.create_unicode_buffer(32768)
    get_path = kernel32.GetFinalPathNameByHandleW
    get_path.argtypes = (wintypes.HANDLE, wintypes.LPWSTR, wintypes.DWORD, wintypes.DWORD)
    get_path.restype = wintypes.DWORD
    length = get_path(handle, buffer, len(buffer), 0)
    if not length or length >= len(buffer):
        raise ctypes.WinError(ctypes.get_last_error())
    final = buffer.value
    if final.startswith('\\\\?\\UNC\\'):
        final = '\\\\' + final[8:]
    elif final.startswith('\\\\?\\'):
        final = final[4:]
    return info.attributes, (info.volume, info.index_high, info.index_low), Path(final)

def _close_windows_handle(handle):
    import ctypes
    from ctypes import wintypes
    close = ctypes.WinDLL('kernel32', use_last_error=True).CloseHandle
    close.argtypes = (wintypes.HANDLE,)
    close.restype = wintypes.BOOL
    close(handle)

def _checked_windows_handle(path, directory=False):
    p = _absolute(path)
    handle = _windows_handle(p, directory=directory)
    try:
        attributes, identity, final = _windows_handle_info(handle)
        if attributes & 0x400 or os.path.normcase(str(final)) != os.path.normcase(str(p)):
            raise G1Error('UNSAFE_LINK')
        return handle, identity
    except Exception:
        _close_windows_handle(handle)
        raise

def safe_path(path):
    """Reject network paths and links/reparse points on each existing component."""
    p = _absolute(path)
    for component in (p, *p.parents):
        try:
            if os.name == 'nt':
                try:
                    handle, _ = _checked_windows_handle(component, directory=component.is_dir())
                    _close_windows_handle(handle)
                except OSError as exc:
                    if exc.errno != 5:
                        raise
                    attributes = getattr(component.lstat(), 'st_file_attributes', 0)
                    if attributes & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0):
                        raise G1Error('UNSAFE_LINK')
            else:
                s = component.lstat()
                if stat.S_ISLNK(s.st_mode):
                    raise G1Error('UNSAFE_LINK')
        except FileNotFoundError:
            continue
    return p

def _path_identity(path):
    path = _absolute(path)
    if os.name == 'nt':
        handle, identity = _checked_windows_handle(path, directory=path.is_dir())
        _close_windows_handle(handle)
        return identity
    info = path.lstat()
    return info.st_dev, info.st_ino

def safe_display(value):
    """Escape control and bidi-format characters before UI display."""
    return ''.join(
        f'\\u{ord(char):04x}' if unicodedata.category(char) in {'Cc','Cf'} else char
        for char in str(value)
    )

def contained(root, relative):
    if not isinstance(relative, str) or not relative:
        raise G1Error('INVALID_PATH')
    parts = re.split(r'[/\\]', relative)
    if len(parts) > MAX_DEPTH or any(x in ('', '.', '..') or WINDOWS_BAD.search(x) or x.rstrip(' .') != x or x.split('.')[0].upper() in RESERVED for x in parts):
        raise G1Error('INVALID_PATH')
    root = safe_path(root)
    p = safe_path(root.joinpath(*parts))
    if not p.is_relative_to(root):
        raise G1Error('INVALID_PATH')
    return p

def _open_binary(path):
    p = _absolute(path)
    if os.name == 'nt':
        import msvcrt
        handle, identity = _checked_windows_handle(p, directory=False)
        try:
            stream = os.fdopen(msvcrt.open_osfhandle(handle, os.O_RDONLY | os.O_BINARY), 'rb', closefd=True)
            return stream, identity
        except Exception:
            _close_windows_handle(handle)
            raise
    stream = os.fdopen(os.open(p, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0)), 'rb', closefd=True)
    info = os.fstat(stream.fileno())
    return stream, (info.st_dev, info.st_ino)

def read_limited(path, max_bytes=MAX_FILE, raw=False):
    p = safe_path(path)
    expected_identity = _path_identity(p)
    try:
        stream, opened_identity = _open_binary(p)
        with stream:
            if opened_identity != expected_identity:
                raise G1Error('CHANGED_DURING_READ')
            before = os.fstat(stream.fileno())
            if not stat.S_ISREG(before.st_mode) or before.st_size > max_bytes:
                raise G1Error('MISSING_OR_OVERSIZED')
            data = stream.read(max_bytes + 1)
            after = os.fstat(stream.fileno())
    except (FileNotFoundError, IsADirectoryError) as exc:
        raise G1Error('MISSING_OR_OVERSIZED') from exc
    if len(data) > max_bytes or (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns):
        raise G1Error('CHANGED_DURING_READ')
    if b'\0' in data:
        raise G1Error('MALFORMED')
    if raw:
        return data
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise G1Error('MALFORMED_UTF8') from exc
    if any(len(line.encode('utf-8')) > MAX_LINE for line in text.splitlines()):
        raise G1Error('OVERSIZED_LINE')
    return text

def verified_trust(bundle):
    bundle = safe_path(bundle)
    manifest = json.loads(read_limited(contained(bundle, 'manifest.json'), max_bytes=65536))
    if not isinstance(manifest, dict) or set(manifest) != {'manifest_version','profile','repository','commit','application','files'}:
        raise G1Error('UNSUPPORTED_SCHEMA')
    if manifest['manifest_version'] != 1 or manifest['profile'] != PROFILE or not re.fullmatch(r'[a-f0-9]{40}', manifest.get('commit', '')):
        raise G1Error('UNSUPPORTED_SCHEMA')
    if manifest['repository'] != 'nevincho/WORKSHOP':
        raise G1Error('UNTRUSTED_SOURCE')
    if manifest['application'] != {'id': APP_ID, 'workspace_versions': [WORKSPACE_VERSION]}:
        raise G1Error('INCOMPATIBLE_APPLICATION')
    expected_files = {'TASK_SCHEMA.md': 'schemas/TASK_SCHEMA.md', 'STATE_MACHINE.md': 'schemas/STATE_MACHINE.md'}
    files = manifest.get('files')
    if not isinstance(files, dict) or set(files) != set(expected_files):
        raise G1Error('TRUST_MISSING')
    for name, source_path in expected_files.items():
        entry = files[name]
        if not isinstance(entry, dict) or set(entry) != {'source_path','sha256'} or entry.get('source_path') != source_path:
            raise G1Error('UNSUPPORTED_SCHEMA')
        expected = entry.get('sha256')
        if not isinstance(expected, str) or not re.fullmatch(r'[0-9a-f]{64}', expected):
            raise G1Error('TRUST_MISSING')
        if hashlib.sha256(read_limited(contained(bundle, name), raw=True)).hexdigest() != expected:
            raise G1Error('TRUST_MODIFIED')
    return manifest

def _task_machine_lines(text):
    """Ignore fenced Markdown code examples when extracting task fields."""
    fence_char = None
    fence_length = 0
    for line in text.splitlines():
        candidate = line.lstrip(' ')
        if len(line) - len(candidate) <= 3:
            match = re.match(r'^(`{3,}|~{3,})', candidate)
            if match:
                token = match.group(1)
                if fence_char is None:
                    fence_char, fence_length = token[0], len(token)
                    continue
                if token[0] == fence_char and len(token) >= fence_length and not candidate[len(token):].strip():
                    fence_char, fence_length = None, 0
                    continue
        if fence_char is None:
            yield line


def parse_task(text):
    fields = {}
    for line in _task_machine_lines(text):
        match = FIELD.match(line)
        if match:
            if match[1] in fields:
                raise G1Error('DUPLICATE_FIELD')
            fields[match[1]] = match[2].strip()
    if any(not fields.get(key) for key in REQUIRED):
        raise G1Error('INVALID_TASK')
    if any(fields.get(key) not in allowed for key, allowed in ENUMS.items()):
        raise G1Error('INVALID_ENUM')
    if 'SCHEMA_VERSION' in fields and fields['SCHEMA_VERSION'] != PROFILE:
        raise G1Error('UNSUPPORTED_SCHEMA')
    if not TASK_REF.fullmatch(fields['TASK_ID']):
        raise G1Error('INVALID_TASK_ID')
    return fields

def document_kind(filename, text):
    if TASK_ID_LINE.search('\n'.join(_task_machine_lines(text))):
        return 'task_candidate'
    if TASK_NAME.match(filename):
        return 'legacy_candidate'
    return 'document'

def _items(value):
    if value.upper() in NONE_VALUES:
        return []
    return [item.strip() for item in re.split(r'[,;]', value) if item.strip()]

def _reference_diagnostics(root, filename, fields, task_ids):
    diagnostics = []
    for field in ('DEPENDENCIES', 'PREREQUISITES'):
        for reference in _items(fields[field]):
            if TASK_REF.fullmatch(reference):
                if reference.casefold() not in task_ids:
                    diagnostics.append((filename, 'MISSING_REFERENCE'))
            elif '/' not in reference and '\\' not in reference and not reference.lower().endswith(('.md','.json','.yaml','.yml')):
                diagnostics.append((filename, 'UNRESOLVED_PREREQUISITE'))
            else:
                try:
                    if not contained(root, reference).exists():
                        diagnostics.append((filename, 'MISSING_REFERENCE'))
                except G1Error:
                    diagnostics.append((filename, 'UNRESOLVED_PREREQUISITE' if field == 'PREREQUISITES' else 'INVALID_PATH'))
    for reference in _items(fields['EVIDENCE_PATHS']):
        try:
            if not contained(root, reference).is_file():
                diagnostics.append((filename, 'MISSING_REFERENCE'))
        except G1Error as exc:
            diagnostics.append((filename, str(exc)))
    return diagnostics

def _inspect_entries(root, entries):
    parsed, diagnostics, total, names = [], [], 0, set()
    for path in sorted(entries, key=lambda item: item.name.casefold()):
        name_key = path.name.casefold()
        if name_key in names:
            diagnostics.append((path.name, 'CASE_COLLISION'))
            continue
        names.add(name_key)
        try:
            contained(path.parent, path.name)
            if path.suffix.lower() != '.md':
                continue
            total += path.stat().st_size
            if total > MAX_TOTAL:
                raise G1Error('CORPUS_OVERSIZED')
            text = read_limited(path)
            kind = document_kind(path.name, text)
            if kind == 'document':
                continue
            if kind == 'legacy_candidate':
                diagnostics.append((path.name, 'LEGACY_TASK_FORMAT'))
                continue
            try:
                fields = parse_task(text)
            except G1Error as exc:
                if str(exc) == 'INVALID_TASK':
                    diagnostics.append((path.name, 'INCOMPLETE_TASK_SCHEMA'))
                    continue
                raise
            parsed.append((path.name, fields))
        except G1Error as exc:
            diagnostics.append((path.name, str(exc)))
        except (OSError, UnicodeError):
            diagnostics.append((path.name, 'UNREADABLE'))
    task_files, duplicate_ids = {}, set()
    for filename, fields in parsed:
        key = fields['TASK_ID'].casefold()
        if key in task_files:
            duplicate_ids.add(key)
        task_files.setdefault(key, []).append(filename)
    for key in duplicate_ids:
        diagnostics.extend((filename, 'DUPLICATE_TASK_ID') for filename in task_files[key])
    valid_ids = set(task_files) - duplicate_ids
    tasks = []
    for filename, fields in parsed:
        if fields['TASK_ID'].casefold() in duplicate_ids:
            continue
        errors = _reference_diagnostics(root, filename, fields, valid_ids)
        diagnostics.extend(errors)
        tasks.append((filename, fields))
    return tasks, diagnostics

def _workspace_metadata_diagnostics(root, manifest):
    """OPEN checks workspace metadata; IMPORT remains untrusted folder inspection."""
    metadata_path = contained(root, 'workspace.json')
    if not metadata_path.is_file():
        return [('workspace.json', 'MISSING_WORKSPACE_METADATA')]
    try:
        metadata = json.loads(read_limited(metadata_path, max_bytes=65536))
    except (G1Error, OSError, ValueError, TypeError):
        return [('workspace.json', 'INVALID_WORKSPACE_METADATA')]
    if not isinstance(metadata, dict) or set(metadata) != {'workspace_version', 'workspace_id', 'trusted_commit'}:
        return [('workspace.json', 'INVALID_WORKSPACE_METADATA')]
    if type(metadata['workspace_version']) is not int or metadata['workspace_version'] != WORKSPACE_VERSION:
        return [('workspace.json', 'UNSUPPORTED_WORKSPACE_VERSION')]
    try:
        uuid.UUID(metadata['workspace_id'])
    except (ValueError, TypeError, AttributeError):
        return [('workspace.json', 'INVALID_WORKSPACE_METADATA')]
    if metadata['trusted_commit'] != manifest['commit']:
        return [('workspace.json', 'INCOMPATIBLE_TRUST_VERSION')]
    return []


def inspect_workspace(root, bundle, require_metadata=False):
    manifest = verified_trust(bundle)
    root = safe_path(root)
    if not root.is_dir():
        raise G1Error('NOT_A_DIRECTORY')
    metadata_diagnostics = _workspace_metadata_diagnostics(root, manifest) if require_metadata else []
    task_root = contained(root, 'tasks')
    if not task_root.exists():
        return [], metadata_diagnostics + [('tasks', 'MISSING_REFERENCE')]
    if not task_root.is_dir():
        raise G1Error('INVALID_PATH')
    before = task_root.stat()
    entries = list(task_root.iterdir())
    after = task_root.stat()
    if (before.st_dev, before.st_ino, before.st_mtime_ns) != (after.st_dev, after.st_ino, after.st_mtime_ns):
        raise G1Error('CHANGED_DURING_READ')
    if len(entries) > MAX_TASKS:
        raise G1Error('TOO_MANY_TASKS')
    tasks, diagnostics = _inspect_entries(root, entries)
    return tasks, metadata_diagnostics + diagnostics

def inspect_import(path, bundle):
    verified_trust(bundle)
    selected = safe_path(path)
    if selected.is_dir():
        return inspect_workspace(selected, bundle)
    if not selected.is_file():
        raise G1Error('MISSING_OR_OVERSIZED')
    return _inspect_entries(selected.parent, [selected])

def create_workspace(dest, bundle):
    manifest = verified_trust(bundle)
    path = _absolute(dest)
    parent = safe_path(path.parent)
    if not parent.is_dir():
        raise G1Error('MISSING_PARENT')
    created = []
    try:
        os.mkdir(path)
        safe_path(path)
        root_identity = _path_identity(path)
        created.append((path, root_identity, False))
        tasks = path / 'tasks'
        os.mkdir(tasks)
        created.append((tasks, _path_identity(tasks), False))
        if _path_identity(path) != root_identity:
            raise G1Error('CHANGED_DURING_CREATE')
        payload = {'workspace_version': WORKSPACE_VERSION, 'workspace_id': str(uuid.uuid4()), 'trusted_commit': manifest['commit']}
        workspace = path / 'workspace.json'
        fd = os.open(workspace, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_BINARY', 0), 0o600)
        # Track the file immediately after exclusive creation so write/fsync errors
        # cannot strand a partially initialized workspace.
        try:
            created.append((workspace, _path_identity(workspace), True))
        except Exception:
            os.close(fd)
            try:
                workspace.unlink()
            except OSError:
                pass
            raise
        with os.fdopen(fd, 'wb') as stream:
            stream.write(json.dumps(payload, indent=2).encode('utf-8'))
            stream.flush()
            os.fsync(stream.fileno())
        safe_path(workspace)
        if _path_identity(path) != root_identity:
            raise G1Error('CHANGED_DURING_CREATE')
        return path
    except FileExistsError as exc:
        raise G1Error('DESTINATION_EXISTS') from exc
    except Exception:
        for item, identity, is_file in reversed(created):
            try:
                if _path_identity(item) == identity:
                    item.unlink() if is_file else item.rmdir()
            except OSError:
                pass
        raise
