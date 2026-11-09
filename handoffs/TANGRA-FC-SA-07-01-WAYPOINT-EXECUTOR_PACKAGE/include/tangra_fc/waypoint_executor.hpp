#pragma once
#include "tangra_fc/mission_lifecycle_v1.hpp"
#include <cstddef>
#include <cstdint>
#include <vector>
namespace tangra::fc {
struct Waypoint { double x=0,y=0,z=0; double acceptance_radius_m=0.5; std::uint32_t timeout_ms=30000; bool valid=true; };
struct ExecutorObservation { double x=0,y=0,z=0; std::uint64_t now_ms=0; bool valid=false; bool fresh=false; };
struct ExecutorStatus { std::size_t active_index=0; std::size_t count=0; double progress=0; MissionLifecycleReasonV1 reason=MissionLifecycleReasonV1::NONE; bool has_active_goal=false; };
class WaypointExecutor {
public:
 explicit WaypointExecutor(IMissionLifecycleV1& lifecycle):lifecycle_(lifecycle){}
 bool load(std::vector<Waypoint> goals); void start(std::uint64_t now_ms);
 ExecutorStatus update(const ExecutorObservation& obs); void hold(); void abort(); ExecutorStatus status()const;
private:
 IMissionLifecycleV1& lifecycle_;std::vector<Waypoint> goals_{};std::size_t index_=0;std::uint64_t goal_start_ms_=0;MissionLifecycleReasonV1 reason_=MissionLifecycleReasonV1::NONE;
};
}
