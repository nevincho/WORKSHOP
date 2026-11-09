#pragma once
#include <cstddef>
#include <cstdint>
#include <vector>

namespace tangra::fc {

enum class MissionLifecycleState : std::uint8_t { INIT, READY, ACTIVE, HOLD, ABORT, COMPLETE, FAULT };
enum class MissionReason : std::uint8_t { NONE, INVALID_GOAL, TIMEOUT, HOLD_REQUESTED, ABORT_REQUESTED, ARRIVED, SEQUENCE_COMPLETE };

class IMissionLifecyclePort {
public:
    virtual ~IMissionLifecyclePort() = default;
    virtual MissionLifecycleState state() const = 0;
    virtual bool request(MissionLifecycleState next, MissionReason reason) = 0;
};

struct Waypoint { double x=0,y=0,z=0; double acceptance_radius_m=0.5; std::uint32_t timeout_ms=30000; bool valid=true; };
struct ExecutorObservation { double x=0,y=0,z=0; std::uint64_t now_ms=0; bool valid=false; bool fresh=false; };
struct ExecutorStatus { std::size_t active_index=0; std::size_t count=0; double progress=0; MissionReason reason=MissionReason::NONE; bool has_active_goal=false; };

class WaypointExecutor {
public:
    explicit WaypointExecutor(IMissionLifecyclePort& lifecycle): lifecycle_(lifecycle) {}
    bool load(std::vector<Waypoint> goals);
    void start(std::uint64_t now_ms);
    ExecutorStatus update(const ExecutorObservation& obs);
    void hold();
    void abort();
    ExecutorStatus status() const;
private:
    IMissionLifecyclePort& lifecycle_;
    std::vector<Waypoint> goals_{};
    std::size_t index_=0;
    std::uint64_t goal_start_ms_=0;
    MissionReason reason_=MissionReason::NONE;
};

} // namespace tangra::fc
