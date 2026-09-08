import json, statistics, time
from test_sparse_geometry_range_source import CAL, profile, geom
from sparse_geometry_range_source import SparseGeometryRangeSource

N=50000
src=SparseGeometryRangeSource(CAL,profile())
g=geom(20.0)
for _ in range(500): src.estimate(g)
vals=[]
for _ in range(N):
    t=time.perf_counter_ns(); src.estimate(g); vals.append((time.perf_counter_ns()-t)/1e6)
vals_sorted=sorted(vals); idx=max(0,min(N-1,int(0.95*N)-1))
out={'benchmark':'SPARSE_GEOMETRY_RANGE_SOURCE_COORDINATE_ONLY','evidence':'SYNTHETIC_HOST_ONLY','sample_count':N,'mean_ms':statistics.fmean(vals),'median_ms':statistics.median(vals),'p95_ms':vals_sorted[idx],'max_ms':max(vals),'platform_claim':'HOST_ONLY; Pi5/end-to-end NOT_VERIFIED'}
print(json.dumps(out,indent=2))
