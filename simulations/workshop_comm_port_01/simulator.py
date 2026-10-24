"""PORT-01 account-neutral, standard-library-only deterministic contract simulation.
No network, external executor, owner credential, or historical chat dependency.
"""
import hashlib
import json
from pathlib import Path

STATES = {'READY', 'IN_PROGRESS', 'REVIEW', 'COMPLETE', 'BLOCKED', 'REWORK', 'HOLD', 'HUMAN_GATE'}
TRANSITIONS = {
    'READY': {'IN_PROGRESS', 'HOLD', 'BLOCKED', 'HUMAN_GATE'},
    'IN_PROGRESS': {'REVIEW', 'BLOCKED', 'HUMAN_GATE'},
    'REVIEW': {'COMPLETE', 'REWORK', 'BLOCKED', 'HUMAN_GATE'},
    'REWORK': {'IN_PROGRESS', 'BLOCKED', 'HUMAN_GATE'},
    'BLOCKED': {'READY'}, 'HOLD': set(), 'HUMAN_GATE': set(), 'COMPLETE': set()
}

class Rejected(Exception):
    pass


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=True)


class Controller:
    def __init__(self, root, config):
        self.root = Path(root)
        self.config = config
        self.ledger = self.root / 'state' / 'events.json'
        self.allowed = set(config['writable_paths'])
        self.task = config['task']
        self.events = json.loads(self.ledger.read_text()) if self.ledger.exists() else []
        self._verify_chain()

    def _verify_chain(self):
        prev = 'GENESIS'
        for e in self.events:
            if e['previous'] != prev or e['hash'] != hashlib.sha256(canonical({'previous': prev, 'data': e['data']}).encode()).hexdigest():
                raise Rejected('corrupt event chain')
            prev = e['hash']

    def _write(self, rel, obj):
        if rel not in self.allowed or '..' in Path(rel).parts or Path(rel).is_absolute():
            raise Rejected('unauthorized file modification')
        target = self.root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(canonical(obj) + '\n')

    def _event(self, data):
        prev = self.events[-1]['hash'] if self.events else 'GENESIS'
        item = {'previous': prev, 'data': data,
                'hash': hashlib.sha256(canonical({'previous': prev, 'data': data}).encode()).hexdigest()}
        self._write('state/events.json', self.events + [item])
        self.events.append(item)

    @property
    def state(self):
        return self.events[-1]['data']['to'] if self.events else 'READY'

    def transition(self, dest, *, approved=False, prereq_ok=True, review_pass=False, checkpoint=None, unblock_verified=False):
        source = self.state
        if dest not in STATES or dest not in TRANSITIONS[source]:
            raise Rejected('invalid state transition')
        if source == 'BLOCKED' and dest == 'READY' and not unblock_verified:
            raise Rejected('blocker unresolved')
        if dest == 'IN_PROGRESS' and not prereq_ok:
            raise Rejected('missing prerequisite')
        if dest == 'COMPLETE' and (not review_pass or not checkpoint):
            raise Rejected('independent PASS and checkpoint required')
        if self.config['task']['human_gate'] and dest == 'IN_PROGRESS' and not approved:
            raise Rejected('human approval required')
        self._event({'type': 'transition', 'from': source, 'to': dest, 'task_id': self.task['id'], 'checkpoint': checkpoint})

    def executor(self, requested):
        if requested not in self.config['executors'] or requested not in self.config['allowed_executors']:
            raise Rejected('unapproved executor escalation')
        if self.config['executors'][requested]['paid']:
            raise Rejected('paid executor forbidden')
        return requested

    def run(self, *, credentials=True, prerequisites=True, scope='synthetic', approved=False):
        if not credentials:
            self.transition('BLOCKED')
            return 'BLOCKED'
        if not prerequisites:
            self.transition('BLOCKED')
            return 'BLOCKED'
        if scope != self.task['scope']:
            raise Rejected('scope expansion')
        ex = self.executor('mock')
        self.transition('IN_PROGRESS', approved=approved, prereq_ok=prerequisites)
        evidence = {'task_id': self.task['id'], 'executor': ex, 'result': 'SIMULATED', 'scope': scope}
        self._write('evidence/worker.json', evidence)
        self.transition('REVIEW')
        return 'REVIEW'

    def review(self, passed):
        if self.state != 'REVIEW':
            raise Rejected('review requires REVIEW state')
        evidence = json.loads((self.root / 'evidence/worker.json').read_text())
        accepted = passed and evidence == {'task_id': self.task['id'], 'executor': 'mock', 'result': 'SIMULATED', 'scope': self.task['scope']}
        self._write('review/verdict.json', {'passed': accepted, 'basis_sha256': hashlib.sha256(canonical(evidence).encode()).hexdigest()})
        if accepted:
            self._write('checkpoints/snapshot.json', {'task_id': self.task['id'], 'evidence_sha256': hashlib.sha256(canonical(evidence).encode()).hexdigest()})
            self.transition('COMPLETE', review_pass=True, checkpoint='checkpoints/snapshot.json')
        else:
            self.transition('REWORK')
        return self.state


def fixture():
    return {'customer': 'synthetic-customer', 'repository': 'synthetic/demo',
            'task': {'id': 'DEMO-001', 'scope': 'synthetic', 'human_gate': False},
            'executors': {'mock': {'paid': False}, 'codex': {'paid': True}},
            'allowed_executors': ['mock'],
            'writable_paths': ['state/events.json', 'evidence/worker.json', 'review/verdict.json', 'checkpoints/snapshot.json']}
