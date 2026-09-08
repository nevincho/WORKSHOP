import json
import cv2
import numpy as np
from sparse_target_geometry import SparseTargetGeometryExtractor, TargetGeometryInput


def make(size):
    h,w=size
    img=np.full((h,w,3),230,np.uint8)
    c=(w//2,h//2)
    pts=np.array([[.38,0],[.10,-.10],[-.10,-.26],[-.30,-.26],[-.22,-.08],[-.38,-.08],[-.38,.08],[-.22,.08],[-.30,.26],[-.10,.26],[.10,.10]],float)
    pts[:,0]*=w; pts[:,1]*=h; pts+=c
    cv2.fillPoly(img,[np.rint(pts).astype(np.int32)],(30,30,30))
    span=np.ptp(pts,axis=0)
    return img,(0,0,w,h),(int(round(span[0])),int(round(span[1])))

E=SparseTargetGeometryExtractor(); rows=[]; all_ms=[]
for size in [(64,64),(96,128),(144,192)]:
    img,b,target_px=make(size); t=TargetGeometryInput("bench",1.0,"t","FPV",0.9,b)
    for _ in range(20): E.extract(img,t)
    ms=[]
    for _ in range(300):
        ms.append(E.extract(img,t).processing_time_ms)
    all_ms += ms; arr=np.array(ms)
    rows.append({"roi_hw":list(size),"target_span_wh_px":list(target_px),"n":len(ms),"mean_ms":float(arr.mean()),"median_ms":float(np.median(arr)),"p95_ms":float(np.percentile(arr,95)),"max_ms":float(arr.max())})
arr=np.array(all_ms)
print(json.dumps({"environment":"container x86_64; OpenCV/Numpy microbenchmark; NOT Pi5 end-to-end","targets_processed":len(all_ms),"sizes":rows,"overall":{"mean_ms":float(arr.mean()),"median_ms":float(np.median(arr)),"p95_ms":float(np.percentile(arr,95)),"max_ms":float(arr.max())}},indent=2))
