#pragma once
#include <cstdint>
namespace tangra::fc {
struct VerticalObservation { double altitude_m=0; double vertical_speed_mps=0; std::uint64_t timestamp_ms=0; bool valid=false; };
struct VerticalState { double z_m=0; double vz_mps=0; std::uint64_t timestamp_ms=0; bool valid=false; bool fresh=false; };
class VerticalStateProducer {
public: explicit VerticalStateProducer(std::uint64_t max_age_ms=250):max_age_ms_(max_age_ms){}
    VerticalState produce(const VerticalObservation& observation,std::uint64_t now_ms) const;
private: std::uint64_t max_age_ms_;
};
struct AltitudeTarget { double altitude_m=0; double vertical_speed_mps=0; bool use_altitude=true; bool valid=false; };
struct VerticalControlLimits { double max_climb_mps=2.0; double max_descent_mps=1.5; double max_collective_delta=0.35; double kp_altitude=0.8; double kp_velocity=0.25; };
struct VerticalControlOutput { double vertical_speed_target_mps=0; double collective_delta=0; bool valid=false; bool safe_fallback=true; };
class VerticalController {
public: explicit VerticalController(VerticalControlLimits limits={}):limits_(limits){}
 VerticalControlOutput update(const VerticalState& state,const AltitudeTarget& target) const;
private: VerticalControlLimits limits_;
};
}
