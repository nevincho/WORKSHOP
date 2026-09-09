import inspect
import unittest
from mission_context_contract import *

def stamp(owner, rev=1, source="AUTH"):
    return AuthorityStamp(owner, source, rev)

class MissionContextTests(unittest.TestCase):
    def test_01_initial_context_fail_closed(self):
        m=map_to_m1_context(MissionContext())
        self.assertFalse(m.authoritative)
        self.assertEqual((m.mission_active,m.operator_intent,m.system_ready,m.safety_available),(False,OperatorIntent.NONE,False,False))
        self.assertEqual(len(m.reasons),4)

    def test_02_explicit_four_authorities_map(self):
        s=MissionContextStore()
        s.set_mission_active(True,stamp(AuthorityOwner.MISSION_ACTIVATION))
        s.set_operator_intent(OperatorIntent.TRACK,stamp(AuthorityOwner.OPERATOR_INTENT))
        s.set_system_ready(True,stamp(AuthorityOwner.SYSTEM_READINESS))
        s.set_safety_available(True,stamp(AuthorityOwner.SAFETY_AVAILABILITY))
        m=map_to_m1_context(s.context)
        self.assertTrue(m.authoritative)
        self.assertEqual((m.mission_active,m.operator_intent,m.system_ready,m.safety_available),(True,OperatorIntent.TRACK,True,True))

    def test_03_mission_activation_not_inferred(self):
        s=MissionContextStore()
        s.set_operator_intent(OperatorIntent.TRACK,stamp(AuthorityOwner.OPERATOR_INTENT))
        m=map_to_m1_context(s.context)
        self.assertFalse(m.mission_active)
        self.assertEqual(m.operator_intent,OperatorIntent.NONE)

    def test_04_operator_intent_not_inferred(self):
        s=MissionContextStore()
        s.set_mission_active(True,stamp(AuthorityOwner.MISSION_ACTIVATION))
        self.assertEqual(map_to_m1_context(s.context).operator_intent,OperatorIntent.NONE)

    def test_05_readiness_not_inferred(self):
        s=MissionContextStore()
        s.set_mission_active(True,stamp(AuthorityOwner.MISSION_ACTIVATION))
        self.assertFalse(map_to_m1_context(s.context).system_ready)

    def test_06_safety_not_inferred(self):
        s=MissionContextStore()
        s.set_system_ready(True,stamp(AuthorityOwner.SYSTEM_READINESS))
        self.assertFalse(map_to_m1_context(s.context).safety_available)

    def test_07_owner_mismatch_rejected(self):
        with self.assertRaisesRegex(ValueError,"authority_owner_mismatch"):
            MissionContextStore().set_system_ready(True,stamp(AuthorityOwner.SAFETY_AVAILABILITY))

    def test_08_missing_source_rejected(self):
        with self.assertRaisesRegex(ValueError,"authority_source_ref_required"):
            MissionContextStore().set_mission_active(True,AuthorityStamp(AuthorityOwner.MISSION_ACTIVATION,"",1))

    def test_09_non_monotonic_revision_rejected(self):
        s=MissionContextStore(); s.set_mission_active(True,stamp(AuthorityOwner.MISSION_ACTIVATION,2))
        with self.assertRaisesRegex(ValueError,"authority_revision_not_monotonic"):
            s.set_mission_active(False,stamp(AuthorityOwner.MISSION_ACTIVATION,2))

    def test_10_source_change_requires_reset(self):
        s=MissionContextStore(); s.set_mission_active(True,stamp(AuthorityOwner.MISSION_ACTIVATION,1,"A"))
        with self.assertRaisesRegex(ValueError,"authority_source_change_requires_reset"):
            s.set_mission_active(False,stamp(AuthorityOwner.MISSION_ACTIVATION,2,"B"))

    def test_11_reset_drops_all_authority(self):
        s=MissionContextStore()
        s.set_mission_active(True,stamp(AuthorityOwner.MISSION_ACTIVATION))
        s.reset_authorities()
        self.assertFalse(map_to_m1_context(s.context).authoritative)

    def test_12_explicit_false_is_authoritative(self):
        s=MissionContextStore()
        s.set_mission_active(False,stamp(AuthorityOwner.MISSION_ACTIVATION))
        s.set_operator_intent(OperatorIntent.NONE,stamp(AuthorityOwner.OPERATOR_INTENT))
        s.set_system_ready(False,stamp(AuthorityOwner.SYSTEM_READINESS))
        s.set_safety_available(False,stamp(AuthorityOwner.SAFETY_AVAILABILITY))
        m=map_to_m1_context(s.context)
        self.assertTrue(m.authoritative)
        self.assertFalse(m.mission_active)
        self.assertFalse(m.system_ready)
        self.assertFalse(m.safety_available)

    def test_13_bad_boolean_rejected(self):
        with self.assertRaises(TypeError):
            MissionContextStore().set_system_ready(1,stamp(AuthorityOwner.SYSTEM_READINESS))

    def test_14_bad_operator_intent_rejected(self):
        with self.assertRaises(TypeError):
            MissionContextStore().set_operator_intent("TRACK",stamp(AuthorityOwner.OPERATOR_INTENT))

    def test_15_no_production_authority(self):
        self.assertFalse(map_to_m1_context(MissionContext()).production_authority)

    def test_16_no_control_transport_side_effects(self):
        src=inspect.getsource(__import__('mission_context_contract')).lower()
        for forbidden in ("import serial","import socket","uart","lora","esp_now","esp-now","pwm","dshot","pid","mixer","esc","arm(","takeoff(","land("):
            self.assertNotIn(forbidden,src)

    def test_17_contract_does_not_accept_target_or_horos_inputs(self):
        sig=inspect.signature(MissionContext)
        for forbidden in ("target","detector","horos","t7","telemetry","connectivity"):
            self.assertFalse(any(forbidden in name.lower() for name in sig.parameters))

    def test_18_mapping_is_deterministic(self):
        c=MissionContext()
        self.assertEqual(map_to_m1_context(c),map_to_m1_context(c))

    def test_19_partial_context_preserves_only_safety_conservative_intent(self):
        for intent in (OperatorIntent.ABORT, OperatorIntent.HOLD):
            s=MissionContextStore()
            s.set_operator_intent(intent,stamp(AuthorityOwner.OPERATOR_INTENT))
            self.assertEqual(map_to_m1_context(s.context).operator_intent,intent)
        for intent in (OperatorIntent.TRACK,OperatorIntent.OBSERVE,OperatorIntent.COMPLETE):
            s=MissionContextStore()
            s.set_operator_intent(intent,stamp(AuthorityOwner.OPERATOR_INTENT))
            self.assertEqual(map_to_m1_context(s.context).operator_intent,OperatorIntent.NONE)

if __name__=="__main__":
    unittest.main()
