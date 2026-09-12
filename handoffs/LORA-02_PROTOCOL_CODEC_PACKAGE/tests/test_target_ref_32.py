import unittest
from tangra_lora_v1 import *

META=EnvelopeMeta(0x1234,0x89ABCDEF,42,12345,987654)

class TargetRef32CompatibilityTests(unittest.TestCase):
    def _rt(self,msg):
        wire=encode(META,msg); decoded=decode(wire)
        self.assertTrue(decoded.ok,decoded.error)
        return decoded.packet.message

    def test_target_ref_32_max(self):
        ref=b'x'*32
        self.assertEqual(self._rt(Target(ref,IdentityProvenance.CURRENT_TARGET_ID,TrackingState.TRACKING)).target_ref,ref)

    def test_target_ref_33_rejected(self):
        with self.assertRaises(CodecError):
            encode(META,Target(b'x'*33,IdentityProvenance.CURRENT_TARGET_ID,TrackingState.TRACKING))

    def test_current_target_0001_19_byte_roundtrip(self):
        ref=b'CURRENT_TARGET_0001'
        self.assertEqual(len(ref),19)
        target=Target(ref,IdentityProvenance.CURRENT_TARGET_ID,TrackingState.TRACKING)
        spatial=Spatial(ref,77,False,PhysicalMetricState.UNAVAILABLE,ValidityState.INVALID,SpatialProvenance.HOROS)
        self.assertEqual(self._rt(target).target_ref,ref)
        self.assertEqual(self._rt(spatial).target_ref,ref)

    def test_event_subject_ref_limit_unchanged(self):
        self.assertEqual(self._rt(Event(1,1,b'x'*16)).subject_ref,b'x'*16)
        with self.assertRaises(CodecError):
            encode(META,Event(1,1,b'x'*17))

if __name__=='__main__': unittest.main()
