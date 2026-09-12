from __future__ import annotations
import struct
from dataclasses import replace
from typing import Type
from .models import *

MAGIC = b'TG'
VERSION = 1
MAX_PACKET_SIZE = 192
FLAG_TIMESTAMP = 0x01
KNOWN_ENV_FLAGS = FLAG_TIMESTAMP
PAYLOAD_EXT = 0x80
HEADER_FMT = '>2sBBBHIHIB'  # magic,ver,type,flags,source,session,seq,uptime,payload_len
HEADER_SIZE = struct.calcsize(HEADER_FMT)  # 18
CRC_SIZE = 2

ERR_EMPTY='EMPTY'; ERR_TRUNCATED='TRUNCATED'; ERR_OVERSIZED='OVERSIZED'; ERR_MAGIC='BAD_MAGIC'; ERR_VERSION='UNSUPPORTED_VERSION'; ERR_TYPE='UNKNOWN_TYPE'; ERR_FLAGS='INVALID_FLAGS'; ERR_LENGTH='BAD_LENGTH'; ERR_CRC='BAD_CRC'; ERR_PAYLOAD='INVALID_PAYLOAD'; ERR_ENUM='INVALID_ENUM'; ERR_TRAILING='TRAILING_GARBAGE'

class CodecError(ValueError): pass

def crc16_ccitt_false(data: bytes) -> int:
    crc = 0xFFFF
    for b in data:
        crc ^= b << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return crc

def _check_uint(name, value, maxv):
    if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= maxv: raise CodecError(f'{name}_RANGE')

def _q_u16(name, value, scale):
    if not isinstance(value,(int,float)) or isinstance(value,bool): raise CodecError(f'{name}_TYPE')
    q=round(value/scale)
    if not 0<=q<=0xFFFF: raise CodecError(f'{name}_RANGE')
    return q

def _q_i16(name, value, scale):
    if not isinstance(value,(int,float)) or isinstance(value,bool): raise CodecError(f'{name}_TYPE')
    q=round(value/scale)
    if not -32768<=q<=32767: raise CodecError(f'{name}_RANGE')
    return q

def _q_i32(name, value, scale):
    if not isinstance(value,(int,float)) or isinstance(value,bool): raise CodecError(f'{name}_TYPE')
    q=round(value/scale)
    if not -2147483648<=q<=2147483647: raise CodecError(f'{name}_RANGE')
    return q

def _q_u32(name, value, scale):
    if not isinstance(value,(int,float)) or isinstance(value,bool): raise CodecError(f'{name}_TYPE')
    q=round(value/scale)
    if not 0<=q<=0xFFFFFFFF: raise CodecError(f'{name}_RANGE')
    return q

def _ref(ref: bytes, max_len: int = MAX_REF_LEN) -> bytes:
    if not isinstance(ref,(bytes,bytearray)): raise CodecError('REF_TYPE')
    ref=bytes(ref)
    if not 1<=len(ref)<=max_len: raise CodecError('REF_LEN')
    return bytes([len(ref)])+ref

def _read_ref(data: bytes, off: int, max_len: int = MAX_REF_LEN):
    if off>=len(data): raise CodecError('REF_TRUNCATED')
    n=data[off]; off+=1
    if not 1<=n<=max_len or off+n>len(data): raise CodecError('REF_LEN')
    return data[off:off+n], off+n

def _enum(cls: Type[IntEnum], value: int):
    try: return cls(value)
    except ValueError: raise CodecError('ENUM')

def _strip_extensions(payload: bytes, known_end: int, flags: int):
    if flags & PAYLOAD_EXT:
        if known_end>=len(payload): raise CodecError('EXT_TRUNCATED')
        ext_len=payload[known_end]; known_end+=1
        if known_end+ext_len!=len(payload): raise CodecError('EXT_LENGTH')
        end=known_end+ext_len; p=known_end
        while p<end:
            if p+2>end: raise CodecError('EXT_TLV_TRUNCATED')
            l=payload[p+1]; p+=2
            if p+l>end: raise CodecError('EXT_TLV_LENGTH')
            p+=l
        return
    if known_end != len(payload): raise CodecError('TRAILING')

def _encode_heartbeat(m: Heartbeat) -> bytes:
    if m.runtime_uptime_s < 0 or m.runtime_uptime_s > 0xFFFFFFFF: raise CodecError('UPTIME_RANGE')
    flags=1 if m.active_track_count is not None else 0
    p=bytearray([flags, int(m.runtime_state)])
    p += struct.pack('>HHhHBBB', _q_u16('CPU',m.cpu_usage,.1), _q_u16('RAM',m.ram_usage,.1), _q_i16('TEMP',m.cpu_temperature,.1), _q_u16('FPS',m.runtime_fps,.1), int(m.hq_state), int(m.detector_state), int(m.ca_authority))
    if m.active_track_count is not None:
        _check_uint('ACTIVE_TRACKS',m.active_track_count,255); p.append(m.active_track_count)
    return bytes(p)

def _decode_heartbeat(p: bytes, uptime: int):
    if len(p)<13: raise CodecError('HB_TRUNCATED')
    flags=p[0]
    if flags & ~0x81: raise CodecError('FLAGS')
    runtime=_enum(RuntimeState,p[1])
    cpu,ram,temp,fps,hq,det,ca=struct.unpack_from('>HHhHBBB',p,2); off=13
    active=None
    if flags&1:
        if off>=len(p): raise CodecError('HB_ACTIVE_TRUNCATED')
        active=p[off]; off+=1
    _strip_extensions(p,off,flags)
    return Heartbeat(runtime, uptime, round(cpu*.1,1), round(ram*.1,1), round(temp*.1,1), round(fps*.1,1), _enum(HQState,hq), _enum(DetectorState,det), _enum(CAAuthority,ca), active)

def _encode_target(m: Target):
    flags=(1 if m.target_class is not None else 0)|(2 if m.continuity_state is not None else 0)
    p=bytearray([flags]); p+=_ref(m.target_ref,MAX_TARGET_REF_LEN); p+=bytes([int(m.identity_provenance),int(m.tracking_state)])
    if m.target_class is not None: _check_uint('TARGET_CLASS',m.target_class,65535); p+=struct.pack('>H',m.target_class)
    if m.continuity_state is not None: p.append(int(m.continuity_state))
    return bytes(p)

def _decode_target(p: bytes):
    if len(p)<5: raise CodecError('TARGET_TRUNCATED')
    flags=p[0]
    if flags & ~0x83: raise CodecError('FLAGS')
    ref,off=_read_ref(p,1,MAX_TARGET_REF_LEN)
    if off+2>len(p): raise CodecError('TARGET_TRUNCATED')
    prov=_enum(IdentityProvenance,p[off]); track=_enum(TrackingState,p[off+1]); off+=2
    cls=None; cont=None
    if flags&1:
        if off+2>len(p): raise CodecError('TARGET_CLASS_TRUNCATED')
        cls=struct.unpack_from('>H',p,off)[0]; off+=2
    if flags&2:
        if off>=len(p): raise CodecError('TARGET_CONT_TRUNCATED')
        cont=_enum(ContinuityState,p[off]); off+=1
    _strip_extensions(p,off,flags)
    return Target(ref,prov,track,cls,cont)

def _encode_spatial(m: Spatial):
    flags=(1 if m.xyz_m is not None else 0)|(2 if m.velocity_mps is not None else 0)|(4 if m.range_m is not None else 0)|(8 if m.uncertainty_m is not None else 0)
    _check_uint('OBS_REF',m.observation_reference,0xFFFFFFFF)
    p=bytearray([flags]); p+=_ref(m.target_ref,MAX_TARGET_REF_LEN); p+=struct.pack('>IBBBB',m.observation_reference,1 if m.metric_usable else 0,int(m.physical_metric_state),int(m.validity),int(m.spatial_provenance))
    if m.xyz_m is not None:
        if len(m.xyz_m)!=3: raise CodecError('XYZ_SHAPE')
        p+=struct.pack('>iii',*[_q_i32('XYZ',v,.01) for v in m.xyz_m])
    if m.velocity_mps is not None:
        if len(m.velocity_mps)!=3: raise CodecError('VEL_SHAPE')
        p+=struct.pack('>hhh',*[_q_i16('VEL',v,.01) for v in m.velocity_mps])
    if m.range_m is not None: p+=struct.pack('>I',_q_u32('RANGE',m.range_m,.01))
    if m.uncertainty_m is not None: p+=struct.pack('>H',_q_u16('UNCERTAINTY',m.uncertainty_m,.01))
    return bytes(p)

def _decode_spatial(p: bytes):
    if len(p)<11: raise CodecError('SPATIAL_TRUNCATED')
    flags=p[0]
    if flags & ~0x8F: raise CodecError('FLAGS')
    ref,off=_read_ref(p,1,MAX_TARGET_REF_LEN)
    if off+8>len(p): raise CodecError('SPATIAL_TRUNCATED')
    obs,metric,physical,validity,prov=struct.unpack_from('>IBBBB',p,off); off+=8
    if metric not in (0,1): raise CodecError('BOOL')
    xyz=vel=rng=unc=None
    if flags&1:
        if off+12>len(p): raise CodecError('XYZ_TRUNCATED')
        xyz=tuple(round(v*.01,2) for v in struct.unpack_from('>iii',p,off)); off+=12
    if flags&2:
        if off+6>len(p): raise CodecError('VEL_TRUNCATED')
        vel=tuple(round(v*.01,2) for v in struct.unpack_from('>hhh',p,off)); off+=6
    if flags&4:
        if off+4>len(p): raise CodecError('RANGE_TRUNCATED')
        rng=round(struct.unpack_from('>I',p,off)[0]*.01,2); off+=4
    if flags&8:
        if off+2>len(p): raise CodecError('UNC_TRUNCATED')
        unc=round(struct.unpack_from('>H',p,off)[0]*.01,2); off+=2
    _strip_extensions(p,off,flags)
    return Spatial(ref,obs,bool(metric),_enum(PhysicalMetricState,physical),_enum(ValidityState,validity),_enum(SpatialProvenance,prov),xyz,vel,rng,unc)

def _encode_event(m: Event):
    _check_uint('EVENT_TYPE',m.event_type,65535); _check_uint('EVENT_REF',m.event_reference,0xFFFFFFFF)
    if m.event_type==0: raise CodecError('EVENT_TYPE_RESERVED')
    flags=(1 if m.subject_ref is not None else 0)|(2 if m.payload is not None else 0)
    p=bytearray([flags]); p+=struct.pack('>HI',m.event_type,m.event_reference)
    if m.subject_ref is not None: p+=_ref(m.subject_ref)
    if m.payload is not None:
        if not isinstance(m.payload,(bytes,bytearray)) or len(m.payload)>MAX_EVENT_PAYLOAD: raise CodecError('EVENT_PAYLOAD')
        p+=bytes([len(m.payload)])+bytes(m.payload)
    return bytes(p)

def _decode_event(p: bytes):
    if len(p)<7: raise CodecError('EVENT_TRUNCATED')
    flags=p[0]
    if flags & ~0x83: raise CodecError('FLAGS')
    et,er=struct.unpack_from('>HI',p,1); off=7
    if et==0: raise CodecError('EVENT_TYPE_RESERVED')
    subject=payload=None
    if flags&1: subject,off=_read_ref(p,off)
    if flags&2:
        if off>=len(p): raise CodecError('EVENT_PAYLOAD_TRUNCATED')
        n=p[off]; off+=1
        if n>MAX_EVENT_PAYLOAD or off+n>len(p): raise CodecError('EVENT_PAYLOAD_LEN')
        payload=p[off:off+n]; off+=n
    _strip_extensions(p,off,flags)
    return Event(et,er,subject,payload)

def _encode_diag(m: Diagnostic):
    if len(m.records)>MAX_DIAG_RECORDS: raise CodecError('DIAG_COUNT')
    p=bytearray([0,int(m.diagnostic_type),len(m.records)])
    seen=set()
    for r in m.records:
        if r.metric in seen: raise CodecError('DIAG_DUP_METRIC')
        seen.add(r.metric)
        if not -2147483648<=r.value<=2147483647: raise CodecError('DIAG_VALUE')
        p.append(int(r.metric)); p+=struct.pack('>i',r.value)
    return bytes(p)

def _decode_diag(p: bytes):
    if len(p)<3: raise CodecError('DIAG_TRUNCATED')
    flags=p[0]
    if flags & ~0x80: raise CodecError('FLAGS')
    dtype=_enum(DiagnosticType,p[1]); n=p[2]
    if n>MAX_DIAG_RECORDS: raise CodecError('DIAG_COUNT')
    off=3; rec=[]; seen=set()
    for _ in range(n):
        if off+5>len(p): raise CodecError('DIAG_REC_TRUNCATED')
        metric=_enum(DiagnosticMetric,p[off]); val=struct.unpack_from('>i',p,off+1)[0]; off+=5
        if metric in seen: raise CodecError('DIAG_DUP_METRIC')
        seen.add(metric); rec.append(DiagnosticRecord(metric,val))
    _strip_extensions(p,off,flags)
    return Diagnostic(dtype,tuple(rec))

ENCODERS={Heartbeat:(MessageType.HEARTBEAT,_encode_heartbeat),Target:(MessageType.TARGET,_encode_target),Spatial:(MessageType.SPATIAL,_encode_spatial),Event:(MessageType.EVENT,_encode_event),Diagnostic:(MessageType.DIAGNOSTIC,_encode_diag)}
DECODERS={MessageType.HEARTBEAT:_decode_heartbeat,MessageType.TARGET:_decode_target,MessageType.SPATIAL:_decode_spatial,MessageType.EVENT:_decode_event,MessageType.DIAGNOSTIC:_decode_diag}

def encode(meta: EnvelopeMeta, message: SemanticMessage) -> bytes:
    if type(message) not in ENCODERS: raise CodecError('MESSAGE_TYPE')
    _check_uint('SOURCE_ID',meta.source_id,0xFFFF); _check_uint('SESSION_ID',meta.session_id,0xFFFFFFFF); _check_uint('SEQUENCE',meta.sequence,0xFFFF); _check_uint('UPTIME',meta.source_uptime_s,0xFFFFFFFF)
    if isinstance(message,Heartbeat) and message.runtime_uptime_s != meta.source_uptime_s: raise CodecError('HEARTBEAT_UPTIME_MISMATCH')
    mt,enc=ENCODERS[type(message)]; payload=enc(message)
    flags=0; ts=b''
    if meta.source_timestamp_ms is not None:
        _check_uint('TIMESTAMP',meta.source_timestamp_ms,0xFFFFFFFF); flags|=FLAG_TIMESTAMP; ts=struct.pack('>I',meta.source_timestamp_ms)
    header=struct.pack(HEADER_FMT,MAGIC,VERSION,int(mt),flags,meta.source_id,meta.session_id,meta.sequence,meta.source_uptime_s,len(payload))
    body=header+ts+payload
    if len(body)+2>MAX_PACKET_SIZE: raise CodecError('PACKET_OVERSIZED')
    return body+struct.pack('>H',crc16_ccitt_false(body))

def decode(data: bytes) -> DecodeResult:
    try:
        if not isinstance(data,(bytes,bytearray,memoryview)): return DecodeResult(False,error=ERR_PAYLOAD)
        data=bytes(data)
        if not data: return DecodeResult(False,error=ERR_EMPTY)
        if len(data)>MAX_PACKET_SIZE: return DecodeResult(False,error=ERR_OVERSIZED)
        if len(data)<HEADER_SIZE+CRC_SIZE: return DecodeResult(False,error=ERR_TRUNCATED)
        magic,ver,mt_raw,flags,source,session,seq,uptime,payload_len=struct.unpack_from(HEADER_FMT,data,0)
        if magic!=MAGIC: return DecodeResult(False,error=ERR_MAGIC)
        if ver!=VERSION: return DecodeResult(False,error=ERR_VERSION)
        try: mt=MessageType(mt_raw)
        except ValueError: return DecodeResult(False,error=ERR_TYPE)
        if flags & ~KNOWN_ENV_FLAGS: return DecodeResult(False,error=ERR_FLAGS)
        off=HEADER_SIZE; timestamp=None
        if flags&FLAG_TIMESTAMP:
            if off+4+CRC_SIZE>len(data): return DecodeResult(False,error=ERR_TRUNCATED)
            timestamp=struct.unpack_from('>I',data,off)[0]; off+=4
        expected=off+payload_len+CRC_SIZE
        if expected!=len(data): return DecodeResult(False,error=ERR_LENGTH)
        got=struct.unpack_from('>H',data,len(data)-2)[0]
        if crc16_ccitt_false(data[:-2])!=got: return DecodeResult(False,error=ERR_CRC)
        payload=data[off:-2]
        try:
            msg=_decode_heartbeat(payload,uptime) if mt==MessageType.HEARTBEAT else DECODERS[mt](payload)
        except CodecError as e:
            if str(e)=='ENUM': return DecodeResult(False,error=ERR_ENUM)
            if str(e)=='TRAILING': return DecodeResult(False,error=ERR_TRAILING)
            return DecodeResult(False,error=ERR_PAYLOAD)
        return DecodeResult(True,DecodedPacket(EnvelopeMeta(source,session,seq,uptime,timestamp),mt,msg))
    except Exception:
        return DecodeResult(False,error=ERR_PAYLOAD)
