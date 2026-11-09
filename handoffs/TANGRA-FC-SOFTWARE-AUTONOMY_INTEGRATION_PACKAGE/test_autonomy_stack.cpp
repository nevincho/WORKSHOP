#include "tangra_fc/mission_lifecycle_v1.hpp"
#include "tangra_fc/command_arbitration.hpp"
#include "tangra_fc/quadx_simulation.hpp"
#include "tangra_fc/vertical_control.hpp"
#include "tangra_fc/local_navigation_state.hpp"
#include "tangra_fc/horizontal_guidance.hpp"
#include "tangra_fc/waypoint_executor.hpp"
#include "tangra_fc/mission_protocol.hpp"
#include "tangra_fc/parameters.hpp"
#include "tangra_fc/watchdog.hpp"
#include "tangra_fc/navigation_observations.hpp"
#include "tangra_fc/mission_planner_adapter.hpp"
#include <cassert>
#include <cmath>
#include <iostream>
#include <optional>
using namespace tangra::fc;
using namespace tangra::fc::sim;

struct SimLifecycle final:IMissionLifecycleV1{MissionLifecycleStateV1 s=MissionLifecycleStateV1::READY;MissionLifecycleReasonV1 reason=MissionLifecycleReasonV1::NONE;MissionLifecycleStateV1 state()const override{return s;}bool request(MissionLifecycleStateV1 n,MissionLifecycleReasonV1 r)override{s=n;reason=r;return true;}};
struct SimMissionSink final:IMissionCommandSink{WaypointExecutor&executor;explicit SimMissionSink(WaypointExecutor&e):executor(e){}bool accept_goal(const MissionGoalCommand&c)override{return executor.load({{c.x,c.y,c.z,.20,20000,true}});}};
struct SimStorage final:IParameterStorage{std::optional<std::string>bytes;bool save(const std::string&s)override{bytes=s;return true;}std::optional<std::string>load()override{return bytes;}};
struct SimWatchdogHw final:IWatchdogHardware{int feeds=0;void feed()override{++feeds;}ResetReason reset_reason()const override{return ResetReason::PowerOn;}};
struct SimControllerFixture final:IControllerAdapter{ControlSetpoint desired{};void set(ControlSetpoint s){desired=s;}AxisDemand update(const AttitudeState&state,double)override{const double tr=.35*desired.roll,tp=.35*desired.pitch;AxisDemand d{};d.roll=1.8*(tr-state.roll)-.45*state.p;d.pitch=1.8*(tp-state.pitch)-.45*state.q;d.yaw=-.25*state.r;d.collective=desired.collective;return d;}};
struct SimMixerFixture final:IMixerAdapter{MotorMix mix(const AxisDemand&d)override{MotorMix m;double c=d.collective;m.motor={c-d.roll-d.pitch+d.yaw,c+d.roll-d.pitch-d.yaw,c+d.roll+d.pitch+d.yaw,c-d.roll+d.pitch-d.yaw};return m;}};
struct SimEstimatorFixture final:IEstimatorAdapter{AttitudeState last{};AttitudeState update(const SensorSample&s,double)override{if(s.valid)last=s.attitude;return last;}};

static MissionStateWire wire_state(MissionLifecycleStateV1 s){switch(s){case MissionLifecycleStateV1::INIT:return MissionStateWire::INIT;case MissionLifecycleStateV1::READY:return MissionStateWire::READY;case MissionLifecycleStateV1::ACTIVE:return MissionStateWire::ACTIVE;case MissionLifecycleStateV1::HOLD:return MissionStateWire::HOLD;case MissionLifecycleStateV1::ABORT:return MissionStateWire::ABORT;case MissionLifecycleStateV1::COMPLETE:return MissionStateWire::COMPLETE;case MissionLifecycleStateV1::FAULT:return MissionStateWire::FAULT;}return MissionStateWire::FAULT;}

int main(){
 ParameterStore params(1,{{"max_speed",1.2,.2,3.0},{"max_tilt",.35,.1,.6},{"kp_position",.9,.1,2.0},{"kp_velocity",.35,.05,1.0},{"kp_altitude",.9,.1,2.0},{"kp_vertical",.35,.05,1.0}});
 assert(params.set("max_speed",1.0));SimStorage storage;assert(params.persist(storage,"standalone-sim"));
 ParameterStore loaded(1,{{"max_speed",1.2,.2,3.0},{"max_tilt",.35,.1,.6},{"kp_position",.9,.1,2.0},{"kp_velocity",.35,.05,1.0},{"kp_altitude",.9,.1,2.0},{"kp_vertical",.35,.05,1.0}});assert(loaded.restore(storage));
 GuidanceLimits gl;gl.max_speed_mps=loaded.get("max_speed");gl.max_tilt_norm=loaded.get("max_tilt");gl.kp_position=loaded.get("kp_position");gl.kp_velocity=loaded.get("kp_velocity");HorizontalGuidance guidance(gl);
 VerticalControlLimits vl;vl.kp_altitude=loaded.get("kp_altitude");vl.kp_velocity=loaded.get("kp_vertical");VerticalController vertical(vl);

 MissionPlannerAdapter planner;auto imported=planner.import({{0,PlannerCommand::NavWaypoint,.6,.3,.4,.20,20000}});assert(imported.accepted);
 SimLifecycle lifecycle;WaypointExecutor executor(lifecycle);SimMissionSink sink(executor);MissionProtocolEndpoint endpoint(sink);
 MavlinkMissionDialectContract fixture_dialect{{42000,(std::uint8_t)MissionPayloadCodec::kGoalPayloadLength,17},{42001,(std::uint8_t)MissionPayloadCodec::kAckPayloadLength,91},{42002,(std::uint8_t)MissionPayloadCodec::kTelemetryPayloadLength,203}};
 MavlinkMissionPayloadAdapter mav(fixture_dialect);
 MissionGoalCommand goal;goal.sequence=1;goal.timestamp_ms=0;goal.ttl_ms=1000;goal.x=imported.waypoints[0].x;goal.y=imported.waypoints[0].y;goal.z=imported.waypoints[0].z;
 auto goal_env=mav.encode_goal(goal);assert(goal_env);auto decoded=mav.decode_goal(*goal_env);assert(decoded.status==MavlinkAdapterStatus::Ok&&decoded.value);
 auto ack=endpoint.receive(*decoded.value,0,wire_state(lifecycle.state()));assert(ack.status==ProtocolStatus::Accepted);executor.start(0);

 CommandArbitrator arbitration;SimControllerFixture controller;SimMixerFixture mixer;SimEstimatorFixture estimator;ClosedLoopHarness plant(controller,mixer,estimator,{});
 VerticalStateProducer vertical_producer(100,1,500);LocalStateProducer local_producer(100,1,500,20.0);StateUncertainty uncertainty{.05,.05,true};
 NavigationObservationIntegrator nav_obs(100);GnssObservation gnss_origin{51.0,-1.0,100.0,.5,.8,0,true};assert(nav_obs.establish_origin(gnss_origin));
 GeodeticObservation origin_obs{51.0,-1.0,100.0,0,true};assert(local_producer.establish_origin(origin_obs));
 SimWatchdogHw watchdog_hw;WatchdogSupervisor watchdog(150);watchdog.initialize(0,watchdog_hw);
 constexpr double earth=6378137.0,pi=3.14159265358979323846;const double lat0=51.0*pi/180.0;std::uint64_t now_ms=0,seq=1;ClosedLoopResult plant_result{};bool completed=false;
 for(int i=0;i<5000&&!completed;i++){
  now_ms+=10;const auto&truth=plant_result.truth;double lat=51.0+(truth.y/earth)*(180.0/pi);double lon=-1.0+(truth.x/(earth*std::cos(lat0)))*(180.0/pi);
  GnssObservation g{lat,lon,100.0+truth.z,.05,.08,now_ms,true};HeadingObservation h{truth.attitude.yaw,.02,now_ms,true};auto nav=nav_obs.update(&g,&h,now_ms);assert(nav.position_valid&&nav.heading_valid&&nav.fresh);
  auto local=local_producer.update({lat,lon,100.0+truth.z,now_ms,true},uncertainty,now_ms);auto vs=vertical_producer.update({100.0+truth.z,now_ms,true},now_ms);
  if(!local.velocity_valid||!vs.velocity_valid){plant_result=plant.run_steps(1,10000);watchdog.heartbeat(now_ms,watchdog_hw);continue;}
  auto hs=guidance.update({local.x,local.y,local.vx,local.vy,local.valid,local.fresh},{goal.x,goal.y,true});auto vo=vertical.update(vs,{goal.z+100.0,0,true,true});assert(hs.valid&&vo.valid);
  SourceCommand autonomy{};autonomy.source=CommandSource::SimulatedAutonomy;autonomy.sequence=seq++;autonomy.timestamp_ms=now_ms;autonomy.ttl_ms=50;autonomy.valid=true;autonomy.setpoint.roll=(float)hs.roll_norm;autonomy.setpoint.pitch=(float)hs.pitch_norm;autonomy.setpoint.collective=(float)(.5+vo.collective_delta);assert(arbitration.submit(autonomy)==SubmitStatus::Accepted);
  auto selected=arbitration.select(now_ms);assert(selected.selected_source==CommandSource::SimulatedAutonomy&&!selected.safe_fallback);controller.set(selected.setpoint);
  plant_result=plant.run_steps(1,10000);watchdog.heartbeat(now_ms,watchdog_hw);assert(!watchdog.evaluate(now_ms).expired);
  auto status=executor.update({plant_result.truth.x,plant_result.truth.y,plant_result.truth.z,now_ms,true,true});if(lifecycle.state()==MissionLifecycleStateV1::COMPLETE){assert(status.progress==1.0);completed=true;}
 }
 assert(completed);
 auto telem=endpoint.telemetry(wire_state(lifecycle.state()),executor.status().progress,MissionFault::None);auto telem_env=mav.encode_telemetry(telem);assert(telem_env);auto telem_rx=mav.decode_telemetry(*telem_env);assert(telem_rx.status==MavlinkAdapterStatus::Ok&&telem_rx.value->mission_state==MissionStateWire::COMPLETE);
 auto wd=watchdog.evaluate(now_ms+500);assert(wd.expired&&wd.recovery==RecoveryState::SafeHold);
 std::cout<<"STANDALONE_SIM_PASS\nREAL_FC_INTEGRATION_NOT_TESTED\nTRANSPORT_ADAPTER_REQUIRED\n";
}
