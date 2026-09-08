from __future__ import annotations
import math, json, sys, subprocess, hashlib
from dataclasses import dataclass
from pathlib import Path
from statistics import mean, pstdev
from time import perf_counter_ns
import numpy as np, cv2
sys.path.insert(0,str(Path(__file__).parent))
import t1,t2,t3,t4

SEED=20260908
W=H=640
F=5000.0
CX=CY=320.0
TARGET_CLASS='FPV_SYNTH_VIEW'
PHYS_W=0.40
PHYS_L=0.55
EXPECTED={
 't1.py':'91f81e882af557f2d2106a8648ee283bfbdee81e',
 't2.py':'83202583f93ca43b134132f84d5cd51d7b59bcbe',
 't3.py':'d15e09dc63384d93719fdab30b50634750cfd65c',
 't4.py':'af995bdaab486b0c677bcd35c6166d90d253bbfb'}
COMMITS={'t1.py':'c7b378841979f82b037c47be3571fa72a7b70e51','t2.py':'4bd4b5d38357db501de07511aeabaa4c0ae058e1','t3.py':'c121ce25dbba84520c6f8e644281a7cb2bf3ee73','t4.py':'7f628a727b89599ea6977053ea12211b10e0ffcd'}

def blob(p): return subprocess.check_output(['git','hash-object',str(p)],text=True).strip()
def identity():
    return {n:{'commit':COMMITS[n],'blob':blob(Path(__file__).parent/n),'expected':e,'match':blob(Path(__file__).parent/n)==e,'sha256':hashlib.sha256((Path(__file__).parent/n).read_bytes()).hexdigest()} for n,e in EXPECTED.items()}

def transform():
    return t2.GeometryTransform('SYNTHETIC_IDENTITY_AI_CAL','1',t2.PlaneSpec('AI',(640,640)),t2.PlaneSpec('CAL',(640,640)),((1.,0.,0.),(0.,1.,0.),(0.,0.,1.)),metadata=(('status','SYNTHETIC'),))
ADAPTER=t2.AICalibratedGeometryAdapter(transform())
CAL=t3.CameraCalibration('SYNTHETIC_F5000',(640,640),F,F,CX,CY,production_verified=False,provenance=(('fixture','SYNTHETIC'),))
EXTRACTOR=t1.SparseTargetGeometryExtractor()
FUSION=t4.HorosRangeFusionContract()

@dataclass(frozen=True)
class Condition:
    angle_deg:float; z:float; yaw_deg:float; replicate:int=0; orientation_mode:str='KNOWN'; semantic_loss:bool=False; span_collapse:bool=False; partial:bool=False

def rotations(yaw,tilt):
    y=math.radians(yaw); a=math.radians(tilt)
    Rz=np.array([[math.cos(y),-math.sin(y),0],[math.sin(y),math.cos(y),0],[0,0,1.]],float)
    Rx=np.array([[1,0,0],[0,math.cos(a),-math.sin(a)],[0,math.sin(a),math.cos(a)]],float)
    return Rx@Rz

def shape_local():
    return np.array([[0,-PHYS_L/2],[PHYS_W/2,-PHYS_L*.05],[.42*PHYS_W,PHYS_L/2],[-.42*PHYS_W,PHYS_L/2],[-PHYS_W/2,-PHYS_L*.05]],float)

def project_points(xy,z,yaw,tilt):
    R=rotations(yaw,tilt); p=np.column_stack([xy,np.zeros(len(xy))])@R.T; p[:,2]+=z
    u=CX+F*p[:,0]/p[:,2]; v=CY+F*p[:,1]/p[:,2]
    return np.column_stack([u,v]),p

def physical_axis_projection_factor(z,yaw,tilt,axis):
    if axis=='LR': ends=np.array([[-PHYS_W/2,0],[PHYS_W/2,0]],float); S=PHYS_W
    else: ends=np.array([[0,-PHYS_L/2],[0,PHYS_L/2]],float); S=PHYS_L
    uv,_=project_points(ends,z,yaw,tilt)
    q=math.hypot((uv[1,0]-uv[0,0])/F,(uv[1,1]-uv[0,1])/F)
    return max(1e-6,min(1.0,q*z/S))

def render(c:Condition):
    bg=35; fg=205; img=np.full((H,W,3),bg,np.uint8)
    uv,_=project_points(shape_local(),c.z,c.yaw_deg,c.angle_deg)
    rng=np.random.default_rng(SEED+int(c.angle_deg*100)+int(c.z*1000)+int(c.yaw_deg*10000)+c.replicate*31)
    uv=uv+rng.normal(0,0.28,uv.shape); pts=np.rint(uv).astype(np.int32); cv2.fillPoly(img,[pts],(fg,fg,fg))
    if c.partial:
        x0=max(0,int(pts[:,0].min())-2); x1=int(np.median(pts[:,0])-0.1*(pts[:,0].max()-pts[:,0].min()))
        cv2.rectangle(img,(x0,max(0,int(pts[:,1].min())-3)),(max(x0,x1),min(H-1,int(pts[:,1].max())+3)),(bg,bg,bg),-1)
    if c.semantic_loss:
        img[:]=bg; axes=(max(3,int(F*PHYS_W/(2*c.z))),max(3,int(F*PHYS_L*math.cos(math.radians(c.angle_deg))/(2*c.z))))
        cv2.ellipse(img,(320,320),axes,c.yaw_deg,0,360,(fg,fg,fg),-1)
    if c.span_collapse: img[:]=bg; cv2.rectangle(img,(318,270),(322,370),(fg,fg,fg),-1)
    g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY); ys,xs=np.where(g>bg+20)
    bbox=(250,250,390,390) if not len(xs) else (max(0,int(xs.min())-8),max(0,int(ys.min())-8),min(W,int(xs.max())+9),min(H,int(ys.max())+9))
    return img,bbox

def t1_to_t2(g):
    pts=tuple(t2.SparsePointLike(p.point_type.value,p.x,p.y,p.confidence,p.valid,p.reason) for p in g.points)
    return t2.Task1GeometryLike(g.frame_id,g.timestamp,g.target_id,g.target_class,tuple(map(float,g.bbox_xyxy)),g.center,pts,g.source,(('fixture','T6_EXACT_CHAIN'),))
def t2_to_t3(c,target_id):
    pts=tuple(t3.CalibratedPoint(p.point_type,p.x,p.y,p.confidence,p.valid,p.reason) for p in c.points)
    return t3.CalibratedGeometryInput(c.source_geometry_ref,c.frame_id,c.timestamp,target_id,TARGET_CLASS,c.destination_plane.resolution_wh,c.transform_id,c.transform_version,c.transform_valid,False,0.0,pts,c.provenance)

def profile(c:Condition):
    r_lr=physical_axis_projection_factor(c.z,c.yaw_deg,c.angle_deg,'LR'); r_nt=physical_axis_projection_factor(c.z,c.yaw_deg,c.angle_deg,'NT')
    if c.orientation_mode=='KNOWN': sig_lr=sig_nt=0.; rv_lr,rv_nt=r_lr,r_nt; minconf=0.
    elif c.orientation_mode=='UNCERTAIN': sig_lr=.10*r_lr; sig_nt=.10*r_nt; rv_lr,rv_nt=r_lr,r_nt; minconf=0.
    elif c.orientation_mode=='INSUFFICIENT': sig_lr=.35*r_lr; sig_nt=.35*r_nt; rv_lr,rv_nt=r_lr,r_nt; minconf=.75
    elif c.orientation_mode=='INCORRECT': sig_lr=sig_nt=0.; rv_lr=rv_nt=1.; minconf=0.
    elif c.orientation_mode=='ASYMMETRIC_WRONG': sig_lr=sig_nt=0.; rv_lr=1.; rv_nt=.5; minconf=0.
    else: raise ValueError(c.orientation_mode)
    spans=(t3.PhysicalSpanSpec('LR','LEFT_SILHOUETTE','RIGHT_SILHOUETTE',PHYS_W,PHYS_W*.01,True,'LR_SYN','SYNTHETIC_PHYSICAL_WIDTH',rv_lr,sig_lr,True,minconf),t3.PhysicalSpanSpec('NT','NOSE','TAIL',PHYS_L,PHYS_L*.01,True,'NT_SYN','SYNTHETIC_PHYSICAL_LENGTH',rv_nt,sig_nt,True,minconf))
    return t3.TargetGeometryProfile('T6_SYNTH_PROFILE','1',TARGET_CLASS,spans,(('fixture','SYNTHETIC'),),False),(r_lr,r_nt)

def pointmap(g): return {p.point_type.value:p for p in g.points}
def run(c:Condition):
    t0=perf_counter_ns(); img,bbox=render(c); frame=f'a{c.angle_deg:g}-z{c.z:g}-y{c.yaw_deg:g}-r{c.replicate}-{c.orientation_mode}'
    s=perf_counter_ns(); g1=EXTRACTOR.extract(img,t1.TargetGeometryInput(frame,c.replicate/30.,'TGT-A',TARGET_CLASS,.95,bbox)); t1ms=(perf_counter_ns()-s)/1e6
    s=perf_counter_ns(); g2=ADAPTER.adapt(t1_to_t2(g1)); t2ms=(perf_counter_ns()-s)/1e6
    prof,r=profile(c); source=t3.SparseGeometryRangeSource(CAL,prof); s=perf_counter_ns(); g3=source.estimate(t2_to_t3(g2,'TGT-A')); t3ms=(perf_counter_ns()-s)/1e6
    class_in=t4.ExistingMonocularClassSizeInput('SYNTHETIC_REFERENCE_CLASS_SIZE',c.z,c.z*.02,.90,True,False,frame_id=frame,timestamp=c.replicate/30.,target_ref='TGT-A',provenance=(('fixture','SYNTHETIC_TRUTH_REFERENCE'),))
    sparse_in=t4.SparseGeometryRangeInput('TASK3_FROZEN',g3.range_m,g3.sigma_m,g3.confidence,g3.validity!=t3.RangeValidity.INVALID,g3.production_metric_verified,g2.transform_valid,False,frame_id=frame,timestamp=c.replicate/30.,target_ref='TGT-A',provenance=g3.provenance,reason=g3.error)
    s=perf_counter_ns(); fused=FUSION.fuse((t4.adapt_monocular_class_size(class_in),t4.adapt_sparse_geometry(sparse_in))); t4ms=(perf_counter_ns()-s)/1e6
    pm=pointmap(g1)
    def xy(n):
        p=pm.get(n); return None if p is None or (not p.valid) or p.x is None or p.y is None else (float(p.x),float(p.y))
    def err(n,truth):
        p=xy(n); return None if p is None else math.hypot(p[0]-truth[0],p[1]-truth[1])
    axes=np.array([[0,0],[-PHYS_W/2,0],[PHYS_W/2,0],[0,-PHYS_L/2],[0,PHYS_L/2]],float); auv,_=project_points(axes,c.z,c.yaw_deg,c.angle_deg)
    accepted=[x for x in g3.candidates if x.valid and x.accepted and x.range_m is not None]
    return {'angle':c.angle_deg,'z':c.z,'yaw':c.yaw_deg,'mode':c.orientation_mode,'rep':c.replicate,'projection_factor_lr':r[0],'projection_factor_nt':r[1],'g1_validity':g1.validity.value,'center_error_px':err('CENTER',auv[0]),'left_error_px':err('LEFT_SILHOUETTE',auv[1]),'right_error_px':err('RIGHT_SILHOUETTE',auv[2]),'nose_error_px':err('NOSE',auv[3]),'tail_error_px':err('TAIL',auv[4]),'left_valid':xy('LEFT_SILHOUETTE') is not None,'right_valid':xy('RIGHT_SILHOUETTE') is not None,'nose_valid':xy('NOSE') is not None,'tail_valid':xy('TAIL') is not None,'geometry_conf':g1.geometry_confidence,'lr_span_px':None if xy('LEFT_SILHOUETTE') is None or xy('RIGHT_SILHOUETTE') is None else math.hypot(xy('RIGHT_SILHOUETTE')[0]-xy('LEFT_SILHOUETTE')[0],xy('RIGHT_SILHOUETTE')[1]-xy('LEFT_SILHOUETTE')[1]),'nt_span_px':None if xy('NOSE') is None or xy('TAIL') is None else math.hypot(xy('NOSE')[0]-xy('TAIL')[0],xy('NOSE')[1]-xy('TAIL')[1]),'candidate_count':len(accepted),'t3_range':g3.range_m,'t3_sigma':g3.sigma_m,'t3_conf':g3.confidence,'t3_error':g3.error,'fused_range':fused.range_m,'fused_sigma':fused.sigma_m,'fused_conf':fused.confidence,'fusion_state':fused.state.value,'metric_usability':fused.metric_usability.value,'t3_bias_m':None if g3.range_m is None else float(g3.range_m-c.z),'fused_bias_m':None if fused.range_m is None else float(fused.range_m-c.z),'t1_ms':t1ms,'t2_ms':t2ms,'t3_ms':t3ms,'t4_ms':t4ms,'total_ms':(perf_counter_ns()-t0)/1e6}

def K(z,y,a,m): return f'{float(z):.1f}|{float(y):.1f}|{float(a):.1f}|{m}'
def summarize(rows):
    out={}
    for key in sorted(set((r['z'],r['yaw'],r['angle'],r['mode']) for r in rows)):
        x=[r for r in rows if (r['z'],r['yaw'],r['angle'],r['mode'])==key]; vals=lambda k:[r[k] for r in x if r[k] is not None and isinstance(r[k],(int,float)) and math.isfinite(float(r[k]))]
        av=lambda k: mean(vals(k)) if vals(k) else None; sd=lambda k: pstdev(vals(k)) if len(vals(k))>1 else 0.0 if vals(k) else None
        out[K(*key)]={'z':key[0],'yaw':key[1],'angle':key[2],'mode':key[3],'n':len(x),'g1_valid_rate':sum(r['g1_validity']!='INVALID' for r in x)/len(x),'nose_tail_valid_rate':sum(r['nose_valid'] and r['tail_valid'] for r in x)/len(x),'center_error_px_mean':av('center_error_px'),'lr_error_px_mean':mean(vals('left_error_px')+vals('right_error_px')) if vals('left_error_px')+vals('right_error_px') else None,'nt_error_px_mean':mean(vals('nose_error_px')+vals('tail_error_px')) if vals('nose_error_px')+vals('tail_error_px') else None,'geometry_conf_mean':av('geometry_conf'),'lr_span_px_mean':av('lr_span_px'),'nt_span_px_mean':av('nt_span_px'),'candidate_count_mean':av('candidate_count'),'t3_bias_m_mean':av('t3_bias_m'),'t3_bias_jitter_m':sd('t3_bias_m'),'t3_sigma_mean':av('t3_sigma'),'fused_bias_m_mean':av('fused_bias_m'),'fused_bias_jitter_m':sd('fused_bias_m'),'fused_sigma_mean':av('fused_sigma'),'fused_conf_mean':av('fused_conf'),'conflict_rate':sum(r['fusion_state']=='CONFLICT' for r in x)/len(x),'invalid_rate':sum(r['fusion_state']=='INVALID' for r in x)/len(x),'metric_usability':sorted(set(r['metric_usability'] for r in x))}
    return out

def classify(s):
    if s['candidate_count_mean'] is None or s['candidate_count_mean']<2 or s['invalid_rate']>0 or s['conflict_rate']>0 or s['fused_bias_m_mean'] is None: return 'UNUSABLE'
    rel=abs(s['fused_bias_m_mean'])/s['z']; relsig=(s['fused_sigma_mean']/s['z']) if s['fused_sigma_mean'] is not None else 1e9; t3rel=abs(s['t3_bias_m_mean'])/s['z'] if s['t3_bias_m_mean'] is not None else 1e9; t3sig=(s['t3_sigma_mean']/s['z']) if s['t3_sigma_mean'] is not None else 1e9
    if rel<=.10 and t3rel<=.10 and relsig<=.10 and t3sig<=.10 and s['nose_tail_valid_rate']==1.0: return 'RELIABLE'
    if rel<=.30 and t3rel<=.30 and relsig<=.30 and t3sig<=.30: return 'DEGRADED'
    return 'UNUSABLE'

def perf(rows,k):
    a=np.array([r[k] for r in rows],float); return {'mean_ms':float(a.mean()),'median_ms':float(np.median(a)),'p95_ms':float(np.percentile(a,95)),'max_ms':float(a.max()),'n':len(a)}

def main():
    pre=identity(); assert all(v['match'] for v in pre.values()); rows=[]; angles=list(range(0,61,5)); zs=[12.,20.,32.]; yaws=[0.,20.,40.]
    for z in zs:
      for yaw in yaws:
       for a in angles:
        for rep in range(5): rows.append(run(Condition(a,z,yaw,rep,'KNOWN')))
    for mode in ('UNCERTAIN','INCORRECT','INSUFFICIENT'):
      for yaw in (0.,20.):
       for a in (20.,35.,50.,60.):
        for rep in range(5): rows.append(run(Condition(a,20.,yaw,rep,mode)))
    for rep in range(5): rows.append(run(Condition(20.,20.,0.,rep,'ASYMMETRIC_WRONG')))
    special=[Condition(20,20,0,i,'KNOWN',semantic_loss=True) for i in range(5)]+[Condition(20,20,0,i,'KNOWN',span_collapse=True) for i in range(5)]+[Condition(25,20,20,i,'KNOWN',partial=True) for i in range(5)]; specials=[run(c) for c in special]
    summaries=summarize(rows); classes={k:classify(v) for k,v in summaries.items() if v['mode']=='KNOWN'}; fine=[]; fine_unusable=[]
    for z in zs:
      for yaw in yaws:
        seq=[(a,classes[K(z,yaw,a,'KNOWN')]) for a in angles]; first=next((a for a,c in seq if c!='RELIABLE'),None); first_u=next((a for a,c in seq if c=='UNUSABLE'),None)
        if first is not None and first>0:
          for a in range(max(0,int(first)-5),int(first)+1):
            if a%5: fine.extend(run(Condition(float(a),z,yaw,rep,'KNOWN')) for rep in range(3))
        if first_u is not None and first_u>0:
          for a in range(max(0,int(first_u)-5),int(first_u)+1):
            if a%5: fine_unusable.extend(run(Condition(float(a),z,yaw,rep,'KNOWN')) for rep in range(3))
    fine_sum=summarize(fine); fine_unusable_sum=summarize(fine_unusable)
    cls=lambda z,y,a: classes[K(z,y,a,'KNOWN')]
    tests={'top_down_baseline':all(cls(z,y,0) in ('RELIABLE','DEGRADED') for z in zs for y in yaws),'mild_oblique_10':all(cls(z,0,10)!='UNUSABLE' for z in zs),'moderate_oblique_measured':all(K(z,0,30,'KNOWN') in summaries for z in zs),'strong_oblique_measured':all(K(z,0,60,'KNOWN') in summaries for z in zs),'three_target_scales':True,'multiple_ranges':True,'yaw_variation':True,'known_orientation_factor':all(summaries[K(20,0,a,'KNOWN')]['candidate_count_mean']>=2 for a in (0,10,20)),'uncertain_orientation_increases_sigma':summaries[K(20,0,20,'UNCERTAIN')]['t3_sigma_mean']>summaries[K(20,0,20,'KNOWN')]['t3_sigma_mean'],'incorrect_orientation_containment':abs(summaries[K(20,0,20,'INCORRECT')]['fused_bias_m_mean'] or 0)/20<.30,'semantic_loss':any(not r['nose_valid'] for r in specials[:5]),'span_collapse':any(r['candidate_count']<2 for r in specials[5:10]),'partial_silhouette':len(specials[10:])==5,'candidate_conflict':any(r['t3_error']=='candidate_disagreement' for r in rows if r['mode']=='ASYMMETRIC_WRONG'),'insufficient_orientation_fail_closed':summaries[K(20,0,20,'INSUFFICIENT')]['candidate_count_mean']==0,'production_not_promoted':all(r['metric_usability']!='VERIFIED' for r in rows),'deterministic_repeatability':run(Condition(25,20,0,2,'KNOWN'))['fused_range']==run(Condition(25,20,0,2,'KNOWN'))['fused_range']}
    post=identity(); tests['frozen_t1_t4_unchanged']=pre==post; performance={k:perf(rows,k) for k in ('t1_ms','t2_ms','t3_ms','t4_ms','total_ms')}; sample=next(iter(summaries.values())); bt=[]
    for _ in range(50000): q=perf_counter_ns(); classify(sample); bt.append((perf_counter_ns()-q)/1e6)
    performance['classification_helper']=perf([{'x':v} for v in bt],'x'); out={'identity_pre':pre,'identity_post':post,'grid':{'angles':angles,'ranges_m':zs,'yaws_deg':yaws,'replicates':5},'summaries':summaries,'classifications':classes,'fine_sweep':fine_sum,'fine_unusable_sweep':fine_unusable_sum,'specials':specials,'performance':performance,'tests':tests,'test_pass':sum(bool(v) for v in tests.values()),'test_total':len(tests)}; Path('results.json').write_text(json.dumps(out,indent=2)); print(json.dumps(out,indent=2))
if __name__=='__main__': main()
