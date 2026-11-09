#include "tangra_fc/waypoint_executor.hpp"
#include <cassert>
#include <iostream>
using namespace tangra::fc;
struct Lifecycle final:IMissionLifecycleV1{MissionLifecycleStateV1 s=MissionLifecycleStateV1::READY;MissionLifecycleStateV1 state()const override{return s;}bool request(MissionLifecycleStateV1 n,MissionLifecycleReasonV1)override{s=n;return true;}};
int main(){Lifecycle l;WaypointExecutor e(l);assert(e.load({{1,0,0,.2,1000,true}}));e.start(0);assert(l.s==MissionLifecycleStateV1::ACTIVE);auto s=e.update({1,0,0,100,true,true});assert(l.s==MissionLifecycleStateV1::COMPLETE&&s.progress==1.0);std::cout<<"PASS: waypoint executor shared lifecycle contract\n";}
