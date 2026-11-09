#pragma once
#include <cstdint>
namespace tangra::fc {
enum class MissionLifecycleStateV1 : std::uint8_t { INIT, READY, ACTIVE, HOLD, ABORT, COMPLETE, FAULT };
enum class MissionLifecycleReasonV1 : std::uint8_t {
    NONE, INVALID_GOAL, TIMEOUT, HOLD_REQUESTED, ABORT_REQUESTED, ARRIVED,
    SEQUENCE_COMPLETE, COMMUNICATION_LOSS, SAFETY_OVERRIDE
};
class IMissionLifecycleV1 {
public:
    virtual ~IMissionLifecycleV1() = default;
    virtual MissionLifecycleStateV1 state() const = 0;
    virtual bool request(MissionLifecycleStateV1 next, MissionLifecycleReasonV1 reason) = 0;
};
}
