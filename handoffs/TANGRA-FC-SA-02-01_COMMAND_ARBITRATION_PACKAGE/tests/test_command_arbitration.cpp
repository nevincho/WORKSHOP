#include "tangra_fc/command_arbitration.hpp"
#include <cassert>
#include <cmath>
#include <iostream>

using namespace tangra::fc;

static SourceCommand cmd(CommandSource source, std::uint64_t seq, std::uint64_t ts,
                         std::uint32_t ttl, float roll = 0.1f) {
    SourceCommand c{};
    c.source = source;
    c.sequence = seq;
    c.timestamp_ms = ts;
    c.ttl_ms = ttl;
    c.valid = true;
    c.setpoint.roll = roll;
    return c;
}

int main() {
    CommandArbitrator a;

    auto d = a.select(100);
    assert(d.safe_fallback && d.selected_source == CommandSource::None);

    a.submit(cmd(CommandSource::SimulatedAutonomy, 1, 100, 50, 0.2f));
    d = a.select(120);
    assert(!d.safe_fallback && d.selected_source == CommandSource::SimulatedAutonomy);

    a.submit(cmd(CommandSource::PiSupervisor, 1, 110, 50, 0.3f));
    d = a.select(120);
    assert(d.selected_source == CommandSource::PiSupervisor);

    a.submit(cmd(CommandSource::BenchTest, 1, 115, 50, 0.4f));
    d = a.select(120);
    assert(d.selected_source == CommandSource::BenchTest);

    auto safety = cmd(CommandSource::SafetyOverride, 1, 119, 50, 0.9f);
    safety.force_safe = true;
    a.submit(safety);
    d = a.select(120);
    assert(d.selected_source == CommandSource::SafetyOverride);
    assert(d.safe_fallback);
    assert(d.reason == ArbitrationReason::SafetyOverride);
    assert(d.setpoint.collective == 0.0f);

    a.clear(CommandSource::SafetyOverride);
    d = a.select(200);
    assert(d.safe_fallback && d.selected_source == CommandSource::None);
    assert(d.had_rejected_input);

    auto invalid = cmd(CommandSource::BenchTest, 2, 200, 20);
    invalid.valid = false;
    a.submit(invalid);
    d = a.select(205);
    assert(d.safe_fallback);

    auto nan_cmd = cmd(CommandSource::PiSupervisor, 2, 205, 20);
    nan_cmd.setpoint.roll = std::nanf("");
    a.submit(nan_cmd);
    d = a.select(210);
    assert(d.safe_fallback);

    a.clear_all();
    a.submit(cmd(CommandSource::PiSupervisor, 10, 300, 100, 5.0f));
    d = a.select(301);
    assert(d.selected_source == CommandSource::PiSupervisor);
    assert(std::fabs(d.setpoint.roll - 1.0f) < 1e-6f);

    a.submit(cmd(CommandSource::PiSupervisor, 9, 302, 100, -0.8f));
    d = a.select(303);
    assert(std::fabs(d.setpoint.roll - 1.0f) < 1e-6f);

    std::cout << "PASS: command arbitration deterministic contract\n";
    return 0;
}
