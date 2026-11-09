#include "tangra_fc/waypoint_executor.hpp"
#include <cassert>
#include <iostream>
using namespace tangra::fc;
struct Lifecycle final:IMissionLifecyclePort{MissionLifecycleState s=MissionLifecycleState::READY;MissionLifecycleState state()const override{return s;}bool request(MissionLifecycleState n,MissionReason)override{s=n;return true;}};
int main(){Lifecycle l;WaypointExecutor e(l);assert(e.load({{1,0,0,0.2,1000,true},{2,0,0,0.2,1000,true}}));e.start(0);assert(l.s==MissionLifecycleState::ACTIVE);auto s=e.update({1,0,0,100,true,true});assert(s.active_index==1);s=e.update({2,0,0,200,true,true});assert(l.s==MissionLifecycleState::COMPLETE);assert(s.progress==1.0);Lifecycle l2;WaypointExecutor e2(l2);assert(e2.load({{5,0,0,0.1,10,true}}));e2.start(0);e2.update({0,0,0,20,true,true});assert(l2.s==MissionLifecycleState::ABORT);Lifecycle l3;WaypointExecutor e3(l3);assert(e3.load({{1,1,1,0.2,100,true}}));e3.start(0);e3.hold();assert(l3.s==MissionLifecycleState::HOLD);std::cout<<"PASS: waypoint executor reuses lifecycle port\n";}
