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

struct Lifecycle final:IMissionLifecycleV1{MissionLifecycleStateV1 s=MissionLifecycleStateV1::READY;MissionLifecycleReasonV1 reason=MissionLifecycleReasonV1::NONE;MissionLifecycleStateV1 state()const override{return s;}bool request(MissionLifecycleStateV1 n,MissionLifecycleReasonV1 r)override{s=n;reason=r;return true;}};
struct Sink final:IMissionCommandSink{WaypointExecutor&executor;explicit Sink(WaypointExecutor&e):executor(e){}bool accept_goal(const MissionGoalCommand&c)override{return executor.load({{c.x,c.y,c.z,.20,20000,true}});}};
struct MemStorage final:IParameterStorage{std::optional<std::string>bytes;bool save(const std::string&s)override{bytes=s;return true;}std::optional<std::string>load()override{return bytes;}};
struct WatchdogHw final:IWatchdogHardware{int feeds=0;void feed()override{++feeds;}ResetReason reset_reason()const override{return ResetReason::PowerOn;}};
struct ExternalSetpointController final:IControllerAdapter{ControlSetpoint desired{};void set(ControlSetpoint s){desired=s;}AxisDemand update(const AttitudeState&state,double)override{const double tr=.35*desired.roll,tp=.35*desired.pitch;AxisDemand d{};d.roll=1.8*(tr-state.roll)-.45*state.p;d.pitch=1.8*(tp-state.pitch)-.45*state.q;d.yaw=-.25*state.r;d.collective=desired.collective;return d;}};
struct QuadMixer final:IMixerAdapter{MotorMix mix(const AxisDemand&d)override{MotorMix m;double c=d.collective;m.motor={c-d.roll-d.pitch+d.yaw,c+d.roll-d.pitch-d.yaw,c+d.roll+d.pitch+d.yaw,c-d.roll+d.pitch-d.yaw};return m;}};
struct PerfectEstimator final:IEstimatorAdapter{AttitudeState last{};AttitudeState update(const SensorSample&s,double)override{if(s.valid)last=s.attitude;return last;}};

static MissionStateWire wire_state(MissionLifecycleStateV1 s){switch(s){case MissionLifecycleStateV1::INIT:return MissionStateWire::INIT;case MissionLifecycleStateV1::READY:return MissionStateWire::READY;case MissionLifecycleStateV1::ACTIVE:return MissionStateWire::ACTIVE;case MissionLifecycleStateV1::HOLD:return MissionStateWire::HOLD;case MissionLifecycleStateV1::ABORT:return MissionStateWire::ABORT;case MissionLifecycleStateV1::COMPLETE:return MissionStateWire::COMPLETE;case MissionLifecycleStateV1::FAULT:return MissionStateWire::FAULT;}return MissionStateWire::FAULT;}

int main(){
 ParameterStore params(1,{{"max_speed",1.2,.2,3.0},{"max_tilt",.35,.1,.6},{"kp_position",.9,.1,2.0},{"kp_velocity",.35,.05,1.0},{"kp_altitude",.9,.1,2.0},{"kp_vertical",.35,.05,1.0}});
 assert(params.set("max_speed",1.0));MemStorage storage;assert(params.persist(storage,"e2e-qualified"));
 ParameterStore loaded(1,{{"max_speed",1.2,.2,3.0},{"max_tilt",.35,.1,.6},{"kp_position",.9,.1,2.0},{"kp_velocity",.35,.05,1.0},{"kp_altitude",.9,.1,2.0},{"kp_vertical",.35,.05,1.0}});assert(loaded.restore(storage));
 GuidanceLimits gl;gl.max_speed_mps=loaded.get("max_speed");gl.max_tilt_norm=loaded.get("max_tilt");gl.kp_position=loaded.get("kp_position");gl.kp_velocity=loaded.get("kp_velocity");HorizontalGuidance guidance(gl);
 VerticalControlLimits vl;vl.kp_altitude=loaded.get("kp_altitude");vl.kp_velocity=loaded.get("kp_vertical");VerticalController vertical(vl);

 MissionPlannerAdapter planner;auto imported=planner.import({{0,PlannerCommand::NavWaypoint,1.0,.6,.8,.20,20000}});assert(imported.accepted&&imported.waypoints.size()==1);
 Lifecycle lifecycle;WaypointExecutor executor(lifecycle);Sink sink(executor);MissionProtocolEndpoint endpoint(sink);MavlinkMissionBinding mav({42000,42001,42002});assert(mav.configured());
 MissionGoalCommand goal;goal.sequence=1;goal.timestamp_ms=0;goal.ttl_ms=1000;goal.x=imported.waypoints[0].x;goal.y=imported.waypoints[0].y;goal.z=imported.waypoints[0].z;
 auto goal_frame=mav.encode_goal(goal);assert(goal_frame);auto decoded_goal=mav.decode_goal(*goal_frame);assert(decoded_goal);auto ack=endpoint.receive(*decoded_goal,0,wire_state(lifecycle.state()));assert(ack.status==ProtocolStatus::Accepted);auto ack_frame=mav.encode_ack(ack);assert(ack_frame&&mav.decode_ack(*ack_frame));executor.start(0);assert(lifecycle.state()==MissionLifecycleStateV1::ACTIVE);

 CommandArbitrator arbitration;SourceCommand replay{};replay.source=CommandSource::PiSupervisor;replay.sequence=10;replay.timestamp_ms=0;replay.ttl_ms=100;replay.valid=true;replay.setpoint.roll=.1f;assert(arbitration.submit(replay)==SubmitStatus::Accepted);replay.setpoint.roll=.9f;assert(arbitration.submit(replay)==SubmitStatus::DuplicateSequence);arbitration.clear_all();

 ExternalSetpointController controller;QuadMixer mixer;PerfectEstimator estimator;ClosedLoopHarness plant(controller,mixer,estimator,{});
 VerticalStateProducer vertical_producer(100);LocalStateProducer local_producer(100);LocalOrigin local_origin;local_origin.valid=true;local_origin.lat_deg=51.0;local_origin.lon_deg=-1.0;local_origin.alt_m=100.0;StateUncertainty uncertainty{.05,.05,true};
 NavigationObservationIntegrator nav_obs(100);GnssObservation gnss_origin{51.0,-1.0,100.0,.5,.8,0,true};assert(nav_obs.establish_origin(gnss_origin));
 WatchdogHw watchdog_hw;WatchdogSupervisor watchdog(150);watchdog.initialize(0,watchdog_hw);

 constexpr double earth=6378137.0,pi=3.14159265358979323846;const double lat0=51.0*pi/180.0;std::uint64_t now_ms=0,seq=1;ClosedLoopResult plant_result{};bool completed=false;
 for(int i=0;i<4000&&!completed;i++){
  now_ms+=10;const auto&truth=plant_result.truth;
  GnssObservation g{};g.lat_deg=51.0+(truth.y/earth)*(180.0/pi);g.lon_deg=-1.0+(truth.x/(earth*std::cos(lat0)))*(180.0/pi);g.alt_m=100.0+truth.z;g.horizontal_sigma_m=.05;g.vertical_sigma_m=.08;g.timestamp_ms=now_ms;g.valid=true;
  HeadingObservation h{truth.attitude.yaw,.02,now_ms,true};auto nav=nav_obs.update(&g,&h,now_ms);assert(nav.position_valid&&nav.heading_valid&&nav.fresh);
  auto local=local_producer.produce({nav.x,nav.y,nav.z,truth.vx,truth.vy,truth.vz,now_ms,true},local_origin,uncertainty,now_ms);assert(local.valid&&local.fresh&&local.health==NavHealth::Healthy);
  auto vs=vertical_producer.produce({local.z,local.vz,now_ms,true},now_ms);
  auto hs=guidance.update({local.x,local.y,local.vx,local.vy,local.valid,local.fresh},{goal.x,goal.y,true});auto vo=vertical.update(vs,{goal.z,0,true,true});assert(hs.valid&&vo.valid);
  SourceCommand autonomy{};autonomy.source=CommandSource::SimulatedAutonomy;autonomy.sequence=seq++;autonomy.timestamp_ms=now_ms;autonomy.ttl_ms=50;autonomy.valid=true;autonomy.setpoint.roll=static_cast<float>(hs.roll_norm);autonomy.setpoint.pitch=static_cast<float>(hs.pitch_norm);autonomy.setpoint.collective=static_cast<float>(.5+vo.collective_delta);assert(arbitration.submit(autonomy)==SubmitStatus::Accepted);
  auto selected=arbitration.select(now_ms);assert(selected.selected_source==CommandSource::SimulatedAutonomy&&!selected.safe_fallback);controller.set(selected.setpoint);
  plant_result=plant.run_steps(1,10000);watchdog.heartbeat(now_ms,watchdog_hw);assert(!watchdog.evaluate(now_ms).expired);
  auto status=executor.update({plant_result.truth.x,plant_result.truth.y,plant_result.truth.z,now_ms,true,true});if(lifecycle.state()==MissionLifecycleStateV1::COMPLETE){assert(status.progress==1.0);completed=true;}
 }
 if(!completed)std::cerr<<"final truth x="<<plant_result.truth.x<<" y="<<plant_result.truth.y<<" z="<<plant_result.truth.z<<"\n";assert(completed);
 auto telem=endpoint.telemetry(wire_state(lifecycle.state()),executor.status().progress,MissionFault::None);auto telem_frame=mav.encode_telemetry(telem);assert(telem_frame);auto telem_rx=mav.decode_telemetry(*telem_frame);assert(telem_rx&&telem_rx->mission_state==MissionStateWire::COMPLETE&&telem_rx->progress==1.0);
 auto wd=watchdog.evaluate(now_ms+500);assert(wd.expired&&wd.recovery==RecoveryState::SafeHold);SourceCommand safety{};safety.source=CommandSource::SafetyOverride;safety.sequence=1;safety.timestamp_ms=now_ms+500;safety.ttl_ms=100;safety.valid=true;safety.force_safe=true;assert(arbitration.submit(safety)==SubmitStatus::Accepted);auto safe=arbitration.select(now_ms+500);assert(safe.selected_source==CommandSource::SafetyOverride&&safe.safe_fallback);assert(safe.setpoint.roll==0.0f&&safe.setpoint.pitch==0.0f&&safe.setpoint.collective==0.0f);
 std::cout<<"PASS: STEP_2-12 actual closed-loop autonomy software chain\n";
}
