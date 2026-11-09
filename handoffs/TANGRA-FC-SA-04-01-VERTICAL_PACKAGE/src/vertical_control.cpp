#include "tangra_fc/vertical_control.hpp"
#include <algorithm>
#include <cmath>
namespace tangra::fc {
namespace { double clamp(double v,double lo,double hi){return std::max(lo,std::min(hi,v));}}
VerticalState VerticalStateProducer::produce(const VerticalObservation&o,std::uint64_t now)const{
 VerticalState s{};s.z_m=o.altitude_m;s.vz_mps=o.vertical_speed_mps;s.timestamp_ms=o.timestamp_ms;
 bool finite=std::isfinite(o.altitude_m)&&std::isfinite(o.vertical_speed_mps);
 s.fresh=now>=o.timestamp_ms&&(now-o.timestamp_ms)<=max_age_ms_;s.valid=o.valid&&finite;return s;
}
VerticalControlOutput VerticalController::update(const VerticalState&s,const AltitudeTarget&t)const{
 VerticalControlOutput o{};if(!s.valid||!s.fresh||!t.valid||!std::isfinite(s.z_m)||!std::isfinite(s.vz_mps)||!std::isfinite(t.altitude_m)||!std::isfinite(t.vertical_speed_mps))return o;
 double vz=t.vertical_speed_mps;if(t.use_altitude)vz+=limits_.kp_altitude*(t.altitude_m-s.z_m);
 vz=clamp(vz,-limits_.max_descent_mps,limits_.max_climb_mps);
 double delta=clamp(limits_.kp_velocity*(vz-s.vz_mps),-limits_.max_collective_delta,limits_.max_collective_delta);
 o.vertical_speed_target_mps=vz;o.collective_delta=delta;o.valid=true;o.safe_fallback=false;return o;
}
}
