import json
import os
import tempfile
import unittest
from pathlib import Path
from workshop_g1.core import G1Error, contained, create_workspace, inspect_workspace, parse_task, safe_path, verified_trust, read_limited, REQUIRED

BUNDLE = Path(__file__).resolve().parents[1] / 'workshop_g1' / 'trusted'

def task(**change):
    f = {k:'sample' for k in REQUIRED}
    f.update(TASK_ID='TASK-01',PRIORITY='HIGH', STATUS='READY',EXECUTION_CLASS='WORKER',CODEX_ALLOWED='NO')
    f.update(change)
    return '\n'.join(f'{k}: {v}' for k,v in f.items())

class G1Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_trusted_bundle(self):
        self.assertEqual(verified_trust(BUNDLE)['profile'], 'workshop-markdown-v1')

    def test_missing_trust(self):
        with self.assertRaises((G1Error,FileNotFoundError)): verified_trust(self.root)

    def test_changed_trust(self):
        b=self.root/'trusted';b.mkdir()
        for f in BUNDLE.iterdir(): (b/f.name).write_bytes(f.read_bytes())
        (b/'TASK_SCHEMA.md').write_text('tamper')
        with self.assertRaisesRegex(G1Error, 'TRUST_MODIFIED'):verified_trust(b)

    def test_create_explicit_and_existing_denied(self):
        p=self.root/'workspace';create_workspace(p,BUNDLE)
        self.assertEqual(sorted(x.name for x in p.iterdir()), ['tasks','workspace.json'])
        with self.assertRaisesRegex(G1Error,'DESTINATION_EXISTS'):create_workspace(p,BUNDLE)
        self.assertFalse((p/'.git').exists())

    def test_open_no_mutation(self):
        p=self.root/'workspace';create_workspace(p,BUNDLE)
        (p/'tasks'/'one.md').write_text(task())
        before={str(q.relative_to(p)):q.read_bytes() for q in p.rglob('*') if q.is_file()}
        rows,errs=inspect_workspace(p,BUNDLE)
        self.assertEqual(len(rows),1);self.assertEqual(errs,[])
        self.assertEqual(before,{str(q.relative_to(p)):q.read_bytes() for q in p.rglob('*') if q.is_file()})

    def test_missing_required(self):
        with self.assertRaisesRegex(G1Error,'INVALID_TASK'):parse_task('TASK_ID: X')

    def test_unsupported_schema(self):
        with self.assertRaisesRegex(G1Error,'UNSUPPORTED_SCHEMA'):parse_task(task(SCHEMA_VERSION='future-v99'))

    def test_duplicate_fields(self):
        with self.assertRaisesRegex(G1Error,'DUPLICATE_FIELD'):parse_task(task()+'\nTASK_ID: OTHER')

    def test_duplicate_task_ids(self):
        p=self.root/'tasks';p.mkdir()
        (p/'one.md').write_text(task());(p/'two.md').write_text(task())
        _,errs=inspect_workspace(self.root,BUNDLE)
        self.assertEqual([e[1] for e in errs].count('DUPLICATE_TASK_ID'),2)

    def test_invalid_paths(self):
        for s in ('../x','CON.md','file:name','.','bad/../../foo'):
            with self.subTest(s=s),self.assertRaisesRegex(G1Error,'INVALID_PATH'):contained(self.root,s)

    def test_symlinks(self):
        p=self.root/'tasks';p.mkdir(); target=self.root/'elsewhere';target.write_text(task())
        try: (p/'link.md').symlink_to(target)
        except (OSError,NotImplementedError):self.skipTest('symlinks unavailable')
        _,errs=inspect_workspace(self.root,BUNDLE)
        self.assertIn(('link.md','UNSAFE_LINK'),errs)

    def test_oversized_and_malformed(self):
        p=self.root/'tasks';p.mkdir();(p/'big.md').write_bytes(b'A'*(1024*1024+1));(p/'binary.md').write_bytes(b'\xff')
        _,errs=inspect_workspace(self.root,BUNDLE)
        self.assertEqual(len(errs),2)

    def test_injection_is_data(self):
        p=self.root/'tasks';p.mkdir();(p/'attack.md').write_text(task(OBJECTIVE='<script>alert(1)</script> ![image](https://example.invalid/secret)'))
        rows,errs=inspect_workspace(self.root,BUNDLE)
        self.assertEqual(len(rows),1)
        self.assertEqual(errs,[])
        self.assertIn('<script>',rows[0][1]['OBJECTIVE'])

    def test_missing_tasks_directory(self):
        rows,errs=inspect_workspace(self.root,BUNDLE)
        self.assertEqual(rows,[]);self.assertEqual(errs,[('tasks','MISSING_REFERENCE')])

    def test_document_not_invalid_task(self):
        p=self.root/'tasks';p.mkdir()
        (p/'README.md').write_text('# Notes\nThis is not a task.')
        (p/'TASK-OLD.md').write_text('# Legacy task without schema')
        (p/'partial.md').write_text('TASK_ID: PARTIAL\nPROJECT: Demo')
        (p/'valid.md').write_text(task(TASK_ID='T-2'))
        rows, errs=inspect_workspace(self.root,BUNDLE)
        self.assertEqual(len(rows),1)
        self.assertEqual(dict(errs), {'TASK-OLD.md':'LEGACY_TASK_FORMAT','partial.md':'INCOMPLETE_TASK_SCHEMA'})

    def test_document_with_command_is_inert(self):
        p=self.root/'tasks';p.mkdir()
        (p/'notes.md').write_text('# Documentation\n```sh\nrm -rf /\n```')
        rows, errs=inspect_workspace(self.root,BUNDLE)
        self.assertEqual((rows,errs),([],[]))

    def test_windows_reparse_attribute(self):
        self.skipTest('Requires real Windows NTFS junction/reparse fixture and post-snapshot')

if __name__=='__main__':unittest.main()
