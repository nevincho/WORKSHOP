#include "tangra_fc/command_arbitration.hpp"
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
#include <iostream>
#include <optional>
using namespace tangra::fc;

struct Lifecycle:IMissionLifecyclePort{MissionLifecycleState s=MissionLifecycleState::READY;MissionLifecycleState state()const override{return s;}bool request(MissionLifecycleState n,MissionReason)override{s=n;return true;}};
struct Sink:IMissionCommandSink{WaypointExecutor& ex; explicit Sink(WaypointExecutor& e):ex(e){} bool accept_goal(const MissionGoalCommand& c)override{return ex.load({{c.x,c.y,c.z,0.5,30000,true}});}};
struct Mem:IParameterStorage{std::optional<std::string>x;bool save(const std::string&s)override{x=s;return true;}std::optional<std::string>load()override{return x;}};
struct WH:IWatchdogHardware{int n=0;void feed()override{n++;}ResetReason reset_reason()const override{return ResetReason::PowerOn;}};

int main(){
  MissionPlannerAdapter mp; auto imported=mp.import({{0,PlannerCommand::NavWaypoint,2,0,3,0.5,30000}}); assert(imported.accepted);
  Lifecycle life; WaypointExecutor exec(life); Sink sink(exec); MissionProtocolEndpoint proto(sink);
  MissionGoalCommand cmd; cmd.sequence=1;cmd.timestamp_ms=100;cmd.ttl_ms=100;cmd.x=imported.waypoints[0].x;cmd.y=imported.waypoints[0].y;cmd.z=imported.waypoints[0].z;
  auto ack=proto.receive(cmd,120,MissionStateWire::READY); assert(ack.status==ProtocolStatus::Accepted); exec.start(120); assert(life.s==MissionLifecycleState::ACTIVE);

  LocalNavigationState ns; ns.x=0;ns.y=0;ns.z=0;ns.valid=true;ns.timestamp_ms=120;ns.origin.valid=true;ns.uncertainty.valid=true; LocalStateValidator lv(100);ns=lv.evaluate(ns,130);assert(ns.health==NavHealth::Healthy);
  HorizontalGuidance hg; auto gs=hg.update({ns.x,ns.y,ns.vx,ns.vy,ns.valid,ns.fresh},{cmd.x,cmd.y,true});assert(gs.valid);
  VerticalController vc;auto vo=vc.update({ns.z,ns.vz,130,true,true},{cmd.z,0,true,true});assert(vo.valid);

  CommandArbitrator arb;SourceCommand ac;ac.source=CommandSource::SimulatedAutonomy;ac.sequence=1;ac.timestamp_ms=130;ac.ttl_ms=100;ac.valid=true;ac.setpoint.roll=(float)gs.roll_norm;ac.setpoint.pitch=(float)gs.pitch_norm;ac.setpoint.collective=(float)vo.collective_delta;arb.submit(ac);auto ad=arb.select(140);assert(ad.selected_source==CommandSource::SimulatedAutonomy&&!ad.safe_fallback);

  NavigationObservationIntegrator ni(100);GnssObservation origin{51,-1,100,1,2,100,true};assert(ni.establish_origin(origin));GnssObservation g=origin;g.lat_deg+=0.00001;g.timestamp_ms=140;HeadingObservation h{1.0,0.1,140,true};auto nu=ni.update(&g,&h,150);assert(nu.position_valid&&nu.heading_valid);

  ParameterStore ps(1,{{"max_speed",5,0,10}});Mem mem;assert(ps.persist(mem,"integration"));ParameterStore ps2(1,{{"max_speed",5,0,10}});assert(ps2.restore(mem));
  WH wh;WatchdogSupervisor wd(100);wd.initialize(100,wh);wd.heartbeat(150,wh);assert(!wd.evaluate(200).expired);

  auto es=exec.update({cmd.x,cmd.y,cmd.z,200,true,true});assert(life.s==MissionLifecycleState::COMPLETE);assert(es.progress==1.0);
  std::cout<<"PASS: TANGRA FC standalone autonomy cross-module integration\n";
}
