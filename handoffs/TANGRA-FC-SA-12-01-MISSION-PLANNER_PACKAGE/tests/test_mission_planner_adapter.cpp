#include "tangra_fc/mission_planner_adapter.hpp"
#include <cassert>
#include <iostream>
using namespace tangra::fc;
int main(){MissionPlannerAdapter a;std::vector<MissionPlannerItem>items={{0,PlannerCommand::NavWaypoint,1,2,3,0.5,1000},{1,PlannerCommand::NavWaypoint,4,5,6,0.5,1000}};auto r=a.import(items);assert(r.accepted&&r.waypoints.size()==2&&r.waypoints[1].x==4);items[1].command=PlannerCommand::Unsupported;r=a.import(items);assert(!r.accepted&&r.rejected_sequence==1);std::cout<<"PASS: Mission Planner compatibility adapter\n";}
