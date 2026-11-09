#pragma once
#include <cstdint>
#include <vector>
namespace tangra::fc {
enum class PlannerCommand:std::uint16_t{NavWaypoint=16,Unsupported=65535};
struct MissionPlannerItem{std::uint16_t seq=0;PlannerCommand command=PlannerCommand::Unsupported;double x=0,y=0,z=0;double acceptance_radius_m=0.5;std::uint32_t timeout_ms=30000;};
struct TangraWaypoint{std::uint16_t sequence=0;double x=0,y=0,z=0;double acceptance_radius_m=0.5;std::uint32_t timeout_ms=30000;};
struct MissionImportResult{bool accepted=false;std::uint16_t rejected_sequence=0;std::vector<TangraWaypoint> waypoints;};
class MissionPlannerAdapter{public:MissionImportResult import(const std::vector<MissionPlannerItem>&items)const;};
}
