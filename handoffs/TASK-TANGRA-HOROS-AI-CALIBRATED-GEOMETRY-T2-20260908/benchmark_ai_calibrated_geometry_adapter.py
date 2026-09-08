import json, time, numpy as np
from ai_calibrated_geometry_adapter import *
AI=PlaneSpec("HQ_AI",(640,640)); CAL=PlaneSpec("HQ_CAL",(2028,1520))
E=AICalibratedGeometryAdapter(GeometryTransform("benchmark_axis_aligned","1",AI,CAL,affine_axis_aligned(640/2028,640/1520,0,0)))
g=Task1GeometryLike("bench",1.0,"target","FPV",(100,100,500,500),(320,320),tuple(SparsePointLike(f"P{i}",50.0+i*50,100.0+i*40,.9,True) for i in range(5)),"TASK1")
for _ in range(1000): E.adapt(g)
samples=[]
for _ in range(20000):
    t=time.perf_counter_ns(); E.adapt(g); samples.append((time.perf_counter_ns()-t)/1e6)
a=np.asarray(samples)
print(json.dumps({"environment":"container x86_64; Python/NumPy coordinate-only microbenchmark; NOT Pi5/end-to-end","sample_count":len(samples),"mean_ms":float(a.mean()),"median_ms":float(np.median(a)),"p95_ms":float(np.percentile(a,95)),"max_ms":float(a.max())},indent=2))
