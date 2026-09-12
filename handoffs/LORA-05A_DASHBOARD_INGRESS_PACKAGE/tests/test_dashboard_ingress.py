import os, sys, struct, unittest
THIS=os.path.abspath(os.path.dirname(__file__))
ROOT=os.path.abspath(os.path.join(THIS,'..'))
L02=os.environ['LORA02_PATH']
L03=os.environ['LORA03_PATH']
for p in (L02,L03,ROOT):
    if p not in sys.path: sys.path.insert(0,p)

from tangra_lora_v1 import *
from lora03_link import *
from dashboard_lora_ingress import *

SID=0x1234

def meta(seq, session=100, uptime=None, sid=SID):
    if uptime is None: uptime=seq
    return EnvelopeMeta(sid,session,seq,uptime,None)

def wire(seq,msg,session=100,uptime=None,sid=SID):
    return encode(meta(seq,session,uptime,sid),msg)

def with_unknown_tlv(packet, tag=0xE1, value=b'xy'):
    b=bytearray(packet); plen=b[17]; start=18; end=start+plen
    b[start] |= 0x80
    ext=bytes([2+len(value),tag,len(value)])+value
    b[end:end]=ext; b[17]=plen+len(ext)
    b[-2:]=struct.pack('>H',crc16_ccitt_false(bytes(b[:-2])))
    return bytes(b)

class IngressTests(unittest.TestCase):
    def setUp(self):
        self.clock=MockClock()
        self.obs=LinkObserver(self.clock,5,15)
        self.sink=InMemoryDashboardSink()
        self.ing=ByteIngress(self.obs,self.sink)

    def test_heartbeat_to_system(self):
        h=Heartbeat(RuntimeState.RUNNING,10,12.3,45.6,55.5,40.1,HQState.AVAILABLE,DetectorState.AVAILABLE,CAAuthority.CA_PRIMARY,2)
        r=self.ing.ingest(wire(1,h,uptime=10),0)
        self.assertTrue(r.accepted); u=self.sink.systems[SID]
        self.assertEqual(u.system.runtime_state,RuntimeState.RUNNING)
        self.assertEqual(u.system.runtime_uptime_s,10); self.assertEqual(u.system.active_track_count,2)
        self.assertEqual(u.transport,'LORA')

    def test_target_mapping_opaque_and_provenance(self):
        t=Target(b'\x00opaque\xff',IdentityProvenance.CURRENT_TARGET_ID,TrackingState.TRACKING,None,ContinuityState.ACTIVE)
        self.ing.ingest(wire(1,t),0); u=self.sink.targets[SID].target
        self.assertEqual(u.target_ref,b'\x00opaque\xff'); self.assertEqual(u.identity_provenance,IdentityProvenance.CURRENT_TARGET_ID)
        self.assertIsNone(u.target_class); self.assertEqual(u.continuity_state,ContinuityState.ACTIVE)

    def test_spatial_mapping_preserves_validity_provenance(self):
        s=Spatial(b't',9,True,PhysicalMetricState.PROVISIONAL,ValidityState.DEGRADED,SpatialProvenance.MONOCULAR_CLASS_SIZE,(1.2,2.3,3.4),(0.1,0.2,0.3),12.5,0.7)
        self.ing.ingest(wire(1,s),0); u=self.sink.spatials[SID].spatial
        self.assertEqual(u.validity,ValidityState.DEGRADED); self.assertEqual(u.spatial_provenance,SpatialProvenance.MONOCULAR_CLASS_SIZE)
        self.assertEqual(u.range_m,12.5); self.assertTrue(u.metric_usable)

    def test_invalid_metric_absence_preserved(self):
        s=Spatial(b't',10,False,PhysicalMetricState.UNAVAILABLE,ValidityState.INVALID,SpatialProvenance.HOROS)
        self.ing.ingest(wire(1,s),0); u=self.sink.spatials[SID].spatial
        self.assertFalse(u.metric_usable); self.assertEqual(u.validity,ValidityState.INVALID)
        self.assertIsNone(u.xyz_m); self.assertIsNone(u.range_m); self.assertIsNone(u.velocity_mps); self.assertIsNone(u.uncertainty_m)

    def test_event_exactly_once_same_packet(self):
        p=wire(1,Event(5,100,b't',b'x'))
        self.assertTrue(self.ing.ingest(p,0).accepted)
        self.assertFalse(self.ing.ingest(p,1).accepted)
        self.assertEqual(len(self.sink.events),1)

    def test_event_same_reference_new_sequence_suppressed(self):
        self.ing.ingest(wire(1,Event(5,100)),0)
        r=self.ing.ingest(wire(2,Event(5,100),uptime=2),1)
        self.assertFalse(r.accepted); self.assertEqual(r.disposition,'EVENT_DUPLICATE'); self.assertEqual(len(self.sink.events),1)

    def test_unknown_compatible_event_generic(self):
        p=with_unknown_tlv(wire(1,Event(0x4567,77)))
        r=self.ing.ingest(p,0); self.assertTrue(r.accepted)
        self.assertEqual(self.sink.events[0].event.event_type,0x4567)

    def test_diagnostic_mapping(self):
        d=Diagnostic(DiagnosticType.RUNTIME_TIMING,(DiagnosticRecord(DiagnosticMetric.LOOP_MS_X10,123),))
        self.ing.ingest(wire(1,d),0); u=self.sink.diagnostics[SID].diagnostic
        self.assertEqual(u.diagnostic_type,DiagnosticType.RUNTIME_TIMING); self.assertEqual(u.records[0].value,123)

    def test_duplicate_no_state_delivery(self):
        h1=Heartbeat(RuntimeState.RUNNING,1,1,1,1,1,HQState.AVAILABLE,DetectorState.AVAILABLE,CAAuthority.CA_PRIMARY)
        p=wire(1,h1,uptime=1); self.ing.ingest(p,0)
        before=self.sink.systems[SID]
        self.ing.ingest(p,1)
        self.assertIs(self.sink.systems[SID],before); self.assertEqual(self.sink.links[SID].link.duplicates,1)

    def test_late_target_no_overwrite(self):
        a=Target(b't',IdentityProvenance.OBJECT_ID,TrackingState.TRACKING)
        b=Target(b't',IdentityProvenance.OBJECT_ID,TrackingState.LOST)
        self.ing.ingest(wire(10,a,uptime=10),0); self.ing.ingest(wire(12,b,uptime=12),1)
        self.ing.ingest(wire(11,a,uptime=11),2)
        self.assertEqual(self.sink.targets[SID].target.tracking_state,TrackingState.LOST)

    def test_late_spatial_no_overwrite(self):
        a=Spatial(b't',1,True,PhysicalMetricState.PHYSICAL,ValidityState.VALID,SpatialProvenance.HOROS,range_m=10)
        b=Spatial(b't',2,True,PhysicalMetricState.PHYSICAL,ValidityState.VALID,SpatialProvenance.HOROS,range_m=20)
        self.ing.ingest(wire(10,a,uptime=10),0); self.ing.ingest(wire(12,b,uptime=12),1); self.ing.ingest(wire(11,a,uptime=11),2)
        self.assertEqual(self.sink.spatials[SID].spatial.range_m,20)

    def test_old_session_no_overwrite(self):
        a=Target(b't',IdentityProvenance.CURRENT_TARGET_ID,TrackingState.TRACKING)
        b=Target(b't',IdentityProvenance.CURRENT_TARGET_ID,TrackingState.LOST)
        self.ing.ingest(wire(10,a,session=1,uptime=10),0)
        self.ing.ingest(wire(0,b,session=2,uptime=0),1)
        r=self.ing.ingest(wire(11,a,session=1,uptime=11),2)
        self.assertFalse(r.accepted); self.assertEqual(r.disposition,'OLD_SESSION'); self.assertEqual(self.sink.targets[SID].target.tracking_state,TrackingState.LOST)

    def test_corrupt_no_dashboard_semantic_update(self):
        p=bytearray(wire(1,Event(1,1))); p[-3]^=1
        r=self.ing.ingest(bytes(p),0)
        self.assertFalse(r.accepted); self.assertEqual(len(self.sink.events),0); self.assertEqual(len(self.sink.systems),0)

    def test_unknown_incompatible_version_no_update(self):
        p=bytearray(wire(1,Event(1,1))); p[2]=2
        r=self.ing.ingest(bytes(p),0)
        self.assertFalse(r.accepted); self.assertEqual(r.error,'UNSUPPORTED_VERSION'); self.assertEqual(len(self.sink.events),0)

    def test_fresh_stale_disconnected_recovery(self):
        self.ing.ingest(wire(1,Event(1,1),uptime=1),0)
        self.assertEqual(self.sink.links[SID].link.link_state,'FRESH')
        self.ing.poll_links(5); self.assertEqual(self.sink.links[SID].link.link_state,'STALE')
        self.ing.poll_links(15); self.assertEqual(self.sink.links[SID].link.link_state,'DISCONNECTED')
        self.ing.ingest(wire(2,Event(1,2),uptime=2),16); self.assertEqual(self.sink.links[SID].link.link_state,'FRESH')

    def test_corruption_does_not_refresh_link(self):
        self.ing.ingest(wire(1,Event(1,1),uptime=1),0)
        bad=bytearray(wire(2,Event(1,2),uptime=2)); bad[-3]^=1
        self.ing.ingest(bytes(bad),4)
        self.ing.poll_links(5); self.assertEqual(self.sink.links[SID].link.link_state,'STALE')

    def test_multiple_sources_isolated(self):
        self.ing.ingest(wire(1,Event(1,1),sid=1,session=1,uptime=1),0)
        self.ing.ingest(wire(50,Event(1,2),sid=2,session=9,uptime=5),1)
        self.ing.ingest(wire(3,Event(1,3),sid=1,session=1,uptime=3),2)
        self.assertEqual(self.sink.links[1].link.inferred_missing_packets,1)
        self.assertEqual(self.sink.links[2].link.inferred_missing_packets,0)

    def test_optional_fields_absent(self):
        t=Target(b'x',IdentityProvenance.OTHER,TrackingState.DETECTED)
        self.ing.ingest(wire(1,t),0); u=self.sink.targets[SID].target
        self.assertIsNone(u.target_class); self.assertIsNone(u.continuity_state)

    def test_link_metrics_local_not_payload_dependency(self):
        p=wire(1,Event(1,1),uptime=1); self.ing.ingest(p,0)
        link=self.sink.links[SID]
        self.assertEqual(link.link.valid_packets,1); self.assertEqual(link.link.link_state,'FRESH'); self.assertIsNone(link.message_class)
        self.assertNotIn(b'lora_connected',p); self.assertNotIn(b'inferred_missing_packets',p)

    def test_transport_metadata_only_no_failover_policy(self):
        self.ing.ingest(wire(1,Event(1,1),uptime=1),0)
        u=self.sink.events[0]
        self.assertEqual(u.transport,'LORA'); self.assertEqual(u.source_id,SID); self.assertEqual(u.session_id,100)

    def test_receive_time_regression_rejected(self):
        self.ing.ingest(wire(1,Event(1,1),uptime=1),10)
        with self.assertRaises(ValueError): self.ing.ingest(wire(2,Event(1,2),uptime=2),9)

if __name__=='__main__': unittest.main()
