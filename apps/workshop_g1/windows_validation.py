"""Windows-only G1 qualification using disposable temporary directories."""
import hashlib
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from workshop_g1.core import G1Error, create_workspace, inspect_import, inspect_workspace, safe_path

BUNDLE = Path(__file__).resolve().parent / 'workshop_g1' / 'trusted'

def snapshot(root):
    result = {}
    for base, dirs, files in os.walk(root, followlinks=False):
        for name in dirs + files:
            path = Path(base) / name
            info = path.lstat()
            result[str(path.relative_to(root))] = (
                info.st_mode, info.st_size, info.st_mtime_ns, info.st_file_attributes,
                hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() and not path.is_symlink() else None,
            )
    return result

class WindowsQualification(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if os.name != 'nt':
            raise unittest.SkipTest('Real Windows required')

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='WORKSHOP_G1_WIN_TEST_')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_create_exact_files_repeat_and_failure_rollback(self):
        workspace = self.root / 'new'
        create_workspace(workspace, BUNDLE)
        self.assertEqual({path.name for path in workspace.iterdir()}, {'workspace.json','tasks'})
        before = snapshot(workspace)
        with self.assertRaisesRegex(G1Error, 'DESTINATION_EXISTS'):
            create_workspace(workspace, BUNDLE)
        self.assertEqual(before, snapshot(workspace))
        failed = self.root / 'failed'
        real_open = os.open
        def injected(path, flags, mode=0o777):
            if str(path).endswith('workspace.json'):
                raise OSError('injected failure')
            return real_open(path, flags, mode)
        with mock.patch('workshop_g1.core.os.open', side_effect=injected):
            with self.assertRaisesRegex(OSError, 'injected failure'):
                create_workspace(failed, BUNDLE)
        self.assertFalse(failed.exists())

    def test_open_and_file_import_no_mutation(self):
        selected = self.root / 'selected'
        (selected / 'tasks').mkdir(parents=True)
        (selected / '.git').mkdir()
        (selected / '.git' / 'config').write_bytes(b'[core]\nrepositoryformatversion = 0\n')
        document = selected / 'tasks' / 'README.md'
        document.write_bytes(b'# inert document\n')
        before = snapshot(selected)
        inspect_workspace(selected, BUNDLE)
        inspect_import(document, BUNDLE)
        self.assertEqual(before, snapshot(selected))

    def test_junction_escape_denied_without_outside_mutation(self):
        outside = self.root / 'outside';outside.mkdir()
        secret = outside / 'secret.md';secret.write_text('do not traverse', encoding='utf-8')
        selected = self.root / 'selected';selected.mkdir();junction = selected / 'tasks'
        result = subprocess.run(['cmd.exe','/d','/c','mklink','/J',str(junction),str(outside)],capture_output=True,text=True,timeout=10)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        before = snapshot(outside)
        try:
            with self.assertRaisesRegex(G1Error,'UNSAFE_LINK'):
                inspect_workspace(selected,BUNDLE)
            self.assertEqual(before,snapshot(outside))
        finally:
            junction.rmdir()

    def test_file_symlink_denied_if_available(self):
        selected = self.root / 'selected';task_root = selected / 'tasks';task_root.mkdir(parents=True)
        outside = self.root / 'outside.md';outside.write_text('TASK_ID: SECRET',encoding='utf-8')
        link = task_root / 'linked.md'
        try:
            link.symlink_to(outside)
        except (OSError,NotImplementedError):
            self.skipTest('Windows file symlinks unavailable without privileges/Developer Mode')
        rows,errors = inspect_workspace(selected,BUNDLE)
        self.assertEqual(rows,[])
        self.assertIn(('linked.md','UNSAFE_LINK'),errors)
        self.assertEqual(outside.read_text(encoding='utf-8'),'TASK_ID: SECRET')

    def test_root_swap_during_enumeration_fails_closed(self):
        selected = self.root / 'selected';task_root = selected / 'tasks';task_root.mkdir(parents=True)
        (task_root / 'README.md').write_text('# original')
        original_iterdir = Path.iterdir
        swapped = False
        def swap(path):
            nonlocal swapped
            if path == task_root and not swapped:
                swapped = True
                path.rename(selected / 'old_tasks')
                path.mkdir()
                (path / 'README.md').write_text('# replacement')
            return original_iterdir(path)
        with mock.patch.object(Path,'iterdir',swap):
            with self.assertRaisesRegex(G1Error,'CHANGED_DURING_READ'):
                inspect_workspace(selected,BUNDLE)

    def test_unc_and_device_paths_denied(self):
        for path in (r'\\server\share\x',r'\\?\C:\Windows',r'\\.\C:\Windows'):
            with self.subTest(path=path), self.assertRaisesRegex(G1Error,'UNSAFE_NETWORK_PATH'):
                safe_path(path)

if __name__ == '__main__':
    unittest.main(verbosity=2)
