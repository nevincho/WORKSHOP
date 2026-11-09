#include "tangra_fc/local_navigation_state.hpp"
#include <cmath>
namespace tangra::fc {
LocalNavigationState LocalStateProducer::produce(const LocalKinematicObservation&o,const LocalOrigin&origin,const StateUncertainty&u,std::uint64_t now)const{
 LocalNavigationState s{};s.x=o.x;s.y=o.y;s.z=o.z;s.vx=o.vx;s.vy=o.vy;s.vz=o.vz;s.timestamp_ms=o.timestamp_ms;s.origin=origin;s.uncertainty=u;
 bool finite=std::isfinite(o.x)&&std::isfinite(o.y)&&std::isfinite(o.z)&&std::isfinite(o.vx)&&std::isfinite(o.vy)&&std::isfinite(o.vz);
 s.fresh=now>=o.timestamp_ms&&(now-o.timestamp_ms)<=max_age_ms_;s.valid=o.valid&&finite&&origin.valid;
 if(!s.valid)s.health=NavHealth::Invalid;else if(!s.fresh||!u.valid)s.health=NavHealth::Degraded;else s.health=NavHealth::Healthy;return s;
}
LocalNavigationState LocalStateValidator::evaluate(LocalNavigationState s,std::uint64_t now)const{
 bool finite=std::isfinite(s.x)&&std::isfinite(s.y)&&std::isfinite(s.z)&&std::isfinite(s.vx)&&std::isfinite(s.vy)&&std::isfinite(s.vz);
 s.fresh=now>=s.timestamp_ms&&(now-s.timestamp_ms)<=max_age_ms_;s.valid=s.valid&&finite&&s.origin.valid;
 if(!s.valid)s.health=NavHealth::Invalid;else if(!s.fresh||!s.uncertainty.valid)s.health=NavHealth::Degraded;else s.health=NavHealth::Healthy;return s;
}
}
