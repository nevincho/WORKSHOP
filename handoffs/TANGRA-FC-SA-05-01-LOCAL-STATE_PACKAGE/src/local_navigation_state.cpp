#include "tangra_fc/local_navigation_state.hpp"
#include <cmath>
namespace tangra::fc {
LocalNavigationState LocalStateValidator::evaluate(LocalNavigationState s,std::uint64_t now) const{
 bool finite=std::isfinite(s.x)&&std::isfinite(s.y)&&std::isfinite(s.z)&&std::isfinite(s.vx)&&std::isfinite(s.vy)&&std::isfinite(s.vz);
 s.fresh = now>=s.timestamp_ms && (now-s.timestamp_ms)<=max_age_ms_;
 s.valid = s.valid && finite && s.origin.valid;
 if(!s.valid) s.health=NavHealth::Invalid; else if(!s.fresh||!s.uncertainty.valid) s.health=NavHealth::Degraded; else s.health=NavHealth::Healthy;
 return s;
}
}
