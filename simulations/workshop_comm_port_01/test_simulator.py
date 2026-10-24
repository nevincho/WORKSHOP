"""Bounded simulation tests; do not assert third-party account integration."""
import json
import tempfile
import unittest
from pathlib import Path
from simulator import Controller, Rejected, fixture

class ContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.cfg = fixture()
        self.ctl = Controller(self.root, self.cfg)

    def test_positive_resume(self):
        self.assertEqual(self.ctl.run(), 'REVIEW')
        restarted = Controller(self.root, json.loads(json.dumps(self.cfg)))
        self.assertEqual(restarted.state, 'REVIEW')
        self.assertEqual(restarted.review(True), 'COMPLETE')
        self.assertEqual(Controller(self.root, self.cfg).state, 'COMPLETE')
        self.assertEqual(len(Controller(self.root, self.cfg).events), 3)

    def test_unauthorized_file(self):
        with self.assertRaisesRegex(Rejected, 'unauthorized'):
            self.ctl._write('policies/AUTONOMY_POLICY.md', {'tamper': True})
        self.assertFalse((self.root / 'policies').exists())

    def test_missing_credentials(self):
        self.assertEqual(self.ctl.run(credentials=False), 'BLOCKED')

    def test_missing_prerequisite(self):
        self.assertEqual(self.ctl.run(prerequisites=False), 'BLOCKED')

    def test_scope_expansion(self):
        with self.assertRaisesRegex(Rejected, 'scope expansion'):
            self.ctl.run(scope='real-repository')

    def test_invalid_transition(self):
        with self.assertRaisesRegex(Rejected, 'invalid state transition'):
            self.ctl.transition('COMPLETE', review_pass=True, checkpoint='fake')

    def test_interruption_resume(self):
        self.ctl.transition('IN_PROGRESS')
        self.assertEqual(Controller(self.root, self.cfg).state, 'IN_PROGRESS')
        with self.assertRaisesRegex(Rejected, 'invalid state transition'):
            Controller(self.root, self.cfg).run()

    def test_failed_review(self):
        self.ctl.run()
        self.assertEqual(self.ctl.review(False), 'REWORK')

    def test_escalation_denied(self):
        with self.assertRaisesRegex(Rejected, 'unapproved executor'):
            self.ctl.executor('codex')

    def test_human_gate(self):
        self.cfg['task']['human_gate'] = True
        with self.assertRaisesRegex(Rejected, 'human approval'):
            self.ctl.run()
        self.assertEqual(Controller(self.root, self.cfg).state, 'READY')

    def test_blocker_requires_explicit_verification(self):
        self.ctl.transition('BLOCKED')
        with self.assertRaisesRegex(Rejected, 'blocker unresolved'):
            self.ctl.transition('READY')
        self.ctl.transition('READY', unblock_verified=True)

    def test_chain_tamper_detected(self):
        self.ctl.transition('BLOCKED')
        f = self.root / 'state/events.json'
        e = json.loads(f.read_text())
        e[0]['data']['to'] = 'COMPLETE'
        f.write_text(json.dumps(e))
        with self.assertRaisesRegex(Rejected, 'corrupt event chain'):
            Controller(self.root, self.cfg)

if __name__ == '__main__':
    unittest.main(verbosity=2)
