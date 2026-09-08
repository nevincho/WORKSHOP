import unittest, math, inspect, importlib.util
from pathlib import Path
from passive_high_level_command_contract import *

repo_root=Path(__file__).resolve().parents[2]
m2_path=repo_root/'handoffs'/'TASK-TANGRA-MISSION-GUIDANCE-M2-20260908'/'passive_guidance_translation.py'
spec=importlib.util.spec_from_file_location('frozen_m2_reviewed',m2_path)
m2=importlib.util.module_from_spec(spec); spec.loader.exec_module(m2)

def gd(intent=m2.GuidanceIntent.MAINTAIN_OBSERVATION,state=m2.GuidanceState.AVAILABLE,
       metric=m2.MetricStatus.VERIFIED,target='T1',ts=10.0,frame='LOCAL',rel=None,alt=None,head=None):
    return m2.PassiveGuidanceDecision(state,intent,target,ts,frame,metric,'TRACK','MAINTAIN_TRACK','valid',rel,alt,head,'m2-test',(('m2','TEST'),),False,'M2_SHADOW_V1')

def tr(g=None,now=10.1,ctx=CommandContext()):
    return PassiveHighLevelCommandTranslator().translate(g or gd(),now,ctx)

class T(unittest.TestCase):
    def test_01_no_guidance(self): self.assertEqual(tr(gd(m2.GuidanceIntent.NO_GUIDANCE,m2.GuidanceState.SUPPRESSED)).command_type,CommandType.NO_COMMAND)
    def test_02_hold(self): self.assertEqual(tr(gd(m2.GuidanceIntent.HOLD)).command_type,CommandType.HOLD)
    def test_03_abort_hold(self):
        d=tr(gd(m2.GuidanceIntent.ABORT_HOLD)); self.assertEqual(d.command_type,CommandType.HOLD); self.assertTrue(d.abort_semantic)
    def test_04_observe_without_movement(self): self.assertEqual(tr(gd(m2.GuidanceIntent.MAINTAIN_OBSERVATION)).command_type,CommandType.NO_COMMAND)
    def test_05_reacquire_without_search(self): self.assertEqual(tr(gd(m2.GuidanceIntent.REACQUIRE_TARGET,state=m2.GuidanceState.DEGRADED)).command_type,CommandType.NO_COMMAND)
    def test_05b_reacquire_with_explicit_authoritative_geometry(self):
        d=tr(gd(m2.GuidanceIntent.REACQUIRE_TARGET,state=m2.GuidanceState.AVAILABLE,rel=(2.,0.,0.))); self.assertEqual((d.command_type,d.relative_vector_m),(CommandType.MOVE_RELATIVE,(2.,0.,0.)))
    def test_05c_maintain_observation_with_explicit_authoritative_geometry(self):
        d=tr(gd(m2.GuidanceIntent.MAINTAIN_OBSERVATION,state=m2.GuidanceState.AVAILABLE,rel=(0.5,0.,0.))); self.assertEqual((d.command_type,d.relative_vector_m),(CommandType.MOVE_RELATIVE,(0.5,0.,0.)))
    def test_05d_semantic_multiple_movement_parameters_rejected(self):
        d=tr(gd(m2.GuidanceIntent.REACQUIRE_TARGET,state=m2.GuidanceState.AVAILABLE,rel=(1.,0.,0.),head=90.)); self.assertEqual(d.command_type,CommandType.NO_COMMAND); self.assertEqual(d.reason,'ambiguous_semantic_movement_geometry')
    def test_06_move_relative_preserved(self):
        d=tr(gd(m2.GuidanceIntent.MOVE_RELATIVE,rel=(1.,-2.,3.))); self.assertEqual(d.relative_vector_m,(1.,-2.,3.)); self.assertEqual(d.command_type,CommandType.MOVE_RELATIVE)
    def test_07_altitude_preserved(self):
        d=tr(gd(m2.GuidanceIntent.SET_ALTITUDE,alt=22.5)); self.assertEqual((d.command_type,d.altitude_m),(CommandType.SET_ALTITUDE,22.5))
    def test_08_heading_preserved(self):
        d=tr(gd(m2.GuidanceIntent.SET_HEADING,head=270.)); self.assertEqual((d.command_type,d.heading_deg),(CommandType.SET_HEADING,270.))
    def test_09_missing_required_parameter(self):
        self.assertEqual(tr(gd(m2.GuidanceIntent.MOVE_RELATIVE)).command_type,CommandType.NO_COMMAND)
        self.assertEqual(tr(gd(m2.GuidanceIntent.SET_ALTITUDE)).command_type,CommandType.NO_COMMAND)
        self.assertEqual(tr(gd(m2.GuidanceIntent.SET_HEADING)).command_type,CommandType.NO_COMMAND)
    def test_10_nonfinite_parameter(self):
        self.assertEqual(tr(gd(m2.GuidanceIntent.MOVE_RELATIVE,rel=(1.,math.nan,3.))).state,CommandState.SUPPRESSED)
        self.assertEqual(tr(gd(m2.GuidanceIntent.SET_ALTITUDE,alt=math.inf)).state,CommandState.SUPPRESSED)
        self.assertEqual(tr(gd(m2.GuidanceIntent.SET_HEADING,head=math.nan)).state,CommandState.SUPPRESSED)
    def test_11_missing_reference_frame(self): self.assertEqual(tr(gd(m2.GuidanceIntent.MOVE_RELATIVE,frame=None,rel=(1.,2.,3.))).command_type,CommandType.NO_COMMAND)
    def test_12_frame_preservation_no_conversion(self):
        d=tr(gd(m2.GuidanceIntent.MOVE_RELATIVE,frame='BODY_NED',rel=(1.,2.,3.))); self.assertEqual(d.frame_ref,'BODY_NED'); self.assertEqual(d.relative_vector_m,(1.,2.,3.))
    def test_12b_source_reason_preserved(self):
        src=gd(m2.GuidanceIntent.HOLD); d=tr(src); self.assertEqual(d.source_guidance_reason,src.reason)
    def test_13_target_identity_mismatch(self):
        d=tr(gd(),ctx=CommandContext(previous_target_ref='OTHER',previous_timestamp=9.,previous_frame_ref='LOCAL')); self.assertEqual(d.reason,'target_identity_mismatch')
    def test_13b_frame_discontinuity(self):
        d=tr(gd(frame='BODY_NED'),ctx=CommandContext(previous_target_ref='T1',previous_timestamp=9.,previous_frame_ref='LOCAL')); self.assertEqual(d.reason,'frame_discontinuity')
    def test_14_stale(self): self.assertEqual(tr(gd(),now=11.).state,CommandState.SUPPRESSED)
    def test_15_timestamp_regression(self): self.assertEqual(tr(gd(ts=9.),now=9.1,ctx=CommandContext('T1',9.5,'LOCAL')).reason,'timestamp_regression')
    def test_16_suppressed_input(self): self.assertEqual(tr(gd(m2.GuidanceIntent.HOLD,state=m2.GuidanceState.SUPPRESSED)).command_type,CommandType.NO_COMMAND)
    def test_17_degraded_movement(self):
        d=tr(gd(m2.GuidanceIntent.MOVE_RELATIVE,state=m2.GuidanceState.DEGRADED,rel=(1.,2.,3.))); self.assertEqual(d.command_type,CommandType.NO_COMMAND)
    def test_18_not_verified(self):
        d=tr(gd(m2.GuidanceIntent.MOVE_RELATIVE,metric=m2.MetricStatus.NOT_VERIFIED,rel=(1.,2.,3.))); self.assertEqual(d.command_type,CommandType.NO_COMMAND)
    def test_19_unusable_conflict_invalid(self):
        for metric in (m2.MetricStatus.UNUSABLE,m2.MetricStatus.CONFLICT,m2.MetricStatus.INVALID): self.assertEqual(tr(gd(m2.GuidanceIntent.MOVE_RELATIVE,metric=metric,rel=(1.,2.,3.))).command_type,CommandType.NO_COMMAND)
    def test_20_determinism(self):
        a=tr(gd(m2.GuidanceIntent.MOVE_RELATIVE,rel=(1.,2.,3.))); b=tr(gd(m2.GuidanceIntent.MOVE_RELATIVE,rel=(1.,2.,3.))); self.assertEqual(a,b)
    def test_21_no_fabricated_movement_values(self):
        for intent in (m2.GuidanceIntent.NO_GUIDANCE,m2.GuidanceIntent.HOLD,m2.GuidanceIntent.ABORT_HOLD,m2.GuidanceIntent.MAINTAIN_OBSERVATION,m2.GuidanceIntent.REACQUIRE_TARGET):
            d=tr(gd(intent,state=m2.GuidanceState.DEGRADED if intent==m2.GuidanceIntent.REACQUIRE_TARGET else m2.GuidanceState.AVAILABLE)); self.assertIsNone(d.relative_vector_m); self.assertIsNone(d.altitude_m); self.assertIsNone(d.heading_deg)
    def test_22_no_coordinate_frame_conversion(self):
        src=gd(m2.GuidanceIntent.MOVE_RELATIVE,frame='CAMERA_LOCAL',rel=(4.,5.,6.)); d=tr(src); self.assertEqual(d.frame_ref,src.frame_ref); self.assertEqual(d.relative_vector_m,src.relative_vector_m)
    def test_23_forbidden_side_effects(self):
        s=inspect.getsource(__import__('passive_high_level_command_contract')).lower()
        for token in ('import serial','import socket','uart','lora','esp-now','esp_now','pwm','dshot','pid','mixer','esc output','motor','payload','release','weapon'): self.assertNotIn(token,s)
    def test_24_target_xyz_cannot_generate_movement(self):
        self.assertNotIn('target_xyz',m2.PassiveGuidanceDecision.__dataclass_fields__)
        d=tr(gd(m2.GuidanceIntent.MAINTAIN_OBSERVATION)); self.assertNotIn(d.command_type,(CommandType.MOVE_RELATIVE,CommandType.SET_ALTITUDE,CommandType.SET_HEADING))
    def test_25_wrong_contract_version(self):
        x=gd(); x=m2.PassiveGuidanceDecision(x.state,x.intent,x.target_ref,x.source_timestamp,x.frame_ref,x.metric_status,x.source_mission_state,x.source_mission_action,x.source_mission_reason,x.relative_vector_m,x.altitude_m,x.heading_deg,x.reason,x.provenance,False,'OTHER'); self.assertEqual(tr(x).state,CommandState.SUPPRESSED)
    def test_26_authoritative_m2_rejected(self):
        x=gd(); x=m2.PassiveGuidanceDecision(x.state,x.intent,x.target_ref,x.source_timestamp,x.frame_ref,x.metric_status,x.source_mission_state,x.source_mission_action,x.source_mission_reason,x.relative_vector_m,x.altitude_m,x.heading_deg,x.reason,x.provenance,True,'M2_SHADOW_V1'); self.assertEqual(tr(x).state,CommandState.SUPPRESSED)
    def test_27_reserved_operational_commands_not_in_m3_vocabulary(self):
        for name in ('ARM','DISARM','TAKEOFF','LAND'): self.assertNotIn(name,CommandType.__members__)

if __name__=='__main__': unittest.main()
