import inspect
import unittest
from mission_context_contract import *

def stamp(owner, rev=1, source="AUTH"):
    return AuthorityStamp(owner, source, rev)

def valid_direct(intent=OperatorIntent.TRACK):
    return MissionContext(
        mission_active=True,
        operator_intent=intent,
        system_ready=True,
        safety_available=True,
        mission_active_stamp=stamp(AuthorityOwner.MISSION_ACTIVATION),
        operator_intent_stamp=stamp(AuthorityOwner.OPERATOR_INTENT),
        system_ready_stamp=stamp(AuthorityOwner.SYSTEM_READINESS),
        safety_available_stamp=stamp(AuthorityOwner.SAFETY_AVAILABILITY),
    )

class MissionContextTests(unittest.TestCase):
    def test_01_initial_context_fail_closed(self):
        m=map_to_m1_context(MissionContext())
        self.assertFalse(m.authoritative)
        self.assertEqual((m.mission_active,m.operator_intent,m.system_ready,m.safety_available),(False,OperatorIntent.NONE,False,False))

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
        s=MissionContextStore(); s.set_operator_intent(OperatorIntent.TRACK,stamp(AuthorityOwner.OPERATOR_INTENT))
        m=map_to_m1_context(s.context)
        self.assertFalse(m.mission_active); self.assertEqual(m.operator_intent,OperatorIntent.NONE)

    def test_04_operator_intent_not_inferred(self):
        s=MissionContextStore(); s.set_mission_active(True,stamp(AuthorityOwner.MISSION_ACTIVATION))
        self.assertEqual(map_to_m1_context(s.context).operator_intent,OperatorIntent.NONE)

    def test_05_readiness_not_inferred(self):
        s=MissionContextStore(); s.set_mission_active(True,stamp(AuthorityOwner.MISSION_ACTIVATION))
        self.assertFalse(map_to_m1_context(s.context).system_ready)

    def test_06_safety_not_inferred(self):
        s=MissionContextStore(); s.set_system_ready(True,stamp(AuthorityOwner.SYSTEM_READINESS))
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
        s=MissionContextStore(); s.set_mission_active(True,stamp(AuthorityOwner.MISSION_ACTIVATION)); s.reset_authorities()
        self.assertFalse(map_to_m1_context(s.context).authoritative)

    def test_12_explicit_false_is_authoritative(self):
        s=MissionContextStore()
        s.set_mission_active(False,stamp(AuthorityOwner.MISSION_ACTIVATION))
        s.set_operator_intent(OperatorIntent.NONE,stamp(AuthorityOwner.OPERATOR_INTENT))
        s.set_system_ready(False,stamp(AuthorityOwner.SYSTEM_READINESS))
        s.set_safety_available(False,stamp(AuthorityOwner.SAFETY_AVAILABILITY))
        m=map_to_m1_context(s.context)
        self.assertTrue(m.authoritative); self.assertFalse(m.mission_active); self.assertFalse(m.system_ready); self.assertFalse(m.safety_available)

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
            s=MissionContextStore(); s.set_operator_intent(intent,stamp(AuthorityOwner.OPERATOR_INTENT))
            self.assertEqual(map_to_m1_context(s.context).operator_intent,intent)
        for intent in (OperatorIntent.TRACK,OperatorIntent.OBSERVE,OperatorIntent.COMPLETE):
            s=MissionContextStore(); s.set_operator_intent(intent,stamp(AuthorityOwner.OPERATOR_INTENT))
            self.assertEqual(map_to_m1_context(s.context).operator_intent,OperatorIntent.NONE)

    def test_20_direct_wrong_owner_all_stamps_fails_closed(self):
        c=valid_direct()
        c=MissionContext(c.mission_active,c.operator_intent,c.system_ready,c.safety_available,
            stamp(AuthorityOwner.SAFETY_AVAILABILITY),stamp(AuthorityOwner.MISSION_ACTIVATION),
            stamp(AuthorityOwner.OPERATOR_INTENT),stamp(AuthorityOwner.SYSTEM_READINESS))
        m=map_to_m1_context(c)
        self.assertFalse(m.authoritative)
        self.assertEqual((m.mission_active,m.operator_intent,m.system_ready,m.safety_available),(False,OperatorIntent.NONE,False,False))

    def test_21_direct_wrong_owner_one_stamp_fails_closed(self):
        c=valid_direct()
        c=MissionContext(c.mission_active,c.operator_intent,c.system_ready,c.safety_available,
            c.mission_active_stamp,c.operator_intent_stamp,c.system_ready_stamp,stamp(AuthorityOwner.SYSTEM_READINESS))
        self.assertFalse(map_to_m1_context(c).authoritative)

    def test_22_direct_empty_source_ref_fails_closed(self):
        c=valid_direct()
        c=MissionContext(c.mission_active,c.operator_intent,c.system_ready,c.safety_available,
            AuthorityStamp(AuthorityOwner.MISSION_ACTIVATION,"",1),c.operator_intent_stamp,c.system_ready_stamp,c.safety_available_stamp)
        self.assertFalse(map_to_m1_context(c).authoritative)

    def test_23_direct_invalid_revision_fails_closed(self):
        for rev in (-1, True, "1"):
            c=valid_direct()
            c=MissionContext(c.mission_active,c.operator_intent,c.system_ready,c.safety_available,
                AuthorityStamp(AuthorityOwner.MISSION_ACTIVATION,"AUTH",rev),c.operator_intent_stamp,c.system_ready_stamp,c.safety_available_stamp)
            self.assertFalse(map_to_m1_context(c).authoritative)

    def test_24_direct_mission_active_wrong_type_fails_closed(self):
        c=valid_direct()
        c=MissionContext(1,c.operator_intent,c.system_ready,c.safety_available,c.mission_active_stamp,c.operator_intent_stamp,c.system_ready_stamp,c.safety_available_stamp)
        self.assertFalse(map_to_m1_context(c).authoritative)

    def test_25_direct_system_ready_wrong_type_fails_closed(self):
        c=valid_direct()
        c=MissionContext(c.mission_active,c.operator_intent,"yes",c.safety_available,c.mission_active_stamp,c.operator_intent_stamp,c.system_ready_stamp,c.safety_available_stamp)
        self.assertFalse(map_to_m1_context(c).authoritative)

    def test_26_direct_safety_available_wrong_type_fails_closed(self):
        c=valid_direct()
        c=MissionContext(c.mission_active,c.operator_intent,c.system_ready,1,c.mission_active_stamp,c.operator_intent_stamp,c.system_ready_stamp,c.safety_available_stamp)
        self.assertFalse(map_to_m1_context(c).authoritative)

    def test_27_direct_operator_intent_wrong_type_fails_closed(self):
        c=valid_direct()
        c=MissionContext(c.mission_active,"TRACK",c.system_ready,c.safety_available,c.mission_active_stamp,c.operator_intent_stamp,c.system_ready_stamp,c.safety_available_stamp)
        m=map_to_m1_context(c); self.assertFalse(m.authoritative); self.assertEqual(m.operator_intent,OperatorIntent.NONE)

    def test_28_direct_mixed_valid_and_forged_stamps_fails_closed(self):
        c=valid_direct()
        c=MissionContext(c.mission_active,c.operator_intent,c.system_ready,c.safety_available,c.mission_active_stamp,
            AuthorityStamp(AuthorityOwner.OPERATOR_INTENT," ",2),c.system_ready_stamp,c.safety_available_stamp)
        m=map_to_m1_context(c); self.assertFalse(m.authoritative); self.assertEqual(m.operator_intent,OperatorIntent.NONE)

    def test_29_direct_missing_stamp_with_affirmative_value_fails_closed(self):
        c=valid_direct()
        c=MissionContext(c.mission_active,c.operator_intent,c.system_ready,c.safety_available,None,c.operator_intent_stamp,c.system_ready_stamp,c.safety_available_stamp)
        m=map_to_m1_context(c); self.assertFalse(m.authoritative); self.assertFalse(m.mission_active)

    def test_30_direct_fully_valid_context_passes(self):
        m=map_to_m1_context(valid_direct())
        self.assertTrue(m.authoritative); self.assertEqual(m.operator_intent,OperatorIntent.TRACK)

    def test_31_direct_forged_track_context_fails_closed(self):
        forged=MissionContext(True,OperatorIntent.TRACK,True,True,
            AuthorityStamp(AuthorityOwner.OPERATOR_INTENT,"",-1),
            AuthorityStamp(AuthorityOwner.MISSION_ACTIVATION,"",-1),
            AuthorityStamp(AuthorityOwner.SAFETY_AVAILABILITY,"",-1),
            AuthorityStamp(AuthorityOwner.SYSTEM_READINESS,"",-1))
        m=map_to_m1_context(forged)
        self.assertFalse(m.authoritative)
        self.assertEqual((m.mission_active,m.operator_intent,m.system_ready,m.safety_available),(False,OperatorIntent.NONE,False,False))

    def test_32_valid_authoritative_hold_behavior(self):
        m=map_to_m1_context(valid_direct(OperatorIntent.HOLD))
        self.assertTrue(m.authoritative); self.assertEqual(m.operator_intent,OperatorIntent.HOLD)

    def test_33_valid_authoritative_abort_behavior(self):
        m=map_to_m1_context(valid_direct(OperatorIntent.ABORT))
        self.assertTrue(m.authoritative); self.assertEqual(m.operator_intent,OperatorIntent.ABORT)

    def test_34_partial_valid_hold_preserved(self):
        c=MissionContext(operator_intent=OperatorIntent.HOLD,operator_intent_stamp=stamp(AuthorityOwner.OPERATOR_INTENT))
        m=map_to_m1_context(c); self.assertFalse(m.authoritative); self.assertEqual(m.operator_intent,OperatorIntent.HOLD)

    def test_35_partial_forged_hold_not_preserved(self):
        c=MissionContext(operator_intent=OperatorIntent.HOLD,operator_intent_stamp=stamp(AuthorityOwner.MISSION_ACTIVATION))
        m=map_to_m1_context(c); self.assertFalse(m.authoritative); self.assertEqual(m.operator_intent,OperatorIntent.NONE)

    def test_36_non_context_input_fails_closed_without_exception(self):
        m=map_to_m1_context(object())
        self.assertFalse(m.authoritative); self.assertEqual(m.operator_intent,OperatorIntent.NONE)

    def test_37_direct_valid_mapping_repeated_deterministic(self):
        c=valid_direct()
        self.assertEqual(map_to_m1_context(c),map_to_m1_context(c))

    def test_38_string_typed_authority_owner_fails_closed(self):
        c=MissionContext(
            True,OperatorIntent.TRACK,True,True,
            AuthorityStamp("MISSION_ACTIVATION_AUTHORITY","AUTH",1),
            AuthorityStamp("OPERATOR_INTENT_AUTHORITY","AUTH",1),
            AuthorityStamp("SYSTEM_READINESS_AUTHORITY","AUTH",1),
            AuthorityStamp("SAFETY_AVAILABILITY_AUTHORITY","AUTH",1),
        )
        m=map_to_m1_context(c)
        self.assertFalse(m.authoritative)
        self.assertEqual((m.mission_active,m.operator_intent,m.system_ready,m.safety_available),(False,OperatorIntent.NONE,False,False))

    def test_39_context_subclass_rejected_fail_closed(self):
        class DerivedMissionContext(MissionContext):
            pass
        c=DerivedMissionContext(
            True,OperatorIntent.TRACK,True,True,
            stamp(AuthorityOwner.MISSION_ACTIVATION),
            stamp(AuthorityOwner.OPERATOR_INTENT),
            stamp(AuthorityOwner.SYSTEM_READINESS),
            stamp(AuthorityOwner.SAFETY_AVAILABILITY),
        )
        m=map_to_m1_context(c)
        self.assertFalse(m.authoritative)
        self.assertEqual(m.operator_intent,OperatorIntent.NONE)

    def test_40_stamp_subclass_rejected_fail_closed(self):
        class DerivedStamp(AuthorityStamp):
            pass
        c=valid_direct()
        c=MissionContext(
            c.mission_active,c.operator_intent,c.system_ready,c.safety_available,
            DerivedStamp(AuthorityOwner.MISSION_ACTIVATION,"AUTH",1),
            c.operator_intent_stamp,c.system_ready_stamp,c.safety_available_stamp,
        )
        self.assertFalse(map_to_m1_context(c).authoritative)

if __name__=="__main__":
    unittest.main()
