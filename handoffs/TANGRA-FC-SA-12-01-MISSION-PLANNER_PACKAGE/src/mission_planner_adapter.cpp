#include "tangra_fc/mission_planner_adapter.hpp"
#include <cmath>
namespace tangra::fc {
MissionImportResult MissionPlannerAdapter::import(const std::vector<MissionPlannerItem>&items)const{MissionImportResult r;std::uint16_t expected=0;for(const auto&i:items){if(i.seq!=expected||i.command!=PlannerCommand::NavWaypoint||!std::isfinite(i.x)||!std::isfinite(i.y)||!std::isfinite(i.z)||i.acceptance_radius_m<=0||i.timeout_ms==0){r.rejected_sequence=i.seq;return r;}r.waypoints.push_back({i.seq,i.x,i.y,i.z,i.acceptance_radius_m,i.timeout_ms});++expected;}r.accepted=!r.waypoints.empty();return r;}
}
