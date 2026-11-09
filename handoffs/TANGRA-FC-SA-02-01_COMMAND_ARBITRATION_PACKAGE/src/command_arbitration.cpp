#include "tangra_fc/command_arbitration.hpp"
#include <algorithm>
#include <cmath>
#include <stdexcept>

namespace tangra::fc {
namespace {

bool finite_setpoint(const ControlSetpoint& s) {
    return std::isfinite(s.roll) && std::isfinite(s.pitch) &&
           std::isfinite(s.yaw_rate) && std::isfinite(s.collective);
}

ControlSetpoint clamp_setpoint(ControlSetpoint s) {
    auto clamp = [](float v) { return std::max(-1.0f, std::min(1.0f, v)); };
    s.roll = clamp(s.roll);
    s.pitch = clamp(s.pitch);
    s.yaw_rate = clamp(s.yaw_rate);
    s.collective = clamp(s.collective);
    return s;
}

}  // namespace

std::size_t CommandArbitrator::index(CommandSource source) {
    switch (source) {
        case CommandSource::SimulatedAutonomy: return 0;
        case CommandSource::PiSupervisor: return 1;
        case CommandSource::BenchTest: return 2;
        case CommandSource::SafetyOverride: return 3;
        default: throw std::invalid_argument("CommandSource::None has no slot");
    }
}

int CommandArbitrator::priority(CommandSource source) {
    switch (source) {
        case CommandSource::SafetyOverride: return 400;
        case CommandSource::BenchTest: return 300;
        case CommandSource::PiSupervisor: return 200;
        case CommandSource::SimulatedAutonomy: return 100;
        case CommandSource::None: return 0;
    }
    return 0;
}

bool CommandArbitrator::eligible(const SourceCommand& command, std::uint64_t now_ms) {
    if (!command.valid || command.source == CommandSource::None) return false;
    if (!finite_setpoint(command.setpoint)) return false;
    if (command.ttl_ms == 0) return false;
    if (now_ms < command.timestamp_ms) return false;
    return (now_ms - command.timestamp_ms) <= command.ttl_ms;
}

ControlSetpoint CommandArbitrator::safe_setpoint() {
    return {};
}

void CommandArbitrator::submit(const SourceCommand& command) {
    if (command.source == CommandSource::None) return;
    auto& slot = slots_[index(command.source)];
    if (slot.source == command.source && command.sequence < slot.sequence) {
        return;
    }
    slot = command;
}

ArbitrationDecision CommandArbitrator::select(std::uint64_t now_ms) const {
    ArbitrationDecision decision{};
    const SourceCommand* best = nullptr;

    for (const auto& cmd : slots_) {
        if (cmd.source == CommandSource::None) continue;
        if (!eligible(cmd, now_ms)) {
            decision.had_rejected_input = true;
            continue;
        }
        if (cmd.source == CommandSource::SafetyOverride && cmd.force_safe) {
            decision.selected_source = CommandSource::SafetyOverride;
            decision.reason = ArbitrationReason::SafetyOverride;
            decision.safe_fallback = true;
            decision.setpoint = safe_setpoint();
            return decision;
        }
        if (best == nullptr || priority(cmd.source) > priority(best->source)) {
            best = &cmd;
        }
    }

    if (best == nullptr) {
        decision.selected_source = CommandSource::None;
        decision.reason = ArbitrationReason::NoEligibleSource;
        decision.safe_fallback = true;
        decision.setpoint = safe_setpoint();
        return decision;
    }

    decision.selected_source = best->source;
    decision.reason = ArbitrationReason::Selected;
    decision.safe_fallback = false;
    decision.setpoint = clamp_setpoint(best->setpoint);
    return decision;
}

void CommandArbitrator::clear(CommandSource source) {
    if (source == CommandSource::None) return;
    slots_[index(source)] = {};
}

void CommandArbitrator::clear_all() {
    for (auto& slot : slots_) slot = {};
}

}  // namespace tangra::fc
