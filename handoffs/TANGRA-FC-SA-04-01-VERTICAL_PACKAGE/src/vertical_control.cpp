#include "tangra_fc/vertical_control.hpp"
#include <algorithm>
#include <cmath>
namespace tangra::fc {
namespace { double clamp(double v,double lo,double hi){return std::max(lo,std::min(hi,v));}}
VerticalControlOutput VerticalController::update(const VerticalState& s,const AltitudeTarget& t) const {
 VerticalControlOutput o{};
 if(!s.valid||!s.fresh||!t.valid||!std::isfinite(s.z_m)||!std::isfinite(s.vz_mps)||!std::isfinite(t.altitude_m)||!std::isfinite(t.vertical_speed_mps)) return o;
 double vz_target=t.vertical_speed_mps;
 if(t.use_altitude) vz_target += limits_.kp_altitude*(t.altitude_m-s.z_m);
 vz_target=clamp(vz_target,-limits_.max_descent_mps,limits_.max_climb_mps);
 double delta=limits_.kp_velocity*(vz_target-s.vz_mps);
 delta=clamp(delta,-limits_.max_collective_delta,limits_.max_collective_delta);
 o.vertical_speed_target_mps=vz_target; o.collective_delta=delta; o.valid=true; o.safe_fallback=false; return o;
}
}
