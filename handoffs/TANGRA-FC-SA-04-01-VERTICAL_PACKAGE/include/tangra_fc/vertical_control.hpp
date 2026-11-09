#pragma once
#include <cstdint>
namespace tangra::fc {
struct AltitudeSample { double altitude_m=0.0; std::uint64_t timestamp_ms=0; bool valid=false; };
struct VerticalState { double z_m=0.0; double vz_mps=0.0; std::uint64_t timestamp_ms=0; bool valid=false; bool fresh=false; bool velocity_valid=false; };
class VerticalStateProducer {
public:
    VerticalStateProducer(std::uint64_t max_age_ms=250,std::uint64_t min_dt_ms=1,std::uint64_t max_dt_ms=1000)
        :max_age_ms_(max_age_ms),min_dt_ms_(min_dt_ms),max_dt_ms_(max_dt_ms){}
    VerticalState update(const AltitudeSample& sample,std::uint64_t now_ms);
    void reset();
    bool initialized() const { return initialized_; }
private:
    std::uint64_t max_age_ms_,min_dt_ms_,max_dt_ms_;
    bool initialized_=false;
    AltitudeSample previous_{};
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
