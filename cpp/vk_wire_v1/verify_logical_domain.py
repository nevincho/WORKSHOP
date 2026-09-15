import json,pathlib,subprocess,sys
root=pathlib.Path(__file__).resolve().parents[2]
p=root/'evidence/VK-WIRE-05/cross_language_matrix.json'
exe=pathlib.Path(__file__).with_name('build')/'vk_wire_logical_probe'
results=[]
for kind in ('bytes','set','implementation_object'):
 r=subprocess.run([exe,kind],text=True,capture_output=True)
 results.append((kind,r.returncode,r.stdout.strip()))
ok=all(rc==2 and out=='INVALID_TYPE' for _,rc,out in results)
d=json.loads(p.read_text()); row=next(x for x in d['rows'] if x['vector_id']=='R05_PROHIBITED_VALUE')
row['cpp_result']='INVALID_TYPE' if ok else 'CONFORMANCE_INFRASTRUCTURE_DEFECT'; row['semantic_equality']=ok; row['pass']=ok; row['cpp_logical_domain_probes']=[{'kind':k,'returncode':rc,'result':out} for k,rc,out in results]
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('R05_LOGICAL_DOMAIN',results,'PASS' if ok else 'FAIL')
if not ok:sys.exit(1)
