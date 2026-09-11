import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {CANONICAL_CONCEPTS, STATES, buildViewModel, validateHealthContract, renderSystemHealth} from '../ui/system_health_v1.js';
const here=path.dirname(fileURLToPath(import.meta.url));
const fixture=n=>JSON.parse(fs.readFileSync(path.join(here,'..','fixtures',n),'utf8'));

test('current HB-04 output renders exactly 12 canonical concepts',()=>{
 const vm=buildViewModel(fixture('hb04_current_output.json'));
 assert.equal(vm.ok,true); assert.equal(vm.cards.length,12);
 assert.deepEqual(vm.cards.map(x=>x.concept),CANONICAL_CONCEPTS);
});

test('all six HB-04 states are accepted and preserved',()=>{
 const p=fixture('hb04_state_matrix_output.json');
 const seen=new Set(Object.values(p.concepts).map(x=>x.state));
 for(const s of STATES) assert.equal(seen.has(s),true,`state ${s} covered`);
 const vm=buildViewModel(p); assert.equal(vm.ok,true);
 for(const card of vm.cards) assert.equal(card.state,p.concepts[card.concept].state);
});

test('reason codes are preserved verbatim',()=>{
 const p=fixture('hb04_state_matrix_output.json'); const vm=buildViewModel(p);
 for(const card of vm.cards) assert.deepEqual(card.reasons,p.concepts[card.concept].reason_codes);
});

test('false-green presentation: NOT_VERIFIED does not become NOMINAL',()=>{
 const vm=buildViewModel(fixture('hb04_current_output.json'));
 for(const c of ['SYSTEM_CPU','SYSTEM_RAM','CPU_TEMPERATURE','RUNTIME_PERFORMANCE','CA_AUTHORITY_STATE','METRIC_HEALTH'])
   assert.equal(vm.cards.find(x=>x.concept===c).state,'NOT_VERIFIED');
});

test('false-green presentation: UNAVAILABLE/STALE/FAULT preserved',()=>{
 const vm=buildViewModel(fixture('hb04_state_matrix_output.json'));
 assert.equal(vm.cards.find(x=>x.concept==='SYSTEM_CPU').state,'UNAVAILABLE');
 assert.equal(vm.cards.find(x=>x.concept==='WIDE_PIPELINE_HEALTH').state,'STALE');
 assert.equal(vm.cards.find(x=>x.concept==='TELEMETRY_EDGE_HEALTH').state,'FAULT');
});

test('WIDE cumulative failures stays diagnostic only in UI',()=>{
 const p=fixture('hb04_current_output.json');
 p.concepts.WIDE_PIPELINE_HEALTH.values.failures=1;
 const vm=buildViewModel(p); const w=vm.cards.find(x=>x.concept==='WIDE_PIPELINE_HEALTH');
 assert.equal(w.state,'NOMINAL');
 assert.deepEqual(w.diagnostics.find(x=>x.key==='failures'),{key:'failures',value:1});
});

test('UI does not derive state from diagnostic values',()=>{
 const p=fixture('hb04_current_output.json');
 p.concepts.RUNTIME_PERFORMANCE.values.fps=0;
 p.concepts.RUNTIME_PERFORMANCE.state='NOT_VERIFIED';
 const vm=buildViewModel(p); assert.equal(vm.cards.find(x=>x.concept==='RUNTIME_PERFORMANCE').state,'NOT_VERIFIED');
});

test('missing concept contract is rejected, not synthesized',()=>{
 const p=fixture('hb04_current_output.json'); delete p.concepts.SYSTEM_RAM;
 const v=validateHealthContract(p); assert.equal(v.ok,false);
 assert.equal(v.errors.some(x=>x.includes('CANONICAL_CONCEPT_SET_MISMATCH')),true);
});

test('extra top-level concept contract is rejected',()=>{
 const p=fixture('hb04_current_output.json'); p.concepts.EXTRA={};
 assert.equal(validateHealthContract(p).ok,false);
});

test('invalid state contract is rejected',()=>{
 const p=fixture('hb04_current_output.json'); p.concepts.RUNTIME_HEALTH.state='GREEN';
 assert.equal(validateHealthContract(p).ok,false);
});

test('diagnostics selection is display-only and keeps supplied values',()=>{
 const vm=buildViewModel(fixture('hb04_current_output.json'));
 const edge=vm.cards.find(x=>x.concept==='TELEMETRY_EDGE_HEALTH');
 assert.deepEqual(edge.diagnostics.find(x=>x.key==='remote_ingest_status'),{key:'remote_ingest_status',value:'OFFLINE'});
 assert.equal(edge.state,'NOMINAL');
});

test('not_verified annotations preserved for operator context',()=>{
 const vm=buildViewModel(fixture('hb04_current_output.json'));
 const hq=vm.cards.find(x=>x.concept==='HQ_CAMERA_HEALTH');
 assert.equal(hq.notVerified.includes('HQ_FRAME_FRESHNESS'),true);
});

test('renderer emits exactly 12 concept cards with supplied states',()=>{
 const p=fixture('hb04_state_matrix_output.json');
 const root={classList:{add(){}},innerHTML:''};
 const vm=renderSystemHealth(root,p); assert.equal(vm.ok,true);
 assert.equal((root.innerHTML.match(/data-concept=/g)||[]).length,12);
 for(const item of Object.values(p.concepts)) assert.equal(root.innerHTML.includes(`state-${item.state}`),true);
});

test('renderer shows contract unavailable for invalid normalized input',()=>{
 const root={classList:{add(){}},innerHTML:''};
 const vm=renderSystemHealth(root,{schema:'BROKEN',concepts:{}});
 assert.equal(vm.ok,false); assert.equal(root.innerHTML.includes('System Health unavailable'),true);
 assert.equal(root.innerHTML.includes('state-NOMINAL'),false);
});
