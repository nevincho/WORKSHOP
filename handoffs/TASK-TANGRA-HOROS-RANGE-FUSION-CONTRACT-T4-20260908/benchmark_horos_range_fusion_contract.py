from time import perf_counter_ns
from statistics import mean, median
from horos_range_fusion_contract import *

f=HorosRangeFusionContract()
a=adapt_monocular_class_size(ExistingMonocularClassSizeInput('v1',20.0,1.2,.82,True,True,'f',1.0,'t','mono'))
b=adapt_sparse_geometry(SparseGeometryRangeInput('t3',20.3,.9,.88,True,False,True,False,'f',1.0,'t','sparse'))
N=100000
vals=[]
for _ in range(N):
    t=perf_counter_ns(); f.fuse((a,b)); vals.append((perf_counter_ns()-t)/1e6)
s=sorted(vals)
p95=s[int(.95*(N-1))]
print({'sample_count':N,'mean_ms':mean(vals),'median_ms':median(vals),'p95_ms':p95,'max_ms':max(vals)})
