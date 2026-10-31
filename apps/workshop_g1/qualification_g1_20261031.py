"""Isolated Windows G1 acceptance probes; intentionally exposes known unsafe CREATE paths.

Run only in disposable TemporaryDirectory. Never use customer paths.
A red test is a failed G1 acceptance invariant, not a test-harness failure by default.
"""
import csv
import json
import os
import platform
import subprocess
import sys
import tempfile
import tkinter as tk
import unittest
from pathlib import Path
from unittest import mock

from workshop_g1 import app, core
from windows_validation import snapshot, snapshot_digest

BUNDLE = Path(__file__).resolve().parent / 'workshop_g1' / 'trusted'


class G1BoundedQualification(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if os.name != 'nt':
            raise unittest.SkipTest('Actual Windows NTFS host required')
        print('HOST=' + platform.platform(), flush=True)
        print('PYTHON=' + sys.version.split()[0], flush=True)
        print('WINDOWS_SERVER_2022_IS_NOT_WINDOWS_10_11_CLIENT=True', flush=True)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='WORKSHOP_G1_QUAL_')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.manifest = core.verified_trust(BUNDLE)

    def workspace(self, name, metadata='valid'):
        root = self.root / name
        (root / 'tasks').mkdir(parents=True)
        (root / '.git').mkdir()
        (root / '.git' / 'config').write_bytes(b'[core]\nrepositoryformatversion = 0\n')
        (root / '.hidden').write_bytes(b'preserve hidden file')
        (root / 'tasks' / 'README.md').write_text('# inert data\n', encoding='utf-8')
        if metadata != 'missing':
            body = {'workspace_version': core.WORKSPACE_VERSION,
                    'workspace_id': 'e47a47b5-1fd5-472e-8d9f-3b7f93b8aa19',
                    'trusted_commit': self.manifest['commit']}
            if metadata == 'malformed':
                data = b'{ invalid JSON'
            else:
                if metadata == 'version':
                    body['workspace_version'] = 999
                if metadata == 'trust':
                    body['trusted_commit'] = '0' * 40
                data = json.dumps(body).encode('utf-8')
            (root / 'workspace.json').write_bytes(data)
        return root

    def test_strict_open_metadata_and_import_ntfs_snapshots(self):
        cases = {'valid': None, 'missing': 'MISSING_WORKSPACE_METADATA',
                 'malformed': 'INVALID_WORKSPACE_METADATA',
                 'version': 'UNSUPPORTED_WORKSPACE_VERSION',
                 'trust': 'INCOMPATIBLE_TRUST_VERSION'}
        for name, diagnostic in cases.items():
            with self.subTest(case=name):
                root = self.workspace('case_' + name, name)
                before = snapshot(root)
                rows, errors = core.inspect_workspace(root, BUNDLE, require_metadata=True)
                if diagnostic:
                    self.assertEqual(rows, [])
                    self.assertIn(('workspace.json', diagnostic), errors)
                else:
                    self.assertEqual(errors, [])
                after_open = snapshot(root)
                self.assertEqual(before, after_open, 'OPEN mutated NTFS file or metadata')
                imported_rows, imported_errors = core.inspect_import(root, BUNDLE)
                self.assertEqual(imported_rows, [])
                self.assertFalse(any(k == 'workspace.json' for k, _ in imported_errors))
                after_import = snapshot(root)
                self.assertEqual(before, after_import, 'IMPORT mutated NTFS file or metadata')
                self.assertIn('.git\\config', before)
                self.assertIn('.hidden', before)
                print('NTFS_STRICT_OPEN_IMPORT case=' + name +
                      ' diagnostic=' + str(diagnostic) +
                      ' BEFORE=' + snapshot_digest(before) +
                      ' AFTER_OPEN=' + snapshot_digest(after_open) +
                      ' AFTER_IMPORT=' + snapshot_digest(after_import), flush=True)

    def test_gui_trust_provenance_widget_contents_not_visual_acceptance(self):
        roots = []
        real_tk = tk.Tk

        def capture_root(*args, **kwargs):
            root = real_tk(*args, **kwargs)
            roots.append(root)
            return root

        try:
            with mock.patch.object(app.tk, 'Tk', side_effect=capture_root), \
                 mock.patch.object(real_tk, 'mainloop', lambda self: None):
                app.main()
            self.assertEqual(len(roots), 1)
            def descendants(widget):
                for child in widget.winfo_children():
                    yield child
                    yield from descendants(child)
            labels = []
            for child in descendants(roots[0]):
                try:
                    if child.winfo_class() == 'TLabel':
                        labels.append(str(child.cget('text')))
                except tk.TclError:
                    pass
            provenance = next((value for value in labels if value.startswith('Verified trust:')), None)
            self.assertIsNotNone(provenance, 'No provenance label constructed')
            self.assertIn(self.manifest['repository'], provenance)
            self.assertIn(self.manifest['commit'], provenance)
            for entry in self.manifest['files'].values():
                self.assertIn(entry['sha256'], provenance)
            print('GUI_PROVENANCE_WIDGET=PASS; ACTUAL_VISIBLE_RENDER_AND_HUMAN_INTERACTION=NOT_VERIFIED', flush=True)
        finally:
            for root in roots:
                root.destroy()

    def test_unreadable_acl_denial_and_recovery(self):
        root = self.workspace('acl')
        locked = root / 'tasks' / 'TASK-LOCK.md'
        original = b'TASK_ID: LOCKED\n'
        locked.write_bytes(original)
        user = subprocess.run(['whoami', '/user', '/fo', 'csv', '/nh'],
                              capture_output=True, text=True, check=True, timeout=15)
        sid = next(csv.reader(user.stdout.splitlines()))[1]
        before = locked.stat()
        grant = subprocess.run(['icacls', str(locked), '/deny', '*' + sid + ':(R)'],
                               capture_output=True, text=True, timeout=15)
        if grant.returncode:
            self.skipTest('ACL deny unavailable: ' + grant.stdout + grant.stderr)
        try:
            with self.assertRaises(OSError, msg='ACL fixture did not deny reading'):
                locked.read_bytes()
            rows, errors = core.inspect_workspace(root, BUNDLE, require_metadata=True)
            self.assertEqual(rows, [])
            self.assertIn(('TASK-LOCK.md', 'UNREADABLE'), errors)
            during = locked.stat()
            self.assertEqual((before.st_size, before.st_mtime_ns),
                             (during.st_size, during.st_mtime_ns))
            print('NTFS_ACL_UNREADABLE=REFUSED; CONTENT_SIZE_MTIME_UNCHANGED=True', flush=True)
        finally:
            revoke = subprocess.run(['icacls', str(locked), '/remove:d', '*' + sid],
                                    capture_output=True, text=True, timeout=15)
            self.assertEqual(revoke.returncode, 0, revoke.stdout + revoke.stderr)
        self.assertEqual(locked.read_bytes(), original)
        print('NTFS_ACL_RESTORED_AND_BYTES_IDENTICAL=True', flush=True)

    def test_create_early_root_failure_rolls_back_new_root(self):
        dest = self.root / 'early_failure'
        parent_before = snapshot(self.root)
        original_safe = core.safe_path

        def fail_after_mkdir(path):
            if Path(path) == dest:
                raise core.G1Error('INJECTED_ROOT_VALIDATION_FAILURE')
            return original_safe(path)

        with mock.patch.object(core, 'safe_path', side_effect=fail_after_mkdir):
            with self.assertRaisesRegex(core.G1Error, 'INJECTED_ROOT_VALIDATION_FAILURE'):
                core.create_workspace(dest, BUNDLE)
        print('CREATE_EARLY_ROOT_LEFT_BEHIND=' + str(dest.exists()), flush=True)
        self.assertFalse(dest.exists(), 'SOURCE_DEFECT: root created before it is registered for rollback')
        self.assertEqual(parent_before, snapshot(self.root))

    def test_create_identity_exception_must_preserve_foreign_replacement(self):
        dest = self.root / 'identity_failure'
        foreign = self.root / 'foreign-owned.txt'
        foreign.write_bytes(b'FOREIGN_OBJECT_MUST_SURVIVE')
        workspace = dest / 'workspace.json'
        original_identity = core._path_identity
        original_close = os.close
        replaced = []

        def fail_identity(path):
            if Path(path) == workspace:
                raise OSError('INJECTED_WORKSPACE_IDENTITY_FAILURE')
            return original_identity(path)

        def replace_after_close(fd):
            original_close(fd)
            if workspace.exists() and not replaced:
                # Inject the foreign replacement after the original descriptor
                # is closed, before any exception cleanup can unlink the path.
                os.replace(foreign, workspace)
                replaced.append(True)

        with mock.patch.object(core, '_path_identity', side_effect=fail_identity), \
             mock.patch.object(core.os, 'close', side_effect=replace_after_close):
            with self.assertRaisesRegex(OSError, 'INJECTED_WORKSPACE_IDENTITY_FAILURE'):
                core.create_workspace(dest, BUNDLE)
        self.assertTrue(replaced, 'Race interleaving did not reach cleanup')
        # os.replace MOVES the sentinel: its original pathname must disappear.
        # The preservation invariant is its bytes at the replacement pathname.
        print('CREATE_FOREIGN_REPLACEMENT_SURVIVES=' + str(workspace.exists()), flush=True)
        self.assertTrue(workspace.exists(),
                        'SOURCE_DEFECT: unverified cleanup deleted the foreign replacement')
        self.assertEqual(workspace.read_bytes(), b'FOREIGN_OBJECT_MUST_SURVIVE')


if __name__ == '__main__':
    unittest.main(verbosity=2)
