import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from workshop_g1 import core
from workshop_g1.core import G1Error, contained, create_workspace, inspect_import, inspect_workspace, parse_task, safe_display, safe_path, verified_trust, read_limited, REQUIRED

BUNDLE = Path(__file__).resolve().parents[1] / 'workshop_g1' / 'trusted'

def task(**change):
    f = {k:'sample' for k in REQUIRED}
    f.update(TASK_ID='TASK-01',PRIORITY='HIGH', STATUS='READY',EXECUTION_CLASS='WORKER',CODEX_ALLOWED='NO',DEPENDENCIES='NONE',PREREQUISITES='NONE',EVIDENCE_PATHS='NONE')
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

    def test_manifest_is_strict_and_compatible(self):
        b=self.root/'trusted';b.mkdir()
        for f in BUNDLE.iterdir(): (b/f.name).write_bytes(f.read_bytes())
        manifest=json.loads((b/'manifest.json').read_text())
        manifest['unknown']=True
        (b/'manifest.json').write_text(json.dumps(manifest))
        with self.assertRaisesRegex(G1Error,'UNSUPPORTED_SCHEMA'):verified_trust(b)
        manifest.pop('unknown');manifest['application']['workspace_versions']=[99]
        (b/'manifest.json').write_text(json.dumps(manifest))
        with self.assertRaisesRegex(G1Error,'INCOMPATIBLE_APPLICATION'):verified_trust(b)

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
        rows,errs=inspect_workspace(self.root,BUNDLE)
        self.assertEqual(rows,[])
        self.assertEqual([e[1] for e in errs].count('DUPLICATE_TASK_ID'),2)

    def test_references_and_safe_readiness(self):
        p=self.root/'tasks';p.mkdir()
        (p/'one.md').write_text(task(DEPENDENCIES='TASK-MISSING',EVIDENCE_PATHS='evidence/missing.md'))
        rows,errs=inspect_workspace(self.root,BUNDLE)
        self.assertEqual(rows[0][1]['DISPLAY_STATUS'],'NOT_READY')
        self.assertEqual([code for _,code in errs].count('MISSING_REFERENCE'),2)
        evidence=self.root/'evidence';evidence.mkdir();(evidence/'ok.md').write_text('proof')
        (p/'two.md').write_text(task(TASK_ID='TASK-02',DEPENDENCIES='TASK-01',EVIDENCE_PATHS='evidence/ok.md'))
        rows,errs=inspect_workspace(self.root,BUNDLE)
        two=next(fields for name,fields in rows if name=='two.md')
        self.assertEqual(two['DISPLAY_STATUS'],'READY')

    def test_invalid_reference_path(self):
        p=self.root/'tasks';p.mkdir();(p/'one.md').write_text(task(EVIDENCE_PATHS='../escape.md'))
        rows,errs=inspect_workspace(self.root,BUNDLE)
        self.assertEqual(rows[0][1]['DISPLAY_STATUS'],'NOT_READY')
        self.assertIn(('one.md','INVALID_PATH'),errs)

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

    def test_control_and_bidi_display_is_escaped(self):
        self.assertEqual(safe_display('safe\u202eevil\x07'),'safe\\u202eevil\\u0007')

    def test_missing_tasks_directory(self):
        rows,errs=inspect_workspace(self.root,BUNDLE)
        self.assertEqual(rows,[]);self.assertEqual(errs,[('tasks','MISSING_REFERENCE')])

    def test_individual_file_import(self):
        selected=self.root/'one.md';selected.write_text(task())
        before=selected.read_bytes()
        rows,errs=inspect_import(selected,BUNDLE)
        self.assertEqual((len(rows),errs),(1,[]))
        self.assertEqual(selected.read_bytes(),before)

    def test_create_failure_rolls_back_only_new_root(self):
        destination=self.root/'workspace'
        real_open=os.open
        def fail_workspace(path, flags, mode=0o777):
            if str(path).endswith('workspace.json'):
                raise OSError('injected failure')
            return real_open(path,flags,mode)
        with mock.patch('workshop_g1.core.os.open',side_effect=fail_workspace):
            with self.assertRaisesRegex(OSError,'injected failure'):
                create_workspace(destination,BUNDLE)
        self.assertFalse(destination.exists())

    def test_create_failure_never_deletes_foreign_object(self):
        destination=self.root/'workspace';real_open=os.open
        def inject_foreign(path,flags,mode=0o777):
            if str(path).endswith('workspace.json'):
                (destination/'foreign.txt').write_text('preserve')
                raise OSError('injected failure')
            return real_open(path,flags,mode)
        with mock.patch('workshop_g1.core.os.open',side_effect=inject_foreign):
            with self.assertRaisesRegex(OSError,'injected failure'):
                create_workspace(destination,BUNDLE)
        self.assertEqual((destination/'foreign.txt').read_text(),'preserve')

    def test_file_swap_between_check_and_open_fails_closed(self):
        selected=self.root/'selected.md';selected.write_text('original')
        real_identity=core._path_identity
        def swap_after_identity(path):
            identity=real_identity(path)
            selected.unlink();selected.write_text('replacement')
            return identity
        with mock.patch('workshop_g1.core._path_identity',side_effect=swap_after_identity):
            with self.assertRaisesRegex(G1Error,'CHANGED_DURING_READ'):
                read_limited(selected)

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
        if os.name != 'nt':
            self.skipTest('Real Windows required')
        outside=self.root/'outside';outside.mkdir();(outside/'secret.md').write_text('outside')
        selected=self.root/'selected';selected.mkdir();junction=selected/'tasks'
        result=subprocess.run(['cmd.exe','/d','/c','mklink','/J',str(junction),str(outside)],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        try:
            with self.assertRaisesRegex(G1Error,'UNSAFE_LINK'):
                inspect_workspace(selected,BUNDLE)
            self.assertEqual((outside/'secret.md').read_text(),'outside')
        finally:
            junction.rmdir()

if __name__=='__main__':unittest.main()
