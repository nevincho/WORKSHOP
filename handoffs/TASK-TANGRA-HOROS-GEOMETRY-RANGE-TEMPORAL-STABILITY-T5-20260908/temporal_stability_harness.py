from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from math import hypot, sqrt
from statistics import mean, pstdev
from time import perf_counter_ns
from typing import Optional, Tuple
import numpy as np
TASK1_COMMIT='c7b378841979f82b037c47be3571fa72a7b70e51'; TASK2_COMMIT='4bd4b5d38357db501de07511aeabaa4c0ae058e1'; TASK3_COMMIT='c121ce25dbba84520c6f8e644281a7cb2bf3ee73'; TASK4_COMMIT='7f628a727b89599ea6977053ea12211b10e0ffcd'
class State(str,Enum): VALID='VALID'; DEGRADED='DEGRADED'; CONFLICT='CONFLICT'; INVALID='INVALID'
@dataclass(frozen=True)
class P: name:str; x:Optional[float]; y:Optional[float]; confidence:float; valid:bool=True
@dataclass(frozen=True)
class FrameFixture:
    sequence:str; index:int; target_id:str; truth_range_m:float; center:P; left:P; right:P; nose:P; tail:P; geometry_confidence:float; class_range_m:Optional[float]; class_sigma_m:Optional[float]; class_confidence:Optional[float]; class_valid:bool=True; transform_valid:bool=True; hard_conflict:bool=False
@dataclass(frozen=True)
class FrameResult:
    sequence:str; index:int; target_id:str; truth_range_m:float; center_xy:Optional[Tuple[float,float]]; left_xy:Optional[Tuple[float,float]]; right_xy:Optional[Tuple[float,float]]; lr_span_px:Optional[float]; nt_span_px:Optional[float]; nose_tail_valid:bool; sparse_range_m:Optional[float]; sparse_sigma_m:Optional[float]; fused_range_m:Optional[float]; fused_sigma_m:Optional[float]; geometry_confidence:float; range_confidence:float; state:State; latency_ms:float
@dataclass(frozen=True)
class StabilityConfig:
    focal_px:float=5000.; physical_width_m:float=.40; physical_length_m:float=.55; point_sigma_px:float=.75; uncertainty_floor_relative:float=.01; soft_disagreement_relative:float=.10; hard_disagreement_relative:float=.30
class EveryFrameEvaluator:
    '''Stateless SHADOW measurement evaluator; no identity/tracking/prediction/propagation state.'''
    def __init__(self,cfg=None): self.cfg=cfg or StabilityConfig()
    @staticmethod
    def _span(a,b):
        if not a.valid or not b.valid or a.x is None or a.y is None or b.x is None or b.y is None: return None
        s=hypot(b.x-a.x,b.y-a.y); return s if np.isfinite(s) and s>1e-9 else None
    def evaluate(self,f):
        t0=perf_counter_ns()
        if not f.transform_valid: return self._invalid(f,t0)
        lr=self._span(f.left,f.right); nt=self._span(f.nose,f.tail); cs=[]
        if lr is not None:
            z=self.cfg.focal_px*self.cfg.physical_width_m/lr; sig=max(z*.01,z*(sqrt(2)*self.cfg.point_sigma_px/max(lr,1e-9))); cs.append((z,sig,min(f.left.confidence,f.right.confidence)))
        if nt is not None:
            z=self.cfg.focal_px*self.cfg.physical_length_m/nt; sig=max(z*.01,z*(sqrt(2)*self.cfg.point_sigma_px/max(nt,1e-9))); cs.append((z,sig,min(f.nose.confidence,f.tail.confidence)))
        sparse=sparse_sig=None; sparse_conf=0.
        if len(cs)>=2:
            rel=abs(cs[0][0]-cs[1][0])/max((cs[0][0]+cs[1][0])*.5,1e-9)
            if rel<=self.cfg.hard_disagreement_relative:
                ws=[c[2]/max(c[1]**2,1e-12) for c in cs]; sparse=sum(w*c[0] for w,c in zip(ws,cs))/sum(ws); formal=sqrt(1/sum(ws)); dis=sqrt(sum(w*(c[0]-sparse)**2 for w,c in zip(ws,cs))/sum(ws)); sparse_sig=max(formal,dis,abs(sparse)*.01); sparse_conf=mean(c[2] for c in cs)
        ev=[]
        if sparse is not None: ev.append((sparse,sparse_sig,sparse_conf))
        if f.class_valid and f.class_range_m is not None and f.class_sigma_m is not None and f.class_confidence is not None: ev.append((f.class_range_m,f.class_sigma_m,f.class_confidence))
        if not ev: return self._invalid(f,t0,lr,nt)
        if len(ev)==1: return self._finish(f,t0,lr,nt,sparse,sparse_sig,ev[0][0],max(ev[0][1],abs(ev[0][0])*.01),ev[0][2],State.DEGRADED)
        a,b=ev; rel=abs(a[0]-b[0])/max((a[0]+b[0])*.5,1e-9)
        if f.hard_conflict or rel>self.cfg.hard_disagreement_relative: return self._finish(f,t0,lr,nt,sparse,sparse_sig,None,max(a[1],b[1],abs(a[0]-b[0])*.5),min(a[2],b[2]),State.CONFLICT)
        wa=a[2]/max(a[1]**2,1e-12); wb=b[2]/max(b[1]**2,1e-12); z=(wa*a[0]+wb*b[0])/(wa+wb); formal=sqrt(1/(wa+wb)); dis=sqrt((wa*(a[0]-z)**2+wb*(b[0]-z)**2)/(wa+wb)); sig=max(formal,dis,abs(z)*.01)
        return self._finish(f,t0,lr,nt,sparse,sparse_sig,z,sig,mean((a[2],b[2])),State.DEGRADED)
    def _finish(self,f,t0,lr,nt,sr,ss,fr,fs,rc,state):
        xy=lambda p: None if not p.valid or p.x is None else (p.x,p.y)
        return FrameResult(f.sequence,f.index,f.target_id,f.truth_range_m,xy(f.center),xy(f.left),xy(f.right),lr,nt,nt is not None,sr,ss,fr,fs,f.geometry_confidence,rc,state,(perf_counter_ns()-t0)/1e6)
    def _invalid(self,f,t0,lr=None,nt=None): return FrameResult(f.sequence,f.index,f.target_id,f.truth_range_m,None,None,None,lr,nt,False,None,None,None,None,f.geometry_confidence,0.,State.INVALID,(perf_counter_ns()-t0)/1e6)
def _points(cx,cy,z,angle=0.,foreshorten=1.,jitter=(0,0),nt_valid=True,conf=.92):
    f=5000.; w=f*.40/z; l=f*.55*foreshorten/z; ca,sa=np.cos(angle),np.sin(angle); ux,uy=ca,sa; vx,vy=-sa,ca; cx+=jitter[0]; cy+=jitter[1]
    left=P('LEFT',cx-vx*w/2,cy-vy*w/2,conf); right=P('RIGHT',cx+vx*w/2,cy+vy*w/2,conf)
    if nt_valid: nose=P('NOSE',cx+ux*l/2,cy+uy*l/2,conf); tail=P('TAIL',cx-ux*l/2,cy-uy*l/2,conf)
    else: nose=P('NOSE',None,None,conf*.2,False); tail=P('TAIL',None,None,conf*.2,False)
    return P('CENTER',cx,cy,conf),left,right,nose,tail
def build_sequences(seed=20260908):
    rng=np.random.default_rng(seed); out={}
    def base(name,i,z=20,cx=320,cy=320,angle=0,foreshorten=1,noise=.35,nt=True,conf=.92):
        c,l,r,n,t=_points(cx,cy,z,angle,foreshorten,(float(rng.normal(0,noise)),float(rng.normal(0,noise))),nt,conf)
        def pj(p): return p if not p.valid else P(p.name,p.x+float(rng.normal(0,.22)),p.y+float(rng.normal(0,.22)),p.confidence,p.valid)
        l,r,n,t=pj(l),pj(r),pj(n),pj(t); cz=z+float(rng.normal(0,z*.004)); return FrameFixture(name,i,'TGT-A',z,c,l,r,n,t,conf,cz,max(.15,z*.02),.90)
    out['A_STATIC_NOISE']=tuple(base('A_STATIC_NOISE',i) for i in range(80)); out['B_TRANSLATION']=tuple(base('B_TRANSLATION',i,cx=280+i*.9,cy=300+i*.35) for i in range(80)); out['C_SCALE_CHANGE']=tuple(base('C_SCALE_CHANGE',i,z=28-i*.16) for i in range(80)); out['D_ROTATION']=tuple(base('D_ROTATION',i,angle=np.deg2rad(-12+24*i/79)) for i in range(80)); out['E_FORESHORTEN']=tuple(base('E_FORESHORTEN',i,foreshorten=.94+.04*np.sin(i/12)) for i in range(80))
    arr=[]
    for i in range(80):
        x=base('F_CORRUPT',i)
        if i==40: x=FrameFixture(x.sequence,i,x.target_id,x.truth_range_m,x.center,x.left,P('RIGHT',x.right.x+95,x.right.y,.2),x.nose,x.tail,.25,x.class_range_m,x.class_sigma_m,x.class_confidence)
        arr.append(x)
    out['F_CORRUPT']=tuple(arr)
    def fault_seq(name,mode):
        arr=[]
        for i in range(80):
            x=base(name,i)
            if 30<=i<=34:
                if mode=='weak': x=FrameFixture(name,i,x.target_id,x.truth_range_m,P('CENTER',None,None,0,False),P('LEFT',None,None,0,False),P('RIGHT',None,None,0,False),P('NOSE',None,None,0,False),P('TAIL',None,None,0,False),0.,None,None,None,False)
                elif mode=='amb': x=FrameFixture(name,i,x.target_id,x.truth_range_m,x.center,x.left,x.right,P('NOSE',None,None,.2,False),P('TAIL',None,None,.2,False),x.geometry_confidence,x.class_range_m,x.class_sigma_m,x.class_confidence)
                else: x=FrameFixture(name,i,x.target_id,x.truth_range_m,x.center,P('LEFT',None,None,.2,False),x.right,x.nose,x.tail,.42,x.class_range_m,x.class_sigma_m,x.class_confidence)
            arr.append(x)
        return tuple(arr)
    out['G_WEAK_CONTRAST']=fault_seq('G_WEAK_CONTRAST','weak'); out['H_AXIAL_AMBIGUITY']=fault_seq('H_AXIAL_AMBIGUITY','amb'); out['I_PARTIAL_SILHOUETTE']=fault_seq('I_PARTIAL_SILHOUETTE','partial'); out['J_RECOVERY']=fault_seq('J_RECOVERY','weak'); return out
def _cv(v):
    v=[float(x) for x in v if x is not None]; return pstdev(v)/abs(mean(v)) if len(v)>1 and abs(mean(v))>1e-12 else 0.
def sequence_metrics(results):
    clean=[r for r in results if r.state not in (State.INVALID,State.CONFLICT) and r.fused_range_m is not None]
    def pr(points):
        p=[x for x in points if x is not None]
        if len(p)<3:return float('nan')
        xs=np.array([x[0] for x in p]); ys=np.array([x[1] for x in p]); dx=np.diff(xs);dy=np.diff(ys);dx-=np.median(dx);dy-=np.median(dy);return float(sqrt(np.mean(dx*dx+dy*dy)))
    fr=[r.fused_range_m for r in clean]; truth=[r.truth_range_m for r in clean]; err=[a-b for a,b in zip(fr,truth)]
    return {'center_rms_jitter_px':pr([r.center_xy for r in clean]),'left_rms_jitter_px':pr([r.left_xy for r in clean]),'right_rms_jitter_px':pr([r.right_xy for r in clean]),'lr_span_cv':_cv([r.lr_span_px for r in clean]),'nt_span_cv':_cv([r.nt_span_px for r in clean]),'sparse_range_cv':_cv([r.sparse_range_m for r in clean]),'fused_range_cv':_cv(fr),'fused_error_jitter_m':pstdev(err) if len(err)>1 else 0.,'range_bias_m':mean(err) if err else float('nan'),'max_transient_error_m':max([abs(e) for e in err],default=float('nan')),'invalid_frames':sum(r.state==State.INVALID for r in results),'conflict_frames':sum(r.state==State.CONFLICT for r in results),'nose_tail_valid_rate':sum(r.nose_tail_valid for r in results)/len(results),'geometry_conf_mean':mean(r.geometry_confidence for r in results),'range_conf_mean':mean(r.range_confidence for r in results),'latency_mean_ms':mean(r.latency_ms for r in results)}
def run_all(seed=20260908):
    ev=EveryFrameEvaluator(); seqs=build_sequences(seed); rr={k:tuple(ev.evaluate(x) for x in v) for k,v in seqs.items()}; return {k:sequence_metrics(v) for k,v in rr.items()},rr
def decision(m):
    x=m['A_STATIC_NOISE']; return x['center_rms_jitter_px']<=1.5 and x['lr_span_cv']<=.02 and x['fused_range_cv']<=.03
