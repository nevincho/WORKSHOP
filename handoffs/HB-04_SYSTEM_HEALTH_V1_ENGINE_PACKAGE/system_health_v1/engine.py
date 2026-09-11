from __future__ import annotations
import time
from typing import Any, Mapping

STATES={"NOMINAL","DEGRADED","FAULT","STALE","UNAVAILABLE","NOT_VERIFIED"}
CANONICAL_CONCEPTS=("RUNTIME_HEALTH","SYSTEM_CPU","SYSTEM_RAM","CPU_TEMPERATURE","RUNTIME_PERFORMANCE","HQ_CAMERA_HEALTH","WIDE_PIPELINE_HEALTH","HAILO_HEALTH","CA_AUTHORITY_STATE","METRIC_HEALTH","HOROS_HEALTH","TELEMETRY_EDGE_HEALTH")
POS_RUN={"ACTIVE","RUNNING","HEALTHY","OK"}; NEG_RUN={"ERROR","FAILED","FAILURE","STOPPED","OFFLINE","UNAVAILABLE"}
POS_CAM={"OPEN","CONNECTED","AVAILABLE","ACTIVE","RUNNING","HEALTHY","OK","RUNTIME_API"}; NEG_CAM={"ERROR","FAILED","FAILURE","CLOSED","DISCONNECTED","OFFLINE","UNAVAILABLE"}
POS_HAILO={"ACTIVE","RUNNING","READY","HEALTHY","OK","BUSY","AVAILABLE"}; NEG_HAILO={"ERROR","FAILED","FAILURE","OFFLINE","UNAVAILABLE","ABSENT","NOT_AVAILABLE"}
POS_TEL={"LIVE","CONNECTED","HEALTHY","ACTIVE","OK"}; NEG_TEL={"ERROR","FAILED","FAILURE","OFFLINE","DISCONNECTED","UNAVAILABLE"}; STALE_TEL={"STALE","NON_LIVE","CACHED","FALLBACK"}

def up(v): return v.strip().upper().replace(" ","_") if isinstance(v,str) else None
def num(v): return isinstance(v,(int,float)) and not isinstance(v,bool)
def get(m,*p):
    for k in p:
        if not isinstance(m,Mapping) or k not in m: return None
        m=m[k]
    return m
def err(v):
    if v is None:return False
    if isinstance(v,str): return bool(v.strip()) and up(v) not in {"NONE","NULL","OK"}
    if isinstance(v,Mapping): return any(err(x) for x in v.values())
    if isinstance(v,(list,tuple,set)): return any(err(x) for x in v)
    if num(v): return v!=0
    return bool(v)
def fresh(age=None,state="UNKNOWN",thr=None,basis="NONE"): return {"age_s":age if num(age) else None,"state":state,"threshold_s":thr if num(thr) else None,"basis":basis}
def out(c,s,r=(),v=None,f=None,p=(),nv=()): return {"concept":c,"state":s,"reason_codes":list(dict.fromkeys(r)),"values":{k:x for k,x in (v or {}).items() if x is not None},"freshness":f or fresh(),"provenance":list(dict.fromkeys(p)),"not_verified":list(dict.fromkeys(nv))}

class SystemHealthV1Engine:
    def __init__(self,monotonic=time.monotonic): self.clock=monotonic; self.hailo_seen=None
    def normalize(self,telemetry=None,pi_status=None):
        t,p=telemetry or {},pi_status or {}; now=self.clock()
        if num(get(t,"detector_timing","hailo_inference_ms")): self.hailo_seen=now
        c={
          "RUNTIME_HEALTH":self.runtime(t,p),"SYSTEM_CPU":self.scalar(t,"SYSTEM_CPU","cpu_usage","CPU_UNAVAILABLE","CPU_SCOPE_NOT_VERIFIED",["CPU_SCOPE"]),
          "SYSTEM_RAM":self.scalar(t,"SYSTEM_RAM","ram_usage","RAM_UNAVAILABLE","RAM_SEMANTICS_NOT_VERIFIED",["RAM_UNIT","RAM_SCOPE"]),
          "CPU_TEMPERATURE":self.scalar(t,"CPU_TEMPERATURE","cpu_temp","CPU_TEMP_UNAVAILABLE","CPU_TEMP_SEMANTICS_NOT_VERIFIED",["CPU_TEMP_UNIT","CPU_TEMP_THRESHOLD"],"temperature"),
          "RUNTIME_PERFORMANCE":self.performance(t),"HQ_CAMERA_HEALTH":self.camera(t,p),"WIDE_PIPELINE_HEALTH":self.wide(t),"HAILO_HEALTH":self.hailo(t,p,now),
          "CA_AUTHORITY_STATE":self.ca(t),"METRIC_HEALTH":self.metric(t),"HOROS_HEALTH":self.horos(t),"TELEMETRY_EDGE_HEALTH":self.edge(t,p)}
        assert tuple(c)==CANONICAL_CONCEPTS
        return {"schema":"TANGRA_SYSTEM_HEALTH_V1","concepts":c}
    def scalar(self,t,c,key,missing,reason,nv,label="usage"):
        x=t.get(key); pr=[f"telemetry.{key}"]
        return out(c,"UNAVAILABLE",[missing],p=pr,f=fresh(basis="CURRENT_POLL")) if x is None else out(c,"NOT_VERIFIED",[reason],{label:x,"unit":"NOT_VERIFIED"},fresh(state="FRESH",basis="CURRENT_POLL"),pr,nv)
    def runtime(self,t,p):
        v={"ai_status":t.get("ai_status"),"droneguard_status":t.get("droneguard_status"),"runtime_controller_state":t.get("runtime_controller_state"),"system_status":t.get("system_status"),"controller_state":p.get("state"),"uptime_s":t.get("runtime_uptime_sec") or get(t,"dashboard_state","system","tangra_uptime_sec")}; ss=[up(x) for x in v.values() if isinstance(x,str)]; pr=["telemetry.ai_status","telemetry.droneguard_status","telemetry.runtime_controller_state","telemetry.system_status","pi_status.state","telemetry.runtime_uptime_sec"]
        if not ss:return out("RUNTIME_HEALTH","UNAVAILABLE",["RUNTIME_STATE_UNAVAILABLE"],v,fresh(basis="CURRENT_POLL"),pr)
        if any(x in NEG_RUN for x in ss):return out("RUNTIME_HEALTH","FAULT",["RUNTIME_ERROR" if any(x in {"ERROR","FAILED","FAILURE"} for x in ss) else "RUNTIME_NOT_ACTIVE"],v,fresh(state="FRESH",basis="CURRENT_POLL"),pr)
        if all(x in POS_RUN for x in ss):return out("RUNTIME_HEALTH","NOMINAL",["RUNTIME_ACTIVE"],v,fresh(state="FRESH",basis="CURRENT_POLL"),pr)
        return out("RUNTIME_HEALTH","NOT_VERIFIED",["RUNTIME_STATE_CONFLICT"],v,fresh(basis="CURRENT_POLL"),pr,["RUNTIME_STATE_SEMANTICS"])
    def performance(self,t):
        fps=t.get("fps"); rp=t.get("runtime_profile") if isinstance(t.get("runtime_profile"),Mapping) else {}; v={"fps":fps,"fps_unit":"frames/s","stage_ms":{k:x for k,x in rp.items() if k.endswith("_ms") and num(x)}}; pr=["telemetry.fps","telemetry.runtime_profile.*"]
        return out("RUNTIME_PERFORMANCE","UNAVAILABLE",["FPS_UNAVAILABLE"],v,fresh(basis="CURRENT_POLL"),pr) if fps is None else out("RUNTIME_PERFORMANCE","NOT_VERIFIED",["PERFORMANCE_THRESHOLD_NOT_DEFINED"],v,fresh(state="FRESH",basis="CURRENT_POLL"),pr,["PERFORMANCE_THRESHOLD"])
    def camera(self,t,p):
        v={"camera_state":t.get("camera_status"),"controller_camera_state":p.get("camera_status")}; ss=[up(x) for x in v.values() if x is not None]; pr=["telemetry.camera_status","pi_status.camera_status"]; nv=["HQ_FRAME_FRESHNESS","HQ_CAMERA_ID_QUALIFICATION"]
        if not ss:return out("HQ_CAMERA_HEALTH","UNAVAILABLE",["HQ_CAMERA_UNAVAILABLE","HQ_FRESHNESS_NOT_VERIFIED"],v,fresh(),pr,nv)
        if any(x in NEG_CAM for x in ss):return out("HQ_CAMERA_HEALTH","FAULT",["HQ_CAMERA_ERROR" if any(x in {"ERROR","FAILED","FAILURE"} for x in ss) else "HQ_CAMERA_UNAVAILABLE","HQ_FRESHNESS_NOT_VERIFIED"],v,fresh(),pr,nv)
        if all(x in POS_CAM for x in ss):return out("HQ_CAMERA_HEALTH","NOMINAL",["HQ_CAMERA_AVAILABLE","HQ_FRESHNESS_NOT_VERIFIED"],v,fresh(),pr,nv)
        return out("HQ_CAMERA_HEALTH","NOT_VERIFIED",["HQ_CAMERA_STATE_CONFLICT","HQ_FRESHNESS_NOT_VERIFIED"],v,fresh(),pr,nv)
    def wide(self,t):
        w=get(t,"horos_shadow","wide_worker"); pr=["telemetry.horos_shadow.wide_worker.*"]
        if not isinstance(w,Mapping):return out("WIDE_PIPELINE_HEALTH","UNAVAILABLE",["WIDE_STATE_UNAVAILABLE"],p=pr,f=fresh(basis="SOURCE_NATIVE"))
        env=w.get("environment"); v={k:w.get(k) for k in ("running","fail_open","last_age_s","last_fresh","max_age_s","stale_rejected","input_dropped","output_dropped","failures","environment_failures","last_error","environment_last_error")}; v["environment_status"]=env.get("status") if isinstance(env,Mapping) else w.get("environment_status"); age,fr,thr=w.get("last_age_s"),w.get("last_fresh"),w.get("max_age_s"); stale=fr is False or (num(age) and num(thr) and age>thr); f=fresh(age,"STALE" if stale else "FRESH" if fr is True else "UNKNOWN",thr,"SOURCE_NATIVE")
        if w.get("running") is False:return out("WIDE_PIPELINE_HEALTH","FAULT",["WIDE_WORKER_NOT_RUNNING"],v,f,pr)
        if err(w.get("last_error")) or err(w.get("environment_last_error")):return out("WIDE_PIPELINE_HEALTH","FAULT",["WIDE_ERROR"],v,f,pr)
        if stale:return out("WIDE_PIPELINE_HEALTH","STALE",["WIDE_STALE"],v,f,pr)
        if w.get("running") is True and fr is True:return out("WIDE_PIPELINE_HEALTH","NOMINAL",v=v,f=f,p=pr)
        return out("WIDE_PIPELINE_HEALTH","UNAVAILABLE",["WIDE_STATE_UNAVAILABLE"],v,f,pr)
    def hailo(self,t,p,now):
        hs,ps=t.get("hailo_status"),p.get("hailo_status"); pa=p.get("hailo"); backend=t.get("detector_backend"); ss=[up(x) for x in (hs,ps) if x is not None]; age=None if self.hailo_seen is None else max(0,now-self.hailo_seen); v={"backend":backend,"hailo_state":hs,"controller_hailo_available":pa,"controller_hailo_state":ps,"inference_ms":get(t,"detector_timing","hailo_inference_ms"),"observation_age_s":age}; pr=["telemetry.detector_backend","telemetry.hailo_status","pi_status.hailo","pi_status.hailo_status","telemetry.detector_timing.hailo_inference_ms","pc.monotonic_clock"]
        if pa is False or any(x in NEG_HAILO for x in ss):return out("HAILO_HEALTH","FAULT",["HAILO_ERROR" if any(x in {"ERROR","FAILED","FAILURE"} for x in ss) else "HAILO_UNAVAILABLE"],v,fresh(age,basis="PC_DERIVED"),pr)
        if (pa is True or up(backend)=="HAILO") and all(x in POS_HAILO for x in ss):return out("HAILO_HEALTH","NOMINAL",["HAILO_AVAILABLE"]+(["HAILO_OBSERVATION_AGE_ONLY"] if age is not None else []),v,fresh(age,basis="PC_DERIVED"),pr,["HAILO_OBSERVATION_STALE_THRESHOLD"])
        if backend is None and hs is None and pa is None and ps is None:return out("HAILO_HEALTH","UNAVAILABLE",["HAILO_STATE_UNAVAILABLE"],v,fresh(age,basis="PC_DERIVED"),pr)
        return out("HAILO_HEALTH","NOT_VERIFIED",["HAILO_STATE_CONFLICT"],v,fresh(age,basis="PC_DERIVED"),pr,["HAILO_STATE_SEMANTICS"])
    def ca(self,t):
        a,b=t.get("kalman_algorithm"),get(t,"horos_shadow","tracking_authority"); v={"kalman_algorithm":a,"tracking_authority":b}; pr=["telemetry.kalman_algorithm","telemetry.horos_shadow.tracking_authority"]
        if a is None or b is None:return out("CA_AUTHORITY_STATE","UNAVAILABLE",["CA_AUTHORITY_UNAVAILABLE"],v,fresh(basis="CURRENT_POLL"),pr,["CA_WORKER_LIVENESS"])
        m=up(a)=="CA_KALMAN_PRIMARY" and up(b)=="UPSTREAM_CA_KALMAN"; v["authority_match"]=m
        return out("CA_AUTHORITY_STATE","NOT_VERIFIED" if m else "DEGRADED",["CA_AUTHORITY_MATCH" if m else "CA_AUTHORITY_MISMATCH","CA_LIVENESS_NOT_VERIFIED"],v,fresh(state="FRESH",basis="CURRENT_POLL"),pr,["CA_WORKER_LIVENESS"])
    def metric(self,t):
        h=t.get("horos_shadow") if isinstance(t.get("horos_shadow"),Mapping) else {}; mp=h.get("map") if isinstance(h.get("map"),Mapping) else {}; tg=h.get("targets"); one=tg[0] if isinstance(tg,list) and tg and isinstance(tg[0],Mapping) else {}; mu=h.get("metric_usable",one.get("metric_usable")); ph=h.get("physical_metric_state",one.get("physical_metric_state")); va=h.get("validity",get(one,"state","meta","validity")); v={"metric_usable":mu,"physical_metric_state":ph,"validity":va,"horos_authoritative":h.get("authoritative"),"map_authoritative":mp.get("authoritative"),"target_authoritative":one.get("authoritative"),"geometry_status":h.get("geometry_status") or mp.get("geometry_status")}; pr=["telemetry.horos_shadow.targets[*].metric_usable","telemetry.horos_shadow.physical_metric_state","telemetry.horos_shadow.targets[*].state.meta.validity","telemetry.horos_shadow.authoritative","telemetry.horos_shadow.map.authoritative","telemetry.horos_shadow.geometry_status"]; nv=["METRIC_EXPECTATION","LAST_VALID_METRIC_FRESHNESS"]
        if not any(x is not None for x in v.values()):return out("METRIC_HEALTH","UNAVAILABLE",["METRIC_STATE_UNAVAILABLE"],v,fresh(),pr,nv)
        r=["METRIC_EXPECTATION_NOT_DEFINED"]+(["METRIC_USABLE"] if mu is True else ["METRIC_NOT_USABLE"] if mu is False else [])+(["METRIC_NON_PHYSICAL"] if ph is False else [])+(["METRIC_NON_AUTHORITATIVE"] if False in (h.get("authoritative"),mp.get("authoritative"),one.get("authoritative")) else [])+(["METRIC_INVALID"] if up(va) in {"INVALID","REJECTED"} else [])+(["METRIC_STALE"] if up(va)=="STALE" else [])
        return out("METRIC_HEALTH","NOT_VERIFIED",r,v,fresh(),pr,nv)
    def horos(self,t):
        h=t.get("horos_shadow"); pr=["telemetry.horos_shadow.*","telemetry.server_time"]
        if not isinstance(h,Mapping):return out("HOROS_HEALTH","UNAVAILABLE",["HOROS_STATE_UNAVAILABLE"],p=pr,f=fresh(basis="PC_DERIVED"))
        st,ts=t.get("server_time"),h.get("timestamp"); age=max(0,st-ts) if num(st) and num(ts) else None; v={"mode":h.get("mode"),"runtime_role":h.get("runtime_role"),"fail_open":h.get("fail_open"),"authoritative":h.get("authoritative"),"schema_version":h.get("schema_version"),"errors":h.get("errors"),"degraded_reasons":h.get("degraded_reasons"),"age_s":age}; f=fresh(age,basis="PC_DERIVED"); nv=["HOROS_FRESHNESS_THRESHOLD"]
        if err(h.get("errors")):return out("HOROS_HEALTH","FAULT",["HOROS_ERROR","HOROS_FRESHNESS_AGE_ONLY"],v,f,pr,nv)
        if err(h.get("degraded_reasons")):return out("HOROS_HEALTH","DEGRADED",["HOROS_DEGRADED","HOROS_FRESHNESS_AGE_ONLY"],v,f,pr,nv)
        return out("HOROS_HEALTH","NOT_VERIFIED",["HOROS_MODE_CONTEXT","HOROS_FRESHNESS_AGE_ONLY"],v,f,pr,nv+["HOROS_AFFIRMATIVE_HEALTH_SEMANTIC"])
    def edge(self,t,p):
        v={"source":t.get("pi_telemetry_source"),"pi_http_status":t.get("pi_http_status"),"pi_http_age_s":t.get("pi_http_age_sec"),"pc_cache_status":t.get("pc_cache_status"),"remote_ingest_status":t.get("remote_ingest_status"),"remote_ingest_age_s":t.get("remote_ingest_age_sec"),"pi_status":p.get("pi_status"),"telemetry_status":p.get("telemetry"),"pi_telemetry_error":t.get("pi_telemetry_error"),"runtime_controller_error":t.get("runtime_controller_error"),"controller_errors":p.get("errors")}; ss=[up(x) for x in (v["pi_http_status"],v["pc_cache_status"],v["pi_status"],v["telemetry_status"]) if x is not None]; age=v["pi_http_age_s"] if num(v["pi_http_age_s"]) else None; pr=["telemetry.pi_telemetry_source","telemetry.pi_http_status","telemetry.pi_http_age_sec","telemetry.pc_cache_status","pi_status.pi_status","pi_status.telemetry","telemetry.pi_telemetry_error","telemetry.runtime_controller_error","pi_status.errors"]
        if any(err(v[k]) for k in ("pi_telemetry_error","runtime_controller_error","controller_errors")) or any(x in NEG_TEL for x in ss):return out("TELEMETRY_EDGE_HEALTH","FAULT",["TELEMETRY_ERROR" if any(err(v[k]) for k in ("pi_telemetry_error","runtime_controller_error","controller_errors")) or any(x in {"ERROR","FAILED","FAILURE"} for x in ss) else "TELEMETRY_DISCONNECTED"],v,fresh(age,basis="SOURCE_NATIVE"),pr)
        if any(x in STALE_TEL for x in ss):return out("TELEMETRY_EDGE_HEALTH","STALE",["TELEMETRY_STALE" if "STALE" in ss else "TELEMETRY_NON_LIVE"],v,fresh(age,"STALE",None,"SOURCE_NATIVE"),pr)
        if ss and all(x in POS_TEL for x in ss):return out("TELEMETRY_EDGE_HEALTH","NOMINAL",["TELEMETRY_CONNECTED"],v,fresh(age,"FRESH",None,"SOURCE_NATIVE"),pr)
        if not ss:return out("TELEMETRY_EDGE_HEALTH","UNAVAILABLE",["TELEMETRY_UNAVAILABLE"],v,fresh(age,basis="SOURCE_NATIVE"),pr)
        return out("TELEMETRY_EDGE_HEALTH","NOT_VERIFIED",["TELEMETRY_SOURCE_CONFLICT"],v,fresh(age,basis="SOURCE_NATIVE"),pr,["TELEMETRY_STATE_SEMANTICS"])
