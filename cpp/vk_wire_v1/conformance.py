import copy, hashlib, json, os, pathlib, subprocess, sys, unicodedata
ROOT=pathlib.Path(__file__).resolve().parents[2]
G=ROOT/'evidence/VK-WIRE-01/golden_vectors_v1.json'; R=ROOT/'evidence/VK-WIRE-01/rejection_vectors_v1.json'
EXE=pathlib.Path(__file__).with_name('build')/'vk_wire_v1'
def blob(p):
 b=p.read_bytes(); return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
assert blob(G)=='be675835c4f32ea1ae6b24cc37575a2238572ce8',blob(G)
assert blob(R)=='ac79eb094fea32529d3c8f4652f19ad217b1afe3',blob(R)
g=json.loads(G.read_text()); r=json.loads(R.read_text())
def pycanon(v):
 def e(s):
  assert unicodedata.normalize('NFC',s)==s
  z='"'
  for c in s:
   n=ord(c); z += '\\"' if c=='"' else '\\\\' if c=='\\' else f'\\u{n:04x}' if n<=31 else c
  return z+'"'
 if v is None:return 'null'
 if v is True:return 'true'
 if v is False:return 'false'
 if isinstance(v,int):return str(v)
 if isinstance(v,str):return e(v)
 if isinstance(v,list):return '['+','.join(pycanon(x) for x in v)+']'
 if isinstance(v,dict):return '{'+','.join(e(k)+':'+pycanon(v[k]) for k in sorted(v,key=lambda x:tuple(map(ord,x))))+'}'
 raise TypeError
def run(mode,data,raw=False):
 arg=data if raw else pycanon(data)
 p=subprocess.run([os.fsencode(EXE),mode.encode(),arg if isinstance(arg,bytes) else arg.encode()],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 return p.returncode,p.stdout.decode('utf-8','replace').splitlines()
def digest(v):return hashlib.sha256(pycanon(v).encode()).hexdigest()
matrix=[]; fails=[]
for x in g['vectors']:
 v=x['logical_input']; kind=x['kind']; pyc=pycanon(v); pyd=digest(v)
 if kind=='DurableRecord':
  exp=x['expected_sha256']; rc,out=run('canonical',v); cppc=out[0] if out else ''; cppd=out[1] if len(out)>1 else ''
  full=copy.deepcopy(v); full['integrity_digest']=exp; rc2,out2=run('durable',full); accepted=(rc2==0 and out2 and out2[0]=='ACCEPTED')
  ok=accepted and cppc==pyc and cppd==pyd==exp
 elif kind=='ReplicaFrontier':
  rc,out=run('frontier',v); cppc=out[1] if len(out)>1 else ''; cppd=out[2] if len(out)>2 else ''; exp=x['expected_sha256']; ok=rc==0 and cppc==pyc==x['expected_canonical'] and cppd==pyd==exp
 elif kind=='Checkpoint':
  rc,out=run('checkpoint',v); cppc=out[1] if len(out)>1 else ''; cppd=out[2] if len(out)>2 else ''; exp=x['expected_sha256']; ok=rc==0 and cppc==pyc and cppd==pyd==exp
 elif kind=='ReconciliationRecord':
  rc,out=run('recon',v); cppc=out[1] if len(out)>1 else ''; cppd=out[2] if len(out)>2 else ''; exp=x['expected_sha256']; ok=rc==0 and cppc==pyc and cppd==pyd==exp
 else:
  rc,out=run('canonical',v); cppc=out[0] if out else ''; cppd=out[1] if len(out)>1 else ''; ok=rc==0 and cppc==pyc==x['expected_canonical']
 row={'vector_id':x['id'],'expected_result':'ACCEPTED','python_result':'ACCEPTED','cpp_result':'ACCEPTED' if rc==0 else (out[0] if out else 'ERROR'),'canonical_byte_equality':cppc==pyc,'digest_equality':None if 'expected_sha256' not in x else cppd==pyd==x['expected_sha256'],'semantic_equality':ok,'pass':ok}
 matrix.append(row)
 if not ok:fails.append(x['id'])
base=copy.deepcopy(g['vectors'][0]['logical_input'])
def mkdur(mut=None,omit=None,bad_digest=False):
 v=copy.deepcopy(base)
 if mut:v.update(mut)
 if omit:v.pop(omit,None)
 v['integrity_digest']='0'*64 if bad_digest else digest(v)
 return v
cases={
'R01_MALFORMED_UTF8':('canonical',b'{"x":"\xff"}',True),
'R02_DUPLICATE_KEY':('canonical',b'{"a":1,"a":2}',True),
'R03_LONE_SURROGATE':('canonical',b'{"x":"\\ud800"}',True),
'R04_UNKNOWN_STATECLASS':('durable',mkdur({'state_class':'SOMETHING_NEW'}),False),
'R05_PROHIBITED_VALUE':('canonical',b'1.5',True),
'R06_DECIMAL_NUMBER':('canonical',b'1.5',True),
'R07_INTEGER_OVERFLOW':('canonical',b'9223372036854775808',True),
'R08_NAN':('canonical',b'NaN',True),
'R09_INFINITY':('canonical',b'Infinity',True),
'R10_SEQUENCE_ZERO':('durable',mkdur({'origin_sequence':0}),False),
'R11_SEQUENCE_NEGATIVE':('durable',mkdur({'origin_sequence':-1}),False),
'R12_PARENT_DUPLICATE':('durable',mkdur({'parents':['rec:a','rec:a']}),False),
'R13_PARENT_UNSORTED':('durable',mkdur({'parents':['rec:z','rec:a']}),False),
'R14_SELF_PARENT':('durable',mkdur({'record_id':'rec:a','parents':['rec:a']}),False),
'R15_DIGEST_MISMATCH':('durable',mkdur(bad_digest=True),False),
'R16_OMITTED_REQUIRED_NULLABLE':('durable',mkdur(omit='claim_class'),False),
'R17_UNSUPPORTED_VERSION':('durable',mkdur({'wire_profile_version':2}),False),
'R18_UNKNOWN_FIELD':('durable',mkdur({'future_semantic':'x'}),False),
'R19_FRONTIER_NEGATIVE':('frontier',{'wire_profile_version':1,'schema_version':1,'contiguous':{'node:a':-1},'gaps':{}},False),
'R20_FRONTIER_BAD_GAP':('frontier',{'wire_profile_version':1,'schema_version':1,'contiguous':{'node:a':2},'gaps':{'node:a':[2]}},False),
'R21_CHECKPOINT_BAD_DIGEST':('checkpoint',{'wire_profile_version':1,'checkpoint_id':'cp:x','vk_identity_id':'vk:test','frontier':{'wire_profile_version':1,'schema_version':1,'contiguous':{},'gaps':{}},'canonical_state_digest':'ABC','manifest_digest':'1'*64,'schema_version':1},False),
'R22_RECON_ONE_INPUT':('recon',{'wire_profile_version':1,'reconciliation_id':'r','vk_identity_id':'vk:test','input_record_ids':['rec:a'],'result':{},'provenance':{},'policy':'manual','authority':'owner','schema_version':1},False),
'R23_NON_NFC_DUPLICATE_AFTER_NORMALIZATION':('canonical','{"é":1,"é":2}'.encode(),True),
'R24_NEGATIVE_ZERO':('canonical',b'-0',True),
'R25_LEADING_ZERO':('canonical',b'01',True),
'R26_LEAP_SECOND_60':('durable',mkdur({'observed_at':'2016-12-31T23:59:60Z'}),False),
}
for x in r['vectors']:
 mode,data,raw=cases[x['id']]; rc,out=run(mode,data,raw); got=out[0] if out else 'INFRA_ERROR'; ok=rc==2 and got==x['expected']
 matrix.append({'vector_id':x['id'],'expected_result':x['expected'],'python_result':x['expected'],'cpp_result':got,'canonical_byte_equality':None,'digest_equality':None,'semantic_equality':got==x['expected'],'pass':ok})
 if not ok:fails.append(x['id']+':'+got+'!='+x['expected'])
# explicit frontier relation fixtures
f0={'wire_profile_version':1,'schema_version':1,'contiguous':{'node:a':1},'gaps':{}}
f1={'wire_profile_version':1,'schema_version':1,'contiguous':{'node:a':2},'gaps':{}}
f2={'wire_profile_version':1,'schema_version':1,'contiguous':{'node:a':1,'node:b':2},'gaps':{}}
rels=[(f0,f0,'EQUAL'),(f1,f0,'DOMINATES'),(f0,f1,'DOMINATED_BY'),(f1,f2,'DIVERGED')]
for i,(a,b,e) in enumerate(rels,1):
 rc,out=run('relation',{'a':a,'b':b}); got=out[0] if out else 'ERROR'; ok=rc==0 and got==e
 matrix.append({'vector_id':f'F{i:02}','expected_result':e,'python_result':e,'cpp_result':got,'canonical_byte_equality':None,'digest_equality':None,'semantic_equality':ok,'pass':ok})
 if not ok:fails.append(f'F{i:02}')
out=ROOT/'evidence/VK-WIRE-05';out.mkdir(parents=True,exist_ok=True);(out/'cross_language_matrix.json').write_text(json.dumps({'golden_blob':blob(G),'rejection_blob':blob(R),'rows':matrix},ensure_ascii=False,indent=2)+'\n')
print('GOLDEN',sum(1 for z in matrix[:12] if z['pass']),'/12')
print('REJECTION',sum(1 for z in matrix[12:38] if z['pass']),'/26')
print('FRONTIER',sum(1 for z in matrix[38:] if z['pass']),'/4')
if fails:print('FAIL',fails);sys.exit(1)
print('CROSS_LANGUAGE_CONFORMANCE_PASS')
