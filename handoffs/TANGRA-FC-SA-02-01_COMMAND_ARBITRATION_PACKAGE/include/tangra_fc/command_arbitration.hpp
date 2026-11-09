#pragma once
#include <array>
#include <cstdint>

namespace tangra::fc {

enum class CommandSource : std::uint8_t {
    None = 0,
    SimulatedAutonomy = 1,
    PiSupervisor = 2,
    BenchTest = 3,
    SafetyOverride = 4,
};

struct ControlSetpoint {
    float roll = 0.0f;
    float pitch = 0.0f;
    float yaw_rate = 0.0f;
    float collective = 0.0f;
};

struct SourceCommand {
    CommandSource source = CommandSource::None;
    std::uint64_t sequence = 0;
    std::uint64_t timestamp_ms = 0;
    std::uint32_t ttl_ms = 0;
    bool valid = false;
    bool force_safe = false;
    ControlSetpoint setpoint{};
};

enum class ArbitrationReason : std::uint8_t {
    Selected = 0,
    NoEligibleSource,
    SafetyOverride,
    Invalid,
    Stale,
};

struct ArbitrationDecision {
    CommandSource selected_source = CommandSource::None;
    ArbitrationReason reason = ArbitrationReason::NoEligibleSource;
    bool safe_fallback = true;
    bool had_rejected_input = false;
    ControlSetpoint setpoint{};
};

class CommandArbitrator {
public:
    static constexpr std::size_t kSourceCount = 4;

    void submit(const SourceCommand& command);
    ArbitrationDecision select(std::uint64_t now_ms) const;
    void clear(CommandSource source);
    void clear_all();

    static int priority(CommandSource source);
    static bool eligible(const SourceCommand& command, std::uint64_t now_ms);
    static ControlSetpoint safe_setpoint();

private:
    static std::size_t index(CommandSource source);
    std::array<SourceCommand, kSourceCount> slots_{};
};

}  // namespace tangra::fc
