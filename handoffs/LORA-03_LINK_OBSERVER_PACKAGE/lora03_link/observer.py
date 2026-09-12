from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Optional, Tuple
from tangra_lora_v1 import decode, DecodedPacket, MessageType, Event
SERIAL_HALF=1<<15
class LinkState(str,Enum):
    NO_DATA='NO_DATA'; FRESH='FRESH'; STALE='STALE'; DISCONNECTED='DISCONNECTED'
class PacketDisposition(str,Enum):
    ACCEPTED='ACCEPTED'; DUPLICATE='DUPLICATE'; OUT_OF_ORDER='OUT_OF_ORDER'; OLD_SESSION='OLD_SESSION'; UPTIME_REGRESSION='UPTIME_REGRESSION'; INVALID='INVALID'; EVENT_DUPLICATE='EVENT_DUPLICATE'
@dataclass
class ReceiverMetrics:
    valid_packets:int=0; invalid_packets:int=0; duplicate_packets:int=0; out_of_order_packets:int=0; inferred_missing_packets:int=0; session_changes:int=0
@dataclass
class SourceObservation:
    source_id:int
    current_session_id:Optional[int]=None
    seen_sessions:set[int]=field(default_factory=set)
    last_sequence:Optional[int]=None
    last_source_uptime:Optional[int]=None
    last_receive_time:Optional[float]=None
    metrics:ReceiverMetrics=field(default_factory=ReceiverMetrics)
    latest_semantic:Dict[MessageType,DecodedPacket]=field(default_factory=dict)
    delivered_event_refs:set[Tuple[int,int]]=field(default_factory=set)
@dataclass(frozen=True)
class ObservationResult:
    source_id:Optional[int]; disposition:PacketDisposition; delivered:bool; packet:Optional[DecodedPacket]=None; error:Optional[str]=None; inferred_missing:int=0; session_changed:bool=False
class MockClock:
    def __init__(self,start:float=0.0): self._now=float(start)
    def now(self)->float: return self._now
    def advance(self,seconds:float)->None:
        if seconds<0: raise ValueError('negative clock advance')
        self._now+=float(seconds)
class LinkObserver:
    def __init__(self,clock:MockClock,stale_after_s:float,disconnect_after_s:float):
        if stale_after_s<=0 or disconnect_after_s<=stale_after_s: raise ValueError('thresholds require 0 < stale < disconnect')
        self.clock=clock; self.stale_after_s=float(stale_after_s); self.disconnect_after_s=float(disconnect_after_s); self.sources:Dict[int,SourceObservation]={}; self.invalid_packets_total=0
    def source(self,source_id:int)->SourceObservation: return self.sources.setdefault(source_id,SourceObservation(source_id))
    def link_state(self,source_id:int)->LinkState:
        s=self.sources.get(source_id)
        if s is None or s.last_receive_time is None: return LinkState.NO_DATA
        age=self.clock.now()-s.last_receive_time
        if age<self.stale_after_s: return LinkState.FRESH
        if age<self.disconnect_after_s: return LinkState.STALE
        return LinkState.DISCONNECTED
    def last_valid_age(self,source_id:int)->Optional[float]:
        s=self.sources.get(source_id)
        if s is None or s.last_receive_time is None: return None
        return max(0.0,self.clock.now()-s.last_receive_time)
    def observe_bytes(self,data:bytes)->ObservationResult:
        d=decode(data)
        if not d.ok:
            self.invalid_packets_total+=1
            return ObservationResult(None,PacketDisposition.INVALID,False,error=d.error)
        p=d.packet; s=self.source(p.meta.source_id); s.metrics.valid_packets+=1
        return self._observe_decoded(s,p)
    def _observe_decoded(self,s:SourceObservation,p:DecodedPacket)->ObservationResult:
        m=p.meta; now=self.clock.now()
        if s.current_session_id is None:
            s.current_session_id=m.session_id; s.seen_sessions.add(m.session_id); s.last_sequence=m.sequence; s.last_source_uptime=m.source_uptime_s; s.last_receive_time=now
            return self._deliver_or_suppress_event(s,p,False)
        if m.session_id!=s.current_session_id:
            if m.session_id in s.seen_sessions: return ObservationResult(m.source_id,PacketDisposition.OLD_SESSION,False,p)
            s.metrics.session_changes+=1; s.current_session_id=m.session_id; s.seen_sessions.add(m.session_id); s.last_sequence=m.sequence; s.last_source_uptime=m.source_uptime_s; s.last_receive_time=now
            return self._deliver_or_suppress_event(s,p,True)
        delta=(m.sequence-s.last_sequence)&0xFFFF
        if delta==0:
            s.metrics.duplicate_packets+=1
            return ObservationResult(m.source_id,PacketDisposition.DUPLICATE,False,p)
        if 0<delta<SERIAL_HALF and m.source_uptime_s<s.last_source_uptime:
            s.metrics.out_of_order_packets+=1
            return ObservationResult(m.source_id,PacketDisposition.UPTIME_REGRESSION,False,p)
        if 0<delta<SERIAL_HALF:
            missing=delta-1; s.metrics.inferred_missing_packets+=missing; s.last_sequence=m.sequence; s.last_source_uptime=m.source_uptime_s; s.last_receive_time=now
            r=self._deliver_or_suppress_event(s,p,False)
            return ObservationResult(r.source_id,r.disposition,r.delivered,r.packet,r.error,missing,False)
        s.metrics.out_of_order_packets+=1
        return ObservationResult(m.source_id,PacketDisposition.OUT_OF_ORDER,False,p)
    def _deliver_or_suppress_event(self,s:SourceObservation,p:DecodedPacket,session_changed:bool)->ObservationResult:
        if p.message_type==MessageType.EVENT:
            ev=p.message; assert isinstance(ev,Event); key=(p.meta.session_id,ev.event_reference)
            if key in s.delivered_event_refs: return ObservationResult(p.meta.source_id,PacketDisposition.EVENT_DUPLICATE,False,p,session_changed=session_changed)
            s.delivered_event_refs.add(key)
        s.latest_semantic[p.message_type]=p
        return ObservationResult(p.meta.source_id,PacketDisposition.ACCEPTED,True,p,session_changed=session_changed)
    def metrics(self,source_id:int)->dict:
        s=self.sources.get(source_id)
        if s is None: return {'valid_packets':0,'invalid_packets':self.invalid_packets_total,'duplicate_packets':0,'out_of_order_packets':0,'inferred_missing_packets':0,'session_changes':0,'current_link_state':LinkState.NO_DATA.value,'last_valid_age':None}
        return {'valid_packets':s.metrics.valid_packets,'invalid_packets':self.invalid_packets_total,'duplicate_packets':s.metrics.duplicate_packets,'out_of_order_packets':s.metrics.out_of_order_packets,'inferred_missing_packets':s.metrics.inferred_missing_packets,'session_changes':s.metrics.session_changes,'current_link_state':self.link_state(source_id).value,'last_valid_age':self.last_valid_age(source_id)}
